# High-Command MCP - Quick Reference Card

**Version**: 1.0.0 | **Status**: Production Ready | **Last Updated**: October 25, 2025

---

## Architecture at a Glance

```
┌─────────────────────────────────────────────────────┐
│  MCP Server (server.py)                              │
│  - @list_tools() decorator                           │
│  - @call_tool() dispatcher                           │
└─────────────────────────────────────────────────────┘
                        ↑
┌─────────────────────────────────────────────────────┐
│  Tools Wrapper (tools.py)                            │
│  - get_X_tool() methods                              │
│  - _run_tool() helper with error handling            │
└─────────────────────────────────────────────────────┘
                        ↑
┌─────────────────────────────────────────────────────┐
│  API Client (api_client.py)                          │
│  - Async context manager                             │
│  - _handle_response() with error categorization      │
│  - get_X() methods for each endpoint                 │
└─────────────────────────────────────────────────────┘
```

---

## Essential Code Patterns

### API Client Usage (MANDATORY)
```python
# ALWAYS use async context manager
async with HighCommandAPIClient() as client:
    data = await client.get_war_status()
    # ✅ Correct - client auto-closed

# NEVER use outside context manager
client = HighCommandAPIClient()
await client.get_war_status()  # ❌ RuntimeError
```

### Tool Implementation Pattern
```python
# Step 1: Add to API Client
async def get_new_endpoint(self) -> dict[str, Any]:
    if not self._client:
        raise RuntimeError("Client not initialized...")
    response = await self._client.get("/api/endpoint")
    return await self._handle_response(response, "/api/endpoint")

# Step 2: Add to Tools
async def get_new_endpoint_tool(self) -> dict[str, Any]:
    async def _fetch() -> Any:
        async with HighCommandAPIClient() as client:
            return await client.get_new_endpoint()
    return await self._run_tool(_fetch)

# Step 3: Register in Server list_tools()
Tool(name="get_new_endpoint", description="...", inputSchema={...})

# Step 4: Dispatch in Server call_tool()
elif name == "get_new_endpoint":
    result = await tools.get_new_endpoint_tool()
```

### Pydantic Model Pattern
```python
from pydantic import BaseModel, ConfigDict, Field

class MyModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    field_name: str
    snake_case_field: int = Field(..., alias="snakeCaseField")
    optional_list: list[str] = Field(default_factory=list)
    optional_dict: dict[str, Any] = Field(default_factory=dict)
```

### Error Response Format
```python
# Success
{"status": "success", "data": {...}, "error": None}

# Error
{"status": "error", "data": None, "error": "ErrorType: description"}

# With metrics (optional)
{"status": "success", "data": {...}, "error": None, "metrics": {"elapsed_ms": 45.2}}
```

---

## Common Tasks Cheat Sheet

| Task | Command |
|------|---------|
| Install deps | `pip install -e ".[dev]"` |
| Run tests | `pytest tests/` or `make test` |
| Run server | `python -m highcommand.server` or `make run` |
| Format code | `black highcommand/ tests/` or `make format` |
| Lint code | `ruff check highcommand/ tests/` or `make lint` |
| Check all | `make check-all` (format + lint + test) |
| Build Docker | `docker build -t high-command .` or `make docker-build` |
| Enable debug | `LOG_LEVEL=DEBUG python -m highcommand.server` |
| Run specific test | `pytest tests/test_file.py::test_name -v` |
| Test with coverage | `pytest --cov=highcommand --cov-report=html` |

---

## Configuration Reference

### Environment Variables
```bash
# API Configuration
HIGH_COMMAND_API_BASE_URL=http://localhost:5000  # or https:// for production

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR

# MCP Transport
MCP_TRANSPORT=stdio  # stdio, http, sse

# Deployment
ENVIRONMENT=development  # development, production

# HTTP Server (if using http transport)
MCP_HOST=0.0.0.0
MCP_PORT=8000
MCP_WORKERS=4
```

### Setting Environment Variables

**Bash/Zsh:**
```bash
export HIGH_COMMAND_API_BASE_URL=http://localhost:5000
python -m highcommand.server
```

**Fish:**
```fish
set -x HIGH_COMMAND_API_BASE_URL http://localhost:5000
python -m highcommand.server
```

**.env file:**
```
HIGH_COMMAND_API_BASE_URL=http://localhost:5000
LOG_LEVEL=INFO
```

---

## Available Tools

| Tool | Parameters | Purpose |
|------|-----------|---------|
| `get_war_status` | None | Get current war status |
| `get_planets` | None | Get all planets |
| `get_planet_status` | `planet_index: int` | Get specific planet status |
| `get_statistics` | None | Get global statistics |
| `get_campaign_info` | None | Get active campaign |
| `get_biomes` | None | Get biome data |
| `get_factions` | None | Get faction data |

---

## Troubleshooting Quick Fixes

| Error | Fix |
|-------|-----|
| "Client not initialized" | Use `async with HighCommandAPIClient() as client:` |
| "Connection refused" | Check `HIGH_COMMAND_API_BASE_URL` and ensure API running |
| "Rate limit exceeded" | Add delay between requests or check rate limits |
| "HTTP 500" | Check API logs: `docker logs high-command-api` |
| "Mutable default" | Use `Field(default_factory=dict)` not `= {}` |
| "Type Error" | Ensure function is `async def`, not `def` |
| "ModuleNotFoundError" | Run `pip install -e ".[dev]"` |
| "HTTPS validation" | Set `ENVIRONMENT=development` or use HTTPS URL |

---

## Documentation Quick Links

| Resource | Purpose |
|----------|---------|
| README.md | Project overview |
| SETUP.md | Installation and setup |
| docs/API.md | Tool specifications |
| CONTRIBUTING.md | Contributing guidelines |
| docs/CODE_REVIEW.md | Architecture and findings |
| docs/DEVELOPMENT_PROMPTS.md | AI assistant prompts |
| docs/DEVELOPMENT_RESOURCES.md | Development guide |
| docs/TROUBLESHOOTING.md | Troubleshooting guide |
| .github/copilot-instructions.md | Code patterns and best practices |

---

## Testing Quick Guide

```python
# Test async function with mocking
import pytest
from unittest.mock import Mock, patch

@pytest.mark.asyncio
async def test_my_tool():
    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client:
        # Setup mock
        mock_response = Mock()
        mock_response.json.return_value = {"key": "value"}
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.1
        
        # Configure context manager
        mock_instance = Mock()
        mock_instance.__aenter__.return_value.get.return_value = mock_response
        mock_instance.__aexit__.return_value = None
        mock_client.return_value = mock_instance
        
        # Test code
        tools = HighCommandTools()
        result = await tools.get_war_status_tool()
        
        assert result["status"] == "success"
        assert "data" in result
```

---

## File Locations

| File | Location | Purpose |
|------|----------|---------|
| API Client | `highcommand/api_client.py` | HTTP requests to High-Command API |
| Tools | `highcommand/tools.py` | MCP tool implementations |
| Server | `highcommand/server.py` | MCP server registration |
| Models | `highcommand/models.py` | Pydantic data models |
| Registry | `highcommand/tool_registry.py` | Tool registry (NEW) |
| Tests | `tests/` | Unit test files |
| Docs | `docs/` | Documentation |
| Config | `pyproject.toml` | Project configuration |

---

## HTTP Status Code Meanings

| Code | Category | Meaning | Solution |
|------|----------|---------|----------|
| 200 | Success | Request succeeded | N/A |
| 400-499 | Client Error | Bad request or not found | Check endpoint/parameters |
| 429 | Rate Limit | Too many requests | Wait and retry later |
| 500-599 | Server Error | API server error | Check API logs |

---

## Performance Benchmarks

- **Avg Response Time**: 50-100ms (API-dependent)
- **Tool Execution**: <200ms avg
- **Concurrent Calls**: 10+ concurrent safely
- **Memory**: ~50-80MB at rest
- **Container Build**: ~2-3 minutes

---

## Pro Tips

💡 **Tip 1: Use DEBUG Logging**
```bash
LOG_LEVEL=DEBUG python -m highcommand.server
# See detailed request/response info and timings
```

💡 **Tip 2: Test with Mock First**
Always test with mocked httpx, not real API calls

💡 **Tip 3: Check Coverage**
```bash
pytest --cov=highcommand --cov-report=html
# Open htmlcov/index.html to see coverage
```

💡 **Tip 4: Use Type Hints**
All functions need type hints for mypy validation

💡 **Tip 5: Structured Logging**
Use keyword args: `logger.info("message", key=value)` not `%` formatting

---

## Version Info

- **Python**: 3.9+ (tested on 3.12.3)
- **MCP SDK**: 0.1.0+
- **httpx**: 0.24.0+
- **Pydantic**: 2.0.0+
- **structlog**: 23.1.0+

---

**Quick Links:**
- 🏠 [Home](README.md)
- 🚀 [Setup](docs/SETUP.md)
- 📚 [API Docs](docs/API.md)
- 🐛 [Troubleshooting](docs/TROUBLESHOOTING.md)
- 💻 [Development](docs/DEVELOPMENT_RESOURCES.md)

**Need Help?** Check TROUBLESHOOTING.md or enable DEBUG logging!

---

*Keep this card nearby for quick reference during development!*
