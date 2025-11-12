#!/bin/bash
# PhiGEN MCP Bridge Starter - WSL/Linux
# Convenience wrapper for scripts/linux/start_mcp_bridge.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/scripts/linux/start_mcp_bridge.sh" "$@"
