@echo off
echo ===================================================
echo MCP Package Verification
echo ===================================================
echo.

cd /d "%~dp0"

if exist "..\.venv\Scripts\python.exe" (
    echo Using virtual environment Python...
    "..\.venv\Scripts\python.exe" verify_mcp_package.py
) else (
    echo Using system Python...
    python verify_mcp_package.py
)

echo.
if %ERRORLEVEL% EQU 0 (
    echo ===================================================
    echo The MCP package is properly installed!
    echo Now run simplified_claude_config.bat to update your
    echo Claude Desktop configuration.
    echo ===================================================
) else (
    echo ===================================================
    echo ❌ MCP package verification failed!
    echo.
    echo Installing required packages...
    if exist "..\.venv\Scripts\pip.exe" (
        "..\.venv\Scripts\pip.exe" install mcp[client] pyodbc python-dotenv --upgrade
    ) else (
        pip install mcp[client] pyodbc python-dotenv --upgrade
    )
    echo.
    echo Please run this verification script again after installation.
    echo ===================================================
)

echo.
pause