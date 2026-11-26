import pytest

from recallconduit.vault import MAX_BYTES, Vault


@pytest.fixture
def vault(tmp_path):
    return Vault(tmp_path, writable=True)


def test_roundtrip(vault):
    initial = vault.create("test.md", "# Hello")
    assert vault.read("test.md")["content"] == "# Hello"
    updated = vault.update("test.md", "World", initial["revision"])
    vault.append("test.md", "\nAgain", updated["revision"])
    assert vault.read("test.md")["content"] == "World\nAgain"


def test_duplicate_and_stale(vault):
    first = vault.create("a.md", "one")
    with pytest.raises(FileExistsError):
        vault.create("a.md", "two")
    vault.update("a.md", "two", first["revision"])
    with pytest.raises(ValueError, match="Revision conflict"):
        vault.update("a.md", "three", first["revision"])
    assert vault.read("a.md")["content"] == "two"


@pytest.mark.parametrize("path", ["../out.md", "/out.md", ".obsidian/a.md",
                                   "C:/out.md", "folder\\a.md", "file.txt"])
def test_reject_paths(vault, path):
    with pytest.raises(ValueError):
        vault.create(path, "bad")


def test_read_only(tmp_path):
    with pytest.raises(PermissionError):
        Vault(tmp_path).create("a.md", "bad")


def test_search_and_list(vault):
    vault.create("python.md", "# Decorators\nPython example")
    vault.create("other.md", "Nothing")
    assert [r["path"] for r in vault.search("DECORATORS")] == ["python.md"]
    assert vault.list(1) == ["other.md"]


def test_size_limit(vault):
    with pytest.raises(ValueError, match="size limit"):
        vault.create("a.md", "x" * (MAX_BYTES + 1))


def test_symlink_rejected(vault, tmp_path):
    target = tmp_path / "target.md"
    target.write_text("private")
    try:
        (tmp_path / "link.md").symlink_to(target)
    except OSError:
        pytest.skip("Symlinks not supported")
    with pytest.raises(ValueError, match="Links"):
        vault.read("link.md")


def test_external_change(vault):
    first = vault.create("a.md", "one")
    (vault.root / "a.md").write_text("external")
    with pytest.raises(ValueError, match="Revision conflict"):
        vault.append("a.md", "more", first["revision"])
