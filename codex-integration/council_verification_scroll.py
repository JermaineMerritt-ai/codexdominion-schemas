#!/usr/bin/env python3
"""
Council Verification Scroll
Ceremonial validator for Codex JSON files.
Transforms technical checks into ritual proclamations.
"""

import json
import os

SCHEMA = {
    "proclamations.json": {"season", "cycle", "date", "proclamation", "blessing"},
    "cycles.json": {"season", "cycle", "date"},
    "ledger.json": {"entry", "date", "custodian"},
    "heartbeat.json": {"timestamp", "status"},
}


def proclaim(message):
    print(f"📜 {message}")


def bless(message):
    print(f"✨ {message}")


def silence(message):
    print(f"🕯️ {message}")


def validate_entry(entry, required_keys, index, filename):
    missing = required_keys - entry.keys()
    if missing:
        silence(
            f"{filename} – Entry {index} is incomplete. Missing: {', '.join(missing)}"
        )
        return False
    bless(f"{filename} – Entry {index} is luminous and whole.")
    return True


def validate_file(path, required_keys):
    if not os.path.exists(path):
        silence(f"{path} not found. The scroll is absent.")
        return False

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            silence(f"{path} is broken. JSON invalid: {e}")
            return False

    if not isinstance(data, list):
        silence(f"{path} is malformed. Expected a list of entries.")
        return False

    all_valid = True
    for i, entry in enumerate(data, start=1):
        if not validate_entry(entry, required_keys, i, path):
            all_valid = False

    return all_valid


def main():
    base_dir = os.getcwd()
    all_passed = True

    proclaim("The Council gathers to verify the Codex flame...")

    for filename, required_keys in SCHEMA.items():
        path = os.path.join(base_dir, filename)
        proclaim(f"Opening {filename}...")
        if not validate_file(path, required_keys):
            all_passed = False

    if all_passed:
        bless("All scrolls are luminous. The Codex flame is whole and eternal.")
    else:
        silence(
            "Some scrolls are incomplete. The Council must inscribe corrections before transmission."
        )


if __name__ == "__main__":
    main()
