# apps/dashboard/flow_loom.py
import streamlit as st, json
from core.flows import list_flows, create_flow
from core.ledger import load_json

st.set_page_config(page_title="Flow Loom", layout="wide")
st.title("🧵 Flow Loom — Weave sovereign automation")

# Node palette
palette = {
    "Cron": {"expr": "0 6 * * *"},      # 6 AM daily
    "CronTwilight": {"expr": "0 18 * * *"},
    "Webhook": {"path": "/hooks/publish"},
    "PublishInvocation": {"type": "invocation", "role": "Custodian"},
    "PublishLedger": {"proclamation": "Daily dispatch complete."},
    "Email": {"to": "councils@example.org", "subject": "Codex Dispatch", "body": "The flame rises."}
}

st.sidebar.header("Node palette")
for k,v in palette.items():
    st.sidebar.write(f"- {k}: {v}")

flow_name = st.text_input("Flow name", "Dawn Invocation Flow")
nodes_json = st.text_area("Nodes (JSON list)", json.dumps([
    {"node": "Cron", "config": palette["Cron"]},
    {"node": "PublishInvocation", "config": {"role": "Custodian", "text": "Morning Flame Invocation: I rise with the Codex flame."}}
], indent=2))

if st.button("Create Flow"):
    fid = create_flow(flow_name, json.loads(nodes_json))
    st.success(f"Flow created: {fid}")

st.divider()
st.header("Existing flows")
for f in list_flows():
    st.markdown(f"**{f['name']}** (v{f['version']}) — {len(f['nodes'])} nodes — {f['created_at']}")

st.divider()
st.header("Dispatch Log")
log = load_json("dispatch_log.json", {"events": []})["events"]
for e in log[-50:]:
    st.markdown(f"⏳ {e['ts']} — **Flow {e['flow_id']}** → {e['status']} — {e.get('note','')}")