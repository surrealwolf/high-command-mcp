"""Tests for MCP server."""

import json

import pytest

from highcommand.server import call_tool, list_tools


@pytest.mark.asyncio
async def test_list_tools():
    """Test that tools are properly listed."""
    tools = await list_tools()

    assert len(tools) == 7
    tool_names = {tool.name for tool in tools}

    expected_tools = {
        "get_war_status",
        "get_planets",
        "get_statistics",
        "get_campaign_info",
        "get_planet_status",
        "get_biomes",
        "get_factions",
    }

    assert tool_names == expected_tools


@pytest.mark.asyncio
async def test_tool_schemas():
    """Test that tools have proper schemas."""
    tools = await list_tools()

    # Find get_planet_status tool (it has required parameters)
    planet_status_tool = next(t for t in tools if t.name == "get_planet_status")

    assert "planet_index" in planet_status_tool.inputSchema["properties"]
    assert "planet_index" in planet_status_tool.inputSchema["required"]


@pytest.mark.asyncio
async def test_call_tool_invalid_name():
    """Test calling tool with invalid name."""
    result = await call_tool("invalid_tool", {})

    assert len(result) == 1
    content = json.loads(result[0].text)
    assert content["status"] == "error"
    assert "Unknown tool" in content["error"]


@pytest.mark.asyncio
async def test_call_tool_missing_required_parameter():
    """Test calling tool with missing required parameter."""
    result = await call_tool("get_planet_status", {})

    assert len(result) == 1
    content = json.loads(result[0].text)
    assert content["status"] == "error"
