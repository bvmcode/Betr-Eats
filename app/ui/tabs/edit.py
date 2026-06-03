from betr_eats.db.conn import Connection
from ui.filters import format_date_label, format_date_str, record_filters
from ui.records import exercises, goals, meals, weight

EDIT_HANDLERS = {
    "Meals": meals.render_edit_list,
    "Exercises": exercises.render_edit_list,
    "Weight": weight.render_edit_list,
    "Goals": goals.render_edit_list,
}


def render_edit_tab() -> None:
    record_type, selected_date = record_filters("edit")
    conn = Connection()
    date_str = format_date_str(selected_date)
    date_label = format_date_label(selected_date)
    EDIT_HANDLERS[record_type](conn, date_str, date_label)
