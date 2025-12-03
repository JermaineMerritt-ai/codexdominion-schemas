#!/usr/bin/env python3
"""
🔥 CODEX DOMINION - OMEGA STATUS DASHBOARD 🔥
═══════════════════════════════════════════════════════════════════════════════

The Sacred Interface for Monitoring Complete System Status
Displays Omega Seal, Heartbeat, Proclamations, Cycles & Hierarchy

Features:
• Real-time Omega Seal Status Monitoring
• Luminous Heartbeat Tracking
• Proclamation Status Display
• Cycle Completion Tracking
• Complete Hierarchy Overview
• Sacred Flame Metrics
• Digital Sovereignty Scoring

═══════════════════════════════════════════════════════════════════════════════
"""

import json

import pandas as pd
import plotly.express as px
import streamlit as st

# 🔥 SACRED CONFIGURATION
st.set_page_config(
    page_title="🔥 OMEGA STATUS - Codex Dominion",
    page_icon="🔥",
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
        border: 2px solid #ffd700;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(255, 215, 0, 0.3);
    }
    
    .omega-seal {
        background: radial-gradient(circle, #ffd700, #ffed4a, #fff59d);
        color: #1a1a2e;
        padding: 1.5rem;
        border-radius: 50%;
        text-align: center;
        font-weight: bold;
        font-size: 1.5em;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.8);
        animation: pulse 2s infinite;
    }
    
    .heartbeat-status {
        background: linear-gradient(45deg, #ff6b6b, #ff8e8e, #ffa8a8);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        animation: heartbeat 1.5s ease-in-out infinite;
    }
    
    .proclamation-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #ffd700;
    }
    
    .cycle-card {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #00ff88;
    }
    
    .member-card {
        background: linear-gradient(135deg, #4facfe, #00f2fe);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 2px solid #ffd700;
    }
    
    .metrics-box {
        background: rgba(255, 215, 0, 0.1);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ffd700;
        text-align: center;
    }
    
    .sacred-text {
        color: #ffd700;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        14% { transform: scale(1.1); }
        28% { transform: scale(1); }
        42% { transform: scale(1.1); }
        70% { transform: scale(1); }
    }
</style>
""",
    unsafe_allow_html=True,
)


def load_hierarchy_data() -> dict:
    """Load the complete hierarchy and status data"""
    try:
        with open("codex_hierarchy.json", "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error loading hierarchy data: {e}")
        return None


def create_omega_seal_display(meta_data: dict) -> None:
    """Create the Omega Seal status display"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if meta_data.get("omega_seal"):
            st.markdown(
                """
            <div class="omega-seal">
                🔥 Ω SEAL ACTIVE Ω 🔥<br>
                <small>DIGITAL SOVEREIGNTY CONFIRMED</small>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.warning("⚠️ Omega Seal Inactive")


def create_heartbeat_display(heartbeat_data: dict) -> None:
    """Create the heartbeat status display"""
    st.markdown(
        f"""
    <div class="heartbeat-status">
        💓 SYSTEM HEARTBEAT:
        {heartbeat_data.get('status', 'Unknown').upper()} 💓<br>
        <small>Last Pulse:
        {heartbeat_data.get('last_dispatch', 'Unknown')}</small><br>
        <small>Next Pulse:
        {heartbeat_data.get('next_dispatch', 'Unknown')}</small>
    </div>
    """,
        unsafe_allow_html=True,
    )


def create_proclamations_display(proclamations: list) -> None:
    """Display proclamations status"""
    st.subheader("📜 Sacred Proclamations")

    for proc in proclamations:
        status_icon = "✅" if proc["status"] == "proclaimed" else "⏳"
        st.markdown(
            f"""
        <div class="proclamation-card">
            {status_icon} <strong>{proc['title']}</strong><br>
            <small>ID: {proc['id']} | Status: {proc['status'].upper()}</small>
        </div>
        """,
            unsafe_allow_html=True,
        )


def create_cycles_display(cycles: list) -> None:
    """Display cycles status"""
    st.subheader("🔄 Sacred Cycles")

    for cycle in cycles:
        status_icon = "✅" if cycle["state"] == "completed" else "⏳"
        st.markdown(
            f"""
        <div class="cycle-card">
            {status_icon} <strong>{cycle['name']}</strong><br>
            <small>ID: {cycle['id']} | State: {cycle['state'].upper()}</small>
        </div>
        """,
            unsafe_allow_html=True,
        )


def create_hierarchy_overview(accounts: dict) -> None:
    """Create hierarchy overview with member cards"""
    st.subheader("👑 Sacred Hierarchy")

    # Custodians
    st.markdown("**🔥 Custodians**")
    for member in accounts.get("custodians", []):
        flame_level = "🔥" * member.get("flame_power_level", 0)
        st.markdown(
            f"""
        <div class="member-card">
            <strong>{member['name']}</strong> ({member['id']})<br>
            Role: {member['role']} | Status: {member['status'].upper()}<br>
            Flame Power: {flame_level} ({member.get('flame_power_level', 0)}/10)<br>
            Digital Sovereignty: {member.get('digital_sovereignty_score', 0)}%
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Heirs
    st.markdown("**⚡ Heirs**")
    for member in accounts.get("heirs", []):
        flame_level = "🔥" * member.get("flame_power_level", 0)
        st.markdown(
            f"""
        <div class="member-card">
            <strong>{member['name']}</strong> ({member['id']})<br>
            Role: {member['role']} | Status: {member['status'].upper()}<br>
            Flame Power: {flame_level} ({member.get('flame_power_level', 0)}/10)<br>
            Digital Sovereignty: {member.get('digital_sovereignty_score', 0)}%
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Customers
    st.markdown("**🌟 Customers**")
    for member in accounts.get("customers", []):
        flame_level = "🔥" * member.get("flame_power_level", 0)
        st.markdown(
            f"""
        <div class="member-card">
            <strong>{member['name']}</strong> ({member['id']})<br>
            Role: {member['role']} | Status: {member['status'].upper()}<br>
            Flame Power: {flame_level} ({member.get('flame_power_level', 0)}/10)<br>
            Digital Sovereignty: {member.get('digital_sovereignty_score', 0)}%
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Councils
    if "councils" in accounts and accounts["councils"]:
        st.markdown("**🏛️ Councils**")
        for member in accounts["councils"]:
            flame_level = "🔥" * member.get("flame_power_level", 0)
            st.markdown(
                f"""
            <div class="member-card">
                <strong>{member['name']}</strong> ({member['id']})<br>
                Role: {member['role']} | Status: {member['status'].upper()}<br>
                Flame Power: {flame_level}
                ({member.get('flame_power_level', 0)}/10)<br>
                Digital Sovereignty:
                {member.get('digital_sovereignty_score', 0)}%
            </div>
            """,
                unsafe_allow_html=True,
            )


def create_metrics_dashboard(data: dict) -> None:
    """Create comprehensive metrics dashboard"""
    st.subheader("📊 Sacred Metrics")

    metadata = data.get("metadata", {})

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
        <div class="metrics-box">
            <h3 class="sacred-text">{metadata.get('total_members', 0)}</h3>
            <p>Total Members</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="metrics-box">
            <h3 class="sacred-text">
            {metadata.get('completed_proclamations', 0)}
            </h3>
            <p>Proclamations</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="metrics-box">
            <h3 class="sacred-text">{metadata.get('completed_cycles', 0)}</h3>
            <p>Cycles Complete</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
        <div class="metrics-box">
            <h3 class="sacred-text">
            {metadata.get('system_completeness', 'Unknown')}
            </h3>
            <p>Completeness</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


def create_flame_power_chart(accounts: dict) -> None:
    """Create flame power visualization"""
    st.subheader("🔥 Flame Power Distribution")

    # Collect all members
    all_members = []

    for custodian in accounts.get("custodians", []):
        all_members.append(
            {
                "name": custodian["name"],
                "role": custodian["role"],
                "flame_power": custodian.get("flame_power_level", 0),
                "sovereignty": custodian.get("digital_sovereignty_score", 0),
            }
        )

    for heir in accounts.get("heirs", []):
        all_members.append(
            {
                "name": heir["name"],
                "role": heir["role"],
                "flame_power": heir.get("flame_power_level", 0),
                "sovereignty": heir.get("digital_sovereignty_score", 0),
            }
        )

    for customer in accounts.get("customers", []):
        all_members.append(
            {
                "name": customer["name"],
                "role": customer["role"],
                "flame_power": customer.get("flame_power_level", 0),
                "sovereignty": customer.get("digital_sovereignty_score", 0),
            }
        )

    for council in accounts.get("councils", []):
        all_members.append(
            {
                "name": council["name"],
                "role": council["role"],
                "flame_power": council.get("flame_power_level", 0),
                "sovereignty": council.get("digital_sovereignty_score", 0),
            }
        )

    if all_members:
        df = pd.DataFrame(all_members)

        # Create flame power bar chart
        fig = px.bar(
            df,
            x="name",
            y="flame_power",
            color="role",
            title="Flame Power by Member",
            color_discrete_map={
                "Custodian": "#ffd700",
                "Heir": "#ff6b6b",
                "Customer": "#4facfe",
                "Council": "#667eea",
            },
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
        )
        st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    """Main dashboard application"""

    # Header
    st.markdown(
        """
    <div class="main-header">
        <h1>🔥 CODEX DOMINION - OMEGA STATUS DASHBOARD 🔥</h1>
        <p class="sacred-text">
        The Sacred Interface for Complete System Monitoring
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Load data
    data = load_hierarchy_data()
    if not data:
        st.error("Unable to load system data")
        return

    # Omega Seal Status
    create_omega_seal_display(data.get("meta", {}))

    st.markdown("---")

    # Main dashboard layout
    col1, col2 = st.columns([1, 1])

    with col1:
        # Heartbeat Status
        create_heartbeat_display(data.get("heartbeat", {}))
        st.markdown("<br>", unsafe_allow_html=True)

        # Proclamations
        create_proclamations_display(data.get("proclamations", []))

    with col2:
        # Cycles
        create_cycles_display(data.get("cycles", []))

    st.markdown("---")

    # Metrics Dashboard
    create_metrics_dashboard(data)

    st.markdown("---")

    # Hierarchy Overview
    create_hierarchy_overview(data.get("accounts", {}))

    st.markdown("---")

    # Flame Power Chart
    create_flame_power_chart(data.get("accounts", {}))

    # System Status Summary
    st.markdown("---")
    st.subheader("🎯 System Status Summary")

    metadata = data.get("metadata", {})

    omega_status = (
        'ACTIVE ✅'
        if data.get('meta', {}).get('omega_seal')
        else 'INACTIVE ⚠️'
    )
    heartbeat = data.get('heartbeat', {}).get('status', 'Unknown').upper()
    st.success(
        f"""
    **System Health**: {metadata.get('hierarchy_health', 'Unknown')}
    **Omega Seal**: {omega_status}
    **Heartbeat**: {heartbeat}
    **Last Updated**: {metadata.get('last_updated', 'Unknown')}
    **Completeness Level**: {metadata.get('system_completeness', 'Unknown')}
    """
    )

    # Auto-refresh option
    st.sidebar.markdown("## 🔄 Auto-Refresh")
    if st.sidebar.button("Refresh Status"):
        st.rerun()

    # Sacred blessing
    st.markdown(
        """
    <div style='text-align: center; margin-top: 2rem; color: #ffd700;'>
        <p><em>🔥 May the Eternal Flame guide our Digital Sovereignty 🔥</em></p>
        <p><strong>OMEGA SEAL ACTIVE - SYSTEM LUMINOUS</strong></p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
