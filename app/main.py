import streamlit as st

from ui.tabs.add import render_add_tab
from ui.tabs.chat import render_chat_tab
from ui.tabs.edit import render_edit_tab
from ui.tabs.reports import render_reports_tab
from ui.sidebar import render_sidebar

st.set_page_config(page_title="Betr Eats", page_icon="🥗", layout="centered")

st.title("Betr Eats")
st.caption("Log meals, track calories, and stay on top of your goals.")

tab1, tab2, tab3, tab4 = st.tabs(["Chat", "Add", "Edit", "Reports"])

with tab1:
    render_chat_tab()

with tab2:
    render_add_tab()

with tab3:
    render_edit_tab()

with tab4:
    render_reports_tab()

with st.sidebar:
    render_sidebar()
