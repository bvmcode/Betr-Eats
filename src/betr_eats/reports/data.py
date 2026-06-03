from datetime import date

from betr_eats.db.conn import Connection
from betr_eats.db.exercise import Exercise
from betr_eats.db.goals import Goals
from betr_eats.db.meals import Meals
from betr_eats.db.weight import Weight


def _records_to_dicts(records):
    return [record.to_dict() for record in records]


def fetch_report_data(conn: Connection, start_date: date, end_date: date) -> dict:
    meals = (
        conn.session.query(Meals)
        .filter(Meals.meal_date >= start_date, Meals.meal_date <= end_date)
        .order_by(Meals.meal_date)
        .all()
    )
    exercises = (
        conn.session.query(Exercise)
        .filter(
            Exercise.exercise_date >= start_date,
            Exercise.exercise_date <= end_date,
        )
        .order_by(Exercise.exercise_date)
        .all()
    )
    weights = (
        conn.session.query(Weight)
        .filter(Weight.weight_date >= start_date, Weight.weight_date <= end_date)
        .order_by(Weight.weight_date)
        .all()
    )
    goals = (
        conn.session.query(Goals)
        .filter(Goals.goal_date >= start_date, Goals.goal_date <= end_date)
        .order_by(Goals.goal_date)
        .all()
    )
    return {
        "meals": _records_to_dicts(meals),
        "exercises": _records_to_dicts(exercises),
        "weights": _records_to_dicts(weights),
        "goals": _records_to_dicts(goals),
    }
