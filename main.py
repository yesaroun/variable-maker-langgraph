import streamlit as st

from utils import init_session_state
from ui_components import (
    render_sidebar,
    render_chat_messages,
    render_input_container,
    render_usage_guide,
)
from chat_handler import handle_user_input

st.set_page_config(page_title="Variable Maker", layout="wide")


init_session_state()

# UI 렌더링
render_sidebar()

st.title("Variable Maker")

render_usage_guide()
render_chat_messages()
user_input = render_input_container()

# 사용자 입력 처리
if user_input:
    handle_user_input(user_input)
