import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from ..core.models import ChatSession
from ..utils.helpers import get_chat_title, generate_chat_session_id


def handle_user_input(user_input: str):
    """사용자 입력을 처리하고 AI 응답을 생성합니다."""
    if not st.session_state.current_session_id:
        new_session_id = generate_chat_session_id()
        st.session_state.current_session_id = new_session_id
        st.session_state.chat_sessions[new_session_id] = ChatSession(
            title=get_chat_title(user_input),
            messages=[],
            thread_id=f"thread_{new_session_id}",
        )

    current_session: ChatSession = st.session_state.chat_sessions[
        st.session_state.current_session_id
    ]

    if not current_session.messages:
        current_session.title = get_chat_title(user_input)

    current_session.add_message(role="user", content=user_input)

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
    config = {"configurable": {"thread_id": current_session.thread_id}}

    try:
        result = st.session_state.app.invoke(initial_state, config)

        if "selected_case_style" in result and result["selected_case_style"]:
            st.session_state.case_style = result["selected_case_style"]

        ai_msg = next(
            (m for m in reversed(result["messages"]) if isinstance(m, AIMessage)),
            None,
        )
        if ai_msg:
            current_session.add_message(role="assistant", content=ai_msg.content)

    except Exception as e:
        current_session.add_message(
            role="assistant", content=f"오류가 발생했습니다: {e}"
        )

    st.rerun()
