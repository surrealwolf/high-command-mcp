#!/usr/bin/env python3
"""Discover available HellHub API endpoints"""

import asyncio

import httpx


async def discover_endpoints():
    """Try to discover available endpoints by testing common ones"""
    base_url = "https://api-hellhub-collective.koyeb.app/api"

    # Common endpoint names to test
    test_endpoints = [
        "/war",
        "/wars",
        "/planet",
        "/planets",
        "/planets/1",
        "/planet/1",
        "/statistics",
        "/stats",
        "/campaign",
        "/campaigns",
        "/operation",
        "/operations",
        "/season",
        "/seasons",
        "/reward",
        "/rewards",
        "/news",
        "/update",
        "/updates",
        "/global-event",
        "/globalEvent",
        "/enemy",
        "/enemies",
        "/biome",
        "/biomes",
        "/hazard",
        "/hazards",
        "/faction",
        "/factions",
    ]

    print("Testing HellHub API Endpoints")
    print("="*60)

    async with httpx.AsyncClient() as client:
        results = {"200": [], "404": [], "500": [], "other": []}

        for endpoint in test_endpoints:
            try:
                url = f"{base_url}{endpoint}"
                r = await client.get(url, timeout=5)

                if r.status_code == 200:
                    results["200"].append((endpoint, len(r.text)))
                elif r.status_code == 404:
                    results["404"].append(endpoint)
                elif r.status_code == 500:
                    results["500"].append(endpoint)
                else:
                    results["other"].append((endpoint, r.status_code))
            except Exception:
                pass

    # Print results
    print("\n✅ WORKING ENDPOINTS (200 OK):")
    for endpoint, size in results["200"]:
        print(f"  {endpoint:30} ({size:,} bytes)")

    print("\n❌ NOT FOUND (404):")
    for endpoint in results["404"][:10]:
        print(f"  {endpoint}")
    if len(results["404"]) > 10:
        print(f"  ... and {len(results['404'])-10} more")

    if results["500"]:
        print("\n⚠️  SERVER ERRORS (500):")
        for endpoint in results["500"]:
            print(f"  {endpoint}")

    if results["other"]:
        print("\n⚠️  OTHER STATUS CODES:")
        for endpoint, code in results["other"]:
            print(f"  {endpoint:30} ({code})")

asyncio.run(discover_endpoints())
