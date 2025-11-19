#!/usr/bin/env python3

import asyncio
import os
from dotenv import load_dotenv
from openai_client import OpenAIDatabaseClient

async def openai_demo():
    """Demonstrate OpenAI database integration"""
    print("🤖 OpenAI Database Integration Demo")
    print("==================================")
    
    # Load environment
    load_dotenv()
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your-openai-api-key-here':
        print("❌ OpenAI API key not configured!")
        print("Please edit the .env file and add your OpenAI API key:")
        print("OPENAI_API_KEY=your-actual-api-key")
        print("\nYou can get an API key from: https://platform.openai.com/api-keys")
        return
    
    try:
        print(f"✅ OpenAI API key found: {api_key[:12]}...")
        
        # Create client
        server_script = os.path.join(os.path.dirname(__file__), "server.py")
        client = OpenAIDatabaseClient(server_script)
        
        print("\n🔄 Testing database connection...")
        connect_result = await client.call_mcp_server("connect_database", {})
        print(f"✅ {connect_result}")
        
        # Demo questions
        demo_questions = [
            "How many tables are in my database?",
            "Show me the structure of the PATIENT_DETAILS table",
            "List the first 5 stored procedures that contain 'PATIENT' in their name"
        ]
        
        print("\n🤖 Demo Questions:")
        for i, question in enumerate(demo_questions, 1):
            print(f"\n{i}. Question: {question}")
            print("   GPT-4 Response:")
            response = await client.chat_with_database(question)
            print(f"   {response[:200]}..." if len(response) > 200 else f"   {response}")
        
        print("\n🎉 Demo completed!")
        print("\n💡 To start interactive chat:")
        print("   • Make sure your OpenAI API key is in .env")
        print("   • Run: start_openai_chat.bat")
        print("   • Ask questions in natural language!")
        
        print("\n📊 Your database stats:")
        print("   • 1,815 tables accessible")
        print("   • 6,064 stored procedures available")
        print("   • USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET ready to use")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(openai_demo())