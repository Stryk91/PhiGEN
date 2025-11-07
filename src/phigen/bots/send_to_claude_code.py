#!/usr/bin/env python3
"""
Send message to Claude Code via window automation
Can be called directly or imported
"""

import os
import json
import time
import sys
from datetime import datetime, timezone

SHARED_BOARD = os.path.join(os.path.dirname(__file__), "shared_messages.jsonl")


def send_to_claude_code(message: str, author: str = "System") -> bool:
    """
    Send a message to Claude Code by writing to bulletin board

    Args:
        message: Text to send
        author: Who is sending it

    Returns:
        True if message was queued successfully
    """
    try:
        # Create message entry
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target": "claude_code",
            "author": author,
            "message": message,
            "processed": False
        }

        # Append to bulletin board
        with open(SHARED_BOARD, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')

        print(f"✅ Message queued for Claude Code")
        print(f"   From: {author}")
        print(f"   Message: {message[:50]}...")

        return True

    except Exception as e:
        print(f"❌ Error queueing message: {e}")
        return False


def main():
    """CLI usage"""
    if len(sys.argv) < 2:
        print("Usage: python send_to_claude_code.py <message> [author]")
        print("Example: python send_to_claude_code.py 'Hello Claude!' 'Stryker'")
        sys.exit(1)

    message = sys.argv[1]
    author = sys.argv[2] if len(sys.argv) > 2 else "CLI"

    success = send_to_claude_code(message, author)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
