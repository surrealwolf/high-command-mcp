# High-Command Development Instructions for GitHub Copilot

## Project Overview

**High-Command** is a Python MCP (Model Context Protocol) Server that integrates with the **HellHub Collective API** for Helldivers 2 game data.

### Key Technologies
- **Language**: Python 3.14.0
- **Framework**: MCP Server (async/await)
- **API Client**: httpx (async HTTP)
- **Data Validation**: Pydantic v2
- **Testing**: pytest + pytest-asyncio
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **API Source**: HellHub Collective (https://api-hellhub-collective.koyeb.app/api, 200 req/min limit)

## Project Structure

```
high-command/
├── highcommand/                   # Main MCP Server Package
│   ├── __init__.py               # Package exports
│   ├── server.py                 # MCP Server (@server.list_tools, @server.call_tool)
│   ├── api_client.py             # HellHub API Client (async context manager)
│   ├── models.py                 # Pydantic v2 models
│   └── tools.py                  # MCP Tools wrapper (async methods)
├── tests/                        # Test Suite (unit tests)
│   ├── test_api_client.py        # API client tests (4/4 passing)
│   ├── test_models.py            # Model validation tests (4/4 passing)
│   ├── test_server.py            # MCP server tests (4/4 passing)
│   ├── test_all_endpoints.py     # All endpoints demo
│   ├── test_new_endpoints.py     # New endpoint tests
│   └── test_imports.py           # Import verification
├── docs/                         # Project Documentation
│   ├── API.md                    # API endpoint documentation
│   ├── SETUP.md                  # Setup and installation guide
│   ├── ENDPOINT_EXPANSION.md     # Endpoint expansion changelog
│   ├── PROJECT_STATUS.md         # Project completion status
│   ├── PROJECT_SUMMARY.md        # High-level project summary
│   ├── GETTING_STARTED.md        # Quick start guide
│   ├── CONTRIBUTING.md           # Contribution guidelines
│   └── ITERATION_SUMMARY.md      # Development iteration notes
├── .github/
│   ├── copilot-instructions.md   # This file
│   └── workflows/
│       ├── tests.yml             # Test CI/CD
│       └── docker.yml            # Docker build CI/CD
├── scripts/                      # Utility scripts
│   └── ...                       # Build and deployment helpers
├── Makefile                      # Development tasks
├── Dockerfile                    # Container definition
├── docker-compose.yml            # Docker Compose config
├── pyproject.toml                # Python project config
├── README.md                     # Project README
└── .env.example                  # Environment variables template
```

## API Endpoints (6/6 Implemented)

### Currently Implemented
1. ✅ `/war` - GET war status (230 B)
2. ✅ `/planets` - GET all planets (7.7 KB, ~261 planets)
3. ✅ `/planets/{id}` - GET specific planet (518 B)
4. ✅ `/statistics` - GET global statistics (5.7 KB)
5. ✅ `/biomes` - GET biome/terrain data (3.8 KB) **NEW**
6. ✅ `/factions` - GET faction data (431 B) **NEW**

### MCP Tools (7 Total)
1. `get_war_status` - Returns current war data
2. `get_planets` - Returns list of planets
3. `get_planet_status` - Returns specific planet details (requires: planet_index)
4. `get_statistics` - Returns global game statistics
5. `get_biomes` - Returns biome information **NEW**
6. `get_factions` - Returns faction information **NEW**
7. `get_campaign_info` - Returns error (endpoint 404)

## Code Patterns & Conventions

### Async/Await Pattern
All API calls use async/await. Always use as context manager:

```python
async with HellHub API Client() as client:
    data = await client.get_war_status()
```

### Error Handling
- Catch `httpx.HTTPError` for network issues
- Raise `RuntimeError` if client used outside context
- Use structlog for logging
- Return graceful error responses in tools

### Type Hints
Always include type hints:
```python
async def get_war_status(self) -> Dict[str, Any]:
    ...
```

### Pydantic v2 Models
Use BaseModel for data validation:
```python
from pydantic import BaseModel, ConfigDict, Field

class WarInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    war_id: int = Field(..., alias="warId")
```

### MCP Tools Response Format
```python
{
    "status": "success"|"error",
    "data": {...},
    "error": "message" # Only if status is error
}
```

## Development Workflow

### Setup
```bash
make help                   # Show all available commands
make venv                   # Create virtual environment (optional, dev/install do this automatically)
make install                # Install package in development mode
make dev                    # Install dev dependencies
make format                 # Auto-format code (black, ruff)
make lint                   # Check code quality
make test                   # Run tests with coverage (12/12 passing ✅)
make run                    # Run the MCP server
```

### Important: Shell Compatibility
- **Makefile uses bash**: All Makefile commands execute with bash shell (not fish/sh)
- **Terminal commands**: When running terminal commands from Python/scripts:
  - Use single-line commands or semicolons for multi-line operations
  - Avoid bash-specific syntax like line continuations with backslash
  - Example: `python3 -c "..." && python3 -m pytest` (good)
  - Example: `python3 \n-c "..."` (bad - not portable)
- **Fish shell compatibility**: Test all terminal commands work in fish shell
  - Wrap complex commands in `bash -c 'command'` if needed
  - Use `; and` instead of `&&` in fish
  - Example for multi-command: Use `make` targets instead of complex one-liners

### Adding New API Endpoint
1. Add method to `HellHubAPIClient` in `highcommand/api_client.py`
2. Add Pydantic model in `highcommand/models.py` if needed
3. Add tool method in `highcommand/tools.py`
4. Register tool in `highcommand/server.py` (2 places: list_tools + call_tool)
5. Write tests in `tests/` (unit tests only)
6. Update docs in `docs/API.md`
7. Run: `make test` (ensure 12/12 tests still passing)

### Test Organization
- **Unit tests only**: All tests in `tests/` folder
- **Test scripts**: Demonstration scripts in root or `scripts/` (not unit tests)
- Examples: `test_all_endpoints.py`, `verify_project.py` are demo scripts, not pytest fixtures
- Run unit tests: `pytest tests/` (shows 4+4+4=12 tests)

### Testing
- Use `pytest` and `pytest-asyncio` for async tests
- Use `unittest.mock` for mocking external dependencies
- Aim for >80% coverage (currently: 100% on implemented code)
- Run: `make test`

## Current Test Status

**All 12 Unit Tests Passing ✅**

```
tests/test_api_client.py   4/4 ✅
tests/test_models.py       4/4 ✅
tests/test_server.py       4/4 ✅
────────────────────────────────
TOTAL                     12/12 ✅
```

## Key APIs & Methods

### HellHubAPIClient

Interfaces with HellHub Collective API:

```python
class HellHubAPIClient:
    BASE_URL = "https://api-hellhub-collective.koyeb.app/api"
    
    async def get_war_status() -> Dict[str, Any]           # GET /war
    async def get_planets() -> Dict[str, Any]              # GET /planets
    async def get_statistics() -> Dict[str, Any]           # GET /statistics
    async def get_planet_status(index: int) -> Dict        # GET /planets/{index}
    async def get_biomes() -> Dict[str, Any]               # GET /biomes (NEW)
    async def get_factions() -> Dict[str, Any]             # GET /factions (NEW)
```

### HellCommandTools

```python
class HellCommandTools:
    async def get_war_status_tool() -> Dict[str, Any]
    async def get_planets_tool() -> Dict[str, Any]
    async def get_statistics_tool() -> Dict[str, Any]
    async def get_planet_status_tool(planet_index: int) -> Dict[str, Any]
    async def get_biomes_tool() -> Dict[str, Any]
    async def get_factions_tool() -> Dict[str, Any]
    async def get_campaign_info_tool() -> Dict[str, Any]  # Returns error
```

## Environment Variables

- `LOG_LEVEL`: Logging level (default: "INFO")

Note: HellHub API requires NO authentication (no headers, API keys, or bot tokens).

## Documentation Files

All documentation moved to `docs/`:
- `docs/API.md` - Full API endpoint reference
- `docs/SETUP.md` - Installation and setup instructions
- `docs/ENDPOINT_EXPANSION.md` - Changelog of added endpoints
- `docs/PROJECT_STATUS.md` - Project completion report
- `docs/PROJECT_SUMMARY.md` - Executive summary
- `docs/GETTING_STARTED.md` - Quick start guide
- `docs/CONTRIBUTING.md` - How to contribute
- `docs/ITERATION_SUMMARY.md` - Development notes

## Terminal Command Best Practices

### For GitHub Copilot Terminal Execution

When using run_in_terminal tool, follow these guidelines:

#### Use Makefile Targets
Always use `make` targets for all operations:
- ✅ `make test` - Run tests with coverage
- ✅ `make check-all` - Format, lint, and test
- ✅ `make commit-changes` - Stage, commit, and show status
- ✅ `make release` - Full quality gate before release
- ✅ `make help` - Show all available targets

Makefile enforces bash shell (`SHELL := /bin/bash`), ensuring cross-shell compatibility.

#### Simple Python Commands
Direct Python commands work for straightforward operations:
- ✅ `python -m pytest tests/test_api_client.py`
- ✅ `python3 --version`
- ✅ `python -m highcommand.server`

#### For Everything Else
Create a new Make target instead of complex shell commands.

#### Available Make Targets

| Target | Purpose |
|--------|---------|
| `make help` | Show all targets |
| `make install` | Install dependencies |
| `make dev` | Install development tools |
| `make test` | Run tests with coverage |
| `make test-fast` | Run tests without coverage |
| `make lint` | Run linters (ruff, mypy) |
| `make format` | Format code with black and ruff |
| `make check-all` | Format + lint + test |
| `make commit-changes` | Add, commit, show status |
| `make release` | Full quality validation |
| `make clean` | Remove build artifacts |
| `make run` | Run MCP server |
| `make docker-build` | Build Docker image |
| `make docker-run` | Run Docker container |
| `make docs` | Build documentation |
| `make docs-serve` | Serve docs locally |

#### Summary for AI Assistant

**Golden Rule:** Prefer `make` targets for all operations

1. Check if make target exists → Use `make target`
2. Otherwise → Use simple Python command or create a new target
3. Never use complex shell commands directly

This ensures 100% compatibility with all shell environments.

## Common Tasks

### Add a new API endpoint
```bash
# Step 1: Update API client
# Edit: highcommand/api_client.py
async def get_new_endpoint(self) -> Dict[str, Any]:
    logger.info("Fetching new endpoint")
````elif name == "get_new_endpoint":
    return await self.tools.get_new_endpoint_tool()
```

### Fix linting errors
```bash
make format       # Auto-fix with black and ruff
make lint         # Check for remaining issues
```

### Run specific tests
```bash
pytest tests/test_api_client.py -v
pytest tests/test_api_client.py::test_function_name -v
pytest tests/ -v  # Run all unit tests
```

### Debug issues
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Important Notes

1. **Package renamed**: `mcp/` → `highcommand/` (avoids import shadowing with MCP SDK)
2. **Always use async context manager** with HellHubAPIClient
3. **Handle httpx errors** properly in API client
4. **Include type hints** in all functions
5. **Add docstrings** to public methods
6. **Test async code** with pytest-asyncio
7. **Mock external HTTP calls** in tests
8. **Use Pydantic v2** with ConfigDict for configuration
9. **Format code** before committing (`make format`)
10. **Response format**: HellHub returns `{"data": {...}, "error": null, "pagination": {...}}`
11. **No authentication**: HellHub API doesn't require special headers
12. **Rate limit**: 200 requests per minute
13. **Test organization**: Unit tests in `tests/`, demo scripts in root

## Useful Commands

```bash
make help                    # Show all available commands
make install                 # Install package
make dev                     # Install dev dependencies
make run                     # Run the MCP server
make test                    # Run unit tests with coverage (12/12 passing ✅)
make test-fast               # Run tests without coverage
make lint                    # Check code quality
make format                  # Format code
make clean                   # Clean build artifacts
make docker-build            # Build Docker image
make docker-run              # Run Docker container
make check                   # Run linters and tests
venv/bin/python3 verify_project.py  # Full project verification
```

## Git Commit Best Practices

When committing changes, use simple single-line commands for reliability:

```bash
# ✅ GOOD: Simple commit with single-line message
git commit -m "fix: update Python version to 3.14"

# ✅ GOOD: Use git commit -m with simple message, then git commit --amend for details
git add file.txt; git commit -m "feature: add new feature"

# ❌ BAD: Multi-line commit messages with complex escaping
git commit -m "feature: long description
with multiple lines"

# ❌ BAD: Complex commit messages with special characters
git commit -m "fix: update version (3.13 -> 3.14)"
```

For detailed commit messages:
```bash
# Use git commit with -m for summary, or use editor for full message
git add .; git commit -m "feature: short summary" && git log -1
```

Pro tip: Use descriptive single-line messages that are clear and concise. If more detail is needed, the git commit --amend or interactive rebase can provide it later.

## Resources

- [Python asyncio docs](https://docs.python.org/3/library/asyncio.html)
- [httpx documentation](https://www.python-httpx.org/)
- [Pydantic v2 docs](https://docs.pydantic.dev/latest/)
- [pytest documentation](https://docs.pytest.org/)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [HellHub API](https://hellhub-collective.gitbook.io/)

## Project Status

**✅ PRODUCTION READY**

- ✅ All 6 API endpoints implemented
- ✅ 7 MCP tools registered
- ✅ 12/12 unit tests passing
- ✅ 100% endpoint coverage
- ✅ Full documentation
- ✅ Docker support
- ✅ CI/CD workflows

---

**Last Updated**: October 19, 2025
**Version**: 1.0.0
**Python**: 3.14.0
**Status**: Production Ready 🟢
