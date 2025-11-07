"""
PhiGEN Bots Package

Discord bot implementations and automation tools.
"""

try:
    from .discord_bot import *
    from .claude_discord_bot import *
    from .discord_bot_mcp_enhanced import *
    from .jc_discord_bot import *
    from .discord_mcp_bridge import *
    from .jc_autonomous_worker import *
    from .task_executor import *
except ImportError as e:
    print(f"Warning: Some bot components not available: {e}")

__version__ = "1.0.0"
__author__ = "PhiGEN Team"