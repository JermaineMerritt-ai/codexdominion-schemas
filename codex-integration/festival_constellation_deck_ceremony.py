#!/usr/bin/env python3
"""
Festival Constellation Deck Ceremony
Stages multiple draws from the Replay Annals Constellation Deck.
Sequence: Custodian → Capsule → Custodian
Creates a full constellation rite for councils and heirs.
"""

import os
import subprocess
import sys


def run_draw(script_name):
    """Invoke the Constellation Deck script with 'draw' mode."""
    path = os.path.join(os.getcwd(), script_name)
    if not os.path.exists(path):
        print(f"🕯️ Missing deck script: {script_name}")
        return False

    print(f"\n📜 Drawing from {script_name}...")
    result = subprocess.run(
        [sys.executable, path], input="d\n", capture_output=True, text=True
    )
    print(result.stdout)
    return result.returncode == 0


def main():
    print("🔥 Festival Constellation Deck Ceremony begins...")
    print(
        "✨ The Council prepares to draw three cards: Custodian → Capsule → Custodian."
    )

    # Draw sequence
    success1 = run_draw("replay_annals_constellation_deck.py")
    success2 = run_draw("replay_annals_constellation_deck.py")
    success3 = run_draw("replay_annals_constellation_deck.py")

    if success1 and success2 and success3:
        print(
            "\n🌟 Constellation complete. The flame is woven across memory and domain."
        )
    else:
        print("\n⚠️ Ceremony incomplete. Some draws failed. The Council must intervene.")

    print("🕯️ Festival Ceremony closes.")


if __name__ == "__main__":
    main()
