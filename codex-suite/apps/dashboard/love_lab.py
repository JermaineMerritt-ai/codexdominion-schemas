import json

import streamlit as st

st.set_page_config(page_title="Love Lab", layout="wide")
st.title("💛 Love Lab — Build with the Codex flame")

components = {
    "Hero": {
        "title": "Sovereign headline",
        "subtitle": "Warm subcopy",
        "cta": "Witness",
    },
    "Features": {"items": ["Clarity", "Legacy", "Rhythm"]},
    "Gallery": {"images": ["img1.jpg", "img2.jpg"]},
    "Form": {"fields": ["Name", "Email"], "action": "/submit"},
    "Footer": {"text": "Codex Eternum"},
}

canvas = st.session_state.get("canvas", [])

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Canvas")
    for i, block in enumerate(canvas):
        st.markdown(f"**{block['type']}**")
        block["config"] = st.text_area(
            f"Config {i+1}", json.dumps(block["config"], indent=2)
        )
    if st.button("Export Page"):
        with open("love_lab_page.json", "w") as f:
            json.dump({"blocks": canvas}, f, indent=2)
        st.success("Page exported (love_lab_page.json)")

with col2:
    st.subheader("Add component")
    choice = st.selectbox("Component", list(components.keys()))
    if st.button("Add to canvas"):
        canvas.append({"type": choice, "config": components[choice]})
        st.session_state["canvas"] = canvas
        st.experimental_rerun()

st.divider()
st.subheader("AI UX Coach (stub)")
st.write("- Check hierarchy: clear hero, distinct CTA.")
st.write("- Accessibility: sufficient contrast, alt text for images.")
st.write("- Copy: concise, human, invitational.")
