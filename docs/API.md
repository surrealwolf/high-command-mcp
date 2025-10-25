# API Documentation

## High-Command MCP Server API

This document describes the tools exposed by the High-Command MCP server, which integrates with the High-Command API.

## Base Information

**API Provider**: High-Command API

**Base URL**: `http://localhost:5000` (configurable via `HIGH_COMMAND_API_BASE_URL`)

**Rate Limit**: The MCP client detects and logs 429 (rate limit) responses but does not implement automatic retry logic. See [Rate Limiting](#rate-limiting) section for details and implementation patterns.

**Update Frequency**: Real-time

## Authentication

The High-Command API requires no authentication. Simple HTTP requests are used:

- No User-Agent header required
- No API keys or special headers required
- All communication via standard HTTP GET requests

### Environment Variables

**Optional**:
- `HIGH_COMMAND_API_BASE_URL`: Base URL for High-Command API (default: `http://localhost:5000`)
- `LOG_LEVEL`: Logging level (default: `INFO`)
- `MCP_TRANSPORT`: Transport mode - `stdio` or `http` (default: `stdio`)

## Tools

### War Status

**Tool Name**: `get_war_status`

Get the current war status in Helldivers 2.

**Parameters**:
None

**Response**:
```json
{
  "data": {
    "id": 1,
    "index": 801,
    "startDate": "2024-01-23T20:05:13.000Z",
    "endDate": "2028-02-08T20:04:55.000Z",
    "time": "1970-04-11T20:12:10.000Z",
    "createdAt": "2024-05-22T12:00:10.239Z",
    "updatedAt": "2024-05-22T12:00:10.239Z"
  },
  "error": null
}
```

**Example**:
```python
async with HelldiverAPIClient() as client:
    war_status = await client.get_war_status()
    war_data = war_status['data']
    print(f"War ID: {war_data['id']}")
```

---

### Planets

**Tool Name**: `get_planets`

Get information about all planets.

**Parameters**:
None

**Response**:
```json
{
  "data": [
    {
      "index": 0,
      "name": "Sicarus Prime",
      "sector": "Sector 1",
      "position": {
        "x": 100,
        "y": 200
      },
      "biome": {
        "name": "Volcanic",
        "description": "..."
      },
      "hazards": [...]
    }
  ],
  "error": null,
  "pagination": {
    "page": 1,
    "pageSize": 50,
    "totalResults": 42,
    "totalPages": 1
  }
}
```

**Example**:
```python
async with HelldiverAPIClient() as client:
    planets_response = await client.get_planets()
    planets = planets_response['data']
    for planet in planets:
        print(f"Planet: {planet['name']} ({planet['sector']})")
```

---

### Statistics

**Tool Name**: `get_statistics`

Get global game statistics.

**Parameters**:
None

**Response**:
```json
{
  "data": [
    {
      "id": 1,
      "missionsWon": 232299033,
      "missionsLost": 24922081,
      "missionTime": 528222382946,
      "bugKills": 38471552786,
      "automatonKills": 15595777961,
      "illuminateKills": 28,
      "bulletsFired": 303336002871,
      "bulletsHit": 336527984287,
      "timePlayed": 528222382946,
      "deaths": 1411862056,
      "revives": 2,
      "friendlyKills": 191683618,
      "missionSuccessRate": 90,
      "accuracy": 100,
      "createdAt": "2024-05-22T12:00:10.239Z",
      "updatedAt": "2024-05-22T12:00:10.239Z"
    }
  ],
  "error": null,
  "pagination": {...}
}
```

**Example**:
```python
async with HelldiverAPIClient() as client:
    stats_response = await client.get_statistics()
    stats = stats_response['data']
    print(f"Missions Won: {stats[0]['missionsWon']}")
```

---

### Campaign Info

**Tool Name**: `get_campaign_info`

Get active campaign information.

**Parameters**:
None

**Response**:
```json
{
  "data": [
    {
      "id": 1,
      "planet": 10,
      "type": 1,
      "count": 5,
      "createdAt": "2024-05-22T12:00:10.239Z",
      "updatedAt": "2024-05-22T12:00:10.239Z"
    }
  ],
  "error": null,
  "pagination": {...}
}
```

**Example**:
```python
async with HelldiverAPIClient() as client:
    campaigns = await client.get_campaign_info()
    for campaign in campaigns['data']:
        print(f"Campaign on planet {campaign['planet']}")
```

---

### Planet Status

**Tool Name**: `get_planet_status`

Get detailed status for a specific planet.

**Parameters**:
- `planet_index` (integer, required): The index of the planet

**Response**:
```json
{
  "data": {
    "index": 0,
    "name": "Sicarus Prime",
    "sector": "Sector 1",
    "position": {"x": 100, "y": 200},
    "biome": {...},
    "hazards": [...],
    "status": {
      "owner": "Humans",
      "health": 100,
      "threats": [...]
    }
  },
  "error": null
}
```

**Example**:
```python
async with HelldiverAPIClient() as client:
    planet_status = await client.get_planet_status(planet_index=0)
    status = planet_status['data']
    print(f"Planet: {status['name']} - Status: {status['status']['owner']}")
```

---

## Response Format

### Success Response

All successful responses follow this format:

```json
{
  "data": {...},
  "error": null,
  "pagination": {...}  // Optional, only for list endpoints
}
```

### Error Response

```json
{
  "data": null,
  "error": "Error message",
  "pagination": null
}
```

## Error Handling

### Network Errors

Raised as `httpx.HTTPError`:

```python
try:
    async with HelldiverAPIClient() as client:
        status = await client.get_war_status()
except httpx.HTTPError as e:
    print(f"API Error: {e}")
```

### Runtime Errors

Raised when client is used outside async context:

```python
client = HelldiverAPIClient()
# This will raise RuntimeError
await client.get_war_status()
```

## Rate Limiting

Monitor rate limit headers in responses:

- `X-Rate-Remaining`: Requests remaining in current window
- `X-Rate-Limit`: Maximum requests per minute (200)
- `X-Rate-Reset`: Unix timestamp when limit resets
- `X-Rate-Count`: Requests made in current window

## Best Practices

1. **Use Context Manager**: Always use the client as async context manager
2. **Error Handling**: Implement proper error handling for network issues
3. **Caching**: Cache responses to reduce API calls
4. **Timeouts**: Set appropriate timeouts for production use
5. **Logging**: Enable logging to debug issues
6. **Rate Limiting**: Respect the 200 requests/minute limit
7. **User-Agent**: Server includes proper User-Agent header

## Examples

### Basic Usage

```python
import asyncio
from mcp.api_client import HelldiverAPIClient

async def main():
    async with HelldiverAPIClient() as client:
        war_status = await client.get_war_status()
        print(war_status['data'])

asyncio.run(main())
```

### With Error Handling and Retry

```python
import asyncio
import httpx
from mcp.api_client import HelldiverAPIClient
import time

async def get_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await func()
        except httpx.TimeoutException:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            print(f"Timeout, retrying in {wait_time}s...")
            await asyncio.sleep(wait_time)

async def main():
    async with HelldiverAPIClient() as client:
        try:
            planets = await get_with_retry(client.get_planets)
            print(f"Found {len(planets['data'])} planets")
        except httpx.HTTPError as e:
            print(f"API error: {e}")

asyncio.run(main())
```

## Rate Limiting

### Client-Side Rate Limit Detection

The High-Command MCP client **detects** but does **not automatically retry** rate-limited requests (HTTP 429).

#### How It Works

1. **Detection**: When the API returns HTTP 429, the client logs a warning:
   ```
   WARNING: Rate limit exceeded endpoint=/api/war/status status=429
   ```

2. **Error Propagation**: The 429 error is raised as `RuntimeError: Rate limit exceeded`

3. **No Automatic Retries**: The MCP client does NOT implement exponential backoff or automatic retries

#### Why No Automatic Retries?

The MCP client follows a **transparent error model** where:
- Applications have full control over retry logic
- Rate limit handling can be customized per use case
- Avoids hiding errors from the calling application
- Prevents unexpected delays in synchronous-feeling APIs

#### Implementing Exponential Backoff

If you need automatic retry with exponential backoff, implement it at the application level:

```python
import asyncio
from highcommand import HighCommandTools

async def get_with_exponential_backoff(tool_func, max_retries=5):
    """
    Call a tool with exponential backoff on rate limit errors.
    
    Implements: 5s → 10s → 20s → 40s → 80s delays
    """
    for attempt in range(max_retries):
        try:
            result = await tool_func()
            
            # Check if the tool returned an error
            if result["status"] == "error" and "Rate limit" in result.get("error", ""):
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 5  # Exponential: 5, 10, 20, 40, 80
                    print(f"Rate limited, waiting {wait_time}s before retry {attempt + 2}/{max_retries}")
                    await asyncio.sleep(wait_time)
                    continue
            
            return result
            
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 5
                print(f"Error: {e}, waiting {wait_time}s before retry {attempt + 2}/{max_retries}")
                await asyncio.sleep(wait_time)
                continue
            raise
    
    return {"status": "error", "data": None, "error": "Max retries exceeded"}


# Usage example
async def main():
    tools = HighCommandTools()
    
    # Wrap tool call with backoff
    result = await get_with_exponential_backoff(tools.get_war_status_tool)
    
    if result["status"] == "success":
        print(f"War data: {result['data']}")
    else:
        print(f"Failed after retries: {result['error']}")
```

#### Retry Timeline Example

| Attempt | Action | Wait Time |
|---------|--------|-----------|
| 1 | Send request | - |
| 2 | 429 response → Wait 5s | 5s |
| 3 | 429 response → Wait 10s | 10s |
| 4 | 429 response → Wait 20s | 20s |
| 5 | 429 response → Wait 40s | 40s |
| 6 | 429 response → Fail | - |

Total max wait time: ~115 seconds across 5 retries

#### Best Practices

1. **Respect the API** - Don't make unnecessary requests
2. **Cache results** - Store data locally when possible to reduce API calls
3. **Implement retry logic** - Use exponential backoff pattern shown above for production use
4. **Handle errors gracefully** - Always check response status in your application
5. **Monitor logs** - Watch for repeated 429 errors indicating consistent rate limiting
6. **Batch operations** - Group related requests when possible to reduce total API calls

#### Rate Limit Headers

Monitor these headers in API responses (if provided by upstream API):
- `X-Rate-Remaining`: Requests remaining in current window
- `X-Rate-Limit`: Maximum requests per time window
- `X-Rate-Reset`: Unix timestamp when limit resets
- `X-Rate-Count`: Requests made in current window

**Note**: Header availability depends on the upstream High-Command API implementation.

## Resources

- [HellHub Collective API](https://github.com/hellhub-collective/api)
- [HellHub Postman Collection](https://documenter.getpostman.com/view/33840175/2sA35Bd54w)
- [Helldivers 2 Game](https://store.steampowered.com/app/553850/HELLDIVERS_2/)

## Support

For issues or questions:
- Check [CONTRIBUTING.md](../CONTRIBUTING.md)
- Open an issue on GitHub
- Start a discussion
