import streamlit as st

from models.chat_models import ChatSession
from utils.helpers import generate_chat_session_id


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
