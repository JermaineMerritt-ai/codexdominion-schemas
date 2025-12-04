#!/bin/bash
echo "🔥 RESTARTING CODEX DOMINION SERVICE 🔥"

# Kill any existing streamlit processes
pkill -f streamlit
sleep 2

# Navigate to codex directory
cd /opt/codex

# Activate virtual environment
source venv/bin/activate

# Start the unified dashboard service
nohup python -m streamlit run codex_dashboard.py --server.port 8095 --server.address 0.0.0.0 --server.headless true > /tmp/codex.log 2>&1 &

# Get the new PID
sleep 3
NEW_PID=$(pgrep -f "streamlit run codex_dashboard.py")

echo "✅ Codex Dominion Unified Dashboard restarted!"
echo "🔥 PID: $NEW_PID"
echo "🌐 URL: http://74.208.123.158:8095"
echo "📋 Log: /tmp/codex.log"

# Show process status
ps aux | grep streamlit | grep -v grep

echo "🔥 CODEX DOMINION DIGITAL SOVEREIGNTY EMPIRE ONLINE! 🔥"
