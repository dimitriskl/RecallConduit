# RecallConduit

**Latest change — v0.0.1:** Minimal local MCP server for listing Markdown filenames; packaging and registry metadata prepared. Publication and test status must be verified before use.

**Different minds. One memory.**

RecallConduit is an independent MIT-licensed project to connect AI assistants to a shared Obsidian knowledge base through MCP.

<!-- mcp-name: io.github.dimitriskl/recallconduit -->

## v0.0.1 scope

One read-only tool, `list_notes`, lists up to 100 visible Markdown filenames in the root of the configured vault. No recursion, note content access, search, writes, remote access or approved ChatGPT/Claude integration yet.

## Local installation from source

Python 3.11 or newer:

```sh
python -m pip install .
```

Configure a compatible local MCP client with the absolute path to the installed command:

```json
{
  "mcpServers": {
    "recallconduit": {
      "command": "C:/path/to/venv/Scripts/recallconduit.exe",
      "env": {
        "RECALLCONDUIT_VAULT": "C:/path/to/test-vault"
      }
    }
  }
}
```

Use a test vault first. Local stdio only; no network listener.

## Project identifiers

| Platform | Intended identifier |
| --- | --- |
| GitHub | dimitriskl/RecallConduit |
| PyPI | recallconduit |
| MCP Registry | io.github.dimitriskl/recallconduit |
| Obsidian plugin (if needed) | recall-conduit |
| ChatGPT / Claude | RecallConduit |

Registry submissions are pending until successful publication. See [release checklist](docs/release.md).

## Development

The maintainer will implement the full functionality, starting with [milestone 1](docs/milestones.md).

## License

[MIT](LICENSE). Independent project; not affiliated with Obsidian, OpenAI, or Anthropic.
