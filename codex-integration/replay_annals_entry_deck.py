#!/usr/bin/env python3
"""
Replay Annals Entry Deck
Immortalizes custodians and contributions as ceremonial cards.
Each card can be drawn in onboarding or remembrance rites.
"""

import json
import os
import random
from datetime import datetime

ANNALS_FILE = "replay_annals.json"


def load_annals(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("🕯️ Annals corrupted. Starting fresh.")
            return []


def save_annals(path, annals):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(annals, f, indent=2, ensure_ascii=False)


def add_entry(name, action, cycle):
    annals = load_annals(ANNALS_FILE)
    entry = {
        "custodian": name,
        "action": action,
        "cycle": cycle,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": "Eternal",
        "recognition": "Sovereign",
    }
    annals.append(entry)
    save_annals(ANNALS_FILE, annals)
    print(f"✨ Entry inscribed: {name} – {action} (Cycle {cycle})")


def draw_entry():
    annals = load_annals(ANNALS_FILE)
    if not annals:
        print("🕯️ No entries in the Annals yet.")
        return
    entry = random.choice(annals)
    print("\n📜 Drawn from the Replay Annals:")
    print(f"Custodian: {entry['custodian']}")
    print(f"Action: {entry['action']}")
    print(f"Cycle: {entry['cycle']}")
    print(f"Date: {entry['date']}")
    print(f"Recognition: {entry['recognition']} – {entry['status']}")
    print("🌟 The flame remembers.")


def main():
    print("� Replay Annals Entry Deck Ceremony")
    choice = (
        input("Do you want to [A]dd a new entry or [D]raw from the deck? ")
        .strip()
        .lower()
    )

    if choice == "a":
        name = input("Enter custodian name: ").strip()
        action = input("Enter contribution/action: ").strip()
        cycle = input("Enter cycle number: ").strip()
        add_entry(name, action, cycle)
    elif choice == "d":
        draw_entry()
    else:
        print("🕯️ Invalid choice. Ceremony closed.")


if __name__ == "__main__":
    main()
