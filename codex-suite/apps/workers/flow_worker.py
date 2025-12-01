# apps/workers/flow_worker.py
import json
import time
from datetime import datetime

from core.flows import list_flows, log_dispatch
from core.ledger import append_entry
from core.settings import REDIS_URL


def run_publish_invocation(cfg):
    append_entry(
        "invocations.json",
        "invocations",
        {"role": cfg.get("role", "Custodian"), "text": cfg.get("text", "")},
    )


def run_publish_ledger(cfg):
    append_entry(
        "ledger.json",
        "entries",
        {"role": "Dispatch", "proclamation": cfg.get("proclamation", "")},
    )


def run_email(cfg):
    # Stub: write to ledger instead of sending email
    append_entry(
        "ledger.json",
        "entries",
        {"role": "Email", "proclamation": f"To {cfg['to']}: {cfg['subject']}"},
    )


def should_run_cron(expr, now):
    # Minimal cron: "0 6 * * *" runs when hour==6 and minute==0
    parts = expr.split()
    return now.minute == int(parts[0]) and now.hour == int(parts[1])


def tick():
    flows = list_flows()
    now = datetime.now()

    # Check Great Year cosmic invocations
    from core.scheduler import check_great_year

    check_great_year()

    for f in flows:
        ran = False
        for n in f["nodes"]:
            if n["node"].startswith("Cron"):
                if should_run_cron(n["config"]["expr"], now):
                    ran = True
            elif n["node"] == "PublishInvocation":
                run_publish_invocation(n["config"])
            elif n["node"] == "PublishLedger":
                run_publish_ledger(n["config"])
            elif n["node"] == "Email":
                run_email(n["config"])
        if ran:
            log_dispatch(f["id"], "OK", f"Ran at {now.isoformat()}")


if __name__ == "__main__":
    while True:
        tick()
        time.sleep(60)  # check every minute
