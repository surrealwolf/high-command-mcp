#!/usr/bin/env python3
"""Test script to verify HellHub API data retrieval"""

import asyncio
import httpx
import json


async def test_hellhub_api():
    """Test HellHub API endpoints"""
    base_url = "https://api-hellhub-collective.koyeb.app/api"

    async with httpx.AsyncClient() as client:
        print("Testing HellHub Collective API\n" + "=" * 50)

        # Test 1: War Status
        print("\n1. Testing /war endpoint...")
        try:
            response = await client.get(f"{base_url}/war", timeout=10)
            war_data = response.json()
            print(f"✓ Status: {response.status_code}")
            print(f"  War ID: {war_data['data']['id']}")
            print(f"  War Index: {war_data['data']['index']}")
            print(f"  Start Date: {war_data['data']['startDate']}")
        except Exception as e:
            print(f"✗ Error: {e}")

        # Test 2: Planets
        print("\n2. Testing /planets endpoint...")
        try:
            response = await client.get(f"{base_url}/planets", timeout=10)
            planets_data = response.json()
            print(f"✓ Status: {response.status_code}")
            print(f"  Total Planets: {planets_data['pagination']['total']}")
            if planets_data['data']:
                p = planets_data['data'][0]
                print(f"  First Planet: {p['name']} ({p['sectorId']} sector)")
        except Exception as e:
            print(f"✗ Error: {e}")

        # Test 3: Statistics
        print("\n3. Testing /statistics endpoint...")
        try:
            response = await client.get(f"{base_url}/statistics", timeout=10)
            stats_data = response.json()
            print(f"✓ Status: {response.status_code}")
            if stats_data['data']:
                s = stats_data['data'][0]
                print(f"  Missions Won: {s['missionsWon']:,}")
                print(f"  Missions Lost: {s['missionsLost']:,}")
                print(f"  Success Rate: {s['missionSuccessRate']}%")
        except Exception as e:
            print(f"✗ Error: {e}")

        # Test 4: Campaigns (NOTE: Not available in HellHub API)
        print("\n4. Testing /campaigns endpoint...")
        try:
            response = await client.get(f"{base_url}/campaigns", timeout=10)
            if response.status_code == 404:
                print(f"ℹ  Campaigns endpoint not available (404)")
            else:
                campaigns_data = response.json()
                print(f"✓ Status: {response.status_code}")
                print(f"  Total Campaigns: {campaigns_data['pagination']['total']}")
                if campaigns_data['data']:
                    c = campaigns_data['data'][0]
                    print(f"  First Campaign: Planet {c['planet']}, Type {c['type']}")
        except Exception as e:
            print(f"ℹ  {e}")

        print("\n" + "=" * 50)
        print("✓ API Testing Complete!")


if __name__ == "__main__":
    asyncio.run(test_hellhub_api())
