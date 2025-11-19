#!/usr/bin/env python3

"""
MCP Client for connecting to a running MCP server

This is a lightweight client that can connect to an MCP server using HTTP.
"""

import json
import os
import sys
import asyncio
import subprocess
from typing import Dict, Any, List, Optional, Union

class MCPClient:
    """Client for connecting to an MCP server"""
    
    def __init__(self, url: str = "http://localhost:8765"):
        """Initialize with server URL"""
        self.url = url
        
    async def call(self, method: str, params: Dict[str, Any]) -> Union[Dict, List, str]:
        """Call an MCP method on the server"""
        # Try to use aiohttp for proper async HTTP
        try:
            import aiohttp
            return await self._call_aiohttp(method, params)
        except ImportError:
            # Fall back to subprocess curl if aiohttp not available
            return await self._call_subprocess(method, params)
            
    async def _call_aiohttp(self, method: str, params: Dict[str, Any]) -> Union[Dict, List, str]:
        """Call using aiohttp"""
        import aiohttp
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.url}/{method}", 
                    json=params,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error = await response.text()
                        raise Exception(f"Server error ({response.status}): {error}")
        except Exception as e:
            # Log error but don't raise - will try subprocess as fallback
            print(f"aiohttp request failed: {e}")
            return await self._call_subprocess(method, params)
    
    async def _call_subprocess(self, method: str, params: Dict[str, Any]) -> Union[Dict, List, str]:
        """Call using curl subprocess as fallback"""
        try:
            # Create a temporary file for the request body
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                json.dump(params, f)
                temp_file = f.name
                
            # Build the curl command
            curl_cmd = [
                "curl", "-s", "-X", "POST",
                "-H", "Content-Type: application/json",
                "-d", f"@{temp_file}",
                f"{self.url}/{method}"
            ]
            
            # Execute the command
            proc = await asyncio.create_subprocess_exec(
                *curl_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await proc.communicate()
            
            # Clean up temp file
            try:
                os.unlink(temp_file)
            except:
                pass
                
            if proc.returncode != 0:
                raise Exception(f"Curl failed: {stderr.decode()}")
                
            # Parse the response
            response_text = stdout.decode()
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                return response_text
                
        except Exception as e:
            return f"Error calling server: {str(e)}"
            
    # Convenience methods for common operations
    async def connect_database(self, server=None, database=None, user=None, password=None):
        """Connect to a database"""
        params = {}
        if server:
            params["server"] = server
        if database:
            params["database"] = database
        if user:
            params["user"] = user
        if password:
            params["password"] = password
            
        return await self.call("connect_database", params)
        
    async def list_tables(self, schema=None):
        """List all tables"""
        params = {}
        if schema:
            params["schema"] = schema
            
        return await self.call("list_tables", params)
        
    async def describe_table(self, table_name, schema=None):
        """Get details of a table"""
        params = {"tableName": table_name}
        if schema:
            params["schema"] = schema
            
        return await self.call("describe_table", params)
        
    async def execute_query(self, query, parameters=None):
        """Execute a SQL query"""
        params = {"query": query}
        if parameters:
            params["parameters"] = parameters
            
        return await self.call("execute_query", params)
        
    async def execute_stored_procedure(self, procedure_name, parameters=None):
        """Execute a stored procedure"""
        params = {"procedureName": procedure_name}
        if parameters:
            params["parameters"] = parameters
            
        return await self.call("execute_stored_procedure", params)
        
    async def list_stored_procedures(self, pattern=None):
        """List stored procedures"""
        params = {}
        if pattern:
            params["pattern"] = pattern
            
        return await self.call("list_stored_procedures", params)