#!/usr/bin/env python3

"""
MCP Server Connection Test Script
This script tests if the MCP server can connect to your database
"""

import os
import sys
import pyodbc
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test connection to SQL Server database"""
    
    # Get connection details
    server = os.getenv('DB_SERVER', 'AHS-LP-945')
    database = os.getenv('DB_NAME', 'Ahs_Bit_Red_QA_8170')
    user = os.getenv('DB_USER', '')
    password = os.getenv('DB_PASSWORD', '')
    
    print(f"Testing connection to {database} on {server}")
    
    try:
        # Build connection string
        if user and password:
            conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'
        else:
            conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
        
        # Connect to database
        conn = pyodbc.connect(conn_str, timeout=10)
        print(f"✅ Connected to database successfully!")
        
        # Test a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES")
        table_count = cursor.fetchone()[0]
        print(f"✅ Database query successful - found {table_count} tables")
        
        # Test a more detailed query
        cursor.execute("""
            SELECT TOP 5
                TABLE_SCHEMA,
                TABLE_NAME,
                TABLE_TYPE
            FROM INFORMATION_SCHEMA.TABLES
            ORDER BY TABLE_NAME
        """)
        
        print("\nSample tables:")
        for row in cursor.fetchall():
            print(f"  - {row.TABLE_SCHEMA}.{row.TABLE_NAME} ({row.TABLE_TYPE})")
        
        # Close connection
        conn.close()
        print("\nDatabase connection test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to database: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== MCP Server Database Connection Test ===\n")
    
    success = test_database_connection()
    
    if success:
        print("\n✅ ALL TESTS PASSED - MCP Server can connect to your database")
        sys.exit(0)
    else:
        print("\n❌ CONNECTION FAILED - Check your database settings")
        sys.exit(1)