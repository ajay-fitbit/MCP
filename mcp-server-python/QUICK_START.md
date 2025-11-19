# 🐍 Python MCP Server Setup Guide

## Quick Start (5 Steps)

### 1. ✅ Dependencies Installed
Your Python environment and packages are already set up!

### 2. 🔧 Configure Database Connection
Edit the `.env` file with your SQL Server details:

```env
# For SQL Server Authentication:
DB_SERVER=your-server-name-or-ip
DB_NAME=Ahs_Bit_Red_QA_8170
DB_USER=your-username
DB_PASSWORD=your-password

# For Windows Authentication (leave user/password empty):
DB_SERVER=localhost\SQLEXPRESS
DB_NAME=Ahs_Bit_Red_QA_8170
# DB_USER=
# DB_PASSWORD=
```

### 3. 🧪 Test Connection
Double-click: `test_connection.bat`

Or run manually:
```bash
python test_connection.py
```

### 4. 🚀 Start the Server
Double-click: `start_server.bat`

Or run manually:
```bash
python server.py
```

### 5. 🎯 Use with MCP Client
The server is now ready to accept MCP connections!

## 📊 Your Database Tools

Once connected, you can:

### Execute Your Stored Procedure:
```json
{
  "tool": "execute_stored_procedure",
  "arguments": {
    "procedureName": "USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET",
    "parameters": {
      "LOGIN_USERID": 68,
      "PAGE_NUMBER": 1,
      "PAGE_SIZE": 20,
      "ORDER_BY_FIELD": "TREATMENT_TYPE_NAME",
      "SORT_ORDER": "DESC"
    }
  }
}
```

### Query Your Tables:
```json
{
  "tool": "execute_query",
  "arguments": {
    "query": "SELECT TOP 10 * FROM PATIENT_DETAILS WHERE DELETED_BY IS NULL"
  }
}
```

### List All Tables:
```json
{
  "tool": "list_tables",
  "arguments": {
    "schema": "dbo"
  }
}
```

## 🔍 Troubleshooting

### ❌ "ODBC Driver not found"
Install Microsoft ODBC Driver 17 for SQL Server:
- Download: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

### ❌ "Login failed"
1. Check your username/password in `.env`
2. Verify the user has access to the database
3. Try Windows Authentication (leave user/password empty)

### ❌ "Server not found"
1. Check if SQL Server is running
2. Verify server name/IP address
3. Check firewall settings
4. Ensure SQL Server accepts remote connections

### ❌ "Database not found"
1. Verify the database name is correct
2. Check if the user has access to that specific database

## 🎉 Why Python is Better for You

- ✅ **No build step** - Just run the Python file
- ✅ **Easy to modify** - Python is readable and flexible
- ✅ **Better error messages** - Clear debugging information
- ✅ **Mature database support** - pyodbc is battle-tested
- ✅ **Cross-platform** - Works everywhere Python works

## 📁 Files Overview

```
mcp-server-python/
├── server.py              # 🎯 Main MCP server
├── test_connection.py     # 🧪 Database connection test
├── start_server.bat       # 🚀 Easy server launcher
├── test_connection.bat    # 🧪 Easy connection test
├── .env                   # 🔧 Your database config
└── README.md              # 📖 Full documentation
```

## 🔗 Next Steps

1. **Test the connection** with `test_connection.bat`
2. **Start the server** with `start_server.bat`
3. **Configure your MCP client** (like Claude Desktop) to use this server
4. **Start querying your database** with natural language!

---

Need help? Check the full README.md or run the test scripts to diagnose issues!