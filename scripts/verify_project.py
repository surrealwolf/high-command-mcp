#!/usr/bin/env python3
"""
Final Project Verification Script
Shows all components are working correctly
"""

import asyncio
import subprocess
import sys


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


async def verify_imports():
    """Verify all imports work correctly."""
    print_section("1. Verifying Package Imports")

    try:
        from mcp.server import Server
        print("✓ MCP SDK imported successfully")
        from highcommand import CampaignInfo, HelldiverAPIClient, WarInfo
        print("✓ HellCommand package imported successfully")
        from highcommand.tools import HelldiverTools
        print("✓ HellCommand tools imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


async def verify_api_connectivity():
    """Verify API connectivity."""
    print_section("2. Verifying API Connectivity")

    import httpx

    base_url = "https://api-hellhub-collective.koyeb.app/api"
    results = []

    async with httpx.AsyncClient() as client:
        # Test war endpoint
        try:
            r = await client.get(f"{base_url}/war", timeout=10)
            if r.status_code == 200:
                print("✓ /war endpoint: 200 OK")
                results.append(True)
            else:
                print(f"✗ /war endpoint: {r.status_code}")
                results.append(False)
        except Exception as e:
            print(f"✗ /war endpoint: {e}")
            results.append(False)

        # Test planets endpoint
        try:
            r = await client.get(f"{base_url}/planets", timeout=10)
            if r.status_code == 200:
                data = r.json()
                total = data.get('pagination', {}).get('total', 'N/A')
                print(f"✓ /planets endpoint: 200 OK ({total} planets)")
                results.append(True)
            else:
                print(f"✗ /planets endpoint: {r.status_code}")
                results.append(False)
        except Exception as e:
            print(f"✗ /planets endpoint: {e}")
            results.append(False)

        # Test statistics endpoint
        try:
            r = await client.get(f"{base_url}/statistics", timeout=10)
            if r.status_code == 200:
                print("✓ /statistics endpoint: 200 OK")
                results.append(True)
            else:
                print(f"✗ /statistics endpoint: {r.status_code}")
                results.append(False)
        except Exception as e:
            print(f"✗ /statistics endpoint: {e}")
            results.append(False)

    return all(results)


def verify_tests():
    """Verify all tests pass."""
    print_section("3. Running Test Suite")

    result = subprocess.run(
        ["python3", "-m", "pytest", "tests/", "-q"],
        capture_output=True,
        text=True,
    )

    output = result.stdout + result.stderr
    if "12 passed" in output:
        print("✓ All 12 tests passed")
        return True
    else:
        print(f"✗ Tests failed:\n{output}")
        return False


def verify_project_structure():
    """Verify project structure."""
    print_section("4. Verifying Project Structure")

    import os

    required_files = [
        "highcommand/__init__.py",
        "highcommand/api_client.py",
        "highcommand/models.py",
        "highcommand/server.py",
        "highcommand/tools.py",
        "tests/__init__.py",
        "tests/test_api_client.py",
        "tests/test_models.py",
        "tests/test_server.py",
        "pyproject.toml",
        "README.md",
    ]

    all_exist = True
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"✓ {filepath}")
        else:
            print(f"✗ {filepath} - MISSING")
            all_exist = False

    return all_exist


async def main():
    """Run all verifications."""
    print("\n" + "="*70)
    print("  HIGH-COMMAND MCP SERVER - PROJECT VERIFICATION")
    print("="*70)

    results = {
        "Imports": await verify_imports(),
        "API Connectivity": await verify_api_connectivity(),
        "Tests": verify_tests(),
        "Project Structure": verify_project_structure(),
    }

    # Print summary
    print_section("SUMMARY")

    all_passed = True
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {check}")
        if not passed:
            all_passed = False

    print_section("CONCLUSION")
    if all_passed:
        print("✓ ALL SYSTEMS GO - Project is fully functional!")
        print("\nThe MCP Server successfully:")
        print("  • Connects to HellHub Collective API")
        print("  • Retrieves live Helldivers 2 game data")
        print("  • Passes all unit tests")
        print("  • Has proper project structure")
        return 0
    else:
        print("✗ Some checks failed - please review above")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
