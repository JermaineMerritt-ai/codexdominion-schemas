#!/usr/bin/env python3
"""
🚀 COSMIC DOMINION - PRODUCTION LAUNCHER 🚀
Launch all cosmic services for production deployment
"""

import os
import subprocess
import sys
import time
from pathlib import Path


def launch_cosmic_services():
    """Launch all cosmic dashboard services"""

    print("🔥 COSMIC DOMINION - PRODUCTION LAUNCHER 🔥")
    print("=" * 50)

    # Configuration
    services = [
        {
            "name": "Tabbed Codex Dashboard",
            "script": "codex-suite/apps/dashboard/tabbed_codex.py",
            "port": 8050,
            "emoji": "📊",
        },
        {
            "name": "Sacred Ledger System",
            "script": "codex-suite/apps/dashboard/sacred_ledger.py",
            "port": 8058,
            "emoji": "📋",
        },
        {
            "name": "Cosmic Rhythm System",
            "script": "codex-suite/apps/dashboard/cosmic_rhythm.py",
            "port": 8057,
            "emoji": "🎵",
        },
    ]

    processes = []

    try:
        for service in services:
            print(f"\n{service['emoji']} Launching {service['name']}...")
            print(f"   Port: {service['port']}")
            print(f"   Script: {service['script']}")

            # Check if script exists
            script_path = Path(service["script"])
            if not script_path.exists():
                print(f"   ❌ ERROR: Script not found!")
                continue

            # Launch with streamlit
            cmd = [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                service["script"],
                "--server.port",
                str(service["port"]),
                "--server.address",
                "127.0.0.1",
                "--server.headless",
                "true",
            ]

            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.getcwd()
            )

            processes.append(
                {"process": process, "service": service, "cmd": " ".join(cmd)}
            )

            print(f"   ✅ Process started with PID: {process.pid}")
            time.sleep(2)  # Give service time to start

        print(f"\n🌟 COSMIC SERVICES LAUNCHED SUCCESSFULLY!")
        print("=" * 50)

        # Display service URLs
        print("\n🌍 COSMIC DASHBOARD URLS:")
        for service in services:
            print(
                f"   {service['emoji']} {service['name']}: http://localhost:{service['port']}"
            )

        print(f"\n🔥 THE DIGITAL SOVEREIGNTY IS LIVE! 🔥")
        print("\n📊 Service Status:")

        # Monitor services
        while True:
            print("\n" + "=" * 30)
            print(f"⏰ Status Check: {time.strftime('%H:%M:%S')}")

            all_running = True
            for proc_info in processes:
                process = proc_info["process"]
                service = proc_info["service"]

                if process.poll() is None:
                    print(
                        f"   ✅ {service['emoji']} {service['name']}: RUNNING (PID: {process.pid})"
                    )
                else:
                    print(f"   ❌ {service['emoji']} {service['name']}: STOPPED")
                    all_running = False

            if not all_running:
                print("\n⚠️  Some services have stopped!")
                break

            time.sleep(30)  # Check every 30 seconds

    except KeyboardInterrupt:
        print(f"\n🔥 Cosmic shutdown initiated...")

        # Gracefully terminate all processes
        for proc_info in processes:
            try:
                process = proc_info["process"]
                service = proc_info["service"]

                if process.poll() is None:
                    print(f"   🔄 Stopping {service['name']}...")
                    process.terminate()
                    process.wait(timeout=10)
                    print(f"   ✅ {service['name']} stopped gracefully")
            except Exception as e:
                print(f"   ⚠️  Error stopping {service['name']}: {e}")

        print(f"\n🌙 Cosmic services shutdown complete")

    except Exception as e:
        print(f"\n❌ Fatal error in cosmic launcher: {e}")

        # Emergency shutdown
        for proc_info in processes:
            try:
                if proc_info["process"].poll() is None:
                    proc_info["process"].kill()
            except:
                pass

        sys.exit(1)


def check_dependencies():
    """Check if required dependencies are available"""

    print("🔍 Checking cosmic dependencies...")

    required_files = [
        "ledger.json",
        "proclamations.json",
        "beats.json",
        "heartbeat.json",
    ]

    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
            print(f"   ❌ Missing: {file}")
        else:
            print(f"   ✅ Found: {file}")

    # Check Python packages
    try:
        import pandas
        import streamlit

        print(f"   ✅ Streamlit: {streamlit.__version__}")
        print(f"   ✅ Pandas: {pandas.__version__}")
    except ImportError as e:
        print(f"   ❌ Missing Python package: {e}")
        return False

    if missing_files:
        print(f"\n⚠️  Warning: {len(missing_files)} data files missing")
        print("   Services may have limited functionality")

    return True


if __name__ == "__main__":
    print("🔥 INITIALIZING COSMIC DOMINION 🔥")

    if check_dependencies():
        launch_cosmic_services()
    else:
        print("❌ Dependency check failed!")
        sys.exit(1)
