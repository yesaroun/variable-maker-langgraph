import streamlit as st

from compnents.chat import render_chat_messages
from compnents.guide import render_usage_guide
from compnents.input import render_input_container
from compnents.sidebar import render_sidebar
from handlers.chat_handler import handle_user_input
from utils.helpers import init_session_state

st.set_page_config(page_title="Variable Maker", layout="wide")

init_session_state()

render_sidebar()

st.title("Variable Maker")

render_usage_guide()
render_chat_messages()
user_input = render_input_container()

if user_input:
    handle_user_input(user_input=user_input)
