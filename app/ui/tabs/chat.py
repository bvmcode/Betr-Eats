import os

import streamlit as st

from betr_eats.agents.main_agent import MainAgent
from betr_eats.helpers.model import Model


def render_chat_tab() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "agent" not in st.session_state:
        model_id = os.getenv("HF_MODEL")
        if not model_id:
            st.error("HF_MODEL is not set. Add it to your environment or `.env` file.")
            st.stop()
        st.session_state.agent = MainAgent(Model(model_id))

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What did you eat today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.agent.run(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
