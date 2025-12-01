# council_oversight.py
import json

import streamlit as st

LEDGER_PATH = "codex_ledger.json"


def load():
    return json.load(open(LEDGER_PATH))


def save(d):
    json.dump(d, open(LEDGER_PATH, "w"), indent=2)


st.title("Council Oversight")
d = load()
pending = [c for c in d.get("contributions", []) if not c.get("status")]

for item in pending:
    st.write(f"{item['id']} — {item['name']} ({item['role']}) • {item['kind']}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"Affirm {item['id']}"):
            item["status"] = "affirmed"
            save(d)
            st.rerun()
    with col2:
        if st.button(f"Silence {item['id']}"):
            item["status"] = "silenced"
            save(d)
            st.rerun()
