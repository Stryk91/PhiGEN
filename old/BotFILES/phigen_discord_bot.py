#!/usr/bin/env python3
"""
PhiGEN Desktop Discord Bot
Executes commands on Windows desktop and reports to Discord
"""

import discord
from discord.ext import commands
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Configuration
TOKEN = "MTM5MDY1MzgyMjUzNTM0MDE2Mg.GIU30F.PC1PtNInVO8qvXNr1zmozb9BhXbFOJP2ZTwkBI"
CHANNEL_ID = 1353335432179482657
ALLOWED_USER_ID = 821263652899782656  # Stryker's user ID - only this user can use commands
AGENT_FEED_PATH = r'E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl'
BOTFILES_DIR = r'E:\PythonProjects\PhiGEN\BotFILES'  # DC has full access to this directory

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Helper Functions
def read_agent_feed():
    """Read the entire agent feed"""
    try:
        with open(AGENT_FEED_PATH, 'r', encoding='utf-8') as f:
            lines = f.read().strip().split('\n')
        entries = []
        for line in lines:
            if line.strip():
                entries.append(json.loads(line))
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
        return "❌ No JC activity found"
    
    action = entry.get('action', 'unknown')
    timestamp = entry.get('timestamp', 'unknown')
    details = entry.get('details', {})
    
    output = f"**📋 JC's Latest Activity**\n"
    output += f"**Action:** {action}\n"
    output += f"**Time:** {timestamp}\n\n"
    
    if action == 'task_complete':
        output += f"✅ **Completed:** {details.get('task', 'unknown')}\n"
        output += f"**Tests:** {'✅ Passing' if details.get('tests_passing') else '❌ Failing'}\n"
        output += f"**Files:** {', '.join(details.get('files', []))}\n"
        output += f"**Notes:** {details.get('notes', 'none')}\n"
    
    elif action == 'task_started':
        output += f"🔄 **Working on:** {details.get('task', 'unknown')}\n"
    
    elif action == 'issue_found':
        output += f"⚠️ **Issue:** {details.get('issue', 'unknown')}\n"
        output += f"**Severity:** {details.get('severity', 'unknown')}\n"
    
    return output

def get_recent_activity(n=5):
    """Get recent activity from all agents"""
    entries, error = read_agent_feed()
    if error:
        return f"❌ Error: {error}"
    
    recent = entries[-n:] if len(entries) >= n else entries
    
    output = f"**📋 Last {len(recent)} Entries**\n\n"
    
    for i, entry in enumerate(recent, 1):
        agent = entry.get('agent', 'unknown')
        action = entry.get('action', 'unknown')
        timestamp = entry.get('timestamp', 'unknown')[:19]  # Trim to readable length
        
        output += f"**{i}. [{agent}]** {action}\n"
        
        if action == 'task_assigned':
            details = entry.get('details', {})
            output += f"   📝 {details.get('task', 'unknown')[:50]}...\n"
        elif action == 'task_complete':
            details = entry.get('details', {})
            output += f"   ✅ {details.get('task', 'unknown')[:50]}...\n"
        
        output += "\n"
    
    return output

# Bot Events
@bot.event
async def on_ready():
    print(f'✅ Bot logged in as {bot.user}')
    print(f'✅ Connected to {len(bot.guilds)} server(s)')
    
    # Send startup message to channel
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("🤖 **PhiGEN Desktop Bot Online!**\nReady to execute commands.\n\nType `!help` for available commands.")

@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return
    
    # Only respond in the specified channel
    if message.channel.id != CHANNEL_ID:
        return
    
    # Only respond to the authorized user (Stryker)
    if message.author.id != ALLOWED_USER_ID:
        # Silently ignore commands from other users
        return
    
    # Process commands
    await bot.process_commands(message)

# Commands
@bot.command(name='check_jc', aliases=['jc', 'status'])
async def check_jc(ctx):
    """Check JC's latest status"""
    await ctx.send("🔍 Checking JC's status...")
    
    entry, error = get_jc_latest()
    
    if error:
        await ctx.send(f"❌ Error: {error}")
        return
    
    status = format_jc_status(entry)
    await ctx.send(status)

@bot.command(name='feed', aliases=['recent', 'activity'])
async def show_feed(ctx, count: int = 5):
    """Show recent agent feed activity"""
    await ctx.send(f"📋 Fetching last {count} entries...")
    
    output = get_recent_activity(count)
    
    # Discord has a 2000 char limit per message
    if len(output) > 1900:
        # Split into chunks
        chunks = [output[i:i+1900] for i in range(0, len(output), 1900)]
        for chunk in chunks:
            await ctx.send(chunk)
    else:
        await ctx.send(output)

@bot.command(name='read')
async def read_file(ctx, *, path: str):
    """Read a file from the desktop"""
    await ctx.send(f"📄 Reading: `{path}`...")
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if len(content) > 1900:
            # Too long, save to file and upload
            temp_file = Path("temp_output.txt")
            temp_file.write_text(content, encoding='utf-8')
            await ctx.send(file=discord.File("temp_output.txt"))
            temp_file.unlink()
        else:
            await ctx.send(f"```\n{content}\n```")
    
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command(name='run', aliases=['cmd', 'exec'])
async def run_command(ctx, *, command: str):
    """Run a shell command on the desktop"""
    await ctx.send(f"⚡ Executing: `{command}`...")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = f"**Return Code:** {result.returncode}\n\n"
        
        if result.stdout:
            output += f"**STDOUT:**\n```\n{result.stdout[:1500]}\n```\n"
        
        if result.stderr:
            output += f"**STDERR:**\n```\n{result.stderr[:500]}\n```"
        
        if len(output) > 1900:
            temp_file = Path("command_output.txt")
            temp_file.write_text(f"Command: {command}\n\n{result.stdout}\n\nErrors:\n{result.stderr}", encoding='utf-8')
            await ctx.send(file=discord.File("command_output.txt"))
            temp_file.unlink()
        else:
            await ctx.send(output)
    
    except subprocess.TimeoutExpired:
        await ctx.send("❌ Command timed out (30s limit)")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command(name='list', aliases=['ls', 'dir'])
async def list_directory(ctx, *, path: str = '.'):
    """List directory contents"""
    await ctx.send(f"📁 Listing: `{path}`...")
    
    try:
        items = os.listdir(path)
        
        output = f"**Directory:** `{path}`\n**Items:** {len(items)}\n\n"
        
        for item in items[:50]:  # Limit to 50 items
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                output += f"📁 {item}\n"
            else:
                output += f"📄 {item}\n"
        
        if len(items) > 50:
            output += f"\n... and {len(items) - 50} more items"
        
        await ctx.send(output)
    
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command(name='ping')
async def ping(ctx):
    """Test bot responsiveness"""
    await ctx.send(f"🏓 Pong! Latency: {round(bot.latency * 1000)}ms")

# BotFILES Commands (DC's workspace)
@bot.command(name='botfiles', aliases=['bf', 'botls'])
async def list_botfiles(ctx):
    """List files in the BotFILES directory"""
    await ctx.send(f"📁 Listing BotFILES directory...")
    
    try:
        items = os.listdir(BOTFILES_DIR)
        
        if not items:
            await ctx.send("📁 BotFILES directory is empty")
            return
        
        output = f"**📁 BotFILES Directory**\n"
        output += f"**Path:** `{BOTFILES_DIR}`\n"
        output += f"**Items:** {len(items)}\n\n"
        
        for item in items[:30]:  # Limit to 30 items
            item_path = os.path.join(BOTFILES_DIR, item)
            if os.path.isdir(item_path):
                output += f"📁 {item}\n"
            else:
                size = os.path.getsize(item_path)
                output += f"📄 {item} ({size} bytes)\n"
        
        if len(items) > 30:
            output += f"\n... and {len(items) - 30} more items"
        
        await ctx.send(output)
    
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command(name='botread', aliases=['br'])
async def read_botfile(ctx, *, filename: str):
    """Read a file from BotFILES directory"""
    await ctx.send(f"📄 Reading from BotFILES: `{filename}`...")
    
    try:
        filepath = os.path.join(BOTFILES_DIR, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if len(content) > 1900:
            # Too long, save to temp file and upload
            temp_file = Path("temp_botfile.txt")
            temp_file.write_text(content, encoding='utf-8')
            await ctx.send(f"File too large, uploading:", file=discord.File("temp_botfile.txt"))
            temp_file.unlink()
        else:
            await ctx.send(f"```\n{content}\n```")
    
    except FileNotFoundError:
        await ctx.send(f"❌ File not found: `{filename}`")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command(name='botwrite', aliases=['bw'])
async def write_botfile(ctx, filename: str, *, content: str):
    """Write a file to BotFILES directory"""
    await ctx.send(f"📝 Writing to BotFILES: `{filename}`...")
    
    try:
        # Create BotFILES directory if it doesn't exist
        Path(BOTFILES_DIR).mkdir(parents=True, exist_ok=True)
        
        filepath = os.path.join(BOTFILES_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        await ctx.send(f"✅ Written to `{filename}` ({len(content)} chars)")
    
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command(name='botrun', aliases=['brun'])
async def run_botfile(ctx, *, filename: str):
    """Run a Python script from BotFILES directory"""
    await ctx.send(f"⚡ Running script from BotFILES: `{filename}`...")
    
    try:
        filepath = os.path.join(BOTFILES_DIR, filename)
        
        if not os.path.exists(filepath):
            await ctx.send(f"❌ File not found: `{filename}`")
            return
        
        result = subprocess.run(
            f'python "{filepath}"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=BOTFILES_DIR
        )
        
        output = f"**Return Code:** {result.returncode}\n\n"
        
        if result.stdout:
            output += f"**STDOUT:**\n```\n{result.stdout[:1500]}\n```\n"
        
        if result.stderr:
            output += f"**STDERR:**\n```\n{result.stderr[:500]}\n```"
        
        if len(output) > 1900:
            temp_file = Path("script_output.txt")
            temp_file.write_text(f"Script: {filename}\n\n{result.stdout}\n\nErrors:\n{result.stderr}", encoding='utf-8')
            await ctx.send(file=discord.File("script_output.txt"))
            temp_file.unlink()
        else:
            await ctx.send(output)
    
    except subprocess.TimeoutExpired:
        await ctx.send("❌ Script timed out (30s limit)")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

# JC Communication Commands
@bot.command(name='assign_task', aliases=['assign', 'task'])
async def assign_task_to_jc(ctx, priority: str, *, task_description: str):
    """Assign a task to JC through the agent feed
    
    Usage: !assign_task MEDIUM Fix the bug in password validation
    Or: !task HIGH Add new feature to UI
    """
    await ctx.send(f"📋 Assigning task to JC...")
    
    try:
        from datetime import datetime, timezone
        
        # Create task entry
        task_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": "DC",
            "action": "task_assigned",
            "details": {
                "task": task_description,
                "priority": priority.upper(),
                "assigned_via": "Discord",
                "assigned_by": str(ctx.author)
            }
        }
        
        # Read current feed
        with open(AGENT_FEED_PATH, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        # Append new task
        new_line = json.dumps(task_entry, ensure_ascii=False, separators=(",", ":"))
        updated_content = current_content + new_line + "\n"
        
        # Write back
        with open(AGENT_FEED_PATH, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        # Confirm
        output = f"✅ **Task Assigned to JC!**\n\n"
        output += f"**Priority:** {priority.upper()}\n"
        output += f"**Task:** {task_description}\n"
        output += f"**Timestamp:** {task_entry['timestamp']}\n\n"
        output += f"📢 Tell JC to check the agent feed!"
        
        await ctx.send(output)
    
    except Exception as e:
        await ctx.send(f"❌ Error assigning task: {e}")

@bot.command(name='message_jc', aliases=['msg_jc', 'tell_jc'])
async def message_jc(ctx, *, message: str):
    """Send a message/note to JC through the agent feed
    
    Usage: !message_jc Great work on Task 3! Ready for Task 4?
    """
    await ctx.send(f"💬 Sending message to JC...")
    
    try:
        from datetime import datetime, timezone
        
        # Create message entry
        message_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": "DC",
            "action": "message_to_jc",
            "details": {
                "message": message,
                "from": str(ctx.author),
                "via": "Discord"
            }
        }
        
        # Read current feed
        with open(AGENT_FEED_PATH, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        # Append message
        new_line = json.dumps(message_entry, ensure_ascii=False, separators=(",", ":"))
        updated_content = current_content + new_line + "\n"
        
        # Write back
        with open(AGENT_FEED_PATH, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        await ctx.send(f"✅ Message sent to JC!\n💬 *\"{message}\"*")
    
    except Exception as e:
        await ctx.send(f"❌ Error sending message: {e}")

@bot.command(name='quick_task', aliases=['qt'])
async def quick_task(ctx, *, task: str):
    """Quick task assignment with default MEDIUM priority
    
    Usage: !quick_task Add unit tests for the new function
    """
    await assign_task_to_jc(ctx, "MEDIUM", task_description=task)

@bot.command(name='pending')
async def show_pending(ctx):
    """Show pending tasks with numbers"""
    await ctx.send("📋 Checking pending tasks...")
    
    try:
        result = subprocess.run(
            f'python "{BOTFILES_DIR}\\get_pending.py"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            await ctx.send(f"```\n{result.stdout}\n```")
        else:
            await ctx.send(f"❌ Error: {result.stderr}")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command(name='execute', aliases=['exec_task'])
async def execute_tasks(ctx, *, task_numbers: str):
    """Queue tasks for DC to execute
    
    Usage: !execute 1,3,5  or  !execute all
    """
    await ctx.send(f"⚡ Queuing tasks: {task_numbers}")
    
    try:
        queue_file = os.path.join(BOTFILES_DIR, 'task_queue.txt')
        with open(queue_file, 'w') as f:
            f.write(task_numbers)
        
        await ctx.send(f"✅ Tasks queued. Tell DC to execute in chat.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command(name='help_commands', aliases=['commands'])
async def help_commands(ctx):
    """Show all available commands"""
    help_text = """
**🤖 PhiGEN Desktop Bot Commands**

**Agent Feed:**
`!check_jc` / `!jc` - Check JC's latest status
`!feed [count]` - Show recent activity (default: 5)

**Communicate with JC:**
`!assign_task <priority> <task>` - Assign task to JC
`!quick_task <task>` - Quick task (MEDIUM priority)
`!message_jc <message>` - Send a message to JC

**BotFILES Management (DC's workspace):**
`!botfiles` - List files in BotFILES directory
`!botread <filename>` - Read a file from BotFILES
`!botwrite <filename> <content>` - Write to BotFILES
`!botrun <filename>` - Run a Python script from BotFILES

**File Operations:**
`!read <path>` - Read any file
`!list <path>` - List directory contents

**System:**
`!run <command>` - Execute shell command
`!ping` - Test bot responsiveness

**Examples:**
`!check_jc`
`!assign_task HIGH Fix critical bug in validation`
`!quick_task Add tests for password function`
`!message_jc Great work on Task 3!`
`!botfiles`
`!feed 10`
    """
    await ctx.send(help_text)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    # Only respond to authorized user
    if ctx.author.id != ALLOWED_USER_ID:
        return
    
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Unknown command. Type `!help_commands` for available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param.name}")
    else:
        await ctx.send(f"❌ Error: {error}")
        print(f"Error: {error}")

# Run the bot
if __name__ == '__main__':
    print("🚀 Starting PhiGEN Desktop Bot...")
    print(f"📡 Listening on channel: {CHANNEL_ID}")
    bot.run(TOKEN)
