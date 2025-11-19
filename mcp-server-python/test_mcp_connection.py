#!/usr/bin/env python3

"""
Direct MCP Server Connection Client

This script connects to an already running MCP server.
"""

import os
import sys
import asyncio
import json
from mcp_client import MCPClient  # We'll create this client

# Main entry point
async def main():
    """Connect to the running MCP server and test it"""
    print("MCP Server Connection Test")
    print("==========================")
    
    try:
        # Create client
        print("Connecting to MCP server...")
        client = MCPClient("http://localhost:8000")
        
        # Test connection
        print("Testing connection...")
        result = await client.call("connect_database", {
            "server": os.getenv("DB_SERVER", "AHS-LP-945"),
            "database": os.getenv("DB_NAME", "Ahs_Bit_Red_QA_8170"),
            "user": os.getenv("DB_USER", ""),
            "password": os.getenv("DB_PASSWORD", "")
        })
        
        print(f"Connection result: {result}")
        
        # List tables
        print("Listing tables...")
        tables = await client.call("list_tables", {})
        
        if isinstance(tables, str):
            tables = json.loads(tables)
            
        print(f"Found {len(tables)} tables")
        print("First 5 tables:")
        for table in tables[:5]:
            print(f"  - {table}")
            
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

# Create simple MCP client
class MCPClient:
    """Simple MCP client to connect to a running server"""
    
    def __init__(self, url):
        """Initialize client with server URL"""
        self.url = url
        
    async def call(self, method, params):
        """Call MCP server method"""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.url}/api/{method}",
                    json=params,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        raise Exception(f"Server error ({response.status}): {error_text}")
                        
        except ImportError:
            print("Error: aiohttp package not installed.")
            print("Please install it with: pip install aiohttp")
            raise

if __name__ == "__main__":
    asyncio.run(main())