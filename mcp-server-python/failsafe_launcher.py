#!/usr/bin/env python3

"""
FAILSAFE OpenAI Chat Launcher

This script uses the simplest possible approach to launch OpenAI chat,
avoiding all potential issues with async, event loops, and encoding.
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

def main():
    """Launch OpenAI chat as a completely separate process"""
    print("Starting OpenAI Database Chat (FAILSAFE VERSION)")
    print("===============================================")
    
    # Load environment variables
    load_dotenv()
    
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your-openai-api-key-here':
        print("ERROR: OpenAI API key not configured!")
        print("Please edit the .env file and add your OpenAI API key.")
        return 1
    
    print("OpenAI API key found")
    
    # Get current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create a very minimal Python script with no emojis, no fancy code, just the basics
    minimal_script = '''
import os
import asyncio
import sys

# Add the current directory to path to ensure imports work
sys.path.insert(0, r"{0}")

# Import required modules
from dotenv import load_dotenv
from openai_client import OpenAIDatabaseClient

# Define main async function
async def chat_main():
    # Load environment variables
    load_dotenv()
    
    # Initialize OpenAI client
    client = OpenAIDatabaseClient(r"{1}")
    
    # Define a simple chat interface
    print("OpenAI Database Chat")
    print("====================")
    print("Type your questions about the database, or 'exit' to quit.")
    print("")
    
    # Simple conversation history
    conversation = []
    
    # First connect to database
    try:
        print("Connecting to database...")
        result = await client.call_mcp_server("connect_database", {{}})
        print("Connected:", result)
        print("")
    except Exception as e:
        print("Database connection error:", e)
    
    # Chat loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break
                
            if not user_input:
                continue
                
            # Get response from OpenAI
            print("GPT-4: ", end="", flush=True)
            response = await client.chat_with_database(user_input, conversation)
            print(response)
            print("")
            
            # Update conversation history
            conversation.append({{"role": "user", "content": user_input}})
            conversation.append({{"role": "assistant", "content": response}})
            
        except KeyboardInterrupt:
            print("\\nGoodbye!")
            break
        except Exception as e:
            print("Error:", str(e))

# Run the main function with proper asyncio handling
if __name__ == "__main__":
    asyncio.run(chat_main())
'''.format(script_dir.replace('\\', '\\\\'), os.path.join(script_dir, "server.py").replace('\\', '\\\\'))
    
    # Create a temporary script
    temp_script = os.path.join(script_dir, "failsafe_chat.py")
    try:
        # Write script with explicit UTF-8 encoding and no special characters
        with open(temp_script, "w", encoding="utf-8") as f:
            f.write(minimal_script)
            
        print("Starting chat in a clean subprocess...")
        
        # Run as a completely separate process
        python = sys.executable or "python"
        
        # Run script in a new process
        subprocess.run([python, temp_script], check=True)
        
        return 0
    
    except subprocess.CalledProcessError as e:
        print(f"Error running chat: {e}")
        return e.returncode
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    finally:
        # Clean up temp file
        try:
            if os.path.exists(temp_script):
                os.remove(temp_script)
        except:
            pass

if __name__ == "__main__":
    sys.exit(main())