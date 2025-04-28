Here is an example MCP server with comments on how to make changes according to user design requests.

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "mcp",
# ]
# ///

"""
MCP Server for Example

An example of Model Context Protocol (MCP) features
including resources, tools, and prompts.
"""

import json
import random
from pathlib import Path

from mcp.server.fastmcp import Context, FastMCP


# ===== INITIALIZATION =====

## Use this code ONLY if you need it
## @dataclass
## class AppContext:
##     db: Database
## @asynccontextmanager
## async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
##     """Manage application lifecycle with type-safe context"""
##     # Initialize on startup
##     db = await Database.connect()
##     try:
##         yield AppContext(db=db)
##     finally:
##         # Cleanup on shutdown
##         await db.disconnect()

## Give the server a useful name that will be visible to clients
## Do not include "Server" or "MCP" in the name
## mcp = FastMCP("Name", lifespan=app_lifespan)  # If you use the app_lifespan function above
mcp = FastMCP("Name")


## This example defines where to look for recipe data
## If needed, you should set up your own variables here for use across functions
RECIPES_FILE = Path(__file__).parent / "recipes.json"


## Define any helper functions / etc. here too
def example():
    """This function is just an example"""
    return


## For functions in the remaining sections, certain parts will be visible to and should be informative enough for LLM agents to use:
##     Should have a unique and descriptive function name
##     Should have self-explanatory argument names
##     Should have a short, preferably 1-liner, docstring that explains what the function does
##     Should ONLY include descriptions of each argument in the docstring if it is not clear from context
##     Only static resources should have in the decorator (..., name="function_name", description="docstring 1-liner")


# ===== RESOURCES =====

# Static resources
@mcp.resource("recipes://all", name="get_all_recipes", description="Get all recipes in JSON format.")
def get_all_recipes() -> str:
    """Get all recipes in JSON format."""
    with open(RECIPES_FILE, "r") as f:
        recipes = json.load(f)
    return json.dumps(recipes, indent=2)

# Resource templates
@mcp.resource("recipes://{index}")
def get_recipe(index: str) -> str:
    """Get a specific recipe by index."""
    try:
        idx = int(index)
        with open(RECIPES_FILE, "r") as f:
            recipes = json.load(f)
        if 0 <= idx < len(recipes):
            return json.dumps(recipes[idx], indent=2)
        return f"Error: Index {idx} out of range (0-{len(recipes)-1})"
    except ValueError:
        return f"Error: Invalid index '{index}'"


# ===== PROMPTS =====

@mcp.prompt()
def make_joke_from_fact() -> str:
    """Make a joke based on a random fun fact."""
    return """I'd like a funny joke.

Please:
1. Retrieve a random fun fact using the get_random_fun_fact tool
2. Think of a way to turn some aspect of the fact into something humorous
3. Write a funny 1-liner based on the fact
"""


# ===== TOOLS =====

@mcp.tool()
def problematic(number: float = 0) -> str:
    """Tool that causes lots of problems"""
    ## Error messages are automatically propagated to the agent
    ## In this case, the agent would see `ZeroDivisionError: division by zero`
    _ = 1 / number

    ## So, you don't have to wrap the entire function body in a try block!
    ## It's fine if errors are raised, and they can even help the agent figure out how to use the tool
    assert number > 10, "This function requires `number` to be greater than 10"

    return "Your number was good!"

@mcp.tool()
def query_db(ctx: Context) -> str:
    """Tool that uses initialized resources"""
    db = ctx.request_context.lifespan_context["db"]
    return db.query()

@mcp.tool()
def search_knowledge_base(query: str) -> str:
    """Search across knowledge base for an exact match to the given query."""
    results = {"recipes": []}

    # Search recipes
    with open(RECIPES_FILE, "r") as f:
        recipes = json.load(f)
    for item in recipes:
        if (query.lower() in item["name"].lower() or
            query.lower() in item["instructions"].lower() or
            any(query.lower() in ingredient.lower() for ingredient in item["ingredients"])):
            results["recipes"].append(item)

    return json.dumps(results, indent=2)

@mcp.tool()
def get_random_fun_fact() -> str:
    """Get a random fun fact."""
    facts = [
        "The unicorn is Scotland's national animal.",
        "A group of flamingos is called a 'flamboyance'.",
        "The Hawaiian alphabet has only 12 letters.",
    ]
    return random.choice(facts)


## DO NOT change anything below this line unless specifically asked to do so.
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
```

# AI GUIDE TO CREATING MCP SERVERS

This guide is designed to help AI models interpret user requirements and create Model Context Protocol (MCP) servers in Python without requiring users to understand MCP details.

## QUICK MCP OVERVIEW

MCP servers define capabilities for AI agent systems to interact with tools, resources, and prompts.
Unless specifically requesting resources and prompts by name or asking for functionality specific to resources and prompts, the user most likely only wants tools in their server.

1. **Tools**: Functions AI can call to perform actions
   - Take parameters from the AI
   - Execute in the MCP server
   - Return results to the AI

1. **Resources**: Data that users or AI can access (files, APIs, databases)
   - Static resources: Fixed data points with unchanging URIs
   - Resource templates: Parameterized URIs that accept variables

3. **Prompts**: Pre-defined templates that users can inject into conversations for specific interactions
   - Guide conversation in particular directions
   - Create consistent patterns for complex tasks

## HOW TO INTERPRET USER REQUIREMENTS

When a user describes what they want:
- Identify which components (tools, resources, prompts) are needed
- Use the FastMCP framework from the Python MCP SDK
- Follow the structure in the example server
- Create meaningful names and documentation for each component
- Implement appropriate error handling
- Return well-structured data (JSON recommended for complex data)

## WRITING CLEAR CODE FOR THE USER

- Keep imports simple and clear
- Document code with concise, helpful comments
- Use meaningful function and parameter names
- Provide useful error messages
- Follow FastMCP patterns from the example

## IMPORTANT DIRECTIONS

- Write only the smallest number of tools, resources, and prompts necessary to satisfy the user's request
- Prefer tools instead of resources and prompts

# INSTRUCTIONS FOR USERS

You should provide these instructions to the user after writing their server.

## Saving and running the server

1. Save the generated server code to a file (e.g., `my_server.py`)

2. If not using uv, install the required packages with pip:
   ```
   pip install mcp
   # Install any other packages mentioned in imports
   ```

## Configuration for clients
   ```json
   {
     "mcpServers": {
       // If using `uv`
       "serverName": {
         "command": "uv",
         "args": [
           "run",
           "/full/path/to/my_server.py"
         ]
       },
       // If using `python`
       "serverName": {
         "command": "python",
         "args": ["/full/path/to/my_server.py"]
       }
     }
   }
   ```
   **Note:** You may need to specify full paths to executables and scripts. For fallback compatibility, provide alternative configurations:
   ```json
   {
     "mcpServers": {
       // If using `uv`
       "serverName": {
         "command": "/full/path/to/uv",
         "args": [
           "run",
           "/full/path/to/my_server.py"
         ]
       },
       // If using `python`
       "serverName": {
         "command": "/full/path/to/python",
         "args": ["/full/path/to/my_server.py"]
       }
     }
   }
   ```
   Make sure to use the absolute path to your server file.