# core/scheduler.py
from datetime import datetime

from core.ledger import append_entry

GREAT_YEAR_DATES = [(3, 20), (6, 21), (9, 22), (12, 21)]


def check_great_year():
    now = datetime.now()
    if (now.month, now.day) in GREAT_YEAR_DATES and now.hour == 6 and now.minute == 0:
        append_entry(
            "invocations.json",
            "invocations",
            {
                "role": "Cosmos",
                "text": "Great Year Invocation: We shine across the turning heavens.",
            },
        )
