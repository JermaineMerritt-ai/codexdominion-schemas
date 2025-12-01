#!/usr/bin/env python3.11
import argparse
import json
import time
from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram, push_to_gateway

def load_snapshot(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def main():
    parser = argparse.ArgumentParser(description="Export compliance metrics to Pushgateway")
    parser.add_argument("--pushgateway", required=True, help="Pushgateway URL (e.g., http://pushgateway:9091)")
    parser.add_argument("--run-id", required=True, help="Unique run ID (e.g., GitHub run_id)")
    parser.add_argument("--snapshot", default="observability/metrics_snapshot.json", help="Optional JSON metrics snapshot path")
    args = parser.parse_args()

    snap = load_snapshot(args.snapshot)
    reg = CollectorRegistry()

    # Fact-check metrics
    fc_total = Counter("markets_fact_checks_total", "Total fact-check runs", registry=reg)
    fc_sources = Counter("markets_online_sources_checked_total", "Online sources checked", registry=reg)
    fc_failures = Counter("markets_online_failures_total", "Online source failures", registry=reg)
    fc_success_ratio = Gauge("markets_fact_checks_success_ratio", "Fact-check success ratio", registry=reg)
    api_latency = Histogram("markets_api_latency_seconds", "API latency seconds", registry=reg, buckets=[0.1, 0.3, 0.5, 1, 2, 5])

    # Drift metrics
    drift_checks = Counter("markets_drift_checks_total", "Total drift checks", registry=reg)
    drift_detected = Counter("markets_drift_detected_total", "Total drift detections", registry=reg)
    drift_open = Gauge("markets_drift_items_open", "Open drift items", registry=reg)
    drift_abs = Histogram("markets_drift_abs_change_bucket", "Absolute change in drift values", registry=reg, buckets=[0.01, 0.05, 0.1, 0.5, 1, 5, 10])

    # Avatar governance
    prompt_decisions = Counter("prompt_filter_decision_total", "Prompt filter decisions", ["decision"], registry=reg)
    watermark_applied = Counter("watermark_applied_total", "Watermarks applied", ["type"], registry=reg)
    watermark_failed = Counter("watermark_failed_total", "Watermark failures", registry=reg)
    consent_events = Counter("consent_events_total", "Consent events", ["event"], registry=reg)
    consent_active = Gauge("consent_subjects_active", "Active consent subjects", registry=reg)
    policy_violations = Counter("policy_violation_attempts_total", "Policy violation attempts", registry=reg)

    # Archives & provenance
    archives_total = Counter("compliance_archives_total", "Monthly compliance archives", registry=reg)
    last_archive_ts = Gauge("last_archive_timestamp", "Last archive timestamp (unix)", registry=reg)
    audit_entries = Counter("audit_log_entries_total", "Audit log entries", registry=reg)
    drift_issues_open = Counter("drift_issues_open_total", "Open drift issues", registry=reg)

    # Apply snapshot values with sane defaults
    fc_total.inc(snap.get("markets_fact_checks_total", 0))
    fc_sources.inc(snap.get("markets_online_sources_checked_total", 0))
    fc_failures.inc(snap.get("markets_online_failures_total", 0))
    fc_success_ratio.set(snap.get("markets_fact_checks_success_ratio", 1.0))
    api_latency.observe(snap.get("markets_api_latency_seconds", 0.3))

    drift_checks.inc(snap.get("markets_drift_checks_total", 0))
    drift_detected.inc(snap.get("markets_drift_detected_total", 0))
    drift_open.set(snap.get("markets_drift_items_open", 0))
    drift_abs.observe(snap.get("markets_drift_abs_change", 0.01))

    prompt_decisions.labels("allow").inc(snap.get("prompt_allow", 0))
    prompt_decisions.labels("block").inc(snap.get("prompt_block", 0))
    prompt_decisions.labels("review").inc(snap.get("prompt_review", 0))

    watermark_applied.labels("visual").inc(snap.get("watermark_visual_applied", 0))
    watermark_applied.labels("audio").inc(snap.get("watermark_audio_applied", 0))
    watermark_failed.inc(snap.get("watermark_failed_total", 0))

    consent_events.labels("grant").inc(snap.get("consent_grant", 0))
    consent_events.labels("revoke").inc(snap.get("consent_revoke", 0))
    consent_events.labels("update").inc(snap.get("consent_update", 0))
    consent_active.set(snap.get("consent_subjects_active", 1))
    policy_violations.inc(snap.get("policy_violation_attempts_total", 0))

    archives_total.inc(snap.get("compliance_archives_total", 0))
    last_archive_ts.set(snap.get("last_archive_timestamp", time.time()))
    audit_entries.inc(snap.get("audit_log_entries_total", 0))
    drift_issues_open.inc(snap.get("drift_issues_open_total", 0))

    job = "compliance_archiver"
    instance = args.run_id
    push_to_gateway(args.pushgateway, job=job, registry=reg, grouping_key={"instance": instance})
    print(f"Pushed metrics to {args.pushgateway} for job={job} instance={instance}")

if __name__ == "__main__":
    main()
