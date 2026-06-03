import os
from collections.abc import Callable
from datetime import datetime

import streamlit as st

from betr_eats.db.conn import Connection
from betr_eats.helpers.model import Model
from betr_eats.reports import month, six_month, three_month, today, week, year

REPORT_OPTIONS: dict[str, Callable] = {
    "Today": today.generate,
    "Past week": week.generate,
    "Past month": month.generate,
    "Past 3 months": three_month.generate,
    "Past 6 months": six_month.generate,
    "Past year": year.generate,
}


def _get_model() -> Model | None:
    model_id = os.getenv("HF_MODEL")
    if not model_id:
        st.error("HF_MODEL is not set. Add it to your environment or `.env` file.")
        return None
    return Model(model_id)


def render_reports_tab() -> None:
    filter_col, date_col = st.columns(2)
    with filter_col:
        period = st.selectbox("Time period", list(REPORT_OPTIONS.keys()))
    with date_col:
        reference_date = st.date_input(
            "Through date",
            value=datetime.today().date(),
            format="MM.DD.YYYY",
        )

    if st.button("Generate summary", use_container_width=True):
        model = _get_model()
        if model is None:
            return

        conn = Connection()
        with st.spinner("Generating summary..."):
            try:
                summary = REPORT_OPTIONS[period](conn, model, reference_date)
                st.markdown(summary)
            except Exception as exc:
                st.error(f"Failed to generate summary: {exc}")
