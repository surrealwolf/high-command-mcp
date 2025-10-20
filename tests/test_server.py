"""Tests for MCP server."""

import json
from unittest.mock import AsyncMock, patch

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


@pytest.mark.asyncio
async def test_call_tool_campaign_info_success():
    """Test successful campaign info tool call."""
    mock_campaign_data = {
        "id": 1,
        "name": "Test Campaign",
        "description": "Test Description",
    }

    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_campaign_info.return_value = mock_campaign_data

        result = await call_tool("get_campaign_info", {})

        assert len(result) == 1
        content = json.loads(result[0].text)
        assert content["status"] == "success"
        assert content["data"] == mock_campaign_data
        assert content["error"] is None


@pytest.mark.asyncio
async def test_call_tool_campaign_info_error():
    """Test campaign info tool with error."""
    error_message = "API connection failed"

    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_campaign_info.side_effect = Exception(error_message)

        result = await call_tool("get_campaign_info", {})

        assert len(result) == 1
        content = json.loads(result[0].text)
        assert content["status"] == "error"
        assert content["data"] is None
        assert error_message in content["error"]


@pytest.mark.asyncio
async def test_call_tool_response_shape():
    """Test that all tool responses have consistent shape."""
    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_war_status.return_value = {"status": "active"}

        result = await call_tool("get_war_status", {})

        assert len(result) == 1
        content = json.loads(result[0].text)
        # All responses should have these fields
        assert "status" in content
        assert "data" in content
        assert "error" in content
        assert content["status"] in ["success", "error"]
