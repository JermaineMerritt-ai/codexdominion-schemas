# core/flows.py
import json
import uuid
from datetime import datetime

from .ledger import load_json, save_json


def list_flows():
    return load_json("flows.json", {"flows": []})["flows"]


def create_flow(name, nodes):
    flows = list_flows()
    fid = str(uuid.uuid4())
    flows.append(
        {
            "id": fid,
            "name": name,
            "nodes": nodes,
            "created_at": datetime.now().isoformat(),
            "version": 1,
        }
    )
    save_json("flows.json", {"flows": flows})
    return fid


def log_dispatch(flow_id, status, note=""):
    log = load_json("dispatch_log.json", {"events": []})
    log["events"].append(
        {
            "flow_id": flow_id,
            "status": status,
            "note": note,
            "ts": datetime.now().isoformat(),
        }
    )
    save_json("dispatch_log.json", log)
