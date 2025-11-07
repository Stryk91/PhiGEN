# Discord MCP Setup Guide

## What is Discord MCP?

Discord MCP (Model Context Protocol) enables Claude to interact with your Discord server:
- Read and send messages
- Search message history
- Create and manage channels
- React to messages
- Use webhooks
- Manage forum posts

## Quick Start

### 1. Start the Discord MCP Server

**PowerShell:**
```powershell
.\phigen.ps1 discord-mcp
```

**Make (WSL/Linux):**
```bash
make discord-mcp
```

**Docker Compose:**
```bash
docker-compose --profile mcp up -d discord-mcp
```

The bot should now appear online in your Discord server!

### 2. Using Discord MCP with Claude

Once the MCP server is running, you can ask Claude to interact with Discord:

```
You: "Send a message to the #general channel saying hello"
Claude: [Uses Discord MCP to send the message]

You: "What are the last 10 messages in #dev-chat?"
Claude: [Fetches and displays recent messages]

You: "Search our Discord for discussions about the password vault"
Claude: [Searches messages and summarizes findings]
```

## Configuration

### Environment Variables

The Discord bot token is stored in `.env`:
```bash
DISCORD_TOKEN=your_bot_token_here
DISCORD_WEBHOOK_URL=your_webhook_url_here
```

**Important**: Never commit `.env` to git! It's already in `.gitignore`.

### MCP Configuration

The MCP server is configured in `.mcp.json`:
```json
{
  "mcpServers": {
    "discord": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--env-file",
        ".env",
        "barryy625/mcp-discord:latest"
      ]
    }
  }
}
```

## Available Features

### Basic Operations
- **Login**: Authenticate bot with Discord
- **List Servers**: View all servers the bot is in
- **Send Messages**: Post messages to channels
- **Get Server Info**: Fetch server details

### Channel Management
- **Create Channels**: Make new text channels
- **Delete Channels**: Remove channels
- **List Channels**: View all channels in a server

### Message Operations
- **Read Messages**: Fetch recent messages from channels
- **Search Messages**: Find messages by content
- **Delete Messages**: Remove messages
- **Add Reactions**: React to messages with emojis
- **Remove Reactions**: Remove emoji reactions

### Forums
- **Create Posts**: Start new forum threads
- **Reply to Posts**: Comment on forum threads
- **Delete Posts**: Remove forum threads

### Webhooks
- **Create Webhooks**: Set up new webhooks
- **Edit Webhooks**: Modify existing webhooks
- **Delete Webhooks**: Remove webhooks
- **Use Webhooks**: Send messages via webhooks

## Use Cases

### 1. Project Updates
```
You: "Post our latest commit to #dev-updates"
Claude: [Sends formatted commit info to Discord]
```

### 2. Code Review Discussions
```
You: "What did the team say about the UI changes in #code-review?"
Claude: [Searches and summarizes Discord discussion]
```

### 3. Bug Tracking
```
You: "Search Discord for any mentions of the login bug"
Claude: [Finds relevant messages and creates bug report]
```

### 4. Team Coordination
```
You: "Tell the team in #general that the new build is ready"
Claude: [Posts message to Discord channel]
```

### 5. Documentation
```
You: "Create a FAQ from the questions in #support"
Claude: [Analyzes Discord messages and generates FAQ]
```

## Integration with Git Hooks

You already have git hooks that post commits to Discord via webhook. Now with MCP:
1. Commit triggers webhook → Discord notification
2. Team discusses in Discord
3. Claude reads the discussion via MCP
4. You ask Claude to summarize feedback and implement changes

This creates a complete feedback loop!

## Troubleshooting

### Bot Not Coming Online
1. Check that the MCP server is running:
   ```bash
   docker ps | grep discord-mcp
   ```

2. Verify the token in `.env` is correct

3. Check Discord Developer Portal:
   - Bot has correct intents enabled
   - Bot is invited to your server

### MCP Not Working with Claude
1. Restart Claude Code to reload `.mcp.json`
2. Check Docker logs:
   ```bash
   docker logs phigen-discord-mcp
   ```

### Permission Errors
The bot needs these permissions:
- Send Messages
- Manage Messages
- Manage Channels
- Add Reactions
- View Channel
- Read Message History

Re-invite the bot with the OAuth2 URL from Discord Developer Portal.

## Stopping the MCP Server

**PowerShell:**
```powershell
.\phigen.ps1 discord-stop
```

**Make:**
```bash
make discord-stop
```

**Docker Compose:**
```bash
docker-compose stop discord-mcp
```

## Security Notes

- The `.env` file contains sensitive tokens - never share it
- The bot token gives full access to your Discord bot
- If compromised, regenerate the token in Discord Developer Portal
- The bot can only access servers it's been invited to
- Consider using role-based permissions to limit bot access

## Next Steps

1. Start the MCP server
2. Test by asking Claude to interact with Discord
3. Explore the 25+ available Discord tools
4. Integrate with your development workflow
5. Create automation scripts that use Discord as a hub

## Resources

- [Discord MCP GitHub](https://github.com/barryyip0625/mcp-discord)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Model Context Protocol Docs](https://github.com/modelcontextprotocol)
