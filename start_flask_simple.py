#!/usr/bin/env python
"""
Simple Flask launcher that stays alive
Bypasses all the complexity and just runs Flask directly
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔥 STARTING FLASK DASHBOARD 👑")
print("=" * 60)

try:
    # Import the Flask app
    print("📦 Importing flask_dashboard...")
    from flask_dashboard import app
    print("✅ Flask app imported successfully")
    
    print("")
    print("🚀 Starting server on http://0.0.0.0:5000")
    print("   Local:   http://localhost:5000")
    print("   Network: http://192.168.254.11:5000")
    print("")
    print("⚠️  Press CTRL+C to quit")
    print("=" * 60)
    print("")
    
    # Run Flask with minimal options to prevent early exit
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True
    )
    
except KeyboardInterrupt:
    print("\n\n✅ Flask stopped by user (Ctrl+C)")
    sys.exit(0)
    
except Exception as e:
    print(f"\n\n❌ FATAL ERROR: {e}")
    import traceback
    traceback.print_exc()
    print("\n\nFlask failed to start. Check the error above.")
    sys.exit(1)
