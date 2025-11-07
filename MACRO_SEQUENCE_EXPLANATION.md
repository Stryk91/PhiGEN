# Claude Desktop Macro Sequence Explained

## The Macro Flow

Your automation now uses a **reliable macro sequence** to send messages to Claude Code's desktop window:

```
┌─────────────────────────────────────────────────────────────┐
│  MACRO SEQUENCE: Discord → Claude Code Desktop              │
└─────────────────────────────────────────────────────────────┘

Step 1: Win + R                  [Opens Windows Run Dialog]
         ↓
    Wait 500ms                    [Let dialog appear]
         ↓
Step 2: Type "DC(DESKC)"         [Desktop Claude shortcut]
         ↓
Step 3: Press Enter              [Execute command]
         ↓
    Wait 7500ms (7.5s)           [Window initialization]
         ↓
Step 4: Type Message             [Your variable message]
         ↓
    Wait 300ms                    [Let typing finish]
         ↓
Step 5: Press Enter              [Send message]
         ↓
       DONE! ✅                    [Message delivered]
```

## Why This Approach?

### Previous Method (Window Title Search)
❌ **Unreliable** - Window titles can change
❌ **Slow** - Has to search through all windows
❌ **Error-prone** - May find wrong window

### New Method (Win+R Macro)
✅ **Reliable** - Uses system shortcut
✅ **Fast** - Direct command execution
✅ **Consistent** - Same behavior every time
✅ **Universal** - Works regardless of window state

## The Keyboard Shortcuts

### QMK Notation (Your Original)
```
{KC_LGUI, KC_R}      → Left Windows key + R
DC(DESKC)            → Types "DC(DESKC)"
```

### Python Implementation
```python
pyautogui.hotkey('win', 'r')           # Win+R
pyautogui.typewrite('DC(DESKC)')       # Type command
pyautogui.press('enter')               # Execute
pyautogui.write(your_message)          # Type variable message
pyautogui.press('enter')               # Send
```

## Timing Breakdown

| Step | Action | Delay | Reason |
|------|--------|-------|--------|
| 1 | Press Win+R | - | Opens Run dialog |
| 2 | Wait | 500ms | Let dialog appear |
| 3 | Type "DC(DESKC)" | - | Focus command |
| 4 | Press Enter | - | Execute command |
| 5 | Wait | 7500ms | Window initialization |
| 6 | Type message | variable | Your text |
| 7 | Wait | 300ms | Typing complete |
| 8 | Press Enter | - | Send message |

**Total Time:** ~8.3 seconds + message length

## Configuration Variables

Located at the top of `type_to_claude_desktop.py`:

```python
RUN_DIALOG_DELAY = 0.5      # Wait after Win+R (500ms)
WINDOW_INIT_DELAY = 7.5     # Wait for Claude Desktop (7500ms)
TYPE_INTERVAL = 0.01        # Delay between keystrokes (10ms)
SEND_DELAY = 0.3            # Wait before Enter (300ms)
```

### Adjusting Timing

**If the window doesn't initialize in time:**
```python
WINDOW_INIT_DELAY = 10.0    # Increase to 10 seconds
```

**If typing is too fast (characters get skipped):**
```python
TYPE_INTERVAL = 0.05        # Slow down to 50ms per character
```

**If Run dialog is slow to appear:**
```python
RUN_DIALOG_DELAY = 1.0      # Increase to 1 second
```

## Message Variable

The `message_text` parameter is your **variable** - it can be any text:

```python
def type_message_to_claude(message_text, author):
    # message_text is the variable - can be:
    # - "Help me debug this code"
    # - "What's the weather?"
    # - "Analyze error logs"
    # - Anything you want!

    formatted_msg = f"Message from {author} via Discord: {message_text}"
    pyautogui.write(formatted_msg, interval=TYPE_INTERVAL)
```

## Testing the Macro

### Quick Test
```bash
# Run the test script
test_macro.bat
```

or

```bash
python BotFILES\test_claude_macro.py
```

### What You'll See

**In the console:**
```
[1/6] Opening Run dialog (Win+R)...
[2/6] Typing DC(DESKC)...
[3/6] Pressing Enter...
[4/6] Waiting 7.5s for window initialization...
[5/6] Typing test message...
[6/6] Pressing Enter to send...
✅ Macro test complete!
```

**On your screen:**
1. Run dialog appears briefly
2. Types "DC(DESKC)"
3. Claude Desktop window opens/focuses
4. Test message appears in input field
5. Message gets sent

## Troubleshooting

### "DC(DESKC)" doesn't focus Claude Desktop

**Problem:** The shortcut isn't configured in Windows

**Solution:** Create a Windows shortcut:
1. Right-click Claude Desktop shortcut
2. Properties → Shortcut key
3. Set to: `Ctrl + Alt + D` (or any key combo)
4. Or create a shortcut named "DC(DESKC)" in a PATH location

**Alternative:** Modify `type_to_claude_desktop.py` line 64:
```python
# Instead of 'DC(DESKC)', use your actual shortcut
pyautogui.typewrite('C:\\Path\\To\\Claude.exe', interval=0.05)
```

### Macro is too slow

**Problem:** 7.5 second wait is too long

**Solution:** Reduce `WINDOW_INIT_DELAY`:
```python
WINDOW_INIT_DELAY = 5.0  # Try 5 seconds
```

### Characters are missing from message

**Problem:** Typing too fast

**Solution:** Increase `TYPE_INTERVAL`:
```python
TYPE_INTERVAL = 0.05  # Slow down to 50ms per char
```

### Wrong window gets focus

**Problem:** Run dialog goes to wrong app

**Solution:** Close other apps or modify the DC(DESKC) command to use full path

## Real-World Usage

### From Discord
```
!send_to_dc Review the authentication code in auth.py
```

**What happens:**
1. Bot writes to bulletin board: `shared_messages.jsonl`
2. Monitor detects new message
3. Macro executes:
   - Win+R → "DC(DESKC)" → Enter
   - Wait 7.5s
   - Type: "Message from Stryker via Discord: Review the authentication code in auth.py"
   - Press Enter
4. Claude Code receives and processes your request

### From PowerShell
```powershell
.\send_to_dc.ps1 "Create unit tests for payment module"
```

Same flow as above, but initiated from PowerShell instead of Discord.

### From Python
```python
from BotFILES.send_to_claude_code import send_to_claude_code

send_to_claude_code("Analyze recent error logs", author="Automation Script")
```

Queue multiple messages programmatically.

## Files Modified

| File | What Changed |
|------|-------------|
| `BotFILES/type_to_claude_desktop.py` | Complete rewrite with macro sequence |
| `BotFILES/test_claude_macro.py` | **NEW** - Test the macro |
| `test_macro.bat` | **NEW** - Easy test launcher |

## Next Steps

1. **Test the macro:** Run `test_macro.bat`
2. **Verify it works:** Check Claude Desktop receives the test message
3. **Adjust timing if needed:** Edit the delay variables
4. **Start monitoring:** Run `start_claude_monitor.bat`
5. **Send from Discord:** Use `!send_to_dc Your message`

---

**The macro is now exactly as you specified:** Win+R → DC(DESKC) → Wait → Type variable → Send! 🚀
