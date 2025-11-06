# Discord MCP Integration Guide

## Overview

This integration connects the PhiGEN Discord bot with MCP (Model Context Protocol), allowing Claude to control the Discord bot remotely and interact with your Discord server programmatically.

## Architecture

```
Claude Code <-> MCP Bridge (HTTP API) <-> Discord Bot <-> Discord Server
                 (Port 5000)              (Python Bot)
```

### Components

1. **Discord MCP Server** (barryy625/mcp-discord:latest)
   - Docker container running on port 3000
   - Official Discord MCP integration
   - Provides full Discord API access through MCP

2. **Discord MCP Bridge** (discord_mcp_bridge.py)
   - Python Flask HTTP API on port 5000
   - Exposes Discord bot controls as MCP-compatible endpoints
   - Manages command queue for bot communication

3. **Enhanced Discord Bot** (discord_bot_mcp_enhanced.py)
   - Python Discord bot with MCP integration
   - Polls command queue every 5 seconds
   - Executes commands from MCP bridge

## Features

### MCP Tools Available

The bridge exposes these tools for Claude to use:

1. **discord_send_message**
   - Send messages to Discord channels
   - Parameters: message (string), channel (optional)

2. **discord_check_jc_status**
   - Check JC agent's latest status
   - Returns: Latest JC activity from agent feed

3. **discord_read_feed**
   - Read recent agent feed entries
   - Parameters: limit (integer, default: 10)

4. **discord_assign_task**
   - Assign tasks to agents via agent feed
   - Parameters: agent (string), task (string), priority (string)

5. **discord_list_botfiles**
   - List files in BotFILES directory
   - Returns: Array of files with metadata

6. **discord_read_botfile**
   - Read file contents from BotFILES
   - Parameters: filename (string)

### API Endpoints

**Health Check:**
```bash
GET http://localhost:5000/health
```

**List Tools:**
```bash
GET http://localhost:5000/mcp/tools
```

**Execute Tool:**
```bash
POST http://localhost:5000/mcp/execute
Content-Type: application/json

{
  "tool": "discord_send_message",
  "parameters": {
    "message": "Hello from MCP!"
  }
}
```

**Get Status:**
```bash
GET http://localhost:5000/mcp/status
```

## Setup

### Option 1: Docker (Recommended)

Start all MCP services:
```bash
docker-compose --profile mcp up -d
```

This starts:
- Discord MCP server (port 3000)
- Discord MCP bridge (port 5000)

### Option 2: Local Python

**Terminal 1 - Start MCP Bridge:**
```bash
cd BotFILES
python discord_mcp_bridge.py
```

**Terminal 2 - Start Enhanced Bot:**
```bash
cd BotFILES
python discord_bot_mcp_enhanced.py
```

**Or use the batch script:**
```bash
BotFILES\start_mcp_integration.bat
```

## Usage Examples

### From Claude Code

Once the MCP bridge is running, Claude can control the Discord bot:

**Example 1: Send a message to Discord**
```
You: "Send 'Hello team!' to Discord"
Claude: [Uses MCP bridge to queue message]
Bot: Sends message to Discord channel
```

**Example 2: Check JC's status**
```
You: "What is JC working on?"
Claude: [Calls discord_check_jc_status]
Bot: Returns JC's latest activity
```

**Example 3: Assign a task**
```
You: "Assign a high priority task to JC: Fix the login bug"
Claude: [Calls discord_assign_task with priority=HIGH]
Bot: Writes task to agent feed
```

### From Discord

The bot responds to these commands:

- `!jc` - Check JC's status
- `!feed 10` - Show last 10 feed entries
- `!mcp` - Check MCP bridge status
- `!ping` - Test bot latency
- `!help` - Show all commands

## File Locations

```
PhiGEN/
├── BotFILES/
│   ├── discord_mcp_bridge.py       # MCP HTTP bridge
│   ├── discord_bot_mcp_enhanced.py # Enhanced bot
│   ├── start_mcp_integration.bat   # Windows startup script
│   ├── mcp_command_queue.jsonl     # Command queue (auto-created)
│   └── mcp_responses.jsonl         # Response log (auto-created)
├── docs/
│   └── agent-feed.jsonl            # Agent communication feed
├── docker-compose.yml              # Container definitions
└── .mcp.json                       # MCP configuration
```

## How It Works

### Command Flow

1. **Claude → MCP Bridge**
   - Claude calls MCP tool (e.g., `discord_send_message`)
   - Bridge receives HTTP POST to `/mcp/execute`

2. **Bridge → Command Queue**
   - Bridge writes command to `mcp_command_queue.jsonl`
   - Command includes timestamp and parameters

3. **Bot Polls Queue**
   - Bot checks queue every 5 seconds
   - Reads new commands from JSONL file

4. **Bot → Discord**
   - Bot executes command
   - Sends message/performs action on Discord

5. **Response Flow**
   - Bot logs response to `mcp_responses.jsonl`
   - Bridge can query responses via API

### Agent Feed Integration

The MCP bridge integrates with the agent feed system:

- Tasks assigned via MCP are written to agent-feed.jsonl
- JC and other agents can read tasks from the feed
- Status updates flow back through the feed
- Complete agent communication loop

## Testing

### Test MCP Bridge

```bash
# Health check
curl http://localhost:5000/health

# List available tools
curl http://localhost:5000/mcp/tools

# Send a test message
curl -X POST http://localhost:5000/mcp/execute \
  -H "Content-Type: application/json" \
  -d '{"tool":"discord_send_message","parameters":{"message":"Test from MCP!"}}'

# Check status
curl http://localhost:5000/mcp/status
```

### Test Bot Integration

1. Start the bridge and bot
2. Use curl to send a message via bridge
3. Check Discord - message should appear within 5 seconds
4. Use `!mcp` command in Discord to verify bridge connection

## Monitoring

### Check MCP Bridge Status
```bash
curl http://localhost:5000/mcp/status
```

Returns:
- Queue size
- Feed entries count
- BotFILES directory
- Timestamp

### Check Bot Status

In Discord, use:
```
!mcp
```

Shows:
- Bridge connection status
- Queue size
- Last update time

### View Logs

**Docker:**
```bash
docker logs phigen-discord-bridge
docker logs phigen-discord-mcp
```

**Local:**
- Check terminal windows where services are running

## Troubleshooting

### Bridge Not Starting

**Error:** Port 5000 already in use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <pid> /F

# Linux
lsof -i :5000
kill -9 <pid>
```

### Bot Not Processing Commands

1. Check if bot is running: `docker ps` or check terminal
2. Verify command queue exists: `BotFILES/mcp_command_queue.jsonl`
3. Check bot logs for errors
4. Use `!mcp` in Discord to test bridge connection

### Bridge Not Accessible

1. Verify Flask is running: `curl http://localhost:5000/health`
2. Check firewall settings
3. Ensure port 5000 is not blocked
4. Check Docker network (if using Docker)

### Commands Not Executing

1. Check command format in queue file
2. Verify bot has permissions in Discord
3. Check bot is in correct channel
4. Review bot logs for errors

## Security Notes

- The MCP bridge runs on localhost by default
- No authentication is implemented (localhost-only access)
- Discord bot token should be kept secure
- Command queue is file-based (no external dependencies)
- Agent feed may contain sensitive task information

## Next Steps

### Potential Enhancements

1. **Add Response Tracking**
   - Return execution results to MCP
   - Store responses in mcp_responses.jsonl

2. **Add More Tools**
   - File upload to Discord
   - Image generation and posting
   - Voice channel control

3. **Add Authentication**
   - API key for MCP bridge
   - User-based permissions

4. **Add Webhooks**
   - Real-time event notifications
   - Bidirectional communication

5. **Add Database**
   - Replace JSONL with SQLite
   - Better query performance
   - Transaction support

## Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MCP Specification](https://github.com/modelcontextprotocol)
- [Discord MCP Server](https://github.com/barryyip0625/mcp-discord)

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review bot and bridge logs
3. Test with curl commands
4. Verify Discord bot permissions
