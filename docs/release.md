# v0.0.1 release

1. Verify the Build and publish workflow passes tests on Windows and Linux and checks both package artifacts.
2. Sign in to PyPI, enable MFA, and open https://pypi.org/manage/account/publishing/. Add a pending GitHub Trusted Publisher with:
   - PyPI project name: recallconduit
   - Owner: dimitriskl
   - Repository: RecallConduit
   - Workflow: release.yml
   - Environment: pypi
3. In GitHub repository settings, create the pypi environment and restrict deployments to main. Review the source and workflow, then manually run Build and publish on main from GitHub Actions. Push and pull requests only test/build, never publish.
4. Verify https://pypi.org/project/recallconduit/0.0.1/ and install the released package in a clean environment.
5. Create the GitHub release/tag v0.0.1 at the tested and published commit.
6. Install the official mcp-publisher CLI from https://github.com/modelcontextprotocol/registry/releases. From the repository root run:
   - mcp-publisher login github
   - mcp-publisher validate server.json
   - mcp-publisher publish server.json
7. Verify the official registry entry for io.github.dimitriskl/recallconduit.

No empty name-reservation packages. This release has a real but deliberately small read-only feature. Future versions must implement note operations and secure remote access before platform directory submissions. A public repository and MIT license do not create exclusive trademark rights.
