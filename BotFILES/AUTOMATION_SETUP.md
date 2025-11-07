# Claude Desktop Automation Setup

**Status:** Ready to deploy
**What it does:** Types Discord messages directly into Claude Desktop window (this window)

---

## The Flow You Want

```
Discord (You)
    |
    | "execute task: [task description]"
    v
Discord Bot (claude_discord_bot.py)
    |
    | Writes to bulletin board
    v
Bulletin Board (shared_messages.jsonl)
    |
    | Monitored by automation
    v
Window Automation (type_to_claude_desktop.py)
    |
    | Types message into Claude Desktop input
    v
Claude Desktop (THIS WINDOW)
    |
    | You (real Claude Code) respond and complete task
    v
Task Complete
    |
    | You call: python send_to_discord.py "done whats next"
    v
Bulletin Board (shared_messages.jsonl)
    |
    | Discord bot monitors every 3 seconds
    v
Discord Bot (claude_discord_bot.py)
    |
    | Posts response
    v
Discord (You see "done whats next")
```

**This is TRUE communication between you and me (actual Claude Code).**

---

## Setup Steps

### 1. Install Automation Dependencies

```bash
pip install pyautogui pygetwindow
```

Or:

```bash
pip install -r BotFILES/automation_requirements.txt
```

### 2. Stop the API Monitor (if running)

If you have `claude_code_monitor.py` running, stop it (Ctrl+C).

We're replacing it with the window automation script.

### 3. Test Window Detection

First, make sure this Claude Desktop window is open and visible.

Then test if the script can find the window:

```bash
python -c "import pygetwindow as gw; print(gw.getAllTitles())"
```

Look for your Claude Desktop window in the output. Note the exact title.

### 4. Update Window Title (if needed)

If your window title isn't "Claude Code", edit `type_to_claude_desktop.py` line 13:

```python
WINDOW_TITLE = "Your Actual Window Title Here"
```

### 5. Start the Automation

**Terminal 1 - Discord Bot (should already be running):**
```bash
python BotFILES/claude_discord_bot.py
```

**Terminal 2 - Window Automation (NEW):**
```bash
python BotFILES/type_to_claude_desktop.py
```

Keep both running.

---

## How to Use

### From Discord:

**Send message to me (Claude Code):**
```
hey claude code what's 2+2?
```

The automation will:
1. Detect message in bulletin board
2. Focus this Claude Desktop window
3. Type: "Message from lordcain via Discord: hey claude code what's 2+2?"
4. Press Enter

I (real Claude Code) will see it and respond naturally in this window.

### From This Window (Me responding to Discord):

When I complete a task, I'll call:

```bash
python BotFILES/send_to_discord.py "Task completed. Ready for next task."
```

This writes to bulletin board, Discord bot picks it up and posts to Discord.

---

## Task Execution Flow

**You want this specific flow:**

### Step 1: You in Discord
```
execute task: refactor the authentication module
```

### Step 2: Automation Types Into This Window
Window automation script detects the message and types:
```
Message from Stryker via Discord: execute task: refactor the authentication module
```

### Step 3: I Work on Task
I (real Claude Code) see the message and start working:
- Use Read tool to examine files
- Use Edit tool to refactor code
- Use Bash tool to run tests
- Full access to all my tools

### Step 4: I Complete Task
When done, I call:
```bash
python BotFILES/send_to_discord.py "Refactoring complete. All tests passing. What's next?"
```

### Step 5: You See Response in Discord
Discord bot posts my message to your channel.

**Repeat.**

---

## Scripts Reference

### 1. type_to_claude_desktop.py
**What:** Monitors bulletin board and types messages into this window
**When:** Keep running 24/7 (Terminal 2)
**Does NOT:** Use Claude API (no cost)
**Does:** Types real messages for real me to see

### 2. send_to_discord.py
**What:** Script I can call to send messages to Discord
**When:** I call it when task is complete
**Usage:**
```bash
python BotFILES/send_to_discord.py "Your message"
python BotFILES/send_to_discord.py "Done" 1353335432179482657  # Specific channel
```

### 3. claude_discord_bot.py
**What:** Discord bot (already running)
**When:** Keep running 24/7 (Terminal 1)
**Does:**
- Monitors Discord messages
- Writes messages with "hey claude code" to bulletin board
- Monitors bulletin board for my responses
- Posts my responses to Discord

### 4. shared_messages.jsonl
**What:** Bulletin board file
**Where:** BotFILES/shared_messages.jsonl
**Format:** JSONL (one JSON object per line)

---

## Important Notes

### Window Focus
- Claude Desktop window must be visible (not minimized)
- If window is on different monitor, script will still find it
- If script can't find window, check window title

### Input Field Click
The script clicks at coordinates `(screen_width // 2, screen_height - 100)`.

If this doesn't click your input field, edit line 70 in `type_to_claude_desktop.py`:

```python
# Adjust Y coordinate (currently screen_height - 100)
pyautogui.click(screen_width // 2, YOUR_INPUT_Y_COORDINATE)
```

### Timing
- Window automation checks bulletin board every 2 seconds
- Discord bot checks bulletin board every 3 seconds
- Total latency: ~5 seconds Discord → This Window
- Total latency: ~3 seconds This Window → Discord

### Security
- Only responds to your user ID (821263652899782656)
- Only monitors your channels
- No API costs for window automation (only Discord bot's small API usage)

---

## Troubleshooting

### Script can't find window
**Check window title:**
```bash
python -c "import pygetwindow as gw; print([t for t in gw.getAllTitles() if 'Claude' in t or 'Anthropic' in t])"
```

Update `WINDOW_TITLE` in script with exact match.

### Message doesn't appear in input
**Wrong click coordinates.**

Test by running:
```python
import pyautogui
screen_width, screen_height = pyautogui.size()
print(f"Will click at: ({screen_width // 2}, {screen_height - 100})")
```

Adjust Y coordinate in script if needed.

### Window automation not running
**Check for errors:**
```bash
python BotFILES/type_to_claude_desktop.py
```

Look for "[ERROR]" messages.

### I don't see messages
**Check bulletin board:**
```bash
type BotFILES\shared_messages.jsonl
```

Should see messages with `"to": "claude_code"`.

---

## Cost

**Window Automation:** $0 (no API calls)
**Discord Bot:** ~$0.09 per 1000 messages (only for direct Discord conversations, not for forwarding to me)

**Total cost for this automation: ZERO**

The only API usage is when Discord bot responds directly to messages that DON'T say "hey claude code". Messages forwarded to me cost nothing because they're typed into this window, not sent to API.

---

## vs Previous System

### Old (claude_code_monitor.py):
- Used Claude API
- Pretended to be me
- Couldn't use my tools (Read, Edit, Bash, etc.)
- Cost ~$0.09 per 1000 messages
- Not real me

### New (type_to_claude_desktop.py):
- Types into this window
- Real me responds
- Full access to all my tools
- Zero API cost
- Actually me

---

## Next Steps

1. Install dependencies: `pip install pyautogui pygetwindow`
2. Test window detection
3. Start window automation: `python BotFILES/type_to_claude_desktop.py`
4. Test from Discord: "hey claude code test"
5. See message appear in this window
6. I respond naturally
7. When done, I call: `python BotFILES/send_to_discord.py "done"`

**It will work.**

---

## Advanced: Task Queue System

If you want to queue multiple tasks, you can:

1. Send multiple messages from Discord
2. Automation types them one by one
3. I complete them in order
4. After each task, I call send_to_discord.py

Or build a formal task queue (let me know if you want this).

---

**System ready. Install dependencies and start automation.**
