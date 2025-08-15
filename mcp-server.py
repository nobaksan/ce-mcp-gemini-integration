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
                ),
                types.Tool(
                    name="enhance_request",
                    description="사용자 요청을 Gemini로 분석하고 구체적인 요구사항으로 개선",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_request": {
                                "type": "string",
                                "description": "사용자의 간단한 요청 (예: '내 앱에 구글 로그인 기능 붙이고 싶어')"
                            },
                            "project_context": {
                                "type": "string",
                                "description": "프로젝트 컨텍스트 (기술 스택, 현재 상태 등)"
                            }
                        },
                        "required": ["user_request"]
                    }
                ),
                types.Tool(
                    name="smart_code_generation",
                    description="개선된 요청으로 단계별 코드 생성 가이드 제공",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "enhanced_request": {
                                "type": "string",
                                "description": "enhance_request로 개선된 상세 요구사항"
                            },
                            "tech_stack": {
                                "type": "string",
                                "description": "사용할 기술 스택 (예: React, Node.js, Python Django 등)"
                            },
                            "complexity_level": {
                                "type": "string",
                                "description": "구현 복잡도 (basic, intermediate, advanced)",
                                "default": "intermediate"
                            }
                        },
                        "required": ["enhanced_request"]
                    }
                ),
                types.Tool(
                    name="enhance_user_request",
                    description="사용자 요청을 한 번에 분석하고 실행 가능한 개발 계획으로 변환",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_request": {
                                "type": "string",
                                "description": "사용자의 간단한 개발 요청"
                            },
                            "project_info": {
                                "type": "string",
                                "description": "프로젝트 정보 (기술 스택, 현재 상태, 제약사항 등)"
                            },
                            "output_format": {
                                "type": "string",
                                "description": "출력 형식 (detailed_plan, quick_guide, step_by_step)",
                                "default": "detailed_plan"
                            }
                        },
                        "required": ["user_request"]
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
            elif name == "enhance_request":
                return await self._handle_enhance_request(arguments)
            elif name == "smart_code_generation":
                return await self._handle_smart_code_generation(arguments)
            elif name == "enhance_user_request":
                return await self._handle_enhance_user_request(arguments)
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

    async def _handle_enhance_request(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """사용자 요청을 Gemini로 분석하고 구체적인 요구사항으로 개선"""
        user_request = arguments.get('user_request', '')
        project_context = arguments.get('project_context', '')
        
        if not user_request:
            return [types.TextContent(
                type="text",
                text="❌ Error: 'user_request' parameter is required"
            )]
        
        # Gemini에게 요청 개선을 위한 프롬프트 구성
        enhancement_prompt = f"""
사용자의 간단한 개발 요청을 분석하고 구체적이고 실행 가능한 요구사항으로 확장해주세요.

사용자 요청: "{user_request}"
프로젝트 컨텍스트: {project_context if project_context else "정보 없음"}

다음 형식으로 응답해주세요:

📋 **구체적 요구사항:**
- 핵심 기능들을 명확히 나열
- 기술적 세부사항 포함
- 보안 및 에러 처리 고려

🔧 **기술 스택 고려사항:**
- 권장 라이브러리/프레임워크
- 설정 및 환경 요구사항

📝 **구현 순서:**
1. 단계별 구현 계획
2. 우선순위가 높은 순서로 정렬

⚠️ **주의사항:**
- 보안 고려사항
- 성능 최적화 포인트
- 잠재적 문제점

한국어로 개발자가 바로 실행할 수 있도록 구체적이고 명확하게 작성해주세요.
        """
        
        print(f"Processing request enhancement: {user_request[:50]}...")
        
        result = await self.gemini.consult_gemini(
            query=enhancement_prompt,
            context="요청 개선 및 구체화",
            comparison_mode=False
        )
        
        if result['status'] == 'success':
            response_text = f"🚀 **요청 개선 완료**\n\n"
            response_text += f"**원본 요청:** {user_request}\n\n"
            response_text += f"**개선된 요구사항:**\n{result['response']}\n\n"
            response_text += f"⏱️ *분석 완료 시간: {result['execution_time']:.2f}s*"
        else:
            response_text = f"❌ **요청 개선 실패**\n\n{result.get('error', 'Unknown error')}"
        
        return [types.TextContent(type="text", text=response_text)]

    async def _handle_smart_code_generation(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """개선된 요청으로 단계별 코드 생성 가이드 제공"""
        enhanced_request = arguments.get('enhanced_request', '')
        tech_stack = arguments.get('tech_stack', '')
        complexity_level = arguments.get('complexity_level', 'intermediate')
        
        if not enhanced_request:
            return [types.TextContent(
                type="text",
                text="❌ Error: 'enhanced_request' parameter is required"
            )]
        
        # 코드 생성 가이드를 위한 프롬프트
        code_guide_prompt = f"""
다음 개선된 요구사항을 바탕으로 단계별 코드 생성 가이드를 제공해주세요.

개선된 요구사항:
{enhanced_request}

기술 스택: {tech_stack if tech_stack else "범용적으로 적용 가능한 방식"}
복잡도 레벨: {complexity_level}

다음 형식으로 응답해주세요:

🏗️ **프로젝트 구조:**
```
폴더/파일 구조 예시
```

📦 **필요한 의존성:**
- 설치해야 할 패키지들
- 설정 파일들

💻 **핵심 코드 스니펫:**
각 주요 기능별로 핵심 코드 예시 제공

🔧 **설정 및 환경:**
- 환경변수 설정
- 초기 설정 방법

🧪 **테스트 방법:**
- 기능 테스트 방법
- 디버깅 팁

📚 **추가 리소스:**
- 참고 문서
- 유용한 튜토리얼

한국어로 개발자가 바로 따라할 수 있도록 구체적인 코드와 명령어를 포함해서 작성해주세요.
        """
        
        print(f"Generating code guide for complexity level: {complexity_level}")
        
        result = await self.gemini.consult_gemini(
            query=code_guide_prompt,
            context="코드 생성 가이드",
            comparison_mode=False
        )
        
        if result['status'] == 'success':
            response_text = f"💻 **스마트 코드 생성 가이드**\n\n"
            response_text += f"**기술 스택:** {tech_stack if tech_stack else '범용'}\n"
            response_text += f"**복잡도:** {complexity_level}\n\n"
            response_text += result['response']
            response_text += f"\n\n⏱️ *가이드 생성 시간: {result['execution_time']:.2f}s*"
        else:
            response_text = f"❌ **코드 가이드 생성 실패**\n\n{result.get('error', 'Unknown error')}"
        
        return [types.TextContent(type="text", text=response_text)]

    async def _handle_enhance_user_request(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """사용자 요청을 한 번에 분석하고 실행 가능한 개발 계획으로 변환"""
        user_request = arguments.get('user_request', '')
        project_info = arguments.get('project_info', '')
        output_format = arguments.get('output_format', 'detailed_plan')
        
        if not user_request:
            return [types.TextContent(
                type="text",
                text="❌ Error: 'user_request' parameter is required"
            )]
        
        # 출력 형식에 따른 프롬프트 조정
        format_instructions = {
            'detailed_plan': "상세한 개발 계획과 단계별 구현 가이드를 제공",
            'quick_guide': "빠른 구현을 위한 핵심 포인트만 간단히 제공",
            'step_by_step': "단계별로 따라할 수 있는 실행 가이드 제공"
        }
        
        comprehensive_prompt = f"""
사용자의 개발 요청을 종합적으로 분석하고 바로 실행 가능한 개발 계획으로 변환해주세요.

사용자 요청: "{user_request}"
프로젝트 정보: {project_info if project_info else "정보 없음"}
출력 형식: {format_instructions.get(output_format, format_instructions['detailed_plan'])}

다음 구조로 응답해주세요:

🎯 **요청 분석 및 목표:**
- 사용자가 원하는 핵심 기능
- 예상되는 기술적 요구사항

📋 **구체적 구현 계획:**
- 필요한 기능들을 세분화
- 우선순위별 정렬
- 각 기능의 기술적 세부사항

🛠️ **기술 스택 및 도구:**
- 권장 프레임워크/라이브러리
- 개발 도구 및 환경 설정

📝 **단계별 실행 가이드:**
1. 환경 설정 및 초기 설정
2. 핵심 기능 구현 순서
3. 테스트 및 배포 준비

💡 **핵심 코드 스니펫:**
- 주요 기능별 코드 예시
- 설정 파일 예시

⚠️ **주의사항 및 팁:**
- 보안 고려사항
- 성능 최적화
- 일반적인 실수 방지

🔗 **다음 단계:**
- 구현 후 확장 가능한 기능들
- 추가 학습 리소스

한국어로 개발자가 바로 시작할 수 있도록 실용적이고 구체적으로 작성해주세요.
        """
        
        print(f"Processing comprehensive request enhancement: {user_request[:50]}...")
        
        result = await self.gemini.consult_gemini(
            query=comprehensive_prompt,
            context="종합적 요청 분석 및 개발 계획",
            comparison_mode=False
        )
        
        if result['status'] == 'success':
            response_text = f"🚀 **종합 개발 계획 완료**\n\n"
            response_text += f"**원본 요청:** {user_request}\n"
            response_text += f"**출력 형식:** {output_format}\n\n"
            response_text += result['response']
            response_text += f"\n\n⏱️ *계획 수립 시간: {result['execution_time']:.2f}s*"
            response_text += f"\n💡 *이제 이 계획을 바탕으로 AI 코딩 도구에게 구체적인 구현을 요청하세요!*"
        else:
            response_text = f"❌ **개발 계획 수립 실패**\n\n{result.get('error', 'Unknown error')}"
        
        return [types.TextContent(type="text", text=response_text)]

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