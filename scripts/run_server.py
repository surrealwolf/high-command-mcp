#!/usr/bin/env python3
"""Development server runner."""
import asyncio
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from highcommand.server import main


if __name__ == "__main__":
    asyncio.run(main())
