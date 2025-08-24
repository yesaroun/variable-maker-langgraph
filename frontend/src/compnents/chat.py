import streamlit as st
from models.chat_models import ChatSession


def render_chat_messages():
    """현재 세션의 채팅 메시지들을 렌더링합니다."""
    chat_container = st.container()
    with chat_container:
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
