#!/usr/bin/env python3

"""
Direct Chat Launcher - No Temp Files

This script directly starts the OpenAI chat without any temporary files
to avoid all encoding issues on Windows.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv
from openai_client import OpenAIDatabaseClient

async def run_chat():
    """Run the OpenAI chat directly"""
    print("[CHAT] OpenAI Database Chat")
    print("=======================")
    print("Ask questions about your database in natural language!")
    print("Type 'quit' or 'exit' to end the session.\n")
    
    try:
        # Load environment
        load_dotenv()
        
        # Check API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your-openai-api-key-here':
            print("[ERROR] OpenAI API key not configured!")
            print("Please edit the .env file and add your OpenAI API key.")
            return 1
            
        # Create client with proper path to server script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        server_script = os.path.join(script_dir, "server.py")
        client = OpenAIDatabaseClient(server_script)
        print("[OK] OpenAI client initialized")
        
        # Start interactive chat (this is already an async function that we're awaiting)
        await client.interactive_chat()
        return 0
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return 1

def main():
    """Main function with proper event loop handling"""
    try:
        # Try to get running loop (we might be in a Jupyter notebook or other environment)
        loop = asyncio.get_running_loop()
        print("[INFO] Detected running event loop - using thread")
        
        # We're in an event loop, use a thread
        import threading
        import concurrent.futures
        
        # Run in thread executor
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(asyncio.run, run_chat())
            return future.result()
            
    except RuntimeError:
        # No running loop, use asyncio.run
        print("[INFO] No event loop detected - creating new one")
        return asyncio.run(run_chat())

if __name__ == "__main__":
    sys.exit(main())