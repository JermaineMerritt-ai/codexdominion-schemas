import json
import os

import pytest

REQUIRED_KEYS = {"season", "cycle", "date", "proclamation", "blessing"}


def load_json_file(path: str):
    """Load a JSON file and return its contents."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_schema(entry: dict):
    """Ensure a proclamation entry has all required keys."""
    missing = REQUIRED_KEYS - entry.keys()
    if missing:
        raise ValueError(f"Missing keys: {missing}")
    return True


# ------------------------
# Tests
# ------------------------


def test_load_json_file_valid(tmp_path):
    file_path = tmp_path / "sample.json"
    data = {
        "season": "Winter",
        "cycle": "Silence Crown",
        "date": "2025-12-21",
        "proclamation": "In stillness we crown the flame.",
        "blessing": "Peace and pause for all heirs.",
    }
    file_path.write_text(json.dumps(data), encoding="utf-8")

    result = load_json_file(str(file_path))
    assert result["season"] == "Winter"
    assert result["cycle"] == "Silence Crown"


def test_load_json_file_missing(tmp_path):
    file_path = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError):
        load_json_file(str(file_path))


def test_load_json_file_invalid_json(tmp_path):
    file_path = tmp_path / "bad.json"
    file_path.write_text("{not: valid}", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_json_file(str(file_path))


def test_validate_schema_complete():
    entry = {
        "season": "Spring",
        "cycle": "Renewal Proclamation",
        "date": "2026-03-20",
        "proclamation": "The flame renews, blossoms rise.",
        "blessing": "Growth and renewal for every custodian.",
    }
    assert validate_schema(entry) is True


def test_validate_schema_missing_keys():
    entry = {
        "season": "Summer",
        "cycle": "Abundance Cycle",
        # Missing date, proclamation, blessing
    }
    with pytest.raises(ValueError) as excinfo:
        validate_schema(entry)
    assert "Missing keys" in str(excinfo.value)
