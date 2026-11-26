"""Bounded Markdown operations for a trusted local vault."""
from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path
from threading import RLock

MAX_BYTES = 256 * 1024
MAX_RESULTS = 50
MAX_SCAN = 10_000


class Vault:
    def __init__(self, root: str | Path, *, writable: bool = False):
        self.root = Path(root).expanduser().resolve(strict=True)
        if not self.root.is_dir():
            raise ValueError("Vault must be a directory")
        self.writable = writable
        self._lock = RLock()

    def _path(self, relative: str) -> Path:
        parts = relative.split("/")
        if (
            not relative or not relative.lower().endswith(".md")
            or any(not p or p.startswith(".") or p.endswith((".", " "))
                   or any(c in p for c in '\\:\x00<>|?*"') for p in parts)
        ):
            raise ValueError("Use a relative Markdown path without hidden components")
        path = self.root
        for part in parts:
            path = path / part
            if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
                raise ValueError("Links are not allowed")
        if not path.resolve().is_relative_to(self.root):
            raise ValueError("Path is outside vault")
        return path

    @staticmethod
    def _read(path: Path) -> bytes:
        if not path.is_file():
            raise ValueError("Note does not exist or is not a regular file")
        with path.open("rb") as handle:
            data = handle.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError("Note exceeds size limit")
        return data

    @staticmethod
    def _revision(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def read(self, relative: str) -> dict:
        with self._lock:
            data = self._read(self._path(relative))
            return {"path": relative, "content": data.decode("utf-8"),
                    "revision": self._revision(data)}

    def _notes(self):
        scanned = 0
        for folder, dirs, files in os.walk(self.root, followlinks=False):
            dirs[:] = sorted(d for d in dirs if not d.startswith(".")
                             and not (Path(folder) / d).is_symlink()
                             and not getattr(Path(folder) / d, "is_junction", lambda: False)())
            for filename in sorted(files):
                scanned += 1
                if scanned > MAX_SCAN:
                    return
                if filename.startswith(".") or not filename.lower().endswith(".md"):
                    continue
                relative = (Path(folder) / filename).relative_to(self.root).as_posix()
                try:
                    yield self.read(relative)
                except (OSError, ValueError):
                    continue

    def search(self, query: str, limit: int = 10) -> list[dict]:
        if not query.strip() or len(query) > 500:
            raise ValueError("Query must contain 1 to 500 characters")
        if not 1 <= limit <= MAX_RESULTS:
            raise ValueError("Limit must be between 1 and 50")
        needle = query.casefold()
        results = []
        for note in self._notes():
            content = note["content"]
            match = next((line for line in content.splitlines()
                          if needle in line.casefold()), None)
            if match is None and needle not in note["path"].casefold():
                continue
            results.append({"path": note["path"], "revision": note["revision"],
                            "snippet": (match or "")[:240]})
            if len(results) == limit:
                break
        return results

    def list(self, limit: int = 50) -> list[str]:
        if not 1 <= limit <= MAX_RESULTS:
            raise ValueError("Limit must be between 1 and 50")
        results = []
        for note in self._notes():
            results.append(note["path"])
            if len(results) == limit:
                break
        return results

    def _write(self, relative: str, content: str,
               expected_revision: str | None, *, append: bool = False) -> dict:
        if not self.writable:
            raise PermissionError("Vault writes are disabled")
        with self._lock:
            path = self._path(relative)
            if not path.parent.is_dir():
                raise ValueError("Parent folder must already exist")
            if expected_revision is None:
                if path.exists():
                    raise FileExistsError("Note already exists")
            else:
                old = self._read(path)
                if self._revision(old) != expected_revision:
                    raise ValueError("Revision conflict: re-read the note")
                if append:
                    content = old.decode("utf-8") + content
            data = content.encode("utf-8")
            if len(data) > MAX_BYTES:
                raise ValueError("Note exceeds size limit")
            fd, name = tempfile.mkstemp(prefix=".recallconduit-", dir=path.parent)
            temp = Path(name)
            try:
                with os.fdopen(fd, "wb") as handle:
                    handle.write(data)
                    handle.flush()
                    os.fsync(handle.fileno())
                if expected_revision is None:
                    # Atomic creation without replacing an existing note.
                    os.link(temp, path)
                else:
                    if self._revision(self._read(path)) != expected_revision:
                        raise ValueError("Revision conflict: re-read the note")
                    os.replace(temp, path)
            finally:
                temp.unlink(missing_ok=True)
            return {"path": relative, "revision": self._revision(data)}

    def create(self, relative: str, content: str) -> dict:
        return self._write(relative, content, None)

    def update(self, relative: str, content: str, expected_revision: str) -> dict:
        if not expected_revision:
            raise ValueError("Revision is required")
        return self._write(relative, content, expected_revision)

    def append(self, relative: str, content: str, expected_revision: str) -> dict:
        if not expected_revision:
            raise ValueError("Revision is required")
        return self._write(relative, content, expected_revision, append=True)
