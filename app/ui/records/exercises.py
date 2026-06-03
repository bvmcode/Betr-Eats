from datetime import date

import streamlit as st

from betr_eats.db.conn import Connection
from betr_eats.db.exercise import Exercise
from ui.widgets import record_card_header, show_record_list_header


def _exercise_form_fields(
    description: str | None = None,
    minutes: int = 0,
    calories_burned: int = 0,
) -> tuple[str, int, int]:
    desc_kwargs = {"value": description} if description is not None else {}
    exercise_description = st.text_input("Description", **desc_kwargs)
    min_col, cal_col = st.columns(2)
    with min_col:
        min_kwargs = {"value": minutes} if description is not None else {}
        excercise_minutes = st.number_input(
            "Minutes", min_value=0, step=1, **min_kwargs
        )
    with cal_col:
        cal_kwargs = {"value": calories_burned} if description is not None else {}
        calories = st.number_input(
            "Calories burned", min_value=0, step=1, **cal_kwargs
        )
    return exercise_description, int(excercise_minutes), int(calories)


def render_add_form(conn: Connection, add_date: date) -> None:
    with st.form("add_exercise_form"):
        exercise_description, excercise_minutes, calories_burned = _exercise_form_fields()
        if st.form_submit_button("Add exercise", use_container_width=True):
            if not exercise_description.strip():
                st.error("Description is required.")
            else:
                exercise = Exercise(
                    exercise_date=add_date,
                    excercise_minutes=excercise_minutes,
                    exercise_description=exercise_description.strip(),
                    exercise_calories_burned=calories_burned,
                )
                exercise.insert(conn)
                st.success("Exercise added.")


def render_edit_list(conn: Connection, date_str: str, date_label: str) -> None:
    exercises = Exercise.get_exercise_by_date(conn, date_str)
    if not show_record_list_header(
        len(exercises),
        "exercise",
        "exercises",
        date_label,
        f"No exercises logged for {date_label}.",
    ):
        return

    for exercise in exercises:
        with st.container(border=True):
            record_card_header(
                f"**{exercise.excercise_minutes} min** · "
                f"{exercise.exercise_calories_burned} cal burned",
                f"delete_exercise_{exercise.id}",
                lambda exercise_id=exercise.id: Exercise.delete_exercise(
                    conn, exercise_id
                ),
            )
            with st.form(key=f"exercise_form_{exercise.id}", border=False):
                exercise_description, excercise_minutes, calories_burned = (
                    _exercise_form_fields(
                        description=exercise.exercise_description,
                        minutes=exercise.excercise_minutes,
                        calories_burned=exercise.exercise_calories_burned,
                    )
                )
                if st.form_submit_button("Save changes", use_container_width=True):
                    Exercise.update_exercise(
                        conn,
                        exercise.id,
                        excercise_minutes,
                        exercise_description,
                        calories_burned,
                        date_str,
                    )
                    st.rerun()
