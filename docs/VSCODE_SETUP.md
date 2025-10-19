# VS Code MCP Integration Guide

This guide shows you how to use the High-Command MCP server with Visual Studio Code and GitHub Copilot.

## ✅ Configuration

The High-Command MCP server is configured in VS Code's MCP settings file.

### Location
- **File**: `~/.config/Code/User/mcp.json` (Linux/Mac)
- **File**: `%APPDATA%\Code\User\mcp.json` (Windows)

### Configuration Example

```jsonc
{
  "servers": {
    "high-command": {
      "type": "stdio",
      "command": "python",
      "args": [
        "-m",
        "highcommand.server"
      ],
      "cwd": "/home/lee/git/high-command/high-command-mcp"
    }
  }
}
```

## 🚀 Setup Steps

### Step 1: Install Dependencies

```bash
cd /home/lee/git/high-command/high-command-mcp
make install
make dev
```

### Step 2: Configure VS Code

Open VS Code settings:
1. Press `Ctrl+,` (or `Cmd+,` on Mac)
2. Search for "MCP"
3. Click "Edit in settings.json"
4. Add the High-Command server configuration above

**Alternative**: Directly edit `~/.config/Code/User/mcp.json`

```json
{
  "servers": {
    "high-command": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "highcommand.server"],
      "cwd": "/path/to/high-command-mcp"
    }
  }
}
```

### Step 3: Verify Connection

1. Open VS Code Command Palette (`Ctrl+Shift+P`)
2. Search for "MCP" or "Copilot"
3. You should see High-Command in the available servers
4. If connected, you'll see ✅ status indicator

## 📖 Usage Examples

### Example 1: Ask Copilot to Get War Status

In any file or chat window:

```
/ask Get the current war status from Helldivers 2
```

Copilot will use the `get_war_status` tool to retrieve real-time data.

### Example 2: Query Planet Information

```
/ask What planets are currently available in Helldivers 2?
```

This calls the `get_planets` tool and shows you all planets with their details.

### Example 3: Get Game Statistics

```
/ask Show me the current global game statistics
```

Retrieves aggregated stats including missions won/lost, kills, etc.

### Example 4: Check Specific Planet

```
/ask Get status of planet at index 0
```

Uses `get_planet_status` with the specified planet index.

## 🔧 Advanced Configuration

### Environment Variables

Set custom environment variables in the MCP config:

```json
{
  "servers": {
    "high-command": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "highcommand.server"],
      "cwd": "/path/to/high-command-mcp",
      "env": {
        "LOG_LEVEL": "DEBUG",
        "X_SUPER_CLIENT": "my-client-id",
        "X_SUPER_CONTACT": "my-email@example.com"
      }
    }
  }
}
```

### Enable Debug Logging

To see detailed MCP communication logs:

```json
{
  "servers": {
    "high-command": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "highcommand.server"],
      "cwd": "/path/to/high-command-mcp",
      "env": {
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

## 🎯 Available Tools

All 7 High-Command tools are available in Copilot:

### `get_war_status`
**Description**: Get current war status from HellHub Collective API

**Example**:
```
/ask What's the current war status?
```

**Returns**: War ID, start/end times, status information

---

### `get_planets`
**Description**: Get all planets with their information

**Example**:
```
/ask List all available planets
```

**Returns**: Planet names, sectors, biomes, positions

---

### `get_planet_status`
**Description**: Get detailed status of a specific planet

**Parameters**:
- `planet_index` (int): The index of the planet

**Example**:
```
/ask Get status of planet 5
```

**Returns**: Planet details, current status, hazards

---

### `get_statistics`
**Description**: Get global game statistics

**Example**:
```
/ask Show me game statistics
```

**Returns**: Missions won/lost, kills, accuracy, time played, etc.

---

### `get_biomes`
**Description**: Get biome and terrain information

**Example**:
```
/ask What biomes are available?
```

**Returns**: List of biomes with type information

---

### `get_factions`
**Description**: Get faction information

**Example**:
```
/ask Show faction data
```

**Returns**: Faction details and information

---

### `get_campaign_info`
**Description**: Get campaign information (currently not available)

**Example**:
```
/ask Get campaign information
```

**Returns**: Error message (endpoint not available in HellHub API)

---

## 🐛 Troubleshooting

### Server Not Connecting

1. **Check if Python is installed**:
   ```bash
   python --version
   ```

2. **Verify package is installed**:
   ```bash
   python -c "from highcommand import server; print('✓')"
   ```

3. **Test server directly**:
   ```bash
   cd /path/to/high-command-mcp
   python -m highcommand.server
   ```

### Connection Timeout

1. **Check log level**:
   ```json
   "env": {
     "LOG_LEVEL": "DEBUG"
   }
   ```

2. **Verify working directory** is correct in config

3. **Check file permissions** on the high-command-mcp directory

### Tools Not Appearing

1. **Reload VS Code**: `Ctrl+Shift+P` → "Reload Window"

2. **Check MCP status**: Look for MCP indicator in status bar

3. **Restart Copilot extension**: 
   - `Ctrl+Shift+P` → "GitHub Copilot: Stop Server"
   - Wait 2 seconds
   - `Ctrl+Shift+P` → "GitHub Copilot: Start Server"

## 📝 Full Configuration Example

Here's a complete `mcp.json` with both GitHub and High-Command servers:

```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "high-command": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "highcommand.server"],
      "cwd": "/home/lee/git/high-command/high-command-mcp",
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## ✨ Tips & Tricks

### Combine with GitHub MCP

Use both GitHub and High-Command tools together:

```
/ask Create a GitHub issue with the current Helldivers 2 war status
```

### Multi-Tool Workflows

```
/ask Get the current statistics and check if we have any open issues about balancing
```

### Data Analysis

```
/ask Analyze the mission success rate and faction performance trends
```

## 🔗 Related Documentation

- [Main README](../README.md)
- [API Documentation](./API.md)
- [Setup Guide](./SETUP.md)
- [Getting Started](./GETTING_STARTED.md)

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review `~/.config/Code/User/mcp.json` syntax
3. Check VS Code output panel for errors
4. Verify Python and dependencies are installed correctly

---

**Last Updated**: October 19, 2025
**Version**: 1.0.0
**Status**: ✅ Ready to Use
