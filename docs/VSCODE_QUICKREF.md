# VS Code Quick Reference

## 🎯 Your Current Configuration

```json
{
  "servers": {
    "high-command": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "highcommand.server"],
      "cwd": "/home/lee/git/high-command/high-command-mcp"
    }
  }
}
```

## ✅ Verify Setup

```bash
# 1. Check Python
python --version

# 2. Install dependencies
cd /home/lee/git/high-command/high-command-mcp
make dev

# 3. Test server directly
python -m highcommand.server

# 4. Reload VS Code (Ctrl+Shift+P → Reload Window)
```

## 🚀 Quick Commands

| Task | Command |
|------|---------|
| List all available tools | `/ask What tools are available?` |
| Get war status | `/ask Get current war status` |
| Show all planets | `/ask List all planets` |
| Get statistics | `/ask Show game statistics` |
| Check planet details | `/ask Get status of planet 0` |
| Show biomes | `/ask What biomes exist?` |
| Get factions | `/ask Show faction information` |

## 📌 Example Prompts

### Simple Query
```
/ask What's the current war status in Helldivers 2?
```

### Data Analysis
```
/ask Analyze the planet status and tell me which is most dangerous
```

### Multi-Tool Workflow
```
/ask Get the current statistics and create a summary
```

## 🔧 Troubleshooting

| Issue | Fix |
|-------|-----|
| Server not found | Restart VS Code (Ctrl+Shift+P → Reload Window) |
| Connection timeout | Run `make dev` to install dependencies |
| Tools not appearing | Check `cwd` path in mcp.json is correct |
| Python not found | Update `cwd` path in mcp.json |

## 📖 Full Guide

See [VSCODE_SETUP.md](./VSCODE_SETUP.md) for complete documentation.
