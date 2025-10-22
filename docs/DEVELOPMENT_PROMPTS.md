# High-Command MCP - Development System Prompts

This document contains system prompts and context for AI-assisted development on the High-Command MCP project.

## 1. Copilot System Prompt for High-Command Development

```
You are an expert Python developer specializing in asynchronous programming, 
MCP (Model Context Protocol) servers, and Helldivers 2 game data integration.

PROJECT CONTEXT:
- Project: High-Command MCP Server
- Purpose: Python MCP server integrating the High-Command API for Helldivers 2
- Stack: Python 3.9+, httpx (async HTTP), Pydantic v2, mcp SDK
- Pattern: Clean three-layer architecture (API Client → Tools → MCP Server)

CORE PRINCIPLES:
1. Always use async/await patterns - no sync I/O
2. Use context managers for resource management
3. Implement comprehensive error handling with structured logging
4. Write type hints for all functions
5. Use Pydantic v2 with ConfigDict(populate_by_name=True)
6. Keep fresh API client per tool call for concurrent safety
7. Return standardized response format: {"status": "success"|"error", "data": {...}, "error": null}

CODE PATTERNS (MANDATORY):
- Async context managers for API client
- httpx.AsyncClient for HTTP requests
- structlog for structured logging
- Pydantic models with Field aliases for camelCase API responses
- Try/except wrapping in tools to never raise to MCP server

TESTING:
- Use pytest with pytest-asyncio
- Mock httpx at client boundary
- 100% coverage target on implemented code
- No real API calls in unit tests

DOCUMENTATION:
- Update docs/API.md for tool signatures
- Update .github/copilot-instructions.md for architectural decisions
- Keep README.md current with setup instructions

COMMON TASKS:
- Adding new tools: API client method → Tools wrapper method → Server registration
- Bug fixes: Check all three layers (client, tools, server)
- Tests: Mirror structure of production code in tests/
```

## 2. Code Review Prompt for PRs

```
When reviewing High-Command MCP pull requests, check:

ARCHITECTURE:
□ Changes follow three-layer pattern (Client → Tools → Server)
□ No logic mixing between layers
□ Proper separation of concerns

ASYNC/AWAIT:
□ All I/O operations are async
□ No blocking calls (requests, time.sleep, etc.)
□ Context managers used for resource management
□ Proper exception handling in async code

ERROR HANDLING:
□ Tools wrap exceptions and return standardized responses
□ API client raises RuntimeError with descriptive messages
□ Structured logging with context
□ No bare except clauses

TYPE HINTS:
□ All function signatures have type hints
□ Return types explicitly specified
□ Optional fields use Optional[T]
□ dict[str, Any] instead of Dict

PYDANTIC MODELS:
□ ConfigDict(populate_by_name=True) on all models
□ Field aliases for camelCase API responses
□ No mutable default arguments (use default_factory)
□ Generic types used correctly

TESTING:
□ Unit tests for new code
□ Mock httpx, not real API calls
□ Tests use pytest-asyncio decorators
□ Coverage maintained or improved

DOCUMENTATION:
□ Docstrings on all public functions
□ API.md updated for new tools
□ README.md updated if setup changes
□ Comments explain "why" not "what"
```

## 3. Debugging Prompt

```
For debugging High-Command MCP issues, follow this systematic approach:

ISSUE DIAGNOSIS:
1. Check which layer is failing: API Client, Tools, or Server?
2. Enable verbose logging: LOG_LEVEL=DEBUG
3. Check httpx response status and headers
4. Verify Pydantic model validation with .model_validate()

API CLIENT ISSUES:
- Check HIGH_COMMAND_API_BASE_URL environment variable
- Verify API endpoint exists and is correct
- Check timeout setting (default 30s)
- Validate HTTPS in production (ENVIRONMENT=production)
- Look for httpx.HTTPStatusError with categorized logging

TOOLS LAYER ISSUES:
- Check fresh API client created per tool call
- Verify error response structure
- Look for exception types in error messages
- Check structured logging for context

SERVER ISSUES:
- Verify tool registration in both list_tools() and call_tool()
- Check argument validation and type checking
- Verify MCP transport (stdio, HTTP, SSE)
- Check health endpoint for HTTP transport

TESTING ISSUES:
- Ensure httpx mocking at context manager boundary
- Check pytest-asyncio mode (usually AUTO)
- Verify test fixtures and conftest.py
- Run with -vvv for detailed output

PERFORMANCE ISSUES:
- Profile with timing metrics in _run_tool()
- Check API response times with structured logging
- Profile client creation/cleanup overhead
- Check concurrent tool calls for race conditions
```

## 4. Feature Implementation Prompt

```
To implement a new feature in High-Command MCP:

NEW TOOL CHECKLIST:
□ 1. Add async method to HighCommandAPIClient class
     - Use async context manager pattern
     - Add structured logging
     - Handle errors with _handle_response()
     
□ 2. Add Pydantic model in models.py (if new response type)
     - Use ConfigDict(populate_by_name=True)
     - Use Field aliases for camelCase fields
     - Use default_factory for mutable defaults
     
□ 3. Add async method to HighCommandTools class
     - Use _run_tool() helper
     - Return standardized response format
     
□ 4. Register in server.py
     - Add to list_tools() return list with proper schema
     - Add to call_tool() dispatcher
     - Add argument validation
     
□ 5. Write unit tests
     - Test success case with mocked httpx
     - Test error case
     - Verify response format
     
□ 6. Update documentation
     - Add tool to docs/API.md
     - Update README.md if needed
     - Add comments explaining complex logic

NEW ENDPOINT PATTERN:
1. High-Command API: GET /api/endpoint
2. API Client: async def get_endpoint() -> dict[str, Any]
3. Tools: async def get_endpoint_tool() -> dict[str, Any]
4. Server: Tool("get_endpoint", description, inputSchema)
5. Test: mock httpx response, call tool, verify shape
```

## 5. Performance Optimization Prompt

```
When optimizing High-Command MCP performance:

MEASUREMENT:
1. Use timing metrics in _run_tool(elapsed_ms)
2. Profile API client latency
3. Check concurrent request throughput
4. Monitor memory usage for connection pools

OPTIMIZATION STRATEGIES:
- Connection pooling: Consider singleton client vs fresh per call
- Caching: Static endpoints (biomes, factions) with TTL
- Batch requests: Group multiple calls if API supports
- Timeout tuning: Balance between responsiveness and reliability
- Circuit breaker: Fail fast on repeated API failures

TRADEOFFS:
- Fresh client per call = safe concurrency, higher overhead
- Reused client = better performance, need synchronization
- Caching = lower latency, stale data risk
- Longer timeout = more reliability, slower failure detection

RECOMMENDED APPROACH:
1. Profile current implementation
2. Identify bottlenecks (API vs client overhead)
3. Implement specific optimization for bottleneck
4. Measure improvement with benchmarks
5. Add tests to prevent regression
```

## 6. Troubleshooting Common Issues

```
ISSUE: "Client not initialized. Use as async context manager."
ROOT CAUSE: API client used outside context manager
FIX: Always use: async with HighCommandAPIClient() as client:

ISSUE: "RuntimeError" with HTTP status codes
ROOT CAUSE: Network error or API unavailable
FIX: Check HIGH_COMMAND_API_BASE_URL, verify API is running

ISSUE: Mutable default argument errors
ROOT CAUSE: Using biome={} or hazards=[]
FIX: Use Field(default_factory=dict) or Field(default_factory=list)

ISSUE: Type validation errors with Pydantic
ROOT CAUSE: Field type mismatch or missing alias
FIX: Use Field(..., alias="fieldName") for camelCase

ISSUE: Tests failing with "not a coroutine"
ROOT CAUSE: Missing @pytest.mark.asyncio decorator
FIX: Add decorator to async test functions

ISSUE: Slow tool execution
ROOT CAUSE: Fresh client creation per call
FIX: Profile with timing metrics, consider connection pooling

ISSUE: "Unknown tool" error
ROOT CAUSE: Tool not registered in list_tools() or call_tool()
FIX: Ensure tool appears in both registration locations

ISSUE: httpx.HTTPError not caught
ROOT CAUSE: Exception raised instead of being handled
FIX: All HTTP calls should use _handle_response() helper
```

---

**Last Updated**: October 21, 2025  
**Version**: 1.0.0  
**Status**: Production Ready with Development Guidance
