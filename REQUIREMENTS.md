# Requirements Files Reference

This project includes multiple `requirements*.txt` files for different use cases.

## Installation Options

### Option 1: Core Installation (Recommended for Local Development)

```bash
pip install -r requirements.txt
```

Installs only core dependencies:
- `mcp` - Model Context Protocol server
- `httpx` - Async HTTP client
- `pydantic` - Data validation
- `python-dotenv` - Environment configuration
- `structlog` - Structured logging

**Size:** ~50 MB

### Option 2: HTTP/Web Support

```bash
pip install -r requirements-http.txt
```

Adds HTTP transport support for Kubernetes:
- Everything from `requirements.txt`
- `fastapi` - Modern web framework
- `uvicorn` - ASGI server

**Size:** ~80 MB

**Use when:** Running as HTTP server (`MCP_TRANSPORT=http`)

### Option 3: Kubernetes Deployment

```bash
pip install -r requirements-kubernetes.txt
```

Complete Kubernetes-ready installation:
- Everything from `requirements-http.txt`
- `python-kubernetes` - Kubernetes Python client

**Size:** ~90 MB

**Use when:** Deploying to Kubernetes cluster

### Option 4: Development & Testing

```bash
pip install -r requirements-dev.txt
```

Development environment with all tools:
- Core dependencies
- Testing: `pytest`, `pytest-asyncio`, `pytest-cov`
- Code quality: `black`, `ruff`, `mypy`
- Documentation: `sphinx`, `sphinx-rtd-theme`

**Size:** ~200 MB

**Use when:** Contributing to the project

### Option 5: Package Installation (Production)

```bash
pip install high-command
pip install high-command[http]
pip install high-command[kubernetes]
pip install high-command[dev]
```

Installs from PyPI with specified extras.

## Requirements File Hierarchy

```
requirements.txt
├── requirements-http.txt
│   └── requirements-kubernetes.txt
└── requirements-dev.txt (independent)
```

Files with `-r requirements.txt` inherit parent dependencies.

## Quick Reference

| Use Case | Command | Size |
|----------|---------|------|
| Local development | `pip install -r requirements.txt` | ~50 MB |
| HTTP server | `pip install -r requirements-http.txt` | ~80 MB |
| Kubernetes | `pip install -r requirements-kubernetes.txt` | ~90 MB |
| Development | `pip install -r requirements-dev.txt` | ~200 MB |
| PyPI package | `pip install high-command[kubernetes]` | ~90 MB |

## Docker Build

```bash
# Docker automatically installs via pyproject.toml
docker build -t high-command:latest .

# Or specify requirements file
docker build --build-arg PIP_INSTALL="requirements-kubernetes.txt" \
  -t high-command:k8s .
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Install dependencies
  run: pip install -r requirements-dev.txt
```

### GitLab CI

```yaml
before_script:
  - pip install -r requirements-dev.txt
```

## Pinned Versions

All requirements use minimum version constraints (`>=`). For pinned versions:

```bash
# Generate lock file
pip freeze > requirements.lock

# Use lock file
pip install -r requirements.lock
```

## Troubleshooting

### Import errors after installation

```bash
# Reinstall with specific requirements
pip uninstall high-command -y
pip install -r requirements.txt
```

### Version conflicts

```bash
# Install specific version
pip install httpx==0.24.0 pydantic==2.0.0
```

### Missing optional dependencies

```bash
# For HTTP support
pip install -r requirements-http.txt

# For Kubernetes
pip install -r requirements-kubernetes.txt
```

## Environment Variables

After installation, configure:

```bash
# Transport mode
export MCP_TRANSPORT=http  # or stdio (default)

# Server
export MCP_HOST=0.0.0.0
export MCP_PORT=8000
export MCP_WORKERS=4

# Logging
export LOG_LEVEL=INFO

# API headers
export X_SUPER_CLIENT=app
export X_SUPER_CONTACT=user@example.com
```

## Development Workflow

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# 2. Install development dependencies
pip install -r requirements-dev.txt

# 3. Install package in development mode
pip install -e .

# 4. Run tests
pytest

# 5. Format code
black highcommand/ tests/

# 6. Check quality
ruff check .
mypy highcommand/
```

## See Also

- [SETUP.md](docs/SETUP.md) - Installation guide
- [KUBERNETES_DEPLOYMENT.md](docs/KUBERNETES_DEPLOYMENT.md) - K8s guide
- [README.md](README.md) - Project overview

---

**Last Updated:** October 19, 2025
