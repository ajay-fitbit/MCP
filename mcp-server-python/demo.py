#!/usr/bin/env python3

import asyncio
import json
import os
from client import DatabaseMCPClient
from dotenv import load_dotenv

async def demo_database_operations():
    """Demonstrate all database operations"""
    print("🎯 MCP Database Demo")
    print("===================")
    
    # Load environment
    load_dotenv()
    
    # Create client
    server_script = os.path.join(os.path.dirname(__file__), "server.py")
    client = DatabaseMCPClient(server_script)
    
    try:
        # Connect to MCP server
        print("\n1️⃣ Connecting to MCP Server...")
        if not await client.connect():
            print("❌ Failed to connect to MCP server")
            return
        
        # List available tools
        print("\n2️⃣ Available Tools:")
        tools = await client.list_tools()
        for tool in tools:
            print(f"   🔧 {tool.name}")
        
        # Connect to database
        print("\n3️⃣ Connecting to Database...")
        server = os.getenv('DB_SERVER', 'localhost')
        database = os.getenv('DB_NAME', 'Ahs_Bit_Red_QA_8170')
        user = os.getenv('DB_USER', '')
        password = os.getenv('DB_PASSWORD', '')
        
        connect_args = {"server": server, "database": database}
        if user and password:
            connect_args.update({"user": user, "password": password})
        
        result = await client.call_tool("connect_database", connect_args)
        if result:
            print(f"✅ {result[0].text}")
        else:
            print("❌ Failed to connect to database")
            return
        
        # List tables
        print("\n4️⃣ Listing Tables...")
        result = await client.call_tool("list_tables", {"schema": "dbo"})
        if result:
            data = json.loads(result[0].text)
            print(f"✅ Found {len(data)} tables")
            for table in data[:5]:  # Show first 5
                print(f"   📊 {table['TABLE_NAME']}")
        
        # Test a simple query
        print("\n5️⃣ Testing Simple Query...")
        result = await client.call_tool("execute_query", {
            "query": "SELECT @@VERSION as ServerVersion"
        })
        if result:
            data = json.loads(result[0].text)
            if data['recordset']:
                version = data['recordset'][0]['ServerVersion']
                print(f"✅ SQL Server: {version[:50]}...")
        
        # List stored procedures
        print("\n6️⃣ Listing Stored Procedures...")
        result = await client.call_tool("list_stored_procedures", {"schema": "dbo"})
        if result:
            data = json.loads(result[0].text)
            print(f"✅ Found {len(data)} stored procedures")
            
            # Look for your specific procedure
            your_proc = None
            for proc in data:
                if proc['ROUTINE_NAME'] == 'USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET':
                    your_proc = proc
                    break
            
            if your_proc:
                print(f"🎯 Found your procedure: {your_proc['ROUTINE_NAME']}")
                
                # Test your stored procedure
                print("\n7️⃣ Testing Your Stored Procedure...")
                result = await client.call_tool("execute_stored_procedure", {
                    "procedureName": "USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET",
                    "parameters": {
                        "LOGIN_USERID": 68,
                        "PAGE_NUMBER": 1,
                        "PAGE_SIZE": 5,  # Small number for demo
                        "ORDER_BY_FIELD": "TREATMENT_TYPE_NAME",
                        "SORT_ORDER": "DESC"
                    }
                })
                
                if result:
                    data = json.loads(result[0].text)
                    recordsets = data.get('recordsets', [])
                    if recordsets and recordsets[0].get('data'):
                        rows = recordsets[0]['data']
                        print(f"✅ Procedure returned {len(rows)} rows")
                        if rows:
                            print("   📋 Sample data columns:")
                            for key in list(rows[0].keys())[:5]:  # Show first 5 columns
                                print(f"      • {key}")
                    else:
                        print("✅ Procedure executed (no data returned)")
            else:
                print("⚠️  Your stored procedure not found")
        
        # Check specific tables that might exist
        print("\n8️⃣ Checking Expected Tables...")
        expected_tables = ['PATIENT_DETAILS', 'CARE_STAFF_DETAILS', 'PATIENT_FOLLOWUP']
        
        for table_name in expected_tables:
            try:
                result = await client.call_tool("describe_table", {
                    "tableName": table_name,
                    "schema": "dbo"
                })
                if result:
                    data = json.loads(result[0].text)
                    columns = data.get('columns', [])
                    print(f"✅ {table_name}: {len(columns)} columns")
            except:
                print(f"⚠️  {table_name}: Not found or no access")
        
        # Disconnect
        print("\n9️⃣ Disconnecting...")
        result = await client.call_tool("disconnect_database")
        if result:
            print(f"✅ {result[0].text}")
        
        print("\n🎉 Demo completed successfully!")
        print("\n💡 Next steps:")
        print("   • Run 'start_client.bat' for interactive mode")
        print("   • Configure Claude Desktop to use this MCP server")
        print("   • Customize the server for your specific needs")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    
    finally:
        # Clean up
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(demo_database_operations())