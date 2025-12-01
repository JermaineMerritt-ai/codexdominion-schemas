"""
Enhanced Dashboard with Performance Optimizations
===============================================
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

                # Store performance data
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

                return result
            except Exception as e:
                st.error(f"Error in {operation_name or func.__name__}: {str(e)}")
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
            return default_data
    except Exception as e:
        st.error(f"Error loading {filename}: {str(e)}")
        return default_data


# Performance dashboard component
@performance_monitor("show_performance_dashboard")
def show_performance_dashboard():
    """Show performance statistics"""
    if "performance_data" in st.session_state and st.session_state.performance_data:
        with st.expander("Performance Dashboard"):
            st.subheader("Operation Performance")

            for operation, times in st.session_state.performance_data.items():
                if times:
                    avg_time = sum(times) / len(times)
                    max_time = max(times)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(f"{operation} Avg", f"{avg_time:.3f}s")
                    with col2:
                        st.metric("Max", f"{max_time:.3f}s")
                    with col3:
                        st.metric("Calls", len(times))


# Enhanced styling
def apply_enhanced_styling():
    """Apply enhanced styling"""
    st.markdown(
        """
    <style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    .enhanced-header {
        text-align: center;
        padding: 30px;
        margin-bottom: 30px;
        background: linear-gradient(45deg, rgba(138,43,226,0.4), rgba(75,0,130,0.3));
        border: 2px solid #8B2BE2;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(138,43,226,0.3);
    }
    
    .enhanced-card {
        background: rgba(255,255,255,0.1);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid rgba(138,43,226,0.3);
        backdrop-filter: blur(15px);
        margin: 15px 0;
        transition: all 0.4s ease;
    }
    
    .enhanced-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 40px rgba(138,43,226,0.4);
        border-color: #8B2BE2;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #8B2BE2, #9370DB);
        border: none;
        border-radius: 15px;
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #9370DB, #8B2BE2);
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(138,43,226,0.5);
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


#!/usr/bin/env python3
"""
🌀 CODEX ETERNUM OMEGA DASHBOARD LAUNCHER
Launches the sovereign dashboard for Codex Eternum Omega operations
Custodian: Jermaine of Waxhaw | Cycle: IX | Mode: Eternal
"""

import os
import subprocess
import sys
from pathlib import Path


def launch_omega_dashboard():
    """Launch the Codex Eternum Omega dashboard."""
    dashboard_file = Path(__file__).parent / "codex_eternum_omega_dashboard.py"

    if not dashboard_file.exists():
        print("❌ Codex Eternum Omega Dashboard not found!")
        return False

    print("🌀 LAUNCHING CODEX ETERNUM OMEGA SOVEREIGN DASHBOARD...")
    print("=" * 70)
    print("👑 Custodian: Jermaine of Waxhaw")
    print("🔱 Seal: CODEX_ETERNUM_OMEGA")
    print("⚡ Status: SOVEREIGN")
    print("🌀 Mode: Eternal")
    print("📡 Cycle: IX")
    print("-" * 70)
    print("🌍 Production: https://aistorelab.com:8503")
    print("🔧 Staging: https://staging.aistorelab.com:8503")
    print("💻 Local: http://localhost:8503")
    print("-" * 70)

    try:
        # Launch Streamlit on different port for Omega dashboard
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(dashboard_file),
                "--server.port",
                "8503",
                "--server.address",
                "0.0.0.0",
                "--server.headless",
                "true",
            ]
        )
    except KeyboardInterrupt:
        print("\n🌀 Omega Dashboard shutdown complete. Sovereignty eternal!")
    except Exception as e:
        print(f"❌ Omega Dashboard launch failed: {e}")
        return False

    return True


def check_omega_system():
    """Check if Codex Eternum Omega system is available."""
    omega_file = Path(__file__).parent / "codex-integration" / "codex_eternum_omega.py"

    if not omega_file.exists():
        print("❌ Codex Eternum Omega system not found!")
        print(f"Expected: {omega_file}")
        return False

    print("✅ Codex Eternum Omega system found")
    return True


def main():
    """Main launcher function."""
    print("🌀 CODEX ETERNUM OMEGA DASHBOARD LAUNCHER v1.0.0")
    print("=" * 70)
    print("🔱 Initializing Sovereign Control Interface...")

    # Check if Omega system is available
    if not check_omega_system():
        return

    # Check if streamlit is installed
    try:
        import streamlit

        print("✅ Streamlit found")
    except ImportError:
        print("❌ Streamlit not found. Installing dependencies...")
        try:
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "streamlit",
                    "plotly",
                    "pandas",
                ]
            )
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies!")
            return

    print("🎯 Ready to launch Omega Dashboard...")

    # Launch dashboard
    launch_omega_dashboard()


if __name__ == "__main__":
    main()
