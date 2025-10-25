# Setup Guide for High-Command

## Prerequisites

- Python 3.14.0 or higher (recommended)
- pip (Python package manager)
- Git
- Docker (optional)

## Installation

### Option 1: Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/high-command.git
   cd high-command
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
   - `LOG_LEVEL`: Logging level (default: INFO)

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

**Solution**: Ensure environment variables are set correctly:
```bash
export X_SUPER_CLIENT=hc.dataknife.ai
export X_SUPER_CONTACT=lee@fullmetal.dev
```

### Issue: "Connection timeout"

**Solution**: The API might be temporarily unavailable or you might have a network issue. Try:
1. Check your internet connection
2. Verify the API endpoint is accessible: `curl https://api.helldivers2.io/api/v1/war/status`
3. Increase the timeout in code: `HelldiverAPIClient(timeout=60.0)`

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
   make check
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
- Review [docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md) for troubleshooting
- Review GitHub Issues
- Start a GitHub Discussion
- Contact: lee@fullmetal.dev

## Additional Resources

- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
- [httpx HTTP Client](https://www.python-httpx.org/)
- [Pydantic Validation](https://docs.pydantic.dev/)
- [pytest Testing](https://docs.pytest.org/)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Helldivers 2 API](https://github.com/helldivers-2/api)

---

**Last Updated**: October 25, 2025
