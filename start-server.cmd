@echo off
REM Simple Windows launcher for Gemini MCP Server

title Gemini MCP Integration Server

REM Change to script directory
cd /d "%~dp0"

REM Check if we should run setup first
if not exist "gemini-config.json" (
    echo First time setup required...
    call setup-gemini-integration.bat
    if errorlevel 1 (
        echo Setup failed. Please check the error messages above.
        pause
        exit /b 1
    )
)

REM Run the server
echo Starting Gemini MCP Server...
python mcp-server.py --project-root .

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Server exited with error code %errorlevel%
    echo Check the error messages above for troubleshooting.
    pause
)