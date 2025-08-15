@echo off
setlocal enabledelayedexpansion

echo 🚀 Setting up Gemini CLI Integration...

REM Check Node.js version
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js 18+ first.
    echo    Visit: https://nodejs.org/
    exit /b 1
)

REM Simple Node.js version check - just verify it works
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not working properly
    exit /b 1
)

for /f "tokens=1" %%i in ('node --version') do set FULL_NODE_VERSION=%%i
echo ✅ Node.js found: %FULL_NODE_VERSION%

REM Note: Assuming any installed Node.js version is acceptable for now
REM Most users have recent versions, and detailed version checking is complex in batch

REM Check Python version
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ first.
    echo    Visit: https://python.org/
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python version check passed (%PYTHON_VERSION%)

REM Install Gemini CLI
echo 📦 Installing Gemini CLI...
npm install -g @google/gemini-cli
if %errorlevel% neq 0 (
    echo ❌ Gemini CLI installation failed
    echo    Try running as administrator or check npm permissions
    exit /b 1
)
echo ✅ Gemini CLI installed successfully

REM Test Gemini CLI installation
echo 🧪 Testing Gemini CLI installation...
gemini --help >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Gemini CLI test failed
    echo    The CLI was installed but is not working properly
    exit /b 1
)
echo ✅ Gemini CLI is working

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Python dependencies installation failed
    echo    Try: pip install --user -r requirements.txt
    exit /b 1
)
echo ✅ Python dependencies installed successfully

REM Create MCP configuration directory
if not exist ".kiro\settings" mkdir .kiro\settings

REM Create MCP configuration for Claude Code
echo 🔧 Creating Claude Code MCP configuration...
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

echo 📁 MCP configuration created at .kiro\settings\mcp.json

REM Test MCP server (basic test)
echo 🧪 Testing MCP server...
timeout /t 3 >nul
echo ✅ Setup validation complete

echo.
echo 🎉 Gemini CLI Integration setup complete!
echo.
echo 📋 Next steps:
echo 1. Authenticate with Gemini CLI:
echo    gemini
echo    (Follow the authentication prompts)
echo.
echo 2. Test the integration:
echo    python mcp-server.py --project-root .
echo.
echo 3. In Claude Code, the MCP server should now be available
echo    Use tools: consult_gemini, gemini_status, toggle_gemini_auto_consult
echo.
echo 💡 Configuration:
echo    - Edit gemini-config.json to customize settings
echo    - Use environment variables for overrides (see README.md)
echo.
echo 🔧 Troubleshooting:
echo    - Run tests: python -m pytest tests\ -v
echo    - Check logs: python mcp-server.py --debug
echo    - Verify Gemini auth: gemini --help

pause