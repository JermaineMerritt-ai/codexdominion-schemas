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
