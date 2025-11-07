#!/usr/bin/env python3
"""
Test the Claude Desktop macro sequence
Verifies Win+R -> DC(DESKC) -> Message input works correctly
"""

import time
import pyautogui

# Configuration
RUN_DIALOG_DELAY = 0.5      # Wait after Win+R (500ms)
WINDOW_INIT_DELAY = 7.5     # Wait for Claude Desktop to initialize (7500ms)

def test_macro():
    """Test the complete macro sequence"""
    print("="*60)
    print("Testing Claude Desktop Macro Sequence")
    print("="*60)
    print()
    print("This will:")
    print("  1. Open Run dialog (Win+R)")
    print("  2. Type 'DC(DESKC)'")
    print("  3. Press Enter")
    print("  4. Wait for window to initialize")
    print("  5. Type a test message")
    print("  6. Send the message")
    print()
    print("Starting in 3 seconds... (Press Ctrl+C to cancel)")
    print()

    try:
        time.sleep(3)

        # Step 1: Open Run dialog
        print("[1/6] Opening Run dialog (Win+R)...")
        pyautogui.hotkey('win', 'r')
        time.sleep(RUN_DIALOG_DELAY)

        # Step 2: Type DC(DESKC) command
        print("[2/6] Typing DC(DESKC)...")
        pyautogui.typewrite('DC(DESKC)', interval=0.05)

        # Step 3: Press Enter
        print("[3/6] Pressing Enter...")
        pyautogui.press('enter')

        # Step 4: Wait for initialization
        print(f"[4/6] Waiting {WINDOW_INIT_DELAY}s for window initialization...")
        for i in range(int(WINDOW_INIT_DELAY)):
            print(f"      {i+1}/{int(WINDOW_INIT_DELAY)}...", end='\r')
            time.sleep(1)
        print()

        # Step 5: Type test message
        test_message = "Test message from macro - If you see this, the automation is working!"
        print(f"[5/6] Typing test message...")
        pyautogui.write(test_message, interval=0.01)
        time.sleep(0.3)

        # Step 6: Send message
        print("[6/6] Pressing Enter to send...")
        pyautogui.press('enter')

        print()
        print("="*60)
        print("✅ Macro test complete!")
        print("="*60)
        print()
        print("Check Claude Desktop window - you should see the test message.")
        print()

    except KeyboardInterrupt:
        print()
        print("❌ Test cancelled by user")
    except Exception as e:
        print()
        print(f"❌ Error during test: {e}")

if __name__ == "__main__":
    test_macro()
