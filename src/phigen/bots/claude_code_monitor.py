#!/usr/bin/env python3
"""
Claude Code Monitor
Watches bulletin board and responds as "Claude Code" using Claude API
"""

import anthropic
import os
import json
import time
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

# Configuration
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
SHARED_BOARD = os.path.join(os.path.dirname(__file__), "shared_messages.jsonl")
CHECK_INTERVAL = 2  # seconds

# Validate
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in .env")

# Initialize Claude client
claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Track processed messages
processed = set()

def read_bulletin_board():
    """Read all messages from bulletin board"""
    if not os.path.exists(SHARED_BOARD):
        return []

    with open(SHARED_BOARD, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    messages = []
    for line in lines:
        if line.strip():
            try:
                messages.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return messages

def write_to_bulletin_board(entry):
    """Write response to bulletin board"""
    with open(SHARED_BOARD, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n')

def respond_as_claude_code(message_data):
    """Respond to message as Claude Code using API"""
    user_message = message_data['message']
    author = message_data['author']

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Message from {author}: {user_message[:50]}...")

    try:
        # Call Claude API as "Claude Code"
        response = claude_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=150,
            system="You are Claude Code, an AI assistant integrated into an IDE. You help with coding, debugging, and development tasks. Be terse. 1-2 sentences MAX.",
            messages=[{
                "role": "user",
                "content": user_message
            }]
        )

        response_text = response.content[0].text

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Claude Code responds: {response_text[:50]}...")

        # Write response to bulletin board
        response_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "from": "claude_code",
            "to": "discord_bot",
            "message": response_text,
            "in_reply_to": message_data['timestamp'],
            "original_author": author,
            "channel": message_data['channel']
        }

        write_to_bulletin_board(response_entry)

        return True

    except anthropic.APIError as e:
        print(f"[ERROR] API Error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def monitor_loop():
    """Main monitoring loop"""
    print("="*60)
    print("Claude Code Monitor Started")
    print("="*60)
    print(f"Bulletin Board: {SHARED_BOARD}")
    print(f"Check Interval: {CHECK_INTERVAL} seconds")
    print(f"API Key: {'Present' if ANTHROPIC_API_KEY else 'Missing'}")
    print("="*60)
    print("\nMonitoring bulletin board for messages...\n")

    while True:
        try:
            messages = read_bulletin_board()

            # Find messages for Claude Code that haven't been processed
            for msg in messages:
                if msg.get('to') == 'claude_code':
                    msg_id = msg.get('timestamp')

                    if msg_id not in processed:
                        # Process this message
                        respond_as_claude_code(msg)
                        processed.add(msg_id)

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n\nMonitor stopped by user.")
            break
        except Exception as e:
            print(f"[ERROR] Monitor loop error: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    monitor_loop()
