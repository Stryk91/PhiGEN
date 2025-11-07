#!/usr/bin/env python3
"""Quick script to send a Discord message"""
import os
import sys
from discord_webhook import DiscordWebhook

# Get message from command line or use default
message = sys.argv[1] if len(sys.argv) > 1 else "Build complete!"

# Discord webhook URL (from git hooks)
WEBHOOK_URL = "https://discord.com/api/webhooks/1435814674242338847/gC1Lkq49pr8aOyxRnSRia8K-b5E7fLJqRMa8REAspOOjGUTzMgLVqRK-O8BhPiUXSIYu"

# Send the message
webhook = DiscordWebhook(url=WEBHOOK_URL, content=f"[MCP] {message}")
response = webhook.execute()

if response.status_code == 200 or response.status_code == 204:
    print(f"Message sent: {message}")
else:
    print(f"Failed with status: {response.status_code}")
