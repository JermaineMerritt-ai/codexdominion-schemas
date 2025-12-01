#!/usr/bin/env python3.11
import logging
import time
from prometheus_client import start_http_server, Gauge

try:
    import fact_check
except ImportError:
    fact_check = None

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Metric definitions
fact_errors = Gauge('fact_check_errors', 'Number of fact-check errors detected')

def run():
    if not fact_check:
        logging.error("fact_check module not found. Exiting.")
        return
    start_http_server(8000)
    logging.info("Fact-check Prometheus exporter started on port 8000.")
    while True:
        try:
            errors = fact_check.main(return_errors=True)
            fact_errors.set(len(errors))
            logging.info(f"Fact-check errors: {len(errors)}")
        except Exception as e:
            logging.error(f"Error running fact_check: {e}")
            fact_errors.set(-1)
        time.sleep(30)

if __name__ == "__main__":
    run()
