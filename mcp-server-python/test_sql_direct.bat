@echo off
echo ===================================================
echo Direct SQL Server Connection Test
echo ===================================================

cd /d "%~dp0"

echo Testing direct connection to SQL Server...
echo Server: AHS-LP-945
echo Database: Ahs_Bit_Red_QA_8170
echo.

:: Try connecting with sqlcmd (SQL Server command-line tool)
echo Using sqlcmd to test connection:
sqlcmd -S AHS-LP-945 -d Ahs_Bit_Red_QA_8170 -E -Q "SELECT @@VERSION" -b

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Connection failed with sqlcmd!
    echo Checking SQL Server configuration...
    echo.
    echo Testing alternative connection with PowerShell...
    
    powershell -Command "$conn = New-Object System.Data.SqlClient.SqlConnection; $conn.ConnectionString = 'Server=AHS-LP-945;Database=Ahs_Bit_Red_QA_8170;Integrated Security=True;'; try { $conn.Open(); Write-Host 'Connection successful!'; $conn.Close(); exit 0; } catch { Write-Host 'Connection failed: ' $_.Exception.Message; exit 1; }"
    
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ===================================================
        echo SQL SERVER CONNECTION FAILED!
        echo.
        echo Possible issues:
        echo 1. SQL Server might not be running
        echo 2. Server name might be incorrect
        echo 3. Network connectivity issues
        echo 4. Windows authentication not working
        echo ===================================================
    )
) else (
    echo.
    echo ===================================================
    echo SQL SERVER CONNECTION SUCCESSFUL!
    echo.
    echo This confirms your database is accessible.
    echo ===================================================
)

echo.
echo Now testing Python connection to database...

if exist "..\.venv\Scripts\python.exe" (
    "..\.venv\Scripts\python.exe" test_db_connection.py
) else (
    python test_db_connection.py
)

echo.
echo ===================================================
echo Next steps for Claude Desktop:
echo.
echo 1. Make sure mcp package is installed:
echo    ..\.venv\Scripts\pip install mcp[client]
echo.
echo 2. Try creating a simplified config for Claude:
echo    Running simplified_claude_config.bat now...
echo ===================================================

pause