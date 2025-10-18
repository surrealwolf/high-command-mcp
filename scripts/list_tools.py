#!/usr/bin/env python3
"""List all available MCP tools."""
import asyncio
from highcommand.server import list_tools

async def main():
    tools = await list_tools()
    print("Available MCP Tools:")
    print("=" * 60)
    for i, tool in enumerate(tools, 1):
        print(f"{i}. {tool.name}")
        print(f"   {tool.description}")
        if tool.inputSchema.get('properties'):
            params = list(tool.inputSchema['properties'].keys())
            if params:
                print(f"   Parameters: {params}")
        print()

if __name__ == "__main__":
    asyncio.run(main())
