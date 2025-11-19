@echo off
echo Starting Stored Procedure Explorer...
echo.

cd /d "%~dp0"

echo Installing required packages...
pip install pyodbc httpx openai python-dotenv -q

echo.
echo Starting SQL Stored Procedure Explorer...
echo This tool will analyze the USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET procedure
echo.

:: Run the stored procedure explorer
py stored_proc_explorer.py

pause