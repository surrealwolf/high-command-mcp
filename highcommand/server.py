"""MCP Server implementation for Helldivers 2 API."""
import asyncio
import json
import logging
import os
from typing import Any

from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
)
from mcp import stdio_server

from highcommand.tools import HelldiverTools

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# Initialize server and tools
server = Server("high-command")
tools = HelldiverTools(
    client_id=os.getenv("X_SUPER_CLIENT", "hc.dataknife.ai"),
    contact_email=os.getenv("X_SUPER_CONTACT", "lee@fullmetal.dev"),
)


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="get_war_status",
            description="Get current war status from HellHub Collective API",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_planets",
            description="Get planet information from HellHub Collective API",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_statistics",
            description="Get global game statistics from HellHub Collective API",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_campaign_info",
            description="Get campaign information from HellHub Collective API",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_planet_status",
            description="Get status for a specific planet",
            inputSchema={
                "type": "object",
                "properties": {
                    "planet_index": {
                        "type": "integer",
                        "description": "The index of the planet",
                    }
                },
                "required": ["planet_index"],
            },
        ),
        Tool(
            name="get_biomes",
            description="Get biome information from HellHub Collective API",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_factions",
            description="Get faction information from HellHub Collective API",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute an MCP tool."""
    logger.info(f"Calling tool: {name}")

    try:
        if name == "get_war_status":
            result = await tools.get_war_status_tool()
        elif name == "get_planets":
            result = await tools.get_planets_tool()
        elif name == "get_statistics":
            result = await tools.get_statistics_tool()
        elif name == "get_campaign_info":
            result = await tools.get_campaign_info_tool()
        elif name == "get_planet_status":
            planet_index = arguments.get("planet_index")
            if planet_index is None:
                raise ValueError("planet_index is required")
            result = await tools.get_planet_status_tool(planet_index)
        elif name == "get_biomes":
            result = await tools.get_biomes_tool()
        elif name == "get_factions":
            result = await tools.get_factions_tool()
        else:
            raise ValueError(f"Unknown tool: {name}")

        return [TextContent(type="text", text=json.dumps(result))]

    except Exception as e:
        logger.error(f"Error calling tool {name}: {str(e)}")
        return [
            TextContent(
                type="text",
                text=json.dumps({"status": "error", "error": str(e)}),
            )
        ]


async def main():
    """Run the MCP server."""
    logger.info("Starting Helldivers 2 MCP Server")
    async with stdio_server(server):
        logger.info("MCP Server started successfully and waiting for connections...")


if __name__ == "__main__":
    asyncio.run(main())
