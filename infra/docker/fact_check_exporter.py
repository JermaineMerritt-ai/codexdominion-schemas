#!/usr/bin/env python3.11
from prometheus_client import start_http_server, Gauge
import time
import fact_check

# Metric definitions

fact_errors = Gauge(
    'fact_check_errors',
    'Number of fact-check errors detected'
)

  
def run() -> None:
    start_http_server(8000)
    while True:
        errors = fact_check.main(return_errors=True)
        fact_errors.set(len(errors))
        time.sleep(30)


if __name__ == "__main__":
    run()
