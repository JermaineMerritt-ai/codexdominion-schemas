# Codex Dashboard Status Checker for Windows
# This is the Windows equivalent of 'systemctl status codex-dashboard.service'

import json
import subprocess
import sys
from datetime import datetime


def check_dashboard_status():
    """Check the status of Codex Dashboard services on Windows"""
    print("🔍 CODEX DASHBOARD STATUS CHECK")
    print("=" * 50)
    print(f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Check ports
    ports_to_check = {
        "8000": "FastAPI Backend",
        "8501": "Streamlit Dashboard (Primary)",
        "8502": "Streamlit Dashboard (Secondary)",
    }

    print("🔍 PORT STATUS:")
    print("-" * 25)

    try:
        result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
        netstat_output = result.stdout

        for port, service in ports_to_check.items():
            if f":{port}" in netstat_output and "LISTENING" in netstat_output:
                # Extract PID
                lines = [
                    line
                    for line in netstat_output.split("\n")
                    if f":{port}" in line and "LISTENING" in line
                ]
                if lines:
                    pid = lines[0].split()[-1]
                    print(f"✅ {service}")
                    print(f"   Port: {port} | PID: {pid}")

                    # Get process name
                    try:
                        tasklist_result = subprocess.run(
                            ["tasklist", "/FI", f"PID eq {pid}"],
                            capture_output=True,
                            text=True,
                        )
                        if "python.exe" in tasklist_result.stdout:
                            print(f"   Process: Python (Likely Streamlit/FastAPI)")
                        else:
                            print(
                                f"   Process: {tasklist_result.stdout.split()[0] if tasklist_result.stdout.split() else 'Unknown'}"
                            )
                    except:
                        print(f"   Process: Unknown")
                else:
                    print(f"❌ {service}: Port {port} - Not listening")
            else:
                print(f"❌ {service}: Port {port} - Not active")

        print()
        print("🌐 ACCESS URLS:")
        print("-" * 20)

        # Check which URLs are accessible
        accessible_urls = []

        if ":8000" in netstat_output and "LISTENING" in netstat_output:
            accessible_urls.append("🔗 FastAPI Backend: http://127.0.0.1:8000")
            accessible_urls.append("📚 API Documentation: http://127.0.0.1:8000/docs")

        if ":8501" in netstat_output and "LISTENING" in netstat_output:
            accessible_urls.append("📊 Main Dashboard: http://127.0.0.1:8501")

        if ":8502" in netstat_output and "LISTENING" in netstat_output:
            accessible_urls.append("📊 Secondary Dashboard: http://127.0.0.1:8502")

        if accessible_urls:
            for url in accessible_urls:
                print(url)
        else:
            print("❌ No services currently accessible")

        print()
        print("⚡ QUICK ACTIONS:")
        print("-" * 20)
        print(
            "To start dashboard: python -m streamlit run codex_simple_dashboard.py --server.port 8502"
        )
        print(
            "To start API: python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
        )
        print("To check status: python dashboard_status.py")

    except Exception as e:
        print(f"❌ Error checking status: {e}")


if __name__ == "__main__":
    check_dashboard_status()
