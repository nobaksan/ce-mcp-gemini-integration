# Windows 사용 가이드

## 🚀 빠른 시작 (Windows)

### 1단계: 자동 설치
```cmd
setup-gemini-integration.bat
```

### 2단계: 서버 실행
다음 중 하나를 선택하세요:

**옵션 A: 간단한 실행**
```cmd
start-server.cmd
```

**옵션 B: 고급 실행 (배치 파일)**
```cmd
run-gemini-mcp.bat
```

**옵션 C: PowerShell 실행**
```powershell
.\run-gemini-mcp.ps1
```

**옵션 D: 직접 실행**
```cmd
python mcp-server.py --project-root .
```

## 🧪 시스템 테스트

설치 후 모든 것이 올바르게 작동하는지 확인:
```cmd
quick-test.bat
```

## 📁 Windows 전용 파일들

| 파일 | 용도 | 설명 |
|------|------|------|
| `setup-gemini-integration.bat` | 설치 | 전체 시스템 자동 설치 |
| `start-server.cmd` | 실행 | 가장 간단한 서버 시작 |
| `run-gemini-mcp.bat` | 실행 | 고급 배치 실행기 (자동 설정 포함) |
| `run-gemini-mcp.ps1` | 실행 | PowerShell 실행기 (고급 기능) |
| `quick-test.bat` | 테스트 | 시스템 상태 빠른 확인 |

## 🔧 PowerShell 고급 사용법

### 기본 실행
```powershell
.\run-gemini-mcp.ps1
```

### 디버그 모드
```powershell
.\run-gemini-mcp.ps1 -Debug
```

### 자동 설치 포함
```powershell
.\run-gemini-mcp.ps1 -Setup
```

### 사용자 정의 프로젝트 루트
```powershell
.\run-gemini-mcp.ps1 -ProjectRoot "C:\MyProject"
```

### 모든 옵션 조합
```powershell
.\run-gemini-mcp.ps1 -Debug -Setup -ProjectRoot "."
```

### PowerShell에서 배치 파일 실행
PowerShell에서 .bat 파일을 실행하려면:
```powershell
# 방법 1: cmd를 통해 실행 (권장)
cmd /c run-gemini-mcp.bat

# 방법 2: & 연산자 사용
& .\start-server.cmd

# 방법 3: Start-Process 사용
Start-Process -FilePath "run-gemini-mcp.bat" -Wait

# 방법 4: Invoke-Expression 사용
Invoke-Expression ".\run-gemini-mcp.bat"
```

## 🛠️ Windows 특별 고려사항

### 실행 정책 (PowerShell)
PowerShell 스크립트 실행이 차단되는 경우:
```powershell
# 현재 세션에서만 허용
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# 또는 현재 사용자에 대해 허용
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 관리자 권한
npm 전역 설치 시 관리자 권한이 필요할 수 있습니다:
1. 명령 프롬프트를 "관리자 권한으로 실행"
2. 또는 PowerShell을 "관리자 권한으로 실행"

### 경로 문제
Windows에서 경로 구분자는 백슬래시(`\`)를 사용합니다:
```cmd
# 올바른 경로
.kiro\settings\mcp.json

# Python에서는 자동으로 처리됨
python mcp-server.py --project-root .
```

### 환경 변수 설정
```cmd
# 임시 설정 (현재 세션만)
set GEMINI_ENABLED=true
set GEMINI_DEBUG=true

# 영구 설정 (시스템 전체)
setx GEMINI_ENABLED true
setx GEMINI_DEBUG true
```

PowerShell에서:
```powershell
# 임시 설정
$env:GEMINI_ENABLED = "true"
$env:GEMINI_DEBUG = "true"

# 영구 설정
[Environment]::SetEnvironmentVariable("GEMINI_ENABLED", "true", "User")
```

## 🚨 Windows 문제 해결

### 일반적인 Windows 오류

**1. "python을 찾을 수 없습니다"**
```cmd
# Python 설치 확인
where python
python --version

# Python이 없으면 설치
# https://python.org/downloads/ 에서 다운로드
```

**2. "gemini을 찾을 수 없습니다"**
```cmd
# Node.js 설치 확인
where node
node --version

# Gemini CLI 설치
npm install -g @google/gemini-cli
```

**3. "권한이 거부되었습니다"**
```cmd
# 관리자 권한으로 명령 프롬프트 실행
# 또는 사용자 디렉토리에 설치
npm install -g @google/gemini-cli --prefix=%APPDATA%\npm
```

**4. "모듈을 찾을 수 없습니다"**
```cmd
# Python 의존성 재설치
pip install --upgrade -r requirements.txt

# 또는 사용자 디렉토리에 설치
pip install --user -r requirements.txt
```

### Windows Defender 경고
일부 경우 Windows Defender가 Python 스크립트를 차단할 수 있습니다:
1. Windows Defender 설정 열기
2. "바이러스 및 위협 방지" → "설정 관리"
3. "실시간 보호" 일시 비활성화 (설치 중에만)
4. 또는 프로젝트 폴더를 예외 목록에 추가

### 네트워크 프록시
회사 네트워크에서 프록시를 사용하는 경우:
```cmd
# npm 프록시 설정
npm config set proxy http://proxy.company.com:8080
npm config set https-proxy http://proxy.company.com:8080

# pip 프록시 설정
pip install --proxy http://proxy.company.com:8080 -r requirements.txt
```

## 📊 성능 최적화 (Windows)

### Windows Terminal 사용
기본 명령 프롬프트 대신 Windows Terminal 사용 권장:
- Microsoft Store에서 "Windows Terminal" 설치
- 더 나은 UTF-8 지원 및 이모지 표시
- 탭 기능 및 향상된 사용자 경험

### 바이러스 스캔 예외
성능 향상을 위해 프로젝트 폴더를 바이러스 스캔에서 제외:
1. Windows Defender 설정
2. "바이러스 및 위협 방지"
3. "설정 관리" → "제외 항목 추가 또는 제거"
4. 프로젝트 폴더 추가

## 🔄 업데이트 및 유지보수

### 자동 업데이트 확인
```cmd
# Gemini CLI 업데이트
npm update -g @google/gemini-cli

# Python 패키지 업데이트
pip install --upgrade -r requirements.txt
```

### 설정 초기화
```cmd
# 설정 파일 삭제 후 재생성
del gemini-config.json
del .kiro\settings\mcp.json
run-gemini-mcp.bat
```

## 💡 Windows 팁

1. **바로가기 만들기**: `start-server.cmd`에 대한 바탕화면 바로가기 생성
2. **시작 프로그램**: 시스템 시작 시 자동 실행하려면 시작 프로그램 폴더에 바로가기 추가
3. **작업 스케줄러**: 정기적인 실행을 위해 Windows 작업 스케줄러 사용
4. **서비스 등록**: `nssm` 도구를 사용하여 Windows 서비스로 등록 가능

이 가이드를 따라하면 Windows에서 Gemini MCP Integration을 쉽게 설치하고 실행할 수 있습니다!