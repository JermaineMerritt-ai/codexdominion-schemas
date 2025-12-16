"""
🚀 MASTER DASHBOARD LAUNCHER (Python 3.12 Compatible)
======================================================
Standalone launcher that works around Streamlit platform detection issues
"""

import sys
import io
# Fix Windows UTF-8 encoding for emojis
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def fix_streamlit_windows_issue():
    """Fix Windows platform detection issue in Python 3.12"""
    try:
        # Set environment variable to bypass platform checks
        os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
        print("✅ Applied Windows platform detection workaround")
    except Exception as e:
        print(f"⚠️  Platform fix warning: {e}")

def main():
    """Launch Master Dashboard Ultimate"""
    print("\n" + "="*80)
    print("👑 CODEX DOMINION MASTER DASHBOARD ULTIMATE LAUNCHER")
    print("="*80 + "\n")

    # Apply fix before importing streamlit
    fix_streamlit_windows_issue()

    print("📦 Loading Streamlit...")

    try:
        import streamlit.web.cli as stcli
        import streamlit as st

        print("✅ Streamlit loaded successfully\n")

        # Set up Streamlit configuration
        os.environ.setdefault('STREAMLIT_SERVER_PORT', '8501')
        os.environ.setdefault('STREAMLIT_SERVER_ADDRESS', 'localhost')
        os.environ.setdefault('STREAMLIT_BROWSER_GATHER_USAGE_STATS', 'false')

        dashboard_path = project_root / "main" / "master_dashboard_ultimate.py"

        if not dashboard_path.exists():
            print(f"❌ Dashboard not found at: {dashboard_path}")
            return 1

        print(f"🚀 Launching dashboard from: {dashboard_path}")
        print(f"🌐 URL: http://localhost:8501\n")
        print("="*80)
        print("Press Ctrl+C to stop the server")
        print("="*80 + "\n")

        # Launch Streamlit
        sys.argv = [
            "streamlit",
            "run",
            str(dashboard_path),
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ]

        sys.exit(stcli.main())

    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped by user")
        return 0
    except ImportError as e:
        print(f"\n❌ Streamlit not installed: {e}")
        print("\n💡 Install with: pip install streamlit")
        return 1
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
