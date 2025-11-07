"""
PhiGEN Main Package

Core Discord bot functionality and utilities.
"""

try:
    from .agent_feed import *
    from .detect_agent import *
except ImportError as e:
    print(f"Warning: Some phigen components not available: {e}")

__version__ = "1.0.0"
__author__ = "PhiGEN Team"