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
async def test_production_url_validation_https():
    """Test that production environment with HTTPS URL passes validation."""
    with patch.dict("os.environ", {"ENVIRONMENT": "production", "HIGH_COMMAND_API_BASE_URL": "https://api.example.com"}):
        # Should not raise
        client = HighCommandAPIClient()
        assert client is not None


@pytest.mark.asyncio
async def test_production_url_validation_http_fails():
    """Test that production environment with HTTP URL raises ValueError."""
    with patch.dict("os.environ", {"ENVIRONMENT": "production", "HIGH_COMMAND_API_BASE_URL": "http://api.example.com"}):
        with pytest.raises(ValueError, match="Production deployments must use HTTPS"):
            HighCommandAPIClient()


@pytest.mark.asyncio
async def test_handle_response_success(api_client):
    """Test successful response handling."""
    import httpx
    from datetime import timedelta

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}
    mock_response.elapsed = timedelta(seconds=0.5)
    mock_response.raise_for_status = MagicMock()

    async with api_client:
        result = await api_client._handle_response(mock_response, "/api/test")
        assert result == {"data": "test"}
        mock_response.raise_for_status.assert_called_once()


@pytest.mark.asyncio
async def test_handle_response_rate_limit(api_client):
    """Test handling of 429 rate limit error."""
    import httpx
    from datetime import timedelta

    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_response.reason_phrase = "Too Many Requests"
    mock_response.elapsed = timedelta(seconds=0.1)

    def raise_http_error():
        raise httpx.HTTPStatusError("Rate limited", request=MagicMock(), response=mock_response)

    mock_response.raise_for_status = raise_http_error

    async with api_client:
        with pytest.raises(RuntimeError, match="Rate limit exceeded"):
            await api_client._handle_response(mock_response, "/api/test")


@pytest.mark.asyncio
async def test_handle_response_server_error(api_client):
    """Test handling of 5xx server errors."""
    import httpx
    from datetime import timedelta

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.reason_phrase = "Internal Server Error"
    mock_response.elapsed = timedelta(seconds=0.2)

    def raise_http_error():
        raise httpx.HTTPStatusError("Server error", request=MagicMock(), response=mock_response)

    mock_response.raise_for_status = raise_http_error

    async with api_client:
        with pytest.raises(RuntimeError, match="Server error"):
            await api_client._handle_response(mock_response, "/api/test")


@pytest.mark.asyncio
async def test_handle_response_client_error(api_client):
    """Test handling of 4xx client errors."""
    import httpx
    from datetime import timedelta

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.reason_phrase = "Not Found"
    mock_response.elapsed = timedelta(seconds=0.1)

    def raise_http_error():
        raise httpx.HTTPStatusError("Not found", request=MagicMock(), response=mock_response)

    mock_response.raise_for_status = raise_http_error

    async with api_client:
        with pytest.raises(RuntimeError, match="Client error"):
            await api_client._handle_response(mock_response, "/api/test")


@pytest.mark.asyncio
async def test_get_planets(api_client):
    """Test getting planets information."""
    mock_response = {"status": "success", "data": []}

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_http_response = MagicMock()
        mock_http_response.json.return_value = mock_response
        mock_http_response.status_code = 200
        mock_http_response.raise_for_status = MagicMock()
        from datetime import timedelta
        mock_http_response.elapsed = timedelta(seconds=0.1)
        mock_client.get.return_value = mock_http_response

        async with api_client:
            result = await api_client.get_planets()
            assert result == mock_response
            mock_client.get.assert_called_once_with("/api/planets")


@pytest.mark.asyncio
async def test_get_statistics(api_client):
    """Test getting statistics."""
    mock_response = {"status": "success", "data": {}}

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_http_response = MagicMock()
        mock_http_response.json.return_value = mock_response
        mock_http_response.status_code = 200
        mock_http_response.raise_for_status = MagicMock()
        from datetime import timedelta
        mock_http_response.elapsed = timedelta(seconds=0.1)
        mock_client.get.return_value = mock_http_response

        async with api_client:
            result = await api_client.get_statistics()
            assert result == mock_response
            mock_client.get.assert_called_once_with("/api/statistics")


@pytest.mark.asyncio
async def test_get_planet_status(api_client):
    """Test getting planet status by index."""
    mock_response = {"status": "success", "data": {"planet": "test"}}

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_http_response = MagicMock()
        mock_http_response.json.return_value = mock_response
        mock_http_response.status_code = 200
        mock_http_response.raise_for_status = MagicMock()
        from datetime import timedelta
        mock_http_response.elapsed = timedelta(seconds=0.1)
        mock_client.get.return_value = mock_http_response

        async with api_client:
            result = await api_client.get_planet_status(123)
            assert result == mock_response
            mock_client.get.assert_called_once_with("/api/planets/123")


@pytest.mark.asyncio
async def test_get_biomes(api_client):
    """Test getting biomes information."""
    mock_response = {"status": "success", "data": []}

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_http_response = MagicMock()
        mock_http_response.json.return_value = mock_response
        mock_http_response.status_code = 200
        mock_http_response.raise_for_status = MagicMock()
        from datetime import timedelta
        mock_http_response.elapsed = timedelta(seconds=0.1)
        mock_client.get.return_value = mock_http_response

        async with api_client:
            result = await api_client.get_biomes()
            assert result == mock_response
            mock_client.get.assert_called_once_with("/api/biomes")


@pytest.mark.asyncio
async def test_get_factions(api_client):
    """Test getting factions information."""
    mock_response = {"status": "success", "data": []}

    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        mock_http_response = MagicMock()
        mock_http_response.json.return_value = mock_response
        mock_http_response.status_code = 200
        mock_http_response.raise_for_status = MagicMock()
        from datetime import timedelta
        mock_http_response.elapsed = timedelta(seconds=0.1)
        mock_client.get.return_value = mock_http_response

        async with api_client:
            result = await api_client.get_factions()
            assert result == mock_response
            mock_client.get.assert_called_once_with("/api/factions")
