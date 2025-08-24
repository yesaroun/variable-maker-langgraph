import streamlit as st

from models.chat_models import get_case_style_options


def render_case_style_selector():
    """케이스 스타일 선택 컴포넌트를 렌더링합니다."""
    options = get_case_style_options()
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
    """입력 컨테이너를 렌러딩합니다."""
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 6])

    with col1:
        render_case_style_selector()

    with col2:
        user_input = st.chat_input("단어 또는 텍스트를 입력하세요.")

    st.markdown("</div>", unsafe_allow_html=True)

    return user_input
