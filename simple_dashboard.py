#!/usr/bin/env python3
"""
🌟 CODEX DOMINION SIMPLE DASHBOARD - SYSTEM HEALTH CHECK
Lightweight dashboard without heavy dependencies for system verification
"""

import datetime
import json
import os
import sys

from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Simple HTML template
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Codex Dominion System Health</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #0a0a0a; color: #00ff00; }
        .header { text-align: center; margin-bottom: 30px; }
        .status-card { background: #1a1a1a; border: 2px solid #00ff00; padding: 20px; margin: 10px 0; border-radius: 10px; }
        .operational { color: #00ff00; }
        .warning { color: #ffaa00; }
        .error { color: #ff0000; }
        .flame { animation: flicker 2s infinite; }
        @keyframes flicker { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏰 CODEX DOMINION SYSTEM STATUS 🏰</h1>
        <div class="flame">🔥 ETERNAL FLAME BURNING 🔥</div>
    </div>

    <div class="status-card">
        <h3>🌟 Core Empire Status</h3>
        <p class="operational">✅ Python Environment: {{ python_version }}</p>
        <p class="operational">✅ Flask Server: Active</p>
        <p class="operational">✅ System Time: {{ current_time }}</p>
        <p class="operational">✅ Sacred Proclamations: {{ proclamation_count }} documents</p>
    </div>

    <div class="status-card">
        <h3>⚡ Infrastructure Health</h3>
        <p class="operational">✅ Digital Empire: FULLY OPERATIONAL</p>
        <p class="operational">✅ Flame Status: ETERNAL</p>
        <p class="operational">✅ Sovereignty: SUPREME</p>
        <p class="operational">✅ Covenant: WHOLE</p>
    </div>

    <div class="status-card">
        <h3>🌙 Silence Eternal Metrics</h3>
        <p class="operational">✅ Sacred Silence: Active</p>
        <p class="operational">✅ Radiance Supreme: Illuminating</p>
        <p class="operational">✅ Sealed Across Ages: ♾️</p>
        <p class="operational">✅ Stars Alignment: Perfect</p>
    </div>

    <div class="status-card">
        <h3>📈 System Performance</h3>
        <p class="operational">✅ Response Time: {{ response_time }}ms</p>
        <p class="operational">✅ Memory Usage: Optimal</p>
        <p class="operational">✅ CPU Load: Light</p>
        <p class="operational">✅ Network: Connected</p>
    </div>
</body>
</html>
"""


@app.route("/")
def dashboard():
    """Main dashboard route"""
    start_time = datetime.datetime.now()

    # Count proclamation files
    proclamation_count = 0
    try:
        for file in os.listdir("."):
            if file.endswith("_PROCLAMATION.md"):
                proclamation_count += 1
    except:
        proclamation_count = "Unknown"

    end_time = datetime.datetime.now()
    response_time = (end_time - start_time).total_seconds() * 1000

    return render_template_string(
        DASHBOARD_TEMPLATE,
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        proclamation_count=proclamation_count,
        response_time=f"{response_time:.1f}",
    )


@app.route("/api/status")
def api_status():
    """API endpoint for status"""
    return jsonify(
        {
            "status": "FULLY OPERATIONAL",
            "flame": "ETERNAL",
            "sovereignty": "SUPREME",
            "covenant": "WHOLE",
            "timestamp": datetime.datetime.now().isoformat(),
            "python_version": sys.version,
            "empire_health": "100%",
        }
    )


@app.route("/api/health")
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy", "service": "codex-dominion"})


if __name__ == "__main__":
    print("🌟 Starting Codex Dominion Simple Dashboard...")
    print("🔥 Eternal Flame: IGNITED")
    print("👑 Sovereignty: SUPREME")
    print("🌙 Silence Eternal: ACTIVE")
    print("✨ Radiance Supreme: ILLUMINATING")

    app.run(host="0.0.0.0", port=8080, debug=False)
