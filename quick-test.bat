@echo off
echo 🧪 Gemini MCP Integration - Quick Test
echo =====================================

REM Test Python
echo Testing Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python test failed
    goto :error
)
echo ✅ Python OK

REM Test Gemini CLI
echo Testing Gemini CLI...
gemini --help >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Gemini CLI test failed
    goto :error
)
echo ✅ Gemini CLI OK

REM Test Python dependencies
echo Testing Python dependencies...
python -c "import mcp, asyncio, json" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python dependencies test failed
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 goto :error
)
echo ✅ Dependencies OK

REM Test MCP server startup
echo Testing MCP server startup...
timeout /t 1 >nul
python -c "
import sys
sys.path.insert(0, '.')
try:
    from mcp_server import MCPServer
    server = MCPServer('.')
    print('✅ MCP Server OK')
except Exception as e:
    print(f'❌ MCP Server test failed: {e}')
    sys.exit(1)
"
if %errorlevel% neq 0 goto :error

REM Test Gemini integration
echo Testing Gemini integration...
python -c "
import sys
sys.path.insert(0, '.')
try:
    from gemini_integration import GeminiIntegration
    gi = GeminiIntegration()
    has_uncertainty, patterns = gi.detect_uncertainty('I think this might work')
    if has_uncertainty:
        print('✅ Pattern detection OK')
    else:
        print('❌ Pattern detection failed')
        sys.exit(1)
except Exception as e:
    print(f'❌ Gemini integration test failed: {e}')
    sys.exit(1)
"
if %errorlevel% neq 0 goto :error

echo.
echo 🎉 All tests passed! The system is ready to use.
echo.
echo 📋 Next steps:
echo 1. Run: start-server.cmd
echo 2. Or: run-gemini-mcp.bat
echo 3. Or: python mcp-server.py --project-root .
echo.
pause
exit /b 0

:error
echo.
echo ❌ Tests failed. Please check the error messages above.
echo 💡 Try running setup-gemini-integration.bat first.
echo 📖 Check TROUBLESHOOTING.md for help.
echo.
pause
exit /b 1