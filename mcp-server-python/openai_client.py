#!/usr/bin/env python3

import asyncio
import json
import os
import openai
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import subprocess
import sys

# Load environment variables
load_dotenv()

class OpenAIDatabaseClient:
    def __init__(self, server_script_path: str):
        self.server_script_path = server_script_path
        self.python_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.venv', 'Scripts', 'python.exe')
        
        # Initialize OpenAI client with corporate environment support
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Remove quotes if present
        api_key = api_key.strip('"\'')
        
        # Always try corporate-friendly settings first
        try:
            import httpx
            print("🏢 Using corporate-friendly SSL settings...")
            http_client = httpx.Client(verify=False, timeout=60.0)
            self.client = openai.OpenAI(api_key=api_key, http_client=http_client)
        except ImportError:
            print("⚠️  httpx not available, using default client")
            self.client = openai.OpenAI(api_key=api_key)
        except Exception as e:
            print(f"⚠️  Corporate client failed: {e}, trying default...")
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
                    "description": "List all tables in the database. Use this when asked to show or list tables.",
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
                    "description": "Execute a stored procedure.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "procedureName": {"type": "string", "description": "Stored procedure name"},
                            "parameters": {"type": "object", "description": "Procedure parameters"}
                        },
                        "required": ["procedureName"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_stored_procedures",
                    "description": "List all stored procedures. Use this when asked to show or list stored procedures.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "schema": {"type": "string", "description": "Schema name (default: dbo)"},
                            "procedureNamePattern": {"type": "string", "description": "Filter procedures by name pattern"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_related_tables",
                    "description": "Get a table and all related tables through foreign key relationships. Use this when asked about table relationships, related tables, foreign keys, or when phrases like 'how tables are connected' or 'related to' are used.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tableName": {"type": "string", "description": "Name of the table to get relationships for"},
                            "schema": {"type": "string", "description": "Schema name (default: dbo)"}
                        },
                        "required": ["tableName"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_procedure_details",
                    "description": "Get details about a stored procedure including parameters and return columns",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "procedureName": {"type": "string", "description": "Name of the stored procedure to get details for"},
                            "schema": {"type": "string", "description": "Schema name (default: dbo)"}
                        },
                        "required": ["procedureName"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_query_from_template",
                    "description": "Read a SQL file from the templates directory or working directory and use it as a template to generate similar query. Use this when asked to use an existing SQL file as a template.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "templateFile": {"type": "string", "description": "Name of the SQL template file (e.g., 'query.sql', 'template.sql'). Templates are looked for in the 'templates' folder first, then in the working directory."},
                            "parameters": {"type": "object", "description": "Parameters to substitute in the template (format: @paramName in SQL)"}
                        },
                        "required": ["templateFile"]
                    }
                }
            }
        ]
    
    async def call_mcp_server(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call the MCP server directly"""
        try:
            # Import the database service directly
            sys.path.insert(0, os.path.dirname(self.server_script_path))
            from server import db_service
            
            # Call the appropriate method
            if tool_name == "connect_database":
                server = arguments.get("server", os.getenv('DB_SERVER', 'localhost'))
                database = arguments.get("database", os.getenv('DB_NAME', 'Ahs_Bit_Red_QA_8170'))
                user = os.getenv('DB_USER', '')
                password = os.getenv('DB_PASSWORD', '')
                
                result = db_service.connect(server, database, user if user else None, password if password else None)
                return result
            
            elif tool_name == "execute_query":
                query = arguments["query"]
                parameters = arguments.get("parameters", {})
                result = db_service.execute_query(query, parameters)
                return json.dumps(result, default=str, indent=2)
            
            elif tool_name == "list_tables":
                schema = arguments.get("schema", "dbo")
                result = db_service.list_tables(schema)
                return json.dumps(result, default=str, indent=2)
            
            elif tool_name == "describe_table":
                table_name = arguments["tableName"]
                schema = arguments.get("schema", "dbo")
                result = db_service.describe_table(table_name, schema)
                return json.dumps(result, default=str, indent=2)
            
            elif tool_name == "execute_stored_procedure":
                procedure_name = arguments["procedureName"]
                parameters = arguments.get("parameters", {})
                result = db_service.execute_stored_procedure(procedure_name, parameters)
                return json.dumps(result, default=str, indent=2)
            
            elif tool_name == "list_stored_procedures":
                schema = arguments.get("schema", "dbo")
                procedure_name_pattern = arguments.get("procedureNamePattern")
                result = db_service.list_stored_procedures(schema, procedure_name_pattern)
                return json.dumps(result, default=str, indent=2)
            
            elif tool_name == "get_related_tables":
                table_name = arguments["tableName"]
                schema = arguments.get("schema", "dbo")
                result = db_service.get_related_tables(table_name, schema)
                return json.dumps(result, default=str, indent=2)
            
            elif tool_name == "get_procedure_details":
                procedure_name = arguments["procedureName"]
                schema = arguments.get("schema", "dbo")
                result = db_service.get_procedure_details(procedure_name, schema)
                return json.dumps(result, default=str, indent=2)
                
            elif tool_name == "generate_query_from_template":
                template_file = arguments["templateFile"]
                parameters = arguments.get("parameters", {})
                result = db_service.generate_query_from_template(template_file, parameters)
                return json.dumps(result, default=str, indent=2)
            
            else:
                return f"Unknown tool: {tool_name}"
                
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"
    
    async def chat_with_database(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """Chat with OpenAI using database tools"""
        if conversation_history is None:
            conversation_history = []
        
        # System message with database context
        system_message = {
    "role": "system",
    "content": """You are a knowledgeable and efficient SQL Server assistant connected to the database 'Ahs_Bit_Red_QA_8170' hosted on server 'AHS-LP-945'.

Your Capabilities:
- Connection to the database
- Execute SQL queries and stored procedures
- Retrieve and describe table schemas
- Explore table relationships and foreign key connections
- List and explain stored procedures and their parameters
- Generate queries from SQL file templates stored in the templates directory
- Analyze and summarize data insights from queries

Important Guidelines:
- Always connect to the database before performing any operations
- When asked about related tables, table relationships, foreign keys, or connections between tables, use the get_related_tables tool
- When asked to use an existing SQL file as a template or to generate a similar query to an existing file, use the generate_query_from_template tool
- SQL templates are preferably stored in the 'templates' directory. Refer to template files by their filename only (e.g., "query.sql")
"""
}
        
        # Build messages
        messages = [system_message] + conversation_history + [{"role": "user", "content": user_message}]
        
        # Try different models
        models_to_try = ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]
        selected_model = None
        response = None
        
        try:
            # Make OpenAI API call with tools - try models in order
            for model in models_to_try:
                try:
                    print(f"🤖 Trying model: {model}")
                    response = self.client.chat.completions.create(
                        model=model,
                        messages=messages,
                        tools=self.available_tools,
                        tool_choice="auto",
                        max_tokens=2000,
                        temperature=0.1
                    )
                    selected_model = model
                    print(f"✅ Using model: {model}")
                    break
                except Exception as model_error:
                    print(f"⚠️  Model {model} failed: {str(model_error)[:100]}...")
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
                    
                    print(f"🔧 Executing: {function_name}")
                    if function_args:
                        print(f"   Arguments: {function_args}")
                    
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
                    return f"Tool executed successfully, but final response failed: {str(final_error)}"
            else:
                return message.content
                
        except Exception as e:
            error_msg = str(e)
            if "insufficient_quota" in error_msg:
                return "❌ OpenAI API quota exceeded. Please check your billing at https://platform.openai.com/account/billing"
            elif "invalid_api_key" in error_msg:
                return "❌ Invalid OpenAI API key. Please check your key at https://platform.openai.com/api-keys"
            elif "rate_limit" in error_msg:
                return "❌ Rate limit exceeded. Please wait a moment and try again."
            else:
                return f"❌ OpenAI Error: {error_msg}"
    
    async def interactive_chat(self):
        """Start an interactive chat session"""
        print("OpenAI Database Chat")
        print("=======================")
        print("Chat with your database using OpenAI GPT-4!")
        print("Type 'quit', 'exit', or 'q' to exit")
        print()
        
        conversation_history = []
        
        # Auto-connect to database
        print("Auto-connecting to database...")
        # Just use await directly since we're already in an async function
        connect_result = await self.call_mcp_server("connect_database", {})
        print(f"Connected: {connect_result}")
        print()
        
        while True:
            try:
                user_input = input("💬 You: ").strip()
                
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
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    """Main function"""
    print("Setting up OpenAI Database Chat...")
    
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("ERROR: OPENAI_API_KEY not found!")
        print("Please add your OpenAI API key to the .env file:")
        print("OPENAI_API_KEY=your-api-key-here")
        return
    
    # Load environment
    load_dotenv()
    
    # Create client
    server_script = os.path.join(os.path.dirname(__file__), "server.py")
    
    try:
        client = OpenAIDatabaseClient(server_script)
        
        # Check if we're already in an event loop
        try:
            # Test if event loop is running
            asyncio.get_running_loop()
            print("Event loop detected - using sync wrapper")
            # We're in an event loop, so we need to run in a separate thread
            import threading
            import concurrent.futures
            
            def run_chat():
                # Create new event loop in thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(client.interactive_chat())
                finally:
                    loop.close()
            
            # Run in separate thread
            thread = threading.Thread(target=run_chat)
            thread.daemon = True
            thread.start()
            thread.join()
            
        except RuntimeError:
            # No event loop running, create a new one
            print("Creating new event loop")
            asyncio.run(client.interactive_chat())
    except Exception as e:
        print(f"ERROR: Failed to start: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()