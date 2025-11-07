#!/usr/bin/env python3
"""
JC Discord Integration
Allows JC to read Discord messages and respond
Two-way communication with the team!
"""

import discord
from discord.ext import commands
import json
import asyncio
from datetime import datetime, timezone
from pathlib import Path

# Configuration
TOKEN = "MTQzNTc5OTk2MTIwMjg1MTkwMQ.G31phL.67kx2Ktoz-H3fKuuMdy2XCw3MeBfOLROSEFxNY"
CHANNEL_ID = 1353335432179482657  # Same channel as DC bot
AGENT_FEED_PATH = r'E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl'

# Authorized user IDs (can be multiple)
AUTHORIZED_USER_IDS = {
    1390653822535340162,  # Stryk (primary Discord ID)
    821263652899782656,   # Stryker (alternate ID)
}

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents, help_command=None)

# Helper Functions
def log_to_feed(action, details):
    """Log JC's actions to the agent feed"""
    try:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": "JC",
            "action": action,
            "details": details
        }
        
        with open(AGENT_FEED_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")
        
        return True
    except Exception as e:
        print(f"Error logging to feed: {e}")
        return False

def read_latest_task():
    """Read the latest task from agent feed"""
    try:
        with open(AGENT_FEED_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Find latest task_assigned to JC
        for line in reversed(lines):
            entry = json.loads(line)
            if entry.get('agent') == 'DC' and entry.get('action') == 'task_assigned':
                return entry
        
        return None
    except Exception as e:
        print(f"Error reading feed: {e}")
        return None

# Bot Events
@bot.event
async def on_ready():
    print(f'✅ JC Bot logged in as {bot.user}')
    print(f'✅ Connected to {len(bot.guilds)} server(s)')
    
    # Send startup message
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("👨‍💻 **JC Online!**\nJetBrains Claude ready and monitoring the feed.\n\nMention me with `@JC <command>` to interact!")
        
        # Log to feed
        log_to_feed("session_start", {
            "message": "JC Discord integration started",
            "channel_id": CHANNEL_ID
        })

@bot.event
async def on_message(message):
    # Ignore own messages
    if message.author == bot.user:
        return
    
    # Debug print
    print(f"📨 Message received: '{message.content}' from {message.author}")
    print(f"   Channel ID: {message.channel.id}")
    print(f"   Author ID: {message.author.id}")
    print(f"   Bot mentioned: {bot.user in message.mentions}")
    
    # Only respond in the designated channel
    if message.channel.id != CHANNEL_ID:
        print(f"   ❌ Wrong channel")
        return
    
    # Only respond to authorized users
    if message.author.id not in AUTHORIZED_USER_IDS:
        print(f"   ❌ Unauthorized user (ID: {message.author.id})")
        return
    
    print(f"   ✅ Processing command...")
    # Process commands and mentions
    await bot.process_commands(message)

# JC Commands
@bot.command(name='status')
async def status_command(ctx):
    """Report JC's current status"""
    await ctx.send("👨‍💻 **JC Status Report**\n\nI'm online and monitoring the agent feed. Ready to take on tasks!")

@bot.command(name='task')
async def current_task(ctx):
    """Show current task"""
    task = read_latest_task()
    
    if not task:
        await ctx.send("📋 No tasks currently assigned.")
        return
    
    details = task.get('details', {})
    task_desc = details.get('task', 'Unknown')
    priority = details.get('priority', 'MEDIUM')
    timestamp = task.get('timestamp', 'Unknown')
    
    output = f"**📋 Current Task**\n\n"
    output += f"**Priority:** {priority}\n"
    output += f"**Task:** {task_desc}\n"
    output += f"**Assigned:** {timestamp[:19]}\n"
    
    await ctx.send(output)

@bot.command(name='complete')
async def mark_complete(ctx, *, notes: str = "Task completed"):
    """Mark current task as complete"""
    task = read_latest_task()
    
    if not task:
        await ctx.send("❌ No task to mark as complete")
        return
    
    task_desc = task.get('details', {}).get('task', 'Unknown task')
    
    # Log completion to feed
    log_to_feed("task_complete", {
        "task": task_desc,
        "notes": notes,
        "completed_via": "Discord",
        "completed_by": str(ctx.author)
    })
    
    await ctx.send(f"✅ **Task Marked Complete!**\n\n**Task:** {task_desc}\n**Notes:** {notes}")

@bot.command(name='ask')
async def ask_question(ctx, *, question: str):
    """Ask a question to the team"""
    await ctx.send(f"❓ **JC Question:**\n\n{question}")
    
    # Log to feed
    log_to_feed("question", {
        "question": question,
        "asked_via": "Discord"
    })

@bot.command(name='report')
async def report_status(ctx, *, status: str):
    """Report status update"""
    await ctx.send(f"📊 **JC Status Update:**\n\n{status}")
    
    # Log to feed
    log_to_feed("status_update", {
        "status": status,
        "reported_via": "Discord"
    })

@bot.command(name='issue')
async def report_issue(ctx, severity: str, *, description: str):
    """Report an issue or blocker"""
    severity = severity.upper()
    
    color_emoji = {
        "LOW": "🟢",
        "MEDIUM": "🟡",
        "HIGH": "🔴",
        "CRITICAL": "🚨"
    }
    
    emoji = color_emoji.get(severity, "⚠️")
    
    await ctx.send(f"{emoji} **Issue Found - {severity}**\n\n{description}")
    
    # Log to feed
    log_to_feed("issue_found", {
        "severity": severity,
        "issue": description,
        "needs_attention": severity in ["HIGH", "CRITICAL"]
    })

@bot.command(name='help')
async def help_command(ctx):
    """Show JC commands"""
    help_text = """
**👨‍💻 JC Commands**

Mention me with `@JC <command>` to use:

**Status:**
`@JC status` - Check if I'm online
`@JC task` - Show current task
`@JC report <status>` - Report progress update

**Task Management:**
`@JC complete <notes>` - Mark task complete
`@JC issue <severity> <description>` - Report issue

**Communication:**
`@JC ask <question>` - Ask the team a question
`@JC help` - Show this help

**Examples:**
`@JC status`
`@JC complete Added 16 tests, all passing`
`@JC issue HIGH Found bug in validation logic`
`@JC ask Should I refactor this before Task 5?`
    """
    await ctx.send(help_text)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if ctx.author.id not in AUTHORIZED_USER_IDS:
        return
    
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Unknown command. Use `@JC help` for available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument: {error.param.name}")
    else:
        await ctx.send(f"❌ Error: {error}")
        print(f"Error: {error}")

# Run the bot
if __name__ == '__main__':
    print("🚀 Starting JC Discord Bot...")
    print(f"📡 Listening on channel: {CHANNEL_ID}")
    print(f"👤 Authorized users: {', '.join(str(uid) for uid in AUTHORIZED_USER_IDS)}")
    bot.run(TOKEN)
