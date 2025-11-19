#!/usr/bin/env python3

"""
Fixed OpenAI Chat Launcher

This script launches the OpenAI database chat with proper event loop handling
to avoid the "asyncio.run() cannot be called from a running event loop" error.
"""

import os
import asyncio
import sys
import subprocess
from dotenv import load_dotenv

def main():
    """Launch the OpenAI database chat with proper event loop handling"""
    print("[LAUNCH] OpenAI Database Chat - FIXED VERSION")
    print("======================================")
    
    # Load environment variables
    load_dotenv()
    
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your-openai-api-key-here':
        print("[ERROR] OpenAI API key not configured!")
        print("Please edit the .env file and add your OpenAI API key.")
        return 1
    
    print("[OK] OpenAI API key found")
    print("[INFO] Creating subprocess to avoid event loop issues...")
    
    # Create a launcher script that runs in its own process - NO EMOJIS to avoid encoding issues
    launcher_script = """
import os
import asyncio
import sys
from dotenv import load_dotenv
from openai_client import OpenAIDatabaseClient

async def main():
    # Load environment
    load_dotenv()
    
    print("[CHAT] OpenAI Database Chat")
    print("=======================")
    print("Ask questions about your database in natural language!")
    print("Type 'quit' or 'exit' to end the session.\\n")
    
    try:
        # Create client with proper path to server script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        server_script = os.path.join(script_dir, "server.py")
        client = OpenAIDatabaseClient(server_script)
        print("[OK] OpenAI client initialized")
        
        # Start interactive chat
        await client.interactive_chat()
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
"""
    
    # Write the launcher script to a temporary file with explicit UTF-8 encoding
    launcher_path = os.path.join(os.path.dirname(__file__), "openai_chat_launcher.py")
    with open(launcher_path, "w", encoding="utf-8") as f:
        f.write(launcher_script)
    
    try:
        # Run the launcher script in a new process
        print("[LAUNCH] Starting chat...")
        
        # Get the Python interpreter path
        python_path = sys.executable
        
        # Run the launcher script as a subprocess
        result = subprocess.run([python_path, launcher_path], cwd=os.path.dirname(__file__))
        
        return result.returncode
    
    finally:
        # Clean up the launcher script
        if os.path.exists(launcher_path):
            os.remove(launcher_path)

if __name__ == "__main__":
    sys.exit(main())