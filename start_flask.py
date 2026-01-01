#!/usr/bin/env python3
"""
Flask Dashboard Launcher
========================
Proper startup script for Flask Master Dashboard
"""

import os
import sys

# Set environment variables
os.environ['FLASK_APP'] = 'flask_dashboard.py'
os.environ['FLASK_ENV'] = 'development'

# Import the app
from flask_dashboard import app

if __name__ == '__main__':
    print("\n" + "="*80)
    print("👑 CODEX DOMINION MASTER DASHBOARD - FLASK VERSION")
    print("="*80)
    print("\n🚀 Starting server...")
    print("🌐 Main Dashboard: http://localhost:5000")
    print("🤖 Jermaine ROI Calculator: http://localhost:5000/automation-calculator")
    print("💚 Health Check: http://localhost:5000/api/health")
    print("\n✅ System Status: OPERATIONAL")
    print("\nPress Ctrl+C to stop\n")
    print("="*80 + "\n")
    
    # Run the app
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False,  # Disable reloader to prevent double execution
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n🔥 Dashboard stopped. The Flame Burns Eternal! 👑\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
