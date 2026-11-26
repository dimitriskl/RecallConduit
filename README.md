# RecallConduit

**Different minds. One memory.**

RecallConduit is an MIT-licensed project developing provider-independent access to a shared Obsidian knowledge base for AI assistants, including ChatGPT and Claude, through the Model Context Protocol (MCP).

## Status

Pre-development. No installable package, plugin, or MCP server has been released yet. The features below are planned, not implemented.

## Planned capabilities

- Search and read Markdown notes in an authorized vault.
- Create, update, and append to notes with safeguards against accidental overwrites.
- Share explicitly saved knowledge across compatible AI assistants.
- Enforce vault boundaries, configurable permissions, and safe concurrent writes.
- Support a Python MCP server and, where necessary, platform-specific integrations.

## Canonical project identifiers

| Target | Intended identifier |
| --- | --- |
| GitHub | [dimitriskl/RecallConduit](https://github.com/dimitriskl/RecallConduit) |
| Python distribution / import | `recallconduit` |
| Official MCP Registry | `io.github.dimitriskl/recallconduit` |
| Obsidian plugin ID (if needed) | `recall-conduit` |
| ChatGPT / Claude display name | RecallConduit |

Only the GitHub repository is established at this time. Other identifiers are planned, not registered or approved.

## Release and distribution

Publish a functional, tested first release rather than an empty name-reservation package. The official MCP Registry supports GitHub namespace authentication. A native Obsidian plugin, if needed, will follow the Obsidian Community directory submission requirements. ChatGPT and Claude integrations will follow their respective developer and review processes.

## License

[MIT](LICENSE). RecallConduit is an independent project and is not affiliated with Obsidian, OpenAI, or Anthropic.
