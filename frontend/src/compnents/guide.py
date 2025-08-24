import streamlit as st


def render_usage_guide():
    """사용법 가이드를 렌더링합니다."""
    st.markdown(
        """
###Variable Maker 사용법

**단어 입력 (약어 생성):
    - 예시: 중취감, international, 데이터베이스
    - 결과: 한국어는 영어 번역 후 약어 생성
    - 케이스 스타일: camelCase, snake_case, PascalCase, kebab-case, CONSTANT_CASE

**문장/텍스트 입력 (변수명 추출):**
    - 예시: 중소기업 취업자 감면을 변수로 만들어주세요
    - 팁: 핵심 비즈니스 용어에 집중합니다
    - 팁: '변수', '만들어주세요' 같은 요청 문구는 무시됩니다

케이스 스타일을 선택하고 단어나 문장을 입력해보세요!
    """
    )
