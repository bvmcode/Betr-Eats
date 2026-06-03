from datetime import date, datetime

import streamlit as st

from ui.constants import DATE_INPUT_FORMAT, RECORD_TYPES


def record_filters(key_prefix: str) -> tuple[str, date]:
    filter_col, date_col = st.columns(2)
    with filter_col:
        record_type = st.selectbox(
            "Record type",
            RECORD_TYPES,
            key=f"{key_prefix}_record_type",
        )
    with date_col:
        selected_date = st.date_input(
            "Date",
            value=datetime.today().date(),
            format=DATE_INPUT_FORMAT,
            key=f"{key_prefix}_date",
        )
    return record_type, selected_date


def format_date_label(selected_date: date) -> str:
    return selected_date.strftime("%b %d, %Y")


def format_date_str(selected_date: date) -> str:
    return selected_date.strftime("%Y-%m-%d")
