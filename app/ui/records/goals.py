from datetime import date

import streamlit as st

from betr_eats.db.conn import Connection
from betr_eats.db.goals import Goals
from ui.widgets import record_card_header, show_record_list_header


def _goal_form_field(value: float | None = None) -> float:
    kwargs = {"value": value} if value is not None else {}
    return st.number_input(
        "Goal weight (lbs)",
        min_value=0.0,
        step=0.1,
        format="%.1f",
        **kwargs,
    )


def render_add_form(conn: Connection, add_date: date) -> None:
    with st.form("add_goal_form"):
        goal_value = _goal_form_field()
        if st.form_submit_button("Add goal", use_container_width=True):
            goal = Goals(goal_date=add_date, goal_value=float(goal_value))
            goal.insert(conn)
            st.success("Goal added.")


def render_edit_list(conn: Connection, date_str: str, date_label: str) -> None:
    goals = Goals.get_goal_by_date(conn, date_str)
    if not show_record_list_header(
        len(goals),
        "goal",
        "goals",
        date_label,
        f"No goals set for {date_label}.",
    ):
        return

    for goal in goals:
        with st.container(border=True):
            record_card_header(
                f"**Goal: {goal.goal_value:.1f} lbs**",
                f"delete_goal_{goal.id}",
                lambda goal_id=goal.id: Goals.delete_goal(conn, goal_id),
            )
            with st.form(key=f"goal_form_{goal.id}", border=False):
                goal_value = _goal_form_field(value=float(goal.goal_value))
                if st.form_submit_button("Save changes", use_container_width=True):
                    Goals.update_goal(conn, goal.id, float(goal_value), date_str)
                    st.rerun()
