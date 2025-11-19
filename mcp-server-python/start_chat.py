#!/usr/bin/env python3

import asyncio
import os
from dotenv import load_dotenv
from openai_client import OpenAIDatabaseClient

async def main():
    """Start interactive OpenAI database chat"""
    print("🤖 OpenAI Database Chat")
    print("=======================")
    print("Ask questions about your database in natural language!")
    print("Type 'quit' or 'exit' to end the session.\n")
    
    # Load environment
    load_dotenv()
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your-openai-api-key-here':
        print("❌ OpenAI API key not configured!")
        print("Please edit the .env file and add your OpenAI API key.")
        return
    
    try:
        # Create client
        server_script = os.path.join(os.path.dirname(__file__), "server.py")
        client = OpenAIDatabaseClient(server_script)
        print("✅ OpenAI client initialized")
        
        # Start interactive chat
        await client.interactive_chat()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def run_chat():
    """Main function that handles event loop properly"""
    try:
        # Check if we're already in an event loop
        loop = asyncio.get_running_loop()
        print("⚡ Event loop detected - running in thread")
        
        # We're in an event loop (like VS Code terminal), run in separate thread
        import threading
        
        def run_in_thread():
            # Create new event loop in thread
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                new_loop.run_until_complete(main())
            finally:
                new_loop.close()
        
        # Run in separate thread
        thread = threading.Thread(target=run_in_thread)
        thread.daemon = True
        thread.start()
        
        # Keep main thread alive for interactive input
        try:
            thread.join()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            
    except RuntimeError:
        # No event loop running, create a new one
        print("🔄 Creating new event loop")
        asyncio.run(main())

if __name__ == "__main__":
    run_chat()