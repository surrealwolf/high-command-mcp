import asyncio
import httpx
import json

async def test():
    async with httpx.AsyncClient() as c:
        r = await c.get('https://api-hellhub-collective.koyeb.app/api/planets?pageSize=1')
        d = r.json()
        print('Top level keys:', list(d.keys()))
        print('Full response:')
        print(json.dumps(d, indent=2)[:1200])

asyncio.run(test())
