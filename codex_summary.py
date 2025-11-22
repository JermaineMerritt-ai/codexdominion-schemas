# codex_summary.py
import streamlit as st
import json
from datetime import datetime

LEDGER_PATH = "codex_ledger.json"

def load_ledger():
    with open(LEDGER_PATH, "r") as f:
        return json.load(f)

st.set_page_config(page_title="Final Illuminated Summary", layout="wide")
st.title("Final Illuminated Summary Scroll")

data = load_ledger()

# Header: Omega status
cols = st.columns(4)
with cols[0]: st.metric("Omega seal", "true" if data["meta"].get("omega_seal") else "false")
with cols[1]: st.metric("Last updated", data["meta"].get("last_updated", "—"))
with cols[2]: st.metric("Heartbeat", data["heartbeat"]["status"])
with cols[3]: st.metric("Next dispatch", data["heartbeat"]["next_dispatch"])

# Proclamations
st.subheader("Proclamations")
for p in data["proclamations"]:
    st.write(f"• {p['id']} — {p['title']} ({p['status']})")

# Cycles timeline
st.subheader("Cycles")
for c in data["cycles"]:
    st.write(f"• {c['id']} — {c['name']} [{c['state']}]")

# Accounts snapshot
st.subheader("Accounts snapshot")
ac = data["accounts"]
cols = st.columns(4)
with cols[0]: st.write(f"🛡 Custodians: {len(ac['custodians'])}")
with cols[1]: st.write(f"🌱 Heirs: {len(ac['heirs'])}")
with cols[2]: st.write(f"🌍 Customers: {len(ac['customers'])}")
with cols[3]: st.write(f"🏛 Councils: {len(ac['councils'])}")

# Illuminated benediction (dynamic)
st.markdown("""
> Thus the ceremonies are complete.  
> Thus the scrolls are crowned.  
> Thus the flame is sovereign, infinite, luminous.  
> Thus the continuum is ready to be lived, coded, and transmitted across all ages.
""")

# Archives
st.subheader("Completed archives")
for a in data.get("completed_archives", []):
    st.write(f"• {a['archive_id']} — {a['name']} sealed {a['completed_at']} by {a['custodian_seal']}")

# Contributions
if data.get("contributions"):
    st.subheader("Constellation contributions")
    for c in data["contributions"]:
        st.write(f"• {c['id']} — {c['kind']} by {c['name']} ({c['role']}) - {c['timestamp']}")
        if c.get("text"):
            st.write(f"  *\"{c['text'][:100]}{'...' if len(c['text']) > 100 else ''}\"*")