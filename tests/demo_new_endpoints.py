#!/usr/bin/env python3
"""Demonstration of new biomes and factions endpoints."""
import asyncio
from highcommand.tools import HellCommandTools

async def main():
    tools = HellCommandTools()
    
    # Test biomes
    print("Testing get_biomes_tool...")
    result = await tools.get_biomes_tool()
    print(f"  Status: {result['status']}")
    if result['status'] == 'success':
        data = result.get('data', {})
        if isinstance(data, dict):
            print(f"  Data keys: {list(data.keys())[:5]}")
    
    # Test factions
    print("\nTesting get_factions_tool...")
    result = await tools.get_factions_tool()
    print(f"  Status: {result['status']}")
    if result['status'] == 'success':
        data = result.get('data', {})
        if isinstance(data, dict):
            print(f"  Data keys: {list(data.keys())[:5]}")

if __name__ == "__main__":
    asyncio.run(main())
