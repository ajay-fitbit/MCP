@echo off
echo Verifying Claude Desktop Configuration...
echo.

cd /d "%~dp0"

:: Check if virtual environment exists
if not exist "..\.venv\Scripts\python.exe" (
    echo Error: Virtual environment not found!
    echo Please run the setup first.
    pause
    exit /b 1
)

echo Using Python environment: ..\.venv\Scripts\python.exe
echo.

:: Run the verification
"..\.venv\Scripts\python.exe" verify_claude_config.py