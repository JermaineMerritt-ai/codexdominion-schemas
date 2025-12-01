#!/bin/bash
"""
CODEX DOMINION - SERVICE DEPLOYMENT SCRIPT

This script creates systemd service files for the complete Codex Dominion
digital sovereignty dashboard ecosystem.
"""

# Create service files for the Codex Dominion ecosystem
create_codex_services() {
    echo "🔥 Creating Codex Dominion Service Files..."

    # Main Dashboard Service
    cat > /etc/systemd/system/codex-main.service << 'EOF'
[Unit]
Description=Codex Dominion - Main Dashboard
After=network.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/codex
ExecStart=/usr/bin/python -m streamlit run codex_summary.py --server.port=8080 --server.address=0.0.0.0
Restart=always
RestartSec=10
User=codex
Group=codex

# Security
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/srv/codex

# Environment
Environment=PYTHONPATH=/srv/codex
Environment=STREAMLIT_SERVER_HEADLESS=true

StandardOutput=journal
StandardError=journal
SyslogIdentifier=codex-main

[Install]
WantedBy=multi-user.target
EOF

    # Contributions Interface Service
    cat > /etc/systemd/system/codex-contributions.service << 'EOF'
[Unit]
Description=Codex Dominion - Community Contributions Interface
After=network.target codex-main.service
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/codex
ExecStart=/usr/bin/python -m streamlit run contributions.py --server.port=8083 --server.address=0.0.0.0
Restart=always
RestartSec=10
User=codex
Group=codex

NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/srv/codex

Environment=PYTHONPATH=/srv/codex
Environment=STREAMLIT_SERVER_HEADLESS=true

StandardOutput=journal
StandardError=journal
SyslogIdentifier=codex-contributions

[Install]
WantedBy=multi-user.target
EOF

    # Council Oversight Service
    cat > /etc/systemd/system/codex-council.service << 'EOF'
[Unit]
Description=Codex Dominion - Council Oversight Interface
After=network.target codex-main.service
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/codex
ExecStart=/usr/bin/python -m streamlit run enhanced_council_oversight.py --server.port=8086 --server.address=0.0.0.0
Restart=always
RestartSec=10
User=codex
Group=codex

NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/srv/codex

Environment=PYTHONPATH=/srv/codex
Environment=STREAMLIT_SERVER_HEADLESS=true

StandardOutput=journal
StandardError=journal
SyslogIdentifier=codex-council

[Install]
WantedBy=multi-user.target
EOF

    # Contributions Viewer Service
    cat > /etc/systemd/system/codex-viewer.service << 'EOF'
[Unit]
Description=Codex Dominion - Contributions Viewer
After=network.target codex-main.service
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/srv/codex
ExecStart=/usr/bin/python -m streamlit run contributions_viewer.py --server.port=8090 --server.address=0.0.0.0
Restart=always
RestartSec=10
User=codex
Group=codex

NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/srv/codex

Environment=PYTHONPATH=/srv/codex
Environment=STREAMLIT_SERVER_HEADLESS=true

StandardOutput=journal
StandardError=journal
SyslogIdentifier=codex-viewer

[Install]
WantedBy=multi-user.target
EOF

    echo "✅ Service files created successfully!"
}

# Setup deployment function
deploy_services() {
    echo "🚀 Deploying Codex Dominion Services..."

    # Create codex user if it doesn't exist
    if ! id "codex" &>/dev/null; then
        useradd -r -s /bin/false -d /srv/codex codex
        echo "👤 Created codex user"
    fi

    # Create directory structure
    mkdir -p /srv/codex
    chown codex:codex /srv/codex
    chmod 755 /srv/codex

    # Copy application files (would need to be adapted for actual deployment)
    echo "📁 Setting up application directory..."

    # Reload systemd
    systemctl daemon-reload

    # Enable services
    systemctl enable codex-main.service
    systemctl enable codex-contributions.service
    systemctl enable codex-council.service
    systemctl enable codex-viewer.service

    echo "⚡ Services enabled!"

    # Start services
    systemctl start codex-main.service
    systemctl start codex-contributions.service
    systemctl start codex-council.service
    systemctl start codex-viewer.service

    echo "🔥 Codex Dominion services started!"

    # Show status
    echo "📊 Service Status:"
    systemctl status codex-main.service --no-pager -l
    systemctl status codex-contributions.service --no-pager -l
    systemctl status codex-council.service --no-pager -l
    systemctl status codex-viewer.service --no-pager -l
}

# Management functions
start_codex() {
    echo "🔥 Starting Codex Dominion Digital Empire..."
    systemctl start codex-main.service
    systemctl start codex-contributions.service
    systemctl start codex-council.service
    systemctl start codex-viewer.service
    echo "⚡ Digital sovereignty activated!"
}

stop_codex() {
    echo "🛑 Stopping Codex Dominion services..."
    systemctl stop codex-main.service
    systemctl stop codex-contributions.service
    systemctl stop codex-council.service
    systemctl stop codex-viewer.service
    echo "💤 Services stopped"
}

status_codex() {
    echo "📊 Codex Dominion Service Status:"
    echo "================================="
    systemctl is-active codex-main.service
    systemctl is-active codex-contributions.service
    systemctl is-active codex-council.service
    systemctl is-active codex-viewer.service
}

# Main execution
case "$1" in
    create)
        create_codex_services
        ;;
    deploy)
        create_codex_services
        deploy_services
        ;;
    start)
        start_codex
        ;;
    stop)
        stop_codex
        ;;
    status)
        status_codex
        ;;
    restart)
        stop_codex
        sleep 2
        start_codex
        ;;
    *)
        echo "Usage: $0 {create|deploy|start|stop|status|restart}"
        echo ""
        echo "Commands:"
        echo "  create  - Create service files only"
        echo "  deploy  - Create and deploy all services"
        echo "  start   - Start Codex Dominion services"
        echo "  stop    - Stop Codex Dominion services"
        echo "  status  - Check service status"
        echo "  restart - Restart all services"
        exit 1
        ;;
esac