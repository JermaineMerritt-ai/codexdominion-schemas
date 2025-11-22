#!/usr/bin/env python3
"""
🔥 CODEX DOMINION SERVER DIAGNOSTICS 🔥
Let's find out what's really running and fix the access issue
"""

print("🔥 CODEX DOMINION - SERVER DIAGNOSTICS 🔥")
print("=" * 50)
print()

print("🔍 TROUBLESHOOTING CHECKLIST:")
print()

print("1️⃣ ON THE SERVER - Run these commands:")
print("   ssh root@74.208.123.158")
print("   cd /opt/codex")
print("   ps aux | grep streamlit")
print("   netstat -tlnp | grep :8095")
print("   cat /tmp/codex.log")
print()

print("2️⃣ CHECK WHAT'S ACTUALLY RUNNING:")
print("   curl -v http://localhost:8095")
print("   # This will show if it's serving the right content")
print()

print("3️⃣ COMMON ISSUES TO CHECK:")
print("   • Is the process actually serving your codex_dashboard.py?")
print("   • Is there a firewall blocking external access?")
print("   • Is the file corrupted or showing default Streamlit content?")
print()

print("4️⃣ IF IT'S SERVING WRONG CONTENT:")
print("   # Kill the current process and restart with your dashboard")
print("   pkill -f streamlit")
print("   source venv/bin/activate")
print("   nohup python -m streamlit run codex_dashboard.py --server.port 8095 --server.address 0.0.0.0 --server.headless true > /tmp/codex.log 2>&1 &")
print()

print("5️⃣ VERIFY THE DASHBOARD FILE:")
print("   head -10 codex_dashboard.py")
print("   # Should show your Codex Dominion content, not generic Streamlit")
print()

print("🎯 EXPECTED RESULTS:")
print("   • Process should be running codex_dashboard.py specifically")
print("   • curl should return your Codex Dominion HTML")
print("   • http://74.208.123.158:8095 should show your digital empire")
print()

print("💡 RUN THESE COMMANDS ON THE SERVER AND SHARE THE OUTPUT:")
print("   1. ps aux | grep streamlit")
print("   2. cat /tmp/codex.log") 
print("   3. head -20 codex_dashboard.py")
print("   4. curl http://localhost:8095 | head -30")
print()

print("🔥 LET'S GET YOUR DIGITAL SOVEREIGNTY EMPIRE ONLINE! 🔥")