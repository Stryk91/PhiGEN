# PhiGEN AI Tools

Local AI integration using Ollama and Granite models. Privacy-first, cost-free AI for your development workflow.

## Features

- 🤖 **Local AI Models** - Run Granite 4.0 and other models locally
- 💻 **Code Review** - AI-powered code analysis and suggestions
- 📊 **Log Analysis** - Automated log parsing and error detection
- 🤝 **Discord Bot** - AI commands in Discord
- 🌐 **REST API** - HTTP interface for AI features
- 🔒 **Privacy** - All data stays local, no cloud APIs

## Quick Start

### 1. Start Ollama with AI Services

```bash
# Start all AI services
docker-compose --profile ai up -d

# Or start individual services
docker-compose up ollama -d
docker-compose up ai-api -d
docker-compose up discord-ai-bot -d
```

### 2. Pull the Granite Model

```bash
docker exec -it phigen-ollama ollama pull granite-4.0-h-micro:latest
```

### 3. Test the API

```bash
curl http://localhost:8000/health
```

## Usage Examples

### Code Review

**Command Line:**
```bash
# Review a single file
docker exec phigen-dev python -m ai_tools.code_reviewer --file myfile.py

# Review entire directory
docker exec phigen-dev python -m ai_tools.code_reviewer --dir ./src --output review.md

# Review git diff
docker exec phigen-dev python -m ai_tools.code_reviewer --diff
```

**Python:**
```python
from ai_tools import CodeReviewer

reviewer = CodeReviewer()
result = reviewer.review_file("myfile.py")
print(result['review'])
```

**API:**
```bash
curl -X POST http://localhost:8000/api/review/file \
  -H "Content-Type: application/json" \
  -d '{"filepath": "myfile.py"}'
```

### Log Analysis

**Command Line:**
```bash
# Analyze log file
docker exec phigen-dev python -m ai_tools.log_analyzer --file app.log

# Analyze Docker logs
docker exec phigen-dev python -m ai_tools.log_analyzer --docker phigen-dev --lines 500
```

**Python:**
```python
from ai_tools import LogAnalyzer

analyzer = LogAnalyzer()
result = analyzer.analyze_docker_logs("phigen-dev")
print(result['analysis'])
```

**API:**
```bash
curl -X POST http://localhost:8000/api/analyze/docker \
  -H "Content-Type: application/json" \
  -d '{"container": "phigen-dev", "lines": 200}'
```

### Discord Bot Commands

Once the Discord bot is running, use these commands:

```
!ai What is Docker?
!code How do I read a file in Python?
!review <paste code here>
!explain What is WSL2?
!chat Tell me about AI models
!clear_chat
!ai_status
```

### REST API

**Generate Text:**
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain Docker in simple terms",
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

**Chat (with history):**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is Python?"},
      {"role": "assistant", "content": "Python is a programming language."},
      {"role": "user", "content": "What can I do with it?"}
    ]
  }'
```

**Code Review:**
```bash
curl -X POST http://localhost:8000/api/review/code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def my_func():\n    return x",
    "language": "python"
  }'
```

### Python Client

```python
from ai_tools import OllamaClient

# Initialize client
client = OllamaClient(
    host="http://localhost:11434",
    model="granite-4.0-h-micro:latest"
)

# Generate text
response = client.generate("Write a haiku about coding")
print(response)

# Chat with context
messages = [
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi! How can I help?"},
    {"role": "user", "content": "Tell me about AI"}
]
response = client.chat(messages)
print(response)

# Check available models
models = client.list_models()
print(f"Available models: {models}")
```

## Docker Services

| Service | Port | Description |
|---------|------|-------------|
| `ollama` | 11434 | Ollama model server |
| `ai-api` | 8000 | REST API for AI features |
| `discord-ai-bot` | - | Discord bot with AI commands |
| `ai-code-reviewer` | - | Background code reviewer |
| `ai-log-analyzer` | - | Background log analyzer |

## Environment Variables

Add to your `.env` file:

```bash
# Ollama Configuration
OLLAMA_HOST=http://ollama:11434
AI_MODEL=granite-4.0-h-micro:latest

# API Configuration
API_PORT=8000
API_HOST=0.0.0.0

# Discord Bot (if using)
DISCORD_TOKEN=your_token_here
```

## Available Models

Common Ollama models you can use:

```bash
# Pull different models
docker exec phigen-ollama ollama pull granite-4.0-h-micro:latest
docker exec phigen-ollama ollama pull llama2:7b
docker exec phigen-ollama ollama pull codellama:7b
docker exec phigen-ollama ollama pull mistral:7b

# List installed models
docker exec phigen-ollama ollama list
```

## Integration Examples

### GitHub Actions (Code Review on PR)

```yaml
name: AI Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Review Code
        run: |
          docker-compose up ollama -d
          docker exec phigen-dev python -m ai_tools.code_reviewer --diff --output review.md
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Review staged changes
docker exec phigen-dev python -m ai_tools.code_reviewer --diff
```

### Automated Log Monitoring

```bash
# Cron job to analyze logs daily
0 0 * * * docker exec phigen-dev python -m ai_tools.log_analyzer --dir /var/log --output /reports/daily-$(date +\%Y\%m\%d).md
```

## API Reference

Full API documentation available at: `http://localhost:8000/`

## Troubleshooting

**Ollama not responding:**
```bash
docker-compose logs ollama
docker restart phigen-ollama
```

**Model not found:**
```bash
docker exec phigen-ollama ollama pull granite-4.0-h-micro:latest
```

**Check service status:**
```bash
docker-compose ps
curl http://localhost:11434/api/tags
curl http://localhost:8000/health
```

**View logs:**
```bash
docker-compose logs -f ai-api
docker-compose logs -f ollama
docker-compose logs -f discord-ai-bot
```

## Performance Tips

1. **GPU Acceleration** - Use Ollama with GPU for faster inference
2. **Model Selection** - Smaller models (7B) are faster, larger (13B+) are more accurate
3. **Batch Processing** - Review multiple files at once
4. **Context Limits** - Keep prompts under 2000 tokens for best performance

## Security

- All AI processing happens locally
- No data sent to external APIs
- Models run in isolated Docker containers
- API is not exposed externally by default

## License

Part of the PhiGEN project.
