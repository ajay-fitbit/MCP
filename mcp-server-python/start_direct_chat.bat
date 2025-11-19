@echo off
echo Starting OpenAI Database Chat (Direct Version)...
echo.

cd /d "%~dp0"

echo Using system Python (py)
echo.
echo Starting OpenAI Database Chat...
echo Type your questions about the database in natural language!
echo.

:: Run the direct chat script with no temp files
py direct_chat.py

pause