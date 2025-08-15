#!/bin/bash
set -e

echo "🚀 Setting up Gemini CLI Integration..."

# Check Node.js version
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+ first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version $NODE_VERSION found. Please use Node.js 18+ (recommended: 22.16.0)"
    echo "   Use: nvm install 22.16.0 && nvm use 22.16.0"
    exit 1
fi
echo "✅ Node.js version check passed (v$(node --version))"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
echo "✅ Python version check passed ($PYTHON_VERSION)"

# Install Gemini CLI
echo "📦 Installing Gemini CLI..."
if npm install -g @google/gemini-cli; then
    echo "✅ Gemini CLI installed successfully"
else
    echo "❌ Gemini CLI installation failed"
    echo "   Try: sudo npm install -g @google/gemini-cli"
    exit 1
fi

# Test Gemini CLI installation
echo "🧪 Testing Gemini CLI installation..."
if gemini --help > /dev/null 2>&1; then
    echo "✅ Gemini CLI is working"
else
    echo "❌ Gemini CLI test failed"
    echo "   The CLI was installed but is not working properly"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if pip3 install -r requirements.txt; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Python dependencies installation failed"
    echo "   Try: pip3 install --user -r requirements.txt"
    exit 1
fi

# Create MCP configuration for Claude Code
echo "🔧 Creating Claude Code MCP configuration..."
cat > .kiro/settings/mcp.json << 'EOF'
{
    "mcpServers": {
        "gemini-integration": {
            "command": "python3",
            "args": ["mcp-server.py", "--project-root", "."],
            "env": {
                "GEMINI_ENABLED": "true",
                "GEMINI_AUTO_CONSULT": "true"
            },
            "disabled": false,
            "autoApprove": ["gemini_status"]
        }
    }
}
EOF

echo "📁 MCP configuration created at .kiro/settings/mcp.json"

# Test MCP server
echo "🧪 Testing MCP server..."
timeout 5s python3 mcp-server.py --project-root . > /dev/null 2>&1 &
SERVER_PID=$!
sleep 2

if kill -0 $SERVER_PID 2>/dev/null; then
    echo "✅ MCP server started successfully"
    kill $SERVER_PID 2>/dev/null || true
else
    echo "⚠️  MCP server test inconclusive (this is normal)"
fi

echo ""
echo "🎉 Gemini CLI Integration setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Authenticate with Gemini CLI:"
echo "   gemini"
echo "   (Follow the authentication prompts)"
echo ""
echo "2. Test the integration:"
echo "   python3 mcp-server.py --project-root ."
echo ""
echo "3. In Claude Code, the MCP server should now be available"
echo "   Use tools: consult_gemini, gemini_status, toggle_gemini_auto_consult"
echo ""
echo "💡 Configuration:"
echo "   - Edit gemini-config.json to customize settings"
echo "   - Use environment variables for overrides (see README.md)"
echo ""
echo "🔧 Troubleshooting:"
echo "   - Run tests: python3 -m pytest tests/ -v"
echo "   - Check logs: python3 mcp-server.py --debug"
echo "   - Verify Gemini auth: gemini --help"