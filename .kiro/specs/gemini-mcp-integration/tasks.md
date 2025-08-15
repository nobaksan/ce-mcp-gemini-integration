전체 # Implementation Plan

- [x] 1. 프로젝트 구조 및 기본 설정 파일 생성


  - 프로젝트 디렉토리 구조 생성
  - 기본 설정 파일들 (gemini-config.json, requirements.txt) 작성
  - 환경 변수 및 설정 로딩 테스트를 위한 기본 구조 구현
  - _Requirements: 6.1, 6.2, 6.3_

- [x] 2. 핵심 Gemini Integration 모듈 구현

  - [x] 2.1 GeminiIntegration 클래스 기본 구조 및 싱글톤 패턴 구현


    - GeminiIntegration 클래스의 기본 구조와 초기화 메서드 작성
    - 싱글톤 패턴을 위한 get_integration() 함수 구현
    - 설정 로딩 및 기본 속성 초기화 코드 작성
    - _Requirements: 5.1, 5.2, 6.1, 6.3_

  - [x] 2.2 불확실성 패턴 감지 시스템 구현


    - 불확실성, 복잡한 결정, 중요한 작업을 위한 정규식 패턴 정의
    - detect_uncertainty() 메서드 구현
    - 패턴 매칭 로직과 결과 반환 구조 작성
    - _Requirements: 1.1, 1.2, 1.3_

  - [x] 2.3 속도 제한 및 상태 관리 구현


    - _enforce_rate_limit() 비동기 메서드 구현
    - 마지막 호출 시간 추적 및 지연 로직 구현
    - 상담 로그 관리 시스템 구현
    - _Requirements: 4.1, 5.3, 8.1, 8.2_

- [x] 3. Gemini CLI 통합 및 쿼리 처리 구현

  - [x] 3.1 Gemini CLI 명령어 실행 시스템 구현


    - _execute_gemini_cli() 비동기 메서드 구현
    - subprocess를 사용한 Gemini CLI 호출 로직 작성
    - 타임아웃 및 기본 오류 처리 구현
    - _Requirements: 4.2, 4.3, 7.1_

  - [x] 3.2 쿼리 준비 및 컨텍스트 처리 구현


    - _prepare_query() 메서드로 쿼리와 컨텍스트 결합 로직 구현
    - 컨텍스트 길이 제한 및 잘림 처리 구현
    - 비교 모드를 위한 구조화된 쿼리 형식 구현
    - _Requirements: 2.3, 2.2_

  - [x] 3.3 메인 상담 메서드 및 응답 처리 구현


    - consult_gemini() 메서드의 전체 플로우 구현
    - 성공/실패 응답 형식 표준화 및 메타데이터 포함
    - 실행 시간 측정 및 상담 ID 생성 로직 구현
    - _Requirements: 2.1, 2.2, 8.1_

- [x] 4. 포괄적인 오류 처리 시스템 구현


  - 인증 오류, 타임아웃, CLI 미설치 등 각 오류 유형별 처리 로직 구현
  - 사용자 친화적인 오류 메시지 및 해결 방법 제안 시스템 구현
  - 오류 응답 형식 표준화 및 오류 타입 분류 시스템 구현
  - _Requirements: 4.2, 4.3, 4.4, 7.2, 7.3_

- [x] 5. MCP Server 기본 구조 및 설정 시스템 구현

  - [x] 5.1 MCPServer 클래스 및 초기화 구현


    - MCPServer 클래스 기본 구조 및 생성자 구현
    - 프로젝트 루트 설정 및 MCP 서버 초기화 코드 작성
    - Gemini Integration 싱글톤 인스턴스 연결 구현
    - _Requirements: 5.1, 6.1_

  - [x] 5.2 설정 로딩 및 환경 변수 처리 구현


    - _load_gemini_config() 메서드로 JSON 설정 파일 로딩 구현
    - 환경 변수 오버라이드 로직 및 타입 변환 구현
    - 설정 검증 및 기본값 적용 시스템 구현
    - _Requirements: 6.1, 6.2, 6.3_

- [x] 6. MCP 도구 등록 및 핸들러 구현

  - [x] 6.1 MCP 도구 정의 및 등록 시스템 구현


    - handle_list_tools() 함수로 3개 도구 스키마 정의 및 등록
    - 각 도구의 입력 스키마 및 설명 작성
    - 도구 호출 라우팅을 위한 handle_call_tool() 함수 구현
    - _Requirements: 2.1, 3.1, 3.2_

  - [x] 6.2 consult_gemini 도구 핸들러 구현


    - _handle_consult_gemini() 메서드 구현
    - 입력 검증 및 Gemini Integration 호출 로직 작성
    - 성공/실패 응답을 MCP TextContent 형식으로 변환하는 코드 구현
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 6.3 상태 관리 도구 핸들러들 구현


    - _handle_gemini_status() 메서드로 통합 상태 및 통계 표시 구현
    - _handle_toggle_auto_consult() 메서드로 자동 상담 토글 기능 구현
    - 상태 정보를 사용자 친화적 형식으로 포맷팅하는 코드 작성
    - _Requirements: 3.1, 3.2, 3.3_

- [x] 7. 서버 실행 및 CLI 인터페이스 구현


  - MCP 서버 실행을 위한 run() 메서드 구현
  - 명령행 인자 처리를 위한 argparse 설정 구현
  - main() 함수 및 서버 시작 로직 구현
  - _Requirements: 7.1_

- [x] 8. 단위 테스트 구현


  - [x] 8.1 GeminiIntegration 클래스 테스트 작성


    - 패턴 감지 정확성을 검증하는 테스트 케이스 작성
    - 속도 제한 동작을 검증하는 비동기 테스트 작성
    - 설정 로딩 및 싱글톤 패턴 동작 테스트 작성
    - _Requirements: 1.1, 1.2, 1.3, 4.1, 5.1, 5.2_

  - [x] 8.2 Gemini CLI 통합 테스트 작성


    - subprocess 모킹을 사용한 CLI 호출 테스트 작성
    - 다양한 오류 시나리오 (타임아웃, 인증 실패 등) 테스트 작성
    - 쿼리 준비 및 응답 처리 로직 테스트 작성
    - _Requirements: 4.2, 4.3, 4.4, 7.2, 7.3_

- [x] 9. MCP Server 통합 테스트 작성


  - MCP 도구 등록 및 호출 플로우 테스트 작성
  - 설정 로딩 및 환경 변수 오버라이드 테스트 작성
  - 전체 시스템 통합 테스트 및 엔드투엔드 시나리오 테스트 작성
  - _Requirements: 2.1, 2.2, 3.1, 3.2, 6.1, 6.2, 6.3_

- [x] 10. 설치 및 설정 스크립트 구현


  - Gemini CLI 설치 확인 및 Node.js 버전 체크 스크립트 작성
  - 기본 설정 파일 생성 및 MCP 설정 템플릿 생성 스크립트 작성
  - 사용자 가이드 및 문제 해결 문서 작성
  - _Requirements: 7.1, 7.2, 7.3_