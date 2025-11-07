# Docker to Windows GUI Bridge

## How It Works

Since the Discord bot runs in a **Linux Docker container** and can't directly control Windows GUI, we use a **file-based bridge**:

```
┌─────────────────────────────────────────────────────────┐
│  Discord (Anywhere) → Bot (Docker/Linux) → Windows GUI  │
└─────────────────────────────────────────────────────────┘

Step 1: User types in Discord
  !send_to_dc Test message

Step 2: Bot (in Linux container) writes to shared file
  /app/dc_message_trigger.txt
  ↓ (shared volume)
  E:\PythonProjects\PhiGEN\dc_message_trigger.txt

Step 3: Windows script watches the file
  watch_and_send_to_dc.py (running on Windows)
  Detects file changed!

Step 4: Windows script executes macro
  Win+R → DC(DESKC) → Type message → Send

Step 5: Claude Code receives message
  ✅ Done!
```

## Setup (2 Steps)

### Step 1: Start the Windows Bridge

Double-click: `start_dc_bridge.bat`

Or run:
```bash
python watch_and_send_to_dc.py
```

**Keep this window open!** It watches for Discord messages.

### Step 2: Use from Discord

```
!send_to_dc Test message to Claude Code!
```

## What You'll See

**In Discord:**
```
📤 Sending to Claude Code
From: YourName
Message: Test message to Claude Code!
Windows script will execute: Win+R → DC(DESKC) → Type message → Send
```

**In Bridge Window (Windows):**
```
[TRIGGER] File detected at 23:45:12
[MESSAGE] Message from YourName via Discord: Test message to Claude Code!
[MACRO] Opening Run dialog (Win+R)...
[MACRO] Typing DC(DESKC)...
[MACRO] Pressing Enter...
[MACRO] Waiting 7.5s for window...
[MACRO] Typing message...
[MACRO] Sending...
[SUCCESS] ✅ Message sent to Claude Code!
```

**In Claude Code:**
Your message appears in the input field and gets sent!

## Why This Approach?

### ❌ What Doesn't Work

**Direct execution from Docker:**
```python
subprocess.Popen(["cmd.exe", ...])  # ❌ No cmd.exe in Linux
```

**Linux GUI automation:**
```python
pyautogui.hotkey('win', 'r')  # ❌ No Windows in Linux container
```

### ✅ What Works

**Shared file bridge:**
```
Docker writes file → Windows watches file → Windows executes macro
```

This is the **standard pattern** for Docker-to-Host GUI automation.

## Files Created

| File | Purpose | Runs On |
|------|---------|---------|
| `dc_message_trigger.txt` | Trigger file (written by bot) | Shared |
| `watch_and_send_to_dc.py` | File watcher + macro executor | Windows |
| `start_dc_bridge.bat` | Easy launcher | Windows |

## Modified Files

| File | Change |
|------|--------|
| `ai_tools/discord_multimodel_bot.py` | `!send_to_dc` now writes to file instead of executing |

## Advantages

✅ **Works across Docker boundary** - No container escape needed
✅ **Simple** - Just write/read a text file
✅ **Fast** - 500ms polling, near-instant response
✅ **Reliable** - File operations are atomic
✅ **Debuggable** - Can see trigger file contents

## Troubleshooting

### "Message sent" in Discord but nothing happens

**Problem:** Bridge script not running

**Solution:** Start it!
```bash
start_dc_bridge.bat
```

### Bridge script shows errors

**Problem:** pyautogui or pygetwindow not installed

**Solution:**
```bash
pip install pyautogui pygetwindow
```

### Messages delayed

**Problem:** File polling interval too slow

**Solution:** Edit `watch_and_send_to_dc.py`:
```python
CHECK_INTERVAL = 0.2  # Faster (200ms)
```

## Technical Details

### Why Files?

Docker containers are **isolated** from the host OS by design. They have:
- ❌ No access to Windows GUI
- ❌ No Windows keyboard/mouse control
- ❌ Different process space
- ✅ But CAN access shared volumes (files)

### The Shared Volume

In `docker-compose.yml`:
```yaml
volumes:
  - .:/app  # Current dir → /app in container
```

This means:
- `E:\PythonProjects\PhiGEN` (Windows)
- = `/app` (Docker container)
- Files written by bot appear on Windows instantly!

### File Watching Pattern

```python
last_modified = 0

while True:
    current_modified = file.stat().st_mtime

    if current_modified > last_modified:
        # File changed! Process it
        execute_macro(read_file())
        last_modified = current_modified

    sleep(0.5)
```

## Container Learning Resources

Want to learn more about Docker?

- **Docker isolation:** Containers can't access host GUI
- **Shared volumes:** How files bridge the gap
- **Container networking:** How containers talk to each other
- **Process namespaces:** Why containers are separate
- **Docker Desktop:** How it bridges Linux containers on Windows

---

**The bridge is ready!** Start `start_dc_bridge.bat` and test with `!send_to_dc`
