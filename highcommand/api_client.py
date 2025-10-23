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
        self._validate_production_url()

    @staticmethod
    def _validate_production_url() -> None:
        """Validate that HTTPS is used in production deployments.

        Raises:
            ValueError: If production deployment uses HTTP instead of HTTPS
        """
        environment = os.getenv("ENVIRONMENT", "development").lower()
        base_url = os.getenv("HIGH_COMMAND_API_BASE_URL", "http://localhost:5000")

        if environment == "production" and base_url.startswith("http://"):
            raise ValueError(
                "Production deployments must use HTTPS. "
                "Set HIGH_COMMAND_API_BASE_URL to an https:// URL."
            )

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

    async def _handle_response(self, response: httpx.Response, endpoint: str) -> dict[str, Any]:
        """Handle API response with proper error categorization.

        Args:
            response: HTTP response object
            endpoint: API endpoint for logging

        Returns:
            Response data as dictionary

        Raises:
            httpx.HTTPError: On HTTP errors with categorized logging
        """
        try:
            response.raise_for_status()
            elapsed_ms = response.elapsed.total_seconds() * 1000
            logger.info(
                "API request succeeded",
                endpoint=endpoint,
                status=response.status_code,
                elapsed_ms=elapsed_ms,
            )
            return response.json()
        except httpx.HTTPStatusError as e:
            elapsed_ms = e.response.elapsed.total_seconds() * 1000
            status_code = e.response.status_code

            # Categorize error based on HTTP status
            if 500 <= status_code < 600:
                logger.warning(
                    "Server error",
                    endpoint=endpoint,
                    status=status_code,
                    elapsed_ms=elapsed_ms,
                )
                error_msg = f"Server error ({status_code}): {e.response.reason_phrase}"
            elif status_code == 429:
                logger.warning(
                    "Rate limit exceeded",
                    endpoint=endpoint,
                    status=status_code,
                    elapsed_ms=elapsed_ms,
                )
                error_msg = "Rate limit exceeded"
            elif 400 <= status_code < 500:
                logger.error(
                    "Client error",
                    endpoint=endpoint,
                    status=status_code,
                    elapsed_ms=elapsed_ms,
                )
                error_msg = f"Client error ({status_code}): {e.response.reason_phrase}"
            else:
                logger.error(
                    "Unknown HTTP error",
                    endpoint=endpoint,
                    status=status_code,
                    elapsed_ms=elapsed_ms,
                )
                error_msg = f"HTTP error ({status_code}): {e.response.reason_phrase}"

            raise RuntimeError(error_msg) from e

    async def get_war_status(self) -> dict[str, Any]:
        """Get current war status.

        Returns:
            War status information from High-Command API
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use as async context manager.")

        logger.info("Fetching war status")
        response = await self._client.get("/api/war/status")
        return await self._handle_response(response, "/api/war/status")

    async def get_planets(self) -> dict[str, Any]:
        """Get planet information.

        Returns:
            Planet information from High-Command API
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use as async context manager.")

        logger.info("Fetching planets")
        response = await self._client.get("/api/planets")
        return await self._handle_response(response, "/api/planets")

    async def get_statistics(self) -> dict[str, Any]:
        """Get global game statistics.

        Returns:
            Global statistics from High-Command API
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use as async context manager.")

        logger.info("Fetching statistics")
        response = await self._client.get("/api/statistics")
        return await self._handle_response(response, "/api/statistics")

    async def get_planet_status(self, planet_index: int) -> dict[str, Any]:
        """Get status for a specific planet.

        Args:
            planet_index: Index of the planet

        Returns:
            Planet status information
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use as async context manager.")

        endpoint = f"/api/planets/{planet_index}"
        logger.info("Fetching planet status", planet_index=planet_index)
        response = await self._client.get(endpoint)
        return await self._handle_response(response, endpoint)

    async def get_campaign_info(self) -> dict[str, Any]:
        """Get campaign information.

        Returns:
            Active campaign information from High-Command API
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use as async context manager.")

        logger.info("Fetching campaign information")
        response = await self._client.get("/api/campaigns/active")
        return await self._handle_response(response, "/api/campaigns/active")

    async def get_biomes(self) -> dict[str, Any]:
        """Get biome information.

        Returns:
            Biome data from High-Command API
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use as async context manager.")

        logger.info("Fetching biomes")
        response = await self._client.get("/api/biomes")
        return await self._handle_response(response, "/api/biomes")

    async def get_factions(self) -> dict[str, Any]:
        """Get faction information.

        Returns:
            Faction data from High-Command API
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use as async context manager.")

        logger.info("Fetching factions")
        response = await self._client.get("/api/factions")
        return await self._handle_response(response, "/api/factions")
