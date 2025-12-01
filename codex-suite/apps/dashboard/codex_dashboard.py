import sys
from pathlib import Path

import streamlit as st

# Add parent directory to path to access modules
sys.path.append(str(Path(__file__).parent.parent.parent))

from core.ledger import append_entry, load_json
from modules.spark_studio import spark_generate

st.set_page_config(page_title="Codex Dashboard", layout="wide")

st.title("🔥 Codex Dashboard — Cycle 1")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Spark Studio", "Ledger", "Invocations", "Tome Formatter"]
)

with tab1:
    st.header("Spark Studio MVP")
    topic = st.text_input("Topic", "Codex Flame Launch")
    audience = st.text_input("Audience", "Heirs and Councils")
    tone = st.selectbox("Tone", ["Sovereign", "Warm", "Direct"])
    constraints = st.text_area("Constraints", "150-200 words, 1 CTA, no jargon")

    if st.button("Generate Drafts"):
        drafts = spark_generate(topic, audience, tone, constraints)
        st.success("Drafts generated and archived to Ledger.")
        for d in drafts:
            st.markdown(f"**{d['title']}** — {d['text']}")

with tab2:
    st.header("Ledger Chronicle")
    ledger = load_json("ledger.json", {"entries": []})
    for e in ledger["entries"][-20:]:
        st.markdown(
            f"**{e.get('role','')}** → *{e.get('proclamation','')}*  \n ⏳ {e.get('timestamp','')}"
        )

    st.divider()
    role = st.selectbox("Role", ["Custodian", "Heirs", "Councils", "Cosmos"])
    proclamation = st.text_input("Proclamation")
    if st.button("Inscribe into Ledger"):
        append_entry(
            "ledger.json", "entries", {"role": role, "proclamation": proclamation}
        )
        st.success("Proclamation inscribed.")

with tab3:
    st.header("Invocations")
    inv = load_json("invocations.json", {"invocations": []})["invocations"]
    for i in inv[-20:]:
        st.markdown(
            f"**{i.get('role','')}** → *{i.get('text','')}*  \n ⏳ {i.get('timestamp','')}"
        )

with tab4:
    st.header("📚 Tome Formatter")
    st.markdown("Convert Codex notebook JSON files to beautiful Markdown documents")

    # Import the tome formatter
    from modules.codex_tome_formatter import batch_format_tomes, format_tome

    # File upload for JSON notebooks
    uploaded_file = st.file_uploader("Upload Codex Notebook (JSON)", type="json")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Single File Conversion")

        if uploaded_file is not None:
            # Save uploaded file
            notebook_data = uploaded_file.read()
            notebook_path = f"data/{uploaded_file.name}"

            with open(notebook_path, "wb") as f:
                f.write(notebook_data)

            # Generate output filename
            output_filename = f"{Path(uploaded_file.name).stem}_tome.md"
            output_path = f"data/{output_filename}"

            if st.button("🔥 Convert to Tome"):
                if format_tome(notebook_path, output_path):
                    st.success(f"✅ Converted to {output_filename}")

                    # Show download button
                    with open(output_path, "r", encoding="utf-8") as f:
                        tome_content = f.read()

                    st.download_button(
                        label="📖 Download Tome",
                        data=tome_content,
                        file_name=output_filename,
                        mime="text/markdown",
                    )

                    # Preview first few lines
                    st.subheader("📋 Preview")
                    lines = tome_content.split("\n")[:15]
                    st.code("\n".join(lines), language="markdown")
                else:
                    st.error("❌ Conversion failed")

    with col2:
        st.subheader("🗂️ Batch Processing")

        if st.button("📁 Process All Notebooks in Data Directory"):
            results = batch_format_tomes("data", "data/tomes")

            if results["success"] > 0:
                st.success(f"✅ Successfully processed {results['success']} notebooks")

                # Show results
                for file_info in results["files"]:
                    if file_info["status"] == "success":
                        st.markdown(
                            f"✅ {Path(file_info['input']).name} → {Path(file_info['output']).name}"
                        )
                    else:
                        st.markdown(f"❌ {Path(file_info['input']).name} - Failed")
            else:
                st.info("No notebook files found to process")

        st.divider()

        # Sample notebook creator
        st.subheader("📝 Create Sample Notebook")
        if st.button("🎯 Generate Sample"):
            from modules.codex_tome_formatter import create_sample_notebook

            create_sample_notebook()
            st.success("📄 Created sample_notebook.json in current directory")

            # Auto-convert sample
            if format_tome("sample_notebook.json", "data/sample_tome.md"):
                st.success("📚 Also created sample_tome.md")

                # Log to ledger
                append_entry(
                    "ledger.json",
                    "entries",
                    {
                        "role": "TomeFormatter",
                        "proclamation": "Sample Codex Tome generated - Demonstrating notebook to markdown conversion",
                    },
                )
