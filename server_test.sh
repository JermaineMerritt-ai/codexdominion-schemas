#!/bin/bash
# Quick server test script for Codex Dominion

echo "🔥 CODEX DOMINION SERVER TEST 🔥"
echo "================================="

echo "📍 Current location:"
pwd

echo -e "\n📋 Files in /opt/codex:"
ls -la

echo -e "\n🐍 Python version:"
python3 --version

echo -e "\n📦 Streamlit check:"
python3 -c "import streamlit; print('✅ Streamlit available')" 2>/dev/null || echo "❌ Streamlit not found - need to install"

echo -e "\n📄 Dashboard file check:"
if [ -f "codex_dashboard.py" ]; then
    echo "✅ codex_dashboard.py exists"
    head -5 codex_dashboard.py
else
    echo "❌ codex_dashboard.py not found"
fi

echo -e "\n🚨 Error log:"
if [ -f "/tmp/codex.log" ]; then
    cat /tmp/codex.log
else
    echo "No error log found at /tmp/codex.log"
fi

echo -e "\n🔌 Port 8095 status:"
netstat -tlnp | grep :8095 || echo "Port 8095 not in use"

echo -e "\n💡 Next steps:"
echo "1. If Streamlit missing: python3 -m pip install streamlit"
echo "2. Try running: python3 -m streamlit run codex_dashboard.py --server.port 8095 --server.address 0.0.0.0"
echo -e "\n🔥 CODEX DOMINION AWAITS! 🔥"
