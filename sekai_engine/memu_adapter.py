from __future__ import annotations

import os
from typing import Dict, List, Optional

from memu.sdk.python.client import MemuClient


class MemUAdapter:
    """
    Adapter class for integrating with MemU memory framework.
    
    This class provides a simplified interface for interacting with MemU's
    memory system, including memory retrieval and conversation storage.
    It handles the communication with MemU's Python SDK client.
    """

    def __init__(self) -> None:
        """
        Initialize MemU client with API configuration from environment variables.
        
        Raises:
            ValueError: If MEMU_API_KEY is not found in environment variables
        """
        base_url = os.getenv("MEMU_API_BASE_URL", "https://api.memu.so")
        api_key = os.getenv("MEMU_API_KEY")
        if not api_key:
            raise ValueError(
                "MEMU_API_KEY environment variable is required. "
                "Get your API key from https://app.memu.so/api-key/"
            )
        self.memu_client = MemuClient(base_url=base_url, api_key=api_key)

    def retrieve_context(self, *, user_id: str, agent_id: str, query: str):
        """
        Retrieve related memories from MemU for use as pre-hook input.

        This method queries MemU's memory system to find relevant memories
        based on the user's query, user ID, and agent ID. It's used to
        provide context for AI responses.

        Args:
            user_id: Unique identifier for the user
            agent_id: Unique identifier for the AI agent
            query: The user's query to search for related memories

        Returns:
            The raw RelatedMemoryItemsResponse from MemU, or None on failure
        """
        try:
            response = self.memu_client.retrieve_related_memory_items(
                user_id=user_id,
                agent_id=agent_id,
                query=query,
                top_k=20,
                min_similarity=0.3,
            )
            return response
        except Exception as e:
            print(f"Warning: Failed to retrieve memories: {e}")
            return None

    def memorize_dialogue(
        self,
        *,
        user_id: str,
        user_name: str,
        agent_id: str,
        agent_name: str,
        user_message: str,
        assistant_message: str
    ) -> None:
        """
        Memorize a pair of user/assistant messages as a post-hook.

        This method stores a conversation exchange in MemU's memory system.
        It's typically called after an AI response is generated to ensure
        the conversation is remembered for future interactions.

        Args:
            user_id: Unique identifier for the user
            user_name: Display name for the user
            agent_id: Unique identifier for the AI agent
            agent_name: Display name for the AI agent
            user_message: The user's message content
            assistant_message: The AI's response content
        """
        self.memu_client.memorize_conversation(
            conversation=[
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": assistant_message},
            ],
            user_id=user_id,
            user_name=user_name,
            agent_id=agent_id,
            agent_name=agent_name,
        )

    def memorize_messages(
        self,
        *,
        conversation: List[Dict[str, str]],
        user_id: str,
        user_name: str,
        agent_id: str,
        agent_name: str
    ) -> None:
        """
        Memorize an arbitrary list of messages for an agent/user.

        This method stores a sequence of messages in MemU's memory system.
        It's used for seeding initial memories or storing complex conversation
        structures.

        Args:
            conversation: List of message dictionaries with 'role' and 'content' keys
            user_id: Unique identifier for the user
            user_name: Display name for the user
            agent_id: Unique identifier for the AI agent
            agent_name: Display name for the AI agent
        """
        self.memu_client.memorize_conversation(
            conversation=conversation,
            user_id=user_id,
            user_name=user_name,
            agent_id=agent_id,
            agent_name=agent_name,
        )
