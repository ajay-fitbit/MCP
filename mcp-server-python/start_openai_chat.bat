@echo off
echo Starting OpenAI Database Chat...
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

:: Check if OpenAI API key is configured
findstr /C:"OPENAI_API_KEY=your-openai-api-key-here" .env >nul
if %ERRORLEVEL% EQU 0 (
    echo Error: OpenAI API key not configured!
    echo Please edit the .env file and add your OpenAI API key:
    echo OPENAI_API_KEY=your-actual-api-key
    echo.
    echo You can get an API key from: https://platform.openai.com/api-keys
    pause
    exit /b 1
)

echo Using Python environment: ..\.venv\Scripts\python.exe
echo.
echo 🤖 Starting OpenAI Database Chat...
echo Type your questions about the database in natural language!
echo.

:: Run the fixed launcher script instead of openai_client.py directly
"..\.venv\Scripts\python.exe" launch_openai_chat.py

pause