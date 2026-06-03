from collections.abc import Callable

import streamlit as st


def record_card_header(title: str, delete_key: str, on_delete: Callable[[], None]) -> None:
    title_col, action_col = st.columns([5, 1])
    with title_col:
        st.markdown(title)
    with action_col:
        if st.button(
            "Delete",
            key=delete_key,
            type="secondary",
            use_container_width=True,
        ):
            on_delete()
            st.rerun()


def show_record_list_header(
    count: int,
    singular: str,
    plural: str,
    date_label: str,
    empty_message: str,
) -> bool:
    if count == 0:
        st.info(empty_message)
        return False
    noun = singular if count == 1 else plural
    st.caption(f"{count} {noun} on {date_label}")
    return True
