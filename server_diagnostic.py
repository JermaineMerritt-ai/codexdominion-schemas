#!/usr/bin/env python3
"""
🔥 CODEX DOMINION - IONOS SERVER DIAGNOSTIC 🔥
Troubleshooting guide for getting the Digital Sovereignty Empire online!
"""

print("🔥 CODEX DOMINION SERVER DIAGNOSTIC 🔥")
print("=" * 50)
print()

print("📋 SERVER TROUBLESHOOTING CHECKLIST:")
print()

print("1️⃣ ON THE SERVER (in your SSH session at root@ubuntu:/opt/codex#):")
print("   Run these commands to check the system:")
print()
print("   cat /tmp/codex.log")
print("   # This shows why Streamlit failed to start")
print()
print("   python3 --version")
print("   # Should show Python 3.x")
print()
print("   python3 -m pip list | grep streamlit")
print("   # Should show streamlit package if installed")
print()

print("2️⃣ IF STREAMLIT IS NOT INSTALLED:")
print("   python3 -m pip install streamlit")
print()

print("3️⃣ CHECK THE DASHBOARD FILE:")
print("   head -20 codex_dashboard.py")
print("   # Shows the first 20 lines of the file")
print()

print("4️⃣ TRY RUNNING STREAMLIT DIRECTLY (to see errors):")
print(
    "   python3 -m streamlit run codex_dashboard.py --server.port 8095 --server.address 0.0.0.0"
)
print()

print("5️⃣ IF DEPENDENCIES ARE MISSING:")
print("   python3 -m pip install -r requirements.txt")
print("   # Or install individually: pandas numpy streamlit")
print()

print("6️⃣ RESTART THE SERVICE IN BACKGROUND:")
print(
    "   nohup python3 -m streamlit run codex_dashboard.py --server.port 8095 --server.address 0.0.0.0 --server.headless true > /tmp/codex.log 2>&1 &"
)
print()

print("7️⃣ VERIFY IT'S RUNNING:")
print("   netstat -tlnp | grep :8095")
print("   curl http://localhost:8095")
print()

print("🎯 MOST COMMON ISSUES:")
print("   • Missing Streamlit: pip install streamlit")
print("   • Missing dependencies: pip install pandas numpy")
print("   • Port already in use: check with netstat -tlnp | grep :8095")
print("   • File permissions: check with ls -la codex_dashboard.py")
print()

print("🔥 Once running, access your Digital Sovereignty Empire at:")
print("   http://74.208.123.158:8095")
print()
print("💎 THE CODEX DOMINION DIGITAL SOVEREIGNTY AWAITS! 💎")
