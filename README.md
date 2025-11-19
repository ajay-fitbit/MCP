# Database MCP Server (Python)

A Python-based Model Context Protocol (MCP) server for Microsoft SQL Server database operations. This server provides tools for connecting to and interacting with SQL Server databases through the MCP protocol.

## Features

- 🔗 Connect to SQL Server databases (Windows Auth & SQL Auth)
- 📊 Execute SQL queries with parameterized query support
- 📋 List tables and describe table structures
- 🔧 List and execute stored procedures
- 🛡️ Secure database connection management
- 🐍 Pure Python implementation (easier to customize)

## Prerequisites

- Python 3.8 or higher
- Microsoft ODBC Driver 17 for SQL Server
- Access to a Microsoft SQL Server database

## Quick Installation

1. **Navigate to the Python server directory:**
   ```bash
   cd mcp-server-python
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install ODBC Driver (if not already installed):**
   - Download from: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
   - Or use chocolatey: `choco install sqlserver-odbcdriver`

4. **Configure your database connection:**
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` with your database details:
   ```env
   DB_SERVER=your-server-name
   DB_NAME=ur-db-name
   DB_USER=your-username
   DB_PASSWORD=your-password
   ```

5. **Test the connection:**
   ```bash
   python test_connection.py
   ```

6. **Run the MCP server:**
   ```bash
   python server.py
   ```

## Database Connection Examples

### SQL Server Authentication:
```env
DB_SERVER=localhost
DB_NAME=ur-db-name
DB_USER=sa
DB_PASSWORD=your-password
```

### Windows Authentication:
```env
DB_SERVER=localhost\\SQLEXPRESS
DB_NAME=ur-db-name
# Leave DB_USER and DB_PASSWORD empty for Windows Auth
```

### Remote SQL Server:
```env
DB_SERVER=192.168.1.100
DB_NAME=ur-db-name
DB_USER=your-username
DB_PASSWORD=your-password
```

## Available Tools

### 1. connect_database
Connect to a SQL Server database.

### 2. execute_query
Execute SQL queries with optional parameters.

### 3. list_tables
List all tables in a specific schema.

### 4. describe_table
Get detailed table information (columns, indexes, etc.).

### 5. list_stored_procedures
List all stored procedures in a schema.

### 6. execute_stored_procedure
Execute stored procedures with parameters.

### 7. disconnect_database
Safely disconnect from the database.

## Testing Your Stored Procedures

Your existing stored procedure can be executed like this:

```python
# Example: Execute ur-procedure-name
{
  "tool": "execute_stored_procedure",
  "arguments": {
    "procedureName": "ur-procedure-name",
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

## File Structure

```
mcp-server-python/
├── server.py              # Main MCP server
├── test_connection.py     # Connection test script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .env                  # Your configuration
└── README.md             # This file
```

## Advantages of Python Version

- ✅ **Easier to read and modify** - Python is more accessible
- ✅ **Better error messages** - More descriptive error handling
- ✅ **No build step required** - Run directly with Python
- ✅ **Extensive SQL Server support** - Mature pyodbc library
- ✅ **Cross-platform** - Works on Windows, Linux, macOS

## Troubleshooting

### ODBC Driver Issues
```bash
# Check available drivers
python -c "import pyodbc; print(pyodbc.drivers())"
```

### Connection Issues
1. Run the test script: `python test_connection.py`
2. Check if SQL Server is running
3. Verify firewall settings
4. Ensure SQL Server accepts remote connections

### Permission Issues
1. Verify database user permissions
2. Check if user can access the specific database
3. Ensure stored procedure execution rights

## Development

The server is built with:
- **mcp** - Model Context Protocol SDK
- **pyodbc** - SQL Server connectivity
- **python-dotenv** - Environment variable management

To modify the server, edit `server.py` and add new tools or modify existing ones.

## License

MIT License