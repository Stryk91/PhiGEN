#!/bin/bash
# Quick start script for Multi-Model Discord Bot

echo "=========================================="
echo "Multi-Model Discord Bot Startup"
echo "=========================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    exit 1
fi

echo "✅ Docker is running"

# Check DISCORD_TOKEN
if [ -z "$DISCORD_TOKEN" ] && ! grep -q "DISCORD_TOKEN=" .env 2>/dev/null; then
    echo ""
    echo "⚠️  WARNING: DISCORD_TOKEN not found in .env"
    echo "   The Discord bot won't start without it."
    echo "   Add it to .env: DISCORD_TOKEN=your_token_here"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Start Ollama
echo ""
echo "1. Starting Ollama..."
docker-compose --profile ai up ollama -d
sleep 3

# Check if models exist
echo ""
echo "2. Checking models..."

MISTRAL_EXISTS=$(docker exec phigen-ollama ollama list 2>/dev/null | grep -c "mistral" || echo "0")
GRANITE_EXISTS=$(docker exec phigen-ollama ollama list 2>/dev/null | grep -c "granite" || echo "0")

if [ "$MISTRAL_EXISTS" -eq "0" ]; then
    echo "   📥 Pulling Mistral (this will take a few minutes)..."
    docker exec phigen-ollama ollama pull mistral:7b-instruct-q4_K_M
else
    echo "   ✅ Mistral found"
fi

if [ "$GRANITE_EXISTS" -eq "0" ]; then
    echo "   📥 Pulling Granite (this will take a few minutes)..."
    docker exec phigen-ollama ollama pull granite-4.0-h-micro:latest
else
    echo "   ✅ Granite found"
fi

# Start multi-model bot
echo ""
echo "3. Starting Multi-Model Discord Bot..."
docker-compose --profile ai up discord-multimodel-bot -d

# Wait a moment for startup
sleep 3

# Show status
echo ""
echo "=========================================="
echo "Services Status:"
echo "=========================================="
docker-compose ps | grep -E "ollama|multimodel|NAME"

# Show logs preview
echo ""
echo "=========================================="
echo "Recent Bot Logs:"
echo "=========================================="
docker-compose logs --tail=10 discord-multimodel-bot

echo ""
echo "=========================================="
echo "Multi-Model Bot is Ready!"
echo "=========================================="
echo ""
echo "📊 Model Status:"
docker exec phigen-dev python ai_tools/test_multimodel.py 2>/dev/null | grep -E "Testing|✅|❌" | head -20 || echo "Run: docker exec phigen-dev python ai_tools/test_multimodel.py"

echo ""
echo "🎮 Discord Commands:"
echo "  !help_ai          - Show all commands"
echo "  !models           - List available models"
echo "  !ai <question>    - Ask Mistral"
echo "  !granite <q>      - Ask Granite"
echo "  !claude <q>       - Ask Claude"
echo "  !compare <q>      - Ask all models"
echo "  !stats            - Usage statistics"
echo ""
echo "📖 Full Guide: MULTIMODEL_BOT_GUIDE.md"
echo ""
echo "🔍 View Live Logs:"
echo "  docker-compose logs -f discord-multimodel-bot"
echo ""
echo "🛑 Stop Services:"
echo "  docker-compose --profile ai down"
echo ""
echo "=========================================="
