#!/usr/bin/env python3
"""
Launch Ultimate Comprehensive Intelligence Dashboard
=================================================

Launches the master dashboard integrating all 24 knowledge domains.
"""

import os
import subprocess
import sys
from pathlib import Path


def launch_ultimate_intelligence():
    """Launch the ultimate comprehensive intelligence dashboard"""

    dashboard_file = (
        Path(__file__).parent / "ultimate_comprehensive_intelligence_dashboard.py"
    )

    if not dashboard_file.exists():
        print(f"❌ Dashboard file not found: {dashboard_file}")
        return False

    print("🌟 Launching Ultimate Comprehensive Intelligence Dashboard...")
    print("📊 Integrating all 24 elite knowledge domains...")
    print("🤖 AI Trinity Enhanced Intelligence System")
    print("🔥 Port: 8507")
    print("\n" + "=" * 60)

    try:
        # Launch with Streamlit
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(dashboard_file),
                "--server.port",
                "8507",
                "--server.headless",
                "true",
                "--server.address",
                "localhost",
                "--browser.gatherUsageStats",
                "false",
            ],
            check=True,
        )

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch dashboard: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
        return True


if __name__ == "__main__":
    success = launch_ultimate_intelligence()
    if success:
        print("✅ Dashboard launched successfully!")
    else:
        print("❌ Failed to launch dashboard")
        sys.exit(1)
