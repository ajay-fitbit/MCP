@echo off
echo ===================================================
echo Simplified Claude Desktop Configuration
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
    copy "%CONFIG_DIR%\claude_desktop_config.json" "%CONFIG_DIR%\claude_desktop_config.backup2.json"
    echo Backup created at: %CONFIG_DIR%\claude_desktop_config.backup2.json
)

echo.
echo Installing MCP package if needed...
echo.
if exist "..\.venv\Scripts\pip.exe" (
    echo Using virtual environment pip...
    "..\.venv\Scripts\pip.exe" install mcp[client] --upgrade
) else (
    echo Using system pip...
    pip install mcp[client] --upgrade
)

echo.
echo Copying simplified configuration to Claude Desktop...
copy "simplified_claude_config.json" "%CONFIG_DIR%\claude_desktop_config.json"
echo Configuration updated successfully!

echo.
echo ===================================================
echo CRITICAL STEPS TO FOLLOW:
echo.
echo 1. COMPLETELY EXIT Claude Desktop:
echo    - Right-click on the Claude icon in system tray
echo    - Select "Quit" or "Exit"
echo    - Check Task Manager to ensure it's fully closed
echo.
echo 2. MANUALLY CHECK THE SERVER WORKS:
echo    Run this command in a new terminal:
echo    ..\.venv\Scripts\python.exe server.py
echo.
echo 3. RESTART Claude Desktop after verifying the server works
echo.
echo 4. If Claude still asks for database details, try:
echo    - "Connect to my database" (in Claude)
echo    - "Use AHS-LP-945 database Ahs_Bit_Red_QA_8170"
echo ===================================================

echo.
pause