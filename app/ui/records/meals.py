from datetime import date

import streamlit as st

from betr_eats.db.conn import Connection
from betr_eats.db.meals import Meals
from ui.constants import MEAL_TYPES
from ui.widgets import record_card_header, show_record_list_header


def _meal_type_index(meal_type: str) -> int:
    if meal_type in MEAL_TYPES:
        return MEAL_TYPES.index(meal_type)
    return len(MEAL_TYPES) - 1


def _meal_form_fields(
    description: str | None = None,
    meal_type_index: int = 0,
    calories: int = 0,
) -> tuple[str, str, int]:
    desc_kwargs = {"value": description} if description is not None else {}
    meal_description = st.text_input("Description", **desc_kwargs)
    type_col, cal_col = st.columns(2)
    with type_col:
        meal_type = st.selectbox("Type", MEAL_TYPES, index=meal_type_index)
    with cal_col:
        cal_kwargs = {"value": calories} if description is not None else {}
        calorie_count = st.number_input("Calories", min_value=0, step=1, **cal_kwargs)
    return meal_description, meal_type, int(calorie_count)


def render_add_form(conn: Connection, add_date: date) -> None:
    with st.form("add_meal_form"):
        meal_description, meal_type, calorie_count = _meal_form_fields()
        if st.form_submit_button("Add meal", use_container_width=True):
            if not meal_description.strip():
                st.error("Description is required.")
            else:
                try:
                    meal = Meals(
                        meal_date=add_date,
                        meal_type=meal_type,
                        meal_description=meal_description.strip(),
                        calorie_count=calorie_count,
                    )
                    meal.insert(conn)
                    st.success("Meal added.")
                except ValueError as exc:
                    st.error(str(exc))


def render_edit_list(conn: Connection, date_str: str, date_label: str) -> None:
    meals = Meals.get_meal_by_date(conn, date_str)
    if not show_record_list_header(
        len(meals),
        "meal",
        "meals",
        date_label,
        f"No meals logged for {date_label}.",
    ):
        return

    for meal in meals:
        with st.container(border=True):
            record_card_header(
                f"**{meal.meal_type.title()}** · {meal.calorie_count} cal",
                f"delete_meal_{meal.id}",
                lambda meal_id=meal.id: Meals.delete_meal(conn, meal_id),
            )
            with st.form(key=f"meal_form_{meal.id}", border=False):
                meal_description, meal_type, calorie_count = _meal_form_fields(
                    description=meal.meal_description,
                    meal_type_index=_meal_type_index(meal.meal_type),
                    calories=meal.calorie_count,
                )
                if st.form_submit_button("Save changes", use_container_width=True):
                    Meals.update_meal(
                        conn,
                        meal.id,
                        calorie_count,
                        meal_description,
                        meal_type,
                        date_str,
                    )
                    st.rerun()
