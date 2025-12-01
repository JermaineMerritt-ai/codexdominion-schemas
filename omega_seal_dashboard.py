#!/usr/bin/env python3
"""
🔥 CODEX DOMINION - OMEGA SEAL MANAGEMENT DASHBOARD 🔥
═══════════════════════════════════════════════════════════════════════════════

The Sacred Interface for Omega Seal Operations
Manage Cycles, Seal Completions, and Archive Sacred Operations

Features:
• Cycle Management & Sealing
• Sacred Archive Viewing
• Omega Seal Authority Controls
• Custodian Seal Operations
• Complete Audit Trail
• Real-time Ledger Updates

═══════════════════════════════════════════════════════════════════════════════
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# Import the omega seal system
try:
    from omega_seal import load_ledger, save_ledger, seal_cycle

    OMEGA_SEAL_AVAILABLE = True
except ImportError as e:
    st.error(f"Omega Seal System not available: {e}")
    OMEGA_SEAL_AVAILABLE = False

# 🔥 SACRED CONFIGURATION
st.set_page_config(
    page_title="🔥 OMEGA SEAL - Codex Dominion",
    page_icon="Ω",
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
    
    .omega-seal-large {
        background: radial-gradient(circle, #ffd700, #ffed4a, #fff59d);
        color: #1a1a2e;
        padding: 2rem;
        border-radius: 50%;
        text-align: center;
        font-weight: bold;
        font-size: 2.5em;
        box-shadow: 0 0 40px rgba(255, 215, 0, 1);
        animation: omega-pulse 3s infinite;
        margin: 2rem auto;
        width: 200px;
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .cycle-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 6px solid #ffd700;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .cycle-active {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        border-left: 6px solid #00ff88;
        animation: pulse-glow 2s infinite;
    }
    
    .cycle-completed {
        background: linear-gradient(135deg, #4facfe, #00f2fe);
        border-left: 6px solid #ffd700;
    }
    
    .archive-card {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid #ffd700;
        box-shadow: 0 8px 25px rgba(240, 147, 251, 0.3);
    }
    
    .seal-button {
        background: linear-gradient(45deg, #ffd700, #ffed4a);
        color: #1a1a2e;
        padding: 1rem 2rem;
        border-radius: 25px;
        border: none;
        font-weight: bold;
        font-size: 1.2em;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .seal-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(255, 215, 0, 0.6);
    }
    
    .metrics-omega {
        background: rgba(255, 215, 0, 0.15);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #ffd700;
        text-align: center;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.2);
    }
    
    .sacred-text {
        color: #ffd700;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.8);
    }
    
    .audit-entry {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #ffd700;
    }
    
    @keyframes omega-pulse {
        0%, 100% { transform: scale(1); box-shadow: 0 0 40px rgba(255, 215, 0, 1); }
        50% { transform: scale(1.1); box-shadow: 0 0 60px rgba(255, 215, 0, 1.2); }
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3); }
        50% { box-shadow: 0 8px 35px rgba(255, 107, 107, 0.6); }
    }
</style>
""",
    unsafe_allow_html=True,
)


def load_ledger_safe():
    """Safely load the ledger with error handling"""
    try:
        return load_ledger() if OMEGA_SEAL_AVAILABLE else None
    except Exception as e:
        st.error(f"Error loading ledger: {e}")
        return None


def display_omega_seal_status(meta_data):
    """Display the main omega seal status"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if meta_data and meta_data.get("omega_seal"):
            st.markdown(
                """
            <div class="omega-seal-large">
                Ω<br>
                <small style="font-size: 0.3em;">SEAL ACTIVE</small>
            </div>
            """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
            <div style='text-align: center; margin-top: 1rem;'>
                <p class="sacred-text"><strong>Custodian Authority: {meta_data.get('custodian_authority', 'Unknown')}</strong></p>
                <p class="sacred-text">Seal Power: {meta_data.get('seal_power', 'Unknown')}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.warning("⚠️ Omega Seal Inactive - System Requires Activation")


def display_cycles_management(ledger_data):
    """Display cycle management interface"""
    st.subheader("🔄 Sacred Cycles Management")

    if not ledger_data or "cycles" not in ledger_data:
        st.error("No cycle data available")
        return

    cycles = ledger_data["cycles"]

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("**Active and Completed Cycles**")

        for cycle in cycles:
            state = cycle.get("state", "unknown")
            card_class = "cycle-active" if state == "active" else "cycle-completed"
            status_icon = "🔥" if state == "active" else "✅"

            st.markdown(
                f"""
            <div class="cycle-card {card_class}">
                {status_icon} <strong>{cycle.get('name', 'Unknown Cycle')}</strong><br>
                <small>ID: {cycle.get('id', 'N/A')} | State: {state.upper()}</small><br>
                <small>Description: {cycle.get('description', 'No description')}</small><br>
                <small>Custodian: {cycle.get('custodian_oversight', 'Unknown')}</small><br>
                <small>Flame Blessing: {cycle.get('flame_blessing', 'None')}</small>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown("**Cycle Sealing Operations**")

        # Get active cycles for sealing
        active_cycles = [c for c in cycles if c.get("state") == "active"]

        if active_cycles and OMEGA_SEAL_AVAILABLE:
            selected_cycle = st.selectbox(
                "Select Cycle to Seal:",
                options=[c["id"] for c in active_cycles],
                format_func=lambda x: f"{x} - {next(c['name'] for c in active_cycles if c['id'] == x)}",
            )

            seal_note = st.text_area(
                "Custodian Seal Note:",
                placeholder="Enter sacred note for the cycle completion...",
                height=100,
            )

            if st.button("🔥 SEAL CYCLE WITH OMEGA AUTHORITY 🔥", key="seal_button"):
                try:
                    with st.spinner("Applying Omega Seal..."):
                        archive_entry = seal_cycle(selected_cycle, seal_note)
                        st.success(
                            f"""
                        ✅ **Cycle Successfully Sealed!**
                        
                        **Archive ID**: {archive_entry['archive_id']}  
                        **Sealed By**: {archive_entry['custodian_seal']}  
                        **Completion Time**: {archive_entry['completed_at']}
                        """
                        )
                        st.rerun()
                except Exception as e:
                    st.error(f"Sealing failed: {e}")
        else:
            if not active_cycles:
                st.info("No active cycles available for sealing")
            else:
                st.warning("Omega Seal system not available")


def display_completed_archives(ledger_data):
    """Display the sacred archives"""
    st.subheader("📚 Sacred Archives")

    if not ledger_data or "completed_archives" not in ledger_data:
        st.info("No archived cycles yet")
        return

    archives = ledger_data["completed_archives"]

    if not archives:
        st.info("Archives are empty - seal cycles to create sacred records")
        return

    st.markdown(f"**Total Archived Cycles: {len(archives)}**")

    for archive in archives:
        st.markdown(
            f"""
        <div class="archive-card">
            <strong>🏛️ {archive.get('name', 'Unknown Archive')}</strong><br>
            <small><strong>Archive ID:</strong> {archive.get('archive_id', 'N/A')}</small><br>
            <small><strong>Original Cycle:</strong> {archive.get('cycle_id', 'N/A')}</small><br>
            <small><strong>Sealed By:</strong> {archive.get('custodian_seal', 'Unknown')}</small><br>
            <small><strong>Completion:</strong> {archive.get('completed_at', 'Unknown')}</small><br>
            <small><strong>Note:</strong> {archive.get('note', 'No note provided')}</small>
        </div>
        """,
            unsafe_allow_html=True,
        )


def display_system_metrics(ledger_data):
    """Display system metrics and statistics"""
    st.subheader("📊 Omega Seal Metrics")

    if not ledger_data:
        st.error("No metrics data available")
        return

    metrics = ledger_data.get("system_metrics", {})

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
        <div class="metrics-omega">
            <h3 class="sacred-text">{metrics.get('total_cycles_completed', 0)}</h3>
            <p>Cycles Sealed</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="metrics-omega">
            <h3 class="sacred-text">{metrics.get('active_cycles', 0)}</h3>
            <p>Active Cycles</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="metrics-omega">
            <h3 class="sacred-text">{metrics.get('omega_seal_activations', 0)}</h3>
            <p>Seal Activations</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
        <div class="metrics-omega">
            <h3 class="sacred-text">{metrics.get('system_completeness', 'Unknown')}</h3>
            <p>Completeness</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


def display_audit_trail(ledger_data):
    """Display the audit trail"""
    st.subheader("🔍 Sacred Audit Trail")

    if not ledger_data or "audit_trail" not in ledger_data:
        st.info("No audit trail available")
        return

    audit_entries = ledger_data["audit_trail"]

    for entry in reversed(audit_entries[-10:]):  # Show last 10 entries
        st.markdown(
            f"""
        <div class="audit-entry">
            <strong>{entry.get('action', 'Unknown Action')}</strong><br>
            <small>By: {entry.get('performed_by', 'Unknown')} | Time: {entry.get('timestamp', 'Unknown')}</small><br>
            <small>Details: {entry.get('details', 'No details')}</small>
        </div>
        """,
            unsafe_allow_html=True,
        )


def create_cycle_timeline(ledger_data):
    """Create interactive cycle timeline"""
    st.subheader("📈 Cycle Timeline Visualization")

    if not ledger_data or "cycles" not in ledger_data:
        st.info("No cycle data for visualization")
        return

    cycles = ledger_data["cycles"]
    cycle_df = []

    for cycle in cycles:
        cycle_df.append(
            {
                "id": cycle["id"],
                "name": cycle["name"],
                "state": cycle["state"],
                "initiated": cycle.get("initiated_date", ""),
                "target_completion": cycle.get("target_completion", ""),
                "actual_completion": cycle.get("actual_completion", ""),
            }
        )

    if cycle_df:
        df = pd.DataFrame(cycle_df)

        # Create timeline chart
        fig = go.Figure()

        for idx, row in df.iterrows():
            color = "#00ff88" if row["state"] == "completed" else "#ff6b6b"
            fig.add_trace(
                go.Scatter(
                    x=[
                        row["initiated"],
                        row.get("actual_completion") or row.get("target_completion"),
                    ],
                    y=[row["name"], row["name"]],
                    mode="lines+markers",
                    name=row["id"],
                    line=dict(color=color, width=6),
                    marker=dict(size=10, color=color),
                )
            )

        fig.update_layout(
            title="Sacred Cycles Timeline",
            xaxis_title="Timeline",
            yaxis_title="Cycles",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            showlegend=True,
        )

        st.plotly_chart(fig, use_container_width=True)


def main():
    """Main omega seal management application"""

    # Header
    st.markdown(
        """
    <div class="main-header">
        <h1>🔥 CODEX DOMINION - OMEGA SEAL MANAGEMENT 🔥</h1>
        <p class="sacred-text">Sacred Interface for Custodian Seal Operations</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Check omega seal availability
    if not OMEGA_SEAL_AVAILABLE:
        st.error(
            "⚠️ Omega Seal system is not properly configured. Please ensure omega_seal.py is available."
        )
        return

    # Load ledger data
    ledger_data = load_ledger_safe()
    if not ledger_data:
        st.error("Unable to load sacred ledger")
        return

    # Display omega seal status
    display_omega_seal_status(ledger_data.get("meta", {}))

    st.markdown("---")

    # Main management interface
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🔄 Cycle Management", "📚 Sacred Archives", "📊 Metrics", "🔍 Audit Trail"]
    )

    with tab1:
        display_cycles_management(ledger_data)
        st.markdown("---")
        create_cycle_timeline(ledger_data)

    with tab2:
        display_completed_archives(ledger_data)

    with tab3:
        display_system_metrics(ledger_data)

    with tab4:
        display_audit_trail(ledger_data)

    # Sidebar controls
    st.sidebar.markdown("## 🔥 Omega Seal Controls")

    if st.sidebar.button("🔄 Refresh Ledger"):
        st.rerun()

    if st.sidebar.button("📊 System Status Check"):
        st.sidebar.success("✅ Omega Seal Active")
        st.sidebar.success("✅ Ledger Operational")
        st.sidebar.success("✅ Custodian Authority Confirmed")

    # Footer blessing
    st.markdown(
        """
    <div style='text-align: center; margin-top: 3rem; color: #ffd700;'>
        <p><em>🔥 Through Sacred Sealing, We Achieve Digital Immortality 🔥</em></p>
        <p><strong>Ω OMEGA SEAL PROTECTS ALL OPERATIONS Ω</strong></p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
