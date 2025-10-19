"""MCP tools for High-Command API."""

from typing import Any

from highcommand.api_client import HighCommandAPIClient


class HighCommandTools:
    """Tools for interacting with High-Command API."""

    def __init__(self):
        """Initialize the tools."""
        self.client = HighCommandAPIClient()

    async def get_war_status_tool(self) -> dict[str, Any]:
        """Tool to get current war status.

        Returns:
            JSON formatted war status
        """
        async with self.client:
            data = await self.client.get_war_status()
            return {"status": "success", "data": data}

    async def get_planets_tool(self) -> dict[str, Any]:
        """Tool to get planet information.

        Returns:
            JSON formatted planet data
        """
        async with self.client:
            data = await self.client.get_planets()
            return {"status": "success", "data": data}

    async def get_statistics_tool(self) -> dict[str, Any]:
        """Tool to get global statistics.

        Returns:
            JSON formatted statistics data
        """
        async with self.client:
            data = await self.client.get_statistics()
            return {"status": "success", "data": data}

    async def get_campaign_info_tool(self) -> dict[str, Any]:
        """Tool to get campaign information.

        Returns:
            JSON formatted campaign data
        """
        async with self.client:
            data = await self.client.get_campaign_info()
            return {"status": "success", "data": data}

    async def get_planet_status_tool(self, planet_index: int) -> dict[str, Any]:
        """Tool to get status for a specific planet.

        Args:
            planet_index: Index of the planet

        Returns:
            JSON formatted planet status data
        """
        async with self.client:
            data = await self.client.get_planet_status(planet_index)
            return {"status": "success", "data": data}

    async def get_biomes_tool(self) -> dict[str, Any]:
        """Tool to get biome information.

        Returns:
            JSON formatted biome data
        """
        async with self.client:
            data = await self.client.get_biomes()
            return {"status": "success", "data": data}

    async def get_factions_tool(self) -> dict[str, Any]:
        """Tool to get faction information.

        Returns:
            JSON formatted faction data
        """
        async with self.client:
            data = await self.client.get_factions()
            return {"status": "success", "data": data}
