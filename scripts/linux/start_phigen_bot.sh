#!/bin/bash
# PhiGEN Discord Bot Launcher (Linux/WSL)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "          PhiGEN MCP Discord Bot Launcher"
echo "============================================================"
echo ""
echo "Starting PhiGEN MCP Bot..."
echo ""

# Load environment variables
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
    echo "[OK] Environment variables loaded from .env"
else
    echo "[WARNING] .env file not found!"
fi

echo ""

# Activate venv and start bot
if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
    echo "[OK] Virtual environment activated"
    echo ""
    echo "Starting bot..."
    echo "============================================================"
    echo ""
    python -m src.phigen.bots.discord_bot_mcp_enhanced
else
    echo "[ERROR] Virtual environment not found!"
    echo "Please run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi
