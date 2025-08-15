# Gemini MCP Integration Server - PowerShell Script
# Requires PowerShell 5.0 or later

param(
    [switch]$Debug,
    [switch]$Setup,
    [string]$ProjectRoot = "."
)

# Set console encoding to UTF-8 for emoji support
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "🤖 Gemini MCP Integration Server" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if a command exists
function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Function to test Python import
function Test-PythonModule {
    param([string]$Module)
    try {
        $result = python -c "import $Module" 2>&1
        return $LASTEXITCODE -eq 0
    }
    catch {
        return $false
    }
}

# Check Python installation
if (-not (Test-Command "python")) {
    Write-Host "❌ Python not found. Please install Python 3.8+ first." -ForegroundColor Red
    Write-Host "   Visit: https://python.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

$pythonVersion = python --version 2>&1
Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green

# Check Gemini CLI installation
if (-not (Test-Command "gemini")) {
    Write-Host "❌ Gemini CLI not found." -ForegroundColor Red
    
    if ($Setup) {
        Write-Host "🔧 Running setup..." -ForegroundColor Yellow
        & ".\setup-gemini-integration.bat"
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Setup failed. Please run setup manually." -ForegroundColor Red
            Read-Host "Press Enter to exit"
            exit 1
        }
    } else {
        Write-Host "💡 Run with -Setup flag to install automatically, or run setup-gemini-integration.bat" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "✅ Gemini CLI found" -ForegroundColor Green

# Check Python dependencies
if (-not (Test-PythonModule "mcp")) {
    Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
}

# Check configuration file
if (-not (Test-Path "gemini-config.json")) {
    Write-Host "📝 Creating default configuration..." -ForegroundColor Yellow
    
    $defaultConfig = @{
        enabled = $true
        auto_consult = $true
        cli_command = "gemini"
        timeout = 60
        rate_limit_delay = 2.0
        max_context_length = 4000
        log_consultations = $true
        model = "gemini-2.5-flash"
        sandbox_mode = $false
        debug_mode = $false
    }
    
    $defaultConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath "gemini-config.json" -Encoding UTF8
    Write-Host "✅ Configuration file created" -ForegroundColor Green
}

# Create MCP configuration directory
$mcpDir = ".kiro\settings"
if (-not (Test-Path $mcpDir)) {
    New-Item -ItemType Directory -Path $mcpDir -Force | Out-Null
}

# Check MCP configuration
$mcpConfigPath = "$mcpDir\mcp.json"
if (-not (Test-Path $mcpConfigPath)) {
    Write-Host "📝 Creating MCP configuration..." -ForegroundColor Yellow
    
    $mcpConfig = @{
        mcpServers = @{
            "gemini-integration" = @{
                command = "python"
                args = @("mcp-server.py", "--project-root", ".")
                env = @{
                    GEMINI_ENABLED = "true"
                    GEMINI_AUTO_CONSULT = "true"
                }
                disabled = $false
                autoApprove = @("gemini_status")
            }
        }
    }
    
    $mcpConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath $mcpConfigPath -Encoding UTF8
    Write-Host "✅ MCP configuration created" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Starting Gemini MCP Server..." -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Tips:" -ForegroundColor Yellow
Write-Host "   - Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host "   - Use -Debug flag for detailed logging" -ForegroundColor Gray
Write-Host "   - Check TROUBLESHOOTING.md if you encounter issues" -ForegroundColor Gray
Write-Host ""

# Prepare server arguments
$serverArgs = @("mcp-server.py", "--project-root", $ProjectRoot)
if ($Debug) {
    $serverArgs += "--debug"
    Write-Host "🐛 Debug mode enabled" -ForegroundColor Yellow
}

# Start the server
try {
    & python @serverArgs
}
catch {
    Write-Host "❌ Server error: $_" -ForegroundColor Red
}
finally {
    Write-Host ""
    Write-Host "👋 Server stopped." -ForegroundColor Yellow
    if (-not $Debug) {
        Read-Host "Press Enter to exit"
    }
}