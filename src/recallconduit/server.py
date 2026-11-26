import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("RecallConduit")


@mcp.tool()
def list_notes() -> list[str]:
    """List up to 100 visible Markdown filenames at the configured vault root."""
    configured = os.environ.get("RECALLCONDUIT_VAULT")
    if not configured:
        raise ValueError("Set RECALLCONDUIT_VAULT to your vault directory")
    root = Path(configured).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Vault must be a directory")
    return sorted(
        p.name for p in root.iterdir()
        if not p.name.startswith(".") and p.suffix.lower() == ".md"
        and not p.is_symlink() and p.is_file()
    )[:100]


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
