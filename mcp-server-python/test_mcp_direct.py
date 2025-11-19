#!/usr/bin/env python3
"""Direct test of MCP server using stdio communication"""

import asyncio
import json
import os
import sys

async def test_mcp_server():
    """Test the MCP server directly"""
    print("="*60)
    print("🧪 Testing MCP Server (Direct stdio communication)")
    print("="*60)
    
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    python_path = os.path.join(os.path.dirname(script_dir), '.venv', 'Scripts', 'python.exe')
    server_path = os.path.join(script_dir, 'server.py')
    
    print(f"\n📍 Python: {python_path}")
    print(f"📍 Server: {server_path}")
    
    try:
        # Start the MCP server process
        print("\n🚀 Starting MCP server...")
        process = await asyncio.create_subprocess_exec(
            python_path,
            server_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={
                **os.environ,
                'DB_SERVER': 'AHS-LP-945',
                'DB_NAME': 'Ahs_Bit_Red_QA_8170'
            }
        )
        
        print("✅ Server process started")
        
        # Step 1: Initialize the connection
        print("\n📡 Step 1: Initializing MCP connection...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        # Send initialization
        init_json = json.dumps(init_request) + '\n'
        process.stdin.write(init_json.encode())
        await process.stdin.drain()
        
        # Read initialization response
        init_response_line = await asyncio.wait_for(process.stdout.readline(), timeout=5.0)
        init_response = json.loads(init_response_line.decode())
        
        if "result" in init_response:
            print("✅ Initialization successful")
            print(f"   Protocol version: {init_response['result'].get('protocolVersion')}")
            print(f"   Server: {init_response['result'].get('serverInfo', {}).get('name')}")
        else:
            print(f"❌ Initialization failed: {init_response.get('error')}")
            return
        
        # Step 2: Send initialized notification
        print("\n📡 Step 2: Sending initialized notification...")
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        
        notif_json = json.dumps(initialized_notification) + '\n'
        process.stdin.write(notif_json.encode())
        await process.stdin.drain()
        print("✅ Notification sent")
        
        # Step 3: List available tools
        print("\n📡 Step 3: Listing available tools...")
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        list_json = json.dumps(list_tools_request) + '\n'
        process.stdin.write(list_json.encode())
        await process.stdin.drain()
        
        # Read tools list response
        tools_response_line = await asyncio.wait_for(process.stdout.readline(), timeout=5.0)
        tools_response = json.loads(tools_response_line.decode())
        
        if "result" in tools_response and "tools" in tools_response["result"]:
            tools = tools_response["result"]["tools"]
            print(f"✅ Found {len(tools)} tools:")
            for i, tool in enumerate(tools, 1):
                print(f"   {i}. {tool['name']}")
                print(f"      {tool['description']}")
        else:
            print(f"❌ Failed to list tools: {tools_response.get('error')}")
            return
        
        # Step 4: Connect to database
        print("\n📡 Step 4: Connecting to database...")
        connect_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "connect_database",
                "arguments": {
                    "server": "AHS-LP-945",
                    "database": "Ahs_Bit_Red_QA_8170"
                }
            }
        }
        
        connect_json = json.dumps(connect_request) + '\n'
        process.stdin.write(connect_json.encode())
        await process.stdin.drain()
        
        # Read connection response
        connect_response_line = await asyncio.wait_for(process.stdout.readline(), timeout=10.0)
        connect_response = json.loads(connect_response_line.decode())
        
        if "result" in connect_response:
            print("✅ Database connection successful!")
            content = connect_response["result"].get("content", [])
            if content:
                for item in content:
                    if item.get("type") == "text":
                        print(f"   {item.get('text')}")
        else:
            print(f"❌ Connection failed: {connect_response.get('error')}")
            return
        
        # Step 5: List tables
        print("\n📡 Step 5: Listing database tables...")
        list_tables_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "list_tables",
                "arguments": {
                    "schema": "dbo"
                }
            }
        }
        
        tables_json = json.dumps(list_tables_request) + '\n'
        process.stdin.write(tables_json.encode())
        await process.stdin.drain()
        
        # Read tables response
        tables_response_line = await asyncio.wait_for(process.stdout.readline(), timeout=10.0)
        tables_response = json.loads(tables_response_line.decode())
        
        if "result" in tables_response:
            print("✅ Tables retrieved:")
            content = tables_response["result"].get("content", [])
            if content:
                for item in content:
                    if item.get("type") == "text":
                        text = item.get('text', '')
                        # Show first few tables
                        lines = text.split('\n')
                        for line in lines[:10]:
                            if line.strip():
                                print(f"   {line}")
                        if len(lines) > 10:
                            print(f"   ... and {len(lines) - 10} more tables")
        else:
            print(f"❌ Failed to list tables: {tables_response.get('error')}")
        
        print("\n" + "="*60)
        print("✅ MCP Server Test Complete!")
        print("="*60)
        
        # Cleanup
        process.stdin.close()
        await process.wait()
        
    except asyncio.TimeoutError:
        print("❌ Timeout waiting for server response")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if process:
            try:
                process.terminate()
                await process.wait()
            except:
                pass

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
