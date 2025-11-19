@echo off
echo ===================================================
echo Claude Desktop Configuration Fix
echo ===================================================
echo.

cd /d "%~dp0"

echo Checking Claude Desktop installation...
set CONFIG_DIR=%APPDATA%\Claude
if not exist "%CONFIG_DIR%" (
    echo ERROR: Claude Desktop configuration directory not found!
    echo Please make sure Claude Desktop is installed.
    pause
    exit /b 1
)

echo.
echo Backing up existing configuration...
if exist "%CONFIG_DIR%\claude_desktop_config.json" (
    copy "%CONFIG_DIR%\claude_desktop_config.json" "%CONFIG_DIR%\claude_desktop_config.backup.json"
    echo Backup created at: %CONFIG_DIR%\claude_desktop_config.backup.json
)

echo.
echo Copying updated configuration to Claude Desktop...
copy "updated_claude_config.json" "%CONFIG_DIR%\claude_desktop_config.json"
echo Configuration updated successfully!

echo.
echo Creating required environment...
if not exist "..\.venv\Scripts\python.exe" (
    echo Creating Python virtual environment...
    python -m venv ..\.venv
    
    echo Installing required packages...
    ..\.venv\Scripts\pip install -r requirements.txt
)

echo.
echo Testing MCP server connection...
echo.
echo Starting MCP server directly to test...
start "Test MCP Server" /b cmd /c "..\.venv\Scripts\python.exe server.py"
timeout /t 5

echo.
echo ===================================================
echo IMPORTANT: Next Steps
echo ===================================================
echo.
echo 1. COMPLETELY CLOSE Claude Desktop if it's running
echo    (Check system tray and Task Manager)
echo.
echo 2. Restart Claude Desktop
echo.
echo 3. Try these test queries:
echo    - "What tables are in my database?"
echo    - "Show me the structure of one table"
echo.
echo If Claude still can't connect to the database:
echo - Check that your database server is accessible
echo - Make sure SQL Server is running
echo - Try running .\start_server.bat manually to check for errors
echo ===================================================

echo.
echo Press any key to close MCP server test and continue...
pause > nul

echo.
echo Stopping test MCP server...
taskkill /f /im python.exe /fi "WINDOWTITLE eq Test MCP Server"

echo.
pause