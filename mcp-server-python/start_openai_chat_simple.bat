@echo off
echo Starting OpenAI Database Chat (Simple Version)...
echo.

cd /d "%~dp0"

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

echo Using system Python (py)
echo.
echo Starting OpenAI Database Chat...
echo Type your questions about the database in natural language!
echo.

:: Run the simple launcher script with system Python
py simple_launcher.py

pause