"""
Smoke test for MemU adapter integration.

This script performs a basic smoke test to verify that the Sekai Engine
can properly initialize and create AI characters from world data.
It loads world story data from memory_data.json and creates agents
with seeded memories.
"""

from __future__ import annotations
import json
import os
import sys
from sekai_engine import SekaiEngine


def main():
    """
    Run smoke test for Sekai Engine initialization.
    
    This function performs a basic test to ensure that:
    1. Required environment variables are set
    2. Sekai Engine can be initialized
    3. World data can be loaded and parsed
    4. Agents can be created with proper memory seeding
    
    Raises:
        SystemExit: If required dependencies or environment variables are missing
    """
    # Check required environment variables
    if not os.getenv("MEMU_API_KEY"):
        raise SystemExit("Missing MEMU_API_KEY. Get your API key from: https://app.memu.so/api-key/")
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Missing OPENAI_API_KEY. Set OPENAI_API_KEY environment variable")
    try:
        eng = SekaiEngine()
    except ImportError:
        raise SystemExit("MemU SDK not found. Run: pip install memu-py")
    # Load the real world story from memory_data.json
    data_path = os.path.join(os.path.dirname(__file__), "memory_data.json")
    if not os.path.exists(data_path):
        # Also try project root if executed from elsewhere
        data_path = os.path.abspath("memory_data.json")
    with open(data_path, "r", encoding="utf-8") as f:
        chapters = json.load(f)
    world_story = {"chapters": chapters}
    print("🎮 Initializing game world...")
    engine_id, agents = eng.init(world_story)
    print("✅ Smoke test completed successfully!")
    
    print(f"\n🆔 Engine ID: {engine_id}")
    print(f"👥 Created {len(agents)} agents:")
    print("=" * 50)
    
    for i, (agent_id, agent_name) in enumerate(agents, 1):
        print(f"{i}. Agent ID: {agent_id}")
        print(f"   Name: {agent_name}")
        print("-" * 30)

if __name__ == "__main__":
    main()
