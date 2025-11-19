# Claude Desktop Configuration

To use this MCP server with Claude Desktop, add this configuration to your Claude Desktop settings:

## Configuration File Location
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

## Configuration Content

```json
{
  "mcpServers": {
    "database": {
      "command": "C:\\Users\\ajay.singh\\Downloads\\test\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\ajay.singh\\Downloads\\test\\mcp-server-python\\server.py"
      ],
      "env": {
        "DB_SERVER": "your-server-name",
        "DB_NAME": "Ahs_Bit_Red_QA_8170",
        "DB_USER": "your-username",
        "DB_PASSWORD": "your-password"
      }
    }
  }
}
```

## For Windows Authentication
If you're using Windows Authentication (no username/password), use this config:

```json
{
  "mcpServers": {
    "database": {
      "command": "C:\\Users\\ajay.singh\\Downloads\\test\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\ajay.singh\\Downloads\\test\\mcp-server-python\\server.py"
      ],
      "env": {
        "DB_SERVER": "localhost\\SQLEXPRESS",
        "DB_NAME": "Ahs_Bit_Red_QA_8170"
      }
    }
  }
}
```

## Setup Steps

1. **Create the config file** if it doesn't exist
2. **Add the configuration** above (adjust paths to match your system)
3. **Restart Claude Desktop**
4. **Test the connection** by asking Claude to list your database tables

## Example Claude Prompts

Once configured, you can ask Claude:

- "List all tables in my database"
- "Show me the structure of the PATIENT_DETAILS table"
- "Execute the USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET stored procedure with LOGIN_USERID=68"
- "Count how many patients are in the PATIENT_DETAILS table"
- "Show me the last 10 entries from CARE_STAFF_DETAILS"

## Troubleshooting

### Issue: "MCP server not found"
- Check that the Python path is correct
- Ensure the server.py path is correct
- Verify the virtual environment exists

### Issue: "Database connection failed"
- Run `test_connection.bat` to verify database connectivity
- Check your database credentials in the env section
- Ensure SQL Server is running and accessible

### Issue: "Permission denied"
- Verify the database user has appropriate permissions
- Check if Windows Authentication is properly configured
- Ensure the user can access the specific database

## Security Note

For production use, consider:
- Using environment variables instead of hardcoding credentials
- Setting up proper database permissions
- Using encrypted connections
- Implementing audit logging