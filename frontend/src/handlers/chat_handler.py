import streamlit as st

from utils.helpers import generate_chat_session_id, get_chat_title
from models.chat_models import ChatSession
from utils.api_client import VariableMakerAPIClient


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

    try:
        api_client = VariableMakerAPIClient()
        result = api_client.process_variable_request(
            user_input=user_input,
            case_style=st.session_state.case_style,
            thread_id=current_session.thread_id,
        )

        if result:
            if "response" in result:
                current_session.add_message(
                    role="assistant", content=result["response"]
                )
            else:
                current_session.add_message(role="assistant", content=str(result))

            if "case_style" in result:
                st.session_state.case_style = result["case_style"]
        else:
            current_session.add_message(
                role="assistant", content="응답을 받지 못했습니다."
            )

    except Exception as e:
        current_session.add_message(
            role="assistant", content=f"오류가 발생했습니다: {e}"
        )

    st.session_state.chat_sessions[st.session_state.current_session_id] = (
        current_session
    )
    st.rerun()
