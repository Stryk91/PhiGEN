# Anthropic API Cost Optimization Guide

## Current Bot Configuration

**Model:** Claude 3 Haiku (cheapest available)
- Input: $0.25 per million tokens
- Output: $1.25 per million tokens

**Settings in Bot:**
- ✅ max_tokens: 150 (minimal)
- ✅ System prompt: Forces terse responses
- ✅ Conversation history: Limited to 20 messages (10 exchanges)

**Estimated Cost Per Message:**
- Input: ~100 tokens = $0.000025
- Output: ~50 tokens = $0.000063
- **Total: ~$0.00009 per message (~$0.09 per 1000 messages)**

---

## Anthropic Console Settings

### 1. API Key Management (console.anthropic.com)

**Set Monthly Spending Limit:**
1. Go to https://console.anthropic.com/settings/limits
2. Click "Set Limit"
3. Recommended: **$5-$10/month** for moderate use
4. This will hard-stop API calls when limit reached

**Enable Alerts:**
1. Settings → Notifications
2. Enable "Budget Alert" at 50%, 75%, 90%
3. Get emails before hitting limit

---

## Code-Level Optimizations (Already Implemented)

### ✅ 1. Use Cheapest Model
```python
model="claude-3-haiku-20240307"  # $0.25 input, $1.25 output
# NOT claude-3-opus (100x more expensive)
# NOT claude-3-sonnet (10x more expensive)
```

### ✅ 2. Minimal Token Limit
```python
max_tokens=150  # Reduced from 1024
# Saves 85% on output tokens
```

### ✅ 3. Terse System Prompt
```python
system="You are a terse assistant. Answer in 1-2 sentences MAX. Be extremely brief."
# Forces short responses = fewer tokens
```

### ✅ 4. Limited Conversation History
```python
if len(conversation_history) > 20:
    conversation_history.pop(0)
    conversation_history.pop(0)
# Keeps context small = fewer input tokens
```

---

## Additional Optimizations You Can Add

### Option 1: Disable History Entirely (Cheapest)

Edit `claude_discord_bot.py`:

```python
# BEFORE sending to API, clear history:
conversation_history = [{"role": "user", "content": message.content}]
```

**Savings:**
- No context sent = minimal input tokens
- Each message is standalone
- **~50% reduction in input costs**

**Trade-off:**
- Claude won't remember previous messages
- No conversation context

---

### Option 2: Rate Limiting

Add to bot:

```python
import time
from collections import defaultdict

user_last_message = defaultdict(float)
COOLDOWN = 5  # seconds between messages

@bot.event
async def on_message(message):
    user_id = message.author.id
    now = time.time()

    if now - user_last_message[user_id] < COOLDOWN:
        await message.channel.send("Please wait 5 seconds between messages.")
        return

    user_last_message[user_id] = now
    # ... rest of code
```

**Savings:**
- Prevents rapid-fire API calls
- Protects against accidental spam

---

### Option 3: Command Prefix Required

Make users type a prefix to trigger Claude:

```python
@bot.event
async def on_message(message):
    # Only respond if message starts with "claude:" or "@claude"
    if not (message.content.startswith("claude:") or f"<@{bot.user.id}>" in message.content):
        return

    # Strip prefix
    content = message.content.replace("claude:", "").replace(f"<@{bot.user.id}>", "").strip()
    # ... send to API
```

**Savings:**
- Only processes messages explicitly for Claude
- Ignores casual chat
- **Massive cost savings if channel has other conversations**

---

### Option 4: Token Counter + Warning

```python
import tiktoken

# At startup
encoder = tiktoken.get_encoding("cl100k_base")

@bot.event
async def on_message(message):
    # Count tokens
    tokens = len(encoder.encode(message.content))

    if tokens > 500:
        await message.channel.send(f"⚠️ Your message is {tokens} tokens. This will cost more. Shorten it?")
        return

    # ... send to API
```

**Savings:**
- Warns about expensive messages
- Prevents accidental large inputs

---

## Anthropic Console - What You CAN'T Control

**No settings for:**
- ❌ Default max_tokens (must set in code)
- ❌ Default model (must set in code)
- ❌ Response caching
- ❌ Batch processing discounts

**Everything must be configured in your code.**

---

## Monitoring Costs

### Via Anthropic Console

1. **Usage Dashboard:**
   - Go to https://console.anthropic.com/settings/usage
   - View daily/monthly token usage
   - See cost breakdown by model

2. **API Key Stats:**
   - Settings → API Keys
   - Click on your key
   - View usage for that specific key

3. **Billing:**
   - Settings → Billing
   - View current month charges
   - Download invoices

---

### Via Code (Log Every Call)

Add to bot:

```python
import logging

logging.basicConfig(filename='api_usage.log', level=logging.INFO)

@bot.event
async def on_message(message):
    # ... after API call
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    # Calculate cost
    input_cost = (input_tokens / 1_000_000) * 0.25
    output_cost = (output_tokens / 1_000_000) * 1.25
    total_cost = input_cost + output_cost

    logging.info(f"Message cost: ${total_cost:.6f} | In: {input_tokens} | Out: {output_tokens}")

    # Optional: Send to Discord
    if total_cost > 0.001:  # More than $0.001
        await message.channel.send(f"💰 That message cost ${total_cost:.4f}")
```

---

## Cost Comparison

### Current Setup (Haiku, 150 tokens, minimal history)
- **Per message:** ~$0.00009
- **1000 messages:** ~$0.09
- **10,000 messages:** ~$0.90

### If you disable history (Option 1)
- **Per message:** ~$0.00005
- **1000 messages:** ~$0.05
- **10,000 messages:** ~$0.50

### If you used Sonnet instead (DON'T)
- **Per message:** ~$0.0009 (10x more)
- **1000 messages:** ~$0.90
- **10,000 messages:** ~$9.00

### If you used Opus instead (REALLY DON'T)
- **Per message:** ~$0.009 (100x more)
- **1000 messages:** ~$9.00
- **10,000 messages:** ~$90.00

---

## Recommended Settings for You

### In Anthropic Console:
1. ✅ Set spending limit: **$5/month**
2. ✅ Enable budget alerts at 50%, 75%, 90%
3. ✅ Set alert email

### In Bot Code (Add These):
1. **Add cooldown** (5 seconds between messages)
2. **Add command prefix** (only respond to "claude: message")
3. **Disable conversation history** (make each message standalone)
4. **Add usage logging** (track costs per message)

### With All Optimizations:
- **Estimated cost:** $0.05 per 1000 messages
- **At $5/month limit:** ~100,000 messages possible
- **That's 3,300 messages per day**

---

## Implementation Priority

**Do These Now:**
1. Set spending limit in console ($5/month)
2. Add cooldown to bot (5 seconds)
3. Add command prefix ("claude: message")

**Optional:**
4. Disable conversation history (if context not needed)
5. Add usage logging
6. Add token counter warnings

---

## How to Add Optimizations

### 1. Set Spending Limit (Console)
- Go to: https://console.anthropic.com/settings/limits
- Click "Set Limit"
- Enter: $5
- Save

### 2. Add Cooldown (Code)

Add this to `claude_discord_bot.py` after imports:

```python
from collections import defaultdict
import time

user_last_message = defaultdict(float)
COOLDOWN = 5  # seconds
```

Then in `on_message`, add before "Send to Claude API":

```python
# Rate limiting
user_id = message.author.id
now = time.time()
if now - user_last_message[user_id] < COOLDOWN:
    await message.channel.send("⏱️ Wait 5 seconds between messages.")
    return
user_last_message[user_id] = now
```

### 3. Add Command Prefix (Code)

In `on_message`, add after checking for commands:

```python
# Only respond if message starts with "claude:"
if not message.content.lower().startswith("claude:"):
    return

# Strip prefix
user_message = message.content[7:].strip()  # Remove "claude:"
```

Then replace `message.content` with `user_message` when sending to API.

---

## Summary

**Absolutely Minimal Cost Configuration:**
- Model: Haiku ✅
- max_tokens: 150 ✅
- Terse system prompt ✅
- Limited history ✅
- Rate limiting (add)
- Command prefix (add)
- Spending limit: $5/month (set in console)

**With all optimizations:**
- ~$0.00003 per message
- $5 = ~166,000 messages
- That's 5,500 messages per day

**You'll barely spend anything.**

---

## Console URLs

- **Usage Dashboard:** https://console.anthropic.com/settings/usage
- **Spending Limits:** https://console.anthropic.com/settings/limits
- **API Keys:** https://console.anthropic.com/settings/keys
- **Billing:** https://console.anthropic.com/settings/billing

---

## Warning Signs of High Usage

Watch for:
- ⚠️ Multiple messages per second
- ⚠️ Very long messages (>500 tokens)
- ⚠️ Bot responding to every message in busy channel
- ⚠️ Conversation history growing large

**Solution:** Add the rate limiting and command prefix immediately.

---

**Bottom line:** You're already optimized. Just set spending limit and add cooldown/prefix to be ultra-safe.
