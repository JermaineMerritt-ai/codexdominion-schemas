# omega_seal.py
import datetime
import json
import uuid

LEDGER_PATH = "codex_ledger.json"


def load_ledger():
    with open(LEDGER_PATH, "r") as f:
        return json.load(f)


def save_ledger(data):
    data["meta"]["last_updated"] = datetime.datetime.utcnow().isoformat() + "Z"
    with open(LEDGER_PATH, "w") as f:
        json.dump(data, f, indent=2)


def seal_cycle(cycle_id, note=""):
    data = load_ledger()
    cycle = next((c for c in data["cycles"] if c["id"] == cycle_id), None)
    if not cycle:
        raise ValueError(f"Cycle {cycle_id} not found")
    cycle["state"] = "completed"
    archive_entry = {
        "archive_id": f"ARC-{uuid.uuid4().hex[:8]}",
        "cycle_id": cycle_id,
        "name": cycle["name"],
        "completed_at": datetime.datetime.utcnow().isoformat() + "Z",
        "custodian_seal": "Jermaine Merritt",
        "note": note,
    }
    data.setdefault("completed_archives", []).append(archive_entry)
    data["meta"]["omega_seal"] = True
    save_ledger(data)
    return archive_entry
