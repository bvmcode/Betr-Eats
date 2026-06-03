import streamlit as st

from betr_eats.db.conn import Connection
from ui.filters import record_filters
from ui.records import exercises, goals, meals, weight

ADD_HANDLERS = {
    "Meals": meals.render_add_form,
    "Exercises": exercises.render_add_form,
    "Weight": weight.render_add_form,
    "Goals": goals.render_add_form,
}


def render_add_tab() -> None:
    record_type, selected_date = record_filters("add")
    conn = Connection()

    with st.container(border=True):
        ADD_HANDLERS[record_type](conn, selected_date)
