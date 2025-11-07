# Conversation Learning System 🧠

## Overview

Your Discord bot now **learns from conversations in real-time** to understand your server's unique communication style, slang, and semantics. Every conversation is logged and used to improve future responses.

## How It Works

### 1. Real-Time Logging
Every message in auto-response enabled channels is logged with:
- **Timestamp** - When the conversation happened
- **Channel & User Info** - Who said what and where
- **Message Content** - The full conversation
- **Bot Response** - What the bot replied
- **Model Used** - Which AI model responded

### 2. Context Injection
When responding to messages, the bot:
- Loads the **last 15 messages** from the conversation history
- Builds a **context prompt** with recent exchanges
- Injects this context into the AI model's prompt
- The AI can then respond with awareness of:
  - Recent topics discussed
  - Communication patterns
  - Server-specific slang and terminology
  - Conversation flow and continuity

### 3. Pattern Learning
The bot analyzes conversations to learn:
- **Frequently used terms** - Server-specific slang and jargon
- **Active users** - Who participates most
- **Communication style** - How your community talks
- **Common topics** - What you discuss frequently

## Commands

### View Conversation Statistics
```
!stats_conv
```
Shows:
- Total messages logged
- Log file size
- Storage location

### Analyze Learned Patterns
```
!learn_patterns
```
Shows:
- Most frequently used terms (top 10)
- Active users (top 5)
- Total messages analyzed
- Communication patterns discovered

### View Recent Context
```
!context
```
Shows:
- Last 5-10 message exchanges in the current channel
- What context the bot is using for responses
- Recent conversation continuity

## Benefits

### 🎯 Better Responses
- Bot understands **ongoing conversations**
- Maintains **context** across multiple messages
- Responds to **follow-up questions** intelligently

### 🗣️ Learns Your Style
- Adapts to your **server's slang**
- Understands **community-specific terms**
- Mirrors your **communication patterns**

### 📊 Continuity
- Remembers **recent topics**
- Maintains **conversation flow**
- Provides **relevant answers** based on context

## Storage

Conversations are stored in:
```
ai_tools/conversation_history.jsonl
```

**Format:** JSONL (JSON Lines)
- One conversation entry per line
- Easy to parse and analyze
- Efficient for large datasets
- Human-readable

**Example Entry:**
```json
{
  "timestamp": "2025-11-07T12:30:00.000000",
  "channel_id": 1234567890,
  "channel_name": "general",
  "user_id": 9876543210,
  "user_name": "Stryker",
  "message": "what's docker?",
  "bot_response": "Docker is a containerization platform...",
  "model_used": "phi"
}
```

## Privacy & Control

### What's Logged
- ✅ Messages in **auto-response enabled channels only**
- ✅ User messages and bot responses
- ✅ Channel and user metadata
- ❌ **NOT logged:** Commands, bot messages, disabled channels

### Data Control
- All data stays **local** in your Docker container
- Stored in **plaintext JSONL** - easy to inspect or delete
- **No external transmission** - conversations never leave your server
- Delete the file anytime: `rm ai_tools/conversation_history.jsonl`

## Advanced Usage

### Analyzing Patterns Manually

You can analyze the conversation log yourself:

```bash
# View recent conversations
docker exec phigen-discord-multimodel tail -20 /app/ai_tools/conversation_history.jsonl

# Count total conversations
docker exec phigen-discord-multimodel wc -l /app/ai_tools/conversation_history.jsonl

# Search for specific terms
docker exec phigen-discord-multimodel grep "docker" /app/ai_tools/conversation_history.jsonl
```

### Clearing History

To start fresh:

```bash
# Clear all conversation history
docker exec phigen-discord-multimodel rm /app/ai_tools/conversation_history.jsonl

# Or clear just old entries (keep last 1000)
docker exec phigen-discord-multimodel bash -c "tail -1000 /app/ai_tools/conversation_history.jsonl > /tmp/temp.jsonl && mv /tmp/temp.jsonl /app/ai_tools/conversation_history.jsonl"
```

## Technical Details

### Context Window
- **Default:** Last 15 messages loaded for context
- **Prompt injection:** Last 10 messages included in prompt
- **Pattern analysis:** Last 500-1000 messages analyzed

### Performance Impact
- **Minimal** - JSONL is efficient
- **Fast reads** - Only recent entries loaded
- **Async logging** - Doesn't slow down responses
- **Memory efficient** - No in-memory caching (reads on demand)

### Word Filtering
Common stopwords are filtered when analyzing patterns:
- "the", "and", "for", "are", "but", "not", etc.
- Words under 3 characters
- This highlights **meaningful terms** and **server-specific slang**

## Examples

### Scenario 1: Learning Slang
```
User: "yo bot, what's the diff between docker and k8s?"
Bot: [logs conversation]

[Later, bot learns: "k8s" = Kubernetes, "diff" = difference]

User: "k8s vs docker?"
Bot: [understands from context] "Kubernetes and Docker serve different purposes..."
```

### Scenario 2: Conversation Continuity
```
User: "explain containers"
Bot: "Containers are isolated environments that package applications..."

User: "how do I make one?"
Bot: [sees recent context about containers] "To create a Docker container, use: docker run..."
```

### Scenario 3: Pattern Recognition
```
After 100 messages, !learn_patterns shows:
- Frequently used terms: `docker`, `python`, `api`, `debug`, `deploy`
- Most active users: Stryker (45 msgs), Alice (30 msgs)
- Bot now prioritizes code/technical responses
```

## Troubleshooting

### Bot not learning?
- Check auto-response is enabled: `!auto_status`
- Verify log file exists: `!stats_conv`
- Ensure you're messaging in the right channel

### Context not working?
- Need at least 3-5 prior messages for context
- View current context: `!context`
- Context resets when bot restarts (but log persists)

### File too large?
- JSONL compresses well (~1KB per message)
- Clear old entries periodically
- Consider rotation after 10,000+ messages

## Future Enhancements

Planned features:
- 🔄 **Automatic summarization** - Condense old conversations
- 🎯 **Topic clustering** - Group conversations by topic
- 📈 **Trend analysis** - Track popular topics over time
- 🧪 **A/B testing** - Compare model performance on your data
- 🔍 **Semantic search** - Find similar past conversations

---

**Start chatting in an auto-enabled channel and watch your bot learn!** 🚀

Use `!stats_conv` and `!learn_patterns` to see what it's learning in real-time.
