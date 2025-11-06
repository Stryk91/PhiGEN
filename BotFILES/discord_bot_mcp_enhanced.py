#!/usr/bin/env python3
"""
PhiGEN Discord Bot with MCP Integration
Enhanced version that can receive commands from MCP bridge
"""

import discord
from discord.ext import commands, tasks
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import asyncio

# Configuration
TOKEN_ENV = os.getenv('DISCORD_TOKEN')
TOKEN = TOKEN_ENV if TOKEN_ENV else "MTM5MDY1MzgyMjUzNTM0MDE2Mg.GIU30F.PC1PtNInVO8qvXNr1zmozb9BhXbFOJP2ZTwkBI"
CHANNEL_ID = 1353335432179482657
ALLOWED_USER_ID = 821263652899782656
AGENT_FEED_PATH = r'E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl'
BOTFILES_DIR = r'E:\PythonProjects\PhiGEN\BotFILES'
MCP_COMMAND_QUEUE = os.path.join(BOTFILES_DIR, 'mcp_command_queue.jsonl')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Track processed MCP commands
processed_commands = set()

def read_agent_feed():
    """Read the entire agent feed"""
    try:
        if not os.path.exists(AGENT_FEED_PATH):
            return [], None

        with open(AGENT_FEED_PATH, 'r', encoding='utf-8') as f:
            lines = f.read().strip().split('\n')

        entries = []
        for line in lines:
            if line.strip():
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return entries, None
    except Exception as e:
        return None, str(e)

def get_jc_latest():
    """Get JC's latest activity"""
    entries, error = read_agent_feed()
    if error:
        return None, error

    for entry in reversed(entries):
        if entry.get('agent') == 'JC':
            return entry, None

    return None, "No JC entries found"

def format_jc_status(entry):
    """Format JC's status for Discord"""
    if not entry:
        return "No JC activity found"

    action = entry.get('action', 'unknown')
    timestamp = entry.get('timestamp', 'unknown')
    details = entry.get('details', {})

    output = f"**JC's Latest Activity**\n"
    output += f"**Action:** {action}\n"
    output += f"**Time:** {timestamp}\n\n"

    if action == 'task_complete':
        output += f"Completed: {details.get('task', 'unknown')}\n"
        output += f"**Tests:** {'Passing' if details.get('tests_passing') else 'Failing'}\n"
        output += f"**Files:** {', '.join(details.get('files', []))}\n"
        output += f"**Notes:** {details.get('notes', 'none')}\n"

    elif action == 'task_started':
        output += f"Working on: {details.get('task', 'unknown')}\n"

    elif action == 'issue_found':
        output += f"Issue: {details.get('issue', 'unknown')}\n"
        output += f"**Severity:** {details.get('severity', 'unknown')}\n"

    return output

async def process_mcp_commands():
    """Process commands from MCP bridge"""
    if not os.path.exists(MCP_COMMAND_QUEUE):
        return

    try:
        with open(MCP_COMMAND_QUEUE, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        channel = bot.get_channel(CHANNEL_ID)
        if not channel:
            return

        for line in lines:
            if not line.strip():
                continue

            try:
                command = json.loads(line)
                command_id = hash(line)

                # Skip if already processed
                if command_id in processed_commands:
                    continue

                # Mark as processed
                processed_commands.add(command_id)

                # Handle different command types
                if command.get('type') == 'send_message':
                    message = command.get('message', '')
                    await channel.send(f"[MCP] {message}")

                elif command.get('tool') == 'discord_send_message':
                    params = command.get('parameters', {})
                    message = params.get('message', '')
                    await channel.send(f"[MCP] {message}")

            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"Error processing MCP command: {e}")

    except Exception as e:
        print(f"Error reading MCP queue: {e}")

@tasks.loop(seconds=5)
async def check_mcp_queue():
    """Periodically check for MCP commands"""
    await process_mcp_commands()

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user}')
    print(f'Connected to {len(bot.guilds)} server(s)')

    # Start MCP queue checker
    if not check_mcp_queue.is_running():
        check_mcp_queue.start()

    # Send startup message
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("**PhiGEN Bot with MCP Integration Online!**\n\nMCP Bridge enabled - Claude can now control me remotely!\n\nType `!help` for commands.")

@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Only respond in the specified channel
    if message.channel.id != CHANNEL_ID:
        return

    # Only respond to the authorized user
    if message.author.id != ALLOWED_USER_ID:
        return

    # Process commands
    await bot.process_commands(message)

# Basic Commands
@bot.command(name='check_jc', aliases=['jc', 'status'])
async def check_jc(ctx):
    """Check JC's latest status"""
    await ctx.send("Checking JC's status...")

    entry, error = get_jc_latest()

    if error:
        await ctx.send(f"Error: {error}")
        return

    status = format_jc_status(entry)
    await ctx.send(status)

@bot.command(name='feed', aliases=['recent', 'activity'])
async def show_feed(ctx, count: int = 5):
    """Show recent agent feed activity"""
    await ctx.send(f"Fetching last {count} entries...")

    entries, error = read_agent_feed()

    if error:
        await ctx.send(f"Error: {error}")
        return

    recent = entries[-count:] if len(entries) >= count else entries

    output = f"**Last {len(recent)} Entries**\n\n"

    for i, entry in enumerate(recent, 1):
        agent = entry.get('agent', 'unknown')
        action = entry.get('action', 'unknown')
        timestamp = entry.get('timestamp', 'unknown')[:19]

        output += f"**{i}. [{agent}]** {action}\n"

        if action == 'task_assigned':
            details = entry.get('details', {})
            output += f"   {details.get('task', 'unknown')[:50]}...\n"
        elif action == 'task_complete':
            details = entry.get('details', {})
            output += f"   {details.get('task', 'unknown')[:50]}...\n"

        output += "\n"

    if len(output) > 1900:
        chunks = [output[i:i+1900] for i in range(0, len(output), 1900)]
        for chunk in chunks:
            await ctx.send(chunk)
    else:
        await ctx.send(output)

@bot.command(name='mcp_status', aliases=['mcp'])
async def mcp_status(ctx):
    """Check MCP bridge status"""
    await ctx.send("Checking MCP bridge status...")

    try:
        import requests
        response = requests.get('http://localhost:5000/mcp/status', timeout=5)

        if response.status_code == 200:
            data = response.json()
            output = "**MCP Bridge Status**\n\n"
            output += f"**Status:** {data.get('status', 'unknown')}\n"
            output += f"**Queue Size:** {data.get('queue_size', 0)}\n"
            output += f"**Feed Entries:** {data.get('feed_entries', 0)}\n"
            output += f"**Last Check:** {data.get('timestamp', 'unknown')[:19]}\n"
            await ctx.send(output)
        else:
            await ctx.send(f"MCP Bridge returned error: {response.status_code}")

    except requests.exceptions.ConnectionError:
        await ctx.send("MCP Bridge is not running or not accessible")
    except Exception as e:
        await ctx.send(f"Error checking MCP bridge: {e}")

@bot.command(name='ping')
async def ping(ctx):
    """Test bot responsiveness"""
    await ctx.send(f"Pong! Latency: {round(bot.latency * 1000)}ms")

@bot.command(name='help')
async def help_command(ctx):
    """Show available commands"""
    help_text = """
**PhiGEN Bot with MCP Integration**

**Agent Feed:**
`!check_jc` / `!jc` - Check JC's latest status
`!feed [count]` - Show recent activity

**MCP Integration:**
`!mcp_status` / `!mcp` - Check MCP bridge status

**System:**
`!ping` - Test bot responsiveness
`!help` - Show this help message

**MCP Features:**
- Claude can send messages through the MCP bridge
- Commands are processed every 5 seconds
- Full integration with agent feed system
    """
    await ctx.send(help_text)

@bot.event
async def on_command_error(ctx, error):
    if ctx.author.id != ALLOWED_USER_ID:
        return

    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Unknown command. Type `!help` for available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param.name}")
    else:
        await ctx.send(f"Error: {error}")
        print(f"Error: {error}")

# Run the bot
if __name__ == '__main__':
    print("Starting PhiGEN Discord Bot with MCP Integration...")
    print(f"Listening on channel: {CHANNEL_ID}")
    print(f"MCP Queue: {MCP_COMMAND_QUEUE}")

    # Ensure directories exist
    Path(BOTFILES_DIR).mkdir(parents=True, exist_ok=True)

    bot.run(TOKEN)
