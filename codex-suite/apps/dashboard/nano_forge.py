import json
from datetime import datetime

import streamlit as st

st.set_page_config(page_title="Nano Forge", layout="centered")
st.title("🔧 Nano Forge — Micro-tools from the Codex flame")

templates = {
    "Checklist": {"items": ["Step 1", "Step 2", "Step 3"]},
    "Calculator": {"inputs": ["a", "b"], "formula": "a + b"},
    "Uploader": {"accept": ["png", "jpg", "pdf"]},
    "Prompt Generator": {"fields": ["Topic", "Audience", "Tone", "Constraints"]},
    "Announcement": {
        "headline": "Proclaim the flame",
        "body": "We shine across the continuum.",
    },
}

tool = st.selectbox("Template", list(templates.keys()))
config = st.text_area("Config (JSON)", json.dumps(templates[tool], indent=2))

if st.button("Generate Tool"):
    artifact = {
        "type": tool,
        "config": json.loads(config),
        "timestamp": datetime.now().isoformat(),
    }
    with open(f"nano_{tool.lower()}.json", "w") as f:
        json.dump(artifact, f, indent=2)
    st.success(f"{tool} generated → nano_{tool.lower()}.json")

st.divider()
st.subheader("One-click run (demo)")
if tool == "Calculator":
    a = st.number_input("a", 0.0)
    b = st.number_input("b", 0.0)
    st.write("Result:", a + b)
elif tool == "Checklist":
    for item in json.loads(config)["items"]:
        st.checkbox(item)
