# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "mcp",
# ]
# ///

"""
MCP Server for Making MCP Servers
"""

from pathlib import Path

from mcp.server.fastmcp import FastMCP


# ===== INITIALIZATION =====

mcp = FastMCP("MakeMCP")

DOCS_FILE = Path(__file__).parent / "docs.md"


# ===== RESOURCES =====

# Static resources
@mcp.resource("makemcp://docs", name="make_mcp", description="Documentation on how to make an MCP server.")
def make_mcp() -> str:
    """Documentation on how to make an MCP server."""
    with open(DOCS_FILE, "r") as f:
        return f.read()


# ===== TOOLS =====

@mcp.tool()
def how_to_make_mcp() -> str:
    """This tool returns instructions on how to build MCP servers.

    You should use this tool if the user asks you to make an MCP server,
    but did not provide general information on MCP servers. The instructions
    include an example server and a quick overview of MCP terms like tools,
    resources, and prompts."""
    with open(DOCS_FILE, "r") as f:
        return f.read()


def main():
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error running server: {e}")
        import traceback
        traceback.print_exc()
        import sys
        sys.exit(1)

# Run the server when executed directly
if __name__ == '__main__':
    main()
