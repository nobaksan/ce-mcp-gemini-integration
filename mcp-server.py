#!/usr/bin/env python3
"""
MCP Server with Gemini Integration
Provides development workflow automation with AI second opinions
"""
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

# Import Gemini integration
from gemini_integration import get_integration


class MCPServer:
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.server = Server("gemini-mcp-integration")
        
        # Initialize Gemini integration with singleton pattern
        self.gemini_config = self._load_gemini_config()
        # Get the singleton instance, passing config on first call
        self.gemini = get_integration(self.gemini_config)
        
        self._setup_tools()
        
        print(f"MCP Server initialized with project root: {self.project_root}")
        print(f"Gemini integration enabled: {self.gemini.enabled}")

    def _load_gemini_config(self) -> Dict[str, Any]:
        """Load Gemini configuration from file and environment"""
        config = {}
        
        # Load from config file if exists
        config_file = self.project_root / "gemini-config.json"
        if config_file.exists():
            try:
                with open(config_file) as f:
                    config = json.load(f)
                print(f"Loaded configuration from {config_file}")
            except Exception as e:
                print(f"Warning: Failed to load config file {config_file}: {e}")
                config = {}
        else:
            print(f"No config file found at {config_file}, using defaults")
        
        # Override with environment variables
        env_mapping = {
            'GEMINI_ENABLED': ('enabled', lambda x: x.lower() == 'true'),
            'GEMINI_AUTO_CONSULT': ('auto_consult', lambda x: x.lower() == 'true'),
            'GEMINI_CLI_COMMAND': ('cli_command', str),
            'GEMINI_TIMEOUT': ('timeout', int),
            'GEMINI_RATE_LIMIT': ('rate_limit_delay', float),
            'GEMINI_MODEL': ('model', str),
            'GEMINI_MAX_CONTEXT': ('max_context_length', int),
        }
        
        env_overrides = 0
        for env_key, (config_key, converter) in env_mapping.items():
            value = os.getenv(env_key)
            if value is not None:
                try:
                    config[config_key] = converter(value)
                    env_overrides += 1
                except ValueError as e:
                    print(f"Warning: Invalid value for {env_key}: {value} ({e})")
        
        if env_overrides > 0:
            print(f"Applied {env_overrides} environment variable overrides")
        
        return config

    def _setup_tools(self):
        """Register all MCP tools"""
        @self.server.list_tools()
        async def handle_list_tools():
            return [
                types.Tool(
                    name="consult_gemini",
                    description="Consult Gemini for a second opinion or validation",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The question or topic to consult Gemini about"
                            },
                            "context": {
                                "type": "string",
                                "description": "Additional context for the consultation"
                            },
                            "comparison_mode": {
                                "type": "boolean",
                                "description": "Whether to request structured comparison format",
                                "default": True
                            }
                        },
                        "required": ["query"]
                    }
                ),
                types.Tool(
                    name="gemini_status",
                    description="Check Gemini integration status and statistics",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                types.Tool(
                    name="toggle_gemini_auto_consult",
                    description="Enable or disable automatic Gemini consultation",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "enable": {
                                "type": "boolean",
                                "description": "Enable (true) or disable (false) auto-consultation"
                            }
                        },
                        "required": []
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]):
            if name == "consult_gemini":
                return await self._handle_consult_gemini(arguments)
            elif name == "gemini_status":
                return await self._handle_gemini_status(arguments)
            elif name == "toggle_gemini_auto_consult":
                return await self._handle_toggle_auto_consult(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")

    async def _handle_consult_gemini(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle Gemini consultation requests"""
        query = arguments.get('query', '')
        context = arguments.get('context', '')
        comparison_mode = arguments.get('comparison_mode', True)
        
        if not query:
            return [types.TextContent(
                type="text",
                text="❌ Error: 'query' parameter is required for Gemini consultation"
            )]
        
        print(f"Processing Gemini consultation request: {query[:50]}...")
        
        result = await self.gemini.consult_gemini(
            query=query,
            context=context,
            comparison_mode=comparison_mode
        )
        
        if result['status'] == 'success':
            response_text = f"🤖 **Gemini Second Opinion**\n\n{result['response']}\n\n"
            response_text += f"⏱️ *Consultation completed in {result['execution_time']:.2f}s*"
            response_text += f"\n📋 *Consultation ID: {result['consultation_id']}*"
        elif result['status'] == 'disabled':
            response_text = "⚠️ **Gemini Integration Disabled**\n\nGemini integration is currently disabled. Enable it with the toggle_gemini_auto_consult tool."
        else:
            error_suggestion = self.gemini.get_error_suggestion(result.get('error_type', 'unknown'))
            response_text = f"❌ **Gemini Consultation Failed**\n\n"
            response_text += f"**Error:** {result.get('error', 'Unknown error')}\n\n"
            response_text += f"**Suggestion:** {error_suggestion}"
        
        return [types.TextContent(type="text", text=response_text)]

    async def _handle_gemini_status(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle Gemini status requests"""
        status_info = self.gemini.get_status_info()
        
        status_lines = [
            "🤖 **Gemini Integration Status**",
            "",
            f"• **Enabled**: {'✅ Yes' if status_info['enabled'] else '❌ No'}",
            f"• **Auto-consult**: {'✅ Yes' if status_info['auto_consult'] else '❌ No'}",
            f"• **CLI Command**: `{status_info['cli_command']}`",
            f"• **Model**: {status_info['model']}",
            f"• **Rate Limit**: {status_info['rate_limit_delay']}s between calls",
            f"• **Timeout**: {status_info['timeout']}s",
            f"• **Max Context**: {status_info['max_context_length']} characters",
            "",
            f"📊 **Statistics**:",
            f"• **Total Consultations**: {status_info['total_consultations']}",
            f"• **Successful**: {status_info['successful_consultations']}",
            f"• **Failed**: {status_info['failed_consultations']}",
        ]
        
        if status_info['last_consultation']:
            status_lines.append(f"• **Last Consultation**: {status_info['last_consultation']}")
        
        return [types.TextContent(type="text", text="\n".join(status_lines))]
    
    async def _handle_toggle_auto_consult(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle toggle auto-consultation requests"""
        enable = arguments.get('enable')
        
        if enable is None:
            # Toggle current state
            self.gemini.auto_consult = not self.gemini.auto_consult
        else:
            self.gemini.auto_consult = enable
        
        status = "enabled" if self.gemini.auto_consult else "disabled"
        response_text = f"🔄 **Auto-consultation {status}**\n\n"
        
        if self.gemini.auto_consult:
            response_text += "Gemini will now be automatically consulted when uncertainty patterns are detected."
        else:
            response_text += "Automatic consultation disabled. Use consult_gemini tool for manual consultations."
        
        print(f"Auto-consultation {status}")
        
        return [types.TextContent(
            type="text",
            text=response_text
        )]

    async def run(self):
        """Run the MCP server"""
        print("Starting MCP server...")
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP Server with Gemini Integration")
    parser.add_argument("--project-root", type=str, default=".", 
                       help="Project root directory (default: current directory)")
    parser.add_argument("--debug", action="store_true", 
                       help="Enable debug logging")
    
    args = parser.parse_args()
    
    if args.debug:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
        print("Debug logging enabled")
    
    try:
        server = MCPServer(project_root=args.project_root)
        await server.run()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())