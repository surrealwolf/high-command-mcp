"""Tests for the API client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from highcommand.api_client import HighCommandAPIClient


@pytest.fixture
def api_client():
    """Create an API client instance."""
    return HighCommandAPIClient()


@pytest.mark.asyncio
async def test_api_client_headers(api_client):
    """Test that API client initializes with minimal headers."""
    headers = api_client.headers
    # High-Command API doesn't require authentication or custom headers
    assert isinstance(headers, dict)
    assert len(headers) == 0


@pytest.mark.asyncio
async def test_get_war_status(api_client):
    """Test getting war status - basic initialization test."""
    # Just verify that the method exists and can be called
    # Real API testing is done in integration tests
    async with api_client:
        assert hasattr(api_client, "get_war_status")
        assert callable(api_client.get_war_status)


@pytest.mark.asyncio
async def test_api_client_context_manager(api_client):
    """Test API client context manager."""
    async with api_client as client:
        assert client._client is not None
    # After exiting context manager, _client should be closed (but not necessarily None)
    # Just verify that the context manager works without errors


@pytest.mark.asyncio
async def test_api_client_without_context_manager_raises(api_client):
    """Test that using API client without context manager raises."""
    with pytest.raises(RuntimeError):
        await api_client.get_war_status()


@pytest.mark.asyncio
async def test_get_campaign_info_success(api_client):
    """Test successful campaign info retrieval."""
    mock_response = {
        "status": "success",
        "data": {
            "name": "Test Campaign",
            "description": "Test Description",
        },
    }

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_http_response = MagicMock()
        mock_http_response.json.return_value = mock_response
        mock_client.get.return_value = mock_http_response

        async with api_client:
            result = await api_client.get_campaign_info()
            assert result == mock_response
            mock_client.get.assert_called_once_with("/api/campaigns/active")


@pytest.mark.asyncio
async def test_get_campaign_info_error(api_client):
    """Test campaign info retrieval with HTTP error."""
    import httpx

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_client.get.side_effect = httpx.HTTPError("Connection failed")

        async with api_client:
            with pytest.raises(httpx.HTTPError):
                await api_client.get_campaign_info()


@pytest.mark.asyncio
async def test_get_planets_success(api_client):
    """Test successful planets retrieval."""
    mock_response = {
        "status": "success",
        "data": [{"index": 0, "name": "Sicarus Prime"}],
    }

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_http_response = MagicMock()
        mock_http_response.json.return_value = mock_response
        mock_client.get.return_value = mock_http_response

        async with api_client:
            result = await api_client.get_planets()
            assert result == mock_response
            mock_client.get.assert_called_once_with("/api/planets")


@pytest.mark.asyncio
async def test_get_planets_error(api_client):
    """Test planets retrieval with HTTP error."""
    import httpx

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_client.get.side_effect = httpx.HTTPError("Connection failed")

        async with api_client:
            with pytest.raises(httpx.HTTPError):
                await api_client.get_planets()


@pytest.mark.asyncio
async def test_get_statistics_success(api_client):
    """Test successful statistics retrieval."""
    mock_response = {
        "status": "success",
        "data": {"missionsWon": 100, "accuracy": 85},
    }

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_http_response = MagicMock()
        mock_http_response.json.return_value = mock_response
        mock_client.get.return_value = mock_http_response

        async with api_client:
            result = await api_client.get_statistics()
            assert result == mock_response
            mock_client.get.assert_called_once_with("/api/statistics")


@pytest.mark.asyncio
async def test_get_statistics_error(api_client):
    """Test statistics retrieval with HTTP error."""
    import httpx

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_client.get.side_effect = httpx.HTTPError("Connection failed")

        async with api_client:
            with pytest.raises(httpx.HTTPError):
                await api_client.get_statistics()


@pytest.mark.asyncio
async def test_get_planet_status_success(api_client):
    """Test successful planet status retrieval."""
    planet_index = 42
    mock_response = {
        "status": "success",
        "data": {"index": planet_index, "name": "Test Planet"},
    }

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_http_response = MagicMock()
        mock_http_response.json.return_value = mock_response
        mock_client.get.return_value = mock_http_response

        async with api_client:
            result = await api_client.get_planet_status(planet_index)
            assert result == mock_response
            mock_client.get.assert_called_once_with(f"/api/planets/{planet_index}")


@pytest.mark.asyncio
async def test_get_planet_status_error(api_client):
    """Test planet status retrieval with HTTP error."""
    import httpx

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_client.get.side_effect = httpx.HTTPError("Connection failed")

        async with api_client:
            with pytest.raises(httpx.HTTPError):
                await api_client.get_planet_status(0)


@pytest.mark.asyncio
async def test_get_biomes_success(api_client):
    """Test successful biomes retrieval."""
    mock_response = {
        "status": "success",
        "data": [{"name": "Desert", "description": "Hot and sandy"}],
    }

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_http_response = MagicMock()
        mock_http_response.json.return_value = mock_response
        mock_client.get.return_value = mock_http_response

        async with api_client:
            result = await api_client.get_biomes()
            assert result == mock_response
            mock_client.get.assert_called_once_with("/api/biomes")


@pytest.mark.asyncio
async def test_get_biomes_error(api_client):
    """Test biomes retrieval with HTTP error."""
    import httpx

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_client.get.side_effect = httpx.HTTPError("Connection failed")

        async with api_client:
            with pytest.raises(httpx.HTTPError):
                await api_client.get_biomes()


@pytest.mark.asyncio
async def test_get_factions_success(api_client):
    """Test successful factions retrieval."""
    mock_response = {
        "status": "success",
        "data": [{"name": "Bugs", "description": "Insectoid aliens"}],
    }

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_http_response = MagicMock()
        mock_http_response.json.return_value = mock_response
        mock_client.get.return_value = mock_http_response

        async with api_client:
            result = await api_client.get_factions()
            assert result == mock_response
            mock_client.get.assert_called_once_with("/api/factions")


@pytest.mark.asyncio
async def test_get_factions_error(api_client):
    """Test factions retrieval with HTTP error."""
    import httpx

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_client.get.side_effect = httpx.HTTPError("Connection failed")

        async with api_client:
            with pytest.raises(httpx.HTTPError):
                await api_client.get_factions()


@pytest.mark.asyncio
async def test_get_war_status_success(api_client):
    """Test successful war status retrieval."""
    mock_response = {
        "status": "success",
        "data": {"id": 1, "index": 801},
    }

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_http_response = MagicMock()
        mock_http_response.json.return_value = mock_response
        mock_client.get.return_value = mock_http_response

        async with api_client:
            result = await api_client.get_war_status()
            assert result == mock_response
            mock_client.get.assert_called_once_with("/api/war/status")


@pytest.mark.asyncio
async def test_get_war_status_error(api_client):
    """Test war status retrieval with HTTP error."""
    import httpx

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_client.get.side_effect = httpx.HTTPError("Connection failed")

        async with api_client:
            with pytest.raises(httpx.HTTPError):
                await api_client.get_war_status()


@pytest.mark.asyncio
async def test_api_client_timeout_configuration():
    """Test API client timeout configuration."""
    custom_timeout = 60.0
    client = HighCommandAPIClient(timeout=custom_timeout)
    assert client.timeout == custom_timeout


@pytest.mark.asyncio
async def test_api_client_http_status_error(api_client):
    """Test handling HTTP status errors."""
    import httpx

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_http_response = MagicMock()
        mock_http_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=MagicMock(), response=MagicMock()
        )
        mock_client.get.return_value = mock_http_response

        async with api_client:
            with pytest.raises(httpx.HTTPStatusError):
                await api_client.get_war_status()


@pytest.mark.asyncio
async def test_get_planets_without_context_manager():
    """Test that get_planets raises without context manager."""
    client = HighCommandAPIClient()
    with pytest.raises(RuntimeError, match="Client not initialized"):
        await client.get_planets()


@pytest.mark.asyncio
async def test_get_statistics_without_context_manager():
    """Test that get_statistics raises without context manager."""
    client = HighCommandAPIClient()
    with pytest.raises(RuntimeError, match="Client not initialized"):
        await client.get_statistics()


@pytest.mark.asyncio
async def test_get_planet_status_without_context_manager():
    """Test that get_planet_status raises without context manager."""
    client = HighCommandAPIClient()
    with pytest.raises(RuntimeError, match="Client not initialized"):
        await client.get_planet_status(0)


@pytest.mark.asyncio
async def test_get_campaign_info_without_context_manager():
    """Test that get_campaign_info raises without context manager."""
    client = HighCommandAPIClient()
    with pytest.raises(RuntimeError, match="Client not initialized"):
        await client.get_campaign_info()


@pytest.mark.asyncio
async def test_get_biomes_without_context_manager():
    """Test that get_biomes raises without context manager."""
    client = HighCommandAPIClient()
    with pytest.raises(RuntimeError, match="Client not initialized"):
        await client.get_biomes()


@pytest.mark.asyncio
async def test_get_factions_without_context_manager():
    """Test that get_factions raises without context manager."""
    client = HighCommandAPIClient()
    with pytest.raises(RuntimeError, match="Client not initialized"):
        await client.get_factions()
