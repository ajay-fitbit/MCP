# 📚 Complete Technical Documentation
# SQL Server Integration with AI Assistants

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [System Components](#system-components)
3. [Setup and Installation](#setup-and-installation)
4. [Database Connection](#database-connection)
5. [OpenAI Integration](#openai-integration)
6. [Claude Desktop Integration](#claude-desktop-integration)
7. [Python File Documentation](#python-file-documentation)
8. [Batch Files and Utilities](#batch-files-and-utilities)
9. [Troubleshooting](#troubleshooting)
10. [Security Considerations](#security-considerations)

---

## Architecture Overview

The system provides multiple ways to interact with your SQL Server database through AI assistants:

1. **MCP Server Approach**: Using the Model Context Protocol (MCP) server as an intermediary between AI assistants and your database.

2. **Direct Connection Approach**: Bypassing the MCP server and connecting directly to SQL Server.

3. **OpenAI Integration**: Using OpenAI models (GPT-4, GPT-4o, etc.) to interact with your database.

4. **Claude Desktop Integration**: Using Anthropic's Claude Desktop application with your database.

### Architecture Diagram

```
                  ┌─────────────────┐
                  │   AI Assistant  │
                  │ (Claude/OpenAI) │
                  └────────┬────────┘
                           │
                           ▼
           ┌─────────────────────────────┐
           │    Model Context Protocol   │
           │          (Optional)         │
           └─────────────┬───────────────┘
                         │
                         ▼
               ┌─────────────────────┐
               │  Database Service   │
               └─────────┬───────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ SQL Server  │
                  │ AHS-LP-945  │
                  └─────────────┘
```

---

## System Components

### Core Components

1. **Database Connection Layer**
   - PyODBC for SQL Server connectivity
   - Windows Authentication integration
   - Query execution engine

2. **AI Integration Layer**
   - OpenAI API client with corporate network support
   - Claude Desktop integration via MCP
   - Natural language to SQL conversion

3. **Model Context Protocol (MCP)**
   - Server implementation for tool-using AI models
   - Schema and metadata management
   - Request/response handling

4. **Direct Database Client**
   - Standalone utility without MCP dependency
   - Built-in OpenAI integration
   - Database querying and exploration

### Dependencies

- **Python 3.8+**: Base runtime environment
- **PyODBC**: SQL Server connectivity
- **OpenAI API**: AI model access
- **Python-dotenv**: Environment configuration
- **HTTPX**: Enhanced HTTP client with SSL fixes
- **MCP Package**: Model Context Protocol implementation

---

## Setup and Installation

### Environment Setup

1. **Python Environment**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file with the following content:
   ```
   # Database Configuration
   DB_SERVER=AHS-LP-945
   DB_NAME=Ahs_Bit_Red_QA_8170
   DB_USER=
   DB_PASSWORD=

   # OpenAI Configuration
   OPENAI_API_KEY=your-api-key-here
   ```

### Installation Options

#### Option 1: Complete Setup
Run the all-in-one installer:
```bash
.\install_requirements.bat
```

#### Option 2: Manual Package Installation
```bash
pip install pyodbc httpx openai python-dotenv mcp[client]
```

#### Option 3: Minimal Setup (Direct Client Only)
```bash
pip install pyodbc httpx openai python-dotenv
```

---

## Database Connection

### Connection Methods

1. **Windows Authentication** (Default)
   ```python
   conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
   ```

2. **SQL Authentication** (Optional)
   ```python
   conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'
   ```

### Database Schema Discovery

The system automatically discovers:
- Tables and views (1,815 found)
- Stored procedures (6,064 found)
- Columns, data types, and relationships
- Table sizes and row counts

### Stored Procedure Support

Special handling for your stored procedures:
- Parameter discovery and validation
- Default value handling
- Output parameter processing
- Multiple result set handling

---

## OpenAI Integration

### Model Support

- **GPT-4o**: Default for best performance
- **GPT-4**: For complex queries
- **GPT-3.5-Turbo**: Faster, economical option

### Corporate Network Adaptations

The system includes special handling for corporate environments:
```python
# SSL certificate verification bypass
http_client = httpx.Client(verify=False, timeout=60.0)
self.client = openai.OpenAI(api_key=api_key, http_client=http_client)
```

### Natural Language Query Processing

1. User submits natural language question
2. System retrieves database schema context
3. OpenAI generates appropriate SQL
4. System executes SQL and returns results
5. OpenAI explains results in natural language

---

## Claude Desktop Integration

### Configuration

Claude Desktop requires an MCP configuration file at:
```
%APPDATA%\Claude\claude_desktop_config.json
```

With content:
```json
{
  "mcpServers": {
    "database": {
      "command": "C:\\Users\\ajay.singh\\Downloads\\test\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\ajay.singh\\Downloads\\test\\mcp-server-python\\server.py"
      ],
      "env": {
        "DB_SERVER": "AHS-LP-945",
        "DB_NAME": "Ahs_Bit_Red_QA_8170"
      }
    }
  }
}
```

### Setup Process

1. Install Claude Desktop from https://claude.ai/download
2. Run `setup_claude_desktop.bat` to configure MCP integration
3. Restart Claude Desktop completely
4. Test with database queries in natural language

---

## Python File Documentation

### `server.py`

**Purpose**: MCP server implementation that connects to SQL Server

**Key Components**:
- `DatabaseService` class: Manages database connections and queries
- MCP server initialization and configuration
- Tool registration for database operations
- Signal handlers for graceful shutdown

**Key Functions**:
- `connect()`: Establishes database connection
- `execute_query()`: Runs SQL queries
- `list_tables()`: Returns database table information
- `describe_table()`: Provides detailed table schema
- `execute_stored_procedure()`: Runs stored procedures

**Example Usage**:
```bash
python server.py
# Server starts and listens for MCP connections
```

### `direct_no_mcp.py`

**Purpose**: Standalone database client without MCP dependency

**Key Components**:
- `DirectDatabaseClient` class: Manages database and OpenAI interaction
- Connection management with error handling
- OpenAI integration with corporate network support
- Natural language to SQL conversion

**Key Functions**:
- `connect_to_database()`: Establishes SQL Server connection
- `get_tables()`: Retrieves database tables
- `execute_query()`: Runs SQL queries directly
- `ask_openai()`: Processes natural language with OpenAI

**Example Usage**:
```bash
python direct_no_mcp.py
# Interactive prompt appears for database questions
```

### `openai_client.py`

**Purpose**: OpenAI client that connects to the MCP server

**Key Components**:
- `OpenAIDatabaseClient` class: Manages OpenAI and MCP connection
- Interactive chat interface
- History management
- Error handling and recovery

**Key Functions**:
- `run_chat()`: Main chat loop
- `process_message()`: Sends user queries to OpenAI
- `execute_tools()`: Handles tool calls from OpenAI

**Example Usage**:
```bash
python openai_client.py
# Interactive chat starts for database questions
```

### `stored_proc_explorer.py`

**Purpose**: Specialized tool for analyzing stored procedures

**Key Components**:
- `StoredProcedureExplorer` class: Analyzes stored procedures
- Detailed parameter analysis
- SQL code explanation with OpenAI
- Execution capabilities

**Key Functions**:
- `analyze_procedure()`: Explains stored procedure purpose and usage
- `execute_procedure()`: Tests procedure with parameters
- `search_stored_procedures()`: Finds relevant procedures

**Example Usage**:
```bash
python stored_proc_explorer.py
# Analysis of USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET
```

---

## Batch Files and Utilities

### Server Management

- `start_server.bat`: Launches the MCP server
- `stop_server.bat`: Gracefully stops the MCP server
- `start_openai_chat.bat`: Starts OpenAI client connected to MCP server

### Direct Database Access

- `start_no_mcp.bat`: Launches direct database client without MCP
- `start_direct_database.bat`: Alternative direct client implementation

### Claude Desktop Integration

- `setup_claude_desktop.bat`: Configures Claude Desktop MCP integration
- `verify_claude_config.bat`: Verifies Claude Desktop configuration
- `fix_claude_config.bat`: Fixes Claude Desktop configuration issues

### Installation and Testing

- `install_requirements.bat`: Installs all required packages
- `test_connection.bat`: Tests database connectivity
- `verify_mcp.bat`: Verifies MCP package installation
- `test_sql_direct.bat`: Tests direct SQL Server connection

---

## Troubleshooting

### Common Issues and Solutions

#### MCP Import Error
**Issue**: `No module named 'mcp'`
**Solution**: Install MCP package: `pip install mcp[client]`

#### Database Connection Failure
**Issue**: `Login timeout expired`
**Solution**: Check SQL Server accessibility, network, firewall

#### SSL Certificate Errors
**Issue**: `SSL: CERTIFICATE_VERIFY_FAILED`
**Solution**: Use `verify=False` with HTTPX client

#### Claude Desktop Not Connecting
**Issue**: Claude asks for database details despite configuration
**Solution**: 
1. Exit Claude Desktop completely
2. Run `fix_claude_config.bat`
3. Restart Claude Desktop
4. Use explicit connection command: "Connect to my database"

#### Event Loop Errors
**Issue**: `asyncio.run() cannot be called from a running event loop`
**Solution**: Use proper async patterns or direct database client

---

## Security Considerations

### Authentication

- Windows Authentication used by default (no passwords stored)
- SQL Authentication supported but not recommended
- Credentials loaded from .env file (not hardcoded)

### Data Protection

- All database communication stays local
- No data sent to OpenAI beyond necessary context
- Query results processed locally

### API Key Management

- OpenAI API key stored in .env file
- Not exposed in code or logs
- Can be rotated without code changes

### Network Security

- Corporate network compatibility with SSL verification options
- No inbound connections required
- All connections initiated from client

---

## USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET Documentation

### Procedure Purpose
Retrieves UM (Utilization Management) activity referral details with extensive filtering, pagination, and sorting options.

### Parameters
- `LOGIN_USERID`: User ID for authentication (BIGINT)
- `FROM_DATE`, `TO_DATE`: Date range filters (VARCHAR)
- `MEMBER_NAME`: Filter by patient name (VARCHAR)
- `REFER_BY`, `REFER_TO`: Filter by referral source/target (BIGINT)
- `PAGE_NUMBER`, `PAGE_SIZE`: Pagination controls (INT)
- `ORDER_BY_FIELD`, `SORT_ORDER`: Sorting controls (VARCHAR)
- Plus 20+ additional filtering parameters

### Key Features
- Comprehensive security checks
- Advanced filtering options
- Performance optimizations
- Support for export operations
- Treatment type filtering

### Usage Examples
```sql
-- Basic usage
EXEC USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET
    @LOGIN_USERID = 68,
    @FROM_DATE = '2022-01-01',
    @TO_DATE = '2022-12-31'

-- Advanced filtering
EXEC USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET
    @LOGIN_USERID = 68,
    @FROM_DATE = '2022-01-01',
    @TO_DATE = '2022-12-31',
    @AUTH_STATUS = '1,2,3',
    @IS_MANAGER_STAFF = 1,
    @PAGE_NUMBER = 1,
    @PAGE_SIZE = 20,
    @ORDER_BY_FIELD = 'TREATMENT_TYPE_NAME',
    @SORT_ORDER = 'DESC'
```

---

*Documentation generated for AHS SQL Server Integration with AI Assistants*
*Last updated: October 10, 2025*