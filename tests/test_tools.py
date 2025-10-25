"""Tests for the tools module."""

from unittest.mock import AsyncMock, patch

import pytest

from highcommand.tools import HighCommandTools


@pytest.fixture
def tools():
    """Create a tools instance."""
    return HighCommandTools()


@pytest.mark.asyncio
async def test_run_tool_with_non_coroutine():
    """Test that _run_tool raises TypeError for non-async functions."""
    
    def sync_function():
        return "test"
    
    with pytest.raises(TypeError, match="Expected async function"):
        await HighCommandTools._run_tool(sync_function)


@pytest.mark.asyncio
async def test_run_tool_with_metrics_success():
    """Test _run_tool with metrics enabled on success."""
    
    async def async_function():
        return {"data": "test"}
    
    result = await HighCommandTools._run_tool(async_function, include_metrics=True)
    
    assert result["status"] == "success"
    assert result["data"] == {"data": "test"}
    assert result["error"] is None
    assert "metrics" in result
    assert "elapsed_ms" in result["metrics"]
    assert result["metrics"]["elapsed_ms"] > 0


@pytest.mark.asyncio
async def test_run_tool_with_metrics_error():
    """Test _run_tool with metrics enabled on error."""
    
    async def async_function():
        raise ValueError("Test error")
    
    result = await HighCommandTools._run_tool(async_function, include_metrics=True)
    
    assert result["status"] == "error"
    assert result["data"] is None
    assert "ValueError: Test error" in result["error"]
    assert "metrics" in result
    assert "elapsed_ms" in result["metrics"]


@pytest.mark.asyncio
async def test_get_war_status_tool(tools):
    """Test get_war_status_tool."""
    mock_data = {"status": "success", "data": {"war": "info"}}
    
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
async def test_get_planets_tool(tools):
    """Test get_planets_tool."""
    mock_data = {"status": "success", "data": []}
    
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
async def test_get_statistics_tool(tools):
    """Test get_statistics_tool."""
    mock_data = {"status": "success", "data": {"stats": "data"}}
    
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
async def test_get_planet_status_tool(tools):
    """Test get_planet_status_tool."""
    mock_data = {"status": "success", "data": {"planet": "info"}}
    
    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_planet_status.return_value = mock_data
        
        result = await tools.get_planet_status_tool(123)
        
        assert result["status"] == "success"
        assert result["data"] == mock_data
        assert result["error"] is None
        mock_client.get_planet_status.assert_called_once_with(123)


@pytest.mark.asyncio
async def test_get_biomes_tool(tools):
    """Test get_biomes_tool."""
    mock_data = {"status": "success", "data": []}
    
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
async def test_get_factions_tool(tools):
    """Test get_factions_tool."""
    mock_data = {"status": "success", "data": []}
    
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
async def test_tool_error_handling(tools):
    """Test tool error handling."""
    
    with patch("highcommand.tools.HighCommandAPIClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        mock_client.get_war_status.side_effect = Exception("API error")
        
        result = await tools.get_war_status_tool()
        
        assert result["status"] == "error"
        assert result["data"] is None
        assert "Exception: API error" in result["error"]
