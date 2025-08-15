#!/bin/bash
set -e

echo "🚀 Gemini MCP Integration - Multi-Tool Setup"
echo "============================================="
echo ""
echo "This script will set up Gemini MCP Integration for:"
echo "- Claude Code"
echo "- Kiro"
echo "- Cursor"
echo ""

# Run the main setup
./setup-gemini-integration.sh
if [ $? -ne 0 ]; then
    echo "❌ Main setup failed"
    exit 1
fi

echo ""
echo "🔧 Creating MCP configurations for all tools..."

# Create Claude Code configuration
mkdir -p .claude/settings
cat > .claude/settings/mcp.json << 'EOF'
{
    "mcpServers": {
        "gemini-integration": {
            "command": "python3",
            "args": ["mcp-server.py", "--project-root", "."],
            "env": {
                "GEMINI_ENABLED": "true",
                "GEMINI_AUTO_CONSULT": "true",
                "GEMINI_MODEL": "gemini-2.5-flash"
            },
            "disabled": false,
            "autoApprove": ["gemini_status"]
        }
    }
}
EOF
echo "✅ Claude Code configuration created"

# Create Kiro configuration
mkdir -p .kiro/settings
cat > .kiro/settings/mcp.json << 'EOF'
{
    "mcpServers": {
        "gemini-integration": {
            "command": "python3",
            "args": ["mcp-server.py", "--project-root", "."],
            "env": {
                "GEMINI_ENABLED": "true",
                "GEMINI_AUTO_CONSULT": "true",
                "GEMINI_MODEL": "gemini-2.5-pro"
            },
            "disabled": false,
            "autoApprove": ["gemini_status"]
        }
    }
}
EOF
echo "✅ Kiro configuration created"

# Create Cursor configuration
mkdir -p .cursor/settings
cat > .cursor/settings/mcp.json << 'EOF'
{
    "mcpServers": {
        "gemini-integration": {
            "command": "python3",
            "args": ["mcp-server.py", "--project-root", "."],
            "env": {
                "GEMINI_ENABLED": "true",
                "GEMINI_AUTO_CONSULT": "true",
                "GEMINI_RATE_LIMIT": "3"
            },
            "disabled": false,
            "autoApprove": ["gemini_status"]
        }
    }
}
EOF
echo "✅ Cursor configuration created"

echo ""
echo "🎉 Multi-tool setup complete!"
echo ""
echo "📋 Available configurations:"
echo "- .claude/settings/mcp.json (Claude Code)"
echo "- .kiro/settings/mcp.json (Kiro)"
echo "- .cursor/settings/mcp.json (Cursor)"
echo ""
echo "🚀 Next steps:"
echo "1. Start the server: python3 mcp-server.py --project-root ."
echo "2. Open your preferred AI coding tool"
echo "3. The MCP server should be automatically detected"
echo ""
echo "💡 Available MCP tools in all supported editors:"
echo "- consult_gemini: Get Gemini's second opinion"
echo "- gemini_status: Check integration status"
echo "- toggle_gemini_auto_consult: Enable/disable auto consultation"