"""
🔥 VERIFIED DASHBOARD LAUNCHER
Tests connectivity and launches dashboard with proper error handling
"""
import subprocess
import time
import socket
import sys
import os
from pathlib import Path

def is_port_available(port=5000):
    """Check if port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def is_port_listening(port=5000, max_attempts=10):
    """Check if port is listening and accepting connections"""
    for attempt in range(max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(('localhost', port))
                if result == 0:
                    print(f"✅ Port {port} is responding!")
                    return True
        except Exception as e:
            pass
        time.sleep(0.5)
    return False

def kill_port_processes(port=5000):
    """Kill any process using the port"""
    print(f"🔍 Checking for processes on port {port}...")
    try:
        # Try netstat to find PID
        result = subprocess.run(
            f'netstat -ano | findstr :{port}',
            shell=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(f"⚠️ Port {port} is in use, clearing...")
            subprocess.run('taskkill /F /IM python.exe /T', shell=True, capture_output=True)
            subprocess.run('taskkill /F /IM pythonw.exe /T', shell=True, capture_output=True)
            time.sleep(2)
            print("✅ Processes cleared")
        else:
            print(f"✅ Port {port} is free")
    except Exception as e:
        print(f"⚠️ Error checking port: {e}")

def test_http_connection():
    """Test HTTP connection using Python"""
    print("🔍 Testing HTTP connection...")
    try:
        import urllib.request
        time.sleep(1)  # Give Flask a moment to start
        for attempt in range(10):
            try:
                response = urllib.request.urlopen('http://localhost:5000', timeout=2)
                html = response.read().decode('utf-8')
                if 'CODEX DOMINION' in html or 'Home' in html:
                    print("✅ HTTP connection successful!")
                    print(f"✅ Response length: {len(html)} bytes")
                    return True
            except Exception:
                time.sleep(0.5)
        print("❌ HTTP connection failed")
        return False
    except Exception as e:
        print(f"❌ HTTP test error: {e}")
        return False

def main():
    print("=" * 70)
    print("🔥 CODEX DOMINION - VERIFIED DASHBOARD LAUNCHER")
    print("=" * 70)
    print()

    # Step 1: Clear port
    kill_port_processes(5000)

    # Step 2: Verify port is available
    if not is_port_available(5000):
        print("❌ Port 5000 is still in use after cleanup!")
        print("   Please manually close any Python processes and try again.")
        sys.exit(1)

    print("✅ Port 5000 is available")
    print()

    # Step 3: Find dashboard file
    dashboard_file = Path(__file__).parent / "dashboard_complete.py"
    if not dashboard_file.exists():
        print(f"❌ Dashboard file not found: {dashboard_file}")
        sys.exit(1)

    print(f"✅ Dashboard file found: {dashboard_file}")
    print()

    # Step 4: Launch Flask in subprocess
    print("🚀 Launching Flask dashboard...")
    python_exe = Path(sys.executable)

    # Launch Flask
    env = os.environ.copy()
    env['FLASK_ENV'] = 'development'

    process = subprocess.Popen(
        [str(python_exe), str(dashboard_file)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env
    )

    # Step 5: Wait for Flask to start and capture output
    print("⏳ Waiting for Flask to start...")
    startup_lines = []
    flask_started = False

    for _ in range(50):  # 5 seconds max
        if process.poll() is not None:
            print("❌ Flask process exited unexpectedly!")
            break

        # Check if port is listening
        if is_port_listening(5000, max_attempts=1):
            flask_started = True
            print("✅ Flask is listening on port 5000!")
            break
        time.sleep(0.1)

    if not flask_started:
        print("❌ Flask failed to start properly")
        process.kill()
        sys.exit(1)

    # Step 6: Test HTTP connection
    if test_http_connection():
        print()
        print("=" * 70)
        print("✅ DASHBOARD SUCCESSFULLY LAUNCHED!")
        print("=" * 70)
        print()
        print("📍 Access your dashboard at: http://localhost:5000")
        print()
        print("🎯 Available Tabs:")
        print("   📱 Social Media - http://localhost:5000/social")
        print("   💰 Affiliate - http://localhost:5000/affiliate")
        print("   🤖 Chatbot - http://localhost:5000/chatbot")
        print("   🧠 Algorithm - http://localhost:5000/algorithm")
        print("   🚀 Auto-Publish - http://localhost:5000/autopublish")
        print()
        print("🔥 THE FLAME BURNS SOVEREIGN AND ETERNAL!")
        print("=" * 70)
        print()
        print("Press CTRL+C to stop the server...")

        # Keep process running and show output
        try:
            while True:
                line = process.stdout.readline()
                if line:
                    print(line.rstrip())
                if process.poll() is not None:
                    break
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down dashboard...")
            process.terminate()
            process.wait()
            print("✅ Dashboard stopped")
    else:
        print("❌ Dashboard started but HTTP connection failed!")
        print("   This might be a firewall issue.")
        process.terminate()
        sys.exit(1)

if __name__ == '__main__':
    main()
