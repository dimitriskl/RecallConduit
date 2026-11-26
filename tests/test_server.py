import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def test_stdio(tmp_path):
    async def run():
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "recallconduit.server"],
            env={**os.environ, "RECALLCONDUIT_VAULT": str(tmp_path),
                 "RECALLCONDUIT_WRITE": "1"},
        )
        async with stdio_client(params) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                await session.initialize()
                tools = await session.list_tools()
                assert {tool.name for tool in tools.tools} == {
                    "search_notes", "list_notes", "read_note",
                    "create_note", "update_note", "append_note"
                }
                result = await session.call_tool(
                    "create_note", {"path": "hello.md", "content": "hello"}
                )
                assert not result.isError
                assert (tmp_path / "hello.md").read_text() == "hello"
                result = await session.call_tool("read_note", {"path": "hello.md"})
                assert not result.isError
    asyncio.run(asyncio.wait_for(run(), timeout=30))
