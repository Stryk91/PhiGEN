#!/usr/bin/env python3
"""Test Claude API connection"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('ANTHROPIC_API_KEY')

if not API_KEY:
    print("ERROR: ANTHROPIC_API_KEY not found in .env")
    exit(1)

print("Testing Claude API connection...")
print(f"API Key: {API_KEY[:20]}...")

try:
    client = anthropic.Anthropic(api_key=API_KEY)

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=100,
        messages=[
            {"role": "user", "content": "Say 'API test successful' and nothing else."}
        ]
    )

    response_text = response.content[0].text
    print(f"\nClaude Response: {response_text}")
    print("\nSUCCESS: Claude API is working!")

except anthropic.APIError as e:
    print(f"\nERROR: API Error - {e}")
    exit(1)
except Exception as e:
    print(f"\nERROR: {e}")
    exit(1)
