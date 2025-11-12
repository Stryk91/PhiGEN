#!/bin/bash
# PhiGEN System Status Checker (Linux/WSL)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "============================================================"
echo "             PHIGEN SYSTEM STATUS"
echo "============================================================"
echo ""

# Check Docker
echo "[Docker Desktop]"
if docker version &>/dev/null; then
    echo "  Status: Running"
else
    echo "  Status: NOT RUNNING"
fi
echo ""

# Check Docker Containers
echo "[Docker Containers]"
docker ps --filter "name=phigen" --format "  {{.Names}}: {{.Status}}" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "  No PhiGEN containers running"
fi
echo ""

# Check MCP Bridge
echo "[MCP Bridge]"
if pgrep -f "discord_mcp_bridge" &>/dev/null; then
    PID=$(pgrep -f "discord_mcp_bridge")
    echo "  Status: Running (PID: $PID)"
else
    echo "  Status: Not running"
fi
echo ""

# Check PhiGEN Bot
echo "[PhiGEN Discord Bot]"
if pgrep -f "discord_bot_mcp_enhanced" &>/dev/null; then
    PID=$(pgrep -f "discord_bot_mcp_enhanced")
    echo "  Status: Running (PID: $PID)"
else
    echo "  Status: Not running"
fi
echo ""

# Check Ollama API
echo "[Ollama API]"
if curl -s http://localhost:11434/api/tags &>/dev/null; then
    echo "  Status: Running (http://localhost:11434)"
else
    echo "  Status: Not responding"
fi
echo ""

# Check MCP Bridge HTTP
echo "[MCP Bridge HTTP]"
if curl -s http://localhost:8765/ &>/dev/null; then
    echo "  Status: Running (http://localhost:8765)"
else
    echo "  Status: Not responding"
fi
echo ""

echo "============================================================"
echo ""
echo "To start MCP Bridge:  ./scripts/linux/start_mcp_bridge.sh"
echo "To start PhiGEN Bot:  ./scripts/linux/start_phigen_bot.sh"
echo ""
echo "============================================================"
echo ""
