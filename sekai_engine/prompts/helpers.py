"""
Helper functions for building system messages in Sekai Engine.

This module provides utility functions for constructing system messages
that combine character context with memory information.
"""

from __future__ import annotations

from .templates import SYSTEM_WITH_CONTEXT_TEMPLATE, SYSTEM_BASE_TEMPLATE


def build_system_message(context: str) -> str:
    """
    Render the system message that embeds retrieved memory context.
    
    This function creates a system message that includes relevant memory
    context if available, or falls back to a basic system message if
    no context is provided.
    
    Args:
        context: Memory context string retrieved from MemU
        
    Returns:
        Formatted system message string
    """
    if context:
        return SYSTEM_WITH_CONTEXT_TEMPLATE.format(context=context)
    return SYSTEM_BASE_TEMPLATE
 
