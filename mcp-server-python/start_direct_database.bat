@echo off
echo Starting OpenAI Database Chat (DIRECT CONNECTION)...
echo.

cd /d "%~dp0"

echo This version bypasses the MCP server completely
echo and connects directly to the SQL Server database.
echo.

echo Installing required packages...
pip install pyodbc httpx openai python-dotenv -q

echo.
echo Starting Direct Database Chat...
echo Type your questions about the database in natural language!
echo.

:: Run the direct database client
py direct_database.py

pause