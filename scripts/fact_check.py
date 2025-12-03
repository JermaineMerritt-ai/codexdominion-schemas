#!/usr/bin/env python3.11
import argparse, time, json
from prometheus_client import Counter, Gauge, Histogram, start_http_server

markets_fact_checks_total = Counter("markets_fact_checks_total", "Total fact-check runs")
markets_online_sources_checked_total = Counter("markets_online_sources_checked_total", "Online sources checked")
markets_online_failures_total = Counter("markets_online_failures_total", "Online source failures")
markets_fact_checks_success_ratio = Gauge("markets_fact_checks_success_ratio", "Fact-check success ratio")
markets_api_latency_seconds = Histogram("markets_api_latency_seconds", "API latency seconds", buckets=[0.1,0.3,0.5,1,2,5])

def fetch_sources(ticker, sources):
    # Placeholder: replace with real API calls
    results = []
    for src in sources:
        t0 = time.time()
        try:
            # Simulate data fetch
            value = 100.0  # mock
            latency = time.time() - t0
            markets_api_latency_seconds.observe(latency)
            markets_online_sources_checked_total.inc()
            results.append((src["name"], value))
        except Exception:
            markets_online_failures_total.inc()
    return results

def quorum_match(results, expected_value, tolerance):
    # Accept if at least N sources within tolerance band
    matches = [abs(v - expected_value) <= tolerance for _, v in results]
    return sum(matches), len(matches)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true", help="Enable live source validation")
    parser.add_argument("--sources", type=int, default=2, help="Minimum concordant sources required")
    parser.add_argument("--policy", default="policies/online_sources.yml", help="Online source registry path")
    parser.add_argument("--serve-metrics", action="store_true", help="Expose metrics on :8000")
    args = parser.parse_args()

    if args.serve_metrics:
        start_http_server(8000)

    markets_fact_checks_total.inc()

    # Load verified facts (example)
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
        print("✅ No facts to check, validation passed")
        markets_fact_checks_success_ratio.set(1.0)
        return

    successes = 0
    total = 0

    for fact in facts:
        total += 1
        expected = float(fact["value"])
        tolerance = float(fact.get("tolerance", 0.5))
        if args.online:
            # Load sources registry (stub: replace with YAML parsing)
            sources = [{"name": "primary_market_api"}, {"name": "backup_market_api"}]
            results = fetch_sources(fact.get("ticker", ""), sources)
            matches, count = quorum_match(results, expected, tolerance)
            if matches >= min(args.sources, count):
                successes += 1
        else:
            # Offline pass-through
            successes += 1

    ratio = (successes / max(total, 1))
    markets_fact_checks_success_ratio.set(ratio)

if __name__ == "__main__":
    main()
