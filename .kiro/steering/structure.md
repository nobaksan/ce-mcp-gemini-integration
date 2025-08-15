# Project Structure

## Root Directory Layout
```
├── gemini_integration.py      # Core integration module (singleton pattern)
├── mcp-server.py             # MCP server implementation
├── gemini-config.json        # Configuration file (optional)
├── requirements.txt          # Python dependencies
├── README.md                 # Main documentation
├── TROUBLESHOOTING.md        # Problem resolution guide
├── WINDOWS-USAGE.md          # Windows-specific instructions
└── tests/                    # Test suite
```

## Setup Scripts
- **Windows**: `setup-gemini-integration.bat`, `setup-all-tools.bat`
- **Linux/macOS**: `setup-gemini-integration.sh`, `setup-all-tools.sh`
- **Cross-platform**: Automated dependency installation and MCP configuration

## Execution Scripts
- **Windows**: `start-server.cmd`, `run-gemini-mcp.bat`, `run-gemini-mcp.ps1`, `quick-test.bat`
- **Linux/macOS**: Direct Python execution with arguments
- **Debug**: `--debug` flag available on all platforms

## Configuration Structure
### MCP Settings (per AI tool)
- `.claude/settings/mcp.json` - Claude Code configuration
- `.kiro/settings/mcp.json` - Kiro configuration  
- `.cursor/settings/mcp.json` - Cursor configuration

### Gemini Configuration
- `gemini-config.json` - Base configuration file
- Environment variables override file settings
- Singleton pattern ensures consistent state across tools

## Test Organization
```
tests/
├── test_gemini_integration.py  # Core integration tests
├── test_gemini_cli.py          # CLI interaction tests
├── test_mcp_server.py          # MCP server tests
└── __init__.py                 # Test package marker
```

## Code Organization Principles
- **Single Responsibility**: Each module has a clear purpose
- **Separation of Concerns**: MCP server, Gemini integration, and configuration are separate
- **Platform Abstraction**: Python code is platform-agnostic, scripts handle platform differences
- **Configuration Hierarchy**: File-based defaults with environment overrides
- **Error Boundaries**: Structured error handling with user-friendly messages

## File Naming Conventions
- **Python modules**: `snake_case.py`
- **Windows scripts**: `.bat`, `.cmd`, `.ps1` extensions
- **Shell scripts**: `.sh` extension with executable permissions
- **Config files**: `kebab-case.json` or `UPPERCASE.md` for docs
- **Test files**: `test_*.py` pattern for pytest discovery