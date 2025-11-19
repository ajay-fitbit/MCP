@echo off
echo Running MCP Database Demo (Simple)...
echo.

cd /d "%~dp0"

:: Check if virtual environment exists
if not exist "..\.venv\Scripts\python.exe" (
    echo Error: Virtual environment not found!
    echo Please run the setup first.
    pause
    exit /b 1
)

:: Check if .env file exists
if not exist ".env" (
    echo Error: .env file not found!
    echo Please copy .env.example to .env and configure your database settings.
    pause
    exit /b 1
)

echo Using Python environment: ..\.venv\Scripts\python.exe
echo.

:: Run the simple demo
"..\.venv\Scripts\python.exe" simple_demo.py

pause