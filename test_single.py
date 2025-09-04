#!/usr/bin/env python3
"""
Test script: talk with an existing agent using given agent_id and user_id,
ask 5 questions based on world memory.

This script demonstrates how to interact with an existing AI character
that has been initialized with world memory. It asks a series of
questions designed to test the character's memory and role-playing abilities.
"""

import os
import sys
import time
from sekai_engine import SekaiEngine
import argparse

def test_memory_chat_with_existing_agent(agent_id: str, user_id: str = "system"):
    """
    Talk to existing agent using provided IDs and ask 6 world-memory-based questions.
    
    This function initializes the Sekai Engine and conducts a conversation
    with an existing AI character to test memory retrieval and character
    consistency. It asks questions designed to verify that the character
    remembers their background and world context.
    
    Args:
        agent_id: The unique identifier of the AI character to interact with
        user_id: The user identifier for the conversation session
        
    Returns:
        bool: True if the test completed successfully, False otherwise
    """
    
    # Check required environment variables
    if not os.getenv("MEMU_API_KEY"):
        print("❌ Missing MEMU_API_KEY. Get your API key from: https://app.memu.so/api-key/")
        return False
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Missing OPENAI_API_KEY. Set OPENAI_API_KEY environment variable")
        return False
    
    try:
        print("🚀 Initializing Sekai Engine...")
        engine = SekaiEngine()

        print("\n" + "="*60)
        print("🧠 与agent对话 - 测试记忆检索功能")
        print("="*60)

     
        questions = [
            "请用第一人称简短自我介绍（包含你的角色定位与当前处境）。",
            "你与Dimitri的关系与近期互动是什么？",
            "你与Sylvain和Annette之间目前有哪些关键动态？",
            "最近在公司发生了哪些影响你的重要事件？",
            "你对Felix或他对你的观察有何看法？",
            "请你回答我刚才都问过你什么问题"  # 新增的测试问题
        ]

        for idx, q in enumerate(questions, start=1):
            print(f"\n💬 Q{idx}: {q}")
            ans = engine.engine_service_struct(user_id, agent_id, q)
            # ans是结构体，不直接打印整个对象；提取最新AI回复
            latest = ans.get("latest_assistant") or ans.get("output") or ""
            print(f"🤖 agent: {latest}")
            time.sleep(2)

        print("\n✅ 完成与agent的6轮对话测试。")
        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Talk to an existing agent by agent_id")
    parser.add_argument("--agent-id", required=True, help="Agent ID to talk with")
    parser.add_argument("--user-id", default=os.getenv("USER_ID", "system"), help="User ID for the session")
    args = parser.parse_args()

    success = test_memory_chat_with_existing_agent(agent_id=args.agent_id, user_id=args.user_id)
    sys.exit(0 if success else 1)
