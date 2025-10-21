"""Tests for High-Command tools."""

from unittest.mock import AsyncMock, patch

import pytest

from highcommand.tools import HighCommandTools


@pytest.fixture
def tools():
    """Create a HighCommandTools instance."""
    return HighCommandTools()


@pytest.mark.asyncio
async def test_get_war_status_tool_success(tools):
    """Test successful war status tool call."""
    mock_data = {"id": 1, "index": 801}

    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_war_status.return_value = mock_data

        result = await tools.get_war_status_tool()

        assert result["status"] == "success"
        assert result["data"] == mock_data
        assert result["error"] is None


@pytest.mark.asyncio
async def test_get_war_status_tool_error(tools):
    """Test war status tool with error."""
    error_message = "API connection failed"

    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_war_status.side_effect = Exception(error_message)

        result = await tools.get_war_status_tool()

        assert result["status"] == "error"
        assert result["data"] is None
        assert error_message in result["error"]


@pytest.mark.asyncio
async def test_get_planets_tool_success(tools):
    """Test successful planets tool call."""
    mock_data = [{"index": 0, "name": "Sicarus Prime"}]

    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_planets.return_value = mock_data

        result = await tools.get_planets_tool()

        assert result["status"] == "success"
        assert result["data"] == mock_data
        assert result["error"] is None


@pytest.mark.asyncio
async def test_get_planets_tool_error(tools):
    """Test planets tool with error."""
    error_message = "Failed to fetch planets"

    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_planets.side_effect = Exception(error_message)

        result = await tools.get_planets_tool()

        assert result["status"] == "error"
        assert result["data"] is None
        assert error_message in result["error"]


@pytest.mark.asyncio
async def test_get_statistics_tool_success(tools):
    """Test successful statistics tool call."""
    mock_data = {"missionsWon": 100, "accuracy": 85}

    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_statistics.return_value = mock_data

        result = await tools.get_statistics_tool()

        assert result["status"] == "success"
        assert result["data"] == mock_data
        assert result["error"] is None


@pytest.mark.asyncio
async def test_get_statistics_tool_error(tools):
    """Test statistics tool with error."""
    error_message = "Failed to fetch statistics"

    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_statistics.side_effect = Exception(error_message)

        result = await tools.get_statistics_tool()

        assert result["status"] == "error"
        assert result["data"] is None
        assert error_message in result["error"]


@pytest.mark.asyncio
async def test_get_planet_status_tool_success(tools):
    """Test successful planet status tool call."""
    planet_index = 42
    mock_data = {"index": planet_index, "name": "Test Planet"}

    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_planet_status.return_value = mock_data

        result = await tools.get_planet_status_tool(planet_index)

        assert result["status"] == "success"
        assert result["data"] == mock_data
        assert result["error"] is None


@pytest.mark.asyncio
async def test_get_planet_status_tool_error(tools):
    """Test planet status tool with error."""
    planet_index = 42
    error_message = "Planet not found"

    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_planet_status.side_effect = Exception(error_message)

        result = await tools.get_planet_status_tool(planet_index)

        assert result["status"] == "error"
        assert result["data"] is None
        assert error_message in result["error"]


@pytest.mark.asyncio
async def test_get_biomes_tool_success(tools):
    """Test successful biomes tool call."""
    mock_data = [{"name": "Desert", "description": "Hot and sandy"}]

    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_biomes.return_value = mock_data

        result = await tools.get_biomes_tool()

        assert result["status"] == "success"
        assert result["data"] == mock_data
        assert result["error"] is None


@pytest.mark.asyncio
async def test_get_biomes_tool_error(tools):
    """Test biomes tool with error."""
    error_message = "Failed to fetch biomes"

    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_biomes.side_effect = Exception(error_message)

        result = await tools.get_biomes_tool()

        assert result["status"] == "error"
        assert result["data"] is None
        assert error_message in result["error"]


@pytest.mark.asyncio
async def test_get_factions_tool_success(tools):
    """Test successful factions tool call."""
    mock_data = [{"name": "Bugs", "description": "Insectoid aliens"}]

    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_factions.return_value = mock_data

        result = await tools.get_factions_tool()

        assert result["status"] == "success"
        assert result["data"] == mock_data
        assert result["error"] is None


@pytest.mark.asyncio
async def test_get_factions_tool_error(tools):
    """Test factions tool with error."""
    error_message = "Failed to fetch factions"

    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_factions.side_effect = Exception(error_message)

        result = await tools.get_factions_tool()

        assert result["status"] == "error"
        assert result["data"] is None
        assert error_message in result["error"]


@pytest.mark.asyncio
async def test_run_tool_helper_with_non_async_function():
    """Test _run_tool helper raises TypeError for non-async function."""
    tools = HighCommandTools()

    def sync_func():
        return {"data": "test"}

    with pytest.raises(TypeError):
        await tools._run_tool(sync_func)


@pytest.mark.asyncio
async def test_run_tool_helper_success():
    """Test _run_tool helper with successful execution."""
    tools = HighCommandTools()

    async def async_func():
        return {"data": "test"}

    result = await tools._run_tool(async_func)

    assert result["status"] == "success"
    assert result["data"] == {"data": "test"}
    assert result["error"] is None


@pytest.mark.asyncio
async def test_run_tool_helper_error():
    """Test _run_tool helper with error."""
    tools = HighCommandTools()
    error_message = "Test error"

    async def async_func():
        raise Exception(error_message)

    result = await tools._run_tool(async_func)

    assert result["status"] == "error"
    assert result["data"] is None
    assert error_message in result["error"]
