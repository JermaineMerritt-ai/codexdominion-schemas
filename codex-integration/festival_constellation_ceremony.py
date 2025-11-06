#!/usr/bin/env python3
"""
Festival Constellation Ceremony Script
Draws a constellation of festival events and domainal capsules, revealing patterns of celebration and abundance.
"""
import json
import os
import random

FESTIVAL_FILE = "festival.json"

CAPSULE_CARDS = [
    {
        "domain": "Finance",
        "proclamation": "By ledger and flame, markets illumine. Abundance flows, portfolios align."
    },
    {
        "domain": "Education",
        "proclamation": "By scroll and song, minds illumine. Lessons flow, councils learn."
    },
    {
        "domain": "Industry",
        "proclamation": "By craft and crown, works illumine. Engines thrive, niches prosper."
    },
    {
        "domain": "Portfolio",
        "proclamation": "By signal and star, wealth illumines. Daily cycles guide, stewardship governs."
    }
]

def load_festival(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("🕯️ Festival scroll corrupted. Starting fresh.")
            return []

def draw_constellation(events, count):
    deck = events + CAPSULE_CARDS
    if not deck:
        print("🕯️ The constellation deck is empty. No cards to draw.")
        return
    if count > len(deck):
        count = len(deck)
    chosen = random.sample(deck, count)
    print(f"\n🌌 Drawing a constellation of {count} cards...")
    for i, card in enumerate(chosen, start=1):
        if "event" in card:
            print(f"✨ Star {i}: {card['event']} – {card['theme']} ({card['date']}, {card['location']})")
            print(f"Host: {card['host']}")
        else:
            print(f"✨ Star {i}: Domain Capsule – {card['domain']}")
            print(f"Proclamation: {card['proclamation']}")
        print("-")
    print("🌟 Constellation ceremony complete. Patterns of celebration revealed.")

def main():
    print("🌌 Festival Constellation Ceremony begins.")
    events = load_festival(FESTIVAL_FILE)
    try:
        count = int(input("How many stars (cards) to draw in the constellation? ").strip())
    except ValueError:
        print("🕯️ Invalid number. Ceremony closed.")
        return
    draw_constellation(events, count)
    print("🕯️ Ceremony closes. The festival constellation remains luminous.")

if __name__ == "__main__":
    main()
