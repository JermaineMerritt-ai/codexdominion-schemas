# apps/dashboard/publisher.py
import streamlit as st
import json
from pathlib import Path
from core.publisher import publish_html

st.title("📖 Codex Publisher")

artifact = st.selectbox("Select artifact", ["Love Lab Page", "Notebook Tome"])
if st.button("Publish"):
    if artifact == "Love Lab Page":
        output = publish_html("love_lab_page.json", "public/page.html")
    elif artifact == "Notebook Tome":
        output = publish_html("tome.md", "public/tome.html")
    st.success(f"Published: {output}")
    st.markdown(f"Artifact now live at your domain.")