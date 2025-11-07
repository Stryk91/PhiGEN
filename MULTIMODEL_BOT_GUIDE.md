# 🎮 Multi-Model Discord Bot - Complete Guide

Your Discord bot can now intelligently route questions between **Mistral**, **Granite**, and **Claude** - saving costs while providing the best answers!

## 🚀 What You Get

### 3 AI Models Working Together

| Model | Strength | Cost | Best For |
|-------|----------|------|----------|
| **Mistral 7B** | Fast, conversational | FREE | General questions, chat |
| **Granite 4.0** | Code-optimized | FREE | Programming, technical |
| **Claude Sonnet** | Most powerful | $$$ | Complex reasoning, analysis |

### Smart Cost Optimization

- **Local models first** (Mistral/Granite) - FREE
- **Claude as fallback** - Only when needed
- **Estimated savings: 90%** vs all-Claude

## 📋 Discord Commands

### Basic Commands

```
!ai <question>
Ask the default model (Mistral)
Example: !ai What is Docker?

!mistral <question>
Fast, conversational responses
Example: !mistral Explain Python in simple terms

!granite <question>
Code-optimized, technical answers
Example: !granite How do I optimize this Python loop?

!claude <question>
Most powerful, costs API tokens
Example: !claude Explain quantum computing in detail

!best <question>
Auto-pick the best model for your question
Example: !best Debug this JavaScript error
```

### Advanced Commands

```
!compare <question>
Ask ALL models and compare answers
Example: !compare What's the best way to learn AI?

!code <question>
Get coding help (routes to Granite or Claude)
Example: !code How do I read JSON in Python?

!models
List all available models and their status

!stats
Show usage statistics and cost savings

!switch <model>
Change your default model
Example: !switch granite

!help_ai
Show detailed help and examples
```

## 🎯 Smart Routing Examples

The bot automatically picks the best model based on your question:

### Code Questions → Granite
```
!best How do I optimize this SQL query?
→ Uses Granite (code-optimized, FREE)
```

### General Chat → Mistral
```
!best What's the weather like for coding?
→ Uses Mistral (fast, conversational, FREE)
```

### Complex Analysis → Claude
```
!best Explain the philosophical implications of AI
→ Uses Claude (deep reasoning, costs $$)
```

### Comparison Mode
```
!compare Best programming language for beginners?

🤖 Mistral 7B: "Python is great because..."
🤖 Granite 4.0: "From a technical standpoint..."
🤖 Claude Sonnet: "Consider these factors..."
```

## 💰 Cost Tracking

The bot tracks your usage and shows savings:

```
!stats

📊 AI Usage Statistics
━━━━━━━━━━━━━━━━━━
Total Requests: 150
Estimated Savings: $42.50

Usage Breakdown:
Mistral: 80 requests (53%)
Granite: 60 requests (40%)
Claude: 10 requests (7%)

💡 You saved 93% by using local models!
```

## 🔧 Setup

### Step 1: Start Services

```bash
# Start Ollama and AI services
docker-compose --profile ai up -d
```

### Step 2: Pull Models

```bash
# Pull Mistral (recommended first)
docker exec phigen-ollama ollama pull mistral:7b-instruct-q4_K_M

# Pull Granite
docker exec phigen-ollama ollama pull granite-4.0-h-micro:latest

# Claude API (already configured via ANTHROPIC_API_KEY)
```

### Step 3: Verify

```bash
# Check bot logs
docker-compose logs discord-multimodel-bot

# Test in Discord
!models
!ai Hello!
```

## 📊 Model Selection Logic

### Automatic Routing (`!best`)

The bot analyzes your question for keywords:

```python
"code", "function", "debug", "error"
  → Granite (code specialist)

"analyze", "review", "explain"
  → Claude (deep analysis)

"chat", "hello", "talk"
  → Mistral (conversational)

Default
  → Mistral (fast & free)
```

### Manual Override

Use specific commands to force a model:
- `!mistral` - Always use Mistral
- `!granite` - Always use Granite
- `!claude` - Always use Claude API

## 🎨 Discord Embed Colors

Models are color-coded for easy recognition:

- 🔵 **Mistral** - Blue
- 🟢 **Granite** - Green
- 🟣 **Claude** - Purple

## 🔥 Pro Tips

### 1. Use !compare for Important Decisions
```
!compare Should I use TypeScript or JavaScript?
```
See all 3 perspectives, make informed choices!

### 2. Set Personal Preference
```
!switch granite    # For developers
!switch mistral    # For general use
!switch claude     # For maximum quality
```

### 3. Save Costs with Local Models
```
Most questions can be answered by Mistral/Granite
Only use !claude for truly complex tasks
→ Save 90%+ on API costs!
```

### 4. Code Review Workflow
```
!granite Review this Python function
→ Fast, free code analysis

!claude Explain the security implications
→ Deep analysis when needed
```

## 🛠️ Configuration

### Environment Variables (.env)

```bash
# Discord Bot
DISCORD_TOKEN=your_discord_bot_token

# Anthropic (for Claude)
ANTHROPIC_API_KEY=your_anthropic_key

# Ollama (auto-configured)
OLLAMA_HOST=http://ollama:11434
```

### Docker Services

```bash
# Start multi-model bot
docker-compose --profile ai up discord-multimodel-bot -d

# View logs
docker-compose logs -f discord-multimodel-bot

# Restart
docker-compose restart discord-multimodel-bot

# Stop
docker-compose stop discord-multimodel-bot
```

## 📈 Performance Expectations

| Model | Speed | Quality | Cost |
|-------|-------|---------|------|
| Mistral | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | FREE |
| Granite | ⚡⚡ Medium | ⭐⭐⭐⭐ Great (code) | FREE |
| Claude | ⚡ Slower | ⭐⭐⭐⭐⭐ Excellent | $$$ |

### Response Times (Approximate)

- **Mistral**: 1-3 seconds
- **Granite**: 2-4 seconds
- **Claude API**: 2-5 seconds (depends on network)

## 🔍 Troubleshooting

### Bot Not Responding

```bash
# Check bot is running
docker-compose ps | grep multimodel

# View logs
docker-compose logs discord-multimodel-bot

# Restart
docker-compose restart discord-multimodel-bot
```

### "Model Not Available"

```bash
# Check Ollama is running
docker-compose ps | grep ollama

# Pull missing model
docker exec phigen-ollama ollama pull mistral:7b-instruct-q4_K_M

# Verify models
docker exec phigen-ollama ollama list
```

### Claude API Errors

```bash
# Check API key is set
docker exec phigen-discord-multimodel env | grep ANTHROPIC

# Test API key
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

## 🎯 Usage Patterns

### For Developers
```
Default: !switch granite
Quick questions: !ai
Code review: !granite
Architecture decisions: !claude
Compare approaches: !compare
```

### For General Users
```
Default: !switch mistral
Daily questions: !ai
Learning: !best
Deep dives: !claude
```

### For Teams
```
Enable !stats tracking
Monitor usage patterns
Optimize model selection
Reduce API costs
```

## 📚 Command Reference

| Command | Arguments | Description | Example |
|---------|-----------|-------------|---------|
| `!ai` | `<question>` | Ask default model | `!ai What is Python?` |
| `!mistral` | `<question>` | Ask Mistral | `!mistral Explain async` |
| `!granite` | `<question>` | Ask Granite | `!granite Review code` |
| `!claude` | `<question>` | Ask Claude | `!claude Deep analysis` |
| `!best` | `<question>` | Auto-route | `!best Debug error` |
| `!compare` | `<question>` | Ask all models | `!compare Best DB?` |
| `!code` | `<question>` | Coding help | `!code Read JSON` |
| `!models` | - | List models | `!models` |
| `!stats` | - | Usage stats | `!stats` |
| `!switch` | `<model>` | Change default | `!switch granite` |
| `!help_ai` | - | Show help | `!help_ai` |

## 💡 Real-World Examples

### Example 1: Code Review
```
User: !granite Review this function:
def process_data(data):
    result = eval(data)
    return result

Bot: 🟢 Granite 4.0 Micro
⚠️ CRITICAL SECURITY ISSUE
Using eval() is dangerous! It allows arbitrary code execution...
Recommendation: Use json.loads() or ast.literal_eval() instead.
```

### Example 2: Learning
```
User: !compare What's the difference between Docker and VM?

Bot: [Shows 3 different perspectives]
🔵 Mistral: Quick, practical explanation
🟢 Granite: Technical architecture details
🟣 Claude: Comprehensive analysis with use cases
```

### Example 3: Cost Optimization
```
User: !stats

Bot: 📊 You've made 500 requests
- Mistral: 350 (70%)
- Granite: 130 (26%)
- Claude: 20 (4%)

💰 Estimated Savings: $147.50
By using local models for 96% of requests!
```

## 🚀 Next Steps

1. **Customize Routing** - Edit `model_router.py` to change selection logic
2. **Add More Models** - Ollama supports 50+ models
3. **Create Custom Commands** - Add domain-specific bot commands
4. **Monitor Usage** - Track which models work best for your team
5. **Fine-tune** - Adjust temperature, context, etc. per model

## 📖 Related Documentation

- **Full AI Guide**: `AI_INTEGRATION_COMPLETE.md`
- **API Documentation**: `ai_tools/README.md`
- **Model Router Code**: `ai_tools/model_router.py`
- **Bot Code**: `ai_tools/discord_multimodel_bot.py`

---

## 🎉 You're Ready!

Your Discord server now has a **smart, cost-optimized AI assistant** that automatically picks the best model for every question!

**Start using it:**
```
!help_ai
!models
!ai Hello, AI!
```

**Happy chatting! 🤖**
