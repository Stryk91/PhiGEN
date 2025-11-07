#!/usr/bin/env python3
"""
Types messages from bulletin board into Claude Desktop window
Replaces the API-based monitor with direct window automation
"""

import os
import json
import time
import pyautogui
from datetime import datetime, timezone

SHARED_BOARD = os.path.join(os.path.dirname(__file__), "shared_messages.jsonl")
CHECK_INTERVAL = 2  # seconds

# Macro timing configuration (in seconds)
RUN_DIALOG_DELAY = 0.5      # Wait after Win+R (500ms)
WINDOW_INIT_DELAY = 7.5     # Wait for Claude Desktop to initialize (7500ms)
TYPE_INTERVAL = 0.01        # Delay between keystrokes (10ms)
SEND_DELAY = 0.3            # Wait before pressing Enter (300ms)

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

def focus_claude_desktop_via_run():
    """
    Focus Claude Desktop window using Windows Run dialog macro

    Sequence:
    1. Win+R (open Run dialog)
    2. Wait 500ms
    3. Type "DC(DESKC)" (Desktop Claude shortcut)
    4. Press Enter
    5. Wait 7500ms (for window initialization)
    """
    try:
        # Step 1: Press Windows Key + R to open Run dialog
        print("[DEBUG] Opening Run dialog (Win+R)...")
        pyautogui.hotkey('win', 'r')

        # Step 2: Wait for Run dialog to appear
        time.sleep(RUN_DIALOG_DELAY)

        # Step 3: Type the Desktop Claude shortcut
        print("[DEBUG] Typing DC(DESKC) command...")
        pyautogui.typewrite('DC(DESKC)', interval=0.05)

        # Step 4: Press Enter to execute
        print("[DEBUG] Pressing Enter to execute...")
        pyautogui.press('enter')

        # Step 5: Wait for Claude Desktop window to initialize
        print(f"[DEBUG] Waiting for window initialization ({WINDOW_INIT_DELAY}s)...")
        time.sleep(WINDOW_INIT_DELAY)

        print("[DEBUG] Claude Desktop window should now be focused")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to focus Claude Desktop: {e}")
        return False

def type_message_to_claude(message_text, author):
    """
    Type message into Claude Desktop input field using macro

    Args:
        message_text: The message to send (variable)
        author: Who is sending the message

    Returns:
        True if successful, False otherwise
    """
    try:
        # Focus window using Win+R macro sequence
        if not focus_claude_desktop_via_run():
            return False

        # Format message with context
        formatted_msg = f"Message from {author} via Discord: {message_text}"

        print(f"[DEBUG] Typing message: {formatted_msg[:50]}...")

        # Type the message (this is the variable part)
        # Using write() which handles special characters better
        pyautogui.write(formatted_msg, interval=TYPE_INTERVAL)
        time.sleep(SEND_DELAY)

        # Press Enter to send
        print("[DEBUG] Pressing Enter to send message...")
        pyautogui.press('enter')

        print("[SUCCESS] Message sent successfully!")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to type message: {e}")
        return False

def monitor_loop():
    """Main monitoring loop"""
    print("="*60)
    print("Claude Desktop Window Automation Started")
    print("="*60)
    print(f"Bulletin Board: {SHARED_BOARD}")
    print(f"Check Interval: {CHECK_INTERVAL} seconds")
    print(f"Focus Method: Win+R -> DC(DESKC)")
    print(f"Init Delay: {WINDOW_INIT_DELAY}s")
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
                        message_text = msg.get('message', '')
                        author = msg.get('author', 'Unknown')

                        print(f"[{datetime.now().strftime('%H:%M:%S')}] New message from {author}")
                        print(f"  Content: {message_text[:50]}...")

                        # Type into Claude Desktop
                        if type_message_to_claude(message_text, author):
                            print(f"  Typed into Claude Desktop window")
                            processed.add(msg_id)
                        else:
                            print(f"  Failed to type into window, will retry")

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n\nMonitor stopped by user.")
            break
        except Exception as e:
            print(f"[ERROR] Monitor loop error: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    monitor_loop()
