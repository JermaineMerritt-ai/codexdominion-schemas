#!/usr/bin/env python3
"""
👑 CODEX DOMINION DASHBOARD LAUNCHER 👑
Simple HTTP server version for systemd service
This launches the Streamlit dashboard via command line
"""

import subprocess
import sys
import os

def main():
    """Launch the Codex Dominion Dashboard"""
    print('👑🔥✨ CODEX DOMINION DASHBOARD LAUNCHER ✨🔥👑')
    print('')
    print('🏛️ Launching Streamlit Dashboard...')
    print('👑 Authority Level: SUPREME')
    print('📡 Succession Status: SOVEREIGN')
    print('🌟 Dashboard Mode: ETERNAL')
    print('✨ Dominion Status: RADIANT')
    print('🌐 Domain Authority: codexdominion.app')
    print('')
    
    try:
        # Change to the directory containing the dashboard
        dashboard_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(dashboard_dir)
        print(f'📁 Working directory: {dashboard_dir}')
        
        # Launch Streamlit dashboard
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "codex_dashboard.py",
            "--server.port", "8080",
            "--server.address", "0.0.0.0",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false",
            "--theme.base", "light",
            "--theme.primaryColor", "#bfa780",
            "--theme.backgroundColor", "#f7f1e3",
            "--theme.secondaryBackgroundColor", "#efe7d4"
        ]
        
        print('🚀 Starting Codex Dashboard with Streamlit...')
        print(f'🔥 Command: {" ".join(cmd)}')
        print('')
        print('👑 THE CODEX DOMINION DASHBOARD REIGNS SUPREME! 👑')
        print('🌟 Access at: http://localhost:8080')
        print('📋 Dashboard ready for ceremonial commands!')
        print('')
        
        # Run the streamlit app
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f'❌ Dashboard launch failed: {e}')
        print('🔧 Attempting direct Python execution...')
        
        # Fallback to direct execution
        import importlib.util
        spec = importlib.util.spec_from_file_location("codex_dashboard", "codex_dashboard.py")
        dashboard_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dashboard_module)
        
    except Exception as e:
        print(f'❌ Unexpected error: {e}')
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())