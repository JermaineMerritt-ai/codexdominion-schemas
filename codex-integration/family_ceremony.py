#!/usr/bin/env python3
"""
Family Ceremony Script
Allows heirs to add proclamations or blessings to the Codex
without needing technical knowledge.
"""

import json
import os
from datetime import datetime

PROCLAMATIONS_FILE = "proclamations.json"

REQUIRED_KEYS = ["season", "cycle", "date", "proclamation", "blessing"]


def load_proclamations(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("🕯️ Existing proclamations corrupted. Starting fresh.")
            return []


def save_proclamations(path, proclamations):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(proclamations, f, indent=2, ensure_ascii=False)


def main():
    print("📜 Family Ceremony begins. Heirs may inscribe a proclamation.")

    # Prompt heir for input
    season = input("Enter the season (Winter, Spring, Summer, Autumn): ").strip()
    cycle = input(
        "Enter the cycle name (e.g., Silence Crown, Renewal Proclamation): "
    ).strip()
    proclamation = input("Enter the proclamation text: ").strip()
    blessing = input("Enter the blessing text: ").strip()

    # Build entry
    entry = {
        "season": season,
        "cycle": cycle,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "proclamation": proclamation,
        "blessing": blessing,
    }

    # Load existing proclamations
    proclamations = load_proclamations(PROCLAMATIONS_FILE)

    # Append new entry
    proclamations.append(entry)
    save_proclamations(PROCLAMATIONS_FILE, proclamations)

    print("✨ Proclamation inscribed successfully!")
    print(f"Season: {season}, Cycle: {cycle}")
    print("🌟 The Codex flame is enriched by your words.")


if __name__ == "__main__":
    main()
