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
