"""
Discord Bot with Local AI Integration
Adds AI commands to Discord bot using local Granite model
"""

import os
import discord
from discord.ext import commands
import logging
from typing import Optional

from .ollama_client import OllamaClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AICommands(commands.Cog):
    """AI-powered commands for Discord bot"""

    def __init__(self, bot, model: str = "granite-4.0-h-micro:latest"):
        self.bot = bot
        self.client = OllamaClient(model=model)
        self.conversation_history = {}  # Store per-user conversation

    @commands.command(name='ai', help='Ask the local AI model anything')
    async def ask_ai(self, ctx, *, question: str):
        """
        Ask a question to the local AI model

        Usage: !ai What is Docker?
        """
        try:
            await ctx.send(f"🤔 Thinking...")

            # Get response from local model
            response = self.client.generate(
                prompt=question,
                temperature=0.7,
                max_tokens=500
            )

            # Split long responses
            if len(response) > 2000:
                chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
                for chunk in chunks:
                    await ctx.send(chunk)
            else:
                await ctx.send(f"🤖 {response}")

        except Exception as e:
            logger.error(f"Error in AI command: {e}")
            await ctx.send(f"❌ Error: {str(e)}")

    @commands.command(name='code', help='Get AI help with code')
    async def code_help(self, ctx, *, code_question: str):
        """
        Get coding help from AI

        Usage: !code How do I read a file in Python?
        """
        try:
            await ctx.send(f"💻 Analyzing...")

            system = "You are an expert programmer. Provide clear, concise code examples."
            response = self.client.generate(
                prompt=code_question,
                system=system,
                temperature=0.5
            )

            await ctx.send(f"```\n{response[:1900]}\n```")

        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

    @commands.command(name='review', help='Review code snippet')
    async def review_code(self, ctx, *, code: str):
        """
        Review code for issues

        Usage: !review ```python
        def my_func():
            return x
        ```
        """
        try:
            await ctx.send(f"🔍 Reviewing code...")

            system = """You are a code reviewer. Analyze for:
- Bugs
- Security issues
- Best practices
- Performance"""

            response = self.client.generate(
                prompt=f"Review this code:\n\n{code}",
                system=system,
                temperature=0.3
            )

            await ctx.send(f"📊 **Code Review:**\n{response[:1900]}")

        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

    @commands.command(name='explain', help='Explain a technical concept')
    async def explain(self, ctx, *, concept: str):
        """
        Explain technical concepts

        Usage: !explain What is Docker?
        """
        try:
            await ctx.send(f"📚 Looking that up...")

            system = "Explain technical concepts clearly and concisely with examples."
            response = self.client.generate(
                prompt=f"Explain: {concept}",
                system=system,
                temperature=0.6
            )

            await ctx.send(f"📖 {response[:1900]}")

        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

    @commands.command(name='chat', help='Have a conversation with AI')
    async def chat(self, ctx, *, message: str):
        """
        Chat with AI (remembers conversation context)

        Usage: !chat Tell me a joke about programming
        """
        try:
            user_id = ctx.author.id

            # Initialize conversation if needed
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []

            # Add user message
            self.conversation_history[user_id].append({
                "role": "user",
                "content": message
            })

            # Keep only last 10 messages
            if len(self.conversation_history[user_id]) > 10:
                self.conversation_history[user_id] = self.conversation_history[user_id][-10:]

            await ctx.send(f"💬 Chatting...")

            # Get AI response
            response = self.client.chat(self.conversation_history[user_id])

            # Add AI response to history
            self.conversation_history[user_id].append({
                "role": "assistant",
                "content": response
            })

            await ctx.send(f"🤖 {response[:1900]}")

        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

    @commands.command(name='clear_chat', help='Clear conversation history')
    async def clear_chat(self, ctx):
        """Clear your conversation history"""
        user_id = ctx.author.id
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
        await ctx.send("✅ Conversation history cleared!")

    @commands.command(name='ai_status', help='Check AI model status')
    async def ai_status(self, ctx):
        """Check if AI model is available"""
        try:
            if self.client.is_available():
                models = self.client.list_models()
                await ctx.send(f"✅ AI is online!\n📦 Models: {', '.join(models)}")
            else:
                await ctx.send(f"❌ AI offline. Host: {self.client.host}")
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")


async def setup(bot):
    """Setup function for Discord bot cog"""
    await bot.add_cog(AICommands(bot))


# Standalone bot example
def create_ai_bot(token: str, model: str = "granite-4.0-h-micro:latest"):
    """
    Create a Discord bot with AI commands

    Args:
        token: Discord bot token
        model: Ollama model to use

    Returns:
        Configured bot instance
    """
    intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f'Bot logged in as {bot.user}')
        await bot.add_cog(AICommands(bot, model=model))

    return bot


if __name__ == "__main__":
    # Run as standalone bot
    TOKEN = os.getenv("DISCORD_TOKEN")

    if not TOKEN:
        print("Error: DISCORD_TOKEN not set")
        exit(1)

    bot = create_ai_bot(TOKEN)
    bot.run(TOKEN)
