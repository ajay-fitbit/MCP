"""
SQL Server Stored Procedure Explorer - Analyze and run specific stored procedures
"""

import os
import sys
import json
import pyodbc
import asyncio
import httpx
from typing import List, Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
import logging
import re
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("StoredProcExplorer")

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY not found in environment variables or .env file")
    print("\n⚠️ OPENAI_API_KEY not found! Please set it as an environment variable or in a .env file.")
    print("You can get an API key from https://platform.openai.com/account/api-keys")
    sys.exit(1)

# SQL Server connection settings - using defaults but allowing override from .env file
SQL_SERVER = os.getenv("SQL_SERVER", "AHS-LP-945")
SQL_DATABASE = os.getenv("SQL_DATABASE", "Ahs_Bit_Red_QA_8170") 
SQL_TRUSTED_CONNECTION = os.getenv("SQL_TRUSTED_CONNECTION", "yes")

class StoredProcedureExplorer:
    def __init__(self):
        """Initialize the stored procedure explorer with SQL Server connection"""
        self.connection_string = (
            f"DRIVER={{SQL Server}};"
            f"SERVER={SQL_SERVER};"
            f"DATABASE={SQL_DATABASE};"
            f"Trusted_Connection={SQL_TRUSTED_CONNECTION};"
        )
        self.conn = None
        self.openai_client = httpx.AsyncClient(verify=False, timeout=60.0)
        self.openai_api_key = OPENAI_API_KEY
        self.model = os.getenv("OPENAI_MODEL", "gpt-5-nano")
        
    async def connect(self):
        """Connect to the SQL Server database"""
        try:
            # Use pyodbc to connect to SQL Server
            self.conn = pyodbc.connect(self.connection_string)
            logger.info(f"Successfully connected to {SQL_DATABASE} on {SQL_SERVER}")
            return True
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            print(f"\nError connecting to database: {str(e)}")
            return False
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    async def get_stored_procedure_definition(self, schema_name: str, procedure_name: str) -> str:
        """Get the SQL definition of a stored procedure"""
        if not self.conn:
            await self.connect()
        
        cursor = self.conn.cursor()
        query = """
        SELECT OBJECT_DEFINITION(OBJECT_ID(QUOTENAME(?) + '.' + QUOTENAME(?))) AS procedure_definition;
        """
        
        try:
            cursor.execute(query, (schema_name, procedure_name))
            row = cursor.fetchone()
            if row and row.procedure_definition:
                return row.procedure_definition
            else:
                logger.error(f"Procedure {schema_name}.{procedure_name} not found")
                return ""
        except Exception as e:
            logger.error(f"Error getting procedure definition: {str(e)}")
            return ""

    async def get_procedure_parameters(self, schema_name: str, procedure_name: str) -> List[Dict[str, Any]]:
        """Get parameters for a specific stored procedure"""
        if not self.conn:
            await self.connect()
        
        cursor = self.conn.cursor()
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
        FROM 
            sys.parameters p
        INNER JOIN 
            sys.types t ON p.user_type_id = t.user_type_id
        INNER JOIN 
            sys.objects o ON p.object_id = o.object_id
        INNER JOIN 
            sys.schemas s ON o.schema_id = s.schema_id
        WHERE 
            o.type = 'P'
            AND s.name = ?
            AND o.name = ?
        ORDER BY 
            p.parameter_id;
        """
        
        try:
            cursor.execute(params_query, (schema_name, procedure_name))
            parameters = []
            for row in cursor.fetchall():
                parameters.append({
                    "parameter_name": row.parameter_name,
                    "data_type": row.data_type,
                    "max_length": row.max_length,
                    "precision": row.precision,
                    "scale": row.scale,
                    "is_output": bool(row.is_output),
                    "has_default_value": bool(row.has_default_value),
                })
            
            logger.info(f"Retrieved {len(parameters)} parameters for {schema_name}.{procedure_name}")
            return parameters
        except Exception as e:
            logger.error(f"Error retrieving parameters for {schema_name}.{procedure_name}: {str(e)}")
            return []
    
    async def search_stored_procedures(self, search_term: str) -> List[Dict[str, Any]]:
        """Search for stored procedures matching a search term"""
        if not self.conn:
            await self.connect()
        
        cursor = self.conn.cursor()
        search_query = """
        SELECT 
            p.name AS procedure_name,
            s.name AS schema_name,
            CAST(ISNULL(ep.value, '') AS NVARCHAR(MAX)) AS description,
            OBJECT_DEFINITION(p.object_id) AS procedure_definition
        FROM 
            sys.procedures p
        INNER JOIN 
            sys.schemas s ON p.schema_id = s.schema_id
        LEFT JOIN 
            sys.extended_properties ep ON ep.major_id = p.object_id AND ep.minor_id = 0 AND ep.name = 'MS_Description'
        WHERE 
            p.name LIKE ? OR
            CAST(ISNULL(ep.value, '') AS NVARCHAR(MAX)) LIKE ? OR
            OBJECT_DEFINITION(p.object_id) LIKE ?
        ORDER BY 
            s.name, p.name;
        """
        
        search_pattern = f'%{search_term}%'
        
        try:
            cursor.execute(search_query, (search_pattern, search_pattern, search_pattern))
            procedures = []
            for row in cursor.fetchall():
                # Extract just a snippet of the procedure definition containing the search term
                definition = row.procedure_definition or ""
                snippet = ""
                if search_term.lower() in definition.lower():
                    # Find the position of the search term
                    pos = definition.lower().find(search_term.lower())
                    start = max(0, pos - 100)
                    end = min(len(definition), pos + 100)
                    snippet = "..." + definition[start:end] + "..."
                
                procedures.append({
                    "procedure_name": row.procedure_name,
                    "schema_name": row.schema_name,
                    "description": row.description,
                    "snippet": snippet
                })
            
            logger.info(f"Found {len(procedures)} stored procedures matching '{search_term}'")
            return procedures
        except Exception as e:
            logger.error(f"Error searching stored procedures: {str(e)}")
            return []
    
    async def analyze_procedure(self, schema_name: str, procedure_name: str) -> Dict[str, Any]:
        """Analyze a stored procedure using GPT"""
        # Get procedure definition
        definition = await self.get_stored_procedure_definition(schema_name, procedure_name)
        if not definition:
            return {
                "success": False,
                "error": f"Procedure {schema_name}.{procedure_name} not found"
            }
        
        # Get procedure parameters
        parameters = await self.get_procedure_parameters(schema_name, procedure_name)
        
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
        
        1. PURPOSE: What is the main purpose of this stored procedure?
        2. PARAMETERS: Explain each parameter and how it's used
        3. LOGIC: Explain the main logic and processing steps
        4. TABLES: List all tables referenced (both read and modified)
        5. RETURN DATA: What data does this procedure return?
        6. POTENTIAL ISSUES: Are there any potential performance issues or bugs?
        7. USAGE EXAMPLE: Show an example of how to call this procedure with sample parameters
        
        FORMAT YOUR RESPONSE AS MARKDOWN with clear sections for each of the above points.
        """
        
        # Send request to GPT
        analysis = await self.ask_gpt(prompt)
        
        return {
            "success": True,
            "procedure_name": procedure_name,
            "schema_name": schema_name,
            "parameters": parameters,
            "definition": definition,
            "analysis": analysis
        }
    
    async def ask_gpt(self, prompt: str) -> str:
        """Send a prompt to OpenAI API and get response"""
        try:
            # Using OpenAI API with httpx client
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_api_key}"
            }
            
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
                "max_tokens": 4000
            }
            
            response = await self.openai_client.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            # Extract content from the response
            content = response_data["choices"][0]["message"]["content"]
            return content
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error when calling OpenAI API: {str(e)}")
            return f"Error calling OpenAI API: {str(e)}"
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            return f"Error: {str(e)}"
    
    async def execute_procedure(self, schema_name: str, procedure_name: str, 
                               parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a stored procedure with parameters"""
        if not self.conn:
            await self.connect()
        
        cursor = self.conn.cursor()
        start_time = time.time()
        
        # Build parameter string
        param_str = ""
        param_values = []
        
        if parameters:
            param_parts = []
            for name, value in parameters.items():
                name = name if name.startswith('@') else f'@{name}'
                param_parts.append(f"{name}=?")
                param_values.append(value)
            
            if param_parts:
                param_str = " " + ", ".join(param_parts)
        
        # Build EXEC statement
        exec_statement = f"EXEC {schema_name}.{procedure_name}{param_str}"
        
        try:
            # Execute the procedure
            cursor.execute(exec_statement, param_values)
            
            # If there are results to fetch
            if cursor.description:
                # Get column names
                columns = [column[0] for column in cursor.description]
                
                # Fetch rows (limited to 1000 for safety)
                rows = []
                count = 0
                max_rows = 1000
                
                for row in cursor:
                    if count >= max_rows:
                        break
                    rows.append([str(value) if value is not None else None for value in row])
                    count += 1
                
                has_more = False
                try:
                    # Check if there are more rows
                    more = cursor.fetchone()
                    if more:
                        has_more = True
                except:
                    pass
                
                duration = time.time() - start_time
                
                return {
                    "success": True,
                    "columns": columns,
                    "rows": rows,
                    "row_count": count,
                    "duration_seconds": duration,
                    "has_more_rows": has_more,
                    "message": f"Procedure returned {count} rows in {duration:.2f} seconds"
                }
            else:
                # For procedures without result sets
                row_count = cursor.rowcount
                duration = time.time() - start_time
                
                return {
                    "success": True,
                    "affected_rows": row_count,
                    "duration_seconds": duration,
                    "message": f"Procedure affected {row_count} rows in {duration:.2f} seconds"
                }
                
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Procedure execution error: {str(e)}")
            
            return {
                "success": False,
                "error": str(e),
                "duration_seconds": duration,
                "message": f"Error executing procedure: {str(e)}"
            }
    
    async def analyze_um_activity_log_procedures(self) -> str:
        """Specifically analyze the UM Activity Log Referrals procedures in your workspace"""
        try:
            # Look specifically for the procedure in your workspace
            results = await self.search_stored_procedures("USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET")
            
            if not results:
                return "No UM Activity Log Referrals procedures found in the database."
            
            # Analyze each found procedure
            analyses = []
            for proc in results:
                analysis = await self.analyze_procedure(proc["schema_name"], proc["procedure_name"])
                if analysis["success"]:
                    analyses.append(analysis)
            
            if not analyses:
                return "Found UM Activity Log Referrals procedures but could not analyze them."
            
            # Compare the procedures if multiple were found
            if len(analyses) > 1:
                comparison_prompt = f"""
                Please compare these related stored procedures:
                
                {json.dumps([{
                    "name": f"{a['schema_name']}.{a['procedure_name']}",
                    "definition": a["definition"][:1000] + "..." if len(a["definition"]) > 1000 else a["definition"]
                } for a in analyses], indent=2)}
                
                Provide a comparison explaining:
                1. How these procedures are related
                2. What are the key differences between them
                3. When you would use each one
                
                FORMAT YOUR RESPONSE AS MARKDOWN.
                """
                
                comparison = await self.ask_gpt(comparison_prompt)
                return comparison
            else:
                # Return the analysis of the single procedure
                return analyses[0]["analysis"]
        
        except Exception as e:
            logger.error(f"Error analyzing UM Activity Log procedures: {str(e)}")
            return f"Error analyzing procedures: {str(e)}"

async def main():
    """Main function to run the Stored Procedure Explorer"""
    explorer = StoredProcedureExplorer()
    
    # Connect to the database
    connected = await explorer.connect()
    if not connected:
        print("Failed to connect to database. Exiting.")
        return
    
    print(f"Connected to {SQL_DATABASE} on {SQL_SERVER}")
    
    print("\nAnalyzing USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET stored procedures...")
    analysis = await explorer.analyze_um_activity_log_procedures()
    
    print("\n" + "="*80)
    print("STORED PROCEDURE ANALYSIS:")
    print(analysis)
    print("="*80)
    
    print("\nWould you like to execute the procedure with test parameters? (y/n)")
    choice = input("> ").strip().lower()
    
    if choice == 'y':
        print("\nExecuting stored procedure with test parameters...")
        
        # Execute with some sample parameters
        result = await explorer.execute_procedure("dbo", "USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET", {
            "@UserID": "test_user",
            "@ReferralID": None,  # Using NULL to get all referrals
            "@DateType": "Created",
            "@FromDate": "2023-01-01",
            "@ToDate": "2023-12-31"
        })
        
        if result["success"]:
            print("\nProcedure executed successfully!")
            if "columns" in result and "rows" in result:
                # Display first few rows of results
                print(f"\nColumns: {', '.join(result['columns'])}")
                print(f"Showing first 5 of {result['row_count']} rows:")
                for i, row in enumerate(result['rows'][:5]):
                    print(f"Row {i+1}: {row}")
            else:
                print(f"\n{result['message']}")
        else:
            print(f"\nError executing procedure: {result['error']}")
    
    # Clean up
    explorer.close()
    print("\nDone!")

if __name__ == "__main__":
    # Configure SSL to ignore certificate verification
    import ssl
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    # Run the main async function
    asyncio.run(main())