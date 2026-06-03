import json
from datetime import date


def build_summary_prompt(
    period_label: str,
    start_date: date,
    end_date: date,
    data: dict,
) -> str:
    data_json = json.dumps(data, indent=2, default=str)
    return f"""You are a health and nutrition coach writing a progress summary for Betr Eats.

Time period: {period_label} ({start_date.isoformat()} to {end_date.isoformat()})

Logged data (JSON):
{data_json}

Write a presentable markdown summary that covers:
- Eating habits and calorie intake patterns
- Exercise activity and calories burned
- Weight trends and progress toward goals
- Encouraging, actionable takeaways

Use markdown headers, bullet points, and **bold** for key numbers.
If there is little or no data, say so clearly and suggest logging more consistently.
Do not invent data that is not present in the JSON."""
