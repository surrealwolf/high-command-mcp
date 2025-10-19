#!/usr/bin/env python3
"""Test import resolution"""

# When importing mcp from server.py, the local mcp dir might take precedence
# We need to be careful about naming

# Try with explicit relative/absolute import patterns

# Option 1: Try importing Server from the SDK mcp
try:
    # This will fail if our local mcp package shadows it
    import mcp
    print(f"mcp module from: {mcp.__file__}")
    print(f"Has Server? {hasattr(mcp, 'Server')}")
    from highcommand import Server  # noqa: F401
    print("✓ Imported Server from mcp SDK")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    print("\nThis means our local 'mcp' package is shadowing the SDK package")
    print("Solution: Rename our package or use different import strategy")
