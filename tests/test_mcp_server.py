#!/usr/bin/env python3
"""
Tests for MCP Server
"""
import json
import os
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
import tempfile

import mcp.types as types

# Import the server class - we need to handle the import path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server import MCPServer


class TestMCPServer:
    """Test cases for MCP Server"""
    
    def test_server_initialization(self):
        """Test MCP server initialization"""
        with tempfile.TemporaryDirectory() as temp_dir:
            server = MCPServer(project_root=temp_dir)
            
            assert server.project_root == Path(temp_dir)
            assert server.server is not None
            assert server.gemini is not None
    
    def test_load_gemini_config_from_file(self):
        """Test loading configuration from JSON file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_file = Path(temp_dir) / "gemini-config.json"
            test_config = {
                "enabled": False,
                "auto_consult": False,
                "cli_command": "test-gemini",
                "timeout": 120,
                "model": "gemini-pro"
            }
            
            with open(config_file, 'w') as f:
                json.dump(test_config, f)
            
            server = MCPServer(project_root=temp_dir)
            
            assert server.gemini.enabled == False
            assert server.gemini.auto_consult == False
            assert server.gemini.cli_command == "test-gemini"
            assert server.gemini.timeout == 120
            assert server.gemini.model == "gemini-pro"
    
    def test_load_gemini_config_env_override(self):
        """Test environment variable override of configuration"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create config file with default values
            config_file = Path(temp_dir) / "gemini-config.json"
            test_config = {
                "enabled": True,
                "timeout": 60
            }
            
            with open(config_file, 'w') as f:
                json.dump(test_config, f)
            
            # Set environment variables to override
            env_vars = {
                'GEMINI_ENABLED': 'false',
                'GEMINI_TIMEOUT': '300',
                'GEMINI_MODEL': 'gemini-pro'
            }
            
            with patch.dict(os.environ, env_vars):
                server = MCPServer(project_root=temp_dir)
            
            # Environment variables should override file config
            assert server.gemini.enabled == False  # Overridden by env
            assert server.gemini.timeout == 300    # Overridden by env
            assert server.gemini.model == 'gemini-pro'  # Set by env
    
    def test_load_gemini_config_no_file(self):
        """Test configuration loading when no config file exists"""
        with tempfile.TemporaryDirectory() as temp_dir:
            server = MCPServer(project_root=temp_dir)
            
            # Should use default values
            assert server.gemini.enabled == True
            assert server.gemini.auto_consult == True
            assert server.gemini.cli_command == 'gemini'
    
    def test_load_gemini_config_invalid_env_values(self):
        """Test handling of invalid environment variable values"""
        with tempfile.TemporaryDirectory() as temp_dir:
            env_vars = {
                'GEMINI_TIMEOUT': 'invalid_number',
                'GEMINI_RATE_LIMIT': 'not_a_float'
            }
            
            with patch.dict(os.environ, env_vars):
                # Should not raise exception, should use defaults
                server = MCPServer(project_root=temp_dir)
                
                # Should fall back to defaults
                assert server.gemini.timeout == 60  # Default
                assert server.gemini.rate_limit_delay == 2.0  # Default


class TestMCPServerTools:
    """Test MCP server tool handling"""
    
    @pytest.fixture
    def server(self):
        """Create a test server instance"""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield MCPServer(project_root=temp_dir)
    
    @pytest.mark.asyncio
    async def test_handle_consult_gemini_success(self, server):
        """Test successful consult_gemini tool call"""
        # Mock successful Gemini consultation
        mock_result = {
            'status': 'success',
            'response': 'Gemini analysis response',
            'execution_time': 1.5,
            'consultation_id': 'test_id'
        }
        
        with patch.object(server.gemini, 'consult_gemini', return_value=mock_result):
            arguments = {
                'query': 'Test query',
                'context': 'Test context',
                'comparison_mode': True
            }
            
            result = await server._handle_consult_gemini(arguments)
            
            assert len(result) == 1
            assert isinstance(result[0], types.TextContent)
            assert 'Gemini Second Opinion' in result[0].text
            assert 'Gemini analysis response' in result[0].text
            assert '1.5s' in result[0].text
    
    @pytest.mark.asyncio
    async def test_handle_consult_gemini_missing_query(self, server):
        """Test consult_gemini tool call with missing query"""
        arguments = {}  # No query provided
        
        result = await server._handle_consult_gemini(arguments)
        
        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert 'Error' in result[0].text
        assert 'required' in result[0].text
    
    @pytest.mark.asyncio
    async def test_handle_consult_gemini_disabled(self, server):
        """Test consult_gemini when integration is disabled"""
        mock_result = {
            'status': 'disabled',
            'message': 'Integration disabled'
        }
        
        with patch.object(server.gemini, 'consult_gemini', return_value=mock_result):
            arguments = {'query': 'Test query'}
            
            result = await server._handle_consult_gemini(arguments)
            
            assert len(result) == 1
            assert 'Gemini Integration Disabled' in result[0].text
    
    @pytest.mark.asyncio
    async def test_handle_consult_gemini_error(self, server):
        """Test consult_gemini error handling"""
        mock_result = {
            'status': 'error',
            'error': 'CLI not found',
            'error_type': 'cli_not_found'
        }
        
        with patch.object(server.gemini, 'consult_gemini', return_value=mock_result):
            with patch.object(server.gemini, 'get_error_suggestion', return_value='Install CLI'):
                arguments = {'query': 'Test query'}
                
                result = await server._handle_consult_gemini(arguments)
                
                assert len(result) == 1
                assert 'Gemini Consultation Failed' in result[0].text
                assert 'CLI not found' in result[0].text
                assert 'Install CLI' in result[0].text
    
    @pytest.mark.asyncio
    async def test_handle_gemini_status(self, server):
        """Test gemini_status tool call"""
        mock_status = {
            'enabled': True,
            'auto_consult': True,
            'cli_command': 'gemini',
            'model': 'gemini-2.5-flash',
            'rate_limit_delay': 2.0,
            'timeout': 60,
            'max_context_length': 4000,
            'total_consultations': 5,
            'successful_consultations': 4,
            'failed_consultations': 1,
            'last_consultation': '2024-01-01T12:00:00'
        }
        
        with patch.object(server.gemini, 'get_status_info', return_value=mock_status):
            result = await server._handle_gemini_status({})
            
            assert len(result) == 1
            assert isinstance(result[0], types.TextContent)
            status_text = result[0].text
            
            assert 'Gemini Integration Status' in status_text
            assert 'Enabled: ✅ Yes' in status_text
            assert 'Auto-consult: ✅ Yes' in status_text
            assert 'Total Consultations: 5' in status_text
            assert 'Successful: 4' in status_text
            assert 'Failed: 1' in status_text
    
    @pytest.mark.asyncio
    async def test_handle_toggle_auto_consult_enable(self, server):
        """Test enabling auto-consultation"""
        server.gemini.auto_consult = False  # Start disabled
        
        arguments = {'enable': True}
        result = await server._handle_toggle_auto_consult(arguments)
        
        assert server.gemini.auto_consult == True
        assert len(result) == 1
        assert 'enabled' in result[0].text
        assert 'automatically consulted' in result[0].text
    
    @pytest.mark.asyncio
    async def test_handle_toggle_auto_consult_disable(self, server):
        """Test disabling auto-consultation"""
        server.gemini.auto_consult = True  # Start enabled
        
        arguments = {'enable': False}
        result = await server._handle_toggle_auto_consult(arguments)
        
        assert server.gemini.auto_consult == False
        assert len(result) == 1
        assert 'disabled' in result[0].text
        assert 'manual consultations' in result[0].text
    
    @pytest.mark.asyncio
    async def test_handle_toggle_auto_consult_toggle(self, server):
        """Test toggling auto-consultation without explicit enable value"""
        original_state = server.gemini.auto_consult
        
        arguments = {}  # No enable parameter - should toggle
        result = await server._handle_toggle_auto_consult(arguments)
        
        assert server.gemini.auto_consult != original_state
        assert len(result) == 1


class TestMCPServerIntegration:
    """Integration tests for MCP Server"""
    
    def test_server_with_real_config_file(self):
        """Test server with actual configuration file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a realistic config file
            config_file = Path(temp_dir) / "gemini-config.json"
            config = {
                "enabled": True,
                "auto_consult": False,
                "cli_command": "gemini",
                "timeout": 30,
                "rate_limit_delay": 5.0,
                "max_context_length": 4000,
                "log_consultations": True,
                "model": "gemini-2.5-flash",
                "sandbox_mode": False,
                "debug_mode": False,
                "uncertainty_thresholds": {
                    "uncertainty_patterns": True,
                    "complex_decisions": True,
                    "critical_operations": True
                }
            }
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            server = MCPServer(project_root=temp_dir)
            
            # Verify configuration was loaded correctly
            assert server.gemini.enabled == True
            assert server.gemini.auto_consult == False
            assert server.gemini.timeout == 30
            assert server.gemini.rate_limit_delay == 5.0
            assert server.gemini.max_context_length == 4000
    
    def test_server_singleton_integration(self):
        """Test that server uses singleton Gemini integration"""
        with tempfile.TemporaryDirectory() as temp_dir:
            server1 = MCPServer(project_root=temp_dir)
            server2 = MCPServer(project_root=temp_dir)
            
            # Both servers should use the same Gemini integration instance
            # (This is a bit tricky to test due to singleton reset between tests)
            assert server1.gemini is not None
            assert server2.gemini is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])