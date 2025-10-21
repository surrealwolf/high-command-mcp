"""High-Command API client for Helldivers 2 data."""

import os
from typing import Any, Optional

import httpx
import structlog

logger = structlog.get_logger(__name__)


class HighCommandAPIClient:
    """Client for interacting with the High-Command API."""

    # WARNING: The default BASE_URL uses 'http://', which transmits data unencrypted.
    # This is acceptable for local development only. For production deployments,
    # always set HIGH_COMMAND_API_BASE_URL to an HTTPS endpoint to ensure secure communication.
    BASE_URL = os.getenv("HIGH_COMMAND_API_BASE_URL", "http://localhost:5000")

    def __init__(self, timeout: float = 30.0):
        """Initialize the API client.

        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    @property
    def headers(self) -> dict[str, str]:
        """Get request headers for API requests."""
        return {}

    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers=self.headers,
            timeout=self.timeout,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()

    async def get_war_status(self) -> dict[str, Any]:
        """Get current war status.

        Returns:
            War status information from High-Command API
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use as async context manager.")

        logger.info("Fetching war status")
        try:
            response = await self._client.get("/api/war/status")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Failed to fetch war status", error=str(e))
            raise

    async def get_planets(self) -> dict[str, Any]:
        """Get planet information.

        Returns:
            Planet information from High-Command API
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use as async context manager.")

        logger.info("Fetching planets")
        try:
            response = await self._client.get("/api/planets")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Failed to fetch planets", error=str(e))
            raise

    async def get_statistics(self) -> dict[str, Any]:
        """Get global game statistics.

        Returns:
            Global statistics from High-Command API
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use as async context manager.")

        logger.info("Fetching statistics")
        try:
            response = await self._client.get("/api/statistics")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Failed to fetch statistics", error=str(e))
            raise

    async def get_planet_status(self, planet_index: int) -> dict[str, Any]:
        """Get status for a specific planet.

        Args:
            planet_index: Index of the planet

        Returns:
            Planet status information
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use as async context manager.")

        logger.info("Fetching planet status", planet_index=planet_index)
        try:
            response = await self._client.get(f"/api/planets/{planet_index}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Failed to fetch planet status", planet_index=planet_index, error=str(e))
            raise

    async def get_campaign_info(self) -> dict[str, Any]:
        """Get campaign information.

        Returns:
            Active campaign information from High-Command API
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use as async context manager.")

        logger.info("Fetching campaign information")
        try:
            response = await self._client.get("/api/campaigns/active")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Failed to fetch campaign info", error=str(e))
            raise

    async def get_biomes(self) -> dict[str, Any]:
        """Get biome information.

        Returns:
            Biome data from High-Command API
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use as async context manager.")

        logger.info("Fetching biomes")
        try:
            response = await self._client.get("/api/biomes")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Failed to fetch biomes", error=str(e))
            raise

    async def get_factions(self) -> dict[str, Any]:
        """Get faction information.

        Returns:
            Faction data from High-Command API
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use as async context manager.")

        logger.info("Fetching factions")
        try:
            response = await self._client.get("/api/factions")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("Failed to fetch factions", error=str(e))
            raise
