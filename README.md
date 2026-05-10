# SQL Server MCP Server

> A Python **Model Context Protocol (MCP)** server that lets AI assistants (Claude Desktop, GitHub Copilot, OpenAI clients) safely query Microsoft SQL Server, inspect schemas, and run stored procedures — including auto-generating T-SQL unit tests for stored procedures.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-server-orange.svg)](https://modelcontextprotocol.io/)
[![SQL Server](https://img.shields.io/badge/SQL%20Server-2017+-CC2927.svg)](https://www.microsoft.com/sql-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)
[![Status: active](https://img.shields.io/badge/status-active-success.svg)]()

---

## Why this exists

Working against SQL Server through an LLM normally means copy-pasting schemas and queries by hand. This MCP server gives AI assistants **structured, allow-listed tools** to do the work directly: discover schemas, run parameterised queries, inspect stored procedures, and generate test scaffolding — without exposing raw credentials to the model.

Originally built to accelerate T-SQL **stored-procedure unit-test generation** (see the `TEST_USP_*.sql` examples) where Claude analyses a proc, identifies edge cases, and emits a runnable test suite.

## Highlights

- 🧰 **11 MCP tools** covering connection, queries, schema discovery, stored-proc execution, and parameter-template generation
- 🤝 **Multi-client support** — Claude Desktop, OpenAI-based clients (GPT-4), direct Python clients
- 🛡️ **Parameterised queries** — pyodbc with explicit parameter binding, no string-concat SQL
- 🔐 **Auth flexibility** — Windows Authentication or SQL Auth via `.env`
- 🧪 **Stored-proc test generation** — example output committed in `TEST_USP_AHS_*.sql`
- 🐍 **Pure Python** — no build step, easy to extend

## Architecture

```
┌────────────────────┐      MCP / stdio       ┌─────────────────────┐
│  Claude Desktop /  │ ─────────────────────▶ │  server.py          │
│  GitHub Copilot /  │ ◀───────────────────── │  (MCP server)       │
│  OpenAI client     │      tool results      │   ├─ 11 tools       │
└────────────────────┘                        │   └─ pyodbc backend │
                                              └──────────┬──────────┘
                                                         │ ODBC
                                                         ▼
                                               ┌─────────────────┐
                                               │  SQL Server     │
                                               └─────────────────┘
```

## MCP tools exposed

| # | Tool | Purpose | R/W |
|---|---|---|---|
| 1 | `connect_database` | Open a connection (Win Auth or SQL Auth) | — |
| 2 | `disconnect_database` | Safely close the connection | — |
| 3 | `execute_query` | Run a parameterised SQL query | R/W |
| 4 | `list_tables` | List tables in a schema | R |
| 5 | `describe_table` | Columns, types, keys, indexes | R |
| 6 | `get_related_tables` | Walk FK relationships | R |
| 7 | `list_stored_procedures` | Enumerate procs in a schema | R |
| 8 | `get_procedure_details` | Parameter signature, definition | R |
| 9 | `execute_stored_procedure` | Run a proc with named parameters | R/W |
| 10 | `generate_query_from_template` | Build queries from saved templates | R |

> Write-capable tools (`execute_query`, `execute_stored_procedure`) should be paired with a **read-only DB role** in production. Recommended pattern: grant the connection user only `db_datareader` + `EXECUTE` on a curated proc list.

## Quickstart

### Prerequisites
- Python 3.8+
- [Microsoft ODBC Driver 17 for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
- Access to a SQL Server instance

### Install & run
```powershell
git clone https://github.com/ajay-fitbit/MCP.git
cd MCP\mcp-server-python

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env with your connection details

python test_connection.py       # sanity check
python server.py                # start the MCP server (stdio)
```

### Wire into Claude Desktop
Add to `claude_desktop_config.json` (full instructions in [`CLAUDE_DESKTOP_GUIDE.md`](mcp-server-python/CLAUDE_DESKTOP_GUIDE.md)):
```json
{
  "mcpServers": {
    "sqlserver": {
      "command": "python",
      "args": ["C:\\path\\to\\mcp-server-python\\server.py"]
    }
  }
}
```

A working example file is provided: [`claude_desktop_config.json`](mcp-server-python/claude_desktop_config.json).

### Use it from OpenAI / GPT-4
A standalone OpenAI client and chat launcher are included — see [`OPENAI_SETUP_GUIDE.md`](mcp-server-python/OPENAI_SETUP_GUIDE.md):
```powershell
.\start_openai_chat.bat
```

## Example: generating a stored-procedure unit test

```text
You:    Generate a unit test for usp_AHS_AG_Care_Staff_Activities_Get_Init.

Agent:  [calls get_procedure_details → analyzes parameters and result sets]
        [calls execute_stored_procedure with synthesized realistic params]
        [emits T-SQL test scaffold with setup, exec, assert, cleanup]
```

Real generated examples are committed:
- [`TEST_USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET_INIT.sql`](mcp-server-python/TEST_USP_AHS_AG_CARE_STAFF_ACTIVITIES_GET_INIT.sql)
- [`TEST_USP_AHS_UM_AUTH_SPECIFIC_DETAILS_GET_UT.sql`](mcp-server-python/TEST_USP_AHS_UM_AUTH_SPECIFIC_DETAILS_GET_UT.sql)

## Configuration reference

| Var | Purpose | Example |
|---|---|---|
| `DB_SERVER` | SQL Server host / instance | `localhost` or `host\SQLEXPRESS` |
| `DB_NAME` | Database name | `MyAppDb` |
| `DB_USER` | SQL Auth username (omit for Win Auth) | `app_reader` |
| `DB_PASSWORD` | SQL Auth password | `***` |
| `OPENAI_API_KEY` | Optional, for OpenAI client samples | `sk-...` |

## Documentation index

- [`COMPLETE_GUIDE.md`](mcp-server-python/COMPLETE_GUIDE.md) — full operator's guide
- [`CLAUDE_DESKTOP_GUIDE.md`](mcp-server-python/CLAUDE_DESKTOP_GUIDE.md) — Claude integration
- [`OPENAI_SETUP_GUIDE.md`](mcp-server-python/OPENAI_SETUP_GUIDE.md) — OpenAI/GPT-4 integration
- [`COMPLETE_TEST_SUITE_GENERATION_GUIDE.md`](mcp-server-python/COMPLETE_TEST_SUITE_GENERATION_GUIDE.md) — stored-proc test workflow
- [`TECHNICAL_DOCUMENTATION.md`](mcp-server-python/TECHNICAL_DOCUMENTATION.md) — internals
- [`PRESENTATION_SLIDES.md`](mcp-server-python/PRESENTATION_SLIDES.md) — overview deck

## Security & responsible use

- **Least privilege** — recommend a dedicated read-only DB login for non-write workloads
- **Parameterised queries** — pyodbc parameter binding throughout, no string concatenation
- **No secrets in the repo** — `.env` is gitignored; example only in `.env.example`
- **Allow-list pattern** — clients should restrict which tools the model may call
- **Tool outputs not re-fed as instructions** — mitigates prompt-injection from result data

## Roadmap

- [ ] Coverage-report tool for stored procs
- [ ] Sprint-aware *untested-changes* tool (git + DB diff)
- [ ] Containerised deploy (Docker + Azure Container Apps)
- [ ] Eval suite (RAGAS / promptfoo) for tool-routing accuracy
- [ ] Foundry agent integration

## Related projects

- [`AI-Resume-Filter`](https://github.com/ajay-fitbit/AI-Resume-Filter) — multi-agent resume screening with semantic matching + RAG
- [`CLR-Project`](https://github.com/ajay-fitbit/CLR-Project) — SQL Server CLR fix for the *INSERT EXEC cannot be nested* error (used by the test-generation workflow)

## Tech stack

`Python 3.8+` · `MCP SDK` · `pyodbc` · `python-dotenv` · `OpenAI SDK` (optional clients) · `Microsoft ODBC Driver 17`

## Author

**Ajay Singh** — Solutions Architect · agentic AI · MCP · LLM applications
[Portfolio](https://www.itshitechs.com/portfolio/) · [LinkedIn](https://www.linkedin.com/in/ajay-singh-ab40082/) · [GitHub](https://github.com/ajay-fitbit)

## License

MIT
