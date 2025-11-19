#!/usr/bin/env python3

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict, List, Optional
import os

# Import MCP client SDK
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class DatabaseMCPClient:
    def __init__(self, server_script_path: str):
        self.server_script_path = server_script_path
        self.session = None
        self.connected = False
    
    async def connect(self):
        """Connect to the MCP server"""
        try:
            # Get the Python executable path
            python_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.venv', 'Scripts', 'python.exe')
            
            server_params = StdioServerParameters(
                command=python_path,
                args=[self.server_script_path],
                env=None
            )
            
            # Use async context manager properly
            stdio_context = stdio_client(server_params)
            self.session = await stdio_context.__aenter__()
            await self.session.initialize()
            
            self.connected = True
            print("✅ Connected to MCP Database Server")
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect to server: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from the MCP server"""
        if self.session:
            await self.session.close()
            self.connected = False
            print("✅ Disconnected from server")
    
    async def list_tools(self):
        """List available tools"""
        if not self.connected:
            print("❌ Not connected to server")
            return []
        
        try:
            response = await self.session.list_tools()
            return response.tools
        except Exception as e:
            print(f"❌ Failed to list tools: {e}")
            return []
    
    async def call_tool(self, name: str, arguments: Dict[str, Any] = None):
        """Call a tool on the server"""
        if not self.connected:
            print("❌ Not connected to server")
            return None
        
        try:
            if arguments is None:
                arguments = {}
            
            print(f"🔄 Calling tool: {name}")
            if arguments:
                print(f"   Arguments: {json.dumps(arguments, indent=2)}")
            
            response = await self.session.call_tool(name, arguments)
            
            return response.content
            
        except Exception as e:
            print(f"❌ Failed to call tool {name}: {e}")
            return None
    
    async def interactive_session(self):
        """Start an interactive session"""
        print("\n" + "="*60)
        print("🎯 MCP Database Client - Interactive Session")
        print("="*60)
        
        if not await self.connect():
            return
        
        # List available tools
        print("\n📋 Available Tools:")
        tools = await self.list_tools()
        for i, tool in enumerate(tools, 1):
            print(f"  {i}. {tool.name} - {tool.description}")
        
        print("\n💡 Example commands:")
        print("  connect - Connect to database")
        print("  tables - List all tables")
        print("  query - Execute a SQL query")
        print("  sp - Execute your stored procedure")
        print("  help - Show this help")
        print("  quit - Exit the client")
        
        while True:
            try:
                print("\n" + "-"*40)
                command = input("🎯 Enter command: ").strip().lower()
                
                if command in ['quit', 'exit', 'q']:
                    break
                elif command == 'help':
                    await self.show_help()
                elif command == 'connect':
                    await self.connect_to_database()
                elif command == 'tables':
                    await self.list_tables()
                elif command == 'query':
                    await self.execute_query()
                elif command == 'sp':
                    await self.execute_stored_procedure()
                elif command == 'disconnect':
                    await self.disconnect_database()
                elif command == 'describe':
                    await self.describe_table()
                elif command == 'procedures':
                    await self.list_procedures()
                else:
                    print(f"❌ Unknown command: {command}")
                    print("   Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Exiting...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        await self.disconnect()
    
    async def show_help(self):
        """Show help information"""
        print("\n📚 Available Commands:")
        print("  connect     - Connect to your database")
        print("  tables      - List all tables in the database")
        print("  describe    - Describe a specific table")
        print("  query       - Execute a custom SQL query")
        print("  sp          - Execute USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET")
        print("  procedures  - List all stored procedures")
        print("  disconnect  - Disconnect from database")
        print("  help        - Show this help")
        print("  quit        - Exit the client")
    
    async def connect_to_database(self):
        """Connect to the database using environment settings"""
        print("\n🔄 Connecting to database using .env settings...")
        
        # Read from .env file or use defaults
        server = os.getenv('DB_SERVER', 'localhost')
        database = os.getenv('DB_NAME', 'Ahs_Bit_Red_QA_8170')
        user = os.getenv('DB_USER', '')
        password = os.getenv('DB_PASSWORD', '')
        
        print(f"   Server: {server}")
        print(f"   Database: {database}")
        print(f"   Authentication: {'Windows' if not user else 'SQL Server'}")
        
        arguments = {
            "server": server,
            "database": database
        }
        
        if user and password:
            arguments["user"] = user
            arguments["password"] = password
        
        result = await self.call_tool("connect_database", arguments)
        if result:
            for content in result:
                print(f"✅ {content.text}")
    
    async def list_tables(self):
        """List all tables"""
        print("\n📋 Listing tables...")
        result = await self.call_tool("list_tables", {"schema": "dbo"})
        if result:
            for content in result:
                data = json.loads(content.text)
                print(f"✅ Found {len(data)} tables:")
                for table in data[:10]:  # Show first 10 tables
                    print(f"   📊 {table['TABLE_SCHEMA']}.{table['TABLE_NAME']} ({table['TABLE_TYPE']})")
                if len(data) > 10:
                    print(f"   ... and {len(data) - 10} more tables")
    
    async def describe_table(self):
        """Describe a specific table"""
        table_name = input("\n📊 Enter table name (e.g., PATIENT_DETAILS): ").strip()
        if not table_name:
            print("❌ Table name is required")
            return
        
        print(f"\n🔍 Describing table: {table_name}")
        result = await self.call_tool("describe_table", {"tableName": table_name, "schema": "dbo"})
        if result:
            for content in result:
                data = json.loads(content.text)
                print(f"✅ Table: {data['table']}")
                print("\n📋 Columns:")
                for col in data['columns']:
                    nullable = "NULL" if col['IS_NULLABLE'] == 'YES' else "NOT NULL"
                    print(f"   🔸 {col['COLUMN_NAME']} ({col['DATA_TYPE']}) {nullable}")
    
    async def execute_query(self):
        """Execute a custom SQL query"""
        print("\n💡 Examples:")
        print("   SELECT TOP 10 * FROM PATIENT_DETAILS")
        print("   SELECT COUNT(*) FROM CARE_STAFF_DETAILS")
        
        query = input("\n📝 Enter SQL query: ").strip()
        if not query:
            print("❌ Query is required")
            return
        
        print(f"\n🔄 Executing query...")
        result = await self.call_tool("execute_query", {"query": query})
        if result:
            for content in result:
                data = json.loads(content.text)
                print(f"✅ Query executed successfully")
                print(f"   Rows affected: {data.get('rowsAffected', 0)}")
                
                recordset = data.get('recordset', [])
                if recordset:
                    print(f"   Results: {len(recordset)} rows")
                    # Show first few rows
                    for i, row in enumerate(recordset[:5]):
                        print(f"   Row {i+1}: {row}")
                    if len(recordset) > 5:
                        print(f"   ... and {len(recordset) - 5} more rows")
    
    async def execute_stored_procedure(self):
        """Execute the USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET stored procedure"""
        print("\n🔧 Executing USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET")
        
        # Get user input for key parameters
        user_id = input("   Enter LOGIN_USERID (default: 68): ").strip() or "68"
        page_size = input("   Enter PAGE_SIZE (default: 20): ").strip() or "20"
        
        parameters = {
            "LOGIN_USERID": int(user_id),
            "PAGE_NUMBER": 1,
            "PAGE_SIZE": int(page_size),
            "ORDER_BY_FIELD": "TREATMENT_TYPE_NAME",
            "SORT_ORDER": "DESC"
        }
        
        print(f"\n🔄 Calling stored procedure with parameters:")
        for key, value in parameters.items():
            print(f"   {key}: {value}")
        
        result = await self.call_tool("execute_stored_procedure", {
            "procedureName": "USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET",
            "parameters": parameters
        })
        
        if result:
            for content in result:
                data = json.loads(content.text)
                print(f"✅ Stored procedure executed successfully")
                
                recordsets = data.get('recordsets', [])
                if recordsets:
                    for i, rs in enumerate(recordsets):
                        print(f"\n📊 Result Set {i+1}:")
                        rows = rs.get('data', [])
                        print(f"   Rows: {len(rows)}")
                        if rows:
                            # Show first few rows
                            for j, row in enumerate(rows[:3]):
                                print(f"   Row {j+1}: {row}")
                            if len(rows) > 3:
                                print(f"   ... and {len(rows) - 3} more rows")
    
    async def list_procedures(self):
        """List all stored procedures"""
        print("\n🔧 Listing stored procedures...")
        result = await self.call_tool("list_stored_procedures", {"schema": "dbo"})
        if result:
            for content in result:
                data = json.loads(content.text)
                print(f"✅ Found {len(data)} stored procedures:")
                for proc in data[:10]:  # Show first 10
                    print(f"   🔧 {proc['ROUTINE_NAME']}")
                if len(data) > 10:
                    print(f"   ... and {len(data) - 10} more procedures")
    
    async def disconnect_database(self):
        """Disconnect from database"""
        print("\n🔄 Disconnecting from database...")
        result = await self.call_tool("disconnect_database")
        if result:
            for content in result:
                print(f"✅ {content.text}")


async def main():
    """Main function"""
    print("🎯 MCP Database Client")
    print("======================")
    
    # Path to the server script
    server_script = os.path.join(os.path.dirname(__file__), "server.py")
    
    if not os.path.exists(server_script):
        print(f"❌ Server script not found: {server_script}")
        return
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    client = DatabaseMCPClient(server_script)
    await client.interactive_session()


if __name__ == "__main__":
    asyncio.run(main())