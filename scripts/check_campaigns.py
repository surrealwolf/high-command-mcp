import asyncio

import httpx


async def test():
    async with httpx.AsyncClient() as c:
        # Try different campaign endpoints
        for path in ['/campaigns', '/campaign', '/operations', '/operation']:
            r = await c.get(f'https://api-hellhub-collective.koyeb.app/api{path}')
            print(f'{path}: Status {r.status_code} - {r.text[:100]}')

asyncio.run(test())
