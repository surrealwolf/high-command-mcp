# High-Command MCP - Troubleshooting Guide

Comprehensive troubleshooting guide for common issues and their solutions.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Runtime Errors](#runtime-errors)
3. [Connection Issues](#connection-issues)
4. [Test Failures](#test-failures)
5. [Performance Issues](#performance-issues)
6. [Docker Issues](#docker-issues)
7. [Kubernetes Issues](#kubernetes-issues)
8. [Development Issues](#development-issues)

---

## Installation Issues

### Issue: "Module not found: mcp"

**Symptoms:**
```
ModuleNotFoundError: No module named 'mcp'
```

**Root Cause:**
Dependencies not installed or wrong Python environment

**Solutions:**
1. Reinstall dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

2. Verify Python version (3.9+):
   ```bash
   python --version
   ```

3. Check active Python environment:
   ```bash
   which python
   pip list | grep mcp
   ```

4. Create fresh virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -e ".[dev]"
   ```

### Issue: "No module named 'httpx'"

**Symptoms:**
```
ModuleNotFoundError: No module named 'httpx'
```

**Root Cause:**
Optional dependency not installed

**Solutions:**
```bash
# Install core dependencies
pip install -e "."

# Or specify extras
pip install -e ".[http,kubernetes]"  # for HTTP transport and K8s

# Or install all dependencies
pip install -e ".[dev]"
```

### Issue: "Pydantic version conflict"

**Symptoms:**
```
ImportError: cannot import name 'ConfigDict' from pydantic
```

**Root Cause:**
Using Pydantic v1 instead of v2

**Solution:**
```bash
pip install 'pydantic>=2.0.0'
pip show pydantic  # verify version is 2.x
```

---

## Runtime Errors

### Issue: "Client not initialized. Use as async context manager."

**Symptoms:**
```
RuntimeError: Client not initialized. Use as async context manager.
```

**Root Cause:**
API client used outside `async with` context manager

**Example of Wrong Code:**
```python
client = HighCommandAPIClient()
await client.get_war_status()  # ❌ Raises RuntimeError
```

**Correct Code:**
```python
async with HighCommandAPIClient() as client:
    data = await client.get_war_status()  # ✅ Works
```

**Solution:**
Always wrap API client in async context manager

### Issue: "Production deployments must use HTTPS"

**Symptoms:**
```
ValueError: Production deployments must use HTTPS. 
Set HIGH_COMMAND_API_BASE_URL to an https:// URL.
```

**Root Cause:**
Production environment using HTTP (insecure)

**Solutions:**

**Option 1: Use HTTPS endpoint**
```bash
export ENVIRONMENT=production
export HIGH_COMMAND_API_BASE_URL=https://api.example.com
python -m highcommand.server
```

**Option 2: Use development environment**
```bash
export ENVIRONMENT=development
export HIGH_COMMAND_API_BASE_URL=http://localhost:5000
python -m highcommand.server
```

**Option 3: Use HTTP in development only**
```bash
export ENVIRONMENT=development  # Default is production
export HIGH_COMMAND_API_BASE_URL=http://localhost:5000
```

### Issue: "HTTP error (500): Internal Server Error"

**Symptoms:**
```
RuntimeError: HTTP error (500): Internal Server Error
```

**Root Cause:**
High-Command API server error

**Solutions:**

1. Check if API is running:
   ```bash
   curl http://localhost:5000/api/war/status
   ```

2. Check API logs for errors:
   ```bash
   docker logs high-command-api  # if running in Docker
   ```

3. Verify API connection:
   ```bash
   ping localhost:5000  # or your API host
   ```

4. Check network connectivity:
   ```bash
   curl -v http://localhost:5000/health  # if health endpoint exists
   ```

### Issue: "HTTP error (429): Too Many Requests"

**Symptoms:**
```
RuntimeError: Rate limit exceeded
WARNING: Rate limit exceeded endpoint=/api/war/status
```

**Root Cause:**
Exceeded API rate limits

**Solutions:**

1. Implement request throttling:
   ```python
   import asyncio
   
   # Add delay between requests
   await asyncio.sleep(1)  # Wait 1 second between calls
   ```

2. Reduce request frequency:
   - Don't call same endpoint repeatedly in quick succession
   - Cache results with TTL

3. Check API rate limit documentation:
   - Typical: 100 requests/minute
   - Contact API provider for rate limit details

4. Use backoff strategy:
   ```python
   async def with_backoff(func, max_retries=3):
       for attempt in range(max_retries):
           try:
               return await func()
           except RuntimeError as e:
               if "429" in str(e) and attempt < max_retries - 1:
                   wait_time = 2 ** attempt
                   await asyncio.sleep(wait_time)
                   continue
               raise
   ```

### Issue: "TypeError: Expected async function, got function"

**Symptoms:**
```
TypeError: Expected async function, got function
```

**Root Cause:**
Passing non-async function to `_run_tool()`

**Solutions:**

**Wrong:**
```python
def sync_function():
    return {"data": "value"}

await HighCommandTools._run_tool(sync_function)  # ❌
```

**Correct:**
```python
async def async_function():
    return {"data": "value"}

await HighCommandTools._run_tool(async_function)  # ✅
```

Make sure all functions passed to `_run_tool()` are `async def`, not `def`

---

## Connection Issues

### Issue: "Connection refused" to High-Command API

**Symptoms:**
```
httpx.ConnectError: [Errno 111] Connection refused
```

**Root Cause:**
High-Command API not running or wrong host/port

**Solutions:**

1. Verify API is running:
   ```bash
   curl http://localhost:5000/api/war/status
   ```

2. Check BASE_URL configuration:
   ```bash
   echo $HIGH_COMMAND_API_BASE_URL
   ```

3. If using Docker, verify container is running:
   ```bash
   docker ps | grep high-command-api
   ```

4. Try connecting with curl:
   ```bash
   curl -v http://localhost:5000/
   ```

5. Check firewall rules:
   ```bash
   netstat -tuln | grep 5000  # Linux
   lsof -i :5000             # macOS
   ```

### Issue: "Connection timeout"

**Symptoms:**
```
httpx.TimeoutException: ReadTimeout
```

**Root Cause:**
API taking too long to respond, network slow, or API unavailable

**Solutions:**

1. Increase timeout:
   ```python
   client = HighCommandAPIClient(timeout=60.0)  # 60 seconds instead of 30
   ```

2. Check API performance:
   ```bash
   time curl http://localhost:5000/api/war/status
   ```

3. Check network latency:
   ```bash
   ping api.example.com
   ```

4. Check API load:
   ```bash
   # If API has metrics endpoint
   curl http://localhost:5000/health
   ```

### Issue: "SSL: CERTIFICATE_VERIFY_FAILED"

**Symptoms:**
```
httpx.SSLError: [SSL] CERTIFICATE_VERIFY_FAILED
```

**Root Cause:**
Self-signed certificate or certificate validation issue

**Solutions:**

**For development only (not production):**
```python
# Disable SSL verification (UNSAFE - dev only)
client = httpx.AsyncClient(verify=False)
```

**Better approach - Use proper certificate:**
```bash
# Update to use proper HTTPS certificate
export HIGH_COMMAND_API_BASE_URL=https://api.example.com
# Ensure certificate is valid and trusted
```

---

## Test Failures

### Issue: "Test failed: assert result['status'] == 'success'"

**Symptoms:**
```
AssertionError: assert 'error' == 'success'
```

**Root Cause:**
Tool returned error status instead of success

**Debug Steps:**

1. Check the error message:
   ```python
   print(result['error'])  # See actual error
   ```

2. Check mock setup:
   ```python
   # Verify mock response is correct
   mock_response.json.return_value = {"expected": "data"}
   ```

3. Check httpx mocking:
   ```python
   # Ensure AsyncClient context manager is properly mocked
   with patch("highcommand.api_client.httpx.AsyncClient") as mock_client:
       mock_instance = Mock()
       mock_instance.__aenter__.return_value = mock_instance
       mock_instance.__aexit__.return_value = None
       mock_client.return_value = mock_instance
   ```

### Issue: "RuntimeWarning: coroutine was never awaited"

**Symptoms:**
```
RuntimeWarning: coroutine '_fetch' was never awaited
```

**Root Cause:**
Async function called without `await`

**Solution:**
```python
# Wrong
result = tools.get_war_status_tool()

# Correct
result = await tools.get_war_status_tool()
```

### Issue: "Event loop is closed"

**Symptoms:**
```
RuntimeError: Event loop is closed
```

**Root Cause:**
Pytest not properly configured for async tests

**Solutions:**

1. Add pytest marker:
   ```python
   @pytest.mark.asyncio
   async def test_something():
       ...
   ```

2. Check pyproject.toml:
   ```toml
   [tool.pytest.ini_options]
   asyncio_mode = "auto"  # Or "strict"
   ```

3. Verify pytest-asyncio is installed:
   ```bash
   pip install pytest-asyncio
   ```

### Issue: "TypeError: not all arguments converted during string formatting"

**Symptoms:**
```
TypeError: not all arguments converted during string formatting
```

**Root Cause:**
Logging statement with wrong argument count

**Solution:**
Use keyword arguments for structured logging:

```python
# Wrong
logger.info("Message %s %s", value)  # Missing argument

# Correct
logger.info("Message", value=value)  # Structured logging

# Or correct count
logger.info("Message %s %s", value1, value2)
```

---

## Performance Issues

### Issue: "Tool execution is slow (>1 second)"

**Symptoms:**
Tool taking longer than expected to return results

**Investigation Steps:**

1. Check if metrics are included:
   ```python
   result = await tools.get_war_status_tool()
   if "metrics" in result:
       print(f"Elapsed: {result['metrics']['elapsed_ms']}ms")
   ```

2. Enable DEBUG logging:
   ```bash
   LOG_LEVEL=DEBUG python -m highcommand.server
   ```

3. Check API response time:
   ```bash
   time curl http://localhost:5000/api/war/status
   ```

4. Check system resources:
   ```bash
   top  # CPU and memory usage
   free -h  # Available memory
   ```

**Solutions:**

1. If API is slow:
   - Check API server logs
   - Check database performance
   - Check network latency

2. If client is slow:
   - Profile with `cProfile`
   - Check for memory leaks
   - Consider connection pooling

3. Implement caching:
   ```python
   # Cache static endpoints
   self.cache["biomes"] = result
   ```

### Issue: "Memory usage growing over time"

**Symptoms:**
Memory usage steadily increases during operation

**Root Cause:**
Resource leak or unclosed connections

**Solutions:**

1. Verify context managers are used:
   ```python
   # Correct pattern
   async with HighCommandAPIClient() as client:
       ...  # Automatically closed
   ```

2. Check for circular references in models

3. Monitor with memory profiler:
   ```bash
   pip install memory-profiler
   python -m memory_profiler script.py
   ```

---

## Docker Issues

### Issue: "Docker build fails: 'package not found'"

**Symptoms:**
```
ERROR: package not found: some-package
```

**Root Cause:**
Python package not available or wrong version

**Solutions:**

1. Check Dockerfile Python version:
   ```dockerfile
   FROM python:3.13-slim  # Must be 3.9+
   ```

2. Verify pyproject.toml dependencies:
   ```bash
   cat pyproject.toml | grep dependencies
   ```

3. Build with verbose output:
   ```bash
   docker build -t high-command --progress=plain .
   ```

### Issue: "Container fails to start: 'Connection refused'"

**Symptoms:**
```
ERROR: Connection refused
Container exiting...
```

**Root Cause:**
API endpoint not available from container

**Solutions:**

1. Check network connectivity:
   ```bash
   docker run --rm high-command curl http://host.docker.internal:5000/
   ```

2. For local API, use host network:
   ```bash
   docker run --network host high-command
   ```

3. Check HIGH_COMMAND_API_BASE_URL:
   ```bash
   docker run -e HIGH_COMMAND_API_BASE_URL=http://host.docker.internal:5000 high-command
   ```

### Issue: "Port 8000 already in use"

**Symptoms:**
```
Address already in use
```

**Solutions:**

1. Kill existing process:
   ```bash
   lsof -i :8000
   kill -9 <PID>
   ```

2. Use different port:
   ```bash
   docker run -p 9000:8000 high-command
   # Or
   docker run -e MCP_PORT=9000 high-command
   ```

---

## Kubernetes Issues

### Issue: "Pod is stuck in CrashLoopBackOff"

**Symptoms:**
```
STATUS: CrashLoopBackOff
RESTARTS: 5
```

**Root Cause:**
Application crashing on startup

**Solutions:**

1. Check pod logs:
   ```bash
   kubectl logs high-command-pod
   ```

2. Check events:
   ```bash
   kubectl describe pod high-command-pod
   ```

3. Check environment variables:
   ```bash
   kubectl exec -it high-command-pod env | grep HIGH_COMMAND
   ```

### Issue: "ReadinessProbe failed"

**Symptoms:**
```
Readiness probe failed: connection refused
```

**Root Cause:**
Health check endpoint not responding

**Solutions:**

1. Check health endpoint:
   ```bash
   kubectl exec -it high-command-pod -- curl localhost:8000/health
   ```

2. Verify deployment has correct port:
   ```yaml
   ports:
     - containerPort: 8000
   ```

3. Check probe configuration:
   ```yaml
   readinessProbe:
     httpGet:
       path: /health
       port: 8000
   ```

---

## Development Issues

### Issue: "pre-commit hook failed"

**Symptoms:**
```
(Python Syntax Errors)
(Black formatter)
(Ruff linter)
```

**Root Cause:**
Code doesn't pass quality checks

**Solutions:**

1. Auto-fix with black:
   ```bash
   black highcommand/ tests/
   ```

2. Fix linting issues:
   ```bash
   ruff check --fix highcommand/ tests/
   ```

3. Check types:
   ```bash
   mypy highcommand/
   ```

4. Run full check:
   ```bash
   make check-all
   ```

### Issue: "Git branch protection blocks PR merge"

**Symptoms:**
```
Merging is blocked
Reason: Not all reviews have been completed
```

**Root Cause:**
PR not approved or checks failing

**Solutions:**

1. Wait for Copilot review (automatic)
2. Ensure all checks pass:
   ```bash
   make check-all
   pytest tests/
   ```

3. Request manual review if needed
4. Address any review comments

### Issue: "Environment variable not loaded"

**Symptoms:**
```
Using default value instead of set environment variable
```

**Root Cause:**
Variable not exported or wrong shell

**Solutions:**

1. Verify export:
   ```bash
   export HIGH_COMMAND_API_BASE_URL=http://localhost:5000
   echo $HIGH_COMMAND_API_BASE_URL
   ```

2. For Fish shell:
   ```fish
   set -x HIGH_COMMAND_API_BASE_URL http://localhost:5000
   ```

3. Use .env file:
   ```bash
   cat > .env << EOF
   HIGH_COMMAND_API_BASE_URL=http://localhost:5000
   LOG_LEVEL=DEBUG
   EOF
   export $(cat .env | xargs)
   ```

---

## Getting More Help

1. **Enable Debug Logging:**
   ```bash
   LOG_LEVEL=DEBUG python -m highcommand.server
   ```

2. **Check Documentation:**
   - docs/API.md - Tool specifications
   - docs/CODE_REVIEW.md - Architecture details
   - .github/copilot-instructions.md - Patterns and practices

3. **Review Test Cases:**
   ```bash
   grep -r "your_issue" tests/
   ```

4. **Check Recent Changes:**
   ```bash
   git log --oneline -10
   git diff main..HEAD
   ```

---

**Last Updated**: October 21, 2025  
**Maintained By**: Development Team  
**Status**: Comprehensive Troubleshooting Guide
