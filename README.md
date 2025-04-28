# Make_MCP
An MCP server for making MCP servers

## Using with Claude Desktop

Go to Claude > Settings > Developer > Edit Config

Add to your `claude_desktop_config.json`:
```json
{
    "mcpServers": {
        "make_mcp": {
            // Fix to your location of `uv`, or swap with python and remove the "run" argument below.
            "command": "/Users/rmbutler/.local/bin/uv",
            "args": [
                "run",
                "/path/to/Make_MCP/main.py"
            ],
            "env": {
            }
        }
    }
}
```

Restart Claude Desktop to see the new resource in the plug menu "Attach from MCP":
![resource](https://github.com/user-attachments/assets/1a37d556-9c2a-4c91-9cd0-a12237c2a911)

Add the make_mcp resource, then ask for an MCP server with whatever you want. For example:
`Write a basic mcp server with a very simple URL fetch tool to get HTML`

Claude will write your MCP server, which you can download and add to the configuration just like Make_MCP:
```json
{
    "mcpServers": {
        "make_mcp": {
            // Fix to your location of `uv`, or swap with python and remove the "run" argument below.
            "command": "/Users/rmbutler/.local/bin/uv",
            "args": [
                "run",
                "/path/to/Make_MCP/main.py"
            ],
            "env": {
            }
        }
    },
    "mcpServers": {
        "new_server": {
            // Fix to your location of `uv`, or swap with python and remove the "run" argument below.
            "command": "/Users/rmbutler/.local/bin/uv",
            "args": [
                "run",
                "/Users/rmbutler/Downloads/new_server.py"
            ],
            "env": {
            }
        }
    }
}
```

Restart Claude Desktop to see your new tools in the hammer menu "1 MCP tool available":
![tool](https://github.com/user-attachments/assets/b360e749-0ec3-43e8-bc0f-7981b5dbb228)
