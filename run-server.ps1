# Simple PowerShell wrapper for running batch files
# This script helps PowerShell users run the batch files easily

param(
    [Parameter(Position=0)]
    [ValidateSet("start", "run", "test", "setup")]
    [string]$Action = "start",
    
    [switch]$Debug
)

Write-Host "🤖 Gemini MCP Integration - PowerShell Wrapper" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

switch ($Action) {
    "start" {
        Write-Host "🚀 Starting server with start-server.cmd..." -ForegroundColor Green
        cmd /c start-server.cmd
    }
    "run" {
        Write-Host "🚀 Running with advanced batch runner..." -ForegroundColor Green
        cmd /c run-gemini-mcp.bat
    }
    "test" {
        Write-Host "🧪 Running system tests..." -ForegroundColor Yellow
        cmd /c quick-test.bat
    }
    "setup" {
        Write-Host "⚙️ Running setup..." -ForegroundColor Blue
        cmd /c setup-gemini-integration.bat
    }
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Command failed with exit code: $LASTEXITCODE" -ForegroundColor Red
} else {
    Write-Host "✅ Command completed successfully" -ForegroundColor Green
}