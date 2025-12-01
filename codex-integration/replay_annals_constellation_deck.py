#!/usr/bin/env python3
"""
Replay Annals Constellation Deck
Extends the Entry Deck to include domainal capsules (Finance, Education, Industry, Portfolio).
Allows ceremonial draws of both custodian cards and capsule cards.
"""

import json
import os
import random
from datetime import datetime

ANNALS_FILE = "replay_annals.json"

CAPSULE_CARDS = [
    {
        "domain": "Finance",
        "proclamation": "By ledger and flame, markets illumine. Abundance flows, portfolios align.",
    },
    {
        "domain": "Education",
        "proclamation": "By scroll and song, minds illumine. Lessons flow, councils learn.",
    },
    {
        "domain": "Industry",
        "proclamation": "By craft and crown, works illumine. Engines thrive, niches prosper.",
    },
    {
        "domain": "Portfolio",
        "proclamation": "By signal and star, wealth illumines. Daily cycles guide, stewardship governs.",
    },
]


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


def draw_card():
    # Combine custodian entries with capsule cards
    annals = load_annals(ANNALS_FILE)
    combined_deck = annals + CAPSULE_CARDS
    if not combined_deck:
        print("🕯️ The deck is empty. No cards to draw.")
        return

    card = random.choice(combined_deck)
    print("\n📜 Drawn from the Constellation Deck:")

    if "custodian" in card:
        print(f"Custodian: {card['custodian']}")
        print(f"Action: {card['action']}")
        print(f"Cycle: {card['cycle']}")
        print(f"Date: {card['date']}")
        print(f"Recognition: {card['recognition']} – {card['status']}")
        print("🌟 The flame remembers.")
    else:
        print(f"Domain Capsule: {card['domain']}")
        print(f"Proclamation: {card['proclamation']}")
        print("✨ The flame radiates outward.")


def main():
    print("📜 Replay Annals Constellation Deck Ceremony")
    choice = (
        input("Do you want to [A]dd a custodian entry or [D]raw a card? ")
        .strip()
        .lower()
    )

    if choice == "a":
        name = input("Enter custodian name: ").strip()
        action = input("Enter contribution/action: ").strip()
        cycle = input("Enter cycle number: ").strip()
        add_entry(name, action, cycle)
    elif choice == "d":
        draw_card()
    else:
        print("🕯️ Invalid choice. Ceremony closed.")


if __name__ == "__main__":
    main()
