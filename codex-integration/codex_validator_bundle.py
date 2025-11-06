#!/usr/bin/env python3
"""
Codex Validator Bundle
Validates all Codex JSON files (proclamations, cycles, ledger, heartbeat).
Ensures each entry has required schema keys.
"""

import json
import sys
import os

# Define required keys for each file type
SCHEMA = {
    "proclamations.json": {"season", "cycle", "date", "proclamation", "blessing"},
    "cycles.json": {"season", "cycle", "date"},
    "ledger.json": {"entry", "date", "custodian"},
    "heartbeat.json": {"timestamp", "status"}
}

def validate_entry(entry, required_keys, index, filename):
    missing = required_keys - entry.keys()
    if missing:
        print(f"❌ {filename} – Entry {index} missing keys: {', '.join(missing)}")
        return False
    print(f"✅ {filename} – Entry {index} valid.")
    return True

def validate_file(path, required_keys):
    if not os.path.exists(path):
        print(f"⚠️ File not found: {path}")
        return False

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in {path}: {e}")
            return False

    if not isinstance(data, list):
        print(f"❌ Expected a list of entries in {path}, got {type(data)}")
        return False

    all_valid = True
    for i, entry in enumerate(data, start=1):
        if not validate_entry(entry, required_keys, i, path):
            all_valid = False

    return all_valid

def main():
    base_dir = os.getcwd()
    all_passed = True

    for filename, required_keys in SCHEMA.items():
        path = os.path.join(base_dir, filename)
        print(f"\n🔍 Validating {filename}...")
        if not validate_file(path, required_keys):
            all_passed = False

    if all_passed:
        print("\n🌟 All Codex files are valid. The flame is luminous across all panels.")
    else:
        print("\n⚠️ Some Codex files contain errors. Please correct them before deployment.")

if __name__ == "__main__":
    main()
