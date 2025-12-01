#!/usr/bin/env python3
"""
Enhanced Revenue Crown Dashboard
===============================
Advanced financial sovereignty dashboard with constellation data visualization
"""

import json
import time
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="👑 Revenue Crown Sovereignty",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Performance monitoring
def performance_monitor(operation_name=None):
    """Monitor performance of functions"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time

                if "performance_data" not in st.session_state:
                    st.session_state.performance_data = {}

                op_name = operation_name or func.__name__
                if op_name not in st.session_state.performance_data:
                    st.session_state.performance_data[op_name] = []

                st.session_state.performance_data[op_name].append(execution_time)

                if len(st.session_state.performance_data[op_name]) > 100:
                    st.session_state.performance_data[op_name] = (
                        st.session_state.performance_data[op_name][-100:]
                    )

                return result
            except Exception as e:
                st.error(f"❌ Error in {operation_name or func.__name__}: {str(e)}")
                raise

        return wrapper

    return decorator


# Enhanced data loading
@st.cache_data(ttl=60)
@performance_monitor("load_data")
def load_json_data(filename, default=None):
    """Enhanced JSON loading with caching"""
    try:
        data_path = Path("data") / filename
        if data_path.exists():
            with open(data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return default or {}
    except Exception as e:
        st.error(f"Error loading {filename}: {str(e)}")
        return default or {}


# Enhanced styling
def apply_revenue_crown_styling():
    """Apply enhanced Revenue Crown styling"""
    st.markdown(
        """
    <style>
    /* Enhanced Revenue Crown Styling */
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 30%, #16213e 70%, #0f0f23 100%);
        color: #fff;
    }
    
    .revenue-crown-header {
        text-align: center;
        padding: 40px;
        margin-bottom: 30px;
        background: linear-gradient(45deg, 
            rgba(255,215,0,0.3) 0%, 
            rgba(218,165,32,0.2) 25%, 
            rgba(255,140,0,0.3) 50%,
            rgba(255,215,0,0.2) 75%,
            rgba(184,134,11,0.3) 100%);
        border: 3px solid #FFD700;
        border-radius: 25px;
        box-shadow: 
            0 0 30px rgba(255,215,0,0.4),
            inset 0 0 30px rgba(255,215,0,0.1);
        backdrop-filter: blur(10px);
        animation: golden-glow 3s ease-in-out infinite;
    }
    
    @keyframes golden-glow {
        0%, 100% { 
            box-shadow: 0 0 30px rgba(255,215,0,0.4), inset 0 0 30px rgba(255,215,0,0.1);
            border-color: #FFD700;
        }
        50% { 
            box-shadow: 0 0 50px rgba(255,215,0,0.6), inset 0 0 50px rgba(255,215,0,0.2);
            border-color: #FFA500;
        }
    }
    
    .constellation-card {
        background: linear-gradient(135deg, 
            rgba(255,255,255,0.1) 0%, 
            rgba(255,215,0,0.1) 50%, 
            rgba(255,255,255,0.05) 100%);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid rgba(255,215,0,0.4);
        backdrop-filter: blur(15px);
        margin: 15px 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .constellation-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255,215,0,0.2), 
            transparent);
        transition: left 0.5s;
    }
    
    .constellation-card:hover::before {
        left: 100%;
    }
    
    .constellation-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 20px 50px rgba(255,215,0,0.3),
            0 0 30px rgba(255,215,0,0.4);
        border-color: #FFD700;
    }
    
    .metric-crown {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, 
            rgba(255,215,0,0.2) 0%, 
            rgba(255,140,0,0.1) 50%,
            rgba(218,165,32,0.2) 100%);
        border-radius: 15px;
        border: 2px solid rgba(255,215,0,0.3);
        margin: 10px 0;
        box-shadow: 0 5px 15px rgba(255,215,0,0.2);
        transition: all 0.3s ease;
    }
    
    .metric-crown:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(255,215,0,0.4);
    }
    
    .stream-indicator {
        display: inline-block;
        padding: 8px 16px;
        margin: 5px;
        border-radius: 20px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 1px solid;
        transition: all 0.3s ease;
    }
    
    .stream-store {
        background: rgba(50, 205, 50, 0.2);
        border-color: #32CD32;
        color: #32CD32;
    }
    
    .stream-social {
        background: rgba(138, 43, 226, 0.2);
        border-color: #8A2BE2;
        color: #8A2BE2;
    }
    
    .stream-website {
        background: rgba(255, 69, 0, 0.2);
        border-color: #FF4500;
        color: #FF4500;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        border: none;
        border-radius: 15px;
        color: #000;
        font-weight: bold;
        padding: 12px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255,215,0,0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #FFA500, #FFD700);
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 8px 25px rgba(255,215,0,0.5);
    }
    
    .performance-indicator {
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(0,0,0,0.8);
        color: #FFD700;
        padding: 15px;
        border-radius: 15px;
        font-size: 12px;
        z-index: 1000;
        border: 1px solid #FFD700;
        backdrop-filter: blur(10px);
    }
    
    .sidebar-enhancement {
        background: linear-gradient(135deg, rgba(15,15,35,0.9), rgba(26,26,46,0.9));
        border-right: 2px solid rgba(255,215,0,0.3);
    }
    
    /* Chart enhancements */
    .plotly-graph-div {
        border-radius: 15px;
        overflow: hidden;
        border: 2px solid rgba(255,215,0,0.2);
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
    }
    
    /* Animation for revenue numbers */
    .revenue-number {
        animation: count-up 2s ease-out;
        font-size: 2.5em;
        font-weight: bold;
        color: #FFD700;
        text-shadow: 0 0 20px rgba(255,215,0,0.5);
    }
    
    @keyframes count-up {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .revenue-crown-header {
            padding: 25px 15px;
        }
        .constellation-card {
            padding: 15px;
        }
        .metric-crown {
            padding: 15px;
        }
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


@performance_monitor("display_constellation")
def display_constellation_data():
    """Display constellation revenue data with enhanced visualization"""

    # Load constellation data
    constellation_data = load_json_data("constellations.json", {})
    revenue_summary = load_json_data("revenue_summary.json", {})

    if not constellation_data.get("constellations"):
        st.warning(
            "⚠️ No constellation data found. Please add constellation data first."
        )
        return

    constellation = constellation_data["constellations"][0]["constellation"]
    metadata = constellation_data.get("metadata", {})

    # Header section
    st.markdown(
        """
    <div class="revenue-crown-header">
        <h1>👑 REVENUE CROWN SOVEREIGNTY 👑</h1>
        <h2>🌟 Constellation Financial Analytics 🌟</h2>
        <p style="color: #FFD700; font-size: 1.2em;">
            <em>Multi-Stream Revenue Dominion • Real-Time Cosmic Analytics</em>
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Performance indicator
    if "performance_data" in st.session_state:
        total_ops = sum(
            len(times) for times in st.session_state.performance_data.values()
        )
        st.markdown(
            f"""
        <div class="performance-indicator">
            🚀 Operations: {total_ops}<br>
            ⚡ Status: Optimized<br>
            👑 Crown: Active
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
        <div class="metric-crown">
            <h4>💰 Total Revenue</h4>
            <div class="revenue-number">${metadata.get('total_revenue', 0):,}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="metric-crown">
            <h4>⭐ Active Streams</h4>
            <div class="revenue-number">{len(constellation)}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="metric-crown">
            <h4>🔥 Active Cycles</h4>
            <div class="revenue-number">{len(metadata.get('active_cycles', []))}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
        <div class="metric-crown">
            <h4>✨ Stellar Sources</h4>
            <div class="revenue-number">{len(metadata.get('active_stars', []))}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Constellation details
    st.markdown("### 🌟 Revenue Constellation Details")

    for i, stream in enumerate(constellation):
        stream_class = f"stream-{stream['stream'].lower()}"

        st.markdown(
            f"""
        <div class="constellation-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="margin: 0; color: #FFD700;">
                    {stream['stream']} Revenue Stream
                </h3>
                <span class="stream-indicator {stream_class}">
                    {stream['stream']}
                </span>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div>
                    <strong>💫 Star Source:</strong><br>
                    <span style="color: #FFD700;">{stream['star']}</span>
                </div>
                <div>
                    <strong>🔄 Cycle:</strong><br>
                    <span style="color: #FFD700;">{stream['cycle']}</span>
                </div>
                <div>
                    <strong>💰 Amount:</strong><br>
                    <span style="color: #32CD32; font-size: 1.3em; font-weight: bold;">${stream['amount']:,}</span>
                </div>
                <div>
                    <strong>⏰ Timestamp:</strong><br>
                    <span style="color: #FFD700;">{stream['timestamp']}</span>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )


@performance_monitor("create_charts")
def create_revenue_charts():
    """Create enhanced revenue visualization charts"""

    constellation_data = load_json_data("constellations.json", {})
    revenue_summary = load_json_data("revenue_summary.json", {})

    if not constellation_data.get("constellations"):
        return

    constellation = constellation_data["constellations"][0]["constellation"]

    # Create DataFrame for charts
    df = pd.DataFrame(constellation)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Revenue Distribution by Stream")

        # Pie chart for streams
        fig_pie = px.pie(
            df,
            values="amount",
            names="stream",
            title="Revenue Distribution",
            color_discrete_sequence=["#FFD700", "#32CD32", "#FF4500"],
        )

        fig_pie.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Amount: $%{value:,.0f}<br>Percent: %{percent}<extra></extra>",
        )

        fig_pie.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            title_font_color="#FFD700",
            height=400,
        )

        st.plotly_chart(fig_pie, width="stretch")

    with col2:
        st.markdown("### 🌟 Revenue by Stellar Source")

        # Bar chart for stars
        fig_bar = px.bar(
            df,
            x="star",
            y="amount",
            title="Revenue by Stellar Source",
            color="amount",
            color_continuous_scale="Viridis",
        )

        fig_bar.update_traces(
            hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>"
        )

        fig_bar.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            title_font_color="#FFD700",
            xaxis_title="Stellar Source",
            yaxis_title="Revenue ($)",
            height=400,
        )

        fig_bar.update_xaxes(gridcolor="rgba(255,215,0,0.2)")
        fig_bar.update_yaxes(gridcolor="rgba(255,215,0,0.2)")

        st.plotly_chart(fig_bar, width="stretch")

    # Timeline chart
    st.markdown("### ⏰ Revenue Timeline by Cycle")

    # Convert timestamp to datetime for proper sorting
    df["datetime"] = pd.to_datetime(df["timestamp"])
    df_sorted = df.sort_values("datetime")

    fig_timeline = go.Figure()

    colors = {"Store": "#32CD32", "Social": "#8A2BE2", "Website": "#FF4500"}

    for stream in df_sorted["stream"].unique():
        stream_data = df_sorted[df_sorted["stream"] == stream]

        fig_timeline.add_trace(
            go.Scatter(
                x=stream_data["datetime"],
                y=stream_data["amount"],
                mode="markers+lines",
                name=stream,
                marker=dict(
                    size=15,
                    color=colors.get(stream, "#FFD700"),
                    line=dict(width=2, color="white"),
                ),
                line=dict(width=3, color=colors.get(stream, "#FFD700")),
                hovertemplate="<b>%{text}</b><br>Time: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>",
                text=[
                    f"{row['stream']} - {row['star']}"
                    for _, row in stream_data.iterrows()
                ],
            )
        )

    fig_timeline.update_layout(
        title="Revenue Timeline Across All Cycles",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        title_font_color="#FFD700",
        xaxis_title="Timeline",
        yaxis_title="Revenue ($)",
        height=400,
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0.5)", bordercolor="#FFD700", borderwidth=1),
    )

    fig_timeline.update_xaxes(gridcolor="rgba(255,215,0,0.2)")
    fig_timeline.update_yaxes(gridcolor="rgba(255,215,0,0.2)")

    st.plotly_chart(fig_timeline, width="stretch")


def show_performance_dashboard():
    """Show performance statistics in sidebar"""
    with st.sidebar:
        st.markdown("### ⚡ Performance Monitor")

        if "performance_data" in st.session_state and st.session_state.performance_data:
            for operation, times in st.session_state.performance_data.items():
                if times:
                    avg_time = sum(times) / len(times)
                    max_time = max(times)

                    st.metric(
                        f"{operation.replace('_', ' ').title()}",
                        f"{avg_time:.3f}s avg",
                        f"Max: {max_time:.3f}s",
                    )

        st.markdown("---")
        st.markdown("### 🎯 System Status")
        st.success("✅ Enhanced Performance Mode")
        st.info("📊 Real-time Monitoring Active")
        st.warning("👑 Revenue Crown Online")


def main():
    """Main Revenue Crown dashboard"""

    # Apply styling
    apply_revenue_crown_styling()

    # Performance monitoring sidebar
    show_performance_dashboard()

    # Main content
    display_constellation_data()

    # Charts section
    create_revenue_charts()

    # Footer
    st.markdown("---")
    st.markdown(
        """
    <div style="text-align: center; color: #FFD700; padding: 20px;">
        <h4>👑 Revenue Crown Sovereignty Dashboard 👑</h4>
        <p><em>Cosmic Financial Analytics • Multi-Stream Revenue Management</em></p>
        <p>🌟 Last Updated: {}</p>
    </div>
    """.format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ),
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
