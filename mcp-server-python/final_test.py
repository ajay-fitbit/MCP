#!/usr/bin/env python3

import asyncio
import os
from dotenv import load_dotenv
from openai_client import OpenAIDatabaseClient

def main():
    """Start interactive OpenAI database chat - sync version"""
    print("🤖 OpenAI Database Chat")
    print("=======================")
    print("Testing your database connection with OpenAI...")
    
    # Load environment
    load_dotenv()
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your-openai-api-key-here':
        print("❌ OpenAI API key not configured!")
        return
    
    try:
        # Create client
        server_script = os.path.join(os.path.dirname(__file__), "server.py")
        client = OpenAIDatabaseClient(server_script)
        print("✅ OpenAI client initialized")
        
        # Test simple question
        print("\n🔄 Testing: 'How many tables are in my database?'")
        
        # Use the sync wrapper for the async function
        async def test_query():
            return await client.chat_with_database("How many tables are in my database?")
        
        # Run in new event loop
        response = asyncio.new_event_loop().run_until_complete(test_query())
        print(f"\n🤖 GPT Response:")
        print(f"{response[:300]}...")
        
        print(f"\n✅ SUCCESS! Your OpenAI database integration is working!")
        print(f"\n💡 You can now ask natural language questions about your database:")
        print(f"   • 'Show me all tables with PATIENT in the name'")  
        print(f"   • 'What columns does the REFERRALS table have?'")
        print(f"   • 'Run the USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET procedure'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()