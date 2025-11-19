#!/usr/bin/env python3

import os
import sys
import pyodbc
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    """Test database connection"""
    print("🔄 Testing database connection...")
    
    # Get connection details from environment
    server = os.getenv('DB_SERVER', 'localhost')
    database = os.getenv('DB_NAME', 'Ahs_Bit_Red_QA_8170')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    
    print(f"Server: {server}")
    print(f"Database: {database}")
    print(f"User: {user if user else 'Windows Authentication'}")
    
    try:
        # Build connection string
        if user and password:
            # SQL Server authentication
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={user};"
                f"PWD={password};"
                f"Encrypt=yes;"
                f"TrustServerCertificate=yes;"
            )
        else:
            # Windows authentication
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"Trusted_Connection=yes;"
                f"Encrypt=yes;"
                f"TrustServerCertificate=yes;"
            )
        
        # Test connection
        print("🔄 Connecting...")
        conn = pyodbc.connect(conn_str, timeout=30)
        
        print("✅ Connection successful!")
        
        # Test a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION as version")
        version = cursor.fetchone()[0]
        print(f"✅ SQL Server version: {version[:50]}...")
        
        # Test listing tables
        cursor.execute("""
            SELECT COUNT(*) as table_count
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'dbo'
        """)
        table_count = cursor.fetchone()[0]
        print(f"✅ Found {table_count} tables in dbo schema")
        
        # Test if specific tables exist
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'dbo' 
            AND TABLE_NAME IN ('PATIENT_DETAILS', 'CARE_STAFF_DETAILS', 'PATIENT_FOLLOWUP')
        """)
        tables = [row[0] for row in cursor.fetchall()]
        if tables:
            print(f"✅ Found expected tables: {', '.join(tables)}")
        else:
            print("⚠️  Expected tables not found, but connection works")
        
        # Test stored procedures
        cursor.execute("""
            SELECT COUNT(*) as proc_count
            FROM INFORMATION_SCHEMA.ROUTINES 
            WHERE ROUTINE_SCHEMA = 'dbo' AND ROUTINE_TYPE = 'PROCEDURE'
        """)
        proc_count = cursor.fetchone()[0]
        print(f"✅ Found {proc_count} stored procedures")
        
        # Check for specific stored procedure
        cursor.execute("""
            SELECT ROUTINE_NAME
            FROM INFORMATION_SCHEMA.ROUTINES 
            WHERE ROUTINE_SCHEMA = 'dbo' 
            AND ROUTINE_NAME = 'USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET'
        """)
        proc = cursor.fetchone()
        if proc:
            print(f"✅ Found your stored procedure: {proc[0]}")
        else:
            print("⚠️  Your stored procedure not found, but connection works")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 All tests passed! Your database is ready for the MCP server.")
        return True
        
    except pyodbc.Error as e:
        print(f"❌ Database connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def check_drivers():
    """Check available ODBC drivers"""
    print("🔄 Checking available ODBC drivers...")
    drivers = pyodbc.drivers()
    
    sql_server_drivers = [d for d in drivers if 'SQL Server' in d]
    
    if sql_server_drivers:
        print("✅ Found SQL Server ODBC drivers:")
        for driver in sql_server_drivers:
            print(f"  - {driver}")
        return True
    else:
        print("❌ No SQL Server ODBC drivers found!")
        print("Available drivers:")
        for driver in drivers:
            print(f"  - {driver}")
        print("\nPlease install 'ODBC Driver 17 for SQL Server' from Microsoft")
        return False

def main():
    print("=== MCP Database Server - Connection Test ===\n")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  .env file not found. Please copy .env.example to .env and configure it.")
        return False
    
    # Check ODBC drivers
    if not check_drivers():
        return False
    
    print()
    
    # Test connection
    return test_connection()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)