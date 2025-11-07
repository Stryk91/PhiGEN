# Remote Command System - Discord to Claude Code 🖥️

## Overview

Your Discord bot can now **send messages directly to Claude Code's desktop window** using automation! This creates a two-way communication system between Discord and your desktop AI assistant.

## How It Works

### The Flow

```
Discord User → Discord Bot → Bulletin Board → Windows Automation → Claude Code Window
```

**Step by step:**

1. **You send a command in Discord:** `!send_to_dc Hello Claude Code!`
2. **Bot writes to bulletin board:** Queues message in `BotFILES/shared_messages.jsonl`
3. **Windows automation picks it up:** `type_to_claude_desktop.py` (running on Windows) monitors the bulletin board
4. **Message is typed:** Automation focuses Claude Code's window and types your message
5. **Claude Code receives it:** As if you typed it manually

## Prerequisites

### 1. Windows Automation Must Be Running

The `type_to_claude_desktop.py` script must be running on your Windows host:

```bash
# From Windows PowerShell or Command Prompt
cd E:\PythonProjects\PhiGEN
.\.venv\Scripts\python.exe BotFILES\type_to_claude_desktop.py
```

**What it does:**
- Monitors `BotFILES/shared_messages.jsonl` for new messages
- Uses `pyautogui` and `pygetwindow` to control windows
- Finds Claude Code's window and focuses it
- Types the message and presses Enter

### 2. Required Python Packages (Windows)

Make sure these are installed in your Windows Python environment:

```bash
pip install pyautogui pygetwindow
```

## Commands

### From Discord

```
!send_to_dc <your message>
```

**Examples:**
```
!send_to_dc Create a new Python function for user authentication
!send_to_dc Analyze the error logs in /var/log
!send_to_dc What's the status of the Docker containers?
!send_to_dc Review the latest changes in model_router.py
```

**Requirements:**
- You need **Manage Channels** permission
- Bot must be online and running

### From PowerShell (Alternative)

You can also send messages directly from PowerShell:

```powershell
.\send_to_dc.ps1 "Your message here"
```

**Example:**
```powershell
.\send_to_dc.ps1 "Fix the authentication bug in user_controller.py"
```

### From Python (Programmatic)

```python
from BotFILES.send_to_claude_code import send_to_claude_code

send_to_claude_code("Your message", author="Script Name")
```

## Setup Guide

### Complete Setup

**1. Start Windows Automation Monitor**

Open a PowerShell window and run:

```powershell
cd E:\PythonProjects\PhiGEN
.\.venv\Scripts\python.exe BotFILES\type_to_claude_desktop.py
```

You should see:
```
============================================================
Claude Desktop Window Automation Started
============================================================
Bulletin Board: E:\PythonProjects\PhiGEN\BotFILES\shared_messages.jsonl
Check Interval: 2 seconds
Target Window: Claude
============================================================

Monitoring bulletin board for messages...
```

**2. Keep This Window Open**

The automation script needs to keep running to process messages. You can:
- Leave the PowerShell window open
- Run it in the background
- Create a scheduled task to auto-start it

**3. Test from Discord**

In your Discord server:

```
!send_to_dc Test message - can you see this?
```

You should see:
- Discord bot confirms message was queued
- Windows automation window shows: "Processing message..."
- Claude Code's window gets focused
- Your message appears in Claude Code's input

### Creating a Startup Script

To automatically start the monitor when Windows boots:

**Option 1: Batch File**

Create `start_claude_monitor.bat`:

```batch
@echo off
cd E:\PythonProjects\PhiGEN
.\.venv\Scripts\python.exe BotFILES\type_to_claude_desktop.py
pause
```

Put this in your Windows Startup folder:
- Press `Win + R`
- Type: `shell:startup`
- Copy the batch file there

**Option 2: Windows Task Scheduler**

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: "At log on"
4. Action: Start a program
5. Program: `E:\PythonProjects\PhiGEN\.venv\Scripts\python.exe`
6. Arguments: `BotFILES\type_to_claude_desktop.py`
7. Start in: `E:\PythonProjects\PhiGEN`

## How Messages Are Queued

### Bulletin Board Format

Messages are stored in `BotFILES/shared_messages.jsonl` (JSONL = JSON Lines):

```json
{
  "timestamp": "2025-11-07T12:30:00.000000",
  "target": "claude_code",
  "author": "Stryker (Discord)",
  "message": "Your message here",
  "processed": false
}
```

**Fields:**
- `timestamp` - When the message was queued
- `target` - Where to send it (`claude_code`)
- `author` - Who sent it
- `message` - The actual message text
- `processed` - Whether automation has handled it yet

### How Automation Processes Messages

The `type_to_claude_desktop.py` script:

1. **Reads bulletin board** every 2 seconds
2. **Finds unprocessed messages** with `target: "claude_code"`
3. **For each message:**
   - Focuses Claude Code's window
   - Clicks in the input area
   - Types: `"Message from [author] via Discord: [message]"`
   - Presses Enter
   - Marks as processed

## Troubleshooting

### "Message queued" but nothing happens

**Check if automation is running:**

```powershell
# List Python processes
Get-Process python
```

You should see `type_to_claude_desktop.py` running.

**Start it if not running:**

```powershell
cd E:\PythonProjects\PhiGEN
.\.venv\Scripts\python.exe BotFILES\type_to_claude_desktop.py
```

### Claude Code window not being found

**Check window title:**

The script looks for windows with "Claude" in the title. If your window has a different title:

1. Open `BotFILES/type_to_claude_desktop.py`
2. Change line 15:
   ```python
   WINDOW_TITLE = "Your Actual Window Title"
   ```

**Find the correct window title:**

```powershell
# PowerShell - list all window titles
Get-Process | Where-Object {$_.MainWindowTitle} | Select-Object MainWindowTitle
```

### Message appears but gets cut off

**Adjust typing speed:**

In `type_to_claude_desktop.py`, line 77:

```python
pyautogui.write(formatted_msg, interval=0.01)  # Increase interval for slower typing
```

Change `0.01` to `0.05` for slower, more reliable typing.

### Wrong window gets focused

**Adjust click coordinates:**

In `type_to_claude_desktop.py`, lines 72-73:

```python
pyautogui.click(screen_width // 2, screen_height - 100)
```

Change `-100` to adjust where the script clicks (e.g., `-150` for higher up).

## Advanced Usage

### Sending Commands from Scripts

Create automated workflows:

```python
# automation_script.py
from BotFILES.send_to_claude_code import send_to_claude_code

# Daily tasks
tasks = [
    "Review system logs from the last 24 hours",
    "Check Docker container health",
    "Analyze recent error patterns"
]

for task in tasks:
    send_to_claude_code(task, author="Daily Automation")
```

### Queuing Multiple Messages

```powershell
# Send a series of related tasks
.\send_to_dc.ps1 "First, analyze the user authentication flow"
Start-Sleep -Seconds 5
.\send_to_dc.ps1 "Then, suggest security improvements"
Start-Sleep -Seconds 5
.\send_to_dc.ps1 "Finally, create a implementation plan"
```

### Integration with Other Bots

The bulletin board system is universal - any script can write to it:

```python
import json
from datetime import datetime
from pathlib import Path

def queue_message_for_claude(msg):
    bulletin = Path("BotFILES/shared_messages.jsonl")

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "target": "claude_code",
        "author": "Your Bot Name",
        "message": msg,
        "processed": False
    }

    with open(bulletin, 'a') as f:
        f.write(json.dumps(entry) + '\n')
```

## Use Cases

### 1. Remote Development Assistance

From your phone via Discord:
```
!send_to_dc Review the authentication logic in user_service.py
!send_to_dc Optimize the database queries in reports.py
!send_to_dc Create unit tests for the payment module
```

### 2. Automated Task Delegation

From automation scripts:
```python
# Daily morning routine
send_to_claude_code("Generate a summary of overnight system logs")
send_to_claude_code("List any failed CI/CD builds")
send_to_claude_code("Review security alerts from the last 12 hours")
```

### 3. Team Collaboration

Team members with Discord access can request code reviews:
```
!send_to_dc Can you review the PR for feature/user-authentication?
!send_to_dc Check if the API changes are backward compatible
```

### 4. Server Monitoring Integration

Integrate with monitoring tools:
```python
# When server alert triggers
if cpu_usage > 90:
    send_to_claude_code(f"HIGH CPU ALERT: {cpu_usage}% - investigate and suggest optimizations")
```

## Security Notes

### Permissions

The `!send_to_dc` command requires **Manage Channels** permission to prevent abuse.

### Message Logging

All messages sent via this system are logged in:
- `BotFILES/shared_messages.jsonl` - Full message queue
- Discord bot logs - Command execution
- Claude Code conversation history - The actual exchanges

### Window Control

The automation has the ability to:
- ✅ Focus windows
- ✅ Type text
- ✅ Press keyboard shortcuts
- ❌ Cannot read screen content
- ❌ Cannot access files outside the project
- ❌ Cannot execute arbitrary system commands

## Files Created

| File | Purpose |
|------|---------|
| `BotFILES/send_to_claude_code.py` | Python module for queuing messages |
| `send_to_dc.ps1` | PowerShell script for command-line usage |
| `BotFILES/type_to_claude_desktop.py` | Existing Windows automation (monitors queue) |
| `BotFILES/shared_messages.jsonl` | Message queue (bulletin board) |

## Next Steps

1. **Start the monitor:** Run `type_to_claude_desktop.py` on Windows
2. **Test the system:** Use `!send_to_dc Test message` in Discord
3. **Watch it work:** See your message appear in Claude Code's window
4. **Automate tasks:** Create workflows that leverage this integration

---

**You now have a complete two-way communication system between Discord and Claude Code!** 🚀

Use `!send_to_dc` from anywhere you have Discord access to interact with your desktop AI assistant.
