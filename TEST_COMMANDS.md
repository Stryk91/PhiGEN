# 🧪 Multi-Model Bot Test Commands

Quick reference for testing your multi-model Discord bot once services are running.

## 🚀 Startup Commands

```bash
# Check if Docker download is complete
docker-compose ps

# View Ollama logs
docker-compose logs ollama

# Start all AI services (if not already running)
docker-compose --profile ai up -d

# Check which models are available
docker exec phigen-ollama ollama list
```

---

## 🔍 Pre-Flight Checks

### 1. Check Services Status
```bash
# View all running containers
docker-compose ps

# Expected output:
# phigen-ollama              - Should be "Up"
# phigen-ai-api              - Should be "Up"
# phigen-discord-multimodel  - Should be "Up"
```

### 2. Verify Ollama is Working
```bash
# Check Ollama API
curl http://localhost:11434/api/tags

# Pull models if needed
docker exec phigen-ollama ollama pull mistral:7b-instruct-q4_K_M
docker exec phigen-ollama ollama pull granite-4.0-h-micro:latest

# List available models
docker exec phigen-ollama ollama list
```

### 3. Test Model Router
```bash
# Run test suite
docker exec phigen-dev python ai_tools/test_multimodel.py

# Expected output:
# ✅ Router Initialization ........ PASS
# ✅ Model Status ................. PASS
# ✅ Mistral Generation ........... PASS
# ✅ Granite Generation ........... PASS
# ⚠️  Claude API .................. FAIL (if no API key)
# ✅ Smart Routing ................ PASS
# ✅ Model Comparison ............. PASS
# ✅ Usage Tracking ............... PASS
```

### 4. Check Discord Bot Logs
```bash
# View bot startup logs
docker-compose logs discord-multimodel-bot

# Expected to see:
# "🤖 Multi-Model Bot logged in as [BotName]"
# "Model Status:"
# "  ✅ Mistral: ollama"
# "  ✅ Granite: ollama"
```

---

## 💬 Discord Test Commands

Once the bot is online in your Discord server, test these:

### Basic Commands

```discord
!help_ai
# Should show: Full command list and examples

!models
# Should show: Status of all 3 models (Mistral, Granite, Claude)
# Expected: Mistral ✅, Granite ✅, Claude ✅ or ❌

!ai_status
# Should show: Which models are available
```

### Model-Specific Tests

```discord
!ai Hello, I'm testing the AI bot!
# Expected: Response from Mistral (default)
# Should see: 🔵 Blue embed with "Mistral 7B Instruct"

!mistral Tell me a joke about programming
# Expected: Response from Mistral
# Should be: Fast, conversational tone

!granite What is a Python decorator?
# Expected: Response from Granite
# Should be: Technical, code-focused answer

!claude Explain quantum entanglement (if API key configured)
# Expected: Response from Claude OR error about API key
```

### Smart Routing Tests

```discord
!best How do I fix a Python syntax error?
# Expected: Routes to GRANITE (code task)
# Should show: "Task: code | Model: granite"

!best Tell me a fun fact
# Expected: Routes to MISTRAL (general task)
# Should show: "Task: general | Model: mistral"

!code How do I read a JSON file in Python?
# Expected: Code help from Granite
# Should include: Code examples
```

### Comparison Mode

```discord
!compare What is Docker?
# Expected: 3 separate responses
# Should see:
#   🔵 Mistral's answer
#   🟢 Granite's answer
#   🟣 Claude's answer (or "not available")

!compare Best way to learn programming?
# Expected: Three different perspectives
# Compare the depth and style of each answer
```

### Statistics

```discord
!stats
# Expected: Usage breakdown
# Should show:
#   - Total Requests: X
#   - Estimated Savings: $X.XX
#   - Usage Breakdown by model

!switch granite
# Expected: "✅ Switched to Granite 4.0 Micro"
# Now !ai will use Granite by default

!ai What is asyncio?
# Expected: Response from Granite (your new default)

!switch mistral
# Expected: Back to Mistral as default
```

---

## 🧪 Advanced Tests

### Test Error Handling

```discord
!ai
# Expected: Error message about missing question

!switch fakemodel
# Expected: Error listing available models

!compare
# Expected: Error about missing question
```

### Test Conversation Memory

```discord
!chat Hello!
# Response from bot

!chat What did I just say?
# Expected: Bot remembers "Hello!"

!clear_chat
# Expected: "✅ Conversation history cleared!"

!chat What did I say before?
# Expected: Bot doesn't remember (fresh start)
```

### Test Code Review

```discord
!review def unsafe(x):
    return eval(x)

# Expected: Security warning about eval()
# Should mention: Use ast.literal_eval() instead
```

---

## 🔧 Command Line Tests

### Test REST API

```bash
# Health check
curl http://localhost:8000/health

# Generate text
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Say hello in one sentence"}'

# Compare models via API
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is Python?", "model": "mistral"}'
```

### Test Python Integration

```bash
# Run examples
docker exec phigen-dev python ai_tools/examples.py

# Interactive test
docker exec -it phigen-dev python3
```

```python
from ai_tools import ModelRouter

router = ModelRouter()

# Check status
print(router.get_status())

# Test generation
response, model = router.route("Say hi!", model="mistral")
print(f"{model.name}: {response}")

# Compare models
results = router.compare_models("What is AI?")
for model, response in results.items():
    print(f"\n{model}:\n{response[:100]}...")

# Check stats
print(router.get_stats())
```

---

## 📊 Performance Tests

### Response Time Tests

```discord
# Test Mistral speed (should be fastest)
!mistral Quick test

# Test Granite speed
!granite Quick test

# Test Claude speed (if configured)
!claude Quick test

# Compare all three
!compare Quick test
```

**Expected times:**
- Mistral: 1-3 seconds ⚡⚡⚡
- Granite: 2-4 seconds ⚡⚡
- Claude: 2-5 seconds ⚡

### Load Test

```discord
# Send 10 quick questions
!ai test 1
!ai test 2
!ai test 3
... (repeat)

# Then check stats
!stats
# Should show: 10+ requests tracked
```

---

## 🐛 Troubleshooting Tests

### If Bot Doesn't Respond

```bash
# Check bot is running
docker-compose ps | grep multimodel

# View logs
docker-compose logs discord-multimodel-bot --tail=50

# Restart bot
docker-compose restart discord-multimodel-bot
```

### If "Model Not Available"

```bash
# Check Ollama
docker-compose ps | grep ollama

# List models
docker exec phigen-ollama ollama list

# Pull missing model
docker exec phigen-ollama ollama pull mistral:7b-instruct-q4_K_M
docker exec phigen-ollama ollama pull granite-4.0-h-micro:latest
```

### If Claude Errors

```bash
# Check API key is set
docker exec phigen-discord-multimodel env | grep ANTHROPIC

# Test API key directly
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 10,
    "messages": [{"role": "user", "content": "Hi"}]
  }'
```

---

## ✅ Success Criteria

After running all tests, you should see:

**✅ Services:**
- [ ] Ollama running
- [ ] Discord bot online
- [ ] API responding on port 8000

**✅ Models:**
- [ ] Mistral available
- [ ] Granite available
- [ ] Claude working (if configured)

**✅ Discord:**
- [ ] Bot responds to !help_ai
- [ ] !ai command works
- [ ] !compare shows 2-3 responses
- [ ] !stats tracks usage

**✅ Routing:**
- [ ] Code questions go to Granite
- [ ] General questions go to Mistral
- [ ] Comparison mode works

**✅ Performance:**
- [ ] Responses under 5 seconds
- [ ] No errors in logs
- [ ] Stats tracking works

---

## 🎯 Next Steps After Testing

1. **Invite to More Servers**
   - Share bot invite link
   - Test in production

2. **Monitor Usage**
   - Check `!stats` weekly
   - Track savings

3. **Customize**
   - Edit routing rules in `model_router.py`
   - Add custom commands

4. **Scale**
   - Try other Ollama models
   - Optimize for your use case

---

## 📝 Test Checklist

```
□ Docker services started
□ Ollama downloaded models
□ Bot appears online in Discord
□ !help_ai shows commands
□ !models shows status
□ !ai responds
□ !mistral responds
□ !granite responds
□ !best routes correctly
□ !compare shows multiple answers
□ !stats tracks usage
□ API health check passes
□ Python integration works
□ No errors in logs
```

---

**When all tests pass, you're ready to use your multi-model AI bot! 🎉**
