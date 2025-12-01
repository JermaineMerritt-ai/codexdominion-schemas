#!/usr/bin/env python3
"""
Simple Dawn Dispatch Integration
===============================

A simple version that integrates with the existing Codex ledger system
while maintaining the original functionality you requested.

This script provides the basic dawn dispatch functionality while
working seamlessly with your existing Codex Dominion infrastructure.
"""

import datetime
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

# Configuration paths
LEDGER_PATH = "codex_ledger.json"
DATA_DIR = Path("data")
PROCLAMATION_PATH = DATA_DIR / "proclamation.md"


def ensure_data_directory():
    """Ensure the data directory exists."""
    DATA_DIR.mkdir(exist_ok=True)


def load_ledger() -> Dict[str, Any]:
    """Load the existing Codex ledger."""
    if os.path.exists(LEDGER_PATH):
        try:
            with open(LEDGER_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            print("⚠️  Warning: Could not load existing ledger")

    # Return minimal structure if ledger doesn't exist
    return {"cycles": [], "proclamations": [], "dawn_dispatches": []}


def save_ledger(ledger: Dict[str, Any]) -> None:
    """Save the ledger back to file."""
    # Update metadata if it exists
    if "meta" in ledger:
        ledger["meta"]["last_updated"] = datetime.datetime.now().isoformat() + "Z"

    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)


def write_proclamation(text: str) -> None:
    """Write proclamation to markdown file."""
    ensure_data_directory()

    timestamp = datetime.date.today().strftime("%Y-%m-%d")

    with open(PROCLAMATION_PATH, "a", encoding="utf-8") as f:
        f.write(f"\n## {timestamp}\n{text}\n")


def dawn_dispatch(custom_proclamation: Optional[str] = None) -> Dict[str, Any]:
    """
    Execute a simple dawn dispatch ritual that integrates with Codex ledger.

    Args:
        custom_proclamation: Optional custom proclamation text

    Returns:
        Dictionary with dispatch results
    """
    print("🌅 Dawn Dispatch initiated...")

    # Generate basic information
    today = datetime.date.today().isoformat()
    timestamp = datetime.datetime.now().isoformat() + "Z"

    # Create proclamation
    if custom_proclamation:
        proclamation = custom_proclamation
    else:
        proclamation = f"Thus the flame endures on {today}."

    print(f"📜 Proclamation: {proclamation}")

    # Load existing ledger
    ledger = load_ledger()

    # Create new cycle entry
    cycle_id = len(ledger.get("cycles", [])) + 1
    cycle_entry = {
        "id": cycle_id,
        "kind": "dawn_dispatch",
        "started_at": today,
        "completed_at": timestamp,
        "proclamation": proclamation,
        "status": "completed",
    }

    # Add to cycles
    if "cycles" not in ledger:
        ledger["cycles"] = []
    ledger["cycles"].append(cycle_entry)

    # Add to dawn dispatches if the structure exists
    if "dawn_dispatches" not in ledger:
        ledger["dawn_dispatches"] = []

    dawn_entry = {
        "date": today,
        "timestamp": timestamp,
        "proclamation": proclamation,
        "cycle_id": cycle_id,
    }
    ledger["dawn_dispatches"].append(dawn_entry)

    # Update heartbeat if it exists
    if "heartbeat" in ledger:
        ledger["heartbeat"]["last_dispatch"] = timestamp
        ledger["heartbeat"]["status"] = "luminous"

    # Save ledger and write proclamation
    save_ledger(ledger)
    write_proclamation(proclamation)

    result = {
        "success": True,
        "date": today,
        "timestamp": timestamp,
        "proclamation": proclamation,
        "cycle_id": cycle_id,
        "files_updated": [LEDGER_PATH, str(PROCLAMATION_PATH)],
    }

    print(f"✅ Dawn Dispatch complete: {proclamation}")
    return result


def get_dawn_status() -> Dict[str, Any]:
    """Get current dawn dispatch status."""
    today = datetime.date.today().isoformat()
    ledger = load_ledger()

    # Check if dispatch already done today
    today_dispatches = []
    if "dawn_dispatches" in ledger:
        today_dispatches = [
            d for d in ledger["dawn_dispatches"] if d.get("date") == today
        ]

    return {
        "date": today,
        "dispatched_today": len(today_dispatches) > 0,
        "today_dispatches": today_dispatches,
        "total_dispatches": len(ledger.get("dawn_dispatches", [])),
        "total_cycles": len(ledger.get("cycles", [])),
        "flame_status": "luminous" if today_dispatches else "awaiting",
    }


def main():
    """Command line interface."""
    import sys

    if len(sys.argv) > 1:
        action = sys.argv[1].lower()

        if action == "status":
            status = get_dawn_status()
            print(f"🌅 Dawn Status:")
            print(f"   Date: {status['date']}")
            print(
                f"   Dispatched Today: {'Yes' if status['dispatched_today'] else 'No'}"
            )
            print(f"   Total Dispatches: {status['total_dispatches']}")
            print(f"   Flame Status: {status['flame_status']}")

        elif action == "dispatch":
            custom_text = sys.argv[2] if len(sys.argv) > 2 else None
            result = dawn_dispatch(custom_text)
            print(f"📋 Result: {json.dumps(result, indent=2)}")

        else:
            print(
                "Usage: python dawn_dispatch_simple.py [dispatch|status] [custom_proclamation]"
            )
    else:
        # Default: run dawn dispatch
        dawn_dispatch()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🌅 Dawn Dispatch interrupted")
    except Exception as e:
        print(f"❌ Error: {e}")
