"""
Codex Dominion - All Systems Status & Quick Launcher
Check system health and launch any service quickly.
"""

import json
import os
import subprocess
import sys
import socket
from datetime import datetime

def print_header(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def check_port_in_use(port):
    """Check if a port is in use"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    except:
        return False

def get_system_status():
    """Check status of all systems"""
    systems = {
        "Main Dashboard": {"port": 5555, "script": "dashboard_working.py"},
        "Unified Launcher": {"port": 5556, "script": "unified_launcher.py"},
        "Workflow Builder": {"port": 5557, "script": "workflow_builder_web.py"},
        "Jermaine AI": {"port": 8501, "script": "jermaine_super_action_ai.py", "streamlit": True},
        "Audio Studio": {"port": 8502, "script": "audio_studio.py", "streamlit": True},
        "Stock Analytics": {"port": 8515, "script": "ai_action_stock_analytics.py", "streamlit": True},
        "Analytics Dashboard": {"port": 8516, "script": "analytics_dashboard.py", "streamlit": True},
    }

    status = {}
    for name, info in systems.items():
        running = check_port_in_use(info["port"])
        status[name] = {
            "running": running,
            "port": info["port"],
            "script": info["script"],
            "streamlit": info.get("streamlit", False),
            "url": f"http://localhost:{info['port']}"
        }

    return status

def launch_system(script, port, streamlit=False):
    """Launch a system"""
    if streamlit:
        cmd = f'streamlit run {script} --server.port {port}'
    else:
        cmd = f'python {script}'

    print(f"\n🚀 Starting {script}...")
    subprocess.Popen(
        ['powershell', '-NoExit', '-Command', f'cd "{os.getcwd()}"; {cmd}'],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    print(f"✅ Launched in new window on port {port}")

def main():
    print_header("🔷 CODEX DOMINION - SYSTEM STATUS & LAUNCHER")

    # Get system status
    status = get_system_status()

    # Display status
    print("📊 SYSTEM STATUS:\n")
    for name, info in status.items():
        status_icon = "🟢" if info["running"] else "🔴"
        status_text = "RUNNING" if info["running"] else "STOPPED"
        print(f"{status_icon} {name:25s} [{status_text}] - Port {info['port']}")
        if info["running"]:
            print(f"   URL: {info['url']}")

    # Count running systems
    running_count = sum(1 for s in status.values() if s["running"])
    total_count = len(status)

    print(f"\n📈 Systems Running: {running_count}/{total_count}")

    # Quick launch menu
    print_header("🚀 QUICK LAUNCH MENU")
    print("1. 🎛️  Main Dashboard (Port 5555)")
    print("2. 🚀 Unified Launcher (Port 5556)")
    print("3. 🔷 Workflow Builder Web UI (Port 5557)")
    print("4. 🛒 Store Manager")
    print("5. 🤖 Jermaine Super AI (Port 8501)")
    print("6. 🎵 Audio Studio (Port 8502)")
    print("7. 📊 Stock Analytics (Port 8515)")
    print("8. 📈 Analytics Dashboard (Port 8516)")
    print("9. 🔄 Refresh Status")
    print("0. 🚪 Exit")

    choice = input("\n👉 Select option: ").strip()

    if choice == "1":
        launch_system("dashboard_working.py", 5555)
    elif choice == "2":
        launch_system("unified_launcher.py", 5556)
    elif choice == "3":
        launch_system("workflow_builder_web.py", 5557)
    elif choice == "4":
        launch_system("store_manager.py", 0)
    elif choice == "5":
        launch_system("jermaine_super_action_ai.py", 8501, streamlit=True)
    elif choice == "6":
        launch_system("audio_studio.py", 8502, streamlit=True)
    elif choice == "7":
        launch_system("ai_action_stock_analytics.py", 8515, streamlit=True)
    elif choice == "8":
        launch_system("analytics_dashboard.py", 8516, streamlit=True)
    elif choice == "9":
        main()  # Refresh
    elif choice == "0":
        print("\n👋 Goodbye!")
        return
    else:
        print("\n❌ Invalid option!")

    # Ask if want to launch another
    another = input("\n🔄 Launch another system? (y/n): ").strip().lower()
    if another == 'y':
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Launcher closed!")
