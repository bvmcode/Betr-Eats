from datetime import date

import streamlit as st

from betr_eats.db.conn import Connection
from betr_eats.db.weight import Weight
from ui.widgets import record_card_header, show_record_list_header


def _weight_form_field(value: float | None = None) -> float:
    kwargs = {"value": value} if value is not None else {}
    return st.number_input(
        "Weight (lbs)",
        min_value=0.0,
        step=0.1,
        format="%.1f",
        **kwargs,
    )


def render_add_form(conn: Connection, add_date: date) -> None:
    with st.form("add_weight_form"):
        weight_lbs = _weight_form_field()
        if st.form_submit_button("Add weight", use_container_width=True):
            weight = Weight(weight_date=add_date, weight_lbs=float(weight_lbs))
            result = weight.insert(conn)
            if result == "success":
                st.success("Weight added.")
            else:
                st.error(result)


def render_edit_list(conn: Connection, date_str: str, date_label: str) -> None:
    weights = Weight.get_weight_by_date(conn, date_str)
    if not show_record_list_header(
        len(weights),
        "weight record",
        "weight records",
        date_label,
        f"No weight logged for {date_label}.",
    ):
        return

    for weight in weights:
        with st.container(border=True):
            record_card_header(
                f"**{weight.weight_lbs:.1f} lbs**",
                f"delete_weight_{weight.id}",
                lambda weight_id=weight.id: Weight.delete_weight(conn, weight_id),
            )
            with st.form(key=f"weight_form_{weight.id}", border=False):
                weight_lbs = _weight_form_field(value=float(weight.weight_lbs))
                if st.form_submit_button("Save changes", use_container_width=True):
                    Weight.update_weight(conn, weight.id, float(weight_lbs), date_str)
                    st.rerun()
