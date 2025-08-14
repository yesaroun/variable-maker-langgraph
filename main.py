import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from graph import create_graph
from models import CaseStyle, get_case_style_options

st.set_page_config(page_title="Variable Maker", layout="wide")


# 초기화
if "app" not in st.session_state:
    st.session_state.app = create_graph()
    st.session_state.thread_id = "st_session_1"
    st.session_state.case_style = CaseStyle.CAMEL_CASE
    st.session_state.history = []  # [(role, content)]
    # 도움말 추가 제거 - 마크다운으로 고정 표시

# 사이드바: 채팅 기록
with st.sidebar:
    st.markdown("### 채팅 기록")
    if st.session_state.history:
        for i, (role, content) in enumerate(st.session_state.history):
            role_icon = "🧑" if role == "user" else "🤖"
            st.markdown(f"**{role_icon} {role.title()}:**")
            st.markdown(f"_{content}_")
            if i < len(st.session_state.history) - 1:
                st.divider()
    else:
        st.markdown("_아직 대화가 없습니다._")

st.title("Variable Maker")

# 도움말을 마크다운으로 직접 표시
st.markdown(
    """
### 💡 Variable Maker 사용법

**단어 입력 (약어 생성):**
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

# 채팅 컨테이너 - 사용자 대화만 표시
chat_container = st.container()
with chat_container:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    # 기존 대화 렌더링 (도움말 제외)
    for role, content in st.session_state.history:
        with st.chat_message(role):
            st.write(content)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='input-container'>", unsafe_allow_html=True)

# 케이스 스타일 선택과 입력을 나란히 배치
col1, col2 = st.columns([2, 6])

with col1:
    options = get_case_style_options()  # [(num, CaseStyle, desc)]
    label_to_case = {desc: cs for _, cs, desc in options}
    labels = list(label_to_case.keys())
    current_idx = [
        i for i, (_, cs, _) in enumerate(options) if cs == st.session_state.case_style
    ][0]
    selected_label = st.selectbox(
        "",
        labels,
        index=current_idx,
        key="case_style_selector",
        label_visibility="collapsed",
    )
    st.session_state.case_style = label_to_case[selected_label]

with col2:
    user_input = st.chat_input("단어 또는 텍스트를 입력하세요.")

st.markdown("</div>", unsafe_allow_html=True)

if user_input:
    # 사용자 메시지를 히스토리에만 추가
    st.session_state.history.append(("user", user_input))

    initial_state = {
        "messages": [HumanMessage(content=user_input)],
        "input_type": None,
        "current_input": "",
        "is_korean": False,
        "translated_word": "",
        "abbreviations": [],
        "processed_text": "",
        "selected_case_style": st.session_state.case_style,
    }
    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    try:
        result = st.session_state.app.invoke(initial_state, config)

        # 그래프에서 케이스 스타일이 바뀌었으면 반영
        if "selected_case_style" in result and result["selected_case_style"]:
            st.session_state.case_style = result["selected_case_style"]

        # 가장 최근 AI 응답을 히스토리에만 추가
        ai_msg = next(
            (m for m in reversed(result["messages"]) if isinstance(m, AIMessage)),
            None,
        )
        if ai_msg:
            st.session_state.history.append(("assistant", ai_msg.content))

    except Exception as e:
        st.session_state.history.append(("assistant", f"오류가 발생했습니다: {e}"))

    st.rerun()
