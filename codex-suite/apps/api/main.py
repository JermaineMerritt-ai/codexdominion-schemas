import sys
from pathlib import Path

from fastapi import FastAPI

# Add parent directory to path to access core modules
sys.path.append(str(Path(__file__).parent.parent.parent))

from core.ledger import append_entry, load_json

app = FastAPI(title="Codex API — Cycle 1")


@app.get("/ledger")
def get_ledger():
    return load_json("ledger", {"entries": []})


@app.post("/ledger")
def post_ledger(role: str, proclamation: str):
    return append_entry(
        "ledger", "entries", {"role": role, "proclamation": proclamation}
    )
