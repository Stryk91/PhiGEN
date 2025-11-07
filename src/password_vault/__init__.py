"""
PhiGEN Password Vault Package

A secure password management application with GUI interface.
"""

try:
    from .backend import *
    from .validators import *
except ImportError as e:
    # GUI components may not be available in all environments
    print(f"Warning: Some password vault components not available: {e}")

__version__ = "1.0.0"
__author__ = "PhiGEN Team"