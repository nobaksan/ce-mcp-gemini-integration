#!/usr/bin/env python3
"""
Gemini CLI Integration Module
Provides automatic consultation with Gemini for second opinions and validation
"""
import asyncio
import json
import logging
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Uncertainty patterns that trigger automatic Gemini consultation
UNCERTAINTY_PATTERNS = [
    # English patterns
    r"\bI'm not sure\b",
    r"\bI think\b",
    r"\bpossibly\b",
    r"\bprobably\b",
    r"\bmight be\b",
    r"\bcould be\b",
    r"\bI believe\b",
    r"\bIt seems\b",
    r"\bappears to be\b",
    r"\buncertain\b",
    r"\bI would guess\b",
    r"\blikely\b",
    r"\bperhaps\b",
    r"\bmaybe\b",
    r"\bI assume\b",
    # Korean patterns
    r"잘 모르겠",
    r"확실하지 않",
    r"확신이 없",
    r"아마도",
    r"어쩌면",
    r"생각해보니",
    r"것 같",
    r"인 듯",
    r"추측",
    r"예상",
    # Error/Problem patterns (Korean)
    r"에러",
    r"오류",
    r"문제",
    r"버그",
    r"안 돼",
    r"안돼",
    r"실패",
    r"작동하지 않",
    r"작동 안",
    r"동작하지 않",
    r"동작 안",
    r"안 되",
    r"막혔",
    r"해결",
    r"고장",
    r"이상해",
    r"이상하",
    # Error/Problem patterns (English)
    r"\berror\b",
    r"\bbug\b",
    r"\bissue\b",
    r"\bproblem\b",
    r"\bfailed\b",
    r"\bfailing\b",
    r"\bnot working\b",
    r"\bdoesn't work\b",
    r"\bbroken\b",
    r"\bstuck\b",
    r"\btrouble\b",
    r"\bwrong\b"
]

# Complex decision patterns that benefit from second opinions
COMPLEX_DECISION_PATTERNS = [
    # English patterns
    r"\bmultiple approaches\b",
    r"\bseveral options\b",
    r"\btrade-offs?\b",
    r"\bconsider(?:ing)?\b",
    r"\balternatives?\b",
    r"\bpros and cons\b",
    r"\bweigh(?:ing)? the options\b",
    r"\bchoice between\b",
    r"\bdecision\b",
    # Korean patterns
    r"어떤 게 좋",
    r"뭐가 나은",
    r"어느 것",
    r"선택",
    r"결정",
    r"고민",
    r"여러 방법",
    r"여러 가지",
    r"장단점",
    r"비교",
    r"vs",
    r"대",
    r"중에",
    # Help/Assistance patterns (Korean)
    r"도와줘",
    r"도움",
    r"해줘",
    r"알려줘",
    r"가르쳐",
    r"설명해",
    r"방법",
    r"어떻게",
    r"왜",
    r"뭔가",
    # Help/Assistance patterns (English)
    r"\bhelp\b",
    r"\bassist\b",
    r"\bguide\b",
    r"\bshow me\b",
    r"\btell me\b",
    r"\bexplain\b",
    r"\bhow to\b",
    r"\bwhat should\b",
    r"\bwhy\b"
]

# Critical operations that should trigger consultation
CRITICAL_OPERATION_PATTERNS = [
    r"\bproduction\b",
    r"\bdatabase migration\b",
    r"\bsecurity\b",
    r"\bauthentication\b",
    r"\bencryption\b",
    r"\bAPI key\b",
    r"\bcredentials?\b",
    r"\bperformance\s+critical\b"
]


class GeminiIntegration:
    """Handles Gemini CLI integration for second opinions and validation"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)
        self.auto_consult = self.config.get('auto_consult', True)
        self.cli_command = self.config.get('cli_command', 'gemini')
        self.timeout = self.config.get('timeout', 60)
        self.rate_limit_delay = self.config.get('rate_limit_delay', 2.0)
        self.last_consultation = 0
        self.consultation_log = []
        self.max_context_length = self.config.get('max_context_length', 4000)
        self.model = self.config.get('model', 'gemini-2.5-flash')
        
        logger.info(f"GeminiIntegration initialized - enabled: {self.enabled}, auto_consult: {self.auto_consult}")
    
    def detect_uncertainty(self, text: str) -> Tuple[bool, List[str]]:
        """Detect if text contains uncertainty patterns"""
        found_patterns = []
        
        # Check uncertainty patterns
        for pattern in UNCERTAINTY_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                found_patterns.append(f"uncertainty: {pattern}")
        
        # Check complex decision patterns
        for pattern in COMPLEX_DECISION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                found_patterns.append(f"complex_decision: {pattern}")
        
        # Check critical operation patterns
        for pattern in CRITICAL_OPERATION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                found_patterns.append(f"critical_operation: {pattern}")
        
        has_uncertainty = len(found_patterns) > 0
        
        if has_uncertainty:
            logger.debug(f"Uncertainty detected in text: {found_patterns}")
        
        return has_uncertainty, found_patterns
    
    async def _enforce_rate_limit(self):
        """Enforce rate limiting between consultations"""
        current_time = time.time()
        time_since_last = current_time - self.last_consultation
        
        if time_since_last < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            await asyncio.sleep(sleep_time)
        
        self.last_consultation = time.time()
    
    def _log_consultation(self, consultation_id: str, query: str, status: str, execution_time: float):
        """Log consultation for debugging and statistics"""
        if not self.config.get('log_consultations', True):
            return
        
        log_entry = {
            'id': consultation_id,
            'timestamp': datetime.now().isoformat(),
            'query': query[:200] + "..." if len(query) > 200 else query,
            'status': status,
            'execution_time': execution_time
        }
        
        self.consultation_log.append(log_entry)
        
        # Keep only last 100 entries to prevent memory issues
        if len(self.consultation_log) > 100:
            self.consultation_log = self.consultation_log[-100:]
        
        logger.info(f"Consultation logged: {consultation_id} - {status} in {execution_time:.2f}s")
    
    async def _execute_gemini_cli(self, query: str) -> Dict[str, Any]:
        """Execute Gemini CLI command and return results"""
        start_time = time.time()
        
        # Build command
        cmd = [self.cli_command]
        if self.model:
            cmd.extend(['-m', self.model])
        cmd.extend(['-p', query])  # Non-interactive mode
        
        logger.debug(f"Executing Gemini CLI: {' '.join(cmd[:3])}...")  # Don't log full query for privacy
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.timeout
            )
            
            execution_time = time.time() - start_time
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                
                # Provide helpful error messages
                if "authentication" in error_msg.lower():
                    error_msg += "\nTip: Run 'gemini' interactively to authenticate with your Google account"
                elif "command not found" in error_msg.lower() or "not recognized" in error_msg.lower():
                    error_msg += "\nTip: Install Gemini CLI with 'npm install -g @google/gemini-cli'"
                
                raise Exception(f"Gemini CLI failed (exit code {process.returncode}): {error_msg}")
            
            output = stdout.decode().strip()
            logger.debug(f"Gemini CLI completed successfully in {execution_time:.2f}s")
            
            return {
                'output': output,
                'execution_time': execution_time
            }
            
        except asyncio.TimeoutError:
            logger.error(f"Gemini CLI timed out after {self.timeout} seconds")
            raise Exception(f"Gemini CLI timed out after {self.timeout} seconds")
        except FileNotFoundError:
            logger.error(f"Gemini CLI command '{self.cli_command}' not found")
            raise Exception(f"Gemini CLI command '{self.cli_command}' not found. Please install with 'npm install -g @google/gemini-cli'")
        except Exception as e:
            logger.error(f"Error executing Gemini CLI: {str(e)}")
            raise
    
    def _prepare_query(self, query: str, context: str, comparison_mode: bool) -> str:
        """Prepare the full query for Gemini CLI"""
        # Truncate context if too long
        if len(context) > self.max_context_length:
            context = context[:self.max_context_length] + "\n[Context truncated...]"
            logger.debug(f"Context truncated to {self.max_context_length} characters")
        
        parts = []
        
        if comparison_mode:
            parts.append("Please provide a technical analysis and second opinion:")
            parts.append("")
        
        if context:
            parts.append("Context:")
            parts.append(context)
            parts.append("")
        
        parts.append("Question/Topic:")
        parts.append(query)
        
        if comparison_mode:
            parts.extend([
                "",
                "Please structure your response with:",
                "1. Your analysis and understanding",
                "2. Recommendations or approach", 
                "3. Any concerns or considerations",
                "4. Alternative approaches (if applicable)"
            ])
        
        full_query = "\n".join(parts)
        logger.debug(f"Prepared query with {len(full_query)} characters")
        
        return full_query
    
    async def consult_gemini(self, query: str, context: str = "", comparison_mode: bool = True, force_consult: bool = False) -> Dict[str, Any]:
        """Consult Gemini CLI for second opinion"""
        if not self.enabled:
            logger.warning("Gemini integration is disabled")
            return {
                'status': 'disabled', 
                'message': 'Gemini integration is disabled'
            }
        
        if not force_consult:
            await self._enforce_rate_limit()
        
        consultation_id = f"consult_{int(time.time())}"
        logger.info(f"Starting Gemini consultation: {consultation_id}")
        
        try:
            # Prepare query with context
            full_query = self._prepare_query(query, context, comparison_mode)
            
            # Execute Gemini CLI command
            result = await self._execute_gemini_cli(full_query)
            
            # Log successful consultation
            self._log_consultation(
                consultation_id, 
                query, 
                'success', 
                result.get('execution_time', 0)
            )
            
            return {
                'status': 'success',
                'response': result['output'],
                'execution_time': result['execution_time'],
                'consultation_id': consultation_id,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error consulting Gemini: {error_msg}")
            
            # Log failed consultation
            self._log_consultation(consultation_id, query, 'error', 0)
            
            # Determine error type for better user guidance
            error_type = "unknown"
            if "authentication" in error_msg.lower():
                error_type = "authentication"
            elif "timeout" in error_msg.lower():
                error_type = "timeout"
            elif "not found" in error_msg.lower():
                error_type = "cli_not_found"
            elif "rate limit" in error_msg.lower():
                error_type = "rate_limit"
            
            return {
                'status': 'error',
                'error': error_msg,
                'error_type': error_type,
                'consultation_id': consultation_id,
                'timestamp': datetime.now().isoformat()
            }
    
    def get_error_suggestion(self, error_type: str) -> str:
        """Get user-friendly error suggestions based on error type"""
        suggestions = {
            "authentication": (
                "Authentication required. Please run 'gemini' command interactively "
                "to authenticate with your Google account."
            ),
            "timeout": (
                f"Request timed out after {self.timeout} seconds. "
                "Try increasing GEMINI_TIMEOUT environment variable or check your network connection."
            ),
            "cli_not_found": (
                "Gemini CLI not found. Please install it with: "
                "'npm install -g @google/gemini-cli'"
            ),
            "rate_limit": (
                "Rate limit exceeded. Please wait before making another request. "
                f"Current rate limit: {self.rate_limit_delay} seconds between calls."
            )
        }
        
        return suggestions.get(error_type, "Please check the error message and try again.")
    
    def get_status_info(self) -> Dict[str, Any]:
        """Get comprehensive status information"""
        return {
            "enabled": self.enabled,
            "auto_consult": self.auto_consult,
            "cli_command": self.cli_command,
            "model": self.model,
            "timeout": self.timeout,
            "rate_limit_delay": self.rate_limit_delay,
            "max_context_length": self.max_context_length,
            "total_consultations": len(self.consultation_log),
            "last_consultation": (
                self.consultation_log[-1]['timestamp'] 
                if self.consultation_log else None
            ),
            "successful_consultations": len([
                log for log in self.consultation_log 
                if log['status'] == 'success'
            ]),
            "failed_consultations": len([
                log for log in self.consultation_log 
                if log['status'] == 'error'
            ])
        }


# Singleton pattern implementation
_integration = None


def get_integration(config: Optional[Dict[str, Any]] = None) -> GeminiIntegration:
    """
    Get or create the global Gemini integration instance.
    
    This ensures that all parts of the application share the same instance,
    maintaining consistent state for rate limiting, consultation history,
    and configuration across all tool calls.
    
    Args:
        config: Optional configuration dict. Only used on first call.
    
    Returns:
        The singleton GeminiIntegration instance
    """
    global _integration
    if _integration is None:
        _integration = GeminiIntegration(config)
        logger.info("Created new GeminiIntegration singleton instance")
    return _integration