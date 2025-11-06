#!/usr/bin/env python3
"""
Codex JSON Validator Script
Checks proclamation JSON files for required schema keys.
"""

import json
import sys
import os

REQUIRED_KEYS = {"season", "cycle", "date", "proclamation", "blessing"}

def validate_entry(entry, index):
    missing = REQUIRED_KEYS - entry.keys()
    if missing:
        print(f"❌ Entry {index} is missing keys: {', '.join(missing)}")
        return False
    print(f"✅ Entry {index} is valid: {entry['season']} – {entry['cycle']}")
    return True

def validate_file(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
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
        if not validate_entry(entry, i):
            all_valid = False

    return all_valid

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python codex_json_validator.py proclamations.json")
        sys.exit(1)

    file_path = sys.argv[1]
    success = validate_file(file_path)
    if success:
        print("🌟 All entries are valid. The Codex flame is luminous.")
    else:
        print("⚠️ Some entries are invalid. Please correct them before committing.")
