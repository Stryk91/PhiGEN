import sys
import traceback

try:
    from discord_webhook import DiscordWebhook
    print("discord_webhook imported successfully")
    
    WEBHOOK_URL = "https://discord.com/api/webhooks/1435814674242338847/gC1Lkq49pr8aOyxRnSRia8K-b5E7fLJqRMa8REAspOOjGUTzMgLVqRK-O8BhPiUXSIYu"
    
    message = "DC Test - If you see this, webhook works!"
    print(f"Attempting to send: {message}")
    
    webhook = DiscordWebhook(url=WEBHOOK_URL, content=f"[MCP] {message}")
    response = webhook.execute()
    
    print(f"Response status: {response.status_code}")
    print(f"Response text: {response.text if hasattr(response, 'text') else 'No text'}")
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    traceback.print_exc()
