"""
🚀 CODEX DOMINION - COMPLETE AUTOMATION LAUNCHER
================================================
Launches Flask dashboard with ALL NEW automation systems integrated

This is your ONE-CLICK launcher for the complete system!
"""

import sys
from datetime import datetime

print("=" * 70)
print("🔥 CODEX DOMINION - COMPLETE AUTOMATION SYSTEM")
print("=" * 70)
print(f"🕐 Launch Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Display system info
print("📊 SYSTEM COMPONENTS:")
print("  ✅ Flask Dashboard (18 navigation tabs)")
print("  ✅ 48 Intelligence Engines")
print("  ✅ 6 Free Tools Suite")
print("  ✅ 52 Dashboards")
print("  ✅ AI Chat (6 models)")
print()

print("🆕 NEW AUTOMATION SYSTEMS:")
print("  ✅ Website Builder - Build unlimited websites")
print("  ✅ Store Builder - E-commerce automation")
print("  ✅ Social Media Automation - 6 platforms")
print("  ✅ Affiliate Marketing - Full campaign management")
print("  ✅ Action Chatbot AI - Multi-platform conversational AI")
print("  ✅ Algorithm Action AI - Content optimization")
print("  ✅ Auto-Publish Orchestration - Jermaine Super Action AI")
print()

print("=" * 70)
print("🚀 LAUNCHING DASHBOARD...")
print("=" * 70)
print()
print("📍 Your dashboard will open at: http://localhost:5000")
print()
print("🎯 NEW PAGES TO EXPLORE:")
print("  • http://localhost:5000/websites - Website Builder")
print("  • http://localhost:5000/stores - Store Builder")
print("  • http://localhost:5000/social - Social Media Automation")
print("  • http://localhost:5000/affiliate - Affiliate Marketing")
print("  • http://localhost:5000/chatbot - Action Chatbot AI")
print("  • http://localhost:5000/algorithm - Algorithm Action AI")
print("  • http://localhost:5000/autopublish - Auto-Publish (Jermaine AI)")
print()
print("💡 PRO TIP:")
print("  Go to /autopublish and click 'Enable Auto-Publish' to start")
print("  full automation across all systems!")
print()
print("=" * 70)
print("🔥 THE FLAME BURNS SOVEREIGN AND ETERNAL! 👑")
print("=" * 70)
print()
print("⌨️ Press Ctrl+C to stop")
print()

# Launch Flask
try:
    print("⏳ Loading Flask application...")
    from flask_dashboard import app
    print("✅ Flask loaded successfully!")
    print()
    app.run(debug=True, host='0.0.0.0', port=5000)
except KeyboardInterrupt:
    print()
    print("=" * 70)
    print("🛑 Dashboard stopped by user")
    print("=" * 70)
except Exception as e:
    print()
    print(f"❌ Error: {e}")
    print()
    print("🔧 Troubleshooting:")
    print("  1. Make sure you're in the virtual environment")
    print("  2. Try: python flask_dashboard.py")
    print("  3. Check that Flask is installed: pip install flask")
