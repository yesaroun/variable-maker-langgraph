import time
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from graph import create_graph
from models import CaseStyle, get_case_style_options

st.set_page_config(page_title="Variable Maker", layout="wide")


def get_chat_title(first_message, max_length=30):
    """첫 번째 메시지에서 채팅 제목을 생성합니다."""
    if len(first_message) <= max_length:
        return first_message
    return first_message[:max_length] + "..."


# 초기화
if "app" not in st.session_state:
    st.session_state.app = create_graph()
    st.session_state.chat_sessions = (
        {}
    )  # {session_id: {"title": str, "messages": [(role, content)], "thread_id": str}} -> TODO: 이거 dataclass로 분리하기
    st.session_state.current_session_id = None
    st.session_state.case_style = CaseStyle.CAMEL_CASE

with st.sidebar:
    st.markdown("### 채팅 목록")

    if st.button("새로운 채팅 시작하기", use_container_width=True):
        new_session_id = f"session_{int(time.time())}"  # TODO: 시간만이 아니라 uuid사용하거나 아니면 현재 streamlit 실행된 고유 아이디 없나? 그거 적용하기
        st.session_state.current_session_id = new_session_id
        st.session_state.chat_sessions[new_session_id] = {
            "title": "새로운 채팅",
            "messages": [],
            "thread_id": f"thread_{new_session_id}",
        }
        st.rerun()

    st.divider()

    if (
        st.session_state.chat_sessions
    ):  # TODO: session_state에 대한 구조를 정의할수는 없는 것인가?
        for session_id, session_data in st.session_state.chat_sessions.items():
            # 현재 활성 세션 표시
            if_current = session_id == st.session_state.current_session_id
            button_style = "➡ " if if_current else ""

            if st.button(
                f"{button_style}{session_data['title']}",
                key=f"chat_{session_id}",
                use_container_width=True,
            ):
                st.session_state.current_session_id = session_id
                st.rerun()

    else:
        st.markdown("_아직 채팅이 없습니다._")

st.title("Variable Maker")

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

# 채팅 컨테이너 - 현재 세션의 대화만 표시
chat_container = st.container()
with chat_container:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    if (
        st.session_state.current_session_id
        and st.session_state.current_session_id in st.session_state.chat_sessions
    ):
        current_messages = st.session_state.chat_sessions[
            st.session_state.current_session_id
        ]["messages"]
        for role, content in current_messages:
            with st.chat_message(role):
                st.write(content)

st.markdown("<div class='input-container'>", unsafe_allow_html=True)

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
    if not st.session_state.current_session_id:
        new_session_id = f"session_{int(time.time())}"
        st.session_state.current_session_id = new_session_id
        st.session_state.chat_sessions[new_session_id] = {
            "title": get_chat_title(user_input),
            "messages": [],
            "thread_id": f"thread_{new_session_id}",
        }

    current_session = st.session_state.chat_sessions[
        st.session_state.current_session_id
    ]

    if not current_session["messages"]:
        current_session["title"] = get_chat_title(user_input)

    current_session["messages"].append(("user", user_input))

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
    config = {"configurable": {"thread_id": current_session["thread_id"]}}

    try:
        result = st.session_state.app.invoke(initial_state, config)

        # 그래프에서 케이스 스타일이 바뀌었으면 반영
        if "selected_case_style" in result and result["selected_case_style"]:
            st.session_state.case_style = result["selected_case_style"]

        ai_msg = next(
            (m for m in reversed(result["messages"]) if isinstance(m, AIMessage)),
            None,
        )
        if ai_msg:
            current_session["messages"].append(("assistant", ai_msg.content))

    except Exception as e:
        current_session["messages"].append(("assistant", f"오류가 발생했습니다: {e}"))

    st.rerun()
