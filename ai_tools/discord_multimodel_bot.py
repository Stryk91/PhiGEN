"""
Enhanced Multi-Model Discord Bot
Routes questions to Mistral, Granite, or Claude based on commands
"""

import os
import sys
import discord
from discord.ext import commands
import logging
from typing import Optional
import asyncio
import json
from pathlib import Path
from datetime import datetime

# Add ai_tools to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from model_router import ModelRouter
from conversation_logger import ConversationLogger
from response_feedback import ResponseFeedbackTracker
from user_settings import UserSettingsManager
from conversation_rag import ConversationRAG
from enhanced_personality import get_personality

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultiModelAI(commands.Cog):
    """Multi-model AI commands for Discord"""

    def __init__(self, bot):
        self.bot = bot
        self.router = ModelRouter(default_model="phi")  # Use Phi for fast responses
        self.user_preferences = {}  # Store user's preferred model
        self.custom_commands = {}  # Store dynamically created commands
        self.custom_commands_file = Path(__file__).parent / "custom_commands.json"
        self.auto_response_file = Path(__file__).parent / "auto_response_channels.json"
        self.auto_response_channels = set()  # Channels with auto-response enabled

        # Initialize conversation logger for learning
        self.conversation_log_file = Path(__file__).parent / "conversation_history.jsonl"
        self.conversation_logger = ConversationLogger(self.conversation_log_file)

        # Initialize response feedback tracker for reaction-based learning
        self.feedback_file = Path(__file__).parent / "response_quality.json"
        self.full_log_file = Path(__file__).parent / "conversation_full_log.txt"
        self.feedback_tracker = ResponseFeedbackTracker(self.feedback_file, self.full_log_file)

        # Initialize user settings manager
        self.user_settings_file = Path(__file__).parent / "user_settings.json"
        self.settings_manager = UserSettingsManager(self.user_settings_file)

        # Initialize RAG system for semantic search over conversation history
        self.rag = ConversationRAG(self.full_log_file)
        self.rag_enabled = True  # Can be toggled per user

        # Initialize enhanced personality (data-driven from 85,968 message analysis)
        self.personality = get_personality()

        self._load_custom_commands()
        self._load_auto_response_channels()

    @commands.command(name='ai', help='Ask AI (uses default model: Mistral)')
    async def ask_ai(self, ctx, *, question: str):
        """
        Ask the default AI model

        Usage: !ai What is Docker?
        """
        await self._generate_response(ctx, question, model="mistral")

    @commands.command(name='mistral', help='Ask Mistral 7B (fast, conversational)')
    async def ask_mistral(self, ctx, *, question: str):
        """
        Ask Mistral specifically

        Usage: !mistral Explain Python decorators
        """
        await self._generate_response(ctx, question, model="mistral")

    @commands.command(name='granite', help='Ask Granite (optimized for code)')
    async def ask_granite(self, ctx, *, question: str):
        """
        Ask Granite specifically

        Usage: !granite Review this Python code
        """
        await self._generate_response(ctx, question, model="granite")

    @commands.command(name='claude', help='Ask Claude API (most powerful, costs $$)')
    async def ask_claude(self, ctx, *, question: str):
        """
        Ask Claude API

        Usage: !claude Explain quantum computing
        """
        await self._generate_response(ctx, question, model="claude")

    @commands.command(name='best', help='Auto-pick best model for your question')
    async def ask_best(self, ctx, *, question: str):
        """
        Automatically pick the best model

        Usage: !best How do I optimize my Docker images?
        """
        # Analyze question to determine task type
        question_lower = question.lower()

        if any(word in question_lower for word in ['code', 'function', 'debug', 'error', 'syntax']):
            task_type = "code"
        elif any(word in question_lower for word in ['analyze', 'review', 'explain']):
            task_type = "analysis"
        elif any(word in question_lower for word in ['chat', 'talk', 'hello', 'hi']):
            task_type = "chat"
        else:
            task_type = "general"

        await ctx.send(f"🎯 Selecting best model for {task_type} task...")

        response, model_config = self.router.route(
            question,
            model="auto",
            task_type=task_type
        )

        embed = discord.Embed(
            title=f"🤖 {model_config.display_name}",
            description=response[:4000],  # Discord limit
            color=self._get_model_color(model_config.name)
        )
        embed.set_footer(text=f"Task: {task_type} | Model: {model_config.name}")

        await ctx.send(embed=embed)

    @commands.command(name='compare', help='Ask all models and compare answers')
    async def compare_models(self, ctx, *, question: str):
        """
        Ask all available models and compare

        Usage: !compare What is the best way to learn Python?
        """
        await ctx.send(f"🔍 Asking all models (this may take a moment)...")

        # Add personality guidelines to question
        enhanced_question = (
            f"[You are PhiGEN, created by JC and STRYK. Use Australian English. "
            f"Never mention being an AI/bot/assistant.]\n\n{question}"
        )

        results = self.router.compare_models(enhanced_question)

        # Create embeds for each model
        embeds = []
        for model_name, response in results.items():
            model_config = self.router.MODELS.get(model_name)
            if not model_config:
                continue

            # Truncate if too long
            if len(response) > 1000:
                response = response[:997] + "..."

            embed = discord.Embed(
                title=f"{model_config.display_name}",
                description=response,
                color=self._get_model_color(model_name)
            )

            cost_indicator = "💰 Costs $$" if not model_config.is_local else "✅ FREE"
            embed.set_footer(text=f"{cost_indicator} | {model_config.provider}")

            embeds.append(embed)

        # Send all embeds
        for embed in embeds:
            await ctx.send(embed=embed)

    @commands.command(name='code', help='Get coding help (routes to best code model)')
    async def code_help(self, ctx, *, question: str):
        """
        Get coding help (prefers Granite, falls back to Claude)

        Usage: !code How do I read a JSON file in Python?
        """
        # Add personality guidelines for code responses
        enhanced_question = (
            f"[You are PhiGEN, created by JC and STRYK. Use Australian English. "
            f"Never mention being an AI/bot. Provide helpful code solutions.]\n\n{question}"
        )

        response, model_config = self.router.route(
            enhanced_question,
            task_type="code"
        )

        embed = discord.Embed(
            title=f"💻 Code Help - {model_config.display_name}",
            description=f"```\n{response[:1900]}\n```",
            color=discord.Color.blue()
        )

        await ctx.send(embed=embed)

    @commands.command(name='models', help='List available AI models')
    async def list_models(self, ctx):
        """
        Show all available models and their status

        Usage: !models
        """
        status = self.router.get_status()

        embed = discord.Embed(
            title="🤖 Available AI Models",
            description="Status of all configured models",
            color=discord.Color.purple()
        )

        for model_name, info in status.items():
            status_icon = "✅" if info['available'] else "❌"
            local_icon = "🏠 Local" if info['local'] else "☁️ Cloud"
            cost = "FREE" if info['cost_per_1m'] == 0 else f"${info['cost_per_1m']}/1M tokens"

            embed.add_field(
                name=f"{status_icon} {info['name']}",
                value=f"{local_icon} | {cost}\nProvider: {info['provider']}",
                inline=True
            )

        await ctx.send(embed=embed)

    @commands.command(name='stats', help='Show AI usage statistics')
    async def show_stats(self, ctx):
        """
        Show usage statistics and cost savings

        Usage: !stats
        """
        stats = self.router.get_stats()

        embed = discord.Embed(
            title="📊 AI Usage Statistics",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="Total Requests",
            value=str(stats['total_requests']),
            inline=True
        )

        embed.add_field(
            name="Estimated Savings",
            value=f"${stats['estimated_savings']:.2f}",
            inline=True
        )

        # Add breakdown by model
        breakdown = "\n".join([
            f"**{model}**: {count} requests"
            for model, count in stats['by_model'].items()
        ])

        embed.add_field(
            name="Usage Breakdown",
            value=breakdown or "No usage yet",
            inline=False
        )

        embed.set_footer(text="Savings calculated vs. using Claude API for all requests")

        await ctx.send(embed=embed)

    @commands.command(name='stats_conv', help='Show conversation learning statistics')
    async def show_conversation_stats(self, ctx):
        """
        Show conversation logging statistics

        Usage: !stats_conv
        """
        stats = self.conversation_logger.get_stats()

        embed = discord.Embed(
            title="💬 Conversation Learning Stats",
            description="The bot logs conversations to learn your communication style",
            color=discord.Color.purple()
        )

        embed.add_field(
            name="Total Messages Logged",
            value=str(stats.get('total_logged', 0)),
            inline=True
        )

        embed.add_field(
            name="Log File Size",
            value=f"{stats.get('file_size_kb', 0)} KB",
            inline=True
        )

        embed.add_field(
            name="Log Location",
            value="`conversation_history.jsonl`",
            inline=False
        )

        embed.set_footer(text="Use !learn_patterns to see what the bot has learned")

        await ctx.send(embed=embed)

    @commands.command(name='learn_patterns', help='Show learned communication patterns')
    async def show_learned_patterns(self, ctx):
        """
        Analyze and show learned patterns from conversations

        Usage: !learn_patterns
        """
        # Analyze recent conversations
        analysis = self.conversation_logger.analyze_patterns(limit=500)

        if analysis['total_messages'] == 0:
            await ctx.send("📊 No conversation data yet. Start chatting with the bot!")
            return

        embed = discord.Embed(
            title="🧠 Learned Communication Patterns",
            description=f"Analysis of last {analysis['total_messages']} messages",
            color=discord.Color.blue()
        )

        # Show most common words/slang
        if analysis['common_words']:
            common_words = ", ".join([f"`{word}`" for word, _ in analysis['common_words'][:10]])
            embed.add_field(
                name="Frequently Used Terms",
                value=common_words,
                inline=False
            )

        # Show active users
        if analysis['active_users']:
            active_users = "\n".join([
                f"{name}: {count} messages"
                for name, count in analysis['active_users'][:5]
            ])
            embed.add_field(
                name="Most Active Users",
                value=active_users,
                inline=False
            )

        embed.add_field(
            name="User Messages",
            value=str(analysis['user_messages']),
            inline=True
        )

        embed.set_footer(text="This helps the bot understand your server's unique communication style")

        await ctx.send(embed=embed)

    @commands.command(name='context', help='Show recent conversation context')
    async def show_context(self, ctx):
        """
        Show recent conversation context used by the bot

        Usage: !context
        """
        recent = self.conversation_logger.get_recent_context(
            channel_id=ctx.channel.id,
            limit=10
        )

        if not recent:
            await ctx.send("📝 No conversation history in this channel yet.")
            return

        embed = discord.Embed(
            title=f"📝 Recent Context - #{ctx.channel.name}",
            description=f"Last {len(recent)} messages the bot uses for context",
            color=discord.Color.teal()
        )

        # Show last few exchanges
        for entry in recent[-5:]:
            user_msg = entry.get('message', '')[:100]
            bot_resp = entry.get('bot_response', '')[:100] if entry.get('bot_response') else 'N/A'

            embed.add_field(
                name=f"{entry.get('user_name', 'User')}",
                value=f"**Q:** {user_msg}\n**A:** {bot_resp}",
                inline=False
            )

        embed.set_footer(text="This context helps the bot maintain conversation continuity")

        await ctx.send(embed=embed)

    @commands.command(name='switch', help='Switch your default model')
    async def switch_model(self, ctx, model_name: str):
        """
        Switch your preferred default model

        Usage: !switch mistral
        """
        model_name = model_name.lower()

        if model_name not in self.router.MODELS:
            available = ", ".join(self.router.MODELS.keys())
            await ctx.send(f"❌ Unknown model. Available: {available}")
            return

        user_id = ctx.author.id
        self.user_preferences[user_id] = model_name

        model_config = self.router.MODELS[model_name]
        await ctx.send(
            f"✅ Switched to **{model_config.display_name}**\n"
            f"Your !ai commands will now use this model by default."
        )

    @commands.command(name='help_ai', help='Show AI bot help and examples')
    async def help_ai(self, ctx):
        """
        Show detailed help for AI commands

        Usage: !help_ai
        """
        embed = discord.Embed(
            title="🤖 AI Bot Help",
            description="Multi-model AI with smart routing",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="⚡ Quick Settings (NEW!)",
            value="""
`!m <model>` - Switch model (!m phi | !m granite)
`!temp=50` - Set creativity (1-100 or robot/creative)
`!len=50` - Set response length (1-100 or brief/detailed)
`!cfg show` - View all your settings
`!profile save <name>` - Save settings as profile
            """,
            inline=False
        )

        embed.add_field(
            name="📝 Basic Commands",
            value="""
`!ai <question>` - Ask AI (uses your active model)
`!mistral <question>` - Fast, conversational
`!granite <question>` - Code-optimized
`!claude <question>` - Most powerful ($$)
`!best <question>` - Auto-pick best model
            """,
            inline=False
        )

        embed.add_field(
            name="🔍 Advanced",
            value="""
`!compare <question>` - Ask all models
`!code <question>` - Coding help
`!models` - List all models
`!stats` - Usage statistics
            """,
            inline=False
        )

        embed.add_field(
            name="🛠️ Custom Commands",
            value="""
`!create_command <name> <desc>` - Create new command
`!list_custom` - List custom commands
`!view_command <name>` - View command code
`!remove_command <name>` - Remove command
            """,
            inline=False
        )

        embed.add_field(
            name="🤖 Auto-Response",
            value="""
`!auto_on` - Enable auto-reply in channel
`!auto_off` - Disable auto-reply
`!auto_status` - Check status
            """,
            inline=False
        )

        embed.add_field(
            name="🖥️ Desktop Control",
            value="""
`!dc <message>` - Send to Claude Code window
            """,
            inline=False
        )

        embed.add_field(
            name="🧠 Conversation Learning",
            value="""
`!stats_conv` - View conversation logs
`!learn_patterns` - See learned patterns
`!context` - Show recent context
            """,
            inline=False
        )

        embed.add_field(
            name="📊 Response Quality (React to teach bot)",
            value="""
`!scrape_history [count]` - Backfill message history
`!show_feedback` - View quality statistics
`!best_responses` - See good examples
`!worst_responses` - See bad examples
React with ✅❌☠️ on bot messages to teach it
            """,
            inline=False
        )

        embed.add_field(
            name="🔍 RAG System (NEW! Semantic Search)",
            value="""
`!index_rag` - Index conversation history for RAG
`!rag_stats` - View RAG statistics
`!rag_search <query>` - Search past conversations
`!rag_toggle` - Enable/disable RAG
Bot automatically finds relevant past examples!
            """,
            inline=False
        )

        embed.add_field(
            name="💡 Examples",
            value="""
`!ai What is Docker?`
`!granite Review my Python code`
`!claude Explain quantum computing`
`!compare Best way to learn AI?`
`!code Read JSON in Python`
            """,
            inline=False
        )

        embed.set_footer(text="💰 Local models are FREE | Claude costs $$ | 🧠 Bot learns from conversations")

        await ctx.send(embed=embed)

    @commands.command(name='create_command', help='Create a new bot command using AI')
    async def create_command(self, ctx, command_name: str, *, description: str):
        """
        Create a new Discord command using Granite's coding abilities

        Usage: !create_command greet Send a friendly greeting to the user
        Usage: !create_command joke Tell a random programming joke
        """
        # Validate command name
        if not command_name.isalnum():
            await ctx.send("❌ Command name must be alphanumeric (no spaces or special chars)")
            return

        if command_name in ['help', 'help_ai'] or hasattr(self, f'ask_{command_name}'):
            await ctx.send(f"❌ Command `{command_name}` already exists!")
            return

        await ctx.send(f"🔨 Using Granite to implement `!{command_name}`...")

        try:
            # Use Granite to generate the command code
            prompt = f"""Create a Discord bot command function in Python.

Command name: {command_name}
Description: {description}

Requirements:
1. Function must be named `custom_{command_name}`
2. Must be async and take (self, ctx, *args) parameters
3. Use ctx.send() to reply to the user
4. Be creative and functional
5. Keep it safe - no file operations, no system calls
6. Return ONLY the Python function code, no explanations

Example format:
async def custom_greet(self, ctx, *args):
    user = ctx.author.mention
    await ctx.send(f"Hello {{user}}! 👋")

Now generate the function for: {command_name} - {description}"""

            async with ctx.typing():
                code, model = self.router.route(prompt, model="granite")

            # Extract code block if wrapped in markdown
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].split("```")[0].strip()

            # Show generated code for approval
            embed = discord.Embed(
                title=f"💻 Generated Code for !{command_name}",
                description=f"```python\n{code[:1900]}\n```",
                color=discord.Color.green()
            )
            embed.set_footer(text="React with ✅ to approve or ❌ to cancel (30s)")

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")

            # Wait for user reaction
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == msg.id

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)

                if str(reaction.emoji) == "✅":
                    # Approve and install command
                    self._install_custom_command(command_name, description, code)
                    await ctx.send(f"✅ Command `!{command_name}` installed! Try it now!")
                else:
                    await ctx.send("❌ Command creation cancelled.")

            except asyncio.TimeoutError:
                await ctx.send("⏱️ Timeout - command not installed.")

        except Exception as e:
            logger.error(f"Error creating command: {e}")
            await ctx.send(f"❌ Error creating command: {str(e)}")

    @commands.command(name='list_custom', help='List all custom commands')
    async def list_custom_commands(self, ctx):
        """
        Show all custom commands created with !create_command

        Usage: !list_custom
        """
        if not self.custom_commands:
            await ctx.send("No custom commands yet! Use `!create_command` to create one.")
            return

        embed = discord.Embed(
            title="🛠️ Custom Commands",
            description="Commands created with AI",
            color=discord.Color.orange()
        )

        for name, info in self.custom_commands.items():
            embed.add_field(
                name=f"!{name}",
                value=info['description'],
                inline=False
            )

        embed.set_footer(text=f"Total: {len(self.custom_commands)} commands")
        await ctx.send(embed=embed)

    @commands.command(name='remove_command', help='Remove a custom command')
    async def remove_custom_command(self, ctx, command_name: str):
        """
        Remove a custom command

        Usage: !remove_command greet
        """
        if command_name not in self.custom_commands:
            await ctx.send(f"❌ Custom command `{command_name}` doesn't exist.")
            return

        del self.custom_commands[command_name]
        self._save_custom_commands()

        # Remove from bot
        command = self.bot.get_command(command_name)
        if command:
            self.bot.remove_command(command_name)

        await ctx.send(f"✅ Removed custom command `!{command_name}`")

    @commands.command(name='view_command', help='View the code for a custom command')
    async def view_command_code(self, ctx, command_name: str):
        """
        View the source code of a custom command

        Usage: !view_command greet
        """
        if command_name not in self.custom_commands:
            await ctx.send(f"❌ Custom command `{command_name}` doesn't exist.")
            return

        info = self.custom_commands[command_name]
        code = info['code']

        embed = discord.Embed(
            title=f"📄 Code for !{command_name}",
            description=f"```python\n{code[:1900]}\n```",
            color=discord.Color.blue()
        )
        embed.add_field(name="Description", value=info['description'])
        embed.set_footer(text=f"Created by AI (Granite)")

        await ctx.send(embed=embed)

    def _install_custom_command(self, name: str, description: str, code: str):
        """Install a custom command dynamically"""
        try:
            # Create a safe namespace for exec
            namespace = {
                'discord': discord,
                'asyncio': asyncio,
                'self': self,
            }

            # Execute the code to define the function
            exec(code, namespace)

            # Get the function
            func_name = f"custom_{name}"
            if func_name not in namespace:
                raise ValueError(f"Function {func_name} not found in generated code")

            custom_func = namespace[func_name]

            # Create Discord command dynamically
            @commands.command(name=name, help=description)
            async def dynamic_command(ctx, *args):
                try:
                    await custom_func(self, ctx, *args)
                except Exception as e:
                    await ctx.send(f"❌ Error in custom command: {str(e)}")

            # Add to bot
            self.bot.add_command(dynamic_command)

            # Store command info
            self.custom_commands[name] = {
                'description': description,
                'code': code
            }

            # Save to file
            self._save_custom_commands()

        except Exception as e:
            logger.error(f"Error installing command: {e}")
            raise

    def _load_custom_commands(self):
        """Load custom commands from file"""
        try:
            if self.custom_commands_file.exists():
                with open(self.custom_commands_file, 'r') as f:
                    saved_commands = json.load(f)

                # Reinstall each command
                for name, info in saved_commands.items():
                    try:
                        self._install_custom_command(name, info['description'], info['code'])
                        logger.info(f"Loaded custom command: {name}")
                    except Exception as e:
                        logger.error(f"Failed to load command {name}: {e}")

        except Exception as e:
            logger.error(f"Error loading custom commands: {e}")

    def _save_custom_commands(self):
        """Save custom commands to file"""
        try:
            with open(self.custom_commands_file, 'w') as f:
                json.dump(self.custom_commands, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving custom commands: {e}")

    def _load_auto_response_channels(self):
        """Load channels with auto-response enabled"""
        try:
            if self.auto_response_file.exists():
                with open(self.auto_response_file, 'r') as f:
                    channels = json.load(f)
                    self.auto_response_channels = set(channels)
                    logger.info(f"Loaded {len(channels)} auto-response channels")
        except Exception as e:
            logger.error(f"Error loading auto-response channels: {e}")

    def _save_auto_response_channels(self):
        """Save auto-response channel list"""
        try:
            with open(self.auto_response_file, 'w') as f:
                json.dump(list(self.auto_response_channels), f, indent=2)
        except Exception as e:
            logger.error(f"Error saving auto-response channels: {e}")

    @commands.command(name='auto_on', help='Enable auto-response in this channel')
    @commands.has_permissions(manage_channels=True)
    async def enable_auto_response(self, ctx):
        """
        Enable automatic responses to all messages in this channel

        Usage: !auto_on
        Note: Requires Manage Channels permission
        """
        channel_id = ctx.channel.id

        if channel_id in self.auto_response_channels:
            await ctx.send("✅ Auto-response is already enabled in this channel.")
            return

        self.auto_response_channels.add(channel_id)
        self._save_auto_response_channels()

        await ctx.send(
            f"✅ **Auto-response enabled!**\n"
            f"I'll now respond to all messages in {ctx.channel.mention}\n"
            f"Using: **Phi 3.5 Mini** (fast & efficient)\n"
            f"To disable: `!auto_off`"
        )

    @commands.command(name='auto_off', help='Disable auto-response in this channel')
    @commands.has_permissions(manage_channels=True)
    async def disable_auto_response(self, ctx):
        """
        Disable automatic responses in this channel

        Usage: !auto_off
        Note: Requires Manage Channels permission
        """
        channel_id = ctx.channel.id

        if channel_id not in self.auto_response_channels:
            await ctx.send("ℹ️ Auto-response is not enabled in this channel.")
            return

        self.auto_response_channels.remove(channel_id)
        self._save_auto_response_channels()

        await ctx.send(f"✅ Auto-response disabled in {ctx.channel.mention}")

    @commands.command(name='auto_status', help='Check auto-response status')
    async def auto_response_status(self, ctx):
        """
        Show auto-response status for this channel

        Usage: !auto_status
        """
        channel_id = ctx.channel.id
        enabled = channel_id in self.auto_response_channels

        embed = discord.Embed(
            title="🤖 Auto-Response Status",
            color=discord.Color.green() if enabled else discord.Color.grey()
        )

        embed.add_field(
            name="This Channel",
            value="✅ Enabled" if enabled else "❌ Disabled",
            inline=False
        )

        if enabled:
            embed.add_field(
                name="Model",
                value="Phi 3.5 Mini (Fast & Efficient)",
                inline=False
            )
            embed.add_field(
                name="Disable",
                value="`!auto_off`",
                inline=False
            )
        else:
            embed.add_field(
                name="Enable",
                value="`!auto_on` (requires Manage Channels permission)",
                inline=False
            )

        total_channels = len(self.auto_response_channels)
        embed.set_footer(text=f"Total auto-response channels: {total_channels}")

        await ctx.send(embed=embed)

    @commands.command(name='scrape_history', help='Scrape channel message history and log it')
    @commands.has_permissions(manage_channels=True)
    async def scrape_channel_history(self, ctx, message_count: int = 1000, offset: int = 0):
        """
        Scrape historical messages from channel and log them

        Usage:
            !scrape_history 1000          - Scrape last 1000 messages
            !scrape_history 5000 5000     - Skip first 5000, scrape next 5000
        Note: Max 10000 messages per scrape, requires Manage Channels permission
        """
        if message_count > 10000:
            await ctx.send("❌ Maximum is 10,000 messages per scrape")
            return

        if message_count < 1:
            await ctx.send("❌ Must scrape at least 1 message")
            return

        if offset < 0:
            await ctx.send("❌ Offset cannot be negative")
            return

        # Send initial progress message
        if offset > 0:
            progress_msg = await ctx.send(f"🔍 Skipping {offset} messages, then scraping {message_count} from {ctx.channel.mention}...")
        else:
            progress_msg = await ctx.send(f"🔍 Scraping last {message_count} messages from {ctx.channel.mention}...")

        try:
            scraped_count = 0
            skipped_count = 0
            user_msg_count = 0
            bot_msg_count = 0

            # Fetch messages in batches (need offset + count total)
            total_to_fetch = offset + message_count
            async for msg in ctx.channel.history(limit=total_to_fetch, oldest_first=False):
                # Skip offset messages first
                if skipped_count < offset:
                    skipped_count += 1
                    continue

                # Skip command messages
                if msg.content.startswith('!'):
                    continue

                # Log the message
                is_bot = msg.author.bot
                self.feedback_tracker.log_message(
                    author=msg.author.name,
                    message=msg.content,
                    is_bot=is_bot,
                    message_id=None  # Historical messages don't need reaction tracking
                )

                scraped_count += 1
                if is_bot:
                    bot_msg_count += 1
                else:
                    user_msg_count += 1

                # Update progress every 100 messages
                if scraped_count % 100 == 0:
                    await progress_msg.edit(content=f"🔍 Scraping... {scraped_count}/{message_count}")

                # Stop when we've scraped enough
                if scraped_count >= message_count:
                    break

            # Final summary
            embed = discord.Embed(
                title="✅ Scrape Complete!",
                description=f"Historical messages logged to `conversation_full_log.txt`",
                color=discord.Color.green()
            )

            embed.add_field(name="Total Messages", value=str(scraped_count), inline=True)
            embed.add_field(name="User Messages", value=str(user_msg_count), inline=True)
            embed.add_field(name="Bot Messages", value=str(bot_msg_count), inline=True)

            if offset > 0:
                embed.add_field(name="Offset", value=f"Skipped {offset} messages", inline=False)

            embed.set_footer(text="Bot will now learn from reactions on new messages")

            await progress_msg.edit(content="", embed=embed)

            logger.info(f"Scraped {scraped_count} messages from {ctx.channel.name} (offset: {offset})")

        except Exception as e:
            logger.error(f"Error scraping history: {e}")
            await progress_msg.edit(content=f"❌ Error scraping history: {str(e)}")

    @commands.command(name='show_feedback', help='Show response quality statistics')
    async def show_feedback_stats(self, ctx):
        """
        Show statistics about response quality feedback

        Usage: !show_feedback
        """
        stats = self.feedback_tracker.get_feedback_stats()

        total_reactions = stats['total_good'] + stats['total_bad'] + stats['total_very_bad']

        embed = discord.Embed(
            title="📊 Response Quality Feedback",
            description="Learning from your reactions to improve responses",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="✅ Good Responses",
            value=f"{stats['total_good']} reactions\n{stats['good_examples_count']} examples stored",
            inline=True
        )

        embed.add_field(
            name="❌ Bad Responses",
            value=f"{stats['total_bad']} reactions\n{stats['bad_examples_count']} examples stored",
            inline=True
        )

        embed.add_field(
            name="☠️ Very Bad Responses",
            value=f"{stats['total_very_bad']} reactions\n{stats['very_bad_examples_count']} examples stored",
            inline=True
        )

        if total_reactions > 0:
            good_pct = (stats['total_good'] / total_reactions) * 100
            embed.add_field(
                name="Overall Quality Score",
                value=f"{good_pct:.1f}% positive",
                inline=False
            )

        embed.set_footer(text="React with ✅/❌/☠️ to bot messages to teach it | Use !best_responses and !worst_responses")

        await ctx.send(embed=embed)

    @commands.command(name='best_responses', help='Show examples of good responses')
    async def show_best_responses(self, ctx):
        """
        Show responses that got positive reactions

        Usage: !best_responses
        """
        responses = self.feedback_tracker.get_all_responses_by_quality()
        good = responses['good']

        if not good:
            await ctx.send("📊 No good responses yet. React with ✅ to bot messages you like!")
            return

        embed = discord.Embed(
            title="✅ Best Responses (Got Positive Reactions)",
            description="These response patterns were well-received",
            color=discord.Color.green()
        )

        # Show last 5
        for i, response in enumerate(good[-5:], 1):
            truncated = response[:200] + "..." if len(response) > 200 else response
            embed.add_field(
                name=f"Example {i}",
                value=f"```{truncated}```",
                inline=False
            )

        embed.set_footer(text=f"Total good responses: {len(good)} | Bot uses these as examples")

        await ctx.send(embed=embed)

    @commands.command(name='worst_responses', help='Show examples of bad responses')
    async def show_worst_responses(self, ctx):
        """
        Show responses that got negative reactions

        Usage: !worst_responses
        """
        responses = self.feedback_tracker.get_all_responses_by_quality()
        bad = responses['bad']
        very_bad = responses['very_bad']

        if not bad and not very_bad:
            await ctx.send("📊 No bad responses recorded yet.")
            return

        embed = discord.Embed(
            title="❌ Worst Responses (Got Negative Reactions)",
            description="These response patterns should be avoided",
            color=discord.Color.red()
        )

        # Show very bad first
        if very_bad:
            embed.add_field(
                name="☠️ Very Bad Examples",
                value=f"{len(very_bad)} responses",
                inline=False
            )
            for i, response in enumerate(very_bad[-3:], 1):
                truncated = response[:150] + "..." if len(response) > 150 else response
                embed.add_field(
                    name=f"Very Bad #{i}",
                    value=f"```{truncated}```",
                    inline=False
                )

        # Then bad
        if bad:
            embed.add_field(
                name="❌ Bad Examples",
                value=f"{len(bad)} responses",
                inline=False
            )
            for i, response in enumerate(bad[-2:], 1):
                truncated = response[:150] + "..." if len(response) > 150 else response
                embed.add_field(
                    name=f"Bad #{i}",
                    value=f"```{truncated}```",
                    inline=False
                )

        embed.set_footer(text="Bot learns to avoid these patterns")

        await ctx.send(embed=embed)

    # ===== RAG (Retrieval-Augmented Generation) Commands =====

    @commands.command(name='index_rag', help='Index conversation history for RAG search')
    @commands.has_permissions(manage_channels=True)
    async def index_rag(self, ctx, force_rebuild: str = "false"):
        """
        Index conversation history into RAG system

        Usage:
            !index_rag             - Index if not already done
            !index_rag true        - Force rebuild index
        """
        rebuild = force_rebuild.lower() in ['true', 'yes', '1', 'force']

        status_msg = await ctx.send("🔍 Indexing conversation history for RAG...")

        try:
            # Index in background
            await asyncio.to_thread(self.rag.index_conversations, force_rebuild=rebuild)

            stats = self.rag.get_stats()

            embed = discord.Embed(
                title="✅ RAG Index Complete",
                description="Conversation history indexed for semantic search",
                color=discord.Color.green()
            )

            embed.add_field(
                name="Total Examples",
                value=str(stats['total_examples']),
                inline=True
            )
            embed.add_field(
                name="✅ Good",
                value=str(stats['good_examples']),
                inline=True
            )
            embed.add_field(
                name="❌ Bad",
                value=str(stats['bad_examples']),
                inline=True
            )

            embed.set_footer(text="Bot will now use RAG to find relevant past conversations")

            await status_msg.edit(content="", embed=embed)

        except Exception as e:
            logger.error(f"Error indexing RAG: {e}")
            await status_msg.edit(content=f"❌ Error indexing: {str(e)}")

    @commands.command(name='rag_stats', help='Show RAG system statistics')
    async def rag_stats(self, ctx):
        """
        Show RAG system stats

        Usage: !rag_stats
        """
        try:
            stats = self.rag.get_stats()

            embed = discord.Embed(
                title="🔍 RAG System Statistics",
                description="Semantic search over conversation history",
                color=discord.Color.blue()
            )

            embed.add_field(
                name="Indexed Examples",
                value=f"{stats['total_examples']} conversations",
                inline=False
            )

            if stats['total_examples'] > 0:
                embed.add_field(
                    name="✅ Good Quality",
                    value=str(stats['good_examples']),
                    inline=True
                )
                embed.add_field(
                    name="❌ Bad Quality",
                    value=str(stats['bad_examples']),
                    inline=True
                )
                embed.add_field(
                    name="⚪ Neutral",
                    value=str(stats['neutral_examples']),
                    inline=True
                )

            embed.add_field(
                name="Status",
                value="✅ Enabled" if self.rag_enabled else "❌ Disabled",
                inline=False
            )

            embed.set_footer(text="Use !index_rag to index scraped conversations")

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error getting RAG stats: {e}")
            await ctx.send(f"❌ Error: {str(e)}")

    @commands.command(name='rag_toggle', help='Toggle RAG on/off')
    @commands.has_permissions(manage_channels=True)
    async def rag_toggle(self, ctx):
        """
        Enable or disable RAG

        Usage: !rag_toggle
        """
        self.rag_enabled = not self.rag_enabled
        status = "✅ Enabled" if self.rag_enabled else "❌ Disabled"
        await ctx.send(f"🔍 RAG system: {status}")

    @commands.command(name='rag_search', help='Search conversation history')
    async def rag_search(self, ctx, *, query: str):
        """
        Search for similar past conversations

        Usage: !rag_search how do I fix Docker errors?
        """
        try:
            results = self.rag.search_similar(query, top_k=3)

            if not results:
                await ctx.send("🔍 No similar conversations found. Try indexing with !index_rag")
                return

            embed = discord.Embed(
                title=f"🔍 Similar Conversations",
                description=f"Found {len(results)} relevant examples",
                color=discord.Color.blue()
            )

            for i, result in enumerate(results, 1):
                reaction_emoji = {
                    'GOOD': '✅',
                    'BAD': '❌',
                    'VERY_BAD': '💀',
                    'NONE': '⚪'
                }.get(result['reaction'], '⚪')

                similarity_pct = result['similarity'] * 100

                embed.add_field(
                    name=f"{reaction_emoji} Example {i} (Similarity: {similarity_pct:.0f}%)",
                    value=(
                        f"**User:** {result['user_message'][:100]}...\n"
                        f"**Bot:** {result['bot_response'][:100]}..."
                    ),
                    inline=False
                )

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in RAG search: {e}")
            await ctx.send(f"❌ Error: {str(e)}")

    # ===== PHASE 1: Advanced Command System =====

    @commands.command(name='m', help='Switch AI model (!m phi | !m mistral | !m granite | !m claude)')
    async def switch_model(self, ctx, model: str = None):
        """
        Switch active AI model

        Usage:
            !m              - Show current model
            !m phi          - Switch to Phi 3.5 Mini (fast)
            !m mistral      - Switch to Mistral 7B (balanced)
            !m granite      - Switch to Granite Code (code-focused)
            !m claude       - Switch to Claude Sonnet (powerful)

        Aliases: !m p, !m ms, !m g, !m c
        """
        user_id = ctx.author.id

        if not model:
            # Show current model
            settings = self.settings_manager.get_user_settings(user_id)
            current = settings.get('model', 'phi')
            model_info = self.router.MODELS.get(current)

            if model_info:
                embed = discord.Embed(
                    title="🤖 Current Model",
                    description=f"**{model_info.display_name}**",
                    color=discord.Color.blue()
                )
                embed.add_field(name="Provider", value=model_info.provider, inline=True)
                embed.add_field(name="Type", value="Local" if model_info.is_local else "Cloud", inline=True)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Current model: {current}")
            return

        # Resolve alias
        model = self.settings_manager.resolve_model_alias(model)

        # Validate model
        if model not in self.router.MODELS:
            available = ", ".join(self.router.MODELS.keys())
            await ctx.send(f"❌ Unknown model. Available: {available}\nAliases: p, ms, g, c")
            return

        # Update user settings
        self.settings_manager.update_user_setting(user_id, 'model', model)

        model_config = self.router.MODELS[model]
        await ctx.send(f"✅ Switched to **{model_config.display_name}**")

    @commands.command(name='temp', help='Set temperature (!temp=50 | !temp creative)')
    async def set_temperature(self, ctx, *, value: str = None):
        """
        Set response creativity/temperature

        Usage:
            !temp              - Show current temperature
            !temp=50           - Set numeric value (1-100)
            !temp robot        - Ultra-focused (1)
            !temp focused      - Clear & direct (25)
            !temp balanced     - Default (50)
            !temp creative     - Exploratory (75)
            !temp wild         - Experimental (100)
        """
        user_id = ctx.author.id

        # Parse value from message if = syntax used
        if not value and '=' in ctx.message.content:
            value = ctx.message.content.split('=', 1)[1].strip()

        if not value:
            # Show current temperature
            settings = self.settings_manager.get_user_settings(user_id)
            temp = settings.get('temperature', 50)
            await ctx.send(f"🌡️ Current temperature: {temp}/100")
            return

        # Try numeric
        if value.isdigit():
            temp = int(value)
            if temp < 1 or temp > 100:
                await ctx.send("❌ Temperature must be between 1 and 100")
                return
        else:
            # Try preset
            temp = self.settings_manager.resolve_temp_preset(value)
            if temp is None:
                presets = ", ".join(self.settings_manager.get_all_presets()['temperature'].keys())
                await ctx.send(f"❌ Unknown preset. Available: {presets}")
                return

        self.settings_manager.update_user_setting(user_id, 'temperature', temp)
        await ctx.send(f"🌡️ Temperature set to {temp}/100")

    @commands.command(name='len', help='Set response length (!len=50 | !len brief)')
    async def set_length(self, ctx, *, value: str = None):
        """
        Set response length

        Usage:
            !len              - Show current length
            !len=50           - Set numeric value (1-100)
            !len brief        - Short responses (10)
            !len normal       - Medium responses (50)
            !len detailed     - Long responses (100)
        """
        user_id = ctx.author.id

        # Parse value from message if = syntax used
        if not value and '=' in ctx.message.content:
            value = ctx.message.content.split('=', 1)[1].strip()

        if not value:
            # Show current length
            settings = self.settings_manager.get_user_settings(user_id)
            length = settings.get('length', 50)
            await ctx.send(f"📏 Current length: {length}/100")
            return

        # Try numeric
        if value.isdigit():
            length = int(value)
            if length < 1 or length > 100:
                await ctx.send("❌ Length must be between 1 and 100")
                return
        else:
            # Try preset
            length = self.settings_manager.resolve_length_preset(value)
            if length is None:
                presets = ", ".join(self.settings_manager.get_all_presets()['length'].keys())
                await ctx.send(f"❌ Unknown preset. Available: {presets}")
                return

        self.settings_manager.update_user_setting(user_id, 'length', length)
        await ctx.send(f"📏 Length set to {length}/100")

    @commands.command(name='cfg', help='Configure multiple settings (!cfg m=granite temp=25 len=75)')
    async def configure(self, ctx, *, config: str = None):
        """
        Configure multiple settings at once

        Usage:
            !cfg show                          - Show all current settings
            !cfg reset                         - Reset to defaults
            !cfg m=granite temp=25 len=75      - Set multiple settings
        """
        user_id = ctx.author.id

        if not config or config.lower() == 'show':
            # Show all settings
            settings = self.settings_manager.get_user_settings(user_id)

            embed = discord.Embed(
                title="⚙️ Your Settings",
                color=discord.Color.blue()
            )

            embed.add_field(name="Model", value=settings.get('model', 'phi'), inline=True)
            embed.add_field(name="Temperature", value=f"{settings.get('temperature', 50)}/100", inline=True)
            embed.add_field(name="Length", value=f"{settings.get('length', 50)}/100", inline=True)
            embed.add_field(name="Tone", value=settings.get('tone', 'casual'), inline=True)
            embed.add_field(name="Context Window", value=settings.get('context_window', 15), inline=True)

            await ctx.send(embed=embed)
            return

        if config.lower() == 'reset':
            # Reset to defaults
            self.settings_manager.reset_user_settings(user_id)
            await ctx.send("✅ Settings reset to defaults")
            return

        # Parse multiple settings
        updates = {}
        parts = config.split()

        for part in parts:
            if '=' not in part:
                continue

            key, value = part.split('=', 1)
            key = key.lower().strip()
            value = value.strip()

            if key in ['m', 'model']:
                model = self.settings_manager.resolve_model_alias(value)
                if model in self.router.MODELS:
                    updates['model'] = model
            elif key in ['temp', 'temperature']:
                if value.isdigit():
                    updates['temperature'] = int(value)
                else:
                    temp = self.settings_manager.resolve_temp_preset(value)
                    if temp:
                        updates['temperature'] = temp
            elif key in ['len', 'length']:
                if value.isdigit():
                    updates['length'] = int(value)
                else:
                    length = self.settings_manager.resolve_length_preset(value)
                    if length:
                        updates['length'] = length
            elif key == 'tone':
                tone = self.settings_manager.resolve_tone_preset(value)
                if tone:
                    updates['tone'] = tone

        if updates:
            self.settings_manager.update_user_settings(user_id, updates)
            changes = ", ".join([f"{k}={v}" for k, v in updates.items()])
            await ctx.send(f"✅ Updated: {changes}")
        else:
            await ctx.send("❌ No valid settings found in command")

    @commands.command(name='profile', help='Manage settings profiles (!profile save coding | !profile load coding)')
    async def manage_profile(self, ctx, action: str = None, name: str = None):
        """
        Save and load settings profiles

        Usage:
            !profile list                - List all your profiles
            !profile save coding         - Save current settings as "coding"
            !profile load coding         - Load "coding" profile
            !profile delete coding       - Delete "coding" profile
        """
        user_id = ctx.author.id

        if not action or action.lower() == 'list':
            # List profiles
            profiles = self.settings_manager.list_profiles(user_id)

            if not profiles:
                await ctx.send("📁 No saved profiles. Use `!profile save <name>` to create one.")
                return

            profile_list = "\n".join([f"• `{p}`" for p in profiles])
            embed = discord.Embed(
                title="📁 Your Profiles",
                description=profile_list,
                color=discord.Color.green()
            )
            embed.set_footer(text="Use !profile load <name> to load a profile")
            await ctx.send(embed=embed)
            return

        if not name:
            await ctx.send("❌ Please specify a profile name")
            return

        if action.lower() == 'save':
            # Save current settings as profile
            success = self.settings_manager.save_profile(user_id, name)
            if success:
                await ctx.send(f"✅ Saved current settings as profile: `{name}`")
            else:
                await ctx.send("❌ Failed to save profile")

        elif action.lower() == 'load':
            # Load profile
            profile = self.settings_manager.load_profile(user_id, name)
            if profile:
                await ctx.send(f"✅ Loaded profile: `{name}`")
            else:
                await ctx.send(f"❌ Profile `{name}` not found")

        elif action.lower() == 'delete':
            # Delete profile
            success = self.settings_manager.delete_profile(user_id, name)
            if success:
                await ctx.send(f"✅ Deleted profile: `{name}`")
            else:
                await ctx.send(f"❌ Profile `{name}` not found")

        else:
            await ctx.send("❌ Unknown action. Use: save, load, delete, or list")

    @commands.command(name='send_to_dc', aliases=['dc'], help='Send message to Claude Code window (Desktop)')
    @commands.has_permissions(manage_channels=True)
    async def send_to_claude_code(self, ctx, *, message: str):
        """
        Send a message to Claude Code's desktop window via automation

        Usage: !send_to_dc Your message here
        Note: Writes trigger file for Windows script to execute macro
        """
        try:
            # Format the message with author info
            formatted_message = f"Message from {ctx.author.name} via Discord: {message}"

            # Write to trigger file (Windows script will pick this up)
            trigger_file = Path(__file__).parent.parent / "dc_message_trigger.txt"

            with open(trigger_file, 'w', encoding='utf-8') as f:
                f.write(formatted_message)

            embed = discord.Embed(
                title="📤 Sending to Claude Code",
                description=f"Trigger file created for Windows automation",
                color=discord.Color.green()
            )

            embed.add_field(
                name="From",
                value=ctx.author.name,
                inline=True
            )

            embed.add_field(
                name="Message",
                value=message[:100] + ("..." if len(message) > 100 else ""),
                inline=False
            )

            embed.set_footer(text="Windows script will execute: Win+R → DC(DESKC) → Type message → Send")

            await ctx.send(embed=embed)

            logger.info(f"Trigger file created for Claude Code from {ctx.author.name}: {message[:50]}")

        except Exception as e:
            logger.error(f"Error creating trigger file: {e}")
            await ctx.send(f"❌ Error creating trigger file: {str(e)}")

    def _analyze_message_length(self, message: str) -> str:
        """Analyze message to determine response length constraint"""
        words = message.split()
        word_count = len(words)
        msg_lower = message.lower().strip()

        # Very short greetings - be super brief
        short_greetings = ['hello', 'hi', 'hey', 'sup', 'yo', 'heya', 'hey bro', 'hey mate', 'g\'day']
        if any(greeting in msg_lower for greeting in short_greetings) and word_count <= 3:
            return "GREETING"  # Just "Hey!" or "What's up?"

        # Acknowledgments
        acknowledgments = ['yes', 'no', 'ok', 'okay', 'thanks', 'ty', 'thx', 'yeah', 'nah', 'yep', 'nope', 'cool', 'nice']
        if any(ack in msg_lower for ack in acknowledgments) and word_count <= 2:
            return "VERY_SHORT"  # 1-2 words max

        # Short messages
        if word_count <= 10:
            return "SHORT"  # 1 sentence max

        # Medium messages
        if word_count <= 30:
            return "MEDIUM"  # 2 sentences max

        # Long/complex messages
        return "LONG"  # Can be detailed

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Listen for reactions on bot messages to learn response quality"""
        # Ignore bot's own reactions
        if user.bot:
            return

        # Only track reactions on bot's messages
        if reaction.message.author != self.bot.user:
            return

        # Get the emoji
        emoji = str(reaction.emoji)

        # Check if it's a tracked reaction
        all_tracked = (self.feedback_tracker.GOOD_REACTIONS +
                      self.feedback_tracker.BAD_REACTIONS +
                      self.feedback_tracker.VERY_BAD_REACTIONS)

        if emoji in all_tracked:
            # Get the bot's response text
            bot_response = reaction.message.content

            # Add to feedback tracker
            self.feedback_tracker.add_reaction(
                message_id=reaction.message.id,
                reaction=emoji,
                bot_response=bot_response
            )

            logger.info(f"Feedback recorded: {emoji} on message {reaction.message.id}")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Listen to all messages for auto-response and logging"""
        # Log ALL messages (users and bot) in auto-response channels
        if message.channel.id in self.auto_response_channels and not message.content.startswith('!'):
            is_bot_msg = message.author.bot and message.author == self.bot.user
            self.feedback_tracker.log_message(
                author=message.author.name,
                message=message.content,
                is_bot=is_bot_msg,
                message_id=message.id if is_bot_msg else None
            )

        # Ignore bot's own messages for response
        if message.author.bot:
            return

        # Ignore messages that are commands
        if message.content.startswith('!'):
            return

        # Check if this channel has auto-response enabled
        if message.channel.id not in self.auto_response_channels:
            return

        # Don't respond to empty messages
        if not message.content.strip():
            return

        try:
            # Show typing indicator
            async with message.channel.typing():
                # Analyze message length
                length_category = self._analyze_message_length(message.content)

                # Build learned feedback context
                learning_context = self.feedback_tracker.build_learning_context()

                # Detect gaming context
                gaming_context = self.personality.detect_gaming_context(message.content)

                # Build enhanced personality prompt (data-driven from 85k message analysis)
                prompt_with_context = self.personality.build_personality_prompt(
                    message_length=length_category,
                    context=learning_context if learning_context else "",
                    gaming_context=gaming_context
                )

                # Add RAG context (similar past conversations)
                if self.rag_enabled:
                    try:
                        rag_context = self.rag.build_rag_context(message.content, max_examples=3)
                        if rag_context:
                            prompt_with_context += f"\n{rag_context}\n"
                    except Exception as e:
                        logger.warning(f"RAG context generation failed: {e}")

                # Add current message
                prompt_with_context += f"\nUser message from {message.author.name}: {message.content}"

                # Use Phi 3.5 for fast responses
                response, model = self.router.route(
                    prompt_with_context,
                    model="phi",
                    task_type="chat"
                )

                # Apply personality post-processing (contractions, Aussie flavor, reactivity)
                response = self.personality.post_process_response(
                    response,
                    message.content,
                    add_aussie=True,
                    add_reactivity=True
                )

                # Truncate if too long (Discord limit: 2000 chars)
                if len(response) > 2000:
                    response = response[:1997] + "..."

                # Log the conversation for learning (JSONL format)
                self.conversation_logger.log_message(
                    channel_id=message.channel.id,
                    channel_name=message.channel.name,
                    user_id=message.author.id,
                    user_name=message.author.name,
                    message=message.content,
                    bot_response=response,
                    model_used="phi"
                )

                # Reply to the message
                bot_message = await message.reply(response, mention_author=False)

                # Log bot's response in simple format (with message ID for reaction tracking)
                self.feedback_tracker.log_message(
                    author="PhiGEN",
                    message=response,
                    is_bot=True,
                    message_id=bot_message.id
                )

        except Exception as e:
            logger.error(f"Error in auto-response: {e}")
            # Silently fail - don't spam error messages

    async def _generate_response(self, ctx, question: str, model: str):
        """Helper to generate and send response"""
        try:
            # Show typing indicator
            async with ctx.typing():
                # Check if model is available
                model_config = self.router.MODELS.get(model)
                if not model_config:
                    await ctx.send(f"❌ Unknown model: {model}")
                    return

                if not self.router._is_available(model_config):
                    await ctx.send(
                        f"❌ {model_config.display_name} is not available.\n"
                        f"Run: `docker-compose --profile ai up -d`"
                    )
                    return

                # Add personality and guidelines to the question
                enhanced_question = (
                    f"[Communication Guidelines: You are PhiGEN, created by JC and STRYK. "
                    f"Use Australian English naturally. Never mention being an AI, bot, or assistant. "
                    f"Respond like a knowledgeable person would.]\n\n"
                    f"User question: {question}"
                )

                # Generate response
                response, used_model = self.router.route(enhanced_question, model=model)

                # Create embed
                embed = discord.Embed(
                    title=f"🤖 {used_model.display_name}",
                    description=response[:4000],
                    color=self._get_model_color(model)
                )

                cost_info = "FREE (local)" if used_model.is_local else "Costs $$"
                embed.set_footer(text=f"{cost_info} | {used_model.provider}")

                await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in _generate_response: {e}")
            await ctx.send(f"❌ Error: {str(e)}")

    def _get_model_color(self, model_name: str) -> discord.Color:
        """Get color for model embed"""
        colors = {
            "mistral": discord.Color.blue(),
            "granite": discord.Color.green(),
            "claude": discord.Color.purple()
        }
        return colors.get(model_name, discord.Color.greyple())


async def setup(bot):
    """Setup function for Discord bot cog"""
    await bot.add_cog(MultiModelAI(bot))


def create_multimodel_bot(token: str) -> commands.Bot:
    """
    Create Discord bot with multi-model AI

    Args:
        token: Discord bot token

    Returns:
        Configured bot
    """
    intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f'🤖 Multi-Model Bot logged in as {bot.user}')
        logger.info(f'📊 Servers: {len(bot.guilds)}')

        # Load cog
        await bot.add_cog(MultiModelAI(bot))

        # Show model status
        router = ModelRouter()
        status = router.get_status()
        logger.info("Model Status:")
        for name, info in status.items():
            icon = "✅" if info['available'] else "❌"
            logger.info(f"  {icon} {info['name']}: {info['provider']}")

    @bot.event
    async def on_command_error(ctx, error):
        """Handle command errors"""
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing argument: {error.param.name}")
        elif isinstance(error, commands.CommandNotFound):
            # Ignore unknown commands
            pass
        else:
            logger.error(f"Command error: {error}")
            await ctx.send(f"❌ Error: {str(error)}")

    return bot


if __name__ == "__main__":
    # Run the bot
    TOKEN = os.getenv("DISCORD_TOKEN")

    if not TOKEN:
        print("❌ Error: DISCORD_TOKEN not set in .env")
        exit(1)

    print("🚀 Starting Multi-Model Discord Bot...")
    bot = create_multimodel_bot(TOKEN)
    bot.run(TOKEN)
