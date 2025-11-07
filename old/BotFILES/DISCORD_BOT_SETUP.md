# PhiGEN Desktop Discord Bot - Setup Guide

## ✅ What You Have Ready:
- Discord bot token: Configured ✅
- Channel ID: Configured ✅
- Bot permissions: Need to enable

## 🔧 Quick Setup (3 Steps)

### Step 1: Enable Bot Intents

Go to your Discord Developer Portal → Your Bot → Bot Settings → Privileged Gateway Intents:

**Enable These:**
- ✅ **Message Content Intent** (CRITICAL!)
- ✅ **Server Members Intent** (Optional but helpful)

Click **Save Changes**

### Step 2: Install Dependencies

Open PowerShell or Command Prompt on your desktop:

```bash
pip install discord.py
```

Or use the requirements.txt:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Bot

Navigate to where you saved `phigen_discord_bot.py` and run:

```bash
python phigen_discord_bot.py
```

You should see:
```
🚀 Starting PhiGEN Desktop Bot...
📡 Listening on channel: 1353335432179482657
✅ Bot logged in as YourBotName
✅ Connected to 1 server(s)
```

**The bot will post a startup message in your Discord channel!**

---

## 🎮 Available Commands

### Agent Feed Commands
- `!check_jc` or `!jc` - Check JC's latest status
- `!feed [count]` - Show recent activity (default: 5 entries)
  - Example: `!feed 10` - Show last 10 entries

### File Operations
- `!read <path>` - Read a file from your desktop
  - Example: `!read E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl`
- `!list <path>` - List directory contents
  - Example: `!list E:\PythonProjects\PhiGEN`

### System Commands
- `!run <command>` - Execute any Windows shell command
  - Example: `!run dir E:\PythonProjects`
  - Example: `!run python --version`
- `!ping` - Test bot responsiveness

### Help
- `!help_commands` - Show all commands

---

## 📱 Using From Your Phone

1. Open Discord mobile app
2. Navigate to your private server
3. Go to the channel (ID: 1353335432179482657)
4. Type commands like:
   - `!check_jc`
   - `!feed`
   - `!run dir`

The bot will execute on your desktop and respond in Discord!

---

## 🔒 Security Notes

**Your token is embedded in the bot file.** Keep it secure:
- ✅ Bot only listens to one specific channel
- ✅ Only you have access to your private Discord server
- ⚠️ Don't share the bot file or token with anyone
- ⚠️ Don't commit it to public repositories

If you ever need to rotate the token:
1. Go to Discord Developer Portal
2. Bot Settings → Reset Token
3. Update the `TOKEN` variable in the bot file

---

## 🐛 Troubleshooting

**Bot doesn't connect:**
- Check your internet connection
- Verify the token is correct
- Make sure you enabled Message Content Intent

**Bot doesn't respond to commands:**
- Verify Message Content Intent is enabled
- Check you're in the right channel (ID: 1353335432179482657)
- Make sure bot has permissions to read/send messages

**Bot can't read files:**
- Verify the file paths are correct (use full paths with `E:\...`)
- Windows paths need double backslashes `\\` or raw strings `r'E:\...'`

**"Command not found" error:**
- Use `!help_commands` to see all available commands
- Make sure to include the `!` prefix

---

## 🚀 Next Steps

Once the bot is running:

1. **Test basic functionality:**
   ```
   !ping
   !help_commands
   ```

2. **Check JC's status:**
   ```
   !check_jc
   ```

3. **View agent feed:**
   ```
   !feed 5
   ```

4. **From your phone, you can now:**
   - Monitor JC's progress
   - Read files
   - Execute commands
   - All while away from your desktop!

---

## 💡 Pro Tips

**Keep bot running in background:**
```bash
# Windows - keep console open
start python phigen_discord_bot.py

# Or use pythonw (no console window)
pythonw phigen_discord_bot.py
```

**Auto-start on boot:**
1. Create a `.bat` file:
   ```batch
   @echo off
   cd E:\PythonProjects\PhiGEN
   python phigen_discord_bot.py
   ```
2. Place in `shell:startup` folder

**Monitor bot logs:**
The bot prints activity to console, so keep an eye on it for errors.

---

## ✨ You're All Set!

Your desktop is now remotely controllable from your phone via Discord! 

Test it out:
1. Start the bot on your desktop
2. Open Discord on your phone
3. Type `!check_jc` in your channel
4. Watch the magic happen! ✨
