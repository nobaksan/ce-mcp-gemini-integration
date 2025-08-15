@echo off
setlocal enabledelayedexpansion

echo 🤖 Gemini MCP Integration Server
echo ================================

REM Check if Python is available
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ first.
    echo    Visit: https://python.org/
    pause
    exit /b 1
)

REM Check if Gemini CLI is available
where gemini >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Gemini CLI not found. Running setup...
    call setup-gemini-integration.bat
    if %errorlevel% neq 0 (
        echo ❌ Setup failed. Please run setup-gemini-integration.bat manually.
        pause
        exit /b 1
    )
)

REM Check if dependencies are installed
python -c "import mcp" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing Python dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies.
        pause
        exit /b 1
    )
)

REM Check if config file exists
if not exist "gemini-config.json" (
    echo 📝 Creating default configuration...
    (
    echo {
    echo     "enabled": true,
    echo     "auto_consult": true,
    echo     "cli_command": "gemini",
    echo     "timeout": 60,
    echo     "rate_limit_delay": 2.0,
    echo     "max_context_length": 4000,
    echo     "log_consultations": true,
    echo     "model": "gemini-2.5-flash",
    echo     "sandbox_mode": false,
    echo     "debug_mode": false
    echo }
    ) > gemini-config.json
    echo ✅ Configuration file created
)

REM Create MCP config directory if it doesn't exist
if not exist ".kiro\settings" mkdir .kiro\settings

REM Check if MCP config exists
if not exist ".kiro\settings\mcp.json" (
    echo 📝 Creating MCP configuration...
    (
    echo {
    echo     "mcpServers": {
    echo         "gemini-integration": {
    echo             "command": "python",
    echo             "args": ["mcp-server.py", "--project-root", "."],
    echo             "env": {
    echo                 "GEMINI_ENABLED": "true",
    echo                 "GEMINI_AUTO_CONSULT": "true"
    echo             },
    echo             "disabled": false,
    echo             "autoApprove": ["gemini_status"]
    echo         }
    echo     }
    echo }
    ) > .kiro\settings\mcp.json
    echo ✅ MCP configuration created
)

echo.
echo 🚀 Starting Gemini MCP Server...
echo.
echo 💡 Tips:
echo    - Press Ctrl+C to stop the server
echo    - Use --debug flag for detailed logging
echo    - Check TROUBLESHOOTING.md if you encounter issues
echo.

REM Start the server
python mcp-server.py --project-root .

echo.
echo 👋 Server stopped. Press any key to exit...
pause >nul