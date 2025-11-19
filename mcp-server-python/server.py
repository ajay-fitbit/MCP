#!/usr/bin/env python3

import asyncio
import json
import os
import sys
import signal
from typing import Any, Dict, List, Optional, Sequence
import pyodbc
from dotenv import load_dotenv

# Import MCP SDK
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio


# Load environment variables
load_dotenv()

# Setup signal handlers for graceful shutdown
def handle_exit_signal(sig, frame):
    print("\nShutdown signal received. Closing database connections...")
    try:
        if hasattr(sys.modules[__name__], 'db_service'):
            db_service.disconnect()
        print("Database disconnected. Shutting down server...")
    except Exception as e:
        print(f"Error during shutdown: {str(e)}")
    
    print("MCP Server stopped.")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, handle_exit_signal)  # Ctrl+C
signal.signal(signal.SIGTERM, handle_exit_signal)  # Termination signal


class DatabaseService:
    def __init__(self):
        self.connection = None
        self.is_connected = False
    
    def connect(self, server: str, database: str, user: str = None, password: str = None) -> str:
        """Connect to SQL Server database"""
        try:
            if self.is_connected and self.connection:
                self.disconnect()
            
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
            
            self.connection = pyodbc.connect(conn_str, timeout=30)
            self.is_connected = True
            
            return f"Successfully connected to database {database} on server {server}"
        
        except Exception as e:
            self.is_connected = False
            raise Exception(f"Failed to connect to database: {str(e)}")
    
    def disconnect(self) -> str:
        """Disconnect from database"""
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
            self.is_connected = False
            return "Successfully disconnected from database"
        except Exception as e:
            raise Exception(f"Failed to disconnect from database: {str(e)}")
    
    def ensure_connected(self):
        """Ensure database is connected"""
        if not self.is_connected or not self.connection:
            raise Exception("Database is not connected. Please connect first.")
    
    def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a SQL query"""
        self.ensure_connected()
        
        try:
            cursor = self.connection.cursor()
            
            if parameters:
                # Convert parameters to a list in the order they appear in the query
                param_values = []
                for key, value in parameters.items():
                    # Replace named parameters with ? placeholders
                    query = query.replace(f"@{key}", "?")
                    param_values.append(value)
                
                cursor.execute(query, param_values)
            else:
                cursor.execute(query)
            
            # Get column names
            columns = [column[0] for column in cursor.description] if cursor.description else []
            
            # Fetch all rows
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            result_set = []
            for row in rows:
                row_dict = {}
                for i, value in enumerate(row):
                    row_dict[columns[i]] = value
                result_set.append(row_dict)
            
            # Get rows affected
            rows_affected = cursor.rowcount if cursor.rowcount > 0 else len(result_set)
            
            cursor.close()
            
            return {
                "recordset": result_set,
                "columns": columns,
                "rowsAffected": rows_affected
            }
            
        except Exception as e:
            raise Exception(f"Failed to execute query: {str(e)}")
    
    def list_tables(self, schema: str = "dbo") -> List[Dict[str, Any]]:
        """List all tables in the database"""
        query = """
            SELECT 
                TABLE_SCHEMA,
                TABLE_NAME,
                TABLE_TYPE
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = ?
            ORDER BY TABLE_NAME
        """
        
        result = self.execute_query(query, {"schema": schema})
        return result["recordset"]
    
    def describe_table(self, table_name: str, schema: str = "dbo") -> Dict[str, Any]:
        """Get detailed information about a table"""
        columns_query = """
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                COLUMN_DEFAULT,
                CHARACTER_MAXIMUM_LENGTH,
                NUMERIC_PRECISION,
                NUMERIC_SCALE,
                ORDINAL_POSITION
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
            ORDER BY ORDINAL_POSITION
        """
        
        indexes_query = """
            SELECT 
                i.name AS index_name,
                i.type_desc AS index_type,
                i.is_unique,
                i.is_primary_key,
                c.name AS column_name
            FROM sys.indexes i
            JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
            JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
            JOIN sys.tables t ON i.object_id = t.object_id
            JOIN sys.schemas s ON t.schema_id = s.schema_id
            WHERE s.name = ? AND t.name = ?
            ORDER BY i.name, ic.key_ordinal
        """
        
        columns = self.execute_query(columns_query, {"schema": schema, "table_name": table_name})
        indexes = self.execute_query(indexes_query, {"schema": schema, "table_name": table_name})
        
        return {
            "table": f"{schema}.{table_name}",
            "columns": columns["recordset"],
            "indexes": indexes["recordset"]
        }
        
    def generate_query_from_template(self, template_file: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate a SQL query from a template file with parameter substitution"""
        self.ensure_connected()
        
        try:
            # Get the current working directory
            import os
            working_dir = os.getcwd()
            
            # Define the templates directory - prioritize this folder
            templates_dir = os.path.join(working_dir, "templates")
            
            # Create the templates directory if it doesn't exist
            if not os.path.exists(templates_dir):
                try:
                    os.makedirs(templates_dir)
                    print(f"Created templates directory at {templates_dir}")
                except Exception as e:
                    print(f"Note: Could not create templates directory: {str(e)}")
            
            # First check if the file exists in the templates directory
            template_path = os.path.join(templates_dir, template_file)
            
            # If not found in the templates directory, try the working directory
            if not os.path.exists(template_path):
                template_path = os.path.join(working_dir, template_file)
            
            # If still not found, try some common subdirectories
            if not os.path.exists(template_path):
                for subdir in ['sql', 'queries', 'scripts', 'sql_templates']:
                    potential_path = os.path.join(working_dir, subdir, template_file)
                    if os.path.exists(potential_path):
                        template_path = potential_path
                        break
            
            # Check if template exists
            if not os.path.exists(template_path):
                raise FileNotFoundError(f"Template file '{template_file}' not found in the working directory or common subdirectories")
            
            # Read the template file
            with open(template_path, 'r') as f:
                template_sql = f.read()
            
            # Perform parameter substitution if parameters are provided
            final_sql = template_sql
            param_values = {}
            
            if parameters:
                # Replace named parameters in the template
                for key, value in parameters.items():
                    param_placeholder = f"@{key}"
                    if param_placeholder in final_sql:
                        # For the generated SQL, keep the parameter as is
                        param_values[key] = value
            
            # Execute the query with parameters if needed
            result = None
            if param_values:
                result = self.execute_query(final_sql, param_values)
            else:
                result = self.execute_query(final_sql)
            
            # Return the template SQL, final SQL (after replacements), and the query results
            return {
                "template_file": template_file,
                "template_path": template_path,
                "template_sql": template_sql,
                "parameters": parameters,
                "execution_results": result,
                "template_locations_checked": [
                    os.path.join(working_dir, "templates", template_file),
                    os.path.join(working_dir, template_file),
                    *[os.path.join(working_dir, subdir, template_file) for subdir in ['sql', 'queries', 'scripts', 'sql_templates']]
                ]
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate query from template: {str(e)}")
    
    def get_related_tables(self, table_name: str, schema: str = "dbo") -> Dict[str, Any]:
        """Get a table and all related tables through foreign key relationships"""
        self.ensure_connected()
        
        try:
            # Get the main table information
            table_info = self.describe_table(table_name, schema)
            
            # Find tables that this table references (outgoing foreign keys)
            outgoing_fk_query = """
            SELECT 
                OBJECT_SCHEMA_NAME(fk.referenced_object_id) AS referenced_schema,
                OBJECT_NAME(fk.referenced_object_id) AS referenced_table,
                COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS referenced_column,
                COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS referencing_column,
                fk.name AS foreign_key_name,
                'Outgoing' AS relationship_type
            FROM sys.foreign_keys fk
            INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
            INNER JOIN sys.tables t ON fk.parent_object_id = t.object_id
            INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
            WHERE s.name = ? AND t.name = ?
            """
            
            # Find tables that reference this table (incoming foreign keys)
            incoming_fk_query = """
            SELECT 
                OBJECT_SCHEMA_NAME(fk.parent_object_id) AS referencing_schema,
                OBJECT_NAME(fk.parent_object_id) AS referencing_table,
                COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS referencing_column,
                COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS referenced_column,
                fk.name AS foreign_key_name,
                'Incoming' AS relationship_type
            FROM sys.foreign_keys fk
            INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
            INNER JOIN sys.tables t ON fk.referenced_object_id = t.object_id
            INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
            WHERE s.name = ? AND t.name = ?
            """
            
            outgoing_relations = self.execute_query(outgoing_fk_query, {"schema": schema, "table_name": table_name})
            incoming_relations = self.execute_query(incoming_fk_query, {"schema": schema, "table_name": table_name})
            
            # Summary of related tables
            related_tables = []
            
            # Process outgoing relationships
            for relation in outgoing_relations["recordset"]:
                related_tables.append({
                    "schema": relation["referenced_schema"],
                    "table": relation["referenced_table"],
                    "relationship": "Parent",
                    "foreign_key": relation["foreign_key_name"],
                    "local_column": relation["referencing_column"],
                    "remote_column": relation["referenced_column"]
                })
            
            # Process incoming relationships
            for relation in incoming_relations["recordset"]:
                related_tables.append({
                    "schema": relation["referencing_schema"],
                    "table": relation["referencing_table"],
                    "relationship": "Child",
                    "foreign_key": relation["foreign_key_name"],
                    "local_column": relation["referenced_column"],
                    "remote_column": relation["referencing_column"]
                })
            
            # Get summary information for each related table
            for related_table in related_tables:
                # Get row count for the table
                count_query = f"SELECT COUNT(*) AS row_count FROM {related_table['schema']}.{related_table['table']}"
                try:
                    count_result = self.execute_query(count_query)
                    row_count = count_result["recordset"][0]["row_count"] if count_result["recordset"] else 0
                    related_table["row_count"] = row_count
                except:
                    related_table["row_count"] = "Unknown"
            
            return {
                "table": f"{schema}.{table_name}",
                "related_tables": related_tables
            }
            
        except Exception as e:
            raise Exception(f"Failed to get related tables: {str(e)}")
    
    def list_stored_procedures(self, schema: str = "dbo", procedure_name_pattern: str = None) -> List[Dict[str, Any]]:
        """List stored procedures with optional name pattern filtering"""
        if procedure_name_pattern:
            query = """
                SELECT 
                    ROUTINE_SCHEMA,
                    ROUTINE_NAME,
                    ROUTINE_TYPE,
                    CREATED,
                    LAST_ALTERED
                FROM INFORMATION_SCHEMA.ROUTINES 
                WHERE ROUTINE_SCHEMA = ? 
                  AND ROUTINE_TYPE = 'PROCEDURE' 
                  AND ROUTINE_NAME LIKE ?
                ORDER BY ROUTINE_NAME
            """
            result = self.execute_query(query, {"schema": schema, "pattern": f"%{procedure_name_pattern}%"})
        else:
            query = """
                SELECT top 10
                    ROUTINE_SCHEMA,
                    ROUTINE_NAME,
                    ROUTINE_TYPE,
                    CREATED,
                    LAST_ALTERED
                FROM INFORMATION_SCHEMA.ROUTINES 
                WHERE ROUTINE_SCHEMA = ? AND ROUTINE_TYPE = 'PROCEDURE'
                ORDER BY ROUTINE_NAME
            """
            result = self.execute_query(query, {"schema": schema})
        
        return result["recordset"]
    
    def get_procedure_details(self, procedure_name: str, schema: str = "dbo") -> Dict[str, Any]:
        """Get details about a stored procedure including parameters and return columns"""
        self.ensure_connected()
        
        try:
            # Get procedure parameters
            params_query = """
            SELECT 
                p.name AS parameter_name,
                t.name AS data_type,
                p.max_length,
                p.precision,
                p.scale,
                p.is_output,
                p.has_default_value,
                p.default_value
            FROM sys.parameters p
            INNER JOIN sys.procedures pr ON p.object_id = pr.object_id
            INNER JOIN sys.schemas s ON pr.schema_id = s.schema_id
            INNER JOIN sys.types t ON p.system_type_id = t.system_type_id AND p.user_type_id = t.user_type_id
            WHERE s.name = ? AND pr.name = ?
            ORDER BY p.parameter_id
            """
            
            parameters_result = self.execute_query(params_query, {"schema": schema, "proc_name": procedure_name})
            
            # Get procedure definition to analyze
            def_query = """
            SELECT definition 
            FROM sys.sql_modules m
            INNER JOIN sys.procedures p ON m.object_id = p.object_id
            INNER JOIN sys.schemas s ON p.schema_id = s.schema_id
            WHERE s.name = ? AND p.name = ?
            """
            
            definition_result = self.execute_query(def_query, {"schema": schema, "proc_name": procedure_name})
            procedure_definition = definition_result["recordset"][0]["definition"] if definition_result["recordset"] else ""
            
            # Try to determine return columns by executing the procedure with NULL parameters
            return_columns = []
            try:
                # Build minimal execution with NULL params
                cursor = self.connection.cursor()
                
                # Get all parameters
                param_names = [p["parameter_name"].replace("@", "") for p in parameters_result["recordset"]]
                param_list = []
                param_values = []
                
                for param in param_names:
                    param_list.append(f"@{param} = ?")
                    param_values.append(None)  # Pass NULL for all parameters
                
                if param_list:
                    exec_statement = f"EXEC {schema}.{procedure_name} {', '.join(param_list)}"
                    cursor.execute(exec_statement, param_values)
                else:
                    cursor.execute(f"EXEC {schema}.{procedure_name}")
                
                # Get column names if available
                if cursor.description:
                    for col in cursor.description:
                        return_columns.append({
                            "name": col[0],
                            "type_code": col[1],
                            "display_size": col[2],
                            "internal_size": col[3],
                            "precision": col[4],
                            "scale": col[5],
                            "nullable": col[6]
                        })
                        
                cursor.close()
            except Exception as e:
                # It's okay if this fails, we tried our best to get the return columns
                return_columns.append({"note": f"Could not determine return columns: {str(e)}"})
            
            return {
                "procedure_name": f"{schema}.{procedure_name}",
                "parameters": parameters_result["recordset"],
                "return_columns": return_columns,
                "has_definition": bool(procedure_definition)
            }
            
        except Exception as e:
            raise Exception(f"Failed to get procedure details: {str(e)}")
    
    def execute_stored_procedure(self, procedure_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a stored procedure"""
        self.ensure_connected()
        
        try:
            cursor = self.connection.cursor()
            
            # Build the EXEC statement
            if parameters:
                param_list = []
                param_values = []
                for key, value in parameters.items():
                    param_list.append(f"@{key} = ?")
                    param_values.append(value)
                
                exec_statement = f"EXEC {procedure_name} {', '.join(param_list)}"
                cursor.execute(exec_statement, param_values)
            else:
                cursor.execute(f"EXEC {procedure_name}")
            
            # Get all result sets
            result_sets = []
            while True:
                try:
                    # Get column names
                    columns = [column[0] for column in cursor.description] if cursor.description else []
                    
                    # Fetch all rows
                    rows = cursor.fetchall()
                    
                    # Convert to list of dictionaries
                    result_set = []
                    for row in rows:
                        row_dict = {}
                        for i, value in enumerate(row):
                            row_dict[columns[i]] = value
                        result_set.append(row_dict)
                    
                    result_sets.append({
                        "columns": columns,
                        "data": result_set
                    })
                    
                    # Try to get next result set
                    if not cursor.nextset():
                        break
                        
                except Exception:
                    break
            
            cursor.close()
            
            return {
                "recordsets": result_sets,
                "recordset": result_sets[0]["data"] if result_sets else [],
                "rowsAffected": len(result_sets[0]["data"]) if result_sets else 0
            }
            
        except Exception as e:
            raise Exception(f"Failed to execute stored procedure: {str(e)}")


# Initialize the database service
db_service = DatabaseService()

# Create the MCP server
server = Server("database-mcp-server")


@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="connect_database",
            description="Connect to the SQL Server database",
            inputSchema={
                "type": "object",
                "properties": {
                    "server": {
                        "type": "string",
                        "description": "Database server name or IP address"
                    },
                    "database": {
                        "type": "string", 
                        "description": "Database name"
                    },
                    "user": {
                        "type": "string",
                        "description": "Username for database connection (optional for Windows auth)"
                    },
                    "password": {
                        "type": "string",
                        "description": "Password for database connection (optional for Windows auth)"
                    }
                },
                "required": ["server", "database"]
            }
        ),
        types.Tool(
            name="execute_query",
            description="Execute a SQL query on the connected database",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL query to execute"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Parameters for parameterized queries",
                        "additionalProperties": True
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="list_tables",
            description="List all tables in the database. Use this when asked to show or list tables.",
            inputSchema={
                "type": "object",
                "properties": {
                    "schema": {
                        "type": "string",
                        "description": "Schema name (optional, defaults to dbo)"
                    }
                }
            }
        ),
        types.Tool(
            name="describe_table",
            description="Get detailed information about a specific table",
            inputSchema={
                "type": "object",
                "properties": {
                    "tableName": {
                        "type": "string",
                        "description": "Name of the table to describe"
                    },
                    "schema": {
                        "type": "string",
                        "description": "Schema name (optional, defaults to dbo)"
                    }
                },
                "required": ["tableName"]
            }
        ),
        types.Tool(
            name="get_related_tables",
            description="Get a table and all related tables through foreign key relationships. Use this when asked about table relationships, related tables, foreign keys, or when phrases like 'how tables are connected' or 'related to' are used.",
            inputSchema={
                "type": "object",
                "properties": {
                    "tableName": {
                        "type": "string",
                        "description": "Name of the table to get relationships for"
                    },
                    "schema": {
                        "type": "string",
                        "description": "Schema name (optional, defaults to dbo)"
                    }
                },
                "required": ["tableName"]
            }
        ),
        types.Tool(
            name="list_stored_procedures",
            description="List stored procedures in the database with optional name pattern filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "schema": {
                        "type": "string",
                        "description": "Schema name (optional, defaults to dbo)"
                    },
                    "procedureNamePattern": {
                        "type": "string",
                        "description": "Filter procedures by name pattern (optional, SQL LIKE pattern)"
                    }
                }
            }
        ),
        types.Tool(
            name="execute_stored_procedure",
            description="Execute a stored procedure with parameters",
            inputSchema={
                "type": "object",
                "properties": {
                    "procedureName": {
                        "type": "string",
                        "description": "Name of the stored procedure to execute"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Parameters for the stored procedure",
                        "additionalProperties": True
                    }
                },
                "required": ["procedureName"]
            }
        ),
        types.Tool(
            name="get_procedure_details",
            description="Get details about a stored procedure including parameters and return columns",
            inputSchema={
                "type": "object",
                "properties": {
                    "procedureName": {
                        "type": "string",
                        "description": "Name of the stored procedure to get details for"
                    },
                    "schema": {
                        "type": "string",
                        "description": "Schema name (optional, defaults to dbo)"
                    }
                },
                "required": ["procedureName"]
            }
        ),
        types.Tool(
            name="generate_query_from_template",
            description="Read a SQL file from the templates directory or working directory and use it as a template to generate and execute a similar query",
            inputSchema={
                "type": "object",
                "properties": {
                    "templateFile": {
                        "type": "string",
                        "description": "Name of the SQL template file (e.g., 'query.sql', 'template.sql'). Templates are looked for in the 'templates' folder first, then in the working directory."
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Parameters to substitute in the template (format: @paramName in SQL)",
                        "additionalProperties": True
                    }
                },
                "required": ["templateFile"]
            }
        ),
        types.Tool(
            name="disconnect_database",
            description="Disconnect from the database",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
    """Handle tool calls"""
    try:
        if name == "connect_database":
            server_name = arguments.get("server")
            database = arguments.get("database")
            user = arguments.get("user")
            password = arguments.get("password")
            
            result = db_service.connect(server_name, database, user, password)
            return [types.TextContent(type="text", text=result)]
        
        elif name == "execute_query":
            query = arguments.get("query")
            parameters = arguments.get("parameters", {})
            
            result = db_service.execute_query(query, parameters)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
        elif name == "list_tables":
            schema = arguments.get("schema", "dbo")
            
            result = db_service.list_tables(schema)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
        elif name == "describe_table":
            table_name = arguments.get("tableName")
            schema = arguments.get("schema", "dbo")
            
            result = db_service.describe_table(table_name, schema)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
        elif name == "get_related_tables":
            table_name = arguments.get("tableName")
            schema = arguments.get("schema", "dbo")
            
            result = db_service.get_related_tables(table_name, schema)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
        elif name == "list_stored_procedures":
            schema = arguments.get("schema", "dbo")
            procedure_name_pattern = arguments.get("procedureNamePattern")
            
            result = db_service.list_stored_procedures(schema, procedure_name_pattern)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
        elif name == "execute_stored_procedure":
            procedure_name = arguments.get("procedureName")
            parameters = arguments.get("parameters", {})
            
            result = db_service.execute_stored_procedure(procedure_name, parameters)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
        elif name == "get_procedure_details":
            procedure_name = arguments.get("procedureName")
            schema = arguments.get("schema", "dbo")
            
            result = db_service.get_procedure_details(procedure_name, schema)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            
        elif name == "generate_query_from_template":
            template_file = arguments.get("templateFile")
            parameters = arguments.get("parameters", {})
            
            result = db_service.generate_query_from_template(template_file, parameters)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
        elif name == "disconnect_database":
            result = db_service.disconnect()
            return [types.TextContent(type="text", text=result)]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    print("Starting MCP Database Server...")
    print("Press Ctrl+C to stop the server")
    
    # Auto-connect to database using settings from .env
    try:
        server_name = os.getenv('DB_SERVER')
        database_name = os.getenv('DB_NAME')
        
        if server_name and database_name:
            print(f"Auto-connecting to database {database_name} on {server_name}...")
            db_service.connect(server_name, database_name)
            print("Connected to database successfully")
    except Exception as e:
        print(f"Warning: Auto-connect failed: {str(e)}")
        print("You'll need to connect manually using connect_database tool")
    
    # Run the server using stdin/stdout streams
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="database-mcp-server",
                    server_version="1.0.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    except KeyboardInterrupt:
        print("\nServer interrupted. Shutting down...")
        db_service.disconnect()
        print("Server stopped.")
    except Exception as e:
        print(f"Server error: {str(e)}")
        db_service.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        if hasattr(sys.modules[__name__], 'db_service'):
            db_service.disconnect()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        if hasattr(sys.modules[__name__], 'db_service'):
            db_service.disconnect()