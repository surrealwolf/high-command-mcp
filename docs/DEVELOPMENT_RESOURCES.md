# High-Command MCP - Development Resources

Comprehensive resources for working with the High-Command MCP Server project.

## Documentation Index

### Getting Started
- **SETUP.md** - Installation, Python environment setup, dependencies
- **GETTING_STARTED.md** - Quick start guide for first contribution
- **README.md** - Project overview and quick reference

### Development Guides
- **CONTRIBUTING.md** - Contribution process and code standards
- **.github/copilot-instructions.md** - Architectural decisions and patterns
- **docs/DEVELOPMENT_PROMPTS.md** - System prompts for AI-assisted development

### Technical Documentation
- **docs/API.md** - Tool specifications and response formats
- **docs/CODE_REVIEW.md** - Comprehensive code review findings and recommendations
- **docs/PROJECT_STATUS.md** - Feature completion checklist

### Code Examples

#### Example 1: Implementing a New Tool

```python
# Step 1: Add to API Client (highcommand/api_client.py)
async def get_new_endpoint(self) -> dict[str, Any]:
    """Get new endpoint data."""
    if not self._client:
        raise RuntimeError("Client not initialized. Use as async context manager.")
    
    logger.info("Fetching new endpoint")
    response = await self._client.get("/api/new-endpoint")
    return await self._handle_response(response, "/api/new-endpoint")

# Step 2: Add to Tools (highcommand/tools.py)
async def get_new_endpoint_tool(self) -> dict[str, Any]:
    """Tool to get new endpoint data."""
    async def _fetch() -> Any:
        async with HighCommandAPIClient() as client:
            return await client.get_new_endpoint()
    
    return await self._run_tool(_fetch)

# Step 3: Register in Server (highcommand/server.py)
# In list_tools():
Tool(
    name="get_new_endpoint",
    description="Get new endpoint data",
    inputSchema={"type": "object", "properties": {}, "required": []},
)

# In call_tool():
elif name == "get_new_endpoint":
    result = await tools.get_new_endpoint_tool()

# Step 4: Write tests (tests/test_server.py)
@pytest.mark.asyncio
async def test_get_new_endpoint():
    with patch("highcommand.api_client.httpx.AsyncClient") as mock_client:
        mock_response = Mock()
        mock_response.json.return_value = {"data": "value"}
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        
        tools = HighCommandTools()
        result = await tools.get_new_endpoint_tool()
        
        assert result["status"] == "success"
        assert result["data"]["data"] == "value"
```

#### Example 2: Adding a Pydantic Model

```python
from pydantic import BaseModel, ConfigDict, Field

class NewEndpointInfo(BaseModel):
    """Information from new endpoint."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    id: int
    name: str
    description: str
    createdAt: datetime = Field(..., alias="createdAt")
    updatedAt: datetime = Field(..., alias="updatedAt")
    metadata: dict[str, Any] = Field(default_factory=dict)
```

#### Example 3: Error Handling in API Client

```python
async def _handle_response(
    self, response: httpx.Response, endpoint: str
) -> dict[str, Any]:
    """Handle API response with error categorization."""
    try:
        response.raise_for_status()
        elapsed_ms = response.elapsed.total_seconds() * 1000
        logger.info("API request succeeded", endpoint=endpoint, elapsed_ms=elapsed_ms)
        return response.json()
    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code
        
        if 500 <= status_code < 600:
            logger.warning("Server error", endpoint=endpoint, status=status_code)
        elif status_code == 429:
            logger.warning("Rate limit exceeded", endpoint=endpoint)
        else:
            logger.error("Client error", endpoint=endpoint, status=status_code)
        
        raise RuntimeError(f"HTTP error ({status_code})") from e
```

#### Example 4: Using Tool Registry

```python
from highcommand.tool_registry import ToolDefinition, ToolParameter, ToolRegistry

# Create registry
registry = ToolRegistry()

# Define tool
params = [
    ToolParameter(
        name="planet_index",
        type="integer",
        description="Index of the planet",
        required=True,
    )
]

tool = ToolDefinition(
    name="get_planet_status",
    description="Get planet status",
    handler=tools.get_planet_status_tool,
    parameters=params,
)

# Register
registry.register(tool)

# Validate and retrieve
validated_tool = registry.validate_and_get("get_planet_status", {"planet_index": 0})

# Generate MCP schema
schema = tool.to_input_schema()
```

## Testing Resources

### Running Tests
```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_api_client.py -v

# Run with coverage
pytest --cov=highcommand --cov-report=html

# Run specific test
pytest tests/test_server.py::test_list_tools -v

# Run with detailed output
pytest tests/ -vvv --tb=long
```

### Mocking httpx for Tests
```python
from unittest.mock import Mock, patch
import pytest

@pytest.mark.asyncio
async def test_api_call():
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
        
        # Test code here
```

## Debugging Tips

### Enable Verbose Logging
```bash
LOG_LEVEL=DEBUG python -m highcommand.server
```

### Check API Client Initialization
```python
import asyncio
from highcommand.api_client import HighCommandAPIClient

async def test():
    try:
        async with HighCommandAPIClient() as client:
            data = await client.get_war_status()
            print(data)
    except RuntimeError as e:
        print(f"Error: {e}")

asyncio.run(test())
```

### Validate Pydantic Models
```python
from highcommand.models import WarInfo

data = {
    "id": 1,
    "index": 801,
    "startDate": "2024-01-23T20:05:13.000Z",
    "endDate": "2028-02-08T20:04:55.000Z",
    "time": "2024-01-23T20:05:13.000Z",
    "createdAt": "2024-01-23T20:05:13.000Z",
    "updatedAt": "2024-01-23T20:05:13.000Z",
}

try:
    war = WarInfo.model_validate(data)
    print(war)
except ValidationError as e:
    print(e.json())
```

### Profile Tool Performance
```python
import time

async def profile_tool():
    start = time.perf_counter()
    result = await tools.get_war_status_tool()
    elapsed = time.perf_counter() - start
    print(f"Executed in {elapsed * 1000:.2f}ms")
    if "metrics" in result:
        print(f"Tool metrics: {result['metrics']}")
```

## Environment Variables

### Required
- None (API is public)

### Optional
| Variable | Default | Purpose |
|----------|---------|---------|
| HIGH_COMMAND_API_BASE_URL | http://localhost:5000 | High-Command API endpoint |
| LOG_LEVEL | INFO | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |
| MCP_TRANSPORT | stdio | Transport mode (stdio, http, sse) |
| ENVIRONMENT | development | Environment (development, production) |
| MCP_HOST | 0.0.0.0 | HTTP server host |
| MCP_PORT | 8000 | HTTP server port |
| MCP_WORKERS | 4 | HTTP server workers |

### Setting Environment Variables

**Bash/Zsh:**
```bash
export LOG_LEVEL=DEBUG
export HIGH_COMMAND_API_BASE_URL=https://api.example.com
python -m highcommand.server
```

**Fish Shell:**
```fish
set -x LOG_LEVEL DEBUG
set -x HIGH_COMMAND_API_BASE_URL https://api.example.com
python -m highcommand.server
```

**.env file:**
```
HIGH_COMMAND_API_BASE_URL=http://localhost:5000
LOG_LEVEL=INFO
MCP_TRANSPORT=stdio
ENVIRONMENT=development
```

## Makefile Targets

| Target | Purpose |
|--------|---------|
| make help | Show all available targets |
| make test | Run unit tests |
| make lint | Run linters (ruff, mypy) |
| make format | Auto-format code with black |
| make check-all | Run format + lint + test |
| make run | Start MCP server |
| make docker-build | Build Docker image |
| make docker-run | Run Docker container |
| make clean | Clean temporary files |

## Repository Structure Explained

```
high-command-mcp/
├── highcommand/              # Main package
│   ├── __init__.py
│   ├── api_client.py        # HTTP client to High-Command API
│   ├── tools.py              # MCP tool implementations
│   ├── server.py             # MCP server with tool registration
│   ├── models.py             # Pydantic data models
│   └── tool_registry.py      # Tool registry (NEW)
├── tests/                    # Unit tests
│   ├── test_api_client.py   # API client tests
│   ├── test_tools.py        # Tools tests (if exists)
│   ├── test_server.py       # Server tests
│   ├── test_models.py       # Model validation tests
│   └── test_tool_registry.py # Registry tests (NEW)
├── docs/                     # Documentation
│   ├── API.md                # Tool specifications
│   ├── CODE_REVIEW.md        # Code review findings (NEW)
│   ├── DEVELOPMENT_PROMPTS.md # AI prompts (NEW)
│   ├── SETUP.md              # Installation guide
│   └── PROJECT_STATUS.md     # Feature checklist
├── k8s/                      # Kubernetes configs
├── .github/                  # GitHub workflows and configs
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Local development setup
├── Makefile                  # Development tasks
├── pyproject.toml            # Project configuration
└── README.md                 # Project overview
```

## Common Development Workflows

### Adding a Feature
1. Create feature branch: `git checkout -b feature/your-feature`
2. Implement changes (follow Add-to-All pattern)
3. Write tests: `make test`
4. Check code quality: `make check-all`
5. Commit and push
6. Create PR and wait for Copilot review
7. Once approved, merge to main

### Fixing a Bug
1. Create bugfix branch: `git checkout -b bugfix/issue-description`
2. Write failing test first
3. Implement fix in appropriate layer
4. Verify test passes
5. Run full test suite: `make test`
6. Commit with reference to issue
7. Create PR

### Running Locally
1. Install dependencies: `make install`
2. Start High-Command API (if testing integration)
3. Run MCP server: `make run`
4. In another terminal, test tools

### Deploying to Kubernetes
1. Build image: `make docker-build`
2. Push to registry
3. Update k8s deployment manifests
4. Apply with `kubectl apply -f k8s/`

## Performance Benchmarks

Current baseline performance (on 3.13.7):
- War status fetch: ~50-100ms (API dependent)
- Tool response latency: <200ms average
- Concurrent requests: Handles 10+ concurrent calls
- Memory usage: ~50-80MB at rest

## External References

- [MCP Protocol](https://modelcontextprotocol.io/)
- [Pydantic v2 Docs](https://docs.pydantic.dev/2.0/)
- [httpx Documentation](https://www.python-httpx.org/)
- [structlog Documentation](https://www.structlog.org/)
- [Helldivers 2 Official](https://www.helldivers2.com/)

## Getting Help

1. Check existing documentation in docs/
2. Review CODE_REVIEW.md for architectural decisions
3. Check .github/copilot-instructions.md for patterns
4. Look at existing tests for examples
5. Enable DEBUG logging to trace issues

---

**Last Updated**: October 21, 2025  
**Maintained By**: Development Team  
**Status**: Current and Complete
