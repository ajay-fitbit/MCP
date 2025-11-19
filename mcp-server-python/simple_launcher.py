#!/usr/bin/env python3

"""
Direct OpenAI Chat Launcher - Simple Version

This script directly launches the OpenAI chat without creating temporary files,
which avoids encoding issues on Windows.
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

def main():
    """Direct launcher for OpenAI chat - simple version with no encoding issues"""
    print("[LAUNCH] OpenAI Database Chat - SIMPLE VERSION")
    print("=========================================")
    
    # Load environment variables
    load_dotenv()
    
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your-openai-api-key-here':
        print("[ERROR] OpenAI API key not configured!")
        print("Please edit the .env file and add your OpenAI API key.")
        return 1
    
    print("[OK] OpenAI API key found")
    
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_script = os.path.join(script_dir, "server.py")
    
    # Create a simple Python script
    direct_script = '''
import os
import sys
import asyncio
from openai_client import OpenAIDatabaseClient

async def run_chat():
    # Initialize client
    server_path = r"{0}"
    client = OpenAIDatabaseClient(server_path)
    print("[INFO] OpenAI client initialized")
    
    # Run interactive chat
    try:
        await client.interactive_chat()
    except Exception as e:
        print(f"[ERROR] {{e}}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(run_chat()))
'''.format(server_script.replace('\\', '\\\\'))
    
    # Create a direct script file that's simple and won't have encoding issues
    direct_path = os.path.join(script_dir, "direct_openai_chat.py")
    try:
        with open(direct_path, "w", encoding="utf-8") as f:
            f.write(direct_script)
        
        print("[INFO] Created simple launcher...")
        print("[LAUNCH] Starting chat...")
        
        # Run the script directly
        python_path = sys.executable or "python"
        result = subprocess.run([python_path, direct_path], cwd=script_dir)
        
        return result.returncode
    
    except Exception as e:
        print(f"[ERROR] Failed to start chat: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        # Clean up
        if os.path.exists(direct_path):
            try:
                os.remove(direct_path)
            except:
                pass

if __name__ == "__main__":
    sys.exit(main())