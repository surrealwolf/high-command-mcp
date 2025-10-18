"""Tests for the API client."""
import pytest
import httpx
from unittest.mock import AsyncMock, patch

from highcommand.api_client import HelldiverAPIClient


@pytest.fixture
def api_client():
    """Create an API client instance."""
    return HelldiverAPIClient()


@pytest.mark.asyncio
async def test_api_client_headers(api_client):
    """Test that API client sets correct headers."""
    headers = api_client.headers
    assert "User-Agent" in headers
    assert "high-command" in headers["User-Agent"]
    assert "lee@fullmetal.dev" in headers["User-Agent"]


@pytest.mark.asyncio
async def test_get_war_status(api_client):
    """Test getting war status - basic initialization test."""
    # Just verify that the method exists and can be called
    # Real API testing is done in integration tests
    async with api_client:
        assert hasattr(api_client, 'get_war_status')
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
