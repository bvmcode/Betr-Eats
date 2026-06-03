from datetime import date

from betr_eats.db.conn import Connection
from betr_eats.helpers.model import Model
from betr_eats.reports.summary import generate_summary

PERIOD_LABEL = "Past 3 months"
PERIOD_DAYS = 90


def generate(
    conn: Connection,
    model: Model,
    reference_date: date | None = None,
) -> str:
    return generate_summary(conn, model, PERIOD_LABEL, PERIOD_DAYS, reference_date)
