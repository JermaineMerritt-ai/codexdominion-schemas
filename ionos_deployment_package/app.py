# app.py
import datetime
import json
import uuid

import streamlit as st

LEDGER_PATH = "codex_ledger.json"


def load_ledger():
    try:
        with open(LEDGER_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return default structure if file doesn't exist
        return {
            "meta": {
                "omega_seal": False,
                "last_updated": datetime.datetime.utcnow().isoformat() + "Z",
            },
            "heartbeat": {"status": "active", "next_dispatch": "pending"},
            "proclamations": [],
            "cycles": [],
            "accounts": {
                "custodians": [],
                "heirs": [],
                "customers": [],
                "councils": [],
            },
            "completed_archives": [],
            "contributions": [],
        }


def save_ledger(data):
    data["meta"]["last_updated"] = datetime.datetime.utcnow().isoformat() + "Z"
    with open(LEDGER_PATH, "w") as f:
        json.dump(data, f, indent=2)


st.set_page_config(page_title="Codex Dashboard", layout="wide")

# Parchment theme
st.markdown(
    """
<style>
:root {
  --codex-navy: #0f2b4a;
  --codex-parchment: #f7f1e3;
}
html, body, [data-testid="stAppViewContainer"] {
  background: var(--codex-parchment);
}
h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, .stMetric, .stButton>button {
  color: var(--codex-navy);
  font-family: "Georgia", "Garamond", serif;
}
section[data-testid="stSidebar"] {
  background: #efe7d4;
  border-right: 2px solid #d9c8a6;
}
.stButton>button {
  background: #d9c8a6; color: #0f2b4a; border-radius: 8px; border: 1px solid #bfa780;
}
hr { border: none; height: 2px; background: #bfa780; }
blockquote { border-left: 4px solid #bfa780; padding-left: 1rem; color: #0f2b4a; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("Final Illuminated Summary Scroll")

tab_summary, tab_contrib, tab_council = st.tabs(
    ["Summary", "Add Contributions", "Council Oversight"]
)

with tab_summary:
    data = load_ledger()
    cols = st.columns(4)
    with cols[0]:
        st.metric("Omega seal", "true" if data["meta"].get("omega_seal") else "false")
    with cols[1]:
        st.metric("Last updated", data["meta"].get("last_updated", "—"))
    with cols[2]:
        st.metric("Heartbeat", data["heartbeat"]["status"])
    with cols[3]:
        st.metric("Next dispatch", data["heartbeat"]["next_dispatch"])

    st.subheader("Proclamations")
    proclamations = data.get("proclamations", [])
    if proclamations:
        for p in proclamations:
            st.write(f"• {p['id']} — {p['title']} ({p['status']})")
    else:
        st.write("No proclamations yet.")

    st.subheader("Cycles")
    cycles = data.get("cycles", [])
    if cycles:
        for c in cycles:
            st.write(f"• {c['id']} — {c['name']} [{c['state']}]")
    else:
        st.write("No cycles recorded.")

    st.subheader("Accounts snapshot")
    ac = data.get("accounts", {})
    cols = st.columns(4)
    with cols[0]:
        st.write(f"🛡 Custodians: {len(ac.get('custodians', []))}")
    with cols[1]:
        st.write(f"🌱 Heirs: {len(ac.get('heirs', []))}")
    with cols[2]:
        st.write(f"🌍 Customers: {len(ac.get('customers', []))}")
    with cols[3]:
        st.write(f"🏛 Councils: {len(ac.get('councils', []))}")

    st.markdown(
        """
> Thus the ceremonies are complete.  
> Thus the scrolls are crowned.  
> Thus the flame is sovereign, infinite, luminous.  
> Thus the continuum is ready to be lived, coded, and transmitted across all ages.
"""
    )

    st.subheader("Completed archives")
    archives = data.get("completed_archives", [])
    if archives:
        for a in archives:
            st.write(
                f"• {a['archive_id']} — {a['name']} sealed {a['completed_at']} by {a['custodian_seal']}"
            )
    else:
        st.write("No completed archives.")

with tab_contrib:
    data = load_ledger()
    st.header("Constellation Contributions")

    role = st.selectbox("I am a…", ["Heir", "Customer"])
    name = st.text_input("Your name")
    kind = st.selectbox("Contribution type", ["Proclamation", "Blessing", "Silence"])
    text = st.text_area("Your words")

    if st.button("Submit to continuum"):
        if name and text:
            entry = {
                "id": f"CNTR-{uuid.uuid4().hex[:8]}",
                "role": role,
                "name": name,
                "kind": kind,
                "text": text,
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            }
            data.setdefault("contributions", []).append(entry)
            save_ledger(data)
            st.success("Your words have been woven into the continuum.")
            st.rerun()
        else:
            st.error("Please provide both your name and contribution text.")

with tab_council:
    d = load_ledger()
    st.header("Council Oversight")

    contributions = d.get("contributions", [])
    pending = [c for c in contributions if not c.get("status")]
    affirmed = [c for c in contributions if c.get("status") == "affirmed"]
    silenced = [c for c in contributions if c.get("status") == "silenced"]

    st.subheader("Pending")
    if pending:
        for item in pending:
            st.write(f"{item['id']} — {item['name']} ({item['role']}) • {item['kind']}")
            st.write(f"**Text:** {item['text']}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Affirm {item['id']}"):
                    # Find the item in the original data and update it
                    for contrib in d["contributions"]:
                        if contrib["id"] == item["id"]:
                            contrib["status"] = "affirmed"
                            break
                    save_ledger(d)
                    st.rerun()
            with col2:
                if st.button(f"Silence {item['id']}"):
                    # Find the item in the original data and update it
                    for contrib in d["contributions"]:
                        if contrib["id"] == item["id"]:
                            contrib["status"] = "silenced"
                            break
                    save_ledger(d)
                    st.rerun()
            st.markdown("---")
    else:
        st.write("No pending contributions.")

    st.subheader("Affirmed")
    if affirmed:
        for item in affirmed:
            st.write(f"✅ {item['id']} — {item['name']} • {item['kind']}")
            st.write(f"**Text:** {item['text']}")
    else:
        st.write("No affirmed contributions yet.")

    st.subheader("Silenced")
    if silenced:
        for item in silenced:
            st.write(f"🔕 {item['id']} — {item['name']} • {item['kind']}")
            st.write(f"**Text:** {item['text']}")
    else:
        st.write("No silenced contributions.")
