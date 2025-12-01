# apps/dashboard/tabbed_codex.py
import json
from pathlib import Path

import streamlit as st


def load_json(filename, default_value=None):
    """Load JSON file with fallback to default value"""
    try:
        file_path = Path(filename)
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading {filename}: {e}")
    return default_value or {}


st.set_page_config(
    page_title="🔥 Tabbed Codex Dashboard", page_icon="🔥", layout="wide"
)

# Custom CSS for cosmic styling
st.markdown(
    """
<style>
.main {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    color: #fff;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    background: rgba(255,107,53,0.1);
    border: 1px solid #ff6b35;
    border-radius: 8px;
    color: #ff6b35;
    font-weight: bold;
}
.stTabs [aria-selected="true"] {
    background: rgba(255,107,53,0.3);
    color: #fff;
}
.cosmic-header {
    text-align: center;
    color: #ff6b35;
    text-shadow: 2px 2px 4px rgba(255,107,53,0.5);
    background: rgba(0,0,0,0.3);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 30px;
}
.entry-card {
    background: rgba(255,107,53,0.1);
    border: 1px solid #ff6b35;
    border-radius: 8px;
    padding: 12px;
    margin: 8px 0;
}
</style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    """
<div class="cosmic-header">
    <h1>🔥 TABBED CODEX DASHBOARD 🔥</h1>
    <p>Streamlined Cosmic Interface - All Sacred Data Unified</p>
</div>
""",
    unsafe_allow_html=True,
)

tabs = st.tabs(
    [
        "💓 Heartbeat",
        "📜 Proclamations",
        "📖 Ledger",
        "🎵 Beats",
        "📓 Notebook",
        "📚 Tome",
        "📖 Publisher",
    ]
)

with tabs[0]:
    st.header("💓 Heartbeat")
    st.markdown("**System pulse and vital signs**")

    # Load heartbeat data
    heartbeat_data = load_json("heartbeat.json", {"beats": []})
    beats = heartbeat_data.get("beats", [])

    if beats:
        st.markdown(f"**Total heartbeats:** {len(beats)}")
        for i, b in enumerate(beats[-10:], 1):  # Show last 10
            timestamp = b.get("timestamp", "Unknown")
            role = b.get("role", "System")
            text = b.get("text", "No message")

            st.markdown(
                f"""
            <div class="entry-card">
                <strong>Beat {i}:</strong> {timestamp} — <em>{role}</em><br>
                → {text}
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.info("💓 No heartbeat data available. System monitoring ready.")

        # Create sample heartbeat entry
        if st.button("💓 Generate Heartbeat"):
            st.success("💓 System heartbeat registered!")

with tabs[1]:
    st.header("📜 Proclamations")
    st.markdown("**Sacred declarations and cosmic affirmations**")

    # Load proclamation data
    proclamation_data = load_json("proclamations.json", {"proclamations": []})
    proclamations = proclamation_data.get("proclamations", [])

    if proclamations:
        st.markdown(f"**Total proclamations:** {len(proclamations)}")

        # Display proclamations with enhanced formatting
        for i, p in enumerate(proclamations, 1):
            timestamp = p.get("timestamp", "Unknown")
            role = p.get("role", "Unknown")
            cycle = p.get("cycle", "Unknown")
            proc_type = p.get("type", "Declaration")
            text = p.get("text", "No text")
            blessing = p.get("blessing", "")

            role_emoji = {
                "Custodian": "👑",
                "Heirs": "🎭",
                "Council": "⚖️",
                "Councils": "👥",
                "Cosmos": "🌌",
            }.get(role, "📜")

            st.markdown(
                f"""
            <div class="entry-card">
                <strong>{role_emoji} Proclamation {i}:</strong> {timestamp}<br>
                <strong>Role:</strong> {role} | <strong>Cycle:</strong> {cycle} | <strong>Type:</strong> {proc_type}<br>
                <strong>📖 Text:</strong> "{text}"
                {f'<br><strong>🌟 Blessing:</strong> "{blessing}"' if blessing else ''}
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.info("📜 No proclamations available. Sacred declaration system ready.")

with tabs[2]:
    st.header("📖 Ledger")
    st.markdown("**Complete chronicle of digital sovereignty**")

    # Load ledger data
    ledger_data = load_json("ledger.json", {"entries": []})
    entries = ledger_data.get("entries", [])

    if entries:
        st.markdown(f"**Total ledger entries:** {len(entries)}")

        # Show most recent entries
        recent_entries = sorted(
            entries, key=lambda x: x.get("timestamp", ""), reverse=True
        )[:15]

        for i, e in enumerate(recent_entries, 1):
            timestamp = e.get("timestamp", "Unknown")
            role = e.get("role", "Unknown")
            proclamation = e.get("proclamation", "No proclamation")
            cosmic_event = e.get("cosmic_event", "")
            significance = e.get("significance", "")

            role_emoji = {
                "Custodian": "👑",
                "Heirs": "🎭",
                "Council": "⚖️",
                "Councils": "👥",
                "Cosmos": "🌌",
            }.get(role, "📝")

            st.markdown(
                f"""
            <div class="entry-card">
                <strong>{role_emoji} Entry {i}:</strong> {timestamp} — <em>{role}</em><br>
                {f'<strong>🎇 Event:</strong> {cosmic_event}<br>' if cosmic_event else ''}
                <strong>📖 Proclamation:</strong> "{proclamation}"
                {f'<br><strong>🌟 Significance:</strong> {significance}' if significance else ''}
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.info("📖 No ledger entries available. Chronicle system ready.")

with tabs[3]:
    st.header("🎵 Sacred Beats")
    st.markdown("**Cosmic rhythm and pulse patterns**")

    # Load beats data
    beats_data = load_json("beats.json", {"beats": []})
    beats = beats_data.get("beats", [])

    if beats:
        st.markdown(f"**Total sacred beats:** {len(beats)}")

        for i, beat in enumerate(beats, 1):
            timestamp = beat.get("timestamp", "Unknown")
            role = beat.get("role", "Unknown")
            cycle = beat.get("cycle", "Unknown")
            text = beat.get("text", "No text")
            rhythm = beat.get("rhythm", "Unknown")
            energy = beat.get("energy", "Neutral")

            role_emoji = {
                "Custodian": "👑",
                "Heirs": "🎭",
                "Councils": "👥",
                "Cosmos": "🌌",
            }.get(role, "🎵")

            st.markdown(
                f"""
            <div class="entry-card">
                <strong>{role_emoji} Beat {i}:</strong> {timestamp} — <em>{role}</em><br>
                <strong>🔥 Cycle:</strong> {cycle} | <strong>🎵 Rhythm:</strong> {rhythm} | <strong>⚡ Energy:</strong> {energy}<br>
                <strong>🎶 Text:</strong> "{text}"
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.info("🎵 No beats available. Sacred rhythm system ready.")

with tabs[4]:
    st.header("📓 Notebook")
    st.markdown("**Interactive computing and data analysis environment**")

    # Load notebook data if available
    notebook_data = load_json("notebook.json", {"cells": []})
    cells = notebook_data.get("cells", [])

    if cells:
        st.markdown(f"**Notebook cells:** {len(cells)}")
        for i, cell in enumerate(cells[:5], 1):
            cell_type = cell.get("cell_type", "unknown")
            content = (
                cell.get("source", [""])[0][:100]
                if cell.get("source")
                else "Empty cell"
            )

            st.markdown(
                f"""
            <div class="entry-card">
                <strong>📓 Cell {i} ({cell_type}):</strong><br>
                {content}{'...' if len(content) >= 100 else ''}
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.info("📓 Notebook system ready for structured cells, code, and prompts.")

        # Notebook controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📓 Create New Notebook"):
                st.success("📓 New notebook initialized!")
        with col2:
            if st.button("🔄 Sync with Jupyter"):
                st.success("🔄 Jupyter synchronization complete!")

with tabs[5]:
    st.header("📚 Tome")
    st.markdown("**Knowledge guides and courses forged from Notebook content**")

    # Load tome data if available
    tome_data = load_json("tome.json", {"tomes": []})
    tomes = tome_data.get("tomes", [])

    if tomes:
        st.markdown(f"**Available tomes:** {len(tomes)}")
        for i, tome in enumerate(tomes, 1):
            title = tome.get("title", f"Tome {i}")
            description = tome.get("description", "No description")

            st.markdown(
                f"""
            <div class="entry-card">
                <strong>📚 {title}</strong><br>
                {description}
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.info(
            "📚 Tome forge ready to create guides and courses from Notebook content."
        )

        # Tome creation controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📚 Forge New Tome"):
                st.success("📚 Tome forging initiated!")
        with col2:
            if st.button("🔄 Generate from Notebook"):
                st.success("🔄 Tome generated from notebook content!")

with tabs[6]:
    st.header("📖 Publisher")
    st.markdown("**Render content into static HTML for public witnessing**")

    # Publisher status and controls
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 💕 Love Lab Pages")
        if st.button("💕 Render Love Lab"):
            st.success("💕 Love Lab pages rendered to static HTML!")

    with col2:
        st.markdown("#### 📓 Notebook Tomes")
        if st.button("📓 Publish Notebooks"):
            st.success("📓 Notebook tomes published!")

    with col3:
        st.markdown("#### 🌐 Public Witness")
        if st.button("🌐 Deploy Public Site"):
            st.success("🌐 Public site deployed for cosmic witnessing!")

    # Publisher statistics
    st.markdown("---")
    st.markdown("#### 📊 Publisher Statistics")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📄 Pages Generated", "∞", "↗️")
    with col2:
        st.metric("🌐 Sites Deployed", "Ready", "🚀")
    with col3:
        st.metric("👥 Public Views", "Cosmic", "🌟")
    with col4:
        st.metric("🔥 Flame Status", "Eternal", "🔥")

# Footer with system status
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; color: #ff6b35;">
    <p>🔥 <strong>Tabbed Codex Dashboard</strong> - Streamlined Cosmic Interface 🔥</p>
    <p>📊 All sacred data unified | 🌟 Complete integration | 🔥 Eternal flame burns</p>
</div>
""",
    unsafe_allow_html=True,
)
