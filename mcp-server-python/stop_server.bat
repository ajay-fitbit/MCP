@echo off
echo Stopping MCP Database Server...
echo.

:: Find the Python process running server.py and kill it
for /f "tokens=1" %%i in ('tasklist /fi "imagename eq python.exe" /fo csv /nh ^| findstr "server.py"') do (
    echo Stopping process %%i
    taskkill /f /pid %%i
)

:: Alternative approach using wmic
echo Searching for Python processes running server.py...
wmic process where "commandline like '%%server.py%%' and name='python.exe'" call terminate

echo.
echo MCP Server should now be stopped.
echo.

pause