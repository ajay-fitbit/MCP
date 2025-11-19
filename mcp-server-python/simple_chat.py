#!/usr/bin/env python3

import asyncio
import os
from dotenv import load_dotenv
from openai_client import OpenAIDatabaseClient

def simple_chat():
    """Simple interactive chat that works in any environment"""
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
        
        # Simple conversation loop
        conversation_history = []
        
        while True:
            try:
                # Get user input
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                
                print("🤖 GPT: ", end="", flush=True)
                
                # Handle the async call with a simple subprocess approach
                print("🔄 Thinking...")
                
                # Create a simple test script and run it
                test_script = f'''
import asyncio
import sys
import os
sys.path.append(r"{os.path.dirname(__file__)}")
from dotenv import load_dotenv
from openai_client import OpenAIDatabaseClient

async def query():
    load_dotenv()
    server_script = r"{server_script}"
    client = OpenAIDatabaseClient(server_script)
    response = await client.chat_with_database(r"""{user_input}""")
    print(response)

asyncio.run(query())
'''
                
                # Write temp script
                temp_file = "temp_query.py"
                with open(temp_file, 'w') as f:
                    f.write(test_script)
                
                # Run it and get response
                import subprocess
                result = subprocess.run(['python', temp_file], capture_output=True, text=True, cwd=os.path.dirname(__file__))
                
                # Clean up
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                
                if result.returncode == 0:
                    response = result.stdout.strip()
                    print(response)
                else:
                    print(f"Error: {result.stderr}")
                    continue
                
                # Add to conversation history
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append({"role": "assistant", "content": response})
                
                # Keep conversation history manageable
                if len(conversation_history) > 20:
                    conversation_history = conversation_history[-10:]
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_chat()