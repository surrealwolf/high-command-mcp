"""MCP tools for High-Command API."""

import inspect
from typing import Any, Callable

from highcommand.api_client import HighCommandAPIClient


class HighCommandTools:
    """Tools for interacting with High-Command API."""

    @staticmethod
    async def _run_tool(func: Callable[..., Any]) -> dict[str, Any]:
        """Helper to run a tool function with standardized response shape.

        Args:
            func: Async callable that returns tool data

        Returns:
            Standardized response with status, data, and error fields

        Raises:
            TypeError: If func is not a coroutine function
        """
        if not inspect.iscoroutinefunction(func):
            raise TypeError(f"Expected async function, got {type(func).__name__}")
        try:
            data = await func()
            return {"status": "success", "data": data, "error": None}
        except Exception as e:
            return {"status": "error", "data": None, "error": str(e)}

    async def get_war_status_tool(self) -> dict[str, Any]:
        """Tool to get current war status.

        Returns:
            JSON formatted war status
        """

        async def _fetch() -> Any:
            async with HighCommandAPIClient() as client:
                return await client.get_war_status()

        return await self._run_tool(_fetch)

    async def get_planets_tool(self) -> dict[str, Any]:
        """Tool to get planet information.

        Returns:
            JSON formatted planet data
        """

        async def _fetch() -> Any:
            async with HighCommandAPIClient() as client:
                return await client.get_planets()

        return await self._run_tool(_fetch)

    async def get_statistics_tool(self) -> dict[str, Any]:
        """Tool to get global statistics.

        Returns:
            JSON formatted statistics data
        """

        async def _fetch() -> Any:
            async with HighCommandAPIClient() as client:
                return await client.get_statistics()

        return await self._run_tool(_fetch)

    async def get_campaign_info_tool(self) -> dict[str, Any]:
        """Tool to get campaign information.

        Returns:
            JSON formatted campaign data
        """

        async def _fetch() -> Any:
            async with HighCommandAPIClient() as client:
                return await client.get_campaign_info()

        return await self._run_tool(_fetch)

    async def get_planet_status_tool(self, planet_index: int) -> dict[str, Any]:
        """Tool to get status for a specific planet.

        Args:
            planet_index: Index of the planet

        Returns:
            JSON formatted planet status data
        """

        async def _fetch() -> Any:
            async with HighCommandAPIClient() as client:
                return await client.get_planet_status(planet_index)

        return await self._run_tool(_fetch)

    async def get_biomes_tool(self) -> dict[str, Any]:
        """Tool to get biome information.

        Returns:
            JSON formatted biome data
        """

        async def _fetch() -> Any:
            async with HighCommandAPIClient() as client:
                return await client.get_biomes()

        return await self._run_tool(_fetch)

    async def get_factions_tool(self) -> dict[str, Any]:
        """Tool to get faction information.

        Returns:
            JSON formatted faction data
        """

        async def _fetch() -> Any:
            async with HighCommandAPIClient() as client:
                return await client.get_factions()

        return await self._run_tool(_fetch)
