# Quick Start: Discord → Claude Code Remote Commands

## 3-Step Setup

### Step 1: Start Windows Monitor

Double-click: `BotFILES\start_claude_monitor.bat`

Or run in PowerShell:
```powershell
cd E:\PythonProjects\PhiGEN
.\.venv\Scripts\python.exe BotFILES\type_to_claude_desktop.py
```

**Keep this window open!**

### Step 2: Test from Discord

In your Discord channel:
```
!send_to_dc Hello Claude Code, can you see this?
```

### Step 3: Watch the Magic

- Discord bot confirms: "Message Queued for Claude Code"
- Monitor window shows: "Processing message from..."
- Claude Code's window opens and receives your message

## That's It!

You can now send commands to Claude Code from:
- 📱 Discord (from anywhere)
- 💻 PowerShell: `.\send_to_dc.ps1 "message"`
- 🐍 Python: `send_to_claude_code("message")`

## Common Commands

```
!send_to_dc Review the latest code changes
!send_to_dc Check Docker container status
!send_to_dc Analyze error logs from today
!send_to_dc Create a function for user authentication
!send_to_dc Help me debug the payment module
```

## Troubleshooting

**Nothing happens?**
- Make sure `start_claude_monitor.bat` is running
- Check Claude Code window is open
- Look for errors in the monitor window

**Wrong window focused?**
- Open `BotFILES/type_to_claude_desktop.py`
- Edit `WINDOW_TITLE = "Claude"` to match your window

## Files

- `!send_to_dc` - Discord bot command (already added)
- `send_to_dc.ps1` - PowerShell script
- `BotFILES/send_to_claude_code.py` - Python module
- `BotFILES/type_to_claude_desktop.py` - Windows monitor (existing)
- `BotFILES/start_claude_monitor.bat` - Easy startup script

---

**Full documentation:** See `REMOTE_COMMAND_GUIDE.md`
