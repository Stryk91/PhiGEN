# Quick Discord Send Guide for DC

## Problem
The MCP bridge doesn't expose tools to Claude Desktop because it needs SSE (Server-Sent Events) protocol, not just REST API.

## Simple Solution: Use Webhook Directly

You already have a working webhook! Just use the `send_discord_message.py` script.

## For DC (Claude Desktop)

### Send Message to Discord
```bash
python BotFILES/send_discord_message.py "Your message here"
```

### Examples

**Send build notification:**
```bash
python BotFILES/send_discord_message.py "Build complete!"
```

**Send status update:**
```bash
python BotFILES/send_discord_message.py "JC: Task completed successfully"
```

**Send alert:**
```bash
python BotFILES/send_discord_message.py "ALERT: Tests failing"
```

## How It Works

1. Script uses Discord webhook
2. Message appears instantly in Discord
3. No MCP tools needed
4. No server needed
5. Works every time

## Alternative: Queue for Bot

If you want to queue messages for the bot to send:

```bash
python -c "import json; cmd={'type':'send_message','message':'Hello'}; print(json.dumps(cmd))" >> BotFILES/mcp_command_queue.jsonl
```

Then the Discord bot (if running) will pick it up within 5 seconds.

## Why MCP Tools Don't Appear

The MCP bridge I created is a REST API, but Claude Desktop expects:
- SSE (Server-Sent Events) protocol
- Or stdio protocol (command-based)
- Not HTTP REST

The phiwave-agent-hub works because it uses SSE (`/sse` endpoint).

## Fix for MCP Tools (Future)

To make Discord tools appear in Claude Desktop, we'd need to:
1. Rewrite bridge to use SSE protocol
2. Or use stdio protocol with command/args
3. Or use the official Discord MCP Docker container (port 3000)

But for now, the webhook method works perfectly!

## Summary

**What Works Now:**
- ✅ Webhook via `send_discord_message.py`
- ✅ Command queue via JSONL
- ✅ Discord bot commands (!jc, !feed, !mcp)

**What Doesn't Work Yet:**
- ❌ MCP tools in Claude Desktop (discord_send_message, etc.)

**Use This:**
```bash
python BotFILES/send_discord_message.py "Message"
```

It's simple, fast, and works!
