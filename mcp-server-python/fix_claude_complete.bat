@echo off
echo ===================================================
echo All-In-One Claude Desktop Database Fix
echo ===================================================
echo.

cd /d "%~dp0"

echo Step 1: Verifying MCP package...
call verify_mcp.bat

echo Step 2: Testing direct database connection...
call test_sql_direct.bat

echo Step 3: Updating Claude Desktop configuration...
call simplified_claude_config.bat

echo Step 4: Running MCP server directly to confirm it works...
start "MCP Server Test" cmd /c "..\.venv\Scripts\python.exe server.py"

echo.
echo ===================================================
echo FINAL STEPS - VERY IMPORTANT
echo ===================================================
echo.
echo 1. Verify the MCP server window shows:
echo    "Connected to database successfully"
echo.
echo 2. Completely exit Claude Desktop if it's running
echo    (use Task Manager to make sure it's closed)
echo.
echo 3. Start Claude Desktop again
echo.
echo 4. Try these test queries:
echo    - "What tables are in my database?"
echo    - "Connect to my SQL Server database"
echo    - "Use database AHS-LP-945 with name Ahs_Bit_Red_QA_8170"
echo ===================================================

echo.
echo Press any key when ready to continue...
pause > nul

echo.
echo Stopping test MCP server...
taskkill /f /im python.exe /fi "WINDOWTITLE eq MCP Server Test"

echo.
pause