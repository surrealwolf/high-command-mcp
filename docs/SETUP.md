# Setup Guide for High-Command

## Prerequisites

- Python 3.9 or higher (3.12.3+ recommended)
- pip (Python package manager)
- Git
- Docker (optional, for containerized deployment)

## Installation

### Option 1: Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/surrealwolf/high-command-mcp.git
   cd high-command-mcp
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package**
   ```bash
   make install
   # Or manually:
   pip install -r requirements.txt
   ```

4. **Install development dependencies** (for development)
   ```bash
   make dev
   # Or manually:
   pip install -r requirements-dev.txt
   ```

### Installing Optional Features

**HTTP Support (for Kubernetes)**
```bash
pip install -r requirements-http.txt
```

**Kubernetes Deployment**
```bash
pip install -r requirements-kubernetes.txt
```

**See [REQUIREMENTS.md](../REQUIREMENTS.md) for all installation options.**

### Option 2: Docker

1. **Build the Docker image**
   ```bash
   make docker-build
   ```

2. **Run the container**
   ```bash
   make docker-run
   ```

## Configuration

1. **Copy the example environment file**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your configuration**
   ```bash
   nano .env
   ```

3. **Optional environment variables:**
   - `HIGH_COMMAND_API_BASE_URL`: Base URL for High-Command API (default: `http://localhost:5000`)
   - `LOG_LEVEL`: Logging level (default: INFO)
   - `MCP_TRANSPORT`: Transport mode - `stdio` or `http` (default: `stdio`)

## Verification

### Run Tests

```bash
make test
```

This will run all unit tests with coverage report.

### Test the MCP Server

```bash
python -m highcommand.server
```

This starts the MCP server on stdio transport (default for Claude integration).

## Common Issues

### Issue: "ImportError: No module named 'mcp'"

**Solution**: Make sure you've installed the package:
```bash
pip install -e .
```

### Issue: "Bot detection HTML response"

**Solution**: This issue is specific to certain upstream APIs with Cloudflare protection. The High-Command API does not require special headers. Ensure environment variables are configured correctly:
```bash
export HIGH_COMMAND_API_BASE_URL=http://localhost:5000
export LOG_LEVEL=INFO
```

### Issue: "Connection timeout"

**Solution**: The API might be temporarily unavailable or you might have a network issue. The High-Command API implements automatic exponential backoff for retries. If you still experience timeouts:
1. Check your internet connection
2. Verify the API endpoint is accessible: `curl http://localhost:5000/api/war/status`
3. Check if the High-Command API service is running
4. Review logs for rate limiting warnings

### Issue: "pytest: command not found"

**Solution**: Install development dependencies:
```bash
make dev
```

## Development Workflow

1. **Code quality checks**
   ```bash
   make lint
   ```

2. **Format code**
   ```bash
   make format
   ```

3. **Run tests**
   ```bash
   make test
   ```

4. **Build Docker image**
   ```bash
   make docker-build
   ```

5. **Run full check** (lint + format + test)
   ```bash
   make check-all
   ```

## Project Layout

```
high-command/
├── highcommand/         # Main MCP server code
├── tests/               # Test files
├── docs/                # Documentation
├── .github/             # GitHub workflows and instructions
├── Makefile             # Development tasks
├── Dockerfile           # Container definition
├── pyproject.toml       # Python configuration
├── README.md            # Project overview
└── CONTRIBUTING.md      # Contribution guidelines
```

## Next Steps

- Read [README.md](../README.md) for project overview
- Check [docs/API.md](API.md) for API documentation
- See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines
- Review [.github/copilot-instructions.md](../.github/copilot-instructions.md) for development patterns

## Getting Help

- Check [README.md](../README.md) for common questions
- Review GitHub Issues at https://github.com/surrealwolf/high-command-mcp/issues
- Start a GitHub Discussion at https://github.com/surrealwolf/high-command-mcp/discussions

## Additional Resources

- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
- [httpx HTTP Client](https://www.python-httpx.org/)
- [Pydantic Validation](https://docs.pydantic.dev/)
- [pytest Testing](https://docs.pytest.org/)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [High-Command API](https://github.com/surrealwolf/high-command-mcp)

---

**Last Updated**: October 21, 2025
