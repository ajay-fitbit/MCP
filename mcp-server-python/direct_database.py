#!/usr/bin/env python3

"""
Direct Database Client - No Server Required

This script provides database access without requiring an MCP server.
It connects directly to SQL Server using pyodbc.
"""

import os
import sys
import json
import asyncio
from typing import Dict, Any, List, Optional, Union
import datetime
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

class DirectDatabaseClient:
    """Direct database client with OpenAI integration"""
    
    def __init__(self):
        """Initialize the direct database client"""
        # Initialize OpenAI client with corporate environment support
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Remove quotes if present
        api_key = api_key.strip('"\'')
        
        # Setup OpenAI with corporate-friendly settings
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
            
        # Initialize database connection
        self.connection = None
        
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
                            "query": {"type": "string", "description": "SQL query to execute"}
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
                            "procedureName": {"type": "string", "description": "Stored procedure name"}
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
    
    async def connect_database(self, server, database):
        """Connect to the database directly"""
        try:
            import pyodbc
        except ImportError:
            return "Error: pyodbc not installed. Please install it with: pip install pyodbc"
        
        try:
            print(f"Connecting to server: {server}, database: {database}")
            
            # Try Windows authentication first
            conn_str = f"Driver={{ODBC Driver 17 for SQL Server}};Server={server};Database={database};Trusted_Connection=yes;"
            
            # Connect to the database
            self.connection = pyodbc.connect(conn_str)
            
            return f"Connected to {database} on {server}"
        except Exception as e:
            print(f"Connection error: {e}")
            return f"Error connecting to database: {str(e)}"
    
    async def execute_query(self, query):
        """Execute a SQL query"""
        if not self.connection:
            return "Error: Not connected to database. Use connect_database first."
            
        try:
            # Execute the query
            cursor = self.connection.cursor()
            cursor.execute(query)
            
            # Get column names
            columns = [column[0] for column in cursor.description]
            
            # Get results
            results = []
            for row in cursor.fetchall():
                # Convert row to dict and handle datetime objects
                row_dict = {}
                for i, value in enumerate(row):
                    if isinstance(value, datetime.datetime):
                        row_dict[columns[i]] = value.isoformat()
                    else:
                        row_dict[columns[i]] = value
                results.append(row_dict)
                
            return json.dumps({"columns": columns, "rows": results}, indent=2)
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
    async def list_tables(self, schema="dbo"):
        """List all tables in the database"""
        if not self.connection:
            return "Error: Not connected to database. Use connect_database first."
            
        try:
            # Query to get all tables
            query = f"""
            SELECT TABLE_SCHEMA, TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
            AND TABLE_SCHEMA = '{schema}'
            ORDER BY TABLE_NAME
            """
            
            # Execute the query
            cursor = self.connection.cursor()
            cursor.execute(query)
            
            # Get results
            tables = [f"{row.TABLE_SCHEMA}.{row.TABLE_NAME}" for row in cursor.fetchall()]
            
            return json.dumps(tables, indent=2)
        except Exception as e:
            return f"Error listing tables: {str(e)}"
    
    async def describe_table(self, tableName, schema="dbo"):
        """Get table schema information"""
        if not self.connection:
            return "Error: Not connected to database. Use connect_database first."
            
        try:
            # Query to get column information
            query = f"""
            SELECT 
                COLUMN_NAME, 
                DATA_TYPE, 
                CHARACTER_MAXIMUM_LENGTH,
                IS_NULLABLE, 
                COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{tableName}'
            AND TABLE_SCHEMA = '{schema}'
            ORDER BY ORDINAL_POSITION
            """
            
            # Execute the query
            cursor = self.connection.cursor()
            cursor.execute(query)
            
            # Get column details
            columns = []
            for row in cursor.fetchall():
                column = {
                    "name": row.COLUMN_NAME,
                    "type": row.DATA_TYPE,
                    "length": row.CHARACTER_MAXIMUM_LENGTH,
                    "nullable": row.IS_NULLABLE,
                    "default": row.COLUMN_DEFAULT
                }
                columns.append(column)
                
            # Query to get primary key information
            query_pk = f"""
            SELECT k.COLUMN_NAME
            FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS c
            JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS k
            ON c.CONSTRAINT_NAME = k.CONSTRAINT_NAME
            WHERE c.CONSTRAINT_TYPE = 'PRIMARY KEY'
            AND k.TABLE_NAME = '{tableName}'
            AND k.TABLE_SCHEMA = '{schema}'
            """
            
            cursor.execute(query_pk)
            primary_keys = [row.COLUMN_NAME for row in cursor.fetchall()]
            
            return json.dumps({
                "table": f"{schema}.{tableName}",
                "columns": columns,
                "primaryKeys": primary_keys
            }, indent=2)
        except Exception as e:
            return f"Error describing table: {str(e)}"
    
    async def execute_stored_procedure(self, procedureName):
        """Execute a stored procedure"""
        if not self.connection:
            return "Error: Not connected to database. Use connect_database first."
            
        try:
            # Execute the stored procedure
            cursor = self.connection.cursor()
            cursor.execute(f"EXEC {procedureName}")
            
            # Get column names if available
            if cursor.description:
                columns = [column[0] for column in cursor.description]
                
                # Get results
                results = []
                for row in cursor.fetchall():
                    # Convert row to dict and handle datetime objects
                    row_dict = {}
                    for i, value in enumerate(row):
                        if isinstance(value, datetime.datetime):
                            row_dict[columns[i]] = value.isoformat()
                        else:
                            row_dict[columns[i]] = value
                    results.append(row_dict)
                    
                return json.dumps({"columns": columns, "rows": results}, indent=2)
            else:
                # No results, but execution succeeded
                return f"Stored procedure {procedureName} executed successfully with no result set."
        except Exception as e:
            return f"Error executing stored procedure: {str(e)}"
    
    async def list_stored_procedures(self, pattern=None):
        """List stored procedures"""
        if not self.connection:
            return "Error: Not connected to database. Use connect_database first."
            
        try:
            # Build query based on pattern
            if pattern:
                query = f"""
                SELECT ROUTINE_SCHEMA, ROUTINE_NAME
                FROM INFORMATION_SCHEMA.ROUTINES
                WHERE ROUTINE_TYPE = 'PROCEDURE'
                AND ROUTINE_NAME LIKE '{pattern}'
                ORDER BY ROUTINE_NAME
                """
            else:
                query = """
                SELECT ROUTINE_SCHEMA, ROUTINE_NAME
                FROM INFORMATION_SCHEMA.ROUTINES
                WHERE ROUTINE_TYPE = 'PROCEDURE'
                ORDER BY ROUTINE_NAME
                """
                
            # Execute the query
            cursor = self.connection.cursor()
            cursor.execute(query)
            
            # Get results
            procedures = [f"{row.ROUTINE_SCHEMA}.{row.ROUTINE_NAME}" for row in cursor.fetchall()]
            
            return json.dumps(procedures, indent=2)
        except Exception as e:
            return f"Error listing stored procedures: {str(e)}"
    
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
                
                # Call the appropriate method based on the function name
                if function_name == "connect_database":
                    server = function_args.get("server", os.getenv('DB_SERVER', 'AHS-LP-945'))
                    database = function_args.get("database", os.getenv('DB_NAME', 'Ahs_Bit_Red_QA_8170'))
                    result = await self.connect_database(server, database)
                
                elif function_name == "execute_query":
                    query = function_args["query"]
                    result = await self.execute_query(query)
                
                elif function_name == "list_tables":
                    schema = function_args.get("schema", "dbo")
                    result = await self.list_tables(schema)
                
                elif function_name == "describe_table":
                    table_name = function_args["tableName"]
                    schema = function_args.get("schema", "dbo")
                    result = await self.describe_table(table_name, schema)
                
                elif function_name == "execute_stored_procedure":
                    procedure_name = function_args["procedureName"]
                    result = await self.execute_stored_procedure(procedure_name)
                
                elif function_name == "list_stored_procedures":
                    pattern = function_args.get("pattern", None)
                    result = await self.list_stored_procedures(pattern)
                
                else:
                    result = f"Unsupported function: {function_name}"
                
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
        print("OpenAI Database Chat (Direct Connection)")
        print("=======================================")
        print("Chat with your database using OpenAI GPT-4!")
        print("Type 'quit' to exit")
        print()
        
        conversation_history = []
        
        # Auto-connect to database
        print("Auto-connecting to database...")
        connect_result = await self.connect_database(
            os.getenv("DB_SERVER", "AHS-LP-945"),
            os.getenv("DB_NAME", "Ahs_Bit_Red_QA_8170")
        )
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
                import traceback
                traceback.print_exc()

async def main():
    """Main function"""
    try:
        client = DirectDatabaseClient()
        await client.interactive_chat()
        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))