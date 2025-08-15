#!/usr/bin/env python3
"""
Tests for Gemini CLI integration
"""
import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import subprocess

from gemini_integration import GeminiIntegration


class TestGeminiCLIIntegration:
    """Test cases for Gemini CLI integration"""
    
    @pytest.mark.asyncio
    async def test_execute_gemini_cli_success(self):
        """Test successful Gemini CLI execution"""
        integration = GeminiIntegration()
        
        # Mock successful subprocess execution
        mock_process = AsyncMock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = (b"Gemini response", b"")
        
        with patch('asyncio.create_subprocess_exec', return_value=mock_process):
            with patch('asyncio.wait_for', return_value=(b"Gemini response", b"")):
                result = await integration._execute_gemini_cli("test query")
        
        assert result['output'] == "Gemini response"
        assert 'execution_time' in result
        assert result['execution_time'] > 0
    
    @pytest.mark.asyncio
    async def test_execute_gemini_cli_command_not_found(self):
        """Test Gemini CLI command not found error"""
        integration = GeminiIntegration()
        
        with patch('asyncio.create_subprocess_exec', side_effect=FileNotFoundError()):
            with pytest.raises(Exception) as exc_info:
                await integration._execute_gemini_cli("test query")
            
            assert "not found" in str(exc_info.value)
            assert "npm install" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_execute_gemini_cli_authentication_error(self):
        """Test Gemini CLI authentication error"""
        integration = GeminiIntegration()
        
        mock_process = AsyncMock()
        mock_process.returncode = 1
        mock_process.communicate.return_value = (b"", b"authentication required")
        
        with patch('asyncio.create_subprocess_exec', return_value=mock_process):
            with patch('asyncio.wait_for', return_value=(b"", b"authentication required")):
                with pytest.raises(Exception) as exc_info:
                    await integration._execute_gemini_cli("test query")
                
                assert "authentication" in str(exc_info.value).lower()
                assert "interactively" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_execute_gemini_cli_timeout(self):
        """Test Gemini CLI timeout"""
        config = {'timeout': 0.1}  # Very short timeout for testing
        integration = GeminiIntegration(config)
        
        with patch('asyncio.create_subprocess_exec', return_value=AsyncMock()):
            with patch('asyncio.wait_for', side_effect=asyncio.TimeoutError()):
                with pytest.raises(Exception) as exc_info:
                    await integration._execute_gemini_cli("test query")
                
                assert "timed out" in str(exc_info.value)
                assert "0.1 seconds" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_execute_gemini_cli_with_model(self):
        """Test Gemini CLI execution with specific model"""
        config = {'model': 'gemini-pro'}
        integration = GeminiIntegration(config)
        
        mock_process = AsyncMock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = (b"response", b"")
        
        with patch('asyncio.create_subprocess_exec', return_value=mock_process) as mock_exec:
            with patch('asyncio.wait_for', return_value=(b"response", b"")):
                await integration._execute_gemini_cli("test query")
        
        # Verify that the model parameter was included in the command
        call_args = mock_exec.call_args[0]
        assert '-m' in call_args
        assert 'gemini-pro' in call_args
    
    @pytest.mark.asyncio
    async def test_consult_gemini_success(self):
        """Test successful Gemini consultation"""
        integration = GeminiIntegration()
        
        # Mock the CLI execution
        mock_cli_result = {
            'output': 'Gemini analysis response',
            'execution_time': 1.5
        }
        
        with patch.object(integration, '_execute_gemini_cli', return_value=mock_cli_result):
            with patch.object(integration, '_enforce_rate_limit'):
                result = await integration.consult_gemini("test query", "test context")
        
        assert result['status'] == 'success'
        assert result['response'] == 'Gemini analysis response'
        assert result['execution_time'] == 1.5
        assert 'consultation_id' in result
        assert 'timestamp' in result
    
    @pytest.mark.asyncio
    async def test_consult_gemini_disabled(self):
        """Test consultation when integration is disabled"""
        config = {'enabled': False}
        integration = GeminiIntegration(config)
        
        result = await integration.consult_gemini("test query")
        
        assert result['status'] == 'disabled'
        assert 'message' in result
    
    @pytest.mark.asyncio
    async def test_consult_gemini_error_handling(self):
        """Test error handling in consultation"""
        integration = GeminiIntegration()
        
        with patch.object(integration, '_execute_gemini_cli', side_effect=Exception("CLI error")):
            with patch.object(integration, '_enforce_rate_limit'):
                result = await integration.consult_gemini("test query")
        
        assert result['status'] == 'error'
        assert result['error'] == 'CLI error'
        assert 'consultation_id' in result
        assert 'timestamp' in result
    
    @pytest.mark.asyncio
    async def test_consult_gemini_force_consult_skips_rate_limit(self):
        """Test that force_consult skips rate limiting"""
        integration = GeminiIntegration()
        
        mock_cli_result = {
            'output': 'response',
            'execution_time': 1.0
        }
        
        with patch.object(integration, '_execute_gemini_cli', return_value=mock_cli_result):
            with patch.object(integration, '_enforce_rate_limit') as mock_rate_limit:
                await integration.consult_gemini("test query", force_consult=True)
        
        # Rate limiting should not be called when force_consult=True
        mock_rate_limit.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_consult_gemini_error_type_detection(self):
        """Test error type detection in consultation"""
        integration = GeminiIntegration()
        
        error_cases = [
            ("authentication failed", "authentication"),
            ("request timed out", "timeout"),
            ("command not found", "cli_not_found"),
            ("rate limit exceeded", "rate_limit"),
            ("unknown error", "unknown")
        ]
        
        for error_msg, expected_type in error_cases:
            with patch.object(integration, '_execute_gemini_cli', side_effect=Exception(error_msg)):
                with patch.object(integration, '_enforce_rate_limit'):
                    result = await integration.consult_gemini("test query")
            
            assert result['status'] == 'error'
            assert result['error_type'] == expected_type
    
    def test_prepare_query_with_context(self):
        """Test query preparation with context"""
        integration = GeminiIntegration()
        
        query = "How to implement authentication?"
        context = "Building a REST API with Node.js"
        
        result = integration._prepare_query(query, context, comparison_mode=True)
        
        # Check that all expected parts are included
        assert "Please provide a technical analysis" in result
        assert "Context:" in result
        assert "Building a REST API with Node.js" in result
        assert "Question/Topic:" in result
        assert "How to implement authentication?" in result
        assert "Please structure your response with:" in result
        assert "1. Your analysis and understanding" in result
    
    def test_prepare_query_without_context(self):
        """Test query preparation without context"""
        integration = GeminiIntegration()
        
        query = "Simple question"
        
        result = integration._prepare_query(query, "", comparison_mode=True)
        
        assert "Context:" not in result
        assert "Simple question" in result
        assert "Please provide a technical analysis" in result
    
    def test_prepare_query_non_comparison_mode(self):
        """Test query preparation in non-comparison mode"""
        integration = GeminiIntegration()
        
        query = "Direct question"
        context = "Some context"
        
        result = integration._prepare_query(query, context, comparison_mode=False)
        
        assert "Please provide a technical analysis" not in result
        assert "Please structure your response with:" not in result
        assert "Direct question" in result
        assert "Some context" in result


class TestGeminiCLICommand:
    """Test Gemini CLI command construction"""
    
    def test_command_construction_basic(self):
        """Test basic command construction"""
        integration = GeminiIntegration()
        
        # We can't easily test the actual command construction without mocking
        # the entire _execute_gemini_cli method, but we can test the config
        assert integration.cli_command == 'gemini'
        assert integration.model == 'gemini-2.5-flash'
    
    def test_command_construction_custom_config(self):
        """Test command construction with custom config"""
        config = {
            'cli_command': 'custom-gemini',
            'model': 'gemini-pro'
        }
        integration = GeminiIntegration(config)
        
        assert integration.cli_command == 'custom-gemini'
        assert integration.model == 'gemini-pro'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])