import json
from datetime import datetime, date
from ddgs import DDGS
from agents import function_tool
from sqlalchemy import select
from sqlalchemy.types import Date
from betr_eats.db import Connection, Meals, Weight


@function_tool
def search_calorie_count(meal_description: str) -> str:
    """Search for calorie count of a meal."""
    results = DDGS().text(meal_description, max_results=5)
    return json.dumps(results)


@function_tool
def write_meal_log(meal_description: str, meal_type: str, calorie_count: int) -> str:
    """Write a meal log to the database. meal_type must be one of breakfast, lunch, dinner, snack, or other."""
    if meal_type.lower() not in ["breakfast", "lunch", "dinner", "snack", "other"]:
        return "Invalid meal type. Must be one of breakfast, lunch, dinner, snack, or other."
    conn = Connection()
    meal = Meals(
        meal_description=meal_description,
        meal_type=meal_type.lower(),
        calorie_count=calorie_count,
        meal_date=datetime.now().date(),
    )
    meal.insert(conn)
    conn.close()
    return "success"


@function_tool
def get_meal_log_for_day(meals_date: str) -> list[Meals]:
    """Get a meal log from the database using the date string in the format YYYY-MM-DD."""
    conn = Connection()
    try:
        meals = Meals.get_meal_by_date(conn, meals_date)
        data = [
            {
                "meal_date": meal.meal_date.strftime("%Y-%m-%d"),
                "meal_type": meal.meal_type,
                "meal_description": meal.meal_description,
                "meal_calorie_count": meal.calorie_count,
            }
            for meal in meals
        ]
        conn.close()
        return json.dumps(data, indent=4)
    except Exception as e:
        print(f"Error getting meal log for day: {e}")
        return "No meals found for the given date."


@function_tool
def write_weight_log(weight_lbs: float) -> str:
    """Write a weight log to the database."""
    try:
        conn = Connection()
        weight = Weight(
            weight_lbs=weight_lbs,
            weight_date=datetime.now().date(),
        )
        weight.insert(conn)
        conn.close()
        return "success"
    except Exception as e:
        print(f"Error writing weight log: {e}")
        return "Failed to write weight log."