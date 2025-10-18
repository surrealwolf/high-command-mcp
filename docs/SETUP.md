# Setup Guide for High-Command

## Prerequisites

- Python 3.9 or higher
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
   ```

4. **Install development dependencies** (for development)
   ```bash
   make dev
   ```

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

3. **Required environment variables:**
   - `X_SUPER_CLIENT`: API client identifier
   - `X_SUPER_CONTACT`: Contact email for API
   - `LOG_LEVEL`: Logging level (default: INFO)

## Verification

### Test API Connection

```bash
python scripts/test_api.py
```

Expected output:
```
Testing API connectivity...

1. Fetching war status...
   ✓ War ID: 1

2. Fetching campaigns...
   ✓ Found X campaign(s)

3. Fetching planets...
   ✓ Found X planet(s)

4. Fetching assignments...
   ✓ Found X assignment(s)

✓ All API endpoints are working!
```

### Run Tests

```bash
make test
```

This will run all tests with coverage report.

### Start Development Server

```bash
python -m mcp.server
```

Or using the script:
```bash
python scripts/run_server.py
```

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
├── mcp/                 # Main MCP server code
├── tests/               # Test files
├── scripts/             # Utility scripts
├── docs/                # Documentation
├── Makefile             # Development tasks
├── Dockerfile           # Container definition
├── pyproject.toml       # Python configuration
├── README.md            # Project overview
└── CONTRIBUTING.md      # Contribution guidelines
```

## Next Steps

- Read [README.md](README.md) for project overview
- Check [docs/API.md](docs/API.md) for API documentation
- See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Review [.copilot-instructions.md](.copilot-instructions.md) for development notes

## Getting Help

- Check [README.md](README.md) for common questions
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

**Last Updated**: October 18, 2025
