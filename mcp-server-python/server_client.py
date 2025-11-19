#!/usr/bin/env python3

"""
Fixed OpenAI Database Client that connects to a running MCP server.

This client will use HTTP requests to communicate with the MCP server instead
of trying to import it directly, which was causing the 'No module named mcp' error.
"""

import os
import sys
import json
import asyncio
import subprocess
from typing import Dict, Any, List, Union, Optional
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

class OpenAIServerClient:
    """OpenAI client that connects to a running MCP server"""
    
    def __init__(self, server_url="http://localhost:8765"):
        """Initialize with the server URL"""
        self.server_url = server_url
        
        # Initialize OpenAI client with corporate environment support
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Remove quotes if present
        api_key = api_key.strip('"\'')
        
        # Always try corporate-friendly settings first
        try:
            import httpx
            print("Using corporate-friendly SSL settings...")
            http_client = httpx.Client(verify=False, timeout=60.0)
            self.client = openai.OpenAI(api_key=api_key, http_client=http_client)
        except ImportError:
            print("httpx not available, using default client")
            self.client = openai.OpenAI(api_key=api_key)
        except Exception as e:
            print(f"Corporate client failed: {e}, trying default...")
            self.client = openai.OpenAI(api_key=api_key)
            
        # Database tools available
        self.available_tools = [
            {
                "type": "function",
                "function": {
                    "name": "connect_database",
                    "description": "Connect to the SQL Server database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "server": {"type": "string", "description": "Database server name"},
                            "database": {"type": "string", "description": "Database name"}
                        },
                        "required": ["server", "database"]
                    }
                }
            },
            {
                "type": "function", 
                "function": {
                    "name": "execute_query",
                    "description": "Execute a SQL query on the database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "SQL query to execute"},
                            "parameters": {"type": "object", "description": "Query parameters"}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tables",
                    "description": "List all tables in the database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "schema": {"type": "string", "description": "Schema name (default: dbo)"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "describe_table",
                    "description": "Get detailed information about a table",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tableName": {"type": "string", "description": "Table name"},
                            "schema": {"type": "string", "description": "Schema name (default: dbo)"}
                        },
                        "required": ["tableName"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "execute_stored_procedure",
                    "description": "Execute a SQL stored procedure",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "procedureName": {"type": "string", "description": "Stored procedure name"},
                            "parameters": {"type": "object", "description": "Stored procedure parameters"}
                        },
                        "required": ["procedureName"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_stored_procedures",
                    "description": "List all stored procedures in the database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {"type": "string", "description": "Filter pattern (e.g., '%Customer%')"}
                        }
                    }
                }
            }
        ]
    
    async def call_mcp_server(self, method: str, params: Dict[str, Any]) -> str:
        """Call the running MCP server using HTTP"""
        try:
            # Try to use httpx for HTTP requests with SSL verification disabled
            import httpx
            
            async with httpx.AsyncClient(verify=False) as client:
                url = f"{self.server_url}/{method}"
                response = await client.post(url, json=params)
                
                if response.status_code == 200:
                    result = response.json()
                    return json.dumps(result, default=str, indent=2)
                else:
                    return f"Error: Server returned status {response.status_code}"
        
        except ImportError:
            # Fall back to curl if httpx not available
            return await self._call_with_curl(method, params)
    
    async def _call_with_curl(self, method: str, params: Dict[str, Any]) -> str:
        """Call the server using curl as a fallback"""
        try:
            # Create temporary file for request body
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                json.dump(params, f)
                temp_file = f.name
            
            # Build the curl command
            curl_cmd = [
                "curl", "-s", "-X", "POST",
                "-H", "Content-Type: application/json",
                "-d", f"@{temp_file}",
                f"{self.server_url}/{method}"
            ]
            
            # Run curl
            proc = await asyncio.create_subprocess_exec(
                *curl_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await proc.communicate()
            
            # Clean up
            try:
                os.unlink(temp_file)
            except:
                pass
                
            if proc.returncode != 0:
                return f"Error: {stderr.decode()}"
                
            return stdout.decode()
            
        except Exception as e:
            return f"Error calling server: {str(e)}"
    
    async def chat_with_database(self, user_input: str, conversation_history: Optional[List] = None) -> str:
        """Chat with the database using OpenAI"""
        if conversation_history is None:
            conversation_history = []
            
        # Create system message
        system_message = {
            "role": "system",
            "content": """You are a helpful assistant with access to a SQL Server database.
You can execute SQL queries and explore the database schema.
When asked questions about the database, use the available tools to query the data.
Always format SQL results in a clear and readable way.
If you encounter errors, try to diagnose the issue and suggest alternatives."""
        }
        
        # Add user input to messages
        messages = [system_message] + conversation_history + [{"role": "user", "content": user_input}]
        
        # Models to try in order of preference
        models_to_try = ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]
        
        response = None
        selected_model = None
        
        # Try models in order until one works
        for model in models_to_try:
            try:
                print(f"Trying model: {model}")
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=self.available_tools,
                    tool_choice="auto",
                    max_tokens=2000,
                    temperature=0.1
                )
                selected_model = model
                print(f"Using model: {model}")
                break
            except Exception as model_error:
                print(f"Model {model} failed: {str(model_error)[:100]}...")
                if model == models_to_try[-1]:  # Last model
                    raise model_error
                continue
        
        if not response:
            return "Error: No models available"
        
        message = response.choices[0].message
        
        # Handle tool calls
        if message.tool_calls:
            # Add assistant message to conversation
            conversation_history.append({
                "role": "assistant", 
                "content": message.content,
                "tool_calls": [{"id": tc.id, "type": tc.type, "function": {"name": tc.function.name, "arguments": tc.function.arguments}} for tc in message.tool_calls]
            })
            
            # Execute tool calls
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"Executing: {function_name}")
                if function_args:
                    print(f"Arguments: {function_args}")
                
                # Call the MCP server
                result = await self.call_mcp_server(function_name, function_args)
                
                # Add tool result to conversation
                conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # Get final response from OpenAI
            try:
                final_response = self.client.chat.completions.create(
                    model=selected_model,  # Use the same model that worked
                    messages=[system_message] + conversation_history,
                    max_tokens=2000,
                    temperature=0.1
                )
                return final_response.choices[0].message.content
            except Exception as final_error:
                return f"Error generating final response: {str(final_error)}"
        else:
            # No tool calls, return the direct message
            return message.content
    
    async def interactive_chat(self):
        """Start an interactive chat session"""
        print("OpenAI Database Chat")
        print("=======================")
        print("Chat with your database using OpenAI GPT-4!")
        print("Type 'quit' to exit")
        print()
        
        conversation_history = []
        
        # Auto-connect to database
        print("Auto-connecting to database...")
        connect_result = await self.call_mcp_server("connect_database", {
            "server": os.getenv("DB_SERVER", "AHS-LP-945"),
            "database": os.getenv("DB_NAME", "Ahs_Bit_Red_QA_8170")
        })
        print(f"Connected: {connect_result}")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not user_input:
                    continue
                
                print("GPT-4: ", end="", flush=True)
                response = await self.chat_with_database(user_input, conversation_history)
                print(response)
                print()
                
                # Add to conversation history
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append({"role": "assistant", "content": response})
                
                # Keep conversation history manageable
                if len(conversation_history) > 20:
                    conversation_history = conversation_history[-10:]
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

# Main function
async def main():
    """Start the OpenAI database chat client"""
    print("Starting OpenAI Database Chat...")
    print("===============================")
    
    # Load environment variables
    load_dotenv()
    
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("ERROR: OPENAI_API_KEY not found!")
        print("Please add your OpenAI API key to the .env file:")
        print("OPENAI_API_KEY=your-api-key-here")
        return 1
    
    try:
        # Get server URL from environment or use default
        server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8765")
        print(f"Connecting to MCP server at: {server_url}")
        
        # Create client
        client = OpenAIServerClient(server_url)
        
        # Start interactive chat
        await client.interactive_chat()
        return 0
        
    except Exception as e:
        print(f"ERROR: Failed to start: {e}")
        import traceback
        traceback.print_exc()
        return 1

# Entry point
if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))