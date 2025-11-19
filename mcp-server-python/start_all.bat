@echo off
echo ===================================================
echo MCP Server and OpenAI Client Launcher
echo ===================================================
echo.

cd /d "%~dp0"

echo Checking Python environment...
py --version
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8 or newer
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install -q pyodbc httpx openai python-dotenv fastapi uvicorn websockets

echo.
echo === Available Options ===
echo.
echo 1. Start MCP Server
echo 2. Start OpenAI Client
echo 3. Start Direct Database Client
echo 4. Start Stored Procedure Explorer
echo 5. Install Dependencies Only
echo 6. Exit
echo.
set /p choice=Enter your choice (1-6): 

if "%choice%"=="1" (
    call :start_mcp_server
) else if "%choice%"=="2" (
    call :start_openai_client
) else if "%choice%"=="3" (
    call :start_direct_database
) else if "%choice%"=="4" (
    call :start_stored_proc_explorer
) else if "%choice%"=="5" (
    echo Dependencies installed successfully.
    pause
) else if "%choice%"=="6" (
    exit /b 0
) else (
    echo Invalid choice!
    pause
    exit /b 1
)

exit /b 0

:start_mcp_server
echo.
echo ===================================================
echo Starting MCP Server...
echo ===================================================
echo.
echo The Model Context Protocol server will start on port 8765
echo Please keep this window open while using the OpenAI client
echo.
start "MCP Server" cmd /c "py server.py && pause"
timeout /t 5
echo.
echo Would you like to start the OpenAI client now? (Y/N)
set /p start_client=
if /i "%start_client%"=="Y" call :start_openai_client
goto :eof

:start_openai_client
echo.
echo ===================================================
echo Starting OpenAI Client...
echo ===================================================
echo.
echo This will connect to the running MCP server
echo and allow you to query your database with OpenAI
echo.
py openai_client.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error starting OpenAI client.
    echo Would you like to try the direct database client instead? (Y/N)
    set /p try_direct=
    if /i "%try_direct%"=="Y" call :start_direct_database
)
pause
goto :eof

:start_direct_database
echo.
echo ===================================================
echo Starting Direct Database Client...
echo ===================================================
echo.
echo This client connects directly to the database
echo without requiring the MCP server to be running
echo.
py direct_database.py
pause
goto :eof

:start_stored_proc_explorer
echo.
echo ===================================================
echo Starting Stored Procedure Explorer...
echo ===================================================
echo.
echo This tool will analyze the USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET procedure
echo.
py stored_proc_explorer.py
pause
goto :eof