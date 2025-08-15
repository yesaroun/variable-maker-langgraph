import streamlit as st
from models import ChatSession, get_case_style_options
from utils import generate_chat_session_id


def render_sidebar():
    """사이드바 채팅 목록을 렌더링합니다."""
    with st.sidebar:
        st.markdown("### 채팅 목록")

        if st.button("새로운 채팅 시작하기", use_container_width=True):
            new_session_id = generate_chat_session_id()
            st.session_state.current_session_id = new_session_id
            st.session_state.chat_sessions[new_session_id] = ChatSession(
                title="새로운 채팅",
                messages=[],
                thread_id=f"thread_{new_session_id}",
            )
            st.rerun()

        st.divider()

        if st.session_state.chat_sessions:
            for session_id, session_data in st.session_state.chat_sessions.items():
                # 현재 활성 세션 표시
                if_current = session_id == st.session_state.current_session_id
                button_style = "➡ " if if_current else ""

                if st.button(
                    f"{button_style}{session_data.title}",
                    key=f"chat_{session_id}",
                    use_container_width=True,
                ):
                    st.session_state.current_session_id = session_id
                    st.rerun()

        else:
            st.markdown("_아직 채팅이 없습니다._")


def render_chat_messages():
    """현재 세션의 채팅 메시지들을 렌더링합니다."""
    chat_container = st.container()
    with chat_container:
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

        if (
            st.session_state.current_session_id
            and st.session_state.current_session_id in st.session_state.chat_sessions
        ):
            current_session: ChatSession = st.session_state.chat_sessions[
                st.session_state.current_session_id
            ]
            for message in current_session.messages:
                with st.chat_message(message.role):
                    st.write(message.content)


def render_case_style_selector():
    """케이스 스타일 선택기를 렌더링합니다."""
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


def render_input_container():
    """입력 컨테이너를 렌더링합니다."""
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 6])

    with col1:
        render_case_style_selector()

    with col2:
        user_input = st.chat_input("단어 또는 텍스트를 입력하세요.")

    st.markdown("</div>", unsafe_allow_html=True)
    
    return user_input


def render_usage_guide():
    """사용법 가이드를 렌더링합니다."""
    st.markdown(
        """
### 💡 Variable Maker 사용법

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
