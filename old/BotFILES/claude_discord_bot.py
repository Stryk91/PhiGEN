#!/usr/bin/env python3
"""
Claude API Discord Bot
Monitors Discord messages and responds using Claude API
"""

import discord
from discord.ext import commands
import anthropic
import os
import json
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
ALLOWED_CHANNELS = [1353335432179482657, 825220914580160574]  # Channels to monitor
ALLOWED_USER_ID = 821263652899782656  # Stryker's user ID
SHARED_BOARD = os.path.join(os.path.dirname(__file__), "shared_messages.jsonl")  # Bulletin board file

# Validate configuration
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found in .env file")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in .env file")

# Initialize clients
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)
claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Background task imports
from discord.ext import tasks

# Conversation history (in memory for now)
conversation_history = []

# Track processed bulletin board messages
processed_responses = set()

@tasks.loop(seconds=3)
async def check_bulletin_board():
    """Check bulletin board for responses from Claude Code"""
    if not os.path.exists(SHARED_BOARD):
        return

    try:
        with open(SHARED_BOARD, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            if not line.strip():
                continue

            try:
                msg = json.loads(line)

                # Look for messages from Claude Code to Discord Bot
                if msg.get('from') == 'claude_code' and msg.get('to') == 'discord_bot':
                    msg_id = msg.get('timestamp')

                    if msg_id not in processed_responses:
                        # Post to Discord
                        channel_id = msg.get('channel')
                        channel = bot.get_channel(channel_id)

                        if channel:
                            response_text = msg.get('message')
                            await channel.send(f"**Claude Code:** {response_text}")

                        processed_responses.add(msg_id)

            except json.JSONDecodeError:
                continue

    except Exception as e:
        print(f"Error checking bulletin board: {e}")

@bot.event
async def on_ready():
    print(f'Claude API Discord Bot logged in as {bot.user}')
    print(f'Connected to {len(bot.guilds)} server(s)')
    print(f'Monitoring channel IDs: {ALLOWED_CHANNELS}')
    print(f'Claude API: Connected')
    print(f'Bulletin Board: {SHARED_BOARD}')

    # Start bulletin board checker
    if not check_bulletin_board.is_running():
        check_bulletin_board.start()

    for channel_id in ALLOWED_CHANNELS:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send("Claude API Bot Online! Monitoring this channel for messages.\nSay 'hey claude code' to talk to Claude Code!")

@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Only respond in allowed channels
    if message.channel.id not in ALLOWED_CHANNELS:
        return

    # Only respond to authorized user
    if message.author.id != ALLOWED_USER_ID:
        return

    # Process commands first
    await bot.process_commands(message)

    # If message starts with !, it's a command, skip Claude API
    if message.content.startswith('!'):
        return

    # Check if message is for "Claude Code" (the other AI)
    msg_lower = message.content.lower()
    if any(phrase in msg_lower for phrase in ["hey claude code", "@claude code", "claude code"]):
        # Write to bulletin board for the monitor to pick up
        board_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "from": "discord_bot",
            "to": "claude_code",
            "message": message.content,
            "author": str(message.author),
            "channel": message.channel.id
        }

        with open(SHARED_BOARD, 'a', encoding='utf-8') as f:
            f.write(json.dumps(board_entry) + '\n')

        await message.channel.send("📋 Message forwarded to Claude Code...")
        return

    # Send to Claude API (Discord Bot's own responses)
    try:
        # Show typing indicator
        async with message.channel.typing():
            # Add user message to history
            conversation_history.append({
                "role": "user",
                "content": message.content
            })

            # Call Claude API with minimal token limit and strict system prompt
            response = claude_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=150,  # MINIMAL tokens
                system="You are Claude API integrated into a Discord bot. You CAN see messages, respond, and help users. Be terse. 1-2 sentences MAX. No fluff.",
                messages=conversation_history
            )

            # Get response text
            response_text = response.content[0].text

            # Add assistant response to history
            conversation_history.append({
                "role": "assistant",
                "content": response_text
            })

            # Keep history manageable (last 10 exchanges = 20 messages)
            if len(conversation_history) > 20:
                conversation_history.pop(0)
                conversation_history.pop(0)

            # Send response to Discord
            # Discord has 2000 char limit
            if len(response_text) > 1900:
                # Split into chunks
                chunks = [response_text[i:i+1900] for i in range(0, len(response_text), 1900)]
                for chunk in chunks:
                    await message.channel.send(chunk)
            else:
                await message.channel.send(response_text)

    except anthropic.APIError as e:
        await message.channel.send(f"API Error: {str(e)}")
        print(f"Claude API Error: {e}")
    except Exception as e:
        await message.channel.send(f"Error: {str(e)}")
        print(f"Error: {e}")

# Bot commands
@bot.command(name='clear')
async def clear_history(ctx):
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    await ctx.send("Conversation history cleared.")

@bot.command(name='history')
async def show_history(ctx):
    """Show conversation history length"""
    await ctx.send(f"Conversation history: {len(conversation_history)} messages")

@bot.command(name='ping')
async def ping(ctx):
    """Test bot responsiveness"""
    await ctx.send(f"Pong! Latency: {round(bot.latency * 1000)}ms")

@bot.command(name='info')
async def info_command(ctx):
    """Show bot info"""
    help_text = """
**Claude API Discord Bot**

**Talk to Claude:**
Just type your message (no command needed)

**Commands:**
`!clear` - Clear conversation history
`!history` - Show history length
`!ping` - Test bot
`!info` - Show this info

**Features:**
- Maintains conversation context
- Responds to all messages in this channel
- Uses Claude 3 Haiku
    """
    await ctx.send(help_text)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if ctx.author.id != ALLOWED_USER_ID:
        return

    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Unknown command. Type `!info` for available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param.name}")
    else:
        await ctx.send(f"Error: {error}")
        print(f"Error: {error}")

# Run the bot
if __name__ == '__main__':
    print("Starting Claude API Discord Bot...")
    print(f"Discord Token: {'Present' if DISCORD_TOKEN else 'Missing'}")
    print(f"Anthropic API Key: {'Present' if ANTHROPIC_API_KEY else 'Missing'}")
    print(f"Allowed Channels: {ALLOWED_CHANNELS}")
    print(f"Authorized User ID: {ALLOWED_USER_ID}")

    bot.run(DISCORD_TOKEN)
