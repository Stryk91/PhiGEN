# Dynamic Custom Commands - AI Creates Commands for You! 🛠️

## Overview

Your Discord bot can now **create new commands on demand** using Granite's coding abilities. Just describe what you want, and Granite writes the Python code!

## How It Works

1. **You describe** what you want the command to do
2. **Granite writes** the Python function
3. **You approve** the generated code (shown to you first)
4. **Bot installs** it immediately - ready to use!

## Commands

### Create a Command
```
!create_command <name> <description>
```

**Examples:**
```
!create_command greet Send a friendly greeting to the user
!create_command joke Tell a random programming joke
!create_command roll Roll a dice from 1 to 6
!create_command quote Share an inspirational coding quote
!create_command time Show the current server time
!create_command flip Flip a coin (heads or tails)
!create_command wisdom Share programming wisdom
```

### List Custom Commands
```
!list_custom
```
Shows all commands you've created

### View Command Code
```
!view_command <name>
```
See the Python code that powers a custom command

### Remove a Command
```
!remove_command <name>
```
Delete a custom command

## Workflow Example

**You type:**
```
!create_command motivate Give me coding motivation
```

**Granite generates:**
```python
async def custom_motivate(self, ctx, *args):
    import random
    quotes = [
        "Code is poetry! 💻✨",
        "Every expert was once a beginner! 🚀",
        "The best way to predict the future is to code it! 💡",
        "Debugging is like being a detective! 🔍",
        "Your only limit is your imagination! 🌟"
    ]
    quote = random.choice(quotes)
    await ctx.send(f"💪 {quote}")
```

**Bot shows you the code and asks:**
> React with ✅ to approve or ❌ to cancel (30s)

**You approve:**
- Click ✅

**Bot responds:**
> ✅ Command `!motivate` installed! Try it now!

**You can now use it:**
```
!motivate
```

## Features

### ✅ Safe Execution
- You **review code before** it runs
- Restricted environment (no file access, no system calls)
- Only Discord-safe operations allowed

### 💾 Persistent
- Commands saved to `custom_commands.json`
- Auto-reload when bot restarts
- Commands survive bot updates

### 🎨 Creative Freedom
- Granite interprets your description
- Can use random choices, calculations, text formatting
- Discord embeds, mentions, and reactions all work

## Advanced Examples

### Random Number Game
```
!create_command lucky Pick a lucky number between 1 and 100
```

### User Info
```
!create_command whois Show info about the user who ran this command
```

### Math Helper
```
!create_command calc Calculate a simple math expression
```

### Countdown
```
!create_command countdown Count down from 5 to blast off
```

## Limitations

For security, custom commands **cannot**:
- Read/write files
- Execute system commands
- Access environment variables
- Import arbitrary modules
- Make network requests

But they **can**:
- Use `discord` module (embeds, reactions, etc.)
- Use `asyncio` for delays
- Access `ctx` (context: user, channel, server)
- Use Python built-ins (random, math, strings, etc.)

## Tips

### Be Specific
❌ Bad: `!create_command test do something`
✅ Good: `!create_command test Reply with 'Hello World!' in bold`

### Use Clear Descriptions
```
!create_command fact Share a random fun fact about Python programming
```

### Start Simple
Begin with basic commands, then get creative!

## Example Use Cases

### Server Management
```
!create_command rules Show server rules in a nice embed
!create_command welcome Welcome new members with a message
```

### Fun & Games
```
!create_command trivia Ask a random coding trivia question
!create_command challenge Give a coding challenge suggestion
!create_command praise Compliment the user who runs this
```

### Utilities
```
!create_command convert Convert celsius to fahrenheit
!create_command length Count characters in a message
```

## Troubleshooting

### Command not working?
```
!view_command <name>
```
Review the generated code for issues

### Want to fix it?
```
!remove_command <name>
!create_command <name> <better description>
```

### Timeout?
If you don't approve in 30 seconds, the command is not installed. Just run `!create_command` again.

## Current Status

**Model Status:**
- ✅ **Mistral 7B** - Ready
- ✅ **Granite Code 3B** - Ready (used for command creation)
- ✅ **Claude Sonnet 4.5** - Ready
- ⏳ **BakLLaVA** - Downloading (for future vision commands)

**Storage:**
- Commands saved to: `/app/ai_tools/custom_commands.json`
- Auto-loads on bot restart

## What's Next?

Once BakLLaVA finishes downloading, you'll be able to create commands that:
- Analyze images
- Read text from screenshots
- Describe uploaded pictures
- Identify objects in photos

Example future command:
```
!create_command analyze Take an uploaded image and describe what's in it
```

---

## Try It Now!

Head to your Discord server and try:

```
!create_command hello Reply with a friendly hello message
```

Approve the code Granite generates, then:

```
!hello
```

Your bot just became **self-modifying**! 🎉

---

**Pro Tip:** Use `!list_custom` to see all your custom creations and share them with your team!
