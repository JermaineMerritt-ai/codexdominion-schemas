#!/usr/bin/env python3
"""
Codex Ledger API Launcher
Simple launcher for the Codex Dominion Ledger API Service
"""

import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ["fastapi", "uvicorn", "pydantic"]
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - Available")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")

    if missing_packages:
        print(f"\n🚨 Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install fastapi uvicorn pydantic")
        return False

    return True


def start_ledger_api():
    """Start the Codex Ledger API service"""
    try:
        print("🚀 Starting Codex Ledger API Service...")
        print("=" * 50)

        # Check if API file exists
        api_file = Path("codex_ledger_api.py")
        if not api_file.exists():
            print("❌ codex_ledger_api.py not found!")
            return False

        # Check dependencies
        if not check_dependencies():
            return False

        print("\n📊 Service Information:")
        print("   - Host: 127.0.0.1")
        print("   - Port: 8001")
        print("   - API Docs: http://127.0.0.1:8001/docs")
        print("   - Health Check: http://127.0.0.1:8001/health")
        print("   - Interactive Docs: http://127.0.0.1:8001/redoc")
        print("")

        # Start the service
        print("🔄 Launching FastAPI service...")

        # Try using uvicorn directly
        try:
            import uvicorn

            print("✅ Using uvicorn directly")

            # Open browser to docs after a short delay
            def open_docs():
                time.sleep(3)  # Wait for server to start
                try:
                    webbrowser.open("http://127.0.0.1:8001/docs")
                    print("🌐 Opened API documentation in browser")
                except:
                    print("💡 Visit http://127.0.0.1:8001/docs for API documentation")

            # Start browser opening in background
            import threading

            browser_thread = threading.Thread(target=open_docs)
            browser_thread.daemon = True
            browser_thread.start()

            # Run the server
            uvicorn.run(
                "codex_ledger_api:app", host="127.0.0.1", port=8001, reload=True
            )

        except ImportError:
            print("⚠️  uvicorn not available, trying subprocess...")

            # Fallback to subprocess
            cmd = [sys.executable, "codex_ledger_api.py"]
            process = subprocess.Popen(cmd, cwd=os.getcwd())

            print(f"🚀 API service started with PID: {process.pid}")
            print("⏹️  Press Ctrl+C to stop the service")

            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping API service...")
                process.terminate()
                process.wait()
                print("✅ Service stopped")

        return True

    except Exception as e:
        print(f"❌ Failed to start API service: {e}")
        return False


def show_help():
    """Show help information"""
    print("Codex Ledger API Launcher")
    print("=" * 30)
    print("Usage: python launch_ledger_api.py [command]")
    print("")
    print("Commands:")
    print("  start    - Start the API service (default)")
    print("  help     - Show this help message")
    print("  test     - Test API endpoints")
    print("")
    print("API Endpoints:")
    print("  GET  /health     - Health check")
    print("  GET  /ledger     - Read ledger entries")
    print("  POST /ledger     - Write ledger entry")
    print("  GET  /treasury   - Read treasury data")
    print("  POST /treasury   - Write treasury transaction")
    print("  GET  /signals    - Read trading signals")
    print("  POST /signals    - Write trading signal")
    print("  GET  /pools      - Read AMM pools")
    print("  POST /pools      - Write AMM pool")
    print("  GET  /stats      - System statistics")
    print("")
    print("Documentation: http://127.0.0.1:8001/docs")


def test_endpoints():
    """Test API endpoints"""
    try:
        import json

        import requests

        base_url = "http://127.0.0.1:8001"

        print("🧪 Testing API Endpoints...")
        print("=" * 30)

        # Test health endpoint
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Health check - OK")
            else:
                print(f"❌ Health check - Failed ({response.status_code})")
        except requests.ConnectionError:
            print("❌ Cannot connect to API service")
            print(
                "💡 Make sure the service is running with: python launch_ledger_api.py start"
            )
            return
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return

        # Test ledger endpoint
        try:
            response = requests.get(f"{base_url}/ledger?limit=5", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Ledger read - OK ({data.get('count', 0)} entries)")
            else:
                print(f"❌ Ledger read - Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ Ledger test error: {e}")

        # Test signals endpoint
        try:
            response = requests.get(f"{base_url}/signals?tier=premium", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Signals read - OK ({data.get('count', 0)} signals)")
            else:
                print(f"❌ Signals read - Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ Signals test error: {e}")

        # Test stats endpoint
        try:
            response = requests.get(f"{base_url}/stats", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print("✅ Stats endpoint - OK")
                if "stats" in data:
                    stats = data["stats"]
                    print(
                        f"   📊 Total Revenue: ${stats['ledger']['total_revenue_usd']:,.2f}"
                    )
                    print(f"   📈 Active Signals: {stats['signals']['active_signals']}")
                    print(f"   🏊 Active Pools: {stats['pools']['active_pools']}")
            else:
                print(f"❌ Stats - Failed ({response.status_code})")
        except Exception as e:
            print(f"❌ Stats test error: {e}")

        print("\n🎉 API testing complete!")
        print("📖 Full documentation: http://127.0.0.1:8001/docs")

    except ImportError:
        print("❌ requests library not available")
        print("Install with: pip install requests")


def main():
    """Main launcher function"""
    # Get command from args
    command = sys.argv[1] if len(sys.argv) > 1 else "start"

    if command == "help":
        show_help()
    elif command == "test":
        test_endpoints()
    elif command == "start":
        start_ledger_api()
    else:
        print(f"Unknown command: {command}")
        print("Use 'python launch_ledger_api.py help' for usage")


if __name__ == "__main__":
    main()
