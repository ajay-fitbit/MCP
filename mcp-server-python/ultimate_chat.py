#!/usr/bin/env python3

"""
ULTIMATE FAILSAFE OpenAI Chat

This script is a completely standalone chat implementation that
avoids ALL potential issues with async, event loops, encoding, etc.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Import OpenAI client
try:
    from openai_client import OpenAIDatabaseClient
except ImportError:
    print("ERROR: Could not import OpenAIDatabaseClient")
    print("Make sure you're running this from the correct directory.")
    sys.exit(1)

# Main async function
async def ultimate_chat():
    """Ultimate failsafe chat implementation"""
    try:
        # Setup
        print("OpenAI Database Chat")
        print("====================")
        
        # Load environment
        load_dotenv()
        
        # Check API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your-openai-api-key-here':
            print("ERROR: OpenAI API key not configured!")
            print("Please edit the .env file and add your OpenAI API key.")
            return 1
        
        # Create client
        script_dir = os.path.dirname(os.path.abspath(__file__))
        server_script = os.path.join(script_dir, "server.py")
        client = OpenAIDatabaseClient(server_script)
        print("Client initialized successfully")
        
        # Simple conversation history
        conversation = []
        
        # Connect to database
        print("Connecting to database...")
        try:
            result = await client.call_mcp_server("connect_database", {})
            print("Connected:", result)
            print("")
        except Exception as e:
            print("Database connection warning:", e)
            print("Continuing anyway - some features might not work.")
            print("")
        
        # Main chat loop
        print("Type your questions about the database, or 'exit' to quit.")
        print("")
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Handle exit
                if user_input.lower() in ["exit", "quit", "q"]:
                    print("Goodbye!")
                    break
                
                # Skip empty input
                if not user_input:
                    continue
                
                # Get response from OpenAI
                print("GPT-4: ", end="", flush=True)
                response = await client.chat_with_database(user_input, conversation)
                print(response)
                print("")
                
                # Update conversation history
                conversation.append({"role": "user", "content": user_input})
                conversation.append({"role": "assistant", "content": response})
                
                # Keep history manageable
                if len(conversation) > 20:
                    # Keep only the most recent interactions
                    conversation = conversation[-10:]
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()
        
        return 0
        
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1

# Main entry point with proper event loop handling
def main():
    """Main entry point with proper event loop handling"""
    try:
        # Try to get running loop (we might be in a Jupyter notebook or other environment)
        loop = asyncio.get_running_loop()
        print("Detected running event loop - using appropriate wrapper")
        
        # We're in an event loop, need to run in a new thread
        import threading
        import concurrent.futures
        
        def run_in_thread():
            """Run in a new thread with its own event loop"""
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                return new_loop.run_until_complete(ultimate_chat())
            finally:
                new_loop.close()
        
        # Run in thread executor
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(run_in_thread)
            return future.result()
            
    except RuntimeError:
        # No running loop, use asyncio.run
        print("No event loop detected - creating new one")
        return asyncio.run(ultimate_chat())

if __name__ == "__main__":
    sys.exit(main())