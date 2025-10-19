#!/usr/bin/env python3
"""Debug HellHub API response structures"""

import asyncio

import httpx


async def debug_api():
    """Check actual API response structures"""
    base_url = "https://api-hellhub-collective.koyeb.app/api"

    async with httpx.AsyncClient() as client:
        # Check planets response
        print("=" * 60)
        print("PLANETS ENDPOINT RESPONSE:")
        print("=" * 60)
        try:
            response = await client.get(f"{base_url}/planets", timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Raw text (first 1000 chars):\n{response.text[:1000]}")
        except Exception as e:
            print(f"Error: {e}")

        # Check campaigns response
        print("\n" + "=" * 60)
        print("CAMPAIGNS ENDPOINT RESPONSE:")
        print("=" * 60)
        try:
            response = await client.get(f"{base_url}/campaigns", timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Raw text (first 1000 chars):\n{response.text[:1000]}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(debug_api())
