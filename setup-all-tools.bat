@echo off
setlocal enabledelayedexpansion

echo 🚀 Gemini MCP Integration - Multi-Tool Setup
echo =============================================
echo.
echo This script will set up Gemini MCP Integration for:
echo - Claude Code
echo - Kiro
echo - Cursor
echo.

REM Run the main setup
call setup-gemini-integration.bat
if %errorlevel% neq 0 (
    echo ❌ Main setup failed
    pause
    exit /b 1
)

echo.
echo 🔧 Creating MCP configurations for all tools...

REM Create Claude Code configuration
if not exist ".claude\settings" mkdir .claude\settings
(
echo {
echo     "mcpServers": {
echo         "gemini-integration": {
echo             "command": "python",
echo             "args": ["mcp-server.py", "--project-root", "."],
echo             "env": {
echo                 "GEMINI_ENABLED": "true",
echo                 "GEMINI_AUTO_CONSULT": "true",
echo                 "GEMINI_MODEL": "gemini-2.5-flash"
echo             },
echo             "disabled": false,
echo             "autoApprove": ["gemini_status"]
echo         }
echo     }
echo }
) > .claude\settings\mcp.json
echo ✅ Claude Code configuration created

REM Create Kiro configuration
if not exist ".kiro\settings" mkdir .kiro\settings
(
echo {
echo     "mcpServers": {
echo         "gemini-integration": {
echo             "command": "python",
echo             "args": ["mcp-server.py", "--project-root", "."],
echo             "env": {
echo                 "GEMINI_ENABLED": "true",
echo                 "GEMINI_AUTO_CONSULT": "true",
echo                 "GEMINI_MODEL": "gemini-2.5-pro"
echo             },
echo             "disabled": false,
echo             "autoApprove": ["gemini_status"]
echo         }
echo     }
echo }
) > .kiro\settings\mcp.json
echo ✅ Kiro configuration created

REM Create Cursor configuration
if not exist ".cursor\settings" mkdir .cursor\settings
(
echo {
echo     "mcpServers": {
echo         "gemini-integration": {
echo             "command": "python",
echo             "args": ["mcp-server.py", "--project-root", "."],
echo             "env": {
echo                 "GEMINI_ENABLED": "true",
echo                 "GEMINI_AUTO_CONSULT": "true",
echo                 "GEMINI_RATE_LIMIT": "3"
echo             },
echo             "disabled": false,
echo             "autoApprove": ["gemini_status"]
echo         }
echo     }
echo }
) > .cursor\settings\mcp.json
echo ✅ Cursor configuration created

echo.
echo 🎉 Multi-tool setup complete!
echo.
echo 📋 Available configurations:
echo - .claude\settings\mcp.json (Claude Code)
echo - .kiro\settings\mcp.json (Kiro)
echo - .cursor\settings\mcp.json (Cursor)
echo.
echo 🚀 Next steps:
echo 1. Start the server: start-server.cmd
echo 2. Open your preferred AI coding tool
echo 3. The MCP server should be automatically detected
echo.
echo 💡 Available MCP tools in all supported editors:
echo - consult_gemini: Get Gemini's second opinion
echo - gemini_status: Check integration status
echo - toggle_gemini_auto_consult: Enable/disable auto consultation
echo.
pause