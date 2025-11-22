#!/bin/bash
# CODEX DOMINION SERVER DIAGNOSTIC SCRIPT
# Run this on your IONOS server: 74.208.123.158
echo "🔥 CODEX DOMINION SERVER DIAGNOSTIC"
echo "===================================="
echo ""

echo "1. CHECKING PORT 8095:"
echo "====================="
netstat -tlnp | grep :8095
echo ""

echo "2. TESTING LOCAL CONNECTION:"
echo "============================"
curl -I http://localhost:8095 2>/dev/null || echo "❌ No response from localhost:8095"
echo ""

echo "3. CHECKING SERVICE STATUS:"
echo "==========================="
systemctl status codex-dashboard --no-pager -l
echo ""

echo "4. CHECKING SERVICE LOGS:"
echo "========================="
journalctl -u codex-dashboard --no-pager -l | tail -20
echo ""

echo "5. CHECKING FIREWALL:"
echo "===================="
ufw status
echo ""

echo "6. CHECKING RUNNING PROCESSES:"
echo "=============================="
ps aux | grep -i streamlit | grep -v grep
ps aux | grep python3 | grep -v grep
echo ""

echo "7. CHECKING DEPLOYMENT FILES:"
echo "============================="
find /tmp -name "codex*" -o -name "ionos*" 2>/dev/null
find /opt -name "codex*" 2>/dev/null
find /home -name "codex*" 2>/dev/null
echo ""

echo "8. NETWORK INTERFACE CHECK:"
echo "==========================="
ip addr show | grep inet
echo ""

echo "🎯 DIAGNOSTIC COMPLETE"
echo "======================"