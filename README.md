# Variable Maker LangGraph
 
'Variable Maker'는 LangGraph와 Google Gemini AI를 사용하여 프로그래밍 변수명에 단어를 생성하는 Python 애플리케이션입니다.

## 주요 기능

- **한글 지원**: 한글 단어를 영어로 번역한 후 줄임말 생성
- **영어 지원**: 영어 단어에서 직접 줄임말 생성
- **대화형 인터페이스**: 명령줄에서 실시간으로 상호작용
- **LangGraph 아키텍처**: 상태 관리와 워크플로우 최적화

## 프로젝트 구조

```
variable-maker-langgraph/
├── main.py
├── cli.py               # 명령줄 인터페이스
├── graph.py             # LangGraph 그래프 설정
├── nodes.py             # LangGraph 노드 함수들
├── models.py            # State 모델
├── services.py          # 비즈니스 로직
├── tools.py
└── pyproject.toml
```

## 설치 및 설정

### 버전 및 패키지

- Python 3.11
- uv
- langchain
- langgraph
- python-dotenv
- black
- google-gemini

### 의존성 설치

```bash
# 기본 의존성 설치
uv sync

# 개발 의존성 포함 설치
uv sync --group dev
```

### 코드 포맷팅

```bash
uv run black .
```

### 환경 설정

프로젝트 루트에 `.env` 파일을 생성하고 Google API 키를 설정하세요:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

## 사용법

### 애플리케이션 실행

```bash
uv run python main.py
```

## 아키텍처

### 워크플로우

1. **명령 처리**: 특수 명령어(`:quit`, `:help`, `:case`) 처리
2. **언어 감지**: 한글 문자 포함 여부 확인
3. **번역**: 한글 단어를 영어로 번역 (필요시)
4. **줄임말 생성**: 영어 단어에서 적절한 줄임말 생성
5. **응답 포맷팅**: 결과를 사용자가 요청한 case 변경 및 사용자 친화적 형태로 포맷
