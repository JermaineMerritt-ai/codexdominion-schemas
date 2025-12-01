# apps/dashboard/council_treasury.py
import streamlit as st

from core.ledger import append_entry, load_json

st.title("💎 Council Treasury Scroll")

tabs = st.tabs(
    ["Stores", "Social Media", "Websites", "Council Oversight", "Custodian Approval"]
)

with tabs[0]:
    st.header("🏬 Stores Revenue")
    stores = load_json("stores.json", {"transactions": []})["transactions"]
    for s in stores:
        st.write(f"{s['timestamp']} — {s['item']} → ${s['amount']}")

with tabs[1]:
    st.header("📱 Social Media Revenue")
    social = load_json("social.json", {"transactions": []})["transactions"]
    for sm in social:
        st.write(f"{sm['timestamp']} — {sm['platform']} → ${sm['amount']}")

with tabs[2]:
    st.header("🌐 Website Revenue")
    sites = load_json("websites.json", {"transactions": []})["transactions"]
    for w in sites:
        st.write(f"{w['timestamp']} — {w['source']} → ${w['amount']}")

with tabs[3]:
    st.header("👥 Council Oversight")
    concord = st.text_area("Council Concord or Affirmation")
    if st.button("Add Concord"):
        append_entry(
            "ledger.json", "entries", {"role": "Council", "proclamation": concord}
        )
        st.success("Council concord inscribed into Codex flame.")

with tabs[4]:
    st.header("👑 Custodian Approval")
    total = sum(
        [s["amount"] for s in stores]
        + [sm["amount"] for sm in social]
        + [w["amount"] for w in sites]
    )
    if st.button("Approve Balance"):
        append_entry(
            "ledger.json",
            "entries",
            {
                "role": "Custodian",
                "proclamation": f"Sovereign Balance Approved: ${total}",
            },
        )
        st.success(f"Sovereign Balance Crowned: ${total}")
