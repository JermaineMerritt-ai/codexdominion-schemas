#!/usr/bin/env python3
"""
📜 COSMIC DOMINION - CODEX BULLETIN 📜
Public Witness Interface for Digital Sovereignty Chronicles
Comprehensive view of heartbeat, proclamations, and ledger entries
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st


def load_json(file_path, default=None):
    """Load JSON data with error handling"""
    if default is None:
        default = {}

    try:
        path = Path(file_path)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return default
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return default


def format_timestamp(timestamp_str):
    """Format timestamp for display"""
    try:
        # Parse the timestamp
        dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))

        # Calculate time ago
        now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
        time_diff = now - dt

        if time_diff.days > 0:
            time_ago = f"{time_diff.days} days ago"
        elif time_diff.seconds > 3600:
            hours = time_diff.seconds // 3600
            time_ago = f"{hours} hours ago"
        elif time_diff.seconds > 60:
            minutes = time_diff.seconds // 60
            time_ago = f"{minutes} minutes ago"
        else:
            time_ago = "Just now"

        formatted_time = dt.strftime("%Y-%m-%d %H:%M")
        return formatted_time, time_ago
    except:
        return (
            timestamp_str[:16] if len(timestamp_str) > 16 else timestamp_str
        ), "Unknown"


def create_role_badge(role):
    """Create styled role badges"""
    role_colors = {
        "Custodian": "#ffd700",  # Gold
        "Heir": "#9370db",  # Purple
        "Council": "#4169e1",  # Royal Blue
        "System": "#32cd32",  # Lime Green
        "Auto": "#ff6347",  # Tomato
    }

    color = role_colors.get(role, "#808080")

    return f"""
    <span style="background-color: {color}; color: black; padding: 2px 8px; 
                 border-radius: 10px; font-size: 0.8em; font-weight: bold;">
        {role}
    </span>
    """


def create_type_badge(entry_type):
    """Create styled type badges"""
    type_colors = {
        "Blessing": "#32cd32",
        "Silence": "#87ceeb",
        "Proclamation": "#ffd700",
        "Command": "#ff6347",
        "Ritual": "#da70d6",
        "Sacred": "#9370db",
        "Crown": "#ffd700",
        "Cosmic": "#4169e1",
    }

    color = type_colors.get(entry_type, "#696969")

    return f"""
    <span style="background-color: {color}33; color: {color}; 
                 border: 1px solid {color}; padding: 1px 6px; 
                 border-radius: 8px; font-size: 0.75em;">
        {entry_type}
    </span>
    """


def display_heartbeat_section(beats, time_filter):
    """Display heartbeat section with enhanced formatting"""

    st.markdown("### 💓 **Cosmic Heartbeat - Eternal Pulse**")

    if not beats:
        st.info("💓 No heartbeat data available - System may be initializing")
        return

    # Filter beats based on time
    filtered_beats = []
    now = datetime.now()

    for beat in beats:
        try:
            beat_time = datetime.fromisoformat(
                beat.get("timestamp", "").replace("Z", "+00:00")
            )

            if time_filter == "All Time":
                filtered_beats.append(beat)
            elif time_filter == "Last 24 Hours" and (now - beat_time).days == 0:
                filtered_beats.append(beat)
            elif time_filter == "Last 7 Days" and (now - beat_time).days <= 7:
                filtered_beats.append(beat)
            elif time_filter == "Last 30 Days" and (now - beat_time).days <= 30:
                filtered_beats.append(beat)
        except:
            if time_filter == "All Time":
                filtered_beats.append(beat)

    if not filtered_beats:
        st.warning(f"💓 No heartbeat entries found for {time_filter}")
        return

    # Show latest heartbeat status
    latest_beat = filtered_beats[-1] if filtered_beats else None
    if latest_beat:
        formatted_time, time_ago = format_timestamp(latest_beat.get("timestamp", ""))
        status = latest_beat.get("status", "Unknown")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💓 Status", status, delta=None)
        with col2:
            st.metric("🕐 Last Beat", formatted_time)
        with col3:
            st.metric("⏰ Time Ago", time_ago)

    # Display recent beats
    with st.expander(
        f"📊 Heartbeat History ({len(filtered_beats)} entries)", expanded=True
    ):
        for beat in reversed(filtered_beats[-10:]):  # Show last 10
            formatted_time, time_ago = format_timestamp(beat.get("timestamp", ""))
            role = beat.get("role", "System")
            text = beat.get("text", beat.get("status", "Heartbeat pulse"))

            st.markdown(
                f"""
            <div style="background: rgba(255,255,255,0.05); padding: 10px; margin: 5px 0; 
                        border-left: 3px solid #ff6347; border-radius: 5px;">
                <div style="display: flex; justify-content: between; align-items: center;">
                    <div>
                        {create_role_badge(role)}
                        <strong style="margin-left: 10px;">{formatted_time}</strong>
                        <em style="margin-left: 10px; color: #aaa;">({time_ago})</em>
                    </div>
                </div>
                <div style="margin-top: 5px; padding-left: 10px;">
                    💓 {text}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )


def display_proclamations_section(proclamations, time_filter, role_filter, type_filter):
    """Display proclamations section with enhanced formatting"""

    st.markdown("### 📜 **Sacred Proclamations - Divine Decrees**")

    if not proclamations:
        st.info("📜 No proclamations available - Begin with your first sacred decree")
        return

    # Apply filters
    filtered_proclamations = []
    now = datetime.now()

    for proc in proclamations:
        # Time filter
        try:
            proc_time = datetime.fromisoformat(
                proc.get("timestamp", "").replace("Z", "+00:00")
            )

            time_match = False
            if time_filter == "All Time":
                time_match = True
            elif time_filter == "Last 24 Hours" and (now - proc_time).days == 0:
                time_match = True
            elif time_filter == "Last 7 Days" and (now - proc_time).days <= 7:
                time_match = True
            elif time_filter == "Last 30 Days" and (now - proc_time).days <= 30:
                time_match = True
        except:
            time_match = time_filter == "All Time"

        # Role filter
        role_match = role_filter == "All Roles" or proc.get("role") == role_filter

        # Type filter
        type_match = type_filter == "All Types" or proc.get("type") == type_filter

        if time_match and role_match and type_match:
            filtered_proclamations.append(proc)

    if not filtered_proclamations:
        st.warning(f"📜 No proclamations found for current filters")
        return

    # Proclamation statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📜 Total Proclamations", len(filtered_proclamations))

    with col2:
        roles = [p.get("role", "Unknown") for p in filtered_proclamations]
        most_active_role = max(set(roles), key=roles.count) if roles else "None"
        st.metric("👑 Most Active Role", most_active_role)

    with col3:
        types = [p.get("type", "Unknown") for p in filtered_proclamations]
        most_common_type = max(set(types), key=types.count) if types else "None"
        st.metric("🎯 Most Common Type", most_common_type)

    # Display proclamations
    with st.expander(
        f"📜 Proclamation Chronicle ({len(filtered_proclamations)} entries)",
        expanded=True,
    ):
        for proc in reversed(filtered_proclamations[-15:]):  # Show last 15
            formatted_time, time_ago = format_timestamp(proc.get("timestamp", ""))
            role = proc.get("role", "Unknown")
            proc_type = proc.get("type", "Proclamation")
            cycle = proc.get("cycle", "Eternal")
            text = proc.get("text", "Sacred proclamation text")

            st.markdown(
                f"""
            <div style="background: rgba(255,215,0,0.1); padding: 15px; margin: 8px 0; 
                        border-left: 4px solid #ffd700; border-radius: 8px;">
                <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 8px;">
                    <div>
                        {create_role_badge(role)}
                        {create_type_badge(proc_type)}
                        <strong style="margin-left: 10px;">{formatted_time}</strong>
                        <em style="margin-left: 10px; color: #aaa;">({time_ago})</em>
                    </div>
                </div>
                <div style="margin-left: 10px; font-style: italic;">
                    <strong>Cycle:</strong> {cycle}
                </div>
                <div style="margin: 10px 0 0 10px; padding: 10px; background: rgba(255,255,255,0.05); 
                            border-radius: 5px; border-left: 2px solid #ffd700;">
                    📜 {text}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )


def display_ledger_section(entries, time_filter, role_filter):
    """Display ledger section with enhanced formatting"""

    st.markdown("### 📖 **Cosmic Ledger - Eternal Chronicle**")

    if not entries:
        st.info("📖 No ledger entries available - Chronicle awaits first entry")
        return

    # Apply filters
    filtered_entries = []
    now = datetime.now()

    for entry in entries:
        # Time filter
        try:
            entry_time = datetime.fromisoformat(
                entry.get("timestamp", "").replace("Z", "+00:00")
            )

            time_match = False
            if time_filter == "All Time":
                time_match = True
            elif time_filter == "Last 24 Hours" and (now - entry_time).days == 0:
                time_match = True
            elif time_filter == "Last 7 Days" and (now - entry_time).days <= 7:
                time_match = True
            elif time_filter == "Last 30 Days" and (now - entry_time).days <= 30:
                time_match = True
        except:
            time_match = time_filter == "All Time"

        # Role filter
        role_match = role_filter == "All Roles" or entry.get("role") == role_filter

        if time_match and role_match:
            filtered_entries.append(entry)

    if not filtered_entries:
        st.warning(f"📖 No ledger entries found for current filters")
        return

    # Ledger statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📖 Total Entries", len(filtered_entries))

    with col2:
        entry_types = [e.get("type", "Unknown") for e in filtered_entries]
        most_common_type = (
            max(set(entry_types), key=entry_types.count) if entry_types else "None"
        )
        st.metric("🎯 Most Common Type", most_common_type)

    with col3:
        if filtered_entries:
            latest_entry_time = filtered_entries[-1].get("timestamp", "")
            _, time_ago = format_timestamp(latest_entry_time)
            st.metric("⏰ Last Entry", time_ago)

    # Display ledger entries
    with st.expander(
        f"📖 Ledger Chronicle ({len(filtered_entries)} entries)", expanded=True
    ):
        for entry in reversed(filtered_entries[-20:]):  # Show last 20
            formatted_time, time_ago = format_timestamp(entry.get("timestamp", ""))
            role = entry.get("role", "Unknown")
            entry_type = entry.get("type", "Entry")
            proclamation = entry.get(
                "proclamation", entry.get("description", "Ledger entry")
            )

            # Color coding based on entry type
            type_colors = {
                "Crown": "#ffd700",
                "Cosmic": "#4169e1",
                "Command": "#ff6347",
                "Sacred": "#9370db",
            }
            border_color = type_colors.get(entry_type, "#32cd32")

            st.markdown(
                f"""
            <div style="background: rgba(255,255,255,0.03); padding: 12px; margin: 6px 0; 
                        border-left: 3px solid {border_color}; border-radius: 6px;">
                <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 6px;">
                    <div>
                        {create_role_badge(role)}
                        {create_type_badge(entry_type)}
                        <strong style="margin-left: 10px;">{formatted_time}</strong>
                        <em style="margin-left: 10px; color: #aaa;">({time_ago})</em>
                    </div>
                </div>
                <div style="margin-left: 10px; padding: 8px; background: rgba(255,255,255,0.02); 
                            border-radius: 4px;">
                    📖 {proclamation}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )


def codex_bulletin_interface():
    """Main Codex Bulletin interface"""

    st.set_page_config(page_title="📜 Codex Bulletin", page_icon="📜", layout="wide")

    # Custom CSS
    st.markdown(
        """
    <style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #fff;
    }
    .bulletin-header {
        text-align: center;
        padding: 30px;
        margin-bottom: 20px;
        background: linear-gradient(45deg, rgba(255,215,0,0.2), rgba(138,43,226,0.1));
        border: 2px solid #ffd700;
        border-radius: 20px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Header
    st.markdown(
        """
    <div class="bulletin-header">
        <h1>📜 CODEX BULLETIN — PUBLIC WITNESS</h1>
        <h3>🌟 Chronicle of Digital Sovereignty 🌟</h3>
        <p><em>Sacred witness to the eternal cosmic flame</em></p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Load data
    beats = load_json("heartbeat.json", {"beats": []})["beats"]
    proclamations = load_json("proclamations.json", {"proclamations": []})[
        "proclamations"
    ]
    entries = load_json("ledger.json", {"entries": []})["entries"]

    # Sidebar filters
    st.sidebar.markdown("## 🎛️ **Chronicle Filters**")

    time_filter = st.sidebar.selectbox(
        "📅 Time Period", ["All Time", "Last 24 Hours", "Last 7 Days", "Last 30 Days"]
    )

    # Get unique roles for filter
    all_roles = set()
    for item in proclamations + entries:
        all_roles.add(item.get("role", "Unknown"))
    all_roles = sorted(list(all_roles))

    role_filter = st.sidebar.selectbox("👤 Role Filter", ["All Roles"] + all_roles)

    # Get unique types for proclamations
    all_types = set()
    for proc in proclamations:
        all_types.add(proc.get("type", "Unknown"))
    all_types = sorted(list(all_types))

    type_filter = st.sidebar.selectbox(
        "🎯 Type Filter (Proclamations)", ["All Types"] + all_types
    )

    st.sidebar.markdown("---")

    # Quick stats in sidebar
    st.sidebar.markdown("## 📊 **Quick Statistics**")
    st.sidebar.metric("💓 Heartbeats", len(beats))
    st.sidebar.metric("📜 Proclamations", len(proclamations))
    st.sidebar.metric("📖 Ledger Entries", len(entries))

    total_chronicle = len(beats) + len(proclamations) + len(entries)
    st.sidebar.metric("🌟 Total Chronicle", total_chronicle)

    st.sidebar.markdown("---")

    # Auto-refresh option
    auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (30s)", value=False)
    if auto_refresh:
        st.rerun()

    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["💓 Heartbeat", "📜 Proclamations", "📖 Ledger", "🌟 Combined View"]
    )

    with tab1:
        display_heartbeat_section(beats, time_filter)

    with tab2:
        display_proclamations_section(
            proclamations, time_filter, role_filter, type_filter
        )

    with tab3:
        display_ledger_section(entries, time_filter, role_filter)

    with tab4:
        st.markdown("### 🌟 **Unified Chronicle View**")

        # Combine all entries with timestamps
        combined_entries = []

        # Add heartbeats
        for beat in beats:
            combined_entries.append(
                {
                    "timestamp": beat.get("timestamp", ""),
                    "type": "Heartbeat",
                    "role": beat.get("role", "System"),
                    "content": beat.get("text", beat.get("status", "Pulse")),
                    "category": "💓",
                }
            )

        # Add proclamations
        for proc in proclamations:
            combined_entries.append(
                {
                    "timestamp": proc.get("timestamp", ""),
                    "type": "Proclamation",
                    "role": proc.get("role", "Unknown"),
                    "content": proc.get("text", "Sacred proclamation"),
                    "category": "📜",
                }
            )

        # Add ledger entries
        for entry in entries:
            combined_entries.append(
                {
                    "timestamp": entry.get("timestamp", ""),
                    "type": "Ledger",
                    "role": entry.get("role", "Unknown"),
                    "content": entry.get(
                        "proclamation", entry.get("description", "Chronicle entry")
                    ),
                    "category": "📖",
                }
            )

        # Sort by timestamp (most recent first)
        try:
            combined_entries.sort(key=lambda x: x["timestamp"], reverse=True)
        except:
            pass

        # Display unified timeline
        st.info(
            f"📊 Showing unified timeline of {len(combined_entries)} total chronicle entries"
        )

        for item in combined_entries[:25]:  # Show last 25 across all types
            formatted_time, time_ago = format_timestamp(item["timestamp"])

            st.markdown(
                f"""
            <div style="background: rgba(255,255,255,0.02); padding: 10px; margin: 5px 0; 
                        border-left: 3px solid #ffd700; border-radius: 5px;">
                <div style="display: flex; justify-content: between; align-items: center;">
                    <div>
                        <span style="font-size: 1.2em;">{item['category']}</span>
                        {create_role_badge(item['role'])}
                        {create_type_badge(item['type'])}
                        <strong style="margin-left: 10px;">{formatted_time}</strong>
                        <em style="margin-left: 10px; color: #aaa;">({time_ago})</em>
                    </div>
                </div>
                <div style="margin-top: 5px; padding-left: 25px;">
                    {item['content'][:200]}{'...' if len(item['content']) > 200 else ''}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    codex_bulletin_interface()
