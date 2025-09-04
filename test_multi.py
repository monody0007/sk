#!/usr/bin/env python3
"""
Minimal multi-agent runner with hardcoded agent IDs.
Calls the improved single-agent test for each ID and prints latest replies.

This script demonstrates how to test multiple AI characters simultaneously
by running the single-agent test for each character in a predefined list.
It's useful for testing character consistency across multiple agents.
"""

from test_improved_memory_chat import test_memory_chat_with_existing_agent

# Fill in the Agent IDs you want to test
AGENT_IDS = [
    "e9623d1a-f3bb-4718-b32d-6c72bf6fc8ff",
    "3dd8af13-2668-49ff-bd46-7cec5c1a98b5",
    "b53628ef-2108-4fc9-aad6-8d4a31185089",
    # "another-agent-id-123",
]


def main() -> bool:
    """
    Run tests for multiple agents sequentially.
    
    This function iterates through the predefined list of agent IDs
    and runs the memory chat test for each one. It provides progress
    information and returns overall success status.
    
    Returns:
        bool: True if all tests passed, False if any test failed
    """
    ok_all = True
    for i, aid in enumerate(AGENT_IDS, 1):
        print("\n" + "=" * 60)
        print(f"🧠 与agent交互（{i}/{len(AGENT_IDS)}） - agent_id={aid}")
        print("=" * 60)
        ok = test_memory_chat_with_existing_agent(aid, user_id="system")
        ok_all = ok_all and ok
    return ok_all


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)

