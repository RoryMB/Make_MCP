# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "mcp",
# ]
# ///

"""
MCP Server for Making MCP Servers
"""

import json
import random
from pathlib import Path

from mcp.server.fastmcp import Context, FastMCP


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

# Run the server when executed directly
if __name__ == "__main__":
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error running server: {e}")
        import traceback
        traceback.print_exc()
        import sys
        sys.exit(1)
