# Release checklist

1. Verify CI succeeds on Linux and Windows. Perform a manual test with Claude Desktop and a disposable vault.
2. Confirm PyPI name availability and create a PyPI account with MFA. Configure a pending trusted publisher for this repository and the intended release workflow, or use a local authenticated upload. Never commit credentials.
3. Build and inspect artifacts: python -m build; python -m twine check "dist/*".
4. After tests pass, tag v0.1.0 and publish the matching artifacts using the owner's authenticated PyPI account.
5. Create and validate server.json against the current official MCP Registry schema. The package README includes the namespace verification marker. Authenticate with mcp-publisher login github and publish the manifest using mcp-publisher publish.
6. Verify package installation from PyPI and the public MCP Registry listing.
7. Implement authenticated remote transport and platform-specific integration before seeking ChatGPT or Claude directory approval. Submit a native Obsidian plugin only if required.

Official resources:

- https://docs.pypi.org/trusted-publishers/
- https://github.com/modelcontextprotocol/registry
- https://platform.openai.com/
- https://claude.ai/directory/manage

A public repository, an MIT license and a registry identifier do not establish exclusive trademark rights. Domain purchases and trademark filings require separate owner authorization.
