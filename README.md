# Gemini MCP Integration

Google Gemini CLI와 AI 코딩 도구들(Claude Code, Kiro, Cursor)을 통합하는 MCP(Model Context Protocol) 서버입니다. AI가 불확실성을 표현하거나 복잡한 기술적 결정에 직면했을 때 자동으로 Gemini에게 두 번째 의견을 요청할 수 있습니다.

## 🎯 지원하는 AI 코딩 도구
- **Claude Code** - Anthropic의 AI 코딩 도구
- **Kiro** - AI 어시스턴트 및 IDE
- **Cursor** - AI 기반 코드 에디터
- **기타 MCP 지원 도구들**

## 🚀 빠른 시작

### 자동 설치 (권장)

**Linux/macOS:**
```bash
# 단일 도구 설정
chmod +x setup-gemini-integration.sh
./setup-gemini-integration.sh

# 모든 도구 동시 설정 (Claude Code + Kiro + Cursor)
chmod +x setup-all-tools.sh
./setup-all-tools.sh
```

**Windows:**
```cmd
# 단일 도구 설정
setup-gemini-integration.bat

# 모든 도구 동시 설정 (Claude Code + Kiro + Cursor)
setup-all-tools.bat
```

---

## 📋 운영체제별 상세 설치 가이드

### 🪟 Windows 사용자

#### 필수 요구사항
- Windows 10/11
- 관리자 권한 (npm 전역 설치용)
- 인터넷 연결

#### 1단계: 사전 준비
1. **Node.js 설치**
   ```cmd
   # 방법 1: 공식 웹사이트에서 다운로드
   # https://nodejs.org/ 방문하여 LTS 버전 다운로드 (22.16.0 권장)
   
   # 방법 2: Chocolatey 사용 (관리자 권한 필요)
   choco install nodejs
   
   # 방법 3: Winget 사용
   winget install OpenJS.NodeJS
   ```

2. **Python 설치**
   ```cmd
   # 방법 1: 공식 웹사이트에서 다운로드
   # https://python.org/downloads/ 방문하여 3.8+ 버전 다운로드
   
   # 방법 2: Microsoft Store에서 설치
   # "Python 3.11" 검색하여 설치
   
   # 방법 3: Chocolatey 사용
   choco install python
   ```

3. **설치 확인**
   ```cmd
   node --version    # v22.16.0 이상
   python --version  # Python 3.8.0 이상
   npm --version     # 자동으로 설치됨
   ```

#### 2단계: 자동 설치 실행
```cmd
# 명령 프롬프트를 관리자 권한으로 실행
setup-gemini-integration.bat
```

#### 3단계: 서버 실행 (여러 방법)

**방법 1: 파일 탐색기 (가장 쉬움)**
- `start-server.cmd` 파일을 더블클릭

**방법 2: 명령 프롬프트**
```cmd
# 간단한 실행
start-server.cmd

# 고급 실행 (자동 설정 포함)
run-gemini-mcp.bat

# 시스템 테스트
quick-test.bat
```

**방법 3: PowerShell**
```powershell
# PowerShell 실행 정책 설정 (최초 1회)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# PowerShell 네이티브 실행
.\run-gemini-mcp.ps1

# 또는 배치 파일 실행
cmd /c run-gemini-mcp.bat

# PowerShell 래퍼 사용
.\run-server.ps1 start
```

#### Windows 문제 해결
```cmd
# Node.js 경로 문제
where node
where npm

# Python 경로 문제  
where python
where pip

# 권한 문제 해결
# 명령 프롬프트를 "관리자 권한으로 실행"

# 프록시 환경에서
npm config set proxy http://proxy.company.com:8080
npm config set https-proxy http://proxy.company.com:8080
```

---

### 🐧 Linux 사용자

#### 필수 요구사항
- Ubuntu 20.04+, CentOS 8+, 또는 기타 최신 배포판
- sudo 권한
- 인터넷 연결

#### 1단계: 시스템 업데이트
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL/Fedora
sudo dnf update -y
# 또는 (구버전)
sudo yum update -y

# Arch Linux
sudo pacman -Syu
```

#### 2단계: Node.js 설치

**방법 1: NodeSource 저장소 (권장)**
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# CentOS/RHEL/Fedora
curl -fsSL https://rpm.nodesource.com/setup_22.x | sudo bash -
sudo dnf install -y nodejs
```

**방법 2: NVM 사용 (개발자 권장)**
```bash
# NVM 설치
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 터미널 재시작 또는
source ~/.bashrc

# Node.js 설치
nvm install 22.16.0
nvm use 22.16.0
nvm alias default 22.16.0
```

**방법 3: 패키지 매니저**
```bash
# Ubuntu/Debian
sudo apt install nodejs npm

# CentOS/RHEL/Fedora
sudo dnf install nodejs npm

# Arch Linux
sudo pacman -S nodejs npm

# openSUSE
sudo zypper install nodejs npm
```

#### 3단계: Python 설치
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL/Fedora
sudo dnf install python3 python3-pip

# Arch Linux
sudo pacman -S python python-pip

# openSUSE
sudo zypper install python3 python3-pip
```

#### 4단계: 자동 설치 실행
```bash
chmod +x setup-gemini-integration.sh
./setup-gemini-integration.sh
```

#### 5단계: 서버 실행
```bash
# 기본 실행
python3 mcp-server.py --project-root .

# 디버그 모드
python3 mcp-server.py --debug

# 백그라운드 실행
nohup python3 mcp-server.py --project-root . > server.log 2>&1 &

# systemd 서비스로 실행 (선택사항)
sudo cp gemini-mcp.service /etc/systemd/system/
sudo systemctl enable gemini-mcp
sudo systemctl start gemini-mcp
```

#### Linux 문제 해결
```bash
# 권한 문제
sudo chown -R $USER:$USER ~/.npm
sudo chown -R $USER:$USER ~/.config

# Python 버전 확인
python3 --version
which python3

# 의존성 문제
sudo apt install build-essential  # Ubuntu/Debian
sudo dnf groupinstall "Development Tools"  # CentOS/RHEL/Fedora

# 방화벽 설정 (필요시)
sudo ufw allow 8080  # Ubuntu
sudo firewall-cmd --permanent --add-port=8080/tcp  # CentOS/RHEL
```

---

### 🍎 macOS 사용자

#### 필수 요구사항
- macOS 10.15 (Catalina) 이상
- Xcode Command Line Tools
- 관리자 권한

#### 1단계: Xcode Command Line Tools 설치
```bash
xcode-select --install
```

#### 2단계: Homebrew 설치 (권장)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# PATH 설정 (M1/M2 Mac의 경우)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

#### 3단계: Node.js 설치

**방법 1: Homebrew (권장)**
```bash
brew install node@22
brew link node@22

# 또는 최신 LTS
brew install node
```

**방법 2: NVM**
```bash
# NVM 설치
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 터미널 재시작 또는
source ~/.zshrc

# Node.js 설치
nvm install 22.16.0
nvm use 22.16.0
nvm alias default 22.16.0
```

**방법 3: 공식 설치 프로그램**
```bash
# https://nodejs.org/ 에서 macOS 설치 프로그램 다운로드
```

#### 4단계: Python 설치
```bash
# 방법 1: Homebrew (권장)
brew install python@3.11

# 방법 2: pyenv 사용
brew install pyenv
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
pyenv install 3.11.0
pyenv global 3.11.0

# 방법 3: 공식 설치 프로그램
# https://python.org/downloads/ 에서 macOS 설치 프로그램 다운로드
```

#### 5단계: 자동 설치 실행
```bash
chmod +x setup-gemini-integration.sh
./setup-gemini-integration.sh
```

#### 6단계: 서버 실행
```bash
# 기본 실행
python3 mcp-server.py --project-root .

# 디버그 모드
python3 mcp-server.py --debug

# 백그라운드 실행
nohup python3 mcp-server.py --project-root . > server.log 2>&1 &

# launchd 서비스로 실행 (선택사항)
cp com.gemini-mcp.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.gemini-mcp.plist
```

#### macOS 문제 해결
```bash
# Homebrew 경로 문제 (M1/M2 Mac)
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Python 경로 문제
which python3
ls -la /usr/bin/python*

# 권한 문제
sudo chown -R $(whoami) /usr/local/lib/node_modules

# Gatekeeper 문제 (보안)
sudo spctl --master-disable  # 주의: 보안 위험
```

---

## 🔧 공통 설정 및 실행

### Gemini CLI 인증 (모든 OS)
```bash
# 대화형 인증 시작
gemini

# 브라우저가 열리면 Google 계정으로 로그인
# 인증 완료 후 터미널로 돌아옴

# 인증 확인
gemini --help
```

### MCP 설정 파일 생성

각 AI 코딩 도구별로 설정 디렉토리가 다릅니다:

```bash
# Claude Code
mkdir -p .claude/settings

# Kiro
mkdir -p .kiro/settings

# Cursor
mkdir -p .cursor/settings

# Windows에서는 백슬래시 사용
mkdir .claude\settings
mkdir .kiro\settings  
mkdir .cursor\settings
```

### 환경 변수 설정

**Linux/macOS:**
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
export GEMINI_ENABLED=true
export GEMINI_AUTO_CONSULT=true
export GEMINI_CLI_COMMAND=gemini
export GEMINI_TIMEOUT=60
export GEMINI_RATE_LIMIT=2
export GEMINI_MODEL=gemini-2.5-flash

# 적용
source ~/.bashrc  # 또는 ~/.zshrc
```

**Windows:**
```cmd
# 임시 설정 (현재 세션)
set GEMINI_ENABLED=true
set GEMINI_AUTO_CONSULT=true

# 영구 설정 (시스템 전체)
setx GEMINI_ENABLED true
setx GEMINI_AUTO_CONSULT true
```

**PowerShell:**
```powershell
# 임시 설정
$env:GEMINI_ENABLED = "true"
$env:GEMINI_AUTO_CONSULT = "true"

# 영구 설정 (사용자)
[Environment]::SetEnvironmentVariable("GEMINI_ENABLED", "true", "User")
[Environment]::SetEnvironmentVariable("GEMINI_AUTO_CONSULT", "true", "User")
```

### 서버 상태 확인
```bash
# 모든 OS에서 공통
python3 -c "
import sys
sys.path.insert(0, '.')
from mcp_server import MCPServer
server = MCPServer('.')
print('✅ MCP Server 설정 완료')
"

# 테스트 실행
python3 -m pytest tests/ -v
```

---

## 🎯 AI 코딩 도구별 연동 설정

### MCP 설정 파일 위치

#### Claude Code
**Windows:**
- 워크스페이스: `.claude\settings\mcp.json`
- 사용자 전역: `%USERPROFILE%\.claude\settings\mcp.json`

**Linux/macOS:**
- 워크스페이스: `.claude/settings/mcp.json`
- 사용자 전역: `~/.claude/settings/mcp.json`

#### Kiro
**Windows:**
- 워크스페이스: `.kiro\settings\mcp.json`
- 사용자 전역: `%USERPROFILE%\.kiro\settings\mcp.json`

**Linux/macOS:**
- 워크스페이스: `.kiro/settings/mcp.json`
- 사용자 전역: `~/.kiro/settings/mcp.json`

#### Cursor
**Windows:**
- 워크스페이스: `.cursor\settings\mcp.json`
- 사용자 전역: `%USERPROFILE%\.cursor\settings\mcp.json`

**Linux/macOS:**
- 워크스페이스: `.cursor/settings/mcp.json`
- 사용자 전역: `~/.cursor/settings/mcp.json`

### 기본 MCP 설정 (모든 도구 공통)
```json
{
    "mcpServers": {
        "gemini-integration": {
            "command": "python3",
            "args": ["mcp-server.py", "--project-root", "."],
            "env": {
                "GEMINI_ENABLED": "true",
                "GEMINI_AUTO_CONSULT": "true"
            },
            "disabled": false,
            "autoApprove": ["gemini_status"]
        }
    }
}
```

### 도구별 최적화 설정

#### Claude Code 최적화 설정
```json
{
    "mcpServers": {
        "gemini-integration": {
            "command": "python3",
            "args": ["mcp-server.py", "--project-root", "."],
            "env": {
                "GEMINI_ENABLED": "true",
                "GEMINI_AUTO_CONSULT": "true",
                "GEMINI_MODEL": "gemini-2.5-flash",
                "GEMINI_RATE_LIMIT": "2"
            },
            "disabled": false,
            "autoApprove": ["gemini_status", "toggle_gemini_auto_consult"]
        }
    }
}
```

#### Kiro 최적화 설정
```json
{
    "mcpServers": {
        "gemini-integration": {
            "command": "python3",
            "args": ["mcp-server.py", "--project-root", "."],
            "env": {
                "GEMINI_ENABLED": "true",
                "GEMINI_AUTO_CONSULT": "true",
                "GEMINI_MODEL": "gemini-2.5-pro",
                "GEMINI_DEBUG": "false"
            },
            "disabled": false,
            "autoApprove": ["gemini_status"]
        }
    }
}
```

#### Cursor 최적화 설정
```json
{
    "mcpServers": {
        "gemini-integration": {
            "command": "python3",
            "args": ["mcp-server.py", "--project-root", "."],
            "env": {
                "GEMINI_ENABLED": "true",
                "GEMINI_AUTO_CONSULT": "true",
                "GEMINI_MODEL": "gemini-2.5-flash",
                "GEMINI_RATE_LIMIT": "3",
                "GEMINI_TIMEOUT": "45"
            },
            "disabled": false,
            "autoApprove": ["gemini_status"]
        }
    }
}
```

**Windows 사용자 주의사항:**
- `python3` 대신 `python` 사용할 수도 있음
- 경로 구분자는 자동으로 처리됨

이제 모든 운영체제에서 Gemini MCP Integration을 완벽하게 설치하고 실행할 수 있습니다! 🎉

## 🎯 주요 기능

### 자동 상담
AI의 응답에서 다음 패턴을 감지하면 자동으로 Gemini 상담:

#### 🤔 불확실성 패턴
- **한국어**: "잘 모르겠어", "확실하지 않아", "것 같아", "아마도", "어쩌면"
- **English**: "I'm not sure", "I think", "possibly", "maybe", "probably"

#### 🚨 에러/문제 패턴
- **한국어**: "에러났어", "오류가 발생", "문제가 있어", "버그", "안 돼", "실패했어", "작동하지 않아"
- **English**: "error", "bug", "issue", "problem", "failed", "not working", "broken", "stuck"

#### 🆘 도움 요청 패턴  
- **한국어**: "도와줘", "어떻게 해야 해", "방법을 알려줘", "설명해줘", "해결"
- **English**: "help me", "how should I", "guide me", "explain", "show me"

#### 🤷 복잡한 결정 패턴
- **한국어**: "어떤 게 좋을까", "선택", "결정", "고민", "여러 방법", "비교", "vs", "중에"
- **English**: "multiple approaches", "trade-offs", "alternatives", "choice between", "which is better"

#### ⚠️ 중요한 작업 패턴
- **공통**: "production", "security", "database migration", "보안", "프로덕션", "데이터베이스"

### 수동 상담
필요시 `consult_gemini` 도구로 직접 Gemini에게 상담 요청

### 상태 관리
- 통합 상태 및 통계 확인
- 자동 상담 활성화/비활성화
- 설정 실시간 변경

## 🔧 사용법

### 자동 상담 사용 예시

다음과 같은 질문들을 하면 자동으로 Gemini 상담이 트리거됩니다:

#### 🚨 에러/문제 상황
```
"Python 코드에서 에러났어"
"React 컴포넌트가 작동하지 않아"  
"이 함수에 버그가 있는 것 같아"
"데이터베이스 연결이 실패했어"
"API 호출이 안 돼"
```

#### 🆘 도움 요청
```
"JWT 토큰 사용법을 알려줘"
"Docker 컨테이너 설정 방법을 설명해줘"
"이 코드를 어떻게 최적화할까?"
"React Hook 사용법 도와줘"
```

#### 🤷 선택/결정 고민
```
"React와 Vue 중에 어떤 게 좋을까?"
"MySQL과 PostgreSQL 중 뭘 선택해야 할지 모르겠어"
"REST API와 GraphQL의 장단점을 비교해줘"
```

#### 🤔 불확실한 상황
```
"이 방법이 맞는지 확실하지 않아"
"보안 설정이 제대로 된 것 같은데..."
"성능 최적화가 필요한 것 같아"
```

### MCP 서버 실행
```bash
python3 mcp-server.py --project-root .

# 디버그 모드
python3 mcp-server.py --debug
```

### AI 코딩 도구에서 사용
MCP 서버가 실행되면 다음 도구들을 사용할 수 있습니다:

1. **consult_gemini** - Gemini 상담 요청
   ```
   query: "실시간 통신에 WebSocket과 gRPC 중 무엇을 사용해야 하나요?"
   context: "멀티플레이어 게임 서버 구축 중"
   ```

2. **gemini_status** - 통합 상태 확인
   ```
   통합 상태, 설정, 통계 정보 표시
   ```

3. **toggle_gemini_auto_consult** - 자동 상담 토글
   ```
   enable: true/false
   ```

## ⚙️ 설정

### 설정 파일 (`gemini-config.json`)
```json
{
    "enabled": true,
    "auto_consult": true,
    "cli_command": "gemini",
    "timeout": 60,
    "rate_limit_delay": 2.0,
    "max_context_length": 4000,
    "log_consultations": true,
    "model": "gemini-2.5-flash",
    "sandbox_mode": false,
    "debug_mode": false
}
```

### 환경 변수
```bash
export GEMINI_ENABLED=true
export GEMINI_AUTO_CONSULT=true
export GEMINI_CLI_COMMAND=gemini
export GEMINI_TIMEOUT=60
export GEMINI_RATE_LIMIT=2
export GEMINI_MODEL=gemini-2.5-flash
```

### MCP 설정 예시 (각 도구별 설정 파일)

**Claude Code** (`.claude/settings/mcp.json`):
```json
{
    "mcpServers": {
        "gemini-integration": {
            "command": "python3",
            "args": ["mcp-server.py", "--project-root", "."],
            "env": {
                "GEMINI_ENABLED": "true",
                "GEMINI_AUTO_CONSULT": "true",
                "GEMINI_MODEL": "gemini-2.5-flash"
            },
            "disabled": false,
            "autoApprove": ["gemini_status"]
        }
    }
}
```

**Kiro** (`.kiro/settings/mcp.json`):
```json
{
    "mcpServers": {
        "gemini-integration": {
            "command": "python3",
            "args": ["mcp-server.py", "--project-root", "."],
            "env": {
                "GEMINI_ENABLED": "true",
                "GEMINI_AUTO_CONSULT": "true",
                "GEMINI_MODEL": "gemini-2.5-pro"
            },
            "disabled": false,
            "autoApprove": ["gemini_status"]
        }
    }
}
```

**Cursor** (`.cursor/settings/mcp.json`):
```json
{
    "mcpServers": {
        "gemini-integration": {
            "command": "python3",
            "args": ["mcp-server.py", "--project-root", "."],
            "env": {
                "GEMINI_ENABLED": "true",
                "GEMINI_AUTO_CONSULT": "true",
                "GEMINI_RATE_LIMIT": "3"
            },
            "disabled": false,
            "autoApprove": ["gemini_status"]
        }
    }
}
```

## 🧪 테스트

```bash
# 모든 테스트 실행
python3 -m pytest tests/ -v

# 특정 테스트 파일
python3 -m pytest tests/test_gemini_integration.py -v

# 커버리지 포함
pip install pytest-cov
python3 -m pytest tests/ --cov=. --cov-report=html
```

## 📁 프로젝트 구조

```
├── gemini_integration.py      # 핵심 통합 모듈 (한국어/영어 패턴 감지)
├── mcp-server.py             # MCP 서버 구현
├── gemini-config.json        # 설정 파일
├── requirements.txt          # Python 의존성
├── setup-all-tools.bat/.sh  # 모든 도구 동시 설정 (Claude Code + Kiro + Cursor)
├── setup-gemini-integration.sh/.bat  # 개별 설치 스크립트
├── start-server.cmd          # Windows 간편 실행
├── run-gemini-mcp.bat/.ps1   # Windows 고급 실행기
├── quick-test.bat            # Windows 시스템 테스트
├── README.md                 # 이 파일 (완전한 설정 가이드)
├── TROUBLESHOOTING.md        # 문제 해결 가이드
├── WINDOWS-USAGE.md          # Windows 전용 사용법
├── QUICK-START-WINDOWS.md    # Windows 빠른 시작
└── tests/                    # 테스트 파일들
    ├── test_gemini_integration.py  # 패턴 감지 테스트
    ├── test_gemini_cli.py          # CLI 통합 테스트
    └── test_mcp_server.py          # MCP 서버 테스트
```

### 🎯 핵심 기능
- **다국어 패턴 감지**: 한국어와 영어 패턴 모두 지원
- **에러 자동 감지**: "에러났어", "버그", "문제" 등 자동 상담 트리거
- **도움 요청 감지**: "도와줘", "알려줘", "설명해줘" 등 자동 상담
- **다중 도구 지원**: Claude Code, Kiro, Cursor 동시 지원
- **Windows 최적화**: 배치 파일, PowerShell 스크립트 완비

## 🚨 문제 해결

일반적인 문제들과 해결 방법은 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)를 참조하세요.

### 자동 상담이 작동하지 않는 경우

#### 1. **패턴이 감지되지 않음**
```bash
# 패턴 테스트
python -c "
from gemini_integration import GeminiIntegration
gi = GeminiIntegration()
result = gi.detect_uncertainty('에러났어 도와줘')
print(f'감지됨: {result[0]}, 패턴: {result[1]}')
"
```

#### 2. **MCP 서버 연결 문제**
- **상태 확인**: `gemini_status` 도구 실행
- **서버 재시작**: `start-server.cmd` 실행
- **디버그 모드**: `python mcp-server.py --debug`

#### 3. **Gemini CLI 인증 문제**
```bash
# 인증 확인 및 재인증
gemini --help
gemini  # 대화형 인증 진행
```

### 빠른 해결책

1. **자동 상담 테스트**
   ```
   "React에서 에러났는데 어떻게 해결할까?"
   ```

2. **MCP 서버 연결 실패**
   ```bash
   python3 mcp-server.py --debug  # 디버그 로그 확인
   ```

3. **Node.js 버전 문제**
   ```bash
   nvm use 22.16.0  # 권장 버전 사용
   ```

## 🔐 보안 고려사항

- API 자격 증명을 안전하게 저장
- 독점 코드 전송 시 주의
- 속도 제한 준수 (무료 등급: 분당 60개, 하루 1000개)
- 입력 데이터 검증

## 📈 성능 최적화

- 적절한 속도 제한 설정
- 컨텍스트 길이 제한
- 상담 로그 관리 (최대 100개 항목)
- 캐싱 활용 (유사한 쿼리)

## 🤝 기여

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 라이선스

MIT License - 자세한 내용은 LICENSE 파일을 참조하세요.

## 🙏 감사

- Google Gemini CLI 팀
- Anthropic Claude Code 개발팀
- Kiro 개발팀
- Cursor 개발팀
- MCP 프로토콜 개발자들