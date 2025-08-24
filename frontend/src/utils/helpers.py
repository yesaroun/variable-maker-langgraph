import time
import uuid
import streamlit as st

from models.chat_models import CaseStyle


def get_chat_title(first_message: str, max_length: int = 30) -> str:
    """첫 번째 메시지에서 채팅 제목을 생성합니다."""
    if len(first_message) <= max_length:
        return first_message
    return first_message[:max_length] + "..."


def _get_user_session_id() -> str:
    """사용자별 고유 세션 ID를 반환합니다."""
    if "user_session_id" not in st.session_state:
        st.session_state.user_session_id = str(uuid.uuid4())
    return st.session_state.user_session_id


def generate_chat_session_id() -> str:
    """채팅 세션을 위한 고유 ID를 생성합니다."""
    user_id = _get_user_session_id()
    timestamp = int(time.time())
    chat_uuid = str(uuid.uuid4())[:8]  # 짧은 UUID 사용
    return f"{user_id[:8]}_{timestamp}_{chat_uuid}"


def init_session_state():
    """Streamlit 세션 상태를 초기화합니다."""
    if "app" not in st.session_state:
        st.session_state.app = True
        st.session_state.chat_sessions = {}  # {session_id: ChatSession}
        st.session_state.current_session_id = None
        st.session_state.case_style = CaseStyle.CAMEL_CASE
