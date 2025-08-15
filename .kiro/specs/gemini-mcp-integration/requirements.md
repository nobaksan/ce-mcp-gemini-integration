# Requirements Document

## Introduction

이 프로젝트는 Google Gemini CLI와 Claude Code를 통합하는 MCP(Model Context Protocol) 서버를 구현합니다. 이 통합을 통해 Claude가 불확실성을 표현하거나 복잡한 기술적 결정에 직면했을 때 자동으로 Gemini에게 두 번째 의견을 요청할 수 있습니다. 또한 사용자가 수동으로 Gemini에게 상담을 요청할 수도 있습니다.

## Requirements

### Requirement 1

**User Story:** 개발자로서, Claude가 불확실한 답변을 할 때 자동으로 Gemini의 두 번째 의견을 받고 싶습니다.

#### Acceptance Criteria

1. WHEN Claude의 응답에 불확실성 패턴("I'm not sure", "I think", "possibly" 등)이 감지되면 THEN 시스템은 자동으로 Gemini에게 상담을 요청해야 합니다
2. WHEN 복잡한 결정 패턴("multiple approaches", "trade-offs", "alternatives" 등)이 감지되면 THEN 시스템은 자동으로 Gemini 상담을 트리거해야 합니다
3. WHEN 중요한 작업 패턴("production", "security", "database migration" 등)이 감지되면 THEN 시스템은 자동으로 Gemini 상담을 트리거해야 합니다
4. WHEN 자동 상담이 트리거되면 THEN 시스템은 Claude의 응답과 Gemini의 응답을 종합하여 제공해야 합니다

### Requirement 2

**User Story:** 개발자로서, 필요할 때 수동으로 Gemini에게 상담을 요청하고 싶습니다.

#### Acceptance Criteria

1. WHEN 사용자가 consult_gemini 도구를 호출하면 THEN 시스템은 지정된 쿼리와 컨텍스트로 Gemini에게 상담을 요청해야 합니다
2. WHEN Gemini 상담이 완료되면 THEN 시스템은 구조화된 응답(분석, 권장사항, 고려사항, 대안)을 제공해야 합니다
3. WHEN 상담 요청에 컨텍스트가 포함되면 THEN 시스템은 컨텍스트를 포함하여 Gemini에게 전달해야 합니다

### Requirement 3

**User Story:** 개발자로서, Gemini 통합의 상태를 확인하고 설정을 관리하고 싶습니다.

#### Acceptance Criteria

1. WHEN 사용자가 gemini_status 도구를 호출하면 THEN 시스템은 통합 상태, 설정, 통계를 표시해야 합니다
2. WHEN 사용자가 toggle_gemini_auto_consult 도구를 호출하면 THEN 시스템은 자동 상담 기능을 활성화/비활성화해야 합니다
3. WHEN 설정이 변경되면 THEN 시스템은 변경 사항을 즉시 적용해야 합니다

### Requirement 4

**User Story:** 시스템 관리자로서, Gemini API 호출에 대한 속도 제한과 오류 처리가 적절히 구현되기를 원합니다.

#### Acceptance Criteria

1. WHEN 연속적인 Gemini 호출이 발생하면 THEN 시스템은 설정된 속도 제한(기본 2초)을 준수해야 합니다
2. WHEN Gemini CLI 호출이 실패하면 THEN 시스템은 적절한 오류 메시지와 함께 정상적으로 실패해야 합니다
3. WHEN Gemini CLI 호출이 타임아웃되면 THEN 시스템은 설정된 타임아웃(기본 60초) 후 요청을 중단해야 합니다
4. WHEN 인증 오류가 발생하면 THEN 시스템은 사용자에게 인증 방법을 안내해야 합니다

### Requirement 5

**User Story:** 개발자로서, 시스템이 싱글톤 패턴을 사용하여 일관된 상태를 유지하기를 원합니다.

#### Acceptance Criteria

1. WHEN 여러 MCP 도구 호출이 발생하면 THEN 모든 호출은 동일한 GeminiIntegration 인스턴스를 공유해야 합니다
2. WHEN 속도 제한이 적용되면 THEN 모든 도구 호출이 동일한 속도 제한기를 공유해야 합니다
3. WHEN 상담 기록이 저장되면 THEN 모든 상담이 동일한 로그에 기록되어야 합니다

### Requirement 6

**User Story:** 개발자로서, 환경 변수와 설정 파일을 통해 시스템을 구성하고 싶습니다.

#### Acceptance Criteria

1. WHEN gemini-config.json 파일이 존재하면 THEN 시스템은 해당 설정을 로드해야 합니다
2. WHEN 환경 변수가 설정되면 THEN 환경 변수가 설정 파일보다 우선해야 합니다
3. WHEN 설정이 로드되면 THEN 시스템은 enabled, auto_consult, cli_command, timeout, rate_limit_delay 등의 설정을 적용해야 합니다

### Requirement 7

**User Story:** 개발자로서, Gemini CLI가 올바르게 설치되고 인증되었는지 확인하고 싶습니다.

#### Acceptance Criteria

1. WHEN 시스템이 시작되면 THEN Gemini CLI의 가용성을 확인해야 합니다
2. WHEN Gemini CLI가 설치되지 않았으면 THEN 시스템은 설치 가이드를 제공해야 합니다
3. WHEN 인증이 필요하면 THEN 시스템은 인증 방법을 안내해야 합니다

### Requirement 8

**User Story:** 개발자로서, 상담 기록과 디버깅 정보를 확인하고 싶습니다.

#### Acceptance Criteria

1. WHEN 상담이 완료되면 THEN 시스템은 상담 ID, 타임스탬프, 실행 시간을 기록해야 합니다
2. WHEN 로깅이 활성화되면 THEN 시스템은 모든 상담을 로그에 기록해야 합니다
3. WHEN 디버그 모드가 활성화되면 THEN 시스템은 상세한 디버그 정보를 제공해야 합니다