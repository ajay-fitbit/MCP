# 🧩 Python File Reference Guide

This document provides detailed information about each Python file in the system, explaining the purpose, key classes/methods, and how they work together.

## Core Server Files

### `server.py`

**Purpose**: Implements the MCP (Model Context Protocol) server that connects to SQL Server.

**Key Classes**:
- `DatabaseService`: Handles all database operations
  - `connect()`: Establishes connection to SQL Server
  - `disconnect()`: Closes database connection
  - `execute_query()`: Runs SQL queries
  - `list_tables()`: Gets table information
  - `describe_table()`: Gets detailed table schema
  - `list_stored_procedures()`: Lists available procedures
  - `execute_stored_procedure()`: Executes stored procedures

**MCP Server Setup**:
```python
# Create the MCP server
server = Server("database-mcp-server")

# Register tools
@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    # Tool definitions here...

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    # Tool implementation here...
```

**Key Features**:
- SQL Server connection using Windows authentication
- JSON schema validation for tools
- Error handling and reporting
- Signal handlers for graceful shutdown
- Auto-connection from environment variables

**How It Works**:
1. Server initializes and connects to database
2. Listens for incoming MCP connections
3. Receives tool calls and executes them
4. Returns results in MCP format

---

## Direct Database Access

### `direct_no_mcp.py`

**Purpose**: Provides direct database access without requiring the MCP server.

**Key Classes**:
- `DirectDatabaseClient`: Handles database and OpenAI integration
  - `connect_to_database()`: Establishes SQL Server connection
  - `get_tables()`: Retrieves database table information
  - `get_stored_procedures()`: Lists stored procedures
  - `execute_query()`: Runs SQL queries
  - `ask_openai()`: Processes natural language with OpenAI

**OpenAI Integration**:
```python
# Setup OpenAI with corporate-friendly SSL settings
http_client = httpx.Client(verify=False, timeout=60.0)
self.client = openai.OpenAI(api_key=api_key, http_client=http_client)

# Call OpenAI API
response = self.client.chat.completions.create(
    model="gpt-4-turbo",
    messages=messages,
    temperature=0.2
)
```

**Key Features**:
- Corporate network support with SSL verification bypass
- Natural language to SQL conversion
- SQL execution and result formatting
- Interactive command-line interface

**How It Works**:
1. Connects directly to SQL Server database
2. Provides a command prompt for natural language questions
3. Uses OpenAI to convert questions to SQL
4. Executes SQL and formats results
5. Uses OpenAI to explain results in natural language

---

### `direct_database.py`

**Purpose**: Enhanced direct database client with more advanced features.

**Key Classes**:
- `DirectDatabaseClient`: Comprehensive database access
  - `connect()`: Establishes database connection
  - `get_tables()`: Retrieves table metadata
  - `get_table_columns()`: Gets detailed column information
  - `get_stored_procedures()`: Lists stored procedures
  - `get_procedure_parameters()`: Gets procedure parameter details
  - `execute_query()`: Runs SQL queries
  - `execute_procedure()`: Runs stored procedures
  - `generate_sql_from_natural_language()`: Converts natural language to SQL
  - `process_user_query()`: Handles end-to-end query processing
  - `explain_results()`: Provides human-readable explanations

**Advanced Features**:
```python
# Generate SQL from natural language
sql_generation_result = await self.generate_sql_from_natural_language(user_query)

# Execute the generated SQL
query_result = await self.execute_query(sql_query)

# Explain results in natural language
explanation = await self.explain_results(query_response)
```

**How It Works**:
1. Uses a multi-stage approach for query processing:
   - First analyzes the database schema for relevant objects
   - Gets detailed schema for those objects
   - Generates SQL based on the schema context
   - Executes the SQL and processes results
   - Explains results in natural language
2. Maintains schema cache for performance
3. Provides confidence scores for generated SQL

---

## OpenAI Client Files

### `openai_client.py`

**Purpose**: Client application that uses OpenAI to interact with the MCP server.

**Key Classes**:
- `OpenAIDatabaseClient`: Manages OpenAI and MCP server interaction
  - `run_chat()`: Main chat loop
  - `process_message()`: Sends user queries to OpenAI
  - `execute_tools()`: Handles tool calls from OpenAI

**OpenAI Integration**:
```python
# Process message with OpenAI
response = await self.client.chat.completions.create(
    model=self.model,
    messages=self.messages,
    tools=self.tools,
    tool_choice="auto"
)
```

**Key Features**:
- Conversation history management
- Tool call handling and execution
- Error recovery and retries
- Interactive command-line interface

**How It Works**:
1. Initializes OpenAI client with API key
2. Defines tools based on MCP server capabilities
3. Presents an interactive chat interface
4. Processes user messages with OpenAI
5. Handles tool calls by executing MCP server functions
6. Presents results back to the user

---

### `server_client.py`

**Purpose**: HTTP-based client that connects to a running MCP server.

**Key Classes**:
- `OpenAIServerClient`: Connects to MCP server via HTTP
  - `connect_database()`: Initiates database connection
  - `execute_query()`: Runs SQL via MCP server
  - `list_tables()`: Gets tables via MCP server
  - `describe_table()`: Gets table details via MCP server
  - `process_user_question()`: Processes natural language queries

**HTTP Client Implementation**:
```python
# Make HTTP request to MCP server
async with self.http_client.post(
    f"{self.server_url}/call-tool",
    json={"name": name, "arguments": arguments}
) as response:
    response.raise_for_status()
    return await response.json()
```

**How It Works**:
1. Creates an HTTP client to communicate with the MCP server
2. Converts OpenAI tool calls to MCP server HTTP requests
3. Processes responses and handles errors
4. Provides a complete OpenAI chat interface

---

## Specialized Tools

### `stored_proc_explorer.py`

**Purpose**: Specialized tool for analyzing and testing stored procedures.

**Key Classes**:
- `StoredProcedureExplorer`: Analyzes stored procedures
  - `get_stored_procedure_definition()`: Gets procedure SQL code
  - `get_procedure_parameters()`: Gets parameter details
  - `search_stored_procedures()`: Searches for procedures
  - `analyze_procedure()`: Generates analysis with OpenAI
  - `execute_procedure()`: Tests procedure execution
  - `analyze_um_activity_log_procedures()`: Special analysis for your procedures

**OpenAI Analysis**:
```python
# Generate analysis using GPT
prompt = f"""
Please analyze this SQL Server stored procedure:

PROCEDURE NAME: {schema_name}.{procedure_name}

PARAMETERS:
{json.dumps(parameters, indent=2)}

PROCEDURE DEFINITION:
```sql
{definition}
```

Provide a comprehensive analysis including:
...
"""

analysis = await self.ask_gpt(prompt)
```

**How It Works**:
1. Connects to SQL Server database
2. Retrieves stored procedure definition and parameters
3. Uses OpenAI to analyze the procedure's purpose and functionality
4. Provides execution capability for testing
5. Special handling for analyzing UM Activity Log procedures

---

## Helper Utilities

### `test_db_connection.py`

**Purpose**: Tests the database connection to verify configuration.

**Key Functions**:
- `test_database_connection()`: Tests SQL Server connectivity
  - Attempts connection with configured parameters
  - Runs test queries to verify functionality
  - Reports connection status and results

**Example Usage**:
```python
# Test connection to SQL Server
success = test_database_connection()
if success:
    print("✅ Database connection successful")
else:
    print("❌ Connection failed")
```

---

### `verify_mcp_package.py`

**Purpose**: Verifies that the MCP package is properly installed.

**Key Functions**:
- `check_package()`: Tests if a package is installed
  - Attempts to import the package
  - Reports version information if available
  - Handles import errors and missing packages

**How It Works**:
1. Checks Python version
2. Tests importing required packages (mcp, mcp.server, etc.)
3. Reports success or failure for each package
4. Provides installation instructions for missing packages

---

## Integration Testing

### `test_openai.py`

**Purpose**: Tests the OpenAI API connection.

**Key Functions**:
- `test_openai_connection()`: Tests OpenAI API connectivity
  - Initializes OpenAI client with API key
  - Makes a simple completion request
  - Reports success or failure

**SSL Handling**:
```python
# Configure SSL to ignore certificate verification
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
```

**How It Works**:
1. Loads API key from environment
2. Configures SSL for corporate network compatibility
3. Makes a test request to OpenAI API
4. Reports success or detailed error information

---

### `test_mcp_connection.py`

**Purpose**: Tests the MCP server connectivity.

**Key Functions**:
- `test_mcp_server()`: Tests starting and connecting to MCP server
  - Attempts to import MCP package
  - Creates and starts a simple MCP server
  - Tests basic functionality
  - Reports success or failure

**How It Works**:
1. Imports required MCP packages
2. Creates a minimal MCP server
3. Tests server startup and basic tool calls
4. Reports detailed diagnostics for any issues

---

## File Relationships and Dependencies

```
server.py ◄─────────────┐
   │                    │
   ▼                    │
openai_client.py ───────┤
   │                    │
   ▼                    │
server_client.py        │
                        │
direct_no_mcp.py        │
   │                    │
   ▼                    │
direct_database.py      │
   │                    │
   ▼                    │
stored_proc_explorer.py ┘
```

- `server.py` is the core MCP server implementation
- `openai_client.py` depends on MCP server functionality
- `server_client.py` connects to a running MCP server
- `direct_no_mcp.py` is independent from MCP
- `direct_database.py` is an enhanced version of direct_no_mcp.py
- `stored_proc_explorer.py` is a specialized tool for procedure analysis

---

*This Python File Reference Guide documents all key Python files as of October 10, 2025.*