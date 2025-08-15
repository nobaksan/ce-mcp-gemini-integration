# Troubleshooting Guide

## Common Issues and Solutions

### 1. Gemini CLI Issues

#### Problem: "gemini command not found"
**Solution:**
```bash
# Install Gemini CLI
npm install -g @google/gemini-cli

# Verify installation
gemini --help
```

#### Problem: "Authentication required"
**Solution:**
```bash
# Run Gemini CLI interactively to authenticate
gemini

# Follow the prompts to sign in with your Google account
```

#### Problem: Node.js version issues
**Solution:**
```bash
# Check Node.js version (need 18+)
node --version

# Install/update Node.js
nvm install 22.16.0
nvm use 22.16.0

# Or download from https://nodejs.org/
```

### 2. MCP Server Issues

#### Problem: "Module not found" errors
**Solution:**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Or with user flag
pip install --user -r requirements.txt
```

#### Problem: MCP server won't start
**Solution:**
```bash
# Check Python version (need 3.8+)
python3 --version

# Run with debug mode
python3 mcp-server.py --debug

# Check for port conflicts
netstat -an | grep :8080
```

#### Problem: Configuration not loading
**Solution:**
```bash
# Verify config file exists and is valid JSON
cat gemini-config.json | python3 -m json.tool

# Check environment variables
env | grep GEMINI_

# Test with minimal config
echo '{"enabled": true}' > gemini-config.json
```

### 3. Claude Code Integration Issues

#### Problem: MCP server not appearing in Claude Code
**Solution:**
1. Check MCP configuration file location:
   - Workspace: `.kiro/settings/mcp.json`
   - User: `~/.kiro/settings/mcp.json`

2. Verify MCP configuration format:
```json
{
    "mcpServers": {
        "gemini-integration": {
            "command": "python3",
            "args": ["mcp-server.py", "--project-root", "."],
            "env": {
                "GEMINI_ENABLED": "true"
            }
        }
    }
}
```

3. Restart Claude Code after configuration changes

#### Problem: Tools not working in Claude Code
**Solution:**
1. Check MCP server logs:
```bash
python3 mcp-server.py --debug
```

2. Verify tool permissions in MCP config:
```json
{
    "autoApprove": ["gemini_status", "consult_gemini"]
}
```

3. Test tools manually:
```bash
# Test consultation
echo '{"query": "test"}' | python3 -c "
import json, asyncio
from mcp_server import MCPServer
server = MCPServer()
result = asyncio.run(server._handle_consult_gemini(json.loads(input())))
print(result)
"
```

### 4. Performance Issues

#### Problem: Slow Gemini responses
**Solution:**
```bash
# Increase timeout in config
export GEMINI_TIMEOUT=120

# Or in gemini-config.json
{
    "timeout": 120
}
```

#### Problem: Rate limiting errors
**Solution:**
```bash
# Increase rate limit delay
export GEMINI_RATE_LIMIT=5

# Or in gemini-config.json
{
    "rate_limit_delay": 5.0
}
```

### 5. Authentication Issues

#### Problem: Google account authentication fails
**Solution:**
1. Clear existing authentication:
```bash
# Remove cached credentials (location varies by OS)
rm -rf ~/.config/gemini-cli/  # Linux/Mac
# Or check %APPDATA%\gemini-cli\ on Windows
```

2. Re-authenticate:
```bash
gemini
# Follow prompts to sign in again
```

3. Check account permissions:
   - Ensure Google account has access to Gemini
   - Verify API quotas (free tier: 60 requests/minute, 1000/day)

### 6. Network Issues

#### Problem: Connection timeouts
**Solution:**
```bash
# Check network connectivity
ping google.com

# Test Gemini API directly
gemini -p "Hello, test message"

# Configure proxy if needed
export HTTP_PROXY=http://proxy:8080
export HTTPS_PROXY=http://proxy:8080
```

### 7. Testing and Debugging

#### Run comprehensive tests
```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_gemini_integration.py -v

# Run with coverage
pip install pytest-cov
python3 -m pytest tests/ --cov=. --cov-report=html
```

#### Debug mode
```bash
# Enable debug logging
python3 mcp-server.py --debug

# Or set environment variable
export GEMINI_DEBUG=true
python3 mcp-server.py
```

#### Manual testing
```bash
# Test Gemini CLI directly
echo "What is Python?" | gemini

# Test pattern detection
python3 -c "
from gemini_integration import GeminiIntegration
gi = GeminiIntegration()
print(gi.detect_uncertainty('I think this might work'))
"

# Test MCP server startup
python3 mcp-server.py --project-root . &
sleep 2
kill %1
```

### 8. Environment-Specific Issues

#### Windows Issues
- Use `python` instead of `python3`
- Use `pip` instead of `pip3`
- Run Command Prompt as Administrator for global npm installs
- Use `setup-gemini-integration.bat` instead of `.sh`

#### macOS Issues
- Install Node.js via Homebrew: `brew install node`
- Use `python3` and `pip3` explicitly
- May need to update PATH for npm global packages

#### Linux Issues
- Install Node.js via package manager or nvm
- May need `sudo` for global npm installs
- Ensure Python 3.8+ is available

### 9. Getting Help

If you're still experiencing issues:

1. **Check logs**: Run with `--debug` flag
2. **Verify versions**: Ensure Node.js 18+, Python 3.8+
3. **Test components**: Test Gemini CLI and MCP server separately
4. **Check configuration**: Validate JSON syntax and environment variables
5. **Review documentation**: Check README.md for setup instructions

### 10. Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `gemini: command not found` | Gemini CLI not installed | `npm install -g @google/gemini-cli` |
| `Authentication required` | Not signed in to Google | Run `gemini` and authenticate |
| `Module 'mcp' not found` | Missing Python dependencies | `pip install -r requirements.txt` |
| `Timeout after 60 seconds` | Slow network/API | Increase `GEMINI_TIMEOUT` |
| `Rate limit exceeded` | Too many requests | Increase `GEMINI_RATE_LIMIT` |
| `Invalid JSON` | Malformed config file | Validate JSON syntax |
| `Permission denied` | File/directory permissions | Check file permissions and ownership |