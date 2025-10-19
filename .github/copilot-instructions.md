# High-Command: AI Development Instructions

**High-Command** is a Python MCP (Model Context Protocol) Server integrating the **HellHub Collective API** for Helldivers 2 game data.

## Architecture Essentials

### Three-Layer Design
The codebase follows a clean separation of concerns across three critical layers:

1. **API Client Layer** (`highcommand/api_client.py`)
   - **Class**: `HelldiverAPIClient` - async HTTP wrapper around HellHub API
   - **Pattern**: Async context manager (`async with client:`)
   - **Key Methods**: `get_war_status()`, `get_planets()`, `get_statistics()`, `get_planet_status(index)`, `get_biomes()`, `get_factions()`
   - **Headers**: Sets User-Agent with client_id and contact_email (no auth required)
   - **Error Handling**: Raises `RuntimeError` if used outside context manager; catches `httpx.HTTPError` for network issues

2. **Tools Wrapper Layer** (`highcommand/tools.py`)
   - **Class**: `HelldiverTools` - bridges API client to MCP server
   - **Pattern**: Instantiates API client, wraps each endpoint as `*_tool()` method
   - **Response Format**: `{"status": "success"|"error", "data": {...}, "error": "message"}`
   - **Lifecycle**: Each tool creates a NEW context manager for every call (allows parallel safe calls)

3. **MCP Server Layer** (`highcommand/server.py`)
   - **Framework**: `mcp.server.Server` with async decorators
   - **Registration**: Two critical places - `@server.list_tools()` (catalog) and `@server.call_tool()` (dispatcher)
   - **Transport**: Supports stdio and SSE transports (set via environment)

### Data Models (`highcommand/models.py`)
- **Pydantic v2** with `ConfigDict(populate_by_name=True)` for flexible aliasing
- **Key Models**: `WarInfo`, `PlanetInfo`, `Statistics`, `APIResponse[T]`, `PaginationInfo`
- **Field Aliasing**: API returns camelCase (`startDate`), models use snake_case with Field aliases
- **Pattern**: All public-facing models inherit from `BaseModel` with explicit Config class

### External API Integration
- **Base URL**: `https://api-hellhub-collective.koyeb.app/api`
- **Rate Limit**: 200 requests/minute (no throttling in code - respect in production)
- **Authentication**: None required (HellHub API is open)
- **Response Wrapper**: All endpoints return `{"data": {...}, "error": null, "pagination": {...}}`
- **6 Endpoints Implemented**: `/war`, `/planets`, `/planets/{id}`, `/statistics`, `/biomes`, `/factions`

## Development Workflows

### Implementing New Endpoints (Add-to-All Pattern)
Must update in sequence to register tools end-to-end:
1. **API Client** (`api_client.py`): Add `async def get_X(self) -> dict[str, Any]`
2. **Models** (`models.py`): Add Pydantic model if new response type
3. **Tools** (`tools.py`): Add `async def get_X_tool(self) -> dict[str, Any]`
4. **Server** (`server.py`): Register in BOTH `list_tools()` and `call_tool()` decorator blocks
5. **Tests** (`tests/test_server.py`): Add unit tests with mocked httpx
6. **Docs** (`docs/API.md`): Document tool and its response

### Testing Strategy
- **Unit Tests Only**: Real tests in `tests/test_*.py` (4 tests per file = 12 total)
- **Mocking Pattern**: Mock `httpx.AsyncClient` at context manager boundary
- **Test Async Code**: Use `@pytest.mark.asyncio` with `pytest-asyncio`
- **No Integration Tests**: Don't call real API in tests (mock everything)
- **Demo Scripts**: Scripts like `test_all_endpoints.py` are NOT unit tests - reference only

### Shell Compatibility (Critical)
- **Makefile**: Explicitly uses `SHELL := /bin/bash` - all `make` targets run in bash
- **Fish Shell Support**: User runs fish, but Makefile forces bash - transparent to user
- **Terminal Commands**: When running ad-hoc commands:
  - ✅ Use `make` targets (bash-safe)
  - ✅ Use simple Python commands: `python -m pytest tests/test_api_client.py`
  - ❌ Avoid bash-specific syntax in AI-generated terminal commands
  - ❌ Don't use line continuations `\` in commands meant to be copy-pasted

## Code Patterns (This Project Specific)

### Async Context Manager Pattern (MANDATORY)
```python
# ✅ CORRECT: Always use as context manager
async with HelldiverAPIClient() as client:
    data = await client.get_war_status()

# ❌ WRONG: Using outside context manager raises RuntimeError
client = HelldiverAPIClient()
await client.get_war_status()  # RuntimeError!
```

### Pydantic v2 Model Definition
```python
from pydantic import BaseModel, Field, ConfigDict

class MyModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)  # Allow both snake_case and camelCase
    war_id: int = Field(..., alias="warId")           # Use alias for API response keys
    created_at: datetime = Field(..., alias="createdAt")
```

### Type Hints (Always)
- Use `dict[str, Any]` (Python 3.9+), not `Dict` from typing
- Use `Optional[T]` for nullable fields
- Annotate return types on all async functions

### Logging (Use structlog)
```python
import structlog
logger = structlog.get_logger(__name__)
logger.info("Fetching data", endpoint="/war", timeout=30.0)  # Structured context
```

### Error Handling
- Catch `httpx.HTTPError` for network failures (wrap in try/except)
- Propagate as `RuntimeError` with context when critical
- Tools return `{"status": "error", "error": "message"}` - never raise exceptions to MCP

## Key Dependencies & Versions
- `mcp>=0.1.0` - Core MCP protocol
- `httpx>=0.24.0` - Async HTTP client (NOT requests)
- `pydantic>=2.0.0` - Data validation (v2, NOT v1)
- `structlog>=23.1.0` - Structured logging
- `pytest>=7.4.0`, `pytest-asyncio>=0.21.0` - Testing

## Git Workflow & Branch Protection

### Main Branch Protection Rules
The `main` branch is now protected with the following rules:
- ✅ **Require 1 PR approval** before merging
- ✅ **Require Copilot code review** (via ruleset)
- ✅ **Dismiss stale reviews** when new commits pushed
- ✅ **Enforce on admins** (rules apply to everyone including repo owner)
- ✅ **No force pushes** allowed to main
- ✅ **No branch deletions** allowed

### Required PR Workflow
```bash
# ✅ CORRECT: Feature branch → PR → Copilot review → You approve → Merge
git checkout -b feature/new-endpoint
git commit -m "feature: add endpoint"
git push origin feature/new-endpoint
gh pr create --base main --head feature/new-endpoint
# Copilot will automatically review your PR
# Once Copilot reviews, you can approve and merge:
gh pr merge <pr-number>

# ❌ WRONG: Direct push to main (will fail)
git push origin main
# Error: refusing to allow you to create or update a ref
```

### Branch Naming Convention
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `docs/*` - Documentation updates
- `refactor/*` - Code refactoring
- `chore/*` - Chores and maintenance

### Copilot Automatic Code Review

The repository is configured with **automatic Copilot code review** on all PRs to `main`:

1. **Automatic Review**: Copilot automatically reviews every pull request without manual request
2. **Configuration**: Set up via GitHub Settings → Rules → Rulesets
3. **Review Behavior**:
   - Copilot reviews on PR creation
   - Reviews new pushes to PR (if enabled in ruleset)
   - Can review draft PRs (if enabled in ruleset)

To enable Copilot auto-review on a ruleset:
```bash
# 1. Go to https://github.com/surrealwolf/high-command-mcp/settings/rules
# 2. Click the "Require Copilot Code Review" ruleset
# 3. Scroll to "Branch rules" section
# 4. Check "Automatically request Copilot code review"
# 5. Optionally enable:
#    - "Review new pushes" - review all updates to PR
#    - "Review draft pull requests" - review draft PRs
# 6. Click "Save"
```

## Build & Deployment

### Makefile Golden Rules
- **Always available targets**: `make help`, `make test`, `make lint`, `make format`, `make run`
- **Quality Gate**: `make check-all` (format + lint + test)
- **Never fails**: Running `make` commands is always safe - they're idempotent
- **Python Resolution**: Makefile auto-detects venv if present, falls back to system Python

### Docker
- **Dockerfile**: Multi-stage build not used (simple, ~80 lines)
- **Base Image**: `python:3.14-slim`
- **Non-root User**: Runs as `appuser` (uid 1000) for security
- **Entrypoint**: `python -m highcommand.server` (starts MCP on stdio)

### CI/CD
- **GitHub Actions**: `.github/workflows/tests.yml` and `docker.yml`
- **Test Matrix**: Multiple Python versions (3.9, 3.10, 3.11, 3.12, 3.13)
- **Coverage**: Pytest-cov configured in pyproject.toml

## File Organization Quick Reference

| File | Purpose | Key Patterns |
|------|---------|--------------|
| `highcommand/api_client.py` | HTTP client to HellHub API | Async context manager, httpx.AsyncClient |
| `highcommand/tools.py` | MCP tool implementations | Wraps API client, `*_tool()` methods |
| `highcommand/server.py` | MCP server registration | Decorators `@server.list_tools()`, `@server.call_tool()` |
| `highcommand/models.py` | Pydantic data models | `ConfigDict(populate_by_name=True)`, Field aliases |
| `tests/test_api_client.py` | API client tests | Mock httpx, async tests |
| `tests/test_server.py` | MCP server tests | Mock HelldiverTools, test tool calling |
| `pyproject.toml` | Project config | Dependencies, tool configs (black, ruff, mypy, pytest) |
| `Makefile` | Development tasks | 15+ targets, bash-enforced |

## Common Tasks

### Create a PR for New Work
```bash
# 1. Create and switch to feature branch
git checkout -b feature/descriptive-name

# 2. Make your changes and commit
git commit -m "feature: clear description"

# 3. Push to remote
git push origin feature/descriptive-name

# 4. Create PR (will need 1 approval before merging)
gh pr create --base main --head feature/descriptive-name

# 5. After approval, merge to main
gh pr merge <pr-number>
```

### Run All Checks Before Committing
```bash
make check-all  # Runs format + lint + test in one shot
```

### Debug a Failing Test
```bash
pytest tests/test_api_client.py::test_name -vvv --tb=short
```

### Check What Changed
```bash
git diff highcommand/  # See code changes
make format  # Auto-fix style issues
```

### Add New Tool to MCP
1. Implement `async def method(self)` in `HelldiverAPIClient`
2. Implement `async def method_tool(self)` in `HelldiverTools`
3. Add to `server.py` list_tools() return list
4. Add to `server.py` call_tool() if/elif chain (match on tool name)
5. Add unit test in `tests/test_server.py`
6. Run `make test` to verify 12/12 pass

### Check Test Coverage
```bash
pytest --cov=highcommand --cov-report=html  # Opens htmlcov/index.html
```

## Important Notes

1. **No Authentication**: HellHub API is public - no API keys, tokens, or auth headers
2. **Rate Limiting**: 200 req/min (respect in production; ignore for now)
3. **All Async**: Every I/O operation uses async/await - no sync calls
4. **Pydantic v2**: Older v1 syntax won't work - use `ConfigDict`, `Field`, not `Config` class
5. **Package Name**: `highcommand`, NOT `mcp` (avoids shadowing the mcp SDK import)
6. **Test Coverage**: Currently 100% on implemented code - maintain for new features
7. **Type Checking**: `mypy` configured in pyproject.toml - all functions need type hints
8. **Format on Save**: Black line-length is 100 chars - configure your editor

## Documentation Quick Links

- **Setup**: `docs/SETUP.md` - Installation, venv, dependencies
- **API Reference**: `docs/API.md` - All tool signatures and responses
- **Contributing**: `CONTRIBUTING.md` - PR process, code style
- **Project Status**: `docs/PROJECT_STATUS.md` - Completion checklist
- **This File**: `.github/copilot-instructions.md` - You are here

## Project Status

✅ **Production Ready** - All 6 API endpoints implemented, 12/12 tests passing, full Docker support, CI/CD workflows active.

---

**Last Updated**: October 19, 2025  
**Version**: 1.0.0  
**Python**: 3.9+ (tested on 3.14.0)  
**Status**: Production Ready 🟢
