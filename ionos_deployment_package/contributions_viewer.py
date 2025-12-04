#!/usr/bin/env python3
"""
CODEX DOMINION - CONSTELLATION CONTRIBUTIONS VIEWER

Sacred Interface for Custodian Review of Contributions
View, Manage, and Bless Contributions from Heirs and Customers

Features:
- Complete Contributions Overview with Council Status
- Sacred Words Display and Management
- Contribution Statistics and Analytics
- Council Decision Tracking
- Continuum Integration Management
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

LEDGER_PATH = "codex_ledger.json"

# SACRED CONFIGURATION
st.set_page_config(
    page_title="CONTRIBUTIONS VIEWER - Codex Dominion",
    page_icon="*",
    layout="wide",
    initial_sidebar_state="expanded",
)

# SACRED STYLING
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

    .contribution-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 15px;
        border: 2px solid #ffd700;
        color: white;
        box-shadow: 0 8px 16px rgba(255, 215, 0, 0.2);
    }

    .contribution-proclamation {
        background: linear-gradient(135deg, #f093fb, #f5576c);
    }

    .contribution-blessing {
        background: linear-gradient(135deg, #4facfe, #00f2fe);
    }

    .contribution-silence {
        background: linear-gradient(135deg, #a8edea, #fed6e3);
    }

    .metric-card {
        background: rgba(255, 215, 0, 0.1);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #ffd700;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(255, 215, 0, 0.3);
        transition: transform 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
    }

    .sacred-text {
        color: #ffd700;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.8);
    }

    .contribution-text {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        font-style: italic;
        border-left: 3px solid #ffd700;
    }

    .council-status-affirmed {
        color: #4ade80;
        font-weight: bold;
        text-shadow: 0 0 8px rgba(74, 222, 128, 0.6);
    }

    .council-status-silenced {
        color: #9ca3af;
        font-weight: bold;
        text-shadow: 0 0 8px rgba(156, 163, 175, 0.4);
    }
</style>
""",
    unsafe_allow_html=True,
)


def load_ledger():
    """Load the sacred ledger with error handling"""
    try:
        with open(LEDGER_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"contributions": []}


def create_metrics_display(contributions):
    """Create enhanced metrics display with council status"""
    col1, col2, col3, col4 = st.columns(4)

    total_contributions = len(contributions)

    # Count by status
    affirmed_count = len([c for c in contributions if c.get("status") == "affirmed"])
    silenced_count = len([c for c in contributions if c.get("status") == "silenced"])
    pending_count = len([c for c in contributions if c.get("status", "") == ""])

    with col1:
        st.markdown(
            f"""
        <div class="metric-card">
            <h3 class="sacred-text">{total_contributions}</h3>
            <p>Total Sacred Words</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="metric-card">
            <h3 class="sacred-text">{affirmed_count}</h3>
            <p>Council Affirmed</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="metric-card">
            <h3 class="sacred-text">{silenced_count}</h3>
            <p>Council Silenced</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
        <div class="metric-card">
            <h3 class="sacred-text">{pending_count}</h3>
            <p>Awaiting Review</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


def display_contributions_detail(contributions):
    """Display detailed view of contributions with council status"""
    st.subheader("Sacred Words from the Community")

    if not contributions:
        st.info("No contributions found in the sacred ledger.")
        return

    # Sort by timestamp (most recent first)
    sorted_contributions = sorted(
        contributions, key=lambda x: x.get("timestamp", ""), reverse=True
    )

    for contrib in sorted_contributions:
        role = contrib.get("role", "Unknown")
        name = contrib.get("name", "Anonymous")
        kind = contrib.get("kind", "Unknown")
        text = contrib.get("text", "")
        timestamp = contrib.get("timestamp", "Unknown time")
        contrib_id = contrib.get("id", "Unknown ID")
        status = contrib.get("status", "")

        # Determine card class and icon based on status first, then type
        card_class = "contribution-card"

        if status == "affirmed":
            card_class += " contribution-blessing"  # Green styling for affirmed
            icon = "[AFFIRMED]"
        elif status == "silenced":
            card_class += " contribution-silence"  # Muted styling for silenced
            icon = "[SILENCED]"
        elif kind == "Proclamation":
            card_class += " contribution-proclamation"
            icon = "[PROCLAMATION]"
        elif kind == "Blessing":
            card_class += " contribution-blessing"
            icon = "[BLESSING]"
        elif kind == "Silence":
            card_class += " contribution-silence"
            icon = "[SILENCE]"
        else:
            icon = "[SACRED]"

        # Create status display with proper styling
        if status:
            status_class = f"council-status-{status}"
            status_display = f'<br><small class="{status_class}"><strong>Council Status: {status.title()}</strong></small>'
        else:
            status_display = '<br><small style="color: #ffd700;"><strong>Status: Awaiting Council Review</strong></small>'

        st.markdown(
            f"""
        <div class="{card_class}">
            <strong>{icon} {kind} from {name}</strong><br>
            <small>Role: {role} | ID: {contrib_id}</small><br>
            <small>Submitted: {timestamp}</small>{status_display}
            <div class="contribution-text">
                "{text}"
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )


def create_contributions_analytics(contributions):
    """Create analytics charts for contributions including council decisions"""
    st.subheader("Contribution Analytics & Council Decisions")

    if not contributions:
        st.info("No data available for analytics")
        return

    # Prepare data for charts
    df_data = []
    for contrib in contributions:
        df_data.append(
            {
                "role": contrib.get("role", "Unknown"),
                "kind": contrib.get("kind", "Unknown"),
                "status": contrib.get("status", "Pending"),
                "timestamp": contrib.get("timestamp", ""),
                "text_length": len(contrib.get("text", "")),
            }
        )

    if df_data:
        df = pd.DataFrame(df_data)

        col1, col2 = st.columns(2)

        with col1:
            # Council decisions pie chart
            st.subheader("Council Decision Distribution")
            status_counts = df["status"].value_counts()

            # Replace empty status with 'Pending'
            status_counts = status_counts.replace({"": "Pending"})
            if "" in status_counts.index:
                status_counts.index = status_counts.index.str.replace("", "Pending")

            fig_status = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Council Decisions",
                color_discrete_map={
                    "affirmed": "#4ade80",
                    "silenced": "#9ca3af",
                    "Pending": "#ffd700",
                },
            )
            fig_status.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig_status, use_container_width=True)

        with col2:
            # Contributions by role
            st.subheader("Contributions by Role")
            role_counts = df["role"].value_counts()

            fig_role = px.bar(
                x=role_counts.index,
                y=role_counts.values,
                title="Sacred Words by Role",
                color=role_counts.values,
                color_continuous_scale="Viridis",
            )
            fig_role.update_layout(
                xaxis_title="Role", yaxis_title="Count", showlegend=False
            )
            st.plotly_chart(fig_role, use_container_width=True)

        # Timeline analysis
        st.subheader("Contribution Timeline")
        if df["timestamp"].notna().any():
            # Convert timestamps for timeline
            df["date"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df_timeline = df.dropna(subset=["date"])

            if not df_timeline.empty:
                fig_timeline = px.scatter(
                    df_timeline,
                    x="date",
                    y="kind",
                    color="status",
                    title="Sacred Words Timeline",
                    color_discrete_map={
                        "affirmed": "#4ade80",
                        "silenced": "#9ca3af",
                        "": "#ffd700",
                        "Pending": "#ffd700",
                    },
                )
                st.plotly_chart(fig_timeline, use_container_width=True)


def filter_contributions(contributions):
    """Add filtering options for contributions"""
    st.sidebar.subheader("Sacred Filters")

    # Status filter
    status_options = ["All"] + list(
        set([c.get("status", "Pending") for c in contributions])
    )
    # Replace empty strings with 'Pending'
    status_options = [
        "All" if x == "All" else ("Pending" if x == "" else x) for x in status_options
    ]
    status_filter = st.sidebar.selectbox("Filter by Council Status:", status_options)

    # Role filter
    roles = ["All"] + list(set([c.get("role", "Unknown") for c in contributions]))
    role_filter = st.sidebar.selectbox("Filter by Role:", roles)

    # Kind filter
    kinds = ["All"] + list(set([c.get("kind", "Unknown") for c in contributions]))
    kind_filter = st.sidebar.selectbox("Filter by Type:", kinds)

    # Apply filters
    filtered = contributions.copy()

    if status_filter != "All":
        if status_filter == "Pending":
            filtered = [c for c in filtered if c.get("status", "") == ""]
        else:
            filtered = [c for c in filtered if c.get("status", "") == status_filter]

    if role_filter != "All":
        filtered = [c for c in filtered if c.get("role", "") == role_filter]

    if kind_filter != "All":
        filtered = [c for c in filtered if c.get("kind", "") == kind_filter]

    return filtered


def main():
    """Main application function"""

    # Header
    st.markdown(
        """
    <div class="main-header">
        <h1>*** CODEX DOMINION - CONSTELLATION CONTRIBUTIONS VIEWER ***</h1>
        <p class="sacred-text">Sacred Interface for Custodian Review of Community Words with Council Oversight</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Load ledger data
    ledger_data = load_ledger()
    contributions = ledger_data.get("contributions", [])

    # Filter contributions
    filtered_contributions = filter_contributions(contributions)

    # Display metrics
    create_metrics_display(filtered_contributions)

    # Create tabs for different views
    tab1, tab2 = st.tabs(["Sacred Words", "Analytics & Decisions"])

    with tab1:
        if st.sidebar.button("Refresh Sacred Data"):
            st.rerun()

        display_contributions_detail(filtered_contributions)

    with tab2:
        create_contributions_analytics(filtered_contributions)

    # Footer with sacred timestamp
    st.markdown("---")
    st.markdown(
        f"""
    <div style="text-align: center; color: #ffd700; font-style: italic;">
        Sacred Interface Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
        <br>
        Total Sacred Words in Ledger: {len(contributions)}
        <br>
        Filtered View: {len(filtered_contributions)} contributions
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
