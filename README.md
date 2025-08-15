# Variable Maker LangGraph

**Variable Maker**는 LangGraph와 Google Gemini AI를 사용하여 프로그래밍 변수명을 자동 생성하는 **Streamlit 웹 애플리케이션**입니다.

## 주요 기능

- **웹 인터페이스**: Streamlit을 사용한 직관적인 웹 UI
- **한글 지원**: 한글 단어를 영어로 번역한 후 변수명 생성
- **영어 지원**: 영어 단어에서 직접 변수명과 약어 생성
- **텍스트 처리**: 문장에서 핵심 비즈니스 용어 추출 및 변수명 생성
- **다양한 케이스 스타일**: camelCase, snake_case, PascalCase, kebab-case, CONSTANT_CASE
- **채팅 인터페이스**: 여러 세션 관리 및 대화형 처리
- **LangGraph 아키텍처**: 상태 관리와 워크플로우 최적화

## 프로젝트 구조

```
variable-maker-langgraph/
├── src/                          # 소스 코드 루트
│   ├── __init__.py
│   ├── core/                     # 핵심 비즈니스 로직 (LangGraph)
│   │   ├── __init__.py
│   │   ├── models.py             # 데이터 모델 및 타입 정의
│   │   ├── graph.py              # LangGraph 정의
│   │   ├── nodes.py              # LangGraph 노드들
│   │   ├── services.py           # AI 서비스 (번역, 약어 생성 등)
│   │   └── tools.py              # LangChain 도구들
│   ├── ui/                       # UI 레이어 (Streamlit)
│   │   ├── __init__.py
│   │   ├── app.py                # Streamlit 앱 메인
│   │   ├── components.py         # UI 컴포넌트들
│   │   └── handlers.py           # 이벤트 핸들러들
│   └── utils/                    # 공통 유틸리티
│       ├── __init__.py
│       └── helpers.py            # 헬퍼 함수들
├── main.py                       # Streamlit 앱 진입점
├── pyproject.toml                # 프로젝트 설정
├── uv.lock                       # 의존성 락 파일
└── README.md                     # 프로젝트 문서
```

## 설치 및 설정

### 시스템 요구사항

- Python 3.11+
- uv (패키지 관리자)

### 핵심 의존성

- **langchain**: LangChain 프레임워크
- **langchain-google-genai**: Google Gemini AI 통합
- **langgraph**: 상태 관리 그래프 워크플로우
- **streamlit**: 웹 UI 프레임워크
- **python-dotenv**: 환경 변수 관리

### 설치 과정

1. **저장소 클론**
```bash
git clone <repository-url>
cd variable-maker-langgraph
```

2. **의존성 설치**
```bash
# 기본 의존성 설치
uv sync

# 개발 의존성 포함 설치
uv sync --group dev
```

3. **환경 설정**

프로젝트 루트에 `.env` 파일을 생성하고 Google API 키를 설정하세요:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

## 사용법

### Streamlit 웹 앱 실행

```bash
streamlit run main.py
```

또는

```bash
uv run streamlit run main.py
```

브라우저에서 `http://localhost:8501`로 접속하여 사용할 수 있습니다.

### 사용 예시

#### 단어 입력 (약어 생성)
- **한글**: `데이터베이스` → `database` → `db`, `database`
- **영어**: `international` → `intl`, `int`
- **복합어**: `사용자 인증` → `userAuth`, `userAuthentication`

#### 문장 입력 (변수명 추출)
- **입력**: "중소기업 취업자 감면을 변수로 만들어주세요"
- **출력**: 
  - 중소기업 취업자 감면: `smallBusinessEmployeeTax`, `smbEmpTax`, `sbeTax`

#### 케이스 스타일 선택
- **camelCase**: `userName`
- **snake_case**: `user_name`
- **PascalCase**: `UserName`
- **kebab-case**: `user-name`
- **CONSTANT_CASE**: `USER_NAME`

## 아키텍처

### 워크플로우

1. **입력 분류**: 단어 vs 텍스트 자동 판별
2. **언어 감지**: 한글 문자 포함 여부 확인
3. **처리 라우팅**: 
   - **단어**: 번역 → 약어 생성 → 케이스 변환
   - **텍스트**: 핵심 용어 추출 → 변수명 생성 → 케이스 변환
4. **결과 포맷팅**: 사용자 친화적 형태로 출력

### LangGraph 노드

- **chatbot_node**: 입력 분류 및 초기 처리
- **word_node**: 단어 처리 (번역 + 약어 생성)
- **text_node**: 텍스트 처리 (핵심 용어 추출)

## 개발

### 코드 포맷팅

```bash
uv run black .
```
