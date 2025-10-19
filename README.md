# High-Command: HellHub Collective MCP Server

A Model Context Protocol (MCP) server for seamless integration with the HellHub Collective API. This project provides tools and resources to access real-time Helldivers 2 game data through the community-driven HellHub API.

## Features

- 🔌 **MCP Server**: Full Model Context Protocol implementation
- 🎮 **Helldivers 2 API**: Direct access to game data (war status, campaigns, planets, assignments)
- 📦 **Async/Await**: Built with modern async Python
- 🐳 **Docker Support**: Easy containerization
- 🧪 **Comprehensive Tests**: Full test coverage
- 📚 **Documentation**: Complete API and usage documentation
- 🔄 **CI/CD**: GitHub Actions workflows for testing and building

## Quick Start

### Prerequisites

- Python 3.14.0+
- pip or uv
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/high-command.git
cd high-command

# Install dependencies
make install

# Install development dependencies
make dev
```

### Running the Server

```bash
# Run with make
make run

# Or with Docker
make docker-run

# Or directly
python -m highcommand.server
```

### Running Tests

```bash
# Run all tests with coverage
make test

# Run tests quickly without coverage
make test-fast

# Run specific test file
pytest tests/test_api_client.py -v
```

### Code Quality

```bash
# Format code
make format

# Run linters
make lint

# Run all checks
make check
```

## API Tools

The MCP server exposes the following tools:

### `get_war_status`
Get current war status from HellHub Collective API.

**Parameters**: None

**Returns**: War information including war ID, start/end times.

### `get_planets`
Get planet information.

**Parameters**: None

**Returns**: List of planets with names, sectors, biomes, and positions.

### `get_statistics`
Get global game statistics.

**Parameters**: None

**Returns**: Aggregated statistics including missions won/lost, kills, accuracy, etc.

### `get_campaign_info`
Get active campaign information.

**Parameters**: None

**Returns**: List of campaigns with planet assignments and types.

### `get_planet_status`
Get status for a specific planet.

**Parameters**:
- `planet_index` (integer, required): The index of the planet

**Returns**: Detailed status information for the specified planet.

## Project Structure

```
high-command/
├── mcp/                    # Main MCP server package
│   ├── __init__.py
│   ├── server.py           # MCP server implementation
│   ├── api_client.py       # Helldivers 2 API client
│   ├── models.py           # Pydantic data models
│   └── tools.py            # MCP tool definitions
├── tests/                  # Test suite
│   ├── test_api_client.py
│   └── test_models.py
├── scripts/                # Utility scripts
│   ├── test_api.py         # API connectivity test
│   └── run_server.py       # Development server runner
├── docs/                   # Documentation
├── Makefile                # Build and development tasks
├── Dockerfile              # Docker container definition
├── docker-compose.yml      # Docker Compose configuration
└── pyproject.toml          # Python project configuration
```

## Docker

### Building the Image

```bash
make docker-build
```

### Running the Container

```bash
docker run -it --rm \
  -e X_SUPER_CLIENT=hc.dataknife.ai \
  -e X_SUPER_CONTACT=lee@fullmetal.dev \
  high-command:latest
```

### Using Docker Compose

```bash
docker-compose up
```

## Environment Variables

- `X_SUPER_CLIENT`: Client identifier for API requests (default: `hc.dataknife.ai`)
- `X_SUPER_CONTACT`: Contact email for API requests (default: `lee@fullmetal.dev`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

## Development

### Setting up the Development Environment

```bash
# Install development dependencies
make dev

# Run formatter
make format

# Run linters
make lint

# Run tests
make test
```

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## API Rate Limiting

The Helldivers 2 API has rate limiting. Be respectful in your requests. The MCP server implements reasonable defaults and handles errors gracefully.

## Troubleshooting

### API Returns Bot Detection HTML

The Helldivers 2 API has Cloudflare bot protection. Make sure you're including the required headers:
- `X-Super-Client`
- `X-Super-Contact`

### Connection Timeouts

Increase the timeout value in `HelldiverAPIClient`:

```python
client = HelldiverAPIClient(timeout=60.0)  # 60 seconds
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [HellHub Collective API](https://github.com/hellhub-collective/api)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Helldivers 2](https://store.steampowered.com/app/553850/HELLDIVERS_2/)

## Support

For issues and questions:
- 📝 [GitHub Issues](https://github.com/yourusername/high-command/issues)
- 💬 [GitHub Discussions](https://github.com/yourusername/high-command/discussions)

---

Made with ❤️ for the Helldivers 2 community
