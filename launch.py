#!/usr/bin/env python3
"""
CODEX DOMINION - QUICK LAUNCHER
Simplified launcher for the streamlined Codex dashboard
"""

import os
import subprocess
import sys
from pathlib import Path


def main():
    print("🔥 CODEX DOMINION - QUICK LAUNCHER 🔥")
    print("=====================================")
    print()

    # Check if app.py exists
    app_path = Path("app.py")
    if not app_path.exists():
        print("❌ app.py not found in current directory")
        print("   Please run this script from the Codex Dominion directory")
        return 1

    # Check for ledger file
    ledger_path = Path("codex_ledger.json")
    if not ledger_path.exists():
        print("⚠️  codex_ledger.json not found - will create default structure")
        print()

    print("🚀 Starting Codex Dashboard...")
    print("   Access at: http://localhost:8095")
    print("   Press Ctrl+C to stop")
    print()

    try:
        # Launch streamlit
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "app.py",
                "--server.port",
                "8095",
                "--server.headless",
                "false",
            ]
        )
    except KeyboardInterrupt:
        print("\n🛑 Codex Dashboard stopped")
        return 0
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
