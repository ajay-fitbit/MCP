@echo off
echo Setting up Claude Desktop MCP Configuration...
echo.

cd /d "%~dp0"

:: Define the Claude Desktop config directory
set "CLAUDE_CONFIG_DIR=%APPDATA%\Claude"
set "CLAUDE_CONFIG_FILE=%CLAUDE_CONFIG_DIR%\claude_desktop_config.json"

echo 📁 Claude Desktop config location: %CLAUDE_CONFIG_FILE%
echo.

:: Check if Claude Desktop is installed
if not exist "%CLAUDE_CONFIG_DIR%" (
    echo ❌ Claude Desktop config directory not found!
    echo    Please make sure Claude Desktop is installed first.
    echo    Download from: https://claude.ai/download
    echo.
    echo    After installing Claude Desktop, run this script again.
    pause
    exit /b 1
)

echo ✅ Claude Desktop config directory found
echo.

:: Backup existing config if it exists
if exist "%CLAUDE_CONFIG_FILE%" (
    echo 📋 Backing up existing config...
    copy "%CLAUDE_CONFIG_FILE%" "%CLAUDE_CONFIG_FILE%.backup.%date:~-4,4%%date:~-10,2%%date:~-7,2%"
    echo ✅ Backup created: %CLAUDE_CONFIG_FILE%.backup.%date:~-4,4%%date:~-10,2%%date:~-7,2%
    echo.
)

:: Copy our config file
echo 🔧 Installing MCP database server configuration...
copy "claude_desktop_config.json" "%CLAUDE_CONFIG_FILE%"

if %ERRORLEVEL% EQU 0 (
    echo ✅ Configuration installed successfully!
    echo.
    echo 🎉 Claude Desktop is now configured to use your database!
    echo.
    echo 📋 Next steps:
    echo    1. Restart Claude Desktop if it's running
    echo    2. Open Claude Desktop
    echo    3. Try asking Claude about your database:
    echo.
    echo 💡 Example prompts to try:
    echo    "List all tables in my database"
    echo    "Show me the structure of the PATIENT_DETAILS table"
    echo    "Execute USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET with LOGIN_USERID 68"
    echo    "How many records are in CARE_STAFF_DETAILS?"
    echo    "Show me the first 5 patients from PATIENT_DETAILS"
    echo.
    echo 🔧 Configuration details:
    echo    Server: AHS-LP-945
    echo    Database: Ahs_Bit_Red_QA_8170
    echo    Authentication: Windows Authentication
    echo.
) else (
    echo ❌ Failed to install configuration
    echo    Please check permissions and try running as administrator
)

pause