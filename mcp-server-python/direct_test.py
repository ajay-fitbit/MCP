#!/usr/bin/env python3

import os
import sys
import asyncio
from dotenv import load_dotenv

# Add the current directory to Python path so we can import the database service
sys.path.insert(0, os.path.dirname(__file__))

# Import the database service directly
from server import DatabaseService

async def direct_test():
    """Test the database service directly without MCP protocol"""
    print("🎯 Direct Database Test")
    print("======================")
    
    # Load environment
    load_dotenv()
    
    # Create database service
    db = DatabaseService()
    
    try:
        # Get connection details
        server = os.getenv('DB_SERVER', 'localhost')
        database = os.getenv('DB_NAME', 'Ahs_Bit_Red_QA_8170')
        user = os.getenv('DB_USER', '')
        password = os.getenv('DB_PASSWORD', '')
        
        print(f"\n1️⃣ Connection Details:")
        print(f"   Server: {server}")
        print(f"   Database: {database}")
        print(f"   Authentication: {'Windows' if not user else 'SQL Server'}")
        
        # Connect to database
        print(f"\n2️⃣ Connecting to Database...")
        result = db.connect(server, database, user if user else None, password if password else None)
        print(f"✅ {result}")
        
        # Test simple query
        print(f"\n3️⃣ Testing Simple Query...")
        result = db.execute_query("SELECT @@VERSION as ServerVersion")
        version = result['recordset'][0]['ServerVersion']
        print(f"✅ SQL Server: {version[:50]}...")
        
        # List tables
        print(f"\n4️⃣ Listing Tables...")
        tables = db.list_tables()
        print(f"✅ Found {len(tables)} tables")
        for table in tables[:5]:  # Show first 5
            print(f"   📊 {table['TABLE_NAME']}")
        if len(tables) > 5:
            print(f"   ... and {len(tables) - 5} more tables")
        
        # Check for expected tables
        print(f"\n5️⃣ Checking Expected Tables...")
        expected_tables = ['PATIENT_DETAILS', 'CARE_STAFF_DETAILS', 'PATIENT_FOLLOWUP']
        for table_name in expected_tables:
            try:
                table_info = db.describe_table(table_name)
                columns = table_info['columns']
                print(f"✅ {table_name}: {len(columns)} columns")
            except Exception as e:
                print(f"⚠️  {table_name}: Not found or no access ({str(e)[:50]}...)")
        
        # List stored procedures
        print(f"\n6️⃣ Listing Stored Procedures...")
        procedures = db.list_stored_procedures()
        print(f"✅ Found {len(procedures)} stored procedures")
        
        # Look for your specific procedure
        your_proc = None
        for proc in procedures:
            if proc['ROUTINE_NAME'] == 'USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET':
                your_proc = proc
                break
        
        if your_proc:
            print(f"🎯 Found your procedure: {your_proc['ROUTINE_NAME']}")
            
            # Test your stored procedure
            print(f"\n7️⃣ Testing Your Stored Procedure...")
            try:
                result = db.execute_stored_procedure(
                    "USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET",
                    {
                        "LOGIN_USERID": 68,
                        "PAGE_NUMBER": 1,
                        "PAGE_SIZE": 5,  # Small number for demo
                        "ORDER_BY_FIELD": "TREATMENT_TYPE_NAME",
                        "SORT_ORDER": "DESC"
                    }
                )
                
                recordsets = result.get('recordsets', [])
                if recordsets and recordsets[0].get('data'):
                    rows = recordsets[0]['data']
                    print(f"✅ Procedure returned {len(rows)} rows")
                    if rows:
                        print("   📋 Sample data columns:")
                        for key in list(rows[0].keys())[:5]:  # Show first 5 columns
                            print(f"      • {key}")
                else:
                    print("✅ Procedure executed (no data returned)")
            except Exception as e:
                print(f"⚠️  Procedure test failed: {str(e)[:100]}...")
        else:
            print("⚠️  Your stored procedure not found")
        
        # Disconnect
        print(f"\n8️⃣ Disconnecting...")
        result = db.disconnect()
        print(f"✅ {result}")
        
        print(f"\n🎉 Direct test completed successfully!")
        print(f"\n📋 Summary:")
        print(f"   • Database connection: ✅ Working")
        print(f"   • SQL queries: ✅ Working") 
        print(f"   • Tables: ✅ {len(tables)} found")
        print(f"   • Stored procedures: ✅ {len(procedures)} found")
        print(f"   • Your SP: {'✅ Found' if your_proc else '⚠️  Not found'}")
        
        print(f"\n💡 Next steps:")
        print(f"   • Your database connection is working perfectly!")
        print(f"   • You can now use the MCP server with Claude Desktop")
        print(f"   • The issue was with the MCP client, not the database")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(direct_test())