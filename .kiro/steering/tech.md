# Technology Stack

## Core Technologies
- **Python 3.8+**: Main implementation language
- **MCP (Model Context Protocol)**: Communication protocol with AI tools
- **Google Gemini CLI**: External AI consultation service
- **Node.js 18+**: Required for Gemini CLI installation
- **asyncio**: Asynchronous Python programming

## Key Dependencies
- `mcp>=1.0.0`: MCP server implementation
- `pydantic>=2.0.0`: Data validation and settings
- `pytest>=7.0.0`: Testing framework
- `pytest-asyncio>=0.21.0`: Async testing support
- `pytest-mock>=3.10.0`: Mocking utilities

## Architecture Patterns
- **Singleton Pattern**: `GeminiIntegration` class uses singleton for shared state
- **MCP Server Pattern**: Standard MCP tool registration and handling
- **Configuration Hierarchy**: JSON file + environment variable overrides
- **Rate Limiting**: Built-in consultation throttling
- **Error Handling**: Structured error types with user-friendly suggestions

## Build & Development Commands

### Setup
```bash
# Windows
setup-gemini-integration.bat
setup-all-tools.bat

# Linux/macOS  
chmod +x setup-gemini-integration.sh
./setup-gemini-integration.sh
```

### Running
```bash
# Basic server start
python mcp-server.py --project-root .

# Debug mode
python mcp-server.py --debug

# Windows shortcuts
start-server.cmd
run-gemini-mcp.bat
```

### Testing
```bash
# Run all tests
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_mcp_server.py -v

# With coverage
python -m pytest tests/ --cov=. --cov-report=html

# Quick system test (Windows)
quick-test.bat
```

### Authentication
```bash
# Interactive Gemini CLI auth
gemini

# Verify authentication
gemini --help
```

## Platform Support
- **Windows**: Primary platform with .bat/.cmd/.ps1 scripts
- **Linux/macOS**: Shell scripts and standard Python execution
- **Cross-platform**: Python code works on all platforms