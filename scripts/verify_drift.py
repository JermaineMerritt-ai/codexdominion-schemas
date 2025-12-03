#!/usr/bin/env python3.11
import argparse
import time
import json
from prometheus_client import Counter, Gauge, Histogram, start_http_server

markets_drift_checks_total = Counter(
    "markets_drift_checks_total",
    "Total drift checks"
)
markets_drift_detected_total = Counter(
    "markets_drift_detected_total",
    "Total drift detections"
)
markets_drift_items_open = Gauge(
    "markets_drift_items_open",
    "Open drift items"
)
markets_drift_abs_change_bucket = Histogram(
    "markets_drift_abs_change_bucket",
    "Absolute change in drift",
    buckets=[0.01, 0.05, 0.1, 0.5, 1, 5, 10]
)
markets_api_latency_seconds = Histogram(
    "markets_api_latency_seconds",
    "API latency seconds",
    buckets=[0.1, 0.3, 0.5, 1, 2, 5]
)

def fetch_value(ticker, source):
    t0 = time.time()
    # Placeholder: replace with real API call
    value = 100.2  # mock
    markets_api_latency_seconds.observe(time.time() - t0)
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--online", action="store_true", help="Enable live drift validation"
    )
    parser.add_argument(
        "--sources", type=int, default=2, help="Minimum sources to confirm drift"
    )
    parser.add_argument(
        "--tolerance", type=float, default=0.5, help="Drift tolerance threshold"
    )
    parser.add_argument(
        "--serve-metrics", action="store_true", help="Expose metrics on :8001"
    )
    args = parser.parse_args()

    if args.serve_metrics:
        start_http_server(8001)

    markets_drift_checks_total.inc()

    # Load facts file, create empty list if missing
    try:
        with open("verified_facts.json", "r", encoding="utf-8") as f:
            facts = json.load(f)
    except FileNotFoundError:
        print("⚠️  verified_facts.json not found, creating empty file")
        facts = []
        with open("verified_facts.json", "w", encoding="utf-8") as f:
            json.dump(facts, f, indent=2)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing verified_facts.json: {e}")
        facts = []

    if not facts:
        print("✅ No facts to verify, drift check passed")
        markets_drift_items_open.set(0)
        return

    open_items = 0
    for fact in facts:
        expected = float(fact["value"])
        ticker = fact.get("ticker", "")
        if args.online:
            sources = ["primary_market_api", "backup_market_api"]
            observed = [fetch_value(ticker, s) for s in sources]
            # Confirm drift only if multiple sources exceed tolerance
            diffs = [abs(v - expected) for v in observed]
            for d in diffs:
                markets_drift_abs_change_bucket.observe(d)
            confirm = sum(d > args.tolerance for d in diffs) >= min(args.sources, len(diffs))
            if confirm:
                markets_drift_detected_total.inc()
                open_items += 1
        else:
            # Offline: no change
            pass

    markets_drift_items_open.set(open_items)


if __name__ == "__main__":
    main()
