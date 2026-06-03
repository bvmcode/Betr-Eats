import asyncio
from datetime import date, timedelta

from betr_eats.db.conn import Connection
from betr_eats.helpers.model import Model
from betr_eats.reports.data import fetch_report_data
from betr_eats.reports.prompts import build_summary_prompt


def date_range(reference: date, days: int) -> tuple[date, date]:
    end = reference
    start = reference - timedelta(days=days - 1)
    return start, end


async def _generate_async(
    model: Model,
    period_label: str,
    start_date: date,
    end_date: date,
    data: dict,
) -> str:
    prompt = build_summary_prompt(period_label, start_date, end_date, data)
    return await model.generate_text(prompt)


def generate_summary(
    conn: Connection,
    model: Model,
    period_label: str,
    period_days: int,
    reference_date: date | None = None,
) -> str:
    reference = reference_date or date.today()
    start_date, end_date = date_range(reference, period_days)
    data = fetch_report_data(conn, start_date, end_date)
    return asyncio.run(
        _generate_async(model, period_label, start_date, end_date, data)
    )
