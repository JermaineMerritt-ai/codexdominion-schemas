#!/usr/bin/env python3
"""
🔥 CODEX DOMINION - ENHANCED COUNCIL OVERSIGHT 🔥
═══════════════════════════════════════════════════════════════════════════════

Sacred Interface for Radiant Council Authority
Review, Affirm, and Silence Community Contributions

Features:
• Sacred Council Authority Interface
• Contribution Review and Status Management
• Affirm/Silence Authority Controls
• Complete Oversight Analytics
• Sacred Styling and Animations

═══════════════════════════════════════════════════════════════════════════════
"""

import json
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

LEDGER_PATH = "codex_ledger.json"

# 🔥 SACRED CONFIGURATION
st.set_page_config(
    page_title="🏛️ COUNCIL OVERSIGHT - Codex Dominion",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 🎨 SACRED STYLING
st.markdown(
    """
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid #ffd700;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 12px 40px rgba(255, 215, 0, 0.4);
    }
    
    .council-seal {
        background: radial-gradient(circle, #667eea, #764ba2, #9a4993);
        color: white;
        padding: 2rem;
        border-radius: 50%;
        text-align: center;
        font-weight: bold;
        font-size: 2em;
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.8);
        animation: council-glow 3s infinite;
        margin: 1rem auto;
        width: 150px;
        height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .pending-contribution {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 6px solid #ffd700;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
        animation: pending-pulse 2s infinite;
    }
    
    .affirmed-contribution {
        background: linear-gradient(135deg, #4facfe, #00f2fe);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 6px solid #00ff88;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.3);
    }
    
    .silenced-contribution {
        background: linear-gradient(135deg, #a8edea, #fed6e3);
        color: #1a1a2e;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 6px solid #9d50bb;
        box-shadow: 0 8px 25px rgba(168, 237, 234, 0.3);
        opacity: 0.7;
    }
    
    .council-metrics {
        background: rgba(102, 126, 234, 0.15);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #667eea;
        text-align: center;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    .sacred-text {
        color: #ffd700;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.8);
    }
    
    .council-text {
        color: #667eea;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(102, 126, 234, 0.8);
    }
    
    .action-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        border: none;
        font-weight: bold;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    @keyframes council-glow {
        0%, 100% { box-shadow: 0 0 30px rgba(102, 126, 234, 0.8); }
        50% { box-shadow: 0 0 45px rgba(102, 126, 234, 1.2); }
    }
    
    @keyframes pending-pulse {
        0%, 100% { border-left-color: #ffd700; }
        50% { border-left-color: #ff6b6b; }
    }
</style>
""",
    unsafe_allow_html=True,
)


def load_ledger():
    """Load the sacred ledger"""
    try:
        with open(LEDGER_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading ledger: {e}")
        return None


def save_ledger(data):
    """Save the ledger with timestamp"""
    try:
        data["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
        with open(LEDGER_PATH, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving ledger: {e}")
        return False


def display_council_seal():
    """Display the Radiant Council seal"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            """
        <div class="council-seal">
            🏛️<br>
            <small style="font-size: 0.4em;">RADIANT COUNCIL</small>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
        <div style='text-align: center; margin-top: 1rem;'>
            <p class="council-text"><strong>Collective Wisdom Authority</strong></p>
            <p class="sacred-text">Sacred Affirmation Power</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


def display_oversight_metrics(contributions):
    """Display council oversight metrics"""
    st.subheader("🏛️ Council Authority Metrics")

    total_contributions = len(contributions)
    pending_count = len([c for c in contributions if not c.get("status")])
    affirmed_count = len([c for c in contributions if c.get("status") == "affirmed"])
    silenced_count = len([c for c in contributions if c.get("status") == "silenced"])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
        <div class="council-metrics">
            <h3 class="council-text">{total_contributions}</h3>
            <p>Total Contributions</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="council-metrics">
            <h3 class="sacred-text">{pending_count}</h3>
            <p>Awaiting Council</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="council-metrics">
            <h3 style="color: #00ff88;">{affirmed_count}</h3>
            <p>Council Affirmed</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
        <div class="council-metrics">
            <h3 style="color: #9d50bb;">{silenced_count}</h3>
            <p>Council Silenced</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


def display_pending_contributions(data):
    """Display pending contributions for council review"""
    st.subheader("⚖️ Contributions Awaiting Council Authority")

    contributions = data.get("contributions", [])
    pending = [c for c in contributions if not c.get("status")]

    if not pending:
        st.success("✅ All contributions have been reviewed by the Radiant Council")
        st.info("No pending contributions require council authority at this time")
        return

    st.markdown(f"**{len(pending)} contributions await your sacred authority**")

    for item in pending:
        contribution_id = item.get("id", "Unknown")
        contributor_name = item.get("name", "Anonymous")
        contributor_role = item.get("role", "Unknown")
        contribution_kind = item.get("kind", "Unknown")
        contribution_text = item.get("text", "")
        contribution_time = item.get("timestamp", "Unknown time")

        st.markdown(
            f"""
        <div class="pending-contribution">
            <strong>🔥 {contribution_id} — {contributor_name} ({contributor_role})</strong><br>
            <small><strong>Type:</strong> {contribution_kind} | <strong>Submitted:</strong> {contribution_time}</small><br>
            <div style="margin-top: 1rem; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
                <em>"{contribution_text}"</em>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Council action buttons
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            if st.button(
                f"✅ Affirm {contribution_id}", key=f"affirm_{contribution_id}"
            ):
                item["status"] = "affirmed"
                item["council_action"] = "AFFIRMED_BY_RADIANT_COUNCIL"
                item["council_timestamp"] = datetime.utcnow().isoformat() + "Z"

                if save_ledger(data):
                    st.success(f"🏛️ Council has AFFIRMED contribution {contribution_id}")
                    st.rerun()

        with col2:
            if st.button(
                f"🤫 Silence {contribution_id}", key=f"silence_{contribution_id}"
            ):
                item["status"] = "silenced"
                item["council_action"] = "SILENCED_BY_RADIANT_COUNCIL"
                item["council_timestamp"] = datetime.utcnow().isoformat() + "Z"

                if save_ledger(data):
                    st.success(f"🏛️ Council has SILENCED contribution {contribution_id}")
                    st.rerun()

        with col3:
            st.markdown(
                f"<small>*Council authority: Affirm to bless, Silence to remove from continuum*</small>",
                unsafe_allow_html=True,
            )

        st.markdown("---")


def display_council_history(contributions):
    """Display council decision history"""
    st.subheader("📚 Council Decision History")

    reviewed = [c for c in contributions if c.get("status")]

    if not reviewed:
        st.info("No council decisions recorded yet")
        return

    for item in reviewed:
        status = item.get("status", "unknown")
        action = item.get("council_action", "Unknown action")
        council_time = item.get("council_timestamp", "Unknown time")

        if status == "affirmed":
            card_class = "affirmed-contribution"
            icon = "✅"
        else:
            card_class = "silenced-contribution"
            icon = "🤫"

        st.markdown(
            f"""
        <div class="{card_class}">
            <strong>{icon} {item['id']} — {item['name']} ({item['role']})</strong><br>
            <small><strong>Council Action:</strong> {action}</small><br>
            <small><strong>Decision Time:</strong> {council_time}</small><br>
            <small><strong>Original Text:</strong> "{item.get('text', '')[:100]}{'...' if len(item.get('text', '')) > 100 else ''}"</small>
        </div>
        """,
            unsafe_allow_html=True,
        )


def create_council_analytics(contributions):
    """Create analytics for council decisions"""
    st.subheader("📊 Council Decision Analytics")

    if not contributions:
        st.info("No contribution data for analytics")
        return

    # Prepare data
    status_counts = {"pending": 0, "affirmed": 0, "silenced": 0}

    for contrib in contributions:
        status = contrib.get("status", "pending")
        if status == "affirmed":
            status_counts["affirmed"] += 1
        elif status == "silenced":
            status_counts["silenced"] += 1
        else:
            status_counts["pending"] += 1

    # Create pie chart
    if sum(status_counts.values()) > 0:
        fig = px.pie(
            values=list(status_counts.values()),
            names=["Pending Council", "Council Affirmed", "Council Silenced"],
            title="Council Decision Distribution",
            color_discrete_map={
                "Pending Council": "#ff6b6b",
                "Council Affirmed": "#00ff88",
                "Council Silenced": "#9d50bb",
            },
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
        )
        st.plotly_chart(fig, use_container_width=True)


def main():
    """Main council oversight application"""

    # Header
    st.markdown(
        """
    <div class="main-header">
        <h1>🏛️ CODEX DOMINION - RADIANT COUNCIL OVERSIGHT 🏛️</h1>
        <p class="council-text">Sacred Authority for Community Contribution Review</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Display Council Seal
    display_council_seal()

    st.markdown("---")

    # Load ledger data
    data = load_ledger()
    if not data:
        st.error("Unable to load sacred ledger")
        return

    contributions = data.get("contributions", [])

    # Display metrics
    display_oversight_metrics(contributions)

    st.markdown("---")

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(
        ["⚖️ Pending Review", "📚 Decision History", "📊 Analytics"]
    )

    with tab1:
        display_pending_contributions(data)

    with tab2:
        display_council_history(contributions)

    with tab3:
        create_council_analytics(contributions)

    # Sidebar controls
    st.sidebar.markdown("## 🏛️ Council Controls")

    if st.sidebar.button("🔄 Refresh Ledger"):
        st.rerun()

    if st.sidebar.button("📊 Generate Council Report"):
        st.sidebar.success("📋 Council Report Generated")
        pending_count = len([c for c in contributions if not c.get("status")])
        affirmed_count = len(
            [c for c in contributions if c.get("status") == "affirmed"]
        )
        silenced_count = len(
            [c for c in contributions if c.get("status") == "silenced"]
        )

        st.sidebar.write(f"**Pending:** {pending_count}")
        st.sidebar.write(f"**Affirmed:** {affirmed_count}")
        st.sidebar.write(f"**Silenced:** {silenced_count}")
        st.sidebar.write(f"**Total Reviewed:** {affirmed_count + silenced_count}")

    # Footer blessing
    st.markdown(
        """
    <div style='text-align: center; margin-top: 3rem; color: #667eea;'>
        <p><em>🏛️ Through Collective Wisdom, We Guide the Sacred Continuum 🏛️</em></p>
        <p><strong>RADIANT COUNCIL AUTHORITY PROTECTS THE COMMUNITY</strong></p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
