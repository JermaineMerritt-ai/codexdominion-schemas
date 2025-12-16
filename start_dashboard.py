"""
CODEX DOMINION - Dashboard Launcher
Ensures dashboard starts correctly with all routes operational
"""
import sys
import os

# Ensure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("\n" + "="*70)
print("CODEX DOMINION - DASHBOARD LAUNCHER")
print("="*70)

# Import and verify routes
print("\n1. Loading dashboard module...")
try:
    from dashboard_working import app
    print("   ✅ Dashboard module loaded successfully")
except Exception as e:
    print(f"   ❌ Failed to load dashboard: {e}")
    sys.exit(1)

print("\n2. Verifying routes...")
routes = [str(rule) for rule in app.url_map.iter_rules()]
print(f"   Total routes registered: {len(routes)}")
for route in routes:
    if route != '/static/<path:filename>':
        print(f"   ✅ {route}")

print("\n3. Starting Waitress server...")
print("   Host: 127.0.0.1")
print("   Port: 5000")
print("   Threads: 4")
print("\n" + "="*70)
print("ACCESS DASHBOARD: http://localhost:5000")
print("Press CTRL+C to stop")
print("="*70 + "\n")

try:
    from waitress import serve
    serve(app, host='127.0.0.1', port=5000, threads=4, _quiet=False)
except KeyboardInterrupt:
    print("\n\n✅ Dashboard stopped by user.\n")
except ImportError:
    print("\n❌ Waitress not installed. Installing...")
    os.system("pip install waitress")
    print("\nPlease run this script again.")
except Exception as e:
    print(f"\n\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
