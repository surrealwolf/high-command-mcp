# MCP Server

This directory contains the main MCP Server implementation for Helldivers 2 API integration.

## Structure

```
mcp/
├── __init__.py           # Package initialization
├── server.py             # Main MCP server implementation
├── api_client.py         # Helldivers 2 API client
├── models.py             # Data models and schemas
└── tools.py              # MCP tools definitions
```

## Overview

The MCP server provides tools and resources to interact with the Helldivers 2 API through the Model Context Protocol.

### Key Components

- **API Client**: Handles HTTP requests to the Helldivers 2 API with proper header management
- **Models**: Pydantic models for API responses and internal data
- **Tools**: MCP tools exposed to clients for API operations
- **Server**: Main MCP server implementation using the MCP framework
