import asyncio
import json

import httpx


async def test():
    async with httpx.AsyncClient() as c:
        r = await c.get('https://api-hellhub-collective.koyeb.app/api/planets?pageSize=1')
        d = r.json()
        print('Pagination:', json.dumps(d['pagination'], indent=2))

asyncio.run(test())
