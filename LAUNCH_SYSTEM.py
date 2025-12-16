"""
🔥 CODEX DOMINION - UNIFIED SYSTEM LAUNCHER 👑
Simple, reliable dashboard launcher
"""
import sys
import io
import subprocess
import time

# Fix Windows UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("\n" + "=" * 70)
print("🔥 CODEX DOMINION - SYSTEM LAUNCHER 👑")
print("=" * 70 + "\n")

def kill_processes():
    """Clean up existing Python processes"""
    print("🔧 Cleaning up processes...")
    try:
        subprocess.run("taskkill /F /IM python.exe /T >nul 2>&1", shell=True)
        subprocess.run("taskkill /F /IM pythonw.exe /T >nul 2>&1", shell=True)
        time.sleep(2)
        print("✅ Cleanup complete\n")
    except:
        print("⚠️  Could not cleanup (may not be needed)\n")

def check_deps():
    """Check installed packages"""
    has_flask = False
    has_streamlit = False

    try:
        import flask
        has_flask = True
        print(f"✅ Flask {flask.__version__} installed")
    except:
        print("❌ Flask not installed")

    try:
        import streamlit
        has_streamlit = True
        print("✅ Streamlit installed")
    except:
        print("❌ Streamlit not installed")

    print()
    return has_flask, has_streamlit

def show_menu():
    """Show dashboard options"""
    print("📋 Available Dashboards:")
    print("-" * 70)
    print("1. Flask Complete Dashboard (RECOMMENDED)")
    print("   → 13 tabs: Social, Affiliate, Chatbot, Algorithm, Auto-Publish, etc.")
    print("   → File: dashboard_complete.py")
    print("   → URL: http://localhost:5000")
    print()
    print("2. Streamlit Master Dashboard Ultimate")
    print("   → AI Studio, 48 Intelligence Engines, Tools Suite")
    print("   → File: main/master_dashboard_ultimate.py")
    print("   → URL: http://localhost:8501")
    print()
    print("3. Flask Master Dashboard")
    print("   → 2182 lines, comprehensive features")
    print("   → File: flask_dashboard.py")
    print("   → URL: http://localhost:5000")
    print()
    print("0. Exit")
    print("-" * 70)

def launch_flask(filename, description):
    """Launch a Flask dashboard"""
    print(f"\n🚀 Launching {description}...")
    print(f"   File: {filename}")
    print(f"   URL: http://localhost:5000\n")
    print("-" * 70)

    # Launch in new window
    subprocess.Popen(
        f'start "CODEX DOMINION - {description}" cmd /k "python {filename}"',
        shell=True
    )

    print("⏳ Waiting for Flask to start...")
    time.sleep(4)

    # Open browser
    print("🌐 Opening browser...")
    subprocess.Popen('start http://localhost:5000', shell=True)

    print("\n✅ DASHBOARD LAUNCHED!")
    print("=" * 70)
    print("   Access: http://localhost:5000")
    print("   Dashboard is running in a separate window")
    print("=" * 70 + "\n")

def launch_streamlit(filename, description, port=8501):
    """Launch a Streamlit dashboard"""
    print(f"\n🚀 Launching {description}...")
    print(f"   File: {filename}")
    print(f"   URL: http://localhost:{port}\n")
    print("-" * 70)

    # Launch in new window
    subprocess.Popen(
        f'start "CODEX DOMINION - {description}" cmd /k "streamlit run {filename} --server.port {port}"',
        shell=True
    )

    print("⏳ Waiting for Streamlit to start...")
    time.sleep(5)

    # Open browser
    print("🌐 Opening browser...")
    subprocess.Popen(f'start http://localhost:{port}', shell=True)

    print("\n✅ DASHBOARD LAUNCHED!")
    print("=" * 70)
    print(f"   Access: http://localhost:{port}")
    print("   Dashboard is running in a separate window")
    print("=" * 70 + "\n")

def main():
    """Main launcher"""
    kill_processes()
    has_flask, has_streamlit = check_deps()

    if not has_flask and not has_streamlit:
        print("❌ ERROR: No dashboard frameworks installed!")
        print("\n   Install with:")
        print("   pip install Flask==3.1.2")
        print("   pip install streamlit")
        input("\n   Press Enter to exit...")
        return

    while True:
        show_menu()

        choice = input("\n👉 Select option (1-3, or 0 to exit): ").strip()

        if choice == "0":
            print("\n👑 Exiting launcher...")
            break
        elif choice == "1":
            if has_flask:
                launch_flask("dashboard_complete.py", "Flask Complete Dashboard")
                break
            else:
                print("\n❌ Flask not installed! Install with: pip install Flask==3.1.2\n")
        elif choice == "2":
            if has_streamlit:
                launch_streamlit("main/master_dashboard_ultimate.py", "Streamlit Master Dashboard")
                break
            else:
                print("\n❌ Streamlit not installed! Install with: pip install streamlit\n")
        elif choice == "3":
            if has_flask:
                launch_flask("flask_dashboard.py", "Flask Master Dashboard")
                break
            else:
                print("\n❌ Flask not installed! Install with: pip install Flask==3.1.2\n")
        else:
            print("\n⚠️  Invalid choice. Please select 1-3 or 0.\n")

    input("Press Enter to close this launcher window...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
