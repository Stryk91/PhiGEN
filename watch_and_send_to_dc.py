#!/usr/bin/env python3
"""
Windows File Watcher - Monitors trigger file and executes macro
Bridges Docker bot to Windows GUI automation
"""

import os
import time
import pyautogui
from pathlib import Path

# Configuration
TRIGGER_FILE = Path(__file__).parent / "dc_message_trigger.txt"
CHECK_INTERVAL = 0.5  # Check every 500ms

# Macro timing
RUN_DIALOG_DELAY = 0.5
WINDOW_INIT_DELAY = 7.5
TYPE_INTERVAL = 0.01
SEND_DELAY = 0.3

def execute_macro(message):
    """Execute the Win+R → DC(DESKC) macro with message"""
    try:
        print(f"[MACRO] Executing for message: {message[:50]}...")

        # Step 1: Win+R
        print("[MACRO] Opening Run dialog (Win+R)...")
        pyautogui.hotkey('win', 'r')
        time.sleep(RUN_DIALOG_DELAY)

        # Step 2: Type DC(DESKC)
        print("[MACRO] Typing DC(DESKC)...")
        pyautogui.typewrite('DC(DESKC)', interval=0.05)

        # Step 3: Enter
        print("[MACRO] Pressing Enter...")
        pyautogui.press('enter')

        # Step 4: Wait for window
        print(f"[MACRO] Waiting {WINDOW_INIT_DELAY}s for window...")
        time.sleep(WINDOW_INIT_DELAY)

        # Step 5: Type message
        print("[MACRO] Typing message...")
        pyautogui.write(message, interval=TYPE_INTERVAL)
        time.sleep(SEND_DELAY)

        # Step 6: Send
        print("[MACRO] Sending...")
        pyautogui.press('enter')

        print("[SUCCESS] Message sent to Claude Code!")
        return True

    except Exception as e:
        print(f"[ERROR] Macro failed: {e}")
        return False

def watch_trigger_file():
    """Monitor trigger file and execute macro when it changes"""
    print("="*60)
    print("Discord -> Claude Code Bridge (File Watcher)")
    print("="*60)
    print(f"Watching: {TRIGGER_FILE}")
    print(f"Check interval: {CHECK_INTERVAL}s")
    print("="*60)
    print("\nWaiting for trigger file...\n")

    last_modified = 0

    while True:
        try:
            # Check if file exists and has been modified
            if TRIGGER_FILE.exists():
                current_modified = TRIGGER_FILE.stat().st_mtime

                # File was modified since last check
                if current_modified > last_modified:
                    print(f"[TRIGGER] File detected at {time.strftime('%H:%M:%S')}")

                    # Read the message
                    with open(TRIGGER_FILE, 'r', encoding='utf-8') as f:
                        message = f.read().strip()

                    if message:
                        print(f"[MESSAGE] {message[:100]}")

                        # Execute the macro
                        execute_macro(message)

                        # Update last modified time
                        last_modified = current_modified

                        print("\n" + "="*60)
                        print("Waiting for next trigger...\n")

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n\n[STOP] File watcher stopped by user")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    watch_trigger_file()
