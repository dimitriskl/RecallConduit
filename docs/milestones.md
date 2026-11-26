# Development milestones

The maintainer writes the implementation. AI assistance is limited to mentoring, reviewing submitted code, explaining concepts and suggesting targeted exercises unless explicitly requested otherwise.

## Milestone 1: Vault reader

- Accept a vault root and a relative Markdown path.
- Return UTF-8 content from a valid note.
- Reject absolute paths, traversal, links that escape the vault, and non-Markdown files.
- Handle missing notes and test with a temporary directory.
- No MCP dependency, search index, remote access, or writes yet.

Acceptance: the maintainer can explain the path validation, run their tests and demonstrate that a note outside the vault cannot be read.

## Later milestones

2. Search and bounded results.
3. Safe create/update/append with revision checking and read-only default.
4. Local MCP adapter and protocol integration tests.
5. Package build and release.
6. Assess authenticated remote access and platform compatibility.
