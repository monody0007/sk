"""
Environment variable utilities for Sekai Engine.

This module provides utility functions for loading and managing
environment variables, particularly for loading .env files.
"""

from __future__ import annotations

from dotenv import load_dotenv


def ensure_env_loaded() -> None:
    """
    Load environment variables from a .env file if present using python-dotenv.
    
    This function ensures that environment variables are loaded from
    a .env file in the current directory, which is useful for local
    development and testing.
    """
    load_dotenv()
