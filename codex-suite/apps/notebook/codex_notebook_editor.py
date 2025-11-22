#!/usr/bin/env python3
"""
📓 Codex Notebook Editor
=======================

A Streamlit-based interactive notebook editor for the Codex Dominion Suite.
Supports text, code, and prompt cells with export/import functionality.

Usage:
    streamlit run codex_notebook_editor.py --server.port 8502

Integration with Codex Suite Cycle 1 - Advanced notebook management.
"""

import streamlit as st
import json
import os
from datetime import datetime

# Set up the main interface
st.set_page_config(
    page_title="📓 Codex Notebook Editor",
    page_icon="📓",
    layout="wide"
)

st.title("📓 Codex Notebook Editor")
st.markdown("### Create and manage different types of cells in your Codex notebook")

# Add some styling
st.markdown("""
<style>
.cell-container {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for cells
if "cells" not in st.session_state:
    st.session_state["cells"] = []

if "notebook_name" not in st.session_state:
    st.session_state["notebook_name"] = "codex_notebook"

# Get cells from session state
cells = st.session_state.get("cells", [])

# Create control buttons in columns
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("📝 Add Text Cell"):
        cells.append({
            "type": "text", 
            "content": "",
            "created_at": datetime.now().isoformat()
        })
        st.session_state["cells"] = cells
        st.rerun()

with col2:
    if st.button("💻 Add Code Cell"):
        cells.append({
            "type": "code", 
            "content": "",
            "created_at": datetime.now().isoformat()
        })
        st.session_state["cells"] = cells
        st.rerun()

with col3:
    if st.button("🤖 Add Prompt Cell"):
        cells.append({
            "type": "prompt", 
            "content": "",
            "created_at": datetime.now().isoformat()
        })
        st.session_state["cells"] = cells
        st.rerun()

with col4:
    if st.button("🗑️ Clear All"):
        st.session_state["cells"] = []
        st.rerun()

with col5:
    if st.button("🔄 Refresh"):
        st.rerun()

# Display information about the notebook
if len(cells) > 0:
    st.markdown(f"**Notebook contains {len(cells)} cells**")
    st.divider()
else:
    st.info("No cells in the notebook. Add some cells to get started!")

# Render cells dynamically
for i, cell in enumerate(cells):
    cell_number = i + 1
    
    # Create a container for each cell with styling
    with st.container():
        # Cell header with type badge and delete button
        col_header, col_delete = st.columns([4, 1])
        
        with col_header:
            if cell["type"] == "text":
                st.markdown(f"**📝 Text Cell {cell_number}**")
                cell_icon = "📝"
                cell_lang = "markdown"
            elif cell["type"] == "code":
                st.markdown(f"**💻 Code Cell {cell_number}**")
                cell_icon = "💻"
                cell_lang = "python"
            elif cell["type"] == "prompt":
                st.markdown(f"**🤖 Prompt Cell {cell_number}**")
                cell_icon = "🤖"
                cell_lang = "text"
        
        with col_delete:
            if st.button(f"🗑️", key=f"delete_{i}", help="Delete this cell"):
                cells.pop(i)
                st.session_state["cells"] = cells
                st.rerun()
        
        # Cell content editor
        if cell["type"] == "text":
            cell["content"] = st.text_area(
                f"Text Cell {cell_number}", 
                cell["content"],
                key=f"text_{i}",
                height=150,
                help="Write markdown text, documentation, or notes here"
            )
        elif cell["type"] == "code":
            cell["content"] = st.text_area(
                f"Code Cell {cell_number}", 
                cell["content"],
                key=f"code_{i}",
                height=200,
                help="Write Python code, scripts, or functions here"
            )
        elif cell["type"] == "prompt":
            cell["content"] = st.text_area(
                f"Prompt Cell {cell_number}", 
                cell["content"],
                key=f"prompt_{i}",
                height=120,
                help="Write AI prompts, instructions, or queries here"
            )
        
        st.divider()

# Update session state with modified cells
st.session_state["cells"] = cells

# Create notebook metadata
notebook_metadata = {
    "name": st.session_state.get("notebook_name", "codex_notebook"),
    "created_at": datetime.now().isoformat(),
    "cell_count": len(cells),
    "codex_version": "1.0",
    "notebook_type": "codex_interactive"
}

# Export functionality in the sidebar
with st.sidebar:
    st.header("📓 Notebook Controls")
    
    # Notebook name input
    notebook_name = st.text_input(
        "Notebook Name", 
        value=st.session_state.get("notebook_name", "codex_notebook")
    )
    st.session_state["notebook_name"] = notebook_name
    
    st.divider()
    
    # Export options
    st.subheader("💾 Export Options")
    
    # Export to JSON
    if st.button("📄 Export to JSON", use_container_width=True):
        export_data = {
            "metadata": notebook_metadata,
            "cells": cells
        }
        
        filename = f"{notebook_name}.json"
        filepath = os.path.join("data", filename)
        
        try:
            os.makedirs("data", exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=4, ensure_ascii=False)
            st.success(f"✅ Notebook exported to {filename}")
        except Exception as e:
            st.error(f"❌ Export failed: {str(e)}")
    
    # Export to Python
    if st.button("🐍 Export to Python", use_container_width=True):
        python_content = f'"""\nCodex Notebook: {notebook_name}\nGenerated: {datetime.now().isoformat()}\n"""\n\n'
        
        for i, cell in enumerate(cells):
            if cell["type"] == "text":
                python_content += f'# Text Cell {i+1}\n"""\n{cell["content"]}\n"""\n\n'
            elif cell["type"] == "code":
                python_content += f'# Code Cell {i+1}\n{cell["content"]}\n\n'
            elif cell["type"] == "prompt":
                python_content += f'# Prompt Cell {i+1}\n"""\n{cell["content"]}\n"""\n\n'
        
        filename = f"{notebook_name}.py"
        filepath = os.path.join("data", filename)
        
        try:
            os.makedirs("data", exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(python_content)
            st.success(f"✅ Python file exported to {filename}")
        except Exception as e:
            st.error(f"❌ Export failed: {str(e)}")
    
    st.divider()
    
    # Import functionality
    st.subheader("📂 Import Options")
    
    uploaded_file = st.file_uploader("Import JSON Notebook", type="json")
    if uploaded_file is not None:
        try:
            import_data = json.load(uploaded_file)
            if "cells" in import_data:
                st.session_state["cells"] = import_data["cells"]
                if "metadata" in import_data and "name" in import_data["metadata"]:
                    st.session_state["notebook_name"] = import_data["metadata"]["name"]
                st.success("✅ Notebook imported successfully!")
                st.rerun()
        except Exception as e:
            st.error(f"❌ Import failed: {str(e)}")
    
    st.divider()
    
    # Statistics
    st.subheader("📊 Notebook Stats")
    text_cells = len([c for c in cells if c["type"] == "text"])
    code_cells = len([c for c in cells if c["type"] == "code"])
    prompt_cells = len([c for c in cells if c["type"] == "prompt"])
    
    st.metric("Total Cells", len(cells))
    st.metric("Text Cells", text_cells)
    st.metric("Code Cells", code_cells)
    st.metric("Prompt Cells", prompt_cells)

# Footer
st.markdown("---")
st.markdown("🔥 **Codex Dominion Suite - Notebook Editor** | *Cycle 1 - Interactive Notebook Management*")

if __name__ == "__main__":
    print("📓 Codex Notebook Editor - Streamlit Application")
    print("Run with: streamlit run codex_notebook_editor.py --server.port 8502")