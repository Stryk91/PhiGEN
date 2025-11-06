# Discord MCP Test Commands

Once Claude Code has loaded the Discord MCP tools (after restart), you can test with these commands:

## Basic Tests

### 1. List Discord Servers
```
You: "List all Discord servers the bot is in"
Claude: [Shows server names and IDs]
```

### 2. List Channels
```
You: "What channels are in my Discord server?"
Claude: [Shows all channels with IDs]
```

### 3. Read Messages
```
You: "Show me the last 5 messages from #general"
Claude: [Fetches and displays recent messages]
```

### 4. Send a Message
```
You: "Send 'Hello from Claude MCP!' to #general"
Claude: [Posts message to Discord]
```

### 5. Search Messages
```
You: "Search Discord for messages containing 'password vault'"
Claude: [Searches and shows relevant messages]
```

## Advanced Tests

### Channel Management
```
You: "Create a new channel called #claude-test"
Claude: [Creates the channel]
```

### Reactions
```
You: "React with 👍 to the latest message in #general"
Claude: [Adds reaction emoji]
```

### Forum Posts
```
You: "Create a forum post in #announcements about the new MCP integration"
Claude: [Creates forum thread]
```

### Webhooks
```
You: "Create a webhook for #dev-updates called 'Build Status'"
Claude: [Creates webhook and returns URL]
```

## Integration Tests

### Git + Discord Workflow
1. Make a commit
2. Git hook posts to Discord webhook
3. Ask Claude: "What was just posted to Discord?"
4. Claude reads the message via MCP
5. Ask Claude to summarize or respond

### Team Coordination
```
You: "Check #code-review for any feedback on my last commit"
Claude: [Searches messages, summarizes feedback]

You: "Reply to the discussion and say I'll implement the changes"
Claude: [Posts reply to Discord]
```

### Documentation Generation
```
You: "Read all messages from #support this week and create a FAQ"
Claude: [Analyzes Discord messages, generates FAQ document]
```

## Verification Steps

To verify Discord MCP is loaded:

1. Ask Claude: "Do you have Discord MCP tools available?"
2. Claude should respond with a list of Discord-related tools
3. If not, restart Claude Code to reload `.mcp.json`

## Current Status

- ✅ Discord bot is online
- ✅ MCP server running in Docker (phigen-discord-mcp)
- ✅ Webhook notifications working
- ⏳ Waiting for Claude Code to load MCP tools (requires restart)

## Troubleshooting

If Discord MCP tools aren't available:

1. Restart Claude Code
2. Check `.mcp.json` is in project root
3. Verify Docker container is running: `docker ps | grep discord-mcp`
4. Check logs: `docker logs phigen-discord-mcp`
5. Verify bot has permissions in Discord server

## Quick Commands

Start MCP server:
```bash
.\phigen.ps1 discord-mcp
# or
make discord-mcp
```

Stop MCP server:
```bash
.\phigen.ps1 discord-stop
# or
make discord-stop
```

Check status:
```bash
docker ps | grep discord-mcp
docker logs phigen-discord-mcp
```
