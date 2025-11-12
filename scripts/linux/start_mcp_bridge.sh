#!/bin/bash
# PhiGEN MCP Bridge Launcher (Linux/WSL)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "          PhiGEN MCP Bridge Launcher"
echo "============================================================"
echo ""
echo "Starting Discord MCP Bridge..."
echo ""

# Activate venv and start bridge
if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
    python -m src.phigen.bots.discord_mcp_bridge
else
    echo "[ERROR] Virtual environment not found!"
    echo "Please run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi
