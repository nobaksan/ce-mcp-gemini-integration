#!/usr/bin/env python3
"""
Tests for GeminiIntegration class
"""
import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import time

from gemini_integration import GeminiIntegration, get_integration, UNCERTAINTY_PATTERNS


class TestGeminiIntegration:
    """Test cases for GeminiIntegration class"""
    
    def test_initialization_with_config(self):
        """Test GeminiIntegration initialization with custom config"""
        config = {
            'enabled': False,
            'auto_consult': False,
            'cli_command': 'custom-gemini',
            'timeout': 120,
            'rate_limit_delay': 5.0,
            'model': 'gemini-pro'
        }
        
        integration = GeminiIntegration(config)
        
        assert integration.enabled == False
        assert integration.auto_consult == False
        assert integration.cli_command == 'custom-gemini'
        assert integration.timeout == 120
        assert integration.rate_limit_delay == 5.0
        assert integration.model == 'gemini-pro'
    
    def test_initialization_with_defaults(self):
        """Test GeminiIntegration initialization with default values"""
        integration = GeminiIntegration()
        
        assert integration.enabled == True
        assert integration.auto_consult == True
        assert integration.cli_command == 'gemini'
        assert integration.timeout == 60
        assert integration.rate_limit_delay == 2.0
        assert integration.model == 'gemini-2.5-flash'
    
    def test_detect_uncertainty_patterns(self):
        """Test uncertainty pattern detection"""
        integration = GeminiIntegration()
        
        # Test cases with expected results
        test_cases = [
            ("I'm not sure about this approach", True),
            ("I think this might work", True),
            ("This is definitely the right way", False),
            ("There are multiple approaches to consider", True),
            ("Security is critical here", True),
            ("This is a simple task", False),
            ("Maybe we should try a different approach", True),
            ("The production deployment requires careful consideration", True)
        ]
        
        for text, expected in test_cases:
            has_uncertainty, patterns = integration.detect_uncertainty(text)
            assert has_uncertainty == expected, f"Failed for text: '{text}'"
            if expected:
                assert len(patterns) > 0, f"Expected patterns for: '{text}'"
    
    def test_detect_uncertainty_case_insensitive(self):
        """Test that pattern detection is case insensitive"""
        integration = GeminiIntegration()
        
        test_cases = [
            "I'M NOT SURE",
            "i think so",
            "MULTIPLE APPROACHES",
            "security"
        ]
        
        for text in test_cases:
            has_uncertainty, patterns = integration.detect_uncertainty(text)
            assert has_uncertainty == True, f"Case insensitive detection failed for: '{text}'"
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self):
        """Test rate limiting functionality"""
        config = {'rate_limit_delay': 0.1}  # Short delay for testing
        integration = GeminiIntegration(config)
        
        # First call should not be delayed
        start_time = time.time()
        await integration._enforce_rate_limit()
        first_call_time = time.time() - start_time
        
        # Second call should be delayed
        start_time = time.time()
        await integration._enforce_rate_limit()
        second_call_time = time.time() - start_time
        
        assert first_call_time < 0.05  # First call should be immediate
        assert second_call_time >= 0.1  # Second call should be delayed
    
    def test_log_consultation(self):
        """Test consultation logging"""
        integration = GeminiIntegration()
        
        # Test logging enabled
        integration._log_consultation("test_id", "test query", "success", 1.5)
        
        assert len(integration.consultation_log) == 1
        log_entry = integration.consultation_log[0]
        assert log_entry['id'] == "test_id"
        assert log_entry['query'] == "test query"
        assert log_entry['status'] == "success"
        assert log_entry['execution_time'] == 1.5
        assert 'timestamp' in log_entry
    
    def test_log_consultation_truncation(self):
        """Test that long queries are truncated in logs"""
        integration = GeminiIntegration()
        
        long_query = "x" * 300  # Query longer than 200 chars
        integration._log_consultation("test_id", long_query, "success", 1.0)
        
        log_entry = integration.consultation_log[0]
        assert len(log_entry['query']) <= 203  # 200 chars + "..."
        assert log_entry['query'].endswith("...")
    
    def test_prepare_query_basic(self):
        """Test basic query preparation"""
        integration = GeminiIntegration()
        
        query = "What is the best approach?"
        context = "Building a web application"
        
        result = integration._prepare_query(query, context, comparison_mode=True)
        
        assert "Please provide a technical analysis" in result
        assert "Context:" in result
        assert "Building a web application" in result
        assert "Question/Topic:" in result
        assert "What is the best approach?" in result
        assert "Please structure your response with:" in result
    
    def test_prepare_query_no_comparison_mode(self):
        """Test query preparation without comparison mode"""
        integration = GeminiIntegration()
        
        query = "Simple question"
        context = ""
        
        result = integration._prepare_query(query, context, comparison_mode=False)
        
        assert "Please provide a technical analysis" not in result
        assert "Please structure your response with:" not in result
        assert "Simple question" in result
    
    def test_prepare_query_context_truncation(self):
        """Test context truncation in query preparation"""
        config = {'max_context_length': 100}
        integration = GeminiIntegration(config)
        
        query = "Test query"
        long_context = "x" * 200  # Longer than max_context_length
        
        result = integration._prepare_query(query, long_context, comparison_mode=False)
        
        assert "[Context truncated...]" in result
        # Context should be truncated but query should remain
        assert "Test query" in result
    
    def test_get_error_suggestion(self):
        """Test error suggestion generation"""
        integration = GeminiIntegration()
        
        suggestions = {
            "authentication": integration.get_error_suggestion("authentication"),
            "timeout": integration.get_error_suggestion("timeout"),
            "cli_not_found": integration.get_error_suggestion("cli_not_found"),
            "rate_limit": integration.get_error_suggestion("rate_limit"),
            "unknown": integration.get_error_suggestion("unknown_error")
        }
        
        # All suggestions should be non-empty strings
        for error_type, suggestion in suggestions.items():
            assert isinstance(suggestion, str)
            assert len(suggestion) > 0
        
        # Specific checks
        assert "authentication" in suggestions["authentication"].lower()
        assert "timeout" in suggestions["timeout"].lower()
        assert "install" in suggestions["cli_not_found"].lower()
        assert "rate limit" in suggestions["rate_limit"].lower()
    
    def test_get_status_info(self):
        """Test status information generation"""
        integration = GeminiIntegration()
        
        # Add some test consultation logs
        integration._log_consultation("test1", "query1", "success", 1.0)
        integration._log_consultation("test2", "query2", "error", 0.0)
        
        status = integration.get_status_info()
        
        required_fields = [
            'enabled', 'auto_consult', 'cli_command', 'model', 'timeout',
            'rate_limit_delay', 'max_context_length', 'total_consultations',
            'successful_consultations', 'failed_consultations'
        ]
        
        for field in required_fields:
            assert field in status
        
        assert status['total_consultations'] == 2
        assert status['successful_consultations'] == 1
        assert status['failed_consultations'] == 1
        assert status['last_consultation'] is not None


class TestSingletonPattern:
    """Test singleton pattern implementation"""
    
    def test_singleton_returns_same_instance(self):
        """Test that get_integration returns the same instance"""
        # Clear any existing singleton
        import gemini_integration
        gemini_integration._integration = None
        
        instance1 = get_integration()
        instance2 = get_integration()
        
        assert instance1 is instance2
    
    def test_singleton_config_only_used_on_first_call(self):
        """Test that config is only used on first call to get_integration"""
        # Clear any existing singleton
        import gemini_integration
        gemini_integration._integration = None
        
        config1 = {'enabled': False, 'timeout': 100}
        config2 = {'enabled': True, 'timeout': 200}
        
        instance1 = get_integration(config1)
        instance2 = get_integration(config2)
        
        assert instance1 is instance2
        assert instance1.enabled == False  # Should use config1
        assert instance1.timeout == 100    # Should use config1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])