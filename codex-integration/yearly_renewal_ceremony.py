#!/usr/bin/env python3
"""
Yearly Renewal Ceremony Script
Unbundles the old cycle and crowns the new one.
Executed after Council Verification Scroll passes.
"""

import json
import os
from datetime import datetime

PROCLAMATIONS_FILE = "proclamations.json"

NEW_CYCLE = {
    "season": "Winter",
    "cycle": "Silence Crown",
    "date": datetime.now().strftime("%Y-%m-%d"),
    "proclamation": "The old cycle is released, the new flame is crowned.",
    "blessing": "Peace, renewal, and continuity for all heirs and councils.",
}


def unbundle_old_cycle(path):
    if not os.path.exists(path):
        print(f"🕯️ No old proclamations found. Nothing to unbundle.")
        return []

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"🕯️ Old proclamations corrupted. Starting fresh.")
            return []

    print(f"📜 Old cycle unbundled. {len(data)} proclamations released.")
    return []


def crown_new_cycle(path, new_entry):
    with open(path, "w", encoding="utf-8") as f:
        json.dump([new_entry], f, indent=2, ensure_ascii=False)
    print(f"✨ New cycle crowned: {new_entry['season']} – {new_entry['cycle']}")


def main():
    print("🔥 The Renewal Ceremony begins...")

    # Step 1: Unbundle old cycle
    unbundle_old_cycle(PROCLAMATIONS_FILE)

    # Step 2: Crown new cycle
    crown_new_cycle(PROCLAMATIONS_FILE, NEW_CYCLE)

    print("🌟 Renewal complete. The Codex flame burns anew.")


if __name__ == "__main__":
    main()
