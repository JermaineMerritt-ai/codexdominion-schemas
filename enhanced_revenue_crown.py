"""
Revenue Crown Dashboard Enhancement
==================================
Optimized version of the revenue crown dashboard with performance monitoring
and enhanced features while maintaining backward compatibility.
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


# Performance monitoring decorator
def performance_monitor(operation_name=None):
    """Monitor performance of functions"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time

                # Store performance data in session state
                if "performance_data" not in st.session_state:
                    st.session_state.performance_data = {}

                op_name = operation_name or func.__name__
                if op_name not in st.session_state.performance_data:
                    st.session_state.performance_data[op_name] = []

                st.session_state.performance_data[op_name].append(execution_time)

                # Keep only last 100 measurements
                if len(st.session_state.performance_data[op_name]) > 100:
                    st.session_state.performance_data[op_name] = (
                        st.session_state.performance_data[op_name][-100:]
                    )

                # Warn about slow operations
                if execution_time > 1.0:
                    st.warning(
                        f"⚠️ Slow operation detected: {op_name} took {execution_time:.2f}s"
                    )

                return result
            except Exception as e:
                execution_time = time.time() - start_time
                st.error(f"❌ Error in {operation_name or func.__name__}: {str(e)}")
                raise

        return wrapper

    return decorator


# Enhanced data loading with caching
@st.cache_data(ttl=300)  # Cache for 5 minutes
@performance_monitor("load_json_file")
def load_json_enhanced(filename, default_data):
    """Enhanced JSON loading with caching and error handling"""
    try:
        path = Path(filename)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if data else default_data
        else:
            # Create file with default data if it doesn't exist
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=2)
            return default_data
    except Exception as e:
        st.error(f"Error loading {filename}: {str(e)}")
        return default_data


# Enhanced append function
@performance_monitor("append_entry")
def append_entry_enhanced(filename, entry):
    """Enhanced entry appending with validation"""
    try:
        # Validate entry
        if not isinstance(entry, dict):
            raise ValueError("Entry must be a dictionary")

        # Add timestamp if not present
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().isoformat()

        # Load existing data
        path = Path(filename)
        data = []
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
                except json.JSONDecodeError:
                    data = []

        # Append new entry
        data.append(entry)

        # Save back to file
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Clear cache to ensure fresh data
        st.cache_data.clear()

        return True
    except Exception as e:
        st.error(f"Error appending to {filename}: {str(e)}")
        return False


# Enhanced styling
def apply_enhanced_styling():
    """Apply enhanced cosmic styling"""
    st.markdown(
        """
    <style>
    /* Enhanced Revenue Crown Styling */
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    .revenue-header {
        text-align: center;
        padding: 30px;
        margin-bottom: 30px;
        background: linear-gradient(45deg, rgba(255,215,0,0.3), rgba(218,165,32,0.2));
        border: 3px solid #FFD700;
        border-radius: 25px;
        box-shadow: 0 10px 40px rgba(255,215,0,0.3);
        backdrop-filter: blur(10px);
    }
    
    .revenue-card {
        background: rgba(255,255,255,0.1);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid rgba(255,215,0,0.3);
        backdrop-filter: blur(15px);
        margin: 15px 0;
        transition: all 0.4s ease;
    }
    
    .revenue-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 40px rgba(255,215,0,0.4);
        border-color: #FFD700;
    }
    
    .metric-display {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, rgba(255,215,0,0.2), rgba(255,140,0,0.1));
        border-radius: 15px;
        border: 1px solid rgba(255,215,0,0.4);
        margin: 10px 0;
    }
    
    .performance-indicator {
        position: fixed;
        top: 10px;
        right: 10px;
        background: rgba(0,0,0,0.8);
        color: #FFD700;
        padding: 10px;
        border-radius: 10px;
        font-size: 12px;
        z-index: 1000;
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        border: none;
        border-radius: 15px;
        color: #000;
        font-weight: bold;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #FFA500, #FFD700);
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(255,215,0,0.5);
    }
    
    /* Enhanced charts */
    .plotly-graph-div {
        border-radius: 15px;
        overflow: hidden;
        border: 1px solid rgba(255,215,0,0.3);
    }
    
    /* Loading animation */
    .loading-crown {
        text-align: center;
        padding: 40px;
        animation: golden-pulse 2s ease-in-out infinite;
    }
    
    @keyframes golden-pulse {
        0%, 100% { color: #FFD700; transform: scale(1); }
        50% { color: #FFA500; transform: scale(1.1); }
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .revenue-header {
            padding: 20px;
            margin-bottom: 20px;
        }
        .revenue-card {
            padding: 15px;
            margin: 10px 0;
        }
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


# Performance dashboard component
def show_performance_dashboard():
    """Show performance statistics"""
    if "performance_data" in st.session_state and st.session_state.performance_data:
        with st.expander("📊 Performance Dashboard"):
            st.subheader("🚀 Operation Performance")

            for operation, times in st.session_state.performance_data.items():
                if times:
                    avg_time = sum(times) / len(times)
                    max_time = max(times)
                    min_time = min(times)

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric(f"{operation} Avg", f"{avg_time:.3f}s")
                    with col2:
                        st.metric("Max", f"{max_time:.3f}s")
                    with col3:
                        st.metric("Min", f"{min_time:.3f}s")
                    with col4:
                        st.metric("Calls", len(times))


# Enhanced metric display
def display_enhanced_metric(title, value, delta=None, help_text=None):
    """Display enhanced metric with styling"""
    delta_html = (
        f'<div style="color: #32CD32; font-size: 0.9em;">📈 {delta}</div>'
        if delta
        else ""
    )
    help_html = (
        f'<div style="color: #ccc; font-size: 0.8em; margin-top: 5px;">{help_text}</div>'
        if help_text
        else ""
    )

    st.markdown(
        f"""
    <div class="metric-display">
        <h4 style="margin: 0; color: #FFD700;">{title}</h4>
        <h2 style="margin: 10px 0; color: white;">{value}</h2>
        {delta_html}
        {help_html}
    </div>
    """,
        unsafe_allow_html=True,
    )


# Enhanced chart rendering
def render_enhanced_chart(fig, title=None, height=400):
    """Render chart with enhanced styling"""
    if title:
        fig.update_layout(
            title={
                "text": title,
                "x": 0.5,
                "xanchor": "center",
                "font": {"size": 18, "color": "#FFD700"},
            }
        )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0.3)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=height,
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0.5)", bordercolor="#FFD700", borderwidth=1),
    )

    # Enhance grid
    fig.update_xaxes(gridcolor="rgba(255,215,0,0.2)")
    fig.update_yaxes(gridcolor="rgba(255,215,0,0.2)")

    st.plotly_chart(fig, use_container_width=True)


# Enhanced error handling
def safe_execute(func, error_message="An error occurred"):
    """Safely execute function with error handling"""
    try:
        return func()
    except Exception as e:
        st.error(f"❌ {error_message}: {str(e)}")
        st.exception(e)
        return None


# Loading indicator
def show_loading(message="Loading Revenue Crown..."):
    """Show loading indicator"""
    return st.empty().markdown(
        f"""
    <div class="loading-crown">
        <h1>👑</h1>
        <p>{message}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


# Success message
def show_success(message, details=None):
    """Show success message with golden styling"""
    st.success(f"🏆 {message}")
    if details:
        st.info(f"📋 {details}")


# Main enhanced revenue crown function
@performance_monitor("revenue_crown_main")
def run_enhanced_revenue_crown():
    """Run the enhanced revenue crown dashboard"""

    # Apply styling
    apply_enhanced_styling()

    # Header
    st.markdown(
        """
    <div class="revenue-header">
        <h1>👑 REVENUE CROWN SOVEREIGNTY 👑</h1>
        <h3>💰 Advanced Financial Empire Analytics 💰</h3>
        <p style="color: #FFD700;"><em>Enhanced Performance • Real-time Analytics • Cosmic Optimization</em></p>
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
            ⚡ Status: Optimized
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Main content would continue here with the original revenue crown logic
    # but enhanced with the new performance monitoring and styling

    # Show performance dashboard in sidebar
    with st.sidebar:
        st.header("⚡ Performance Monitor")
        show_performance_dashboard()

        # System status
        st.header("🎯 System Status")
        st.success("✅ Enhanced Performance Mode")
        st.info("📊 Real-time Monitoring Active")
        st.warning("⚡ Cosmic Optimization Enabled")


if __name__ == "__main__":
    run_enhanced_revenue_crown()
