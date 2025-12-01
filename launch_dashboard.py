#!/usr/bin/env python3
"""
🚀 CODEX DOMINION DASHBOARD LAUNCHER
Installs dependencies and launches the Digital Empire Command Center
"""

import os
import subprocess
import sys
from pathlib import Path


def install_dashboard_dependencies():
    """Install additional dashboard dependencies."""
    print("📦 Installing dashboard dependencies...")

    additional_deps = [
        "plotly>=5.17.0",
        "streamlit-plotly-events>=0.0.6",
        "altair>=5.1.0",
    ]

    for dep in additional_deps:
        try:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}: {e}")
            return False

    return True


def launch_dashboard():
    """Launch the Streamlit dashboard."""
    dashboard_file = Path(__file__).parent / "dashboard_app.py"

    if not dashboard_file.exists():
        print("❌ Dashboard app not found!")
        return False

    print("🚀 Launching Codex Dominion Dashboard...")
    print("🌍 Production: https://aistorelab.com")
    print("🔧 Staging: https://staging.aistorelab.com")
    print("💻 Local: http://localhost:8501")
    print("-" * 60)

    try:
        # Launch Streamlit
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(dashboard_file),
                "--server.port",
                "8501",
                "--server.address",
                "0.0.0.0",
                "--server.headless",
                "true",
            ]
        )
    except KeyboardInterrupt:
        print("\n👑 Dashboard shutdown complete. Empire remains supreme!")
    except Exception as e:
        print(f"❌ Dashboard launch failed: {e}")
        return False

    return True


def main():
    """Main launcher function."""
    print("👑 CODEX DOMINION DASHBOARD LAUNCHER v1.0.0")
    print("=" * 60)
    print("🏛️ Initializing Digital Empire Command Center...")

    # Check if streamlit is installed
    try:
        import streamlit

        print("✅ Streamlit found")
    except ImportError:
        print("❌ Streamlit not found. Please install requirements.txt first:")
        print("   pip install -r requirements.txt")
        return

    # Install additional dependencies
    if not install_dashboard_dependencies():
        print("❌ Failed to install dependencies!")
        return

    print("✅ All dependencies installed successfully!")
    print("\n🎯 Ready to launch dashboard...")

    # Launch dashboard
    launch_dashboard()


if __name__ == "__main__":
    main()
