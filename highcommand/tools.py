"""MCP tools for High-Command API."""

from typing import Any

from highcommand.api_client import HighCommandAPIClient


class HighCommandTools:
    """Tools for interacting with High-Command API."""

    async def get_war_status_tool(self) -> dict[str, Any]:
        """Tool to get current war status.

        Returns:
            JSON formatted war status
        """
        try:
            async with HighCommandAPIClient() as client:
                data = await client.get_war_status()
                return {"status": "success", "data": data, "error": None}
        except Exception as e:
            return {"status": "error", "data": None, "error": str(e)}

    async def get_planets_tool(self) -> dict[str, Any]:
        """Tool to get planet information.

        Returns:
            JSON formatted planet data
        """
        try:
            async with HighCommandAPIClient() as client:
                data = await client.get_planets()
                return {"status": "success", "data": data, "error": None}
        except Exception as e:
            return {"status": "error", "data": None, "error": str(e)}

    async def get_statistics_tool(self) -> dict[str, Any]:
        """Tool to get global statistics.

        Returns:
            JSON formatted statistics data
        """
        try:
            async with HighCommandAPIClient() as client:
                data = await client.get_statistics()
                return {"status": "success", "data": data, "error": None}
        except Exception as e:
            return {"status": "error", "data": None, "error": str(e)}

    async def get_campaign_info_tool(self) -> dict[str, Any]:
        """Tool to get campaign information.

        Returns:
            JSON formatted campaign data
        """
        try:
            async with HighCommandAPIClient() as client:
                data = await client.get_campaign_info()
                return {"status": "success", "data": data, "error": None}
        except Exception as e:
            return {"status": "error", "data": None, "error": str(e)}

    async def get_planet_status_tool(self, planet_index: int) -> dict[str, Any]:
        """Tool to get status for a specific planet.

        Args:
            planet_index: Index of the planet

        Returns:
            JSON formatted planet status data
        """
        try:
            async with HighCommandAPIClient() as client:
                data = await client.get_planet_status(planet_index)
                return {"status": "success", "data": data, "error": None}
        except Exception as e:
            return {"status": "error", "data": None, "error": str(e)}

    async def get_biomes_tool(self) -> dict[str, Any]:
        """Tool to get biome information.

        Returns:
            JSON formatted biome data
        """
        try:
            async with HighCommandAPIClient() as client:
                data = await client.get_biomes()
                return {"status": "success", "data": data, "error": None}
        except Exception as e:
            return {"status": "error", "data": None, "error": str(e)}

    async def get_factions_tool(self) -> dict[str, Any]:
        """Tool to get faction information.

        Returns:
            JSON formatted faction data
        """
        try:
            async with HighCommandAPIClient() as client:
                data = await client.get_factions()
                return {"status": "success", "data": data, "error": None}
        except Exception as e:
            return {"status": "error", "data": None, "error": str(e)}
