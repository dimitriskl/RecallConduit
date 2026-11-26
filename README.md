# RecallConduit

**Latest change — v0.1.0 development:** First local MCP server and automated tests added. Not yet published.

**Different minds. One memory.**

RecallConduit is an independent, MIT-licensed Python project for shared Obsidian knowledge across AI assistants using the Model Context Protocol (MCP).

<!-- mcp-name: io.github.dimitriskl/recallconduit -->

## Current scope

Local stdio MCP only. Remote access, ChatGPT/Claude web and mobile integrations, directory approval, and native Obsidian plugin support are not yet implemented.

Six tools: search_notes, list_notes, read_note, create_note, update_note, append_note. Reads are limited to Markdown in a selected directory. Writes are disabled by default and require explicit opt-in. Updates require the revision returned by read_note.

## Development installation

Python 3.11 or newer:

```sh
python -m pip install ".[test]"
python -m pytest -q
```

Configure a local MCP-compatible client (for example Claude Desktop) using the absolute path to your installed recallconduit executable:

```json
{
  "mcpServers": {
    "recallconduit": {
      "command": "C:/path/to/venv/Scripts/recallconduit.exe",
      "env": {
        "RECALLCONDUIT_VAULT": "C:/path/to/test-vault",
        "RECALLCONDUIT_WRITE": "0"
      }
    }
  }
}
```

Use a dedicated test vault before enabling writes. Set RECALLCONDUIT_WRITE to 1 only when you intend to permit note changes. Parent folders must exist. Append adds exact text, including any required newlines.

## Security and limitations

- Local trusted filesystem only; no authentication or network listener.
- No deletion or arbitrary filesystem tools. Hidden paths and symbolic links are rejected.
- Notes are untrusted content, not instructions. Client-side approval remains important.
- Size and result limits bound individual responses; search is a linear scan.
- Revision checks and atomic replacement reduce conflicts. They do not eliminate races with other processes, such as Obsidian Sync; do not use simultaneous writers.
- Not a security sandbox against hostile local filesystem manipulation. Use a dedicated vault and normal OS permissions. Atomic creation requires filesystem hard-link support.
- No claim of tested compatibility with any specific client until integration tests pass.

## Distribution

| Platform | Planned identifier |
| --- | --- |
| GitHub | dimitriskl/RecallConduit |
| PyPI | recallconduit |
| MCP Registry | io.github.dimitriskl/recallconduit |
| Obsidian plugin (if needed) | recall-conduit |
| ChatGPT / Claude | RecallConduit |

See [release checklist](docs/release.md). Registry identifiers are not yet registered.

## License

[MIT](LICENSE). Not affiliated with Obsidian, OpenAI, or Anthropic.
