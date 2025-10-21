# API Documentation

## High-Command MCP Server API

This document describes the tools exposed by the High-Command MCP server, which integrates with the High-Command API.

## Base Information

**API Provider**: High-Command API

**Base URL**: `http://localhost:5000` (configurable via `HIGH_COMMAND_API_BASE_URL`)

**Rate Limit**: The High-Command API implements automatic exponential backoff for rate limiting (see [Rate Limiting](#rate-limiting) section)

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
async with HighCommandAPIClient() as client:
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
async with HighCommandAPIClient() as client:
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
async with HighCommandAPIClient() as client:
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
async with HighCommandAPIClient() as client:
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
async with HighCommandAPIClient() as client:
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
    async with HighCommandAPIClient() as client:
        status = await client.get_war_status()
except httpx.HTTPError as e:
    print(f"API Error: {e}")
```

### Runtime Errors

Raised when client is used outside async context:

```python
client = HighCommandAPIClient()
# This will raise RuntimeError
await client.get_war_status()
```

## Rate Limiting

### Automatic Exponential Backoff

The High-Command API implements **automatic exponential backoff** to handle rate limit responses (HTTP 429).

#### Backoff Strategy

When a request receives a 429 (Too Many Requests) response:

1. **Exponential delays** are applied: `5s → 10s → 20s → 40s → 80s`
2. **Up to 5 retry attempts** before failing
3. **Calculation**: Each retry waits `2^attempt * 5` seconds

#### Example Timeline

| Attempt | Status | Action |
|---------|--------|--------|
| 1 | Sent | Initial request |
| 2 | 429 | Wait 5s, retry |
| 3 | 429 | Wait 10s, retry |
| 4 | 429 | Wait 20s, retry |
| 5 | 429 | Wait 40s, retry |
| 6 | 429 | Wait 80s, then fail |

#### Rate Limiting is Transparent

- **No action required** - All MCP tools automatically handle rate limiting
- **Graceful degradation** - Returns error after max retries (not an infinite loop)
- **Logging** - Detailed warnings logged when rate limits are encountered

#### Example: Handling Rate Limits in Your Code

```python
# Rate limiting is handled automatically by the MCP server
# Your code doesn't need special handling for 429 errors

from highcommand import HighCommandTools

tools = HighCommandTools()

# This will automatically retry with exponential backoff if rate limited
response = await tools.get_war_status_tool()

if response["status"] == "error":
    # If all retries failed, this is where you see the error
    print(f"API error: {response['error']}")
else:
    # Data successfully retrieved (possibly after automatic retries)
    war_data = response["data"]
```

#### Best Practices

1. **Respect the API** - Don't make unnecessary requests
2. **Cache results** - Store data locally when possible
3. **Handle errors gracefully** - Check response status even though retries are automatic
4. **Monitor logs** - Watch for repeated 429 errors indicating consistent rate limiting

#### Configuration

The backoff behavior is configured in the upstream High-Command API:
- Base backoff: 5 seconds
- Max attempts: 5
- Max total wait time: ~155 seconds (5+10+20+40+80)

For production deployments, monitor API performance and adjust caching strategies if rate limits become frequent.

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
from highcommand.api_client import HighCommandAPIClient

async def main():
    async with HighCommandAPIClient() as client:
        war_status = await client.get_war_status()
        print(war_status['data'])

asyncio.run(main())
```

### With Error Handling and Retry

```python
import asyncio
import httpx
from highcommand.api_client import HighCommandAPIClient
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
    async with HighCommandAPIClient() as client:
        try:
            planets = await get_with_retry(client.get_planets)
            print(f"Found {len(planets['data'])} planets")
        except httpx.HTTPError as e:
            print(f"API error: {e}")

asyncio.run(main())
```

## Rate Limiting

### Automatic Exponential Backoff

The High-Command API implements **automatic exponential backoff** to handle rate limit responses (HTTP 429).

#### Backoff Strategy

When a request receives a 429 (Too Many Requests) response:

1. **Exponential delays** are applied: `5s → 10s → 20s → 40s → 80s`
2. **Up to 5 retry attempts** before failing
3. **Calculation**: Each retry waits `2^attempt * 5` seconds

#### Example Timeline

| Attempt | Status | Action |
|---------|--------|--------|
| 1 | Sent | Initial request |
| 2 | 429 | Wait 5s, retry |
| 3 | 429 | Wait 10s, retry |
| 4 | 429 | Wait 20s, retry |
| 5 | 429 | Wait 40s, retry |
| 6 | 429 | Wait 80s, then fail |

#### Rate Limiting is Transparent

- **No action required** - All MCP tools automatically handle rate limiting
- **Graceful degradation** - Returns error after max retries (not an infinite loop)
- **Logging** - Detailed warnings logged when rate limits are encountered

#### Example: Handling Rate Limits in Your Code

```python
# Rate limiting is handled automatically by the MCP server
# Your code doesn't need special handling for 429 errors

from highcommand import HighCommandTools

tools = HighCommandTools()

# This will automatically retry with exponential backoff if rate limited
response = await tools.get_war_status_tool()

if response["status"] == "error":
    # If all retries failed, this is where you see the error
    print(f"API error: {response['error']}")
else:
    # Data successfully retrieved (possibly after automatic retries)
    war_data = response["data"]
```

#### Best Practices

1. **Respect the API** - Don't make unnecessary requests
2. **Cache results** - Store data locally when possible
3. **Handle errors gracefully** - Check response status even though retries are automatic
4. **Monitor logs** - Watch for repeated 429 errors indicating consistent rate limiting

#### Configuration

The backoff behavior is configured in the upstream High-Command API:
- Base backoff: 5 seconds
- Max attempts: 5
- Max total wait time: ~155 seconds (5+10+20+40+80)

For production deployments, monitor API performance and adjust caching strategies if rate limits become frequent.

## Resources

- [HellHub Collective API](https://github.com/hellhub-collective/api)
- [HellHub Postman Collection](https://documenter.getpostman.com/view/33840175/2sA35Bd54w)
- [Helldivers 2 Game](https://store.steampowered.com/app/553850/HELLDIVERS_2/)

## Support

For issues or questions:
- Check [CONTRIBUTING.md](../CONTRIBUTING.md)
- Open an issue on GitHub
- Start a discussion
