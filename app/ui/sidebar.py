import streamlit as st


def render_sidebar() -> None:
    st.header("Session")
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        if "agent" in st.session_state:
            st.session_state.agent.clear_history()
        st.rerun()
