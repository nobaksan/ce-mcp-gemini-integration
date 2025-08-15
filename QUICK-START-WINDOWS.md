# Windows 빠른 시작 가이드

## 🎯 가장 쉬운 방법 (초보자용)

### 1단계: 설치
1. 파일 탐색기에서 프로젝트 폴더 열기
2. `setup-gemini-integration.bat` **더블클릭**
3. 설치 완료까지 기다리기

### 2단계: 실행
1. `start-server.cmd` **더블클릭**
2. 서버가 시작되면 완료!

## 🔧 명령줄 사용자용

### 명령 프롬프트 (CMD)
```cmd
# 설치
setup-gemini-integration.bat

# 실행 (간단)
start-server.cmd

# 실행 (고급)
run-gemini-mcp.bat

# 테스트
quick-test.bat
```

### PowerShell
```powershell
# 설치
cmd /c setup-gemini-integration.bat

# 실행 옵션들
.\run-gemini-mcp.ps1                    # PowerShell 네이티브
cmd /c start-server.cmd                 # 간단한 방법
cmd /c run-gemini-mcp.bat              # 고급 배치 실행기

# 또는 PowerShell 래퍼 사용
.\run-server.ps1 start                 # 서버 시작
.\run-server.ps1 test                  # 테스트 실행
.\run-server.ps1 setup                 # 설치 실행
```

## 🚨 문제 해결

### "실행할 수 없습니다" 오류
**PowerShell에서 스크립트 실행이 차단되는 경우:**
```powershell
# 현재 세션에서만 허용
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# 그 후 다시 실행
.\run-gemini-mcp.ps1
```

### "명령을 찾을 수 없습니다" 오류
**PowerShell에서 .bat 파일을 직접 실행할 수 없는 경우:**
```powershell
# 올바른 방법
cmd /c run-gemini-mcp.bat

# 잘못된 방법 (오류 발생)
run-gemini-mcp.bat
```

### 권한 오류
**관리자 권한이 필요한 경우:**
1. 명령 프롬프트를 **"관리자 권한으로 실행"**
2. 또는 PowerShell을 **"관리자 권한으로 실행"**
3. 그 후 설치 스크립트 실행

## 📋 체크리스트

설치 전 확인사항:
- [ ] Windows 10/11
- [ ] 인터넷 연결
- [ ] 관리자 권한 (npm 설치용)

설치 후 확인사항:
- [ ] `quick-test.bat` 실행해서 모든 테스트 통과
- [ ] `gemini` 명령어로 Google 계정 인증 완료
- [ ] `start-server.cmd`로 서버 정상 시작

## 💡 팁

1. **바탕화면 바로가기**: `start-server.cmd`를 바탕화면에 복사해서 바로가기 만들기
2. **시작 메뉴 등록**: 시작 메뉴에 바로가기 추가
3. **자동 시작**: 시작 프로그램에 추가하여 부팅시 자동 실행
4. **작업 표시줄 고정**: 자주 사용하는 경우 작업 표시줄에 고정

## 🎉 완료!

이제 Claude Code에서 다음 MCP 도구들을 사용할 수 있습니다:
- `consult_gemini`: Gemini에게 상담 요청
- `gemini_status`: 통합 상태 확인  
- `toggle_gemini_auto_consult`: 자동 상담 토글

더 자세한 정보는 [WINDOWS-USAGE.md](WINDOWS-USAGE.md)를 참조하세요!