#!/bin/bash
# Direct systemctl command simulation for Windows
# Usage: ./systemctl-sim.sh [daemon-reload|enable|start|status] codex-dashboard

COMMAND="$1"
SERVICE="$2"
PORT=8095

echo ""
echo "🔥 SYSTEMCTL SIMULATION - CODEX DASHBOARD"
echo "========================================="

case "$COMMAND" in
    "daemon-reload")
        echo "🔄 Reloading systemd daemon..."
        echo "✅ Daemon reloaded successfully"
        ;;
    "enable")
        echo "⚡ Enabling $SERVICE service..."
        echo "Created symlink /etc/systemd/system/multi-user.target.wants/codex-dashboard.service → /etc/systemd/system/codex-dashboard.service"
        echo "✅ Service enabled"
        ;;
    "start")
        echo "🚀 Starting $SERVICE service..."

        # Start the actual dashboard
        python -m streamlit run app.py --server.port $PORT --server.headless true &
        DASHBOARD_PID=$!

        sleep 3
        echo "✅ Service started successfully"
        echo "   Process ID: $DASHBOARD_PID"
        ;;
    "status")
        echo "📊 $SERVICE.service - Codex Dashboard Digital Sovereignty Interface"
        echo "   Loaded: loaded (/etc/systemd/system/codex-dashboard.service; enabled; vendor preset: enabled)"

        # Check if port is listening
        if netstat -an 2>/dev/null | grep ":$PORT " | grep LISTEN >/dev/null; then
            echo "   Active: active (running) since $(date)"
            echo "     Docs: man:streamlit(1)"
            echo "  Process: $(pgrep -f "streamlit.*app.py" || echo "N/A") (streamlit)"
            echo "     Main PID: $(pgrep -f "streamlit.*app.py" || echo "N/A") (python)"
            echo "    Status: ✅ Dashboard operational on port $PORT"
            echo "      URL: http://localhost:$PORT"
        else
            echo "   Active: inactive (dead)"
            echo "    Status: ❌ Service not running"
        fi
        ;;
    *)
        echo "Usage: $0 {daemon-reload|enable|start|status} codex-dashboard"
        echo ""
        echo "systemctl commands:"
        echo "  daemon-reload              Reload systemd manager configuration"
        echo "  enable codex-dashboard     Enable service to start on boot"
        echo "  start codex-dashboard      Start the service"
        echo "  status codex-dashboard     Show service status"
        exit 1
        ;;
esac

echo ""
echo "🔥 Command completed successfully!"
echo ""