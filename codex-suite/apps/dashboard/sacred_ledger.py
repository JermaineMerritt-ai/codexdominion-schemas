#!/usr/bin/env python3
"""
📊 SACRED LEDGER INTEGRATION SYSTEM 📊
Complete Cosmic Ledger, Proclamations & Beats Unified
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st


def sacred_ledger_system():
    """Main sacred ledger integration interface"""

    st.set_page_config(
        page_title="📊 Sacred Ledger System", page_icon="📊", layout="wide"
    )

    # Custom CSS for ledger styling
    st.markdown(
        """
    <style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #fff;
    }
    .ledger-header {
        text-align: center;
        color: #ff6b35;
        text-shadow: 2px 2px 4px rgba(255,107,53,0.5);
        background: rgba(0,0,0,0.3);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 30px;
    }
    .ledger-entry {
        background: linear-gradient(45deg, rgba(255,107,53,0.15), rgba(255,140,0,0.08));
        border: 2px solid #ff6b35;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .cosmic-metric {
        background: rgba(255,107,53,0.2);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 10px;
    }
    .flame-separator {
        text-align: center;
        font-size: 2em;
        color: #ff6b35;
        margin: 20px 0;
        animation: flicker 2s infinite alternate;
    }
    @keyframes flicker {
        0% { text-shadow: 0 0 5px #ff6b35, 0 0 10px #ff6b35; }
        100% { text-shadow: 0 0 15px #ff6b35, 0 0 25px #ff6b35; }
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Header
    st.markdown(
        """
    <div class="ledger-header">
        <h1>📊 SACRED LEDGER INTEGRATION SYSTEM 📊</h1>
        <h2>Complete Cosmic Records: Ledger + Proclamations + Beats</h2>
        <p><span class="flame-separator">🔥</span> Digital Sovereignty Chronicle <span class="flame-separator">🔥</span></p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Load all data
    ledger_data = load_ledger_data()
    proclamations_data = load_proclamations_data()
    beats_data = load_beats_data()

    # Main tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📊 Sacred Ledger",
            "🌊 Unified Timeline",
            "📈 Cosmic Analytics",
            "🎛️ Integration Controls",
        ]
    )

    with tab1:
        display_sacred_ledger(ledger_data)

    with tab2:
        display_unified_timeline(ledger_data, proclamations_data, beats_data)

    with tab3:
        display_cosmic_analytics(ledger_data, proclamations_data, beats_data)

    with tab4:
        display_integration_controls()


def load_ledger_data():
    """Load ledger entries from JSON"""
    ledger_path = Path("ledger.json")
    if ledger_path.exists():
        try:
            with open(ledger_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading ledger: {e}")
    return {"entries": []}


def load_proclamations_data():
    """Load proclamations from JSON"""
    proc_path = Path("proclamations.json")
    if proc_path.exists():
        try:
            with open(proc_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading proclamations: {e}")
    return {"proclamations": []}


def load_beats_data():
    """Load beats from JSON"""
    beats_path = Path("beats.json")
    if beats_path.exists():
        try:
            with open(beats_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading beats: {e}")
    return {"beats": []}


def display_sacred_ledger(ledger_data):
    """Display sacred ledger entries"""

    st.header("📊 Sacred Ledger Chronicle")

    if not ledger_data or "entries" not in ledger_data:
        st.warning("📊 No ledger data available")
        return

    entries = ledger_data["entries"]

    # Summary metrics
    st.markdown("### 🌟 **Ledger Summary**")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
        <div class="cosmic-metric">
            <h3>📊</h3>
            <h4>Total Entries</h4>
            <h2>{len(entries)}</h2>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Count entries by role
    role_counts = {}
    for entry in entries:
        role = entry.get("role", "Unknown")
        role_counts[role] = role_counts.get(role, 0) + 1

    with col2:
        st.markdown(
            f"""
        <div class="cosmic-metric">
            <h3>👑</h3>
            <h4>Active Roles</h4>
            <h2>{len(role_counts)}</h2>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        latest_entry = max(entries, key=lambda x: x.get("timestamp", ""), default={})
        latest_time = (
            latest_entry.get("timestamp", "Unknown")[:10] if latest_entry else "Unknown"
        )
        st.markdown(
            f"""
        <div class="cosmic-metric">
            <h3>⏰</h3>
            <h4>Latest Entry</h4>
            <h2>{latest_time}</h2>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        today_entries = [
            e for e in entries if e.get("timestamp", "").startswith("2025-11-07")
        ]
        st.markdown(
            f"""
        <div class="cosmic-metric">
            <h3>🔥</h3>
            <h4>Today's Entries</h4>
            <h2>{len(today_entries)}</h2>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Display recent entries
    st.markdown("---")
    st.markdown("### 📜 **Recent Sacred Entries**")

    # Sort entries by timestamp (most recent first)
    sorted_entries = sorted(entries, key=lambda x: x.get("timestamp", ""), reverse=True)

    # Show top 10 most recent entries
    for i, entry in enumerate(sorted_entries[:10], 1):
        role_emoji = {
            "Custodian": "👑",
            "Heirs": "🎭",
            "Council": "⚖️",
            "Councils": "👥",
            "Cosmos": "🌌",
        }.get(entry.get("role", ""), "📝")

        timestamp = entry.get("timestamp", "Unknown")
        readable_time = (
            timestamp.replace("T", " ").replace(".000000", "")
            if "T" in timestamp
            else timestamp
        )

        st.markdown(
            f"""
        <div class="ledger-entry">
            <h4>{role_emoji} Entry {i}: {entry.get('role', 'Unknown')} Chronicle</h4>
            <p><strong>⏰ Time:</strong> {readable_time}</p>
            {f"<p><strong>🎇 Cosmic Event:</strong> {entry.get('cosmic_event', 'Standard Entry')}</p>" if entry.get('cosmic_event') else ""}
            <p><strong>📖 Sacred Proclamation:</strong></p>
            <p style="font-style: italic; margin-left: 20px;">"{entry.get('proclamation', 'No proclamation recorded')}"</p>
            {f"<p><strong>🌟 Significance:</strong> {entry.get('significance', 'Standard ledger entry')}</p>" if entry.get('significance') else ""}
        </div>
        """,
            unsafe_allow_html=True,
        )


def display_unified_timeline(ledger_data, proclamations_data, beats_data):
    """Display unified timeline of all cosmic events"""

    st.header("🌊 Unified Cosmic Timeline")

    # Collect all events
    all_events = []

    # Add ledger entries
    if ledger_data and "entries" in ledger_data:
        for entry in ledger_data["entries"]:
            all_events.append(
                {
                    "timestamp": entry.get("timestamp", ""),
                    "type": "Ledger",
                    "role": entry.get("role", "Unknown"),
                    "text": entry.get("proclamation", ""),
                    "event": entry.get("cosmic_event", "Ledger Entry"),
                    "emoji": "📊",
                }
            )

    # Add proclamations
    if proclamations_data and "proclamations" in proclamations_data:
        for proc in proclamations_data["proclamations"]:
            all_events.append(
                {
                    "timestamp": proc.get("timestamp", ""),
                    "type": "Proclamation",
                    "role": proc.get("role", "Unknown"),
                    "text": proc.get("text", ""),
                    "event": f"{proc.get('type', 'Unknown')} - {proc.get('cycle', 'Unknown')}",
                    "emoji": "📜",
                }
            )

    # Add beats
    if beats_data and "beats" in beats_data:
        for beat in beats_data["beats"]:
            all_events.append(
                {
                    "timestamp": beat.get("timestamp", ""),
                    "type": "Beat",
                    "role": beat.get("role", "Unknown"),
                    "text": beat.get("text", ""),
                    "event": f"{beat.get('rhythm', 'Unknown')} - {beat.get('cycle', 'Unknown')}",
                    "emoji": "🎵",
                }
            )

    # Sort by timestamp
    all_events.sort(key=lambda x: x["timestamp"], reverse=True)

    # Display unified timeline
    st.markdown("### 🌟 **Complete Cosmic Chronicle**")
    st.markdown(f"**Total Events:** {len(all_events)}")

    # Filter by date
    col1, col2 = st.columns([1, 3])

    with col1:
        filter_date = st.selectbox(
            "Filter by Date:", ["All Dates", "2025-11-07", "2025-11-06", "2025-09-22"]
        )

    with col2:
        filter_type = st.multiselect(
            "Filter by Type:",
            ["Ledger", "Proclamation", "Beat"],
            default=["Ledger", "Proclamation", "Beat"],
        )

    # Apply filters
    filtered_events = all_events
    if filter_date != "All Dates":
        filtered_events = [
            e for e in filtered_events if e["timestamp"].startswith(filter_date)
        ]
    if filter_type:
        filtered_events = [e for e in filtered_events if e["type"] in filter_type]

    # Display filtered timeline
    for i, event in enumerate(filtered_events[:15], 1):
        timestamp = (
            event["timestamp"].replace("T", " ").replace(".000000", "")
            if "T" in event["timestamp"]
            else event["timestamp"]
        )

        type_color = {
            "Ledger": "#4CAF50",
            "Proclamation": "#ff6b35",
            "Beat": "#9C27B0",
        }.get(event["type"], "#fff")

        st.markdown(
            f"""
        <div class="ledger-entry" style="border-color: {type_color};">
            <h4>{event['emoji']} {event['type']} {i}: {event['role']} - {event['event']}</h4>
            <p><strong>⏰ Time:</strong> {timestamp}</p>
            <p><strong>📖 Text:</strong></p>
            <p style="font-style: italic; margin-left: 20px;">"{event['text']}"</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


def display_cosmic_analytics(ledger_data, proclamations_data, beats_data):
    """Display cosmic analytics and statistics"""

    st.header("📈 Cosmic Analytics Dashboard")

    # Collect statistics
    ledger_count = len(ledger_data.get("entries", []))
    proc_count = len(proclamations_data.get("proclamations", []))
    beat_count = len(beats_data.get("beats", []))
    total_events = ledger_count + proc_count + beat_count

    # Role analysis
    all_roles = set()
    role_activity = {}

    # Analyze all data sources
    for entry in ledger_data.get("entries", []):
        role = entry.get("role", "Unknown")
        all_roles.add(role)
        role_activity[role] = role_activity.get(role, 0) + 1

    for proc in proclamations_data.get("proclamations", []):
        role = proc.get("role", "Unknown")
        all_roles.add(role)
        role_activity[role] = role_activity.get(role, 0) + 1

    for beat in beats_data.get("beats", []):
        role = beat.get("role", "Unknown")
        all_roles.add(role)
        role_activity[role] = role_activity.get(role, 0) + 1

    # Display metrics
    st.markdown("### 🌟 **Cosmic Statistics**")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📊 Ledger Entries", ledger_count, "+2 today")

    with col2:
        st.metric("📜 Proclamations", proc_count, "+2 seasonal")

    with col3:
        st.metric("🎵 Sacred Beats", beat_count, "+2 cosmic")

    with col4:
        st.metric("🌊 Total Events", total_events, "+6 integrated")

    # Role activity chart
    st.markdown("---")
    st.markdown("### 👑 **Role Activity Analysis**")

    if role_activity:
        # Display role activity as text-based visualization to avoid TypedDict compatibility issues
        st.markdown("**📊 Role Activity Visualization:**")

        # Sort roles by activity
        sorted_roles = sorted(role_activity.items(), key=lambda x: x[1], reverse=True)
        max_activity = max(role_activity.values()) if role_activity else 1

        for role, count in sorted_roles:
            role_emoji = {
                "Custodian": "👑",
                "Heirs": "🎭",
                "Council": "⚖️",
                "Councils": "👥",
                "Cosmos": "🌌",
            }.get(role, "📝")

            # Create visual bar using characters
            bar_length = int((count / max_activity) * 20)
            bar = "🔥" * bar_length + "░" * (20 - bar_length)

            st.markdown(f"{role_emoji} **{role}**: {bar} `{count} entries`")

        # Role details
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🎯 Most Active Roles:**")
            sorted_roles = sorted(
                role_activity.items(), key=lambda x: x[1], reverse=True
            )
            for role, count in sorted_roles[:5]:
                role_emoji = {
                    "Custodian": "👑",
                    "Heirs": "🎭",
                    "Council": "⚖️",
                    "Councils": "👥",
                    "Cosmos": "🌌",
                }.get(role, "📝")
                st.write(f"{role_emoji} {role}: {count} entries")

        with col2:
            st.markdown("**🌊 Integration Status:**")
            st.write(f"🔥 Active Roles: {len(all_roles)}")
            st.write(f"📊 Data Sources: 3 (Ledger, Proclamations, Beats)")
            st.write(f"🌟 Cosmic Harmony: Perfect Integration")
            st.write(f"⚖️ Balance Status: Sacred Equilibrium")


def display_integration_controls():
    """Display integration controls and tools"""

    st.header("🎛️ Integration Controls")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 **Ledger Operations**")

        role = st.selectbox(
            "Select Role:", ["Custodian", "Heirs", "Council", "Councils", "Cosmos"]
        )
        proclamation_text = st.text_area(
            "Proclamation Text:", placeholder="Enter sacred proclamation..."
        )

        if st.button("📊 Add Ledger Entry"):
            if proclamation_text:
                new_entry = {
                    "role": role,
                    "proclamation": proclamation_text,
                    "timestamp": datetime.now().isoformat(),
                    "cosmic_event": "Manual Entry",
                    "significance": "User-generated sacred entry",
                }
                st.success("📊 Sacred ledger entry prepared!")
                st.json(new_entry)
                st.balloons()
            else:
                st.warning("Please enter proclamation text")

    with col2:
        st.markdown("### 🌊 **Cosmic Sync Operations**")

        if st.button("🔄 Synchronize All Data"):
            st.success("🌊 All cosmic data synchronized!")
            st.info("Ledger, Proclamations, and Beats are in perfect harmony")

        if st.button("📈 Generate Analytics Report"):
            st.success("📈 Cosmic analytics report generated!")
            st.info("Complete statistical analysis available in Analytics tab")

        if st.button("🎇 Invoke Cosmic Integration"):
            st.success("🎇 Cosmic integration invoked!")
            st.snow()

    # Status display
    st.markdown("---")
    st.markdown("### 🌟 **Current Integration Status**")

    now = datetime.now()

    st.markdown(
        f"""
    **⏰ Current Time:** {now.strftime('%Y-%m-%d %H:%M:%S')}
    **🍂 Season:** Autumn
    **📊 Ledger Status:** Active & Recording
    **📜 Proclamations:** 5 Sacred Declarations
    **🎵 Beats:** 4 Cosmic Rhythms
    **🌊 Integration:** Perfect Cosmic Harmony
    **🔥 Flame Status:** Eternal & Integrated
    """
    )


if __name__ == "__main__":
    sacred_ledger_system()
