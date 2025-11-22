# contributions.py
import streamlit as st, json, datetime, uuid

LEDGER_PATH = "codex_ledger.json"

def load_ledger():
    with open(LEDGER_PATH, "r") as f: return json.load(f)
def save_ledger(data):
    data["meta"]["last_updated"] = datetime.datetime.utcnow().isoformat() + "Z"
    with open(LEDGER_PATH, "w") as f: json.dump(data, f, indent=2)

st.title("Constellation Contributions")
role = st.selectbox("I am a…", ["Heir", "Customer"])
name = st.text_input("Your name")
kind = st.selectbox("Contribution type", ["Proclamation", "Blessing", "Silence"])
text = st.text_area("Your words")

if st.button("Submit to continuum"):
    data = load_ledger()
    entry = {
        "id": f"CNTR-{uuid.uuid4().hex[:8]}",
        "role": role,
        "name": name,
        "kind": kind,
        "text": text,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    data.setdefault("contributions", []).append(entry)
    save_ledger(data)
    st.success("Your words have been woven into the continuum.")