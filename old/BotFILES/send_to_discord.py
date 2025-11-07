#!/usr/bin/env python3
"""
Script for Claude Code to send messages to Discord
Usage: python send_to_discord.py "Your message here" [channel_id]
"""

import os
import sys
import json
from datetime import datetime, timezone

SHARED_BOARD = os.path.join(os.path.dirname(__file__), "shared_messages.jsonl")
DEFAULT_CHANNEL = 825220914580160574  # Your server channel

def send_to_discord(message, channel_id=None):
    """Write message to bulletin board for Discord bot to pick up"""
    if channel_id is None:
        channel_id = DEFAULT_CHANNEL

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "from": "claude_code",
        "to": "discord_bot",
        "message": message,
        "in_reply_to": None,
        "original_author": "Claude Code (Desktop)",
        "channel": channel_id
    }

    with open(SHARED_BOARD, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n')

    print(f"Message sent to Discord channel {channel_id}")
    print(f"Content: {message}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python send_to_discord.py \"Your message here\" [channel_id]")
        sys.exit(1)

    message = sys.argv[1]
    channel_id = int(sys.argv[2]) if len(sys.argv) > 2 else None

    send_to_discord(message, channel_id)
