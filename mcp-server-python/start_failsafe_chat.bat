@echo off
echo Starting OpenAI Database Chat (FAILSAFE VERSION)...
echo.

cd /d "%~dp0"

echo Using system Python (py)
echo.
echo Starting OpenAI Database Chat (Failsafe)...
echo This uses the most robust approach to avoid event loop and encoding issues
echo.

:: Run the failsafe launcher 
py failsafe_launcher.py

pause