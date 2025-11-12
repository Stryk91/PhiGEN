# PhiGEN Linux/WSL Scripts

Shell scripts for running PhiGEN components in Linux/WSL environments.

## Quick Start (from project root)

```bash
# Check system status
./status.sh

# Start MCP Bridge
./start_bridge.sh

# Start PhiGEN Bot
./start_system.sh
```

## Available Scripts

### In `scripts/linux/` directory:

- **status_check.sh** - Check status of all PhiGEN components
  - Docker Desktop
  - Docker Containers
  - MCP Bridge
  - PhiGEN Discord Bot
  - Ollama API
  - MCP Bridge HTTP endpoint

- **start_mcp_bridge.sh** - Start the Discord MCP Bridge
  - Provides HTTP endpoints for controlling Discord bot
  - Runs on http://localhost:8765

- **start_phigen_bot.sh** - Start the PhiGEN MCP Discord Bot
  - Loads environment from `.env`
  - Activates virtual environment
  - Launches discord_bot_mcp_enhanced

- **run_password_vault.sh** - Launch the Password Vault GUI
  - Requires PyQt6
  - Runs the GUI application

### Root Convenience Scripts:

- **status.sh** → Wrapper for `scripts/linux/status_check.sh`
- **start_bridge.sh** → Wrapper for `scripts/linux/start_mcp_bridge.sh`
- **start_system.sh** → Wrapper for `scripts/linux/start_phigen_bot.sh`

## Windows Equivalents

Windows batch file versions are located in:
- `scripts/windows/` - Windows-specific scripts
- Root directory `.bat` files - Main Windows launchers

## Requirements

- Python 3.8+ with venv
- Docker Desktop (for container services)
- All Python dependencies installed (`pip install -r requirements.txt`)
- `.env` file configured with Discord token and API keys

## Current System Status

Run `./status.sh` to see:
```
============================================================
             PHIGEN SYSTEM STATUS
============================================================

[Docker Desktop]
  Status: Running

[MCP Bridge]
  Status: Running (PID: 12345)

[PhiGEN Discord Bot]
  Status: Running (PID: 67890)

[MCP Bridge HTTP]
  Status: Running (http://localhost:8765)
============================================================
```
