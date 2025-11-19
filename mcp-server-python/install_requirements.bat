@echo off
echo ===================================================
echo Installing MCP SDK and Required Packages
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
echo Creating a Python virtual environment...
py -m venv .venv
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create virtual environment
    echo Installing without virtual environment...
) else (
    echo Activating virtual environment...
    call .venv\Scripts\activate
)

echo.
echo Installing required packages from requirements.txt...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install packages from requirements.txt
    echo Installing core packages individually...
    
    echo Installing Python-dotenv...
    pip install python-dotenv
    
    echo Installing PyODBC...
    pip install pyodbc
    
    echo Installing OpenAI...
    pip install openai
    
    echo Installing HTTPX...
    pip install httpx
    
    echo Installing FastAPI and Uvicorn...
    pip install fastapi uvicorn
    
    echo Installing MCP SDK...
    pip install mcp[client]
)

echo.
echo Verifying MCP installation...
py -c "import mcp; print(f'MCP SDK version: {mcp.__version__}')"
if %ERRORLEVEL% NEQ 0 (
    echo Failed to import MCP module
    echo Attempting alternative installation methods...
    
    echo Installing MCP with pip...
    pip install --upgrade pip
    pip install mcp
    
    echo Checking installation...
    py -c "import mcp; print('MCP SDK installed successfully')"
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ===================================================
        echo ERROR: Failed to install MCP SDK
        echo ===================================================
        echo.
        echo Let's create a version that doesn't require MCP...
        echo.
        
        echo Creating server bypass version...
        copy direct_database.py direct_no_mcp.py
        echo @echo off > start_no_mcp.bat
        echo echo Starting direct database connection without MCP... >> start_no_mcp.bat
        echo python direct_no_mcp.py >> start_no_mcp.bat
        echo pause >> start_no_mcp.bat
        
        echo.
        echo Created start_no_mcp.bat that uses direct database connection
        echo without requiring the MCP package.
        echo.
        echo Please run: start_no_mcp.bat
    )
) else (
    echo.
    echo ===================================================
    echo SUCCESS: All packages installed successfully!
    echo ===================================================
    echo.
    echo You can now run:
    echo   .\start_server.bat       - to start the MCP server
    echo   .\start_openai_chat.bat  - to start the OpenAI client
)

pause