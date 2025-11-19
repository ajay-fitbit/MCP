@echo off
echo Testing OpenAI Connection...
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
    echo Please copy .env.example to .env and configure your settings.
    pause
    exit /b 1
)

echo Using Python environment: ..\.venv\Scripts\python.exe
echo.

:: Run the OpenAI connection test
"..\.venv\Scripts\python.exe" test_openai.py