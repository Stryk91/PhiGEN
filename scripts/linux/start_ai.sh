#!/bin/bash
# Quick start script for PhiGEN AI services

echo "=========================================="
echo "PhiGEN AI Services Startup"
echo "=========================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    exit 1
fi

echo "✅ Docker is running"

# Start Ollama
echo ""
echo "1. Starting Ollama..."
docker-compose --profile ai up ollama -d

# Wait for Ollama to be ready
echo "   Waiting for Ollama to start..."
sleep 5

# Check if model exists
echo ""
echo "2. Checking for Granite model..."
if docker exec phigen-ollama ollama list | grep -q "granite-4.0-h-micro"; then
    echo "   ✅ Granite model found"
else
    echo "   📥 Pulling Granite model (this may take a few minutes)..."
    docker exec phigen-ollama ollama pull granite-4.0-h-micro:latest
fi

# Start AI API
echo ""
echo "3. Starting AI REST API..."
docker-compose --profile ai up ai-api -d

# Optionally start Discord bot
read -p "Start Discord AI bot? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -z "$DISCORD_TOKEN" ]; then
        echo "   ⚠️  DISCORD_TOKEN not set in .env"
        echo "   Skipping Discord bot..."
    else
        echo "   Starting Discord bot..."
        docker-compose --profile ai up discord-ai-bot -d
    fi
fi

# Show status
echo ""
echo "=========================================="
echo "Services Status:"
echo "=========================================="
docker-compose ps

echo ""
echo "=========================================="
echo "Quick Test:"
echo "=========================================="
echo ""
echo "Test API:"
echo "  curl http://localhost:8000/health"
echo ""
echo "Test generation:"
echo '  curl -X POST http://localhost:8000/api/generate -H "Content-Type: application/json" -d '"'"'{"prompt": "Hello!"}'"'"''
echo ""
echo "Run examples:"
echo "  docker exec phigen-dev python ai_tools/examples.py"
echo ""
echo "Run tests:"
echo "  docker exec phigen-dev python ai_tools/test_ai_integration.py"
echo ""
echo "View logs:"
echo "  docker-compose logs -f ai-api"
echo ""
echo "Stop services:"
echo "  docker-compose --profile ai down"
echo ""
echo "=========================================="
echo "✅ AI services are ready!"
echo "=========================================="
