# Release checklist

- Build a functional Python package and verify automated tests on Windows and Linux.
- Confirm package name availability and create a PyPI account with MFA.
- Configure a trusted publisher or use an authenticated local upload. Never commit credentials.
- Build and inspect distributions, tag v0.1.0, and publish matching artifacts after successful tests.
- Validate an MCP Registry manifest against the current official schema and publish using GitHub namespace authentication.
- Verify the public package and registry listing.
- Implement and test any necessary authenticated remote access before submitting integrations to ChatGPT and Claude.
- Submit a native Obsidian plugin only if required.

Official resources:

- https://docs.pypi.org/trusted-publishers/
- https://github.com/modelcontextprotocol/registry
- https://platform.openai.com/
- https://claude.ai/directory/manage

GitHub ownership and MIT licensing do not grant exclusive trademark rights. Domain purchases and trademark filings require separate owner authorization. Do not upload empty packages solely to reserve names.
