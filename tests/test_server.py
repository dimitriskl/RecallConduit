import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import pytest

from recallconduit.server import list_notes


def test_list_notes(tmp_path, monkeypatch):
    monkeypatch.setenv("RECALLCONDUIT_VAULT", str(tmp_path))
    for name in ("b.md", "a.md", ".hidden.md", "image.png"):
        (tmp_path / name).touch()
    (tmp_path / "folder.md").mkdir()
    assert list_notes() == ["a.md", "b.md"]


def test_missing_config(monkeypatch):
    monkeypatch.delenv("RECALLCONDUIT_VAULT", raising=False)
    with pytest.raises(ValueError):
        list_notes()


def test_mcp(tmp_path):
    (tmp_path / "note.md").touch()
    async def run():
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "recallconduit.server"],
            env={**os.environ, "RECALLCONDUIT_VAULT": str(tmp_path)},
        )
        async with stdio_client(params) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                await session.initialize()
                tools = await session.list_tools()
                assert [tool.name for tool in tools.tools] == ["list_notes"]
                result = await session.call_tool("list_notes", {})
                assert not result.isError
                assert "note.md" in str(result.content)
    asyncio.run(asyncio.wait_for(run(), timeout=30))
