@echo off
echo Starting OpenAI Database Chat (HTTP Client)...
echo.

cd /d "%~dp0"

echo This version connects to an already running MCP server
echo Make sure the server is running in another terminal with .\start_server.bat
echo.

:: Set the MCP server URL - modify if your server uses a different port
set MCP_SERVER_URL=http://localhost:8765

echo Using server URL: %MCP_SERVER_URL%
echo.
echo Starting OpenAI Chat...
echo Type your questions about the database in natural language!
echo.

:: Run the server client Python script
py server_client.py

pause