# 🚀 Quick Start Guide
# Using the SQL Server Integration with AI Assistants

This guide provides simple steps to get started with the SQL Server integration tools.

## 1. Choose Your Approach

You have three main options for using this system:

### Option A: Direct Database Client (No MCP Required)
Best for: Quick start, no dependencies, immediate results
```batch
.\start_no_mcp.bat
```

### Option B: OpenAI with MCP Server
Best for: Full features, advanced queries, more capabilities
```batch
.\start_server.bat
.\start_openai_chat.bat
```

### Option C: Claude Desktop
Best for: Desktop application experience, persistent interface
```batch
.\setup_claude_desktop.bat
```
Then launch Claude Desktop and ask database questions

## 2. Example Queries

Try these example queries with any of the options:

### Basic Information
- "What tables are in the database?"
- "How many tables are in my database?"
- "What stored procedures are available?"

### Table Information
- "Show me the structure of the PATIENT_DETAILS table"
- "What columns are in the UM_ACTIVITY_LOG_REFERRALS table?"
- "How many records are in the CARE_STAFF_DETAILS table?"

### Using Stored Procedures
- "How do I use the USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET procedure?"
- "What parameters does USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET accept?"
- "Execute USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET with LOGIN_USERID 68"

### Advanced Queries
- "Find all tables related to patient information"
- "Get referrals created in the last 30 days"
- "Show me how patient data relates to referrals"

## 3. Using the Direct Database Client

When using `start_no_mcp.bat`, you'll see an interactive prompt:

1. Enter your question in natural language
2. The system will:
   - Analyze your question
   - Generate appropriate SQL
   - Execute the SQL
   - Show the results
   - Explain what the results mean

Example session:
```
> What tables are in the database?
Thinking...

Response:
I'll list some of the tables in your SQL Server database.

SQL Results:
Found 25 rows:
Row 1: {"name": "PATIENT_DETAILS", "schema": "dbo", "row_count": 1250000}
Row 2: {"name": "UM_ACTIVITY_LOG_REFERRALS", "schema": "dbo", "row_count": 950000}
Row 3: {"name": "CARE_STAFF_DETAILS", "schema": "dbo", "row_count": 85000}
Row 4: {"name": "AUTH_STATUS", "schema": "dbo", "row_count": 25}
Row 5: {"name": "AUTH_TYPE", "schema": "dbo", "row_count": 18}
...and 20 more rows
```

## 4. Using the MCP Server with OpenAI

When using the OpenAI client with MCP server:

1. Start the server first: `.\start_server.bat`
2. Then start the client: `.\start_openai_chat.bat`
3. Enter questions in natural language
4. The system will interact with the database and provide answers

Example session:
```
OpenAI Database Assistant: I'm connected to your SQL Server database. What would you like to know?

You: What stored procedures handle UM Activity logs?

OpenAI Database Assistant: I found several stored procedures related to UM Activity logs:

1. USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET
   - Purpose: Retrieves UM activity referral details with filtering options
   - Parameters: LOGIN_USERID, FROM_DATE, TO_DATE, and 30+ filtering parameters

2. USP_AHS_UM_ACTIVITY_LOG_REFERRALS_INSERT
   - Purpose: Creates new UM activity referral records
   - Parameters: PATIENT_ID, AUTH_NO, REFERRED_BY, etc.

3. USP_AHS_UM_ACTIVITY_LOG_REFERRALS_UPDATE
   - Purpose: Updates existing UM activity referral records
   - Parameters: UM_ACTIVITY_LOG_ID and various update fields

Would you like details about any specific procedure?
```

## 5. Using Claude Desktop

After setting up Claude Desktop:

1. Launch Claude Desktop
2. Ask questions about your database in natural language
3. Claude will use the MCP server to query the database
4. Results will be presented in a conversational format

Example queries:
- "What tables are in my SQL Server database?"
- "Show me the schema of the PATIENT_DETAILS table"
- "Execute USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET with LOGIN_USERID 68"

## 6. Need More Help?

- For detailed documentation: See `TECHNICAL_DOCUMENTATION.md`
- For Python file details: See `PYTHON_FILE_REFERENCE.md`
- For troubleshooting: See the Troubleshooting section in `TECHNICAL_DOCUMENTATION.md`

---

*SQL Server Integration with AI Assistants - Quick Start Guide*  
*Last updated: October 10, 2025*