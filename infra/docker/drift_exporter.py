#!/usr/bin/env python3.11
from prometheus_client import start_http_server, Gauge
import time
import verify_drift

drift_flags = Gauge(
    'drift_events_detected',
    'Number of drift events detected'
)


def run() -> None:
    start_http_server(8001)
    while True:
        drift = verify_drift.check_drift()
        drift_flags.set(len(drift))
        time.sleep(60)


if __name__ == "__main__":
    run()
