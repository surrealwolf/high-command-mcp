"""MCP tools for HellHub Collective API."""
from typing import Any, Dict, Optional
import json

from highcommand.api_client import HelldiverAPIClient


class HelldiverTools:
    """Tools for interacting with HellHub Collective API."""

    def __init__(
        self,
        client_id: str = "high-command",
        contact_email: str = "lee@fullmetal.dev",
    ):
        """Initialize the tools.

        Args:
            client_id: Identifier for this client
            contact_email: Contact email for API usage
        """
        self.client = HelldiverAPIClient(client_id=client_id, contact_email=contact_email)

    async def get_war_status_tool(self) -> Dict[str, Any]:
        """Tool to get current war status.

        Returns:
            JSON formatted war status
        """
        async with self.client:
            data = await self.client.get_war_status()
            return {"status": "success", "data": data}

    async def get_planets_tool(self) -> Dict[str, Any]:
        """Tool to get planet information.

        Returns:
            JSON formatted planet data
        """
        async with self.client:
            data = await self.client.get_planets()
            return {"status": "success", "data": data}

    async def get_statistics_tool(self) -> Dict[str, Any]:
        """Tool to get global statistics.

        Returns:
            JSON formatted statistics data
        """
        async with self.client:
            data = await self.client.get_statistics()
            return {"status": "success", "data": data}

    async def get_campaign_info_tool(self) -> Dict[str, Any]:
        """Tool to get campaign information.

        Note: This endpoint is not available in the current HellHub API.

        Returns:
            Error response indicating endpoint unavailability
        """
        return {
            "status": "error",
            "data": None,
            "error": "Campaigns endpoint is not available in the HellHub Collective API",
        }

    async def get_planet_status_tool(self, planet_index: int) -> Dict[str, Any]:
        """Tool to get status for a specific planet.

        Args:
            planet_index: Index of the planet

        Returns:
            JSON formatted planet status data
        """
        async with self.client:
            data = await self.client.get_planet_status(planet_index)
            return {"status": "success", "data": data}

    async def get_biomes_tool(self) -> Dict[str, Any]:
        """Tool to get biome information.

        Returns:
            JSON formatted biome data
        """
        async with self.client:
            data = await self.client.get_biomes()
            return {"status": "success", "data": data}

    async def get_factions_tool(self) -> Dict[str, Any]:
        """Tool to get faction information.

        Returns:
            JSON formatted faction data
        """
        async with self.client:
            data = await self.client.get_factions()
            return {"status": "success", "data": data}
