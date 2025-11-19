#!/usr/bin/env python3

import asyncio
import os
from dotenv import load_dotenv
from openai_client import OpenAIDatabaseClient

async def quick_test():
    """Quick test of the fixed OpenAI client"""
    print("🧪 Quick OpenAI Database Test")
    print("=============================")
    
    load_dotenv()
    
    try:
        # Create client
        server_script = os.path.join(os.path.dirname(__file__), "server.py")
        client = OpenAIDatabaseClient(server_script)
        print("✅ Client created successfully")
        
        # Test database connection
        print("\n🔄 Testing database connection...")
        connect_result = await client.call_mcp_server("connect_database", {})
        print(f"✅ {connect_result}")
        
        # Test simple chat
        print("\n🔄 Testing OpenAI chat...")
        response = await client.chat_with_database("How many tables are in my database?")
        print(f"🤖 GPT Response: {response[:200]}...")
        
        print(f"\n🎉 Everything is working!")
        print(f"You can now use: start_openai_chat.bat")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(quick_test())