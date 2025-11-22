#!/bin/bash
# Linux systemd service management for Codex Dashboard
# This script provides the systemctl functionality you requested

SERVICE_NAME="codex-dashboard"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
WORKING_DIR="/srv/codex"
USER="codex"
GROUP="codex"

echo "🔥 CODEX DASHBOARD SYSTEMD SERVICE MANAGEMENT"
echo "=============================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

function check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo -e "${RED}❌ This script must be run as root (use sudo)${NC}"
        exit 1
    fi
}

function install_service() {
    echo -e "${CYAN}🚀 Installing Codex Dashboard systemd service...${NC}"
    
    # Create service user if not exists
    if ! id "$USER" &>/dev/null; then
        echo -e "${YELLOW}👤 Creating service user: $USER${NC}"
        useradd --system --create-home --home-dir "$WORKING_DIR" --shell /bin/false "$USER"
    fi
    
    # Create working directory
    mkdir -p "$WORKING_DIR"
    chown "$USER:$GROUP" "$WORKING_DIR"
    
    # Copy service files (you'll need to customize paths)
    # cp /path/to/your/codex/files/* "$WORKING_DIR/"
    # chown -R "$USER:$GROUP" "$WORKING_DIR"
    
    # Create the service file
    cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Codex Dashboard - Digital Sovereignty Control Interface
After=network.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=$WORKING_DIR
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port=8095 --server.address=0.0.0.0 --server.headless=true
Restart=always
RestartSec=10
User=$USER
Group=$GROUP

# Security settings
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$WORKING_DIR

# Environment
Environment=PYTHONPATH=$WORKING_DIR
Environment=STREAMLIT_SERVER_HEADLESS=true

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=$SERVICE_NAME

[Install]
WantedBy=multi-user.target
EOF

    echo -e "${GREEN}✅ Service file created at: $SERVICE_FILE${NC}"
}

function daemon_reload() {
    echo -e "${CYAN}🔄 Reloading systemd daemon...${NC}"
    systemctl daemon-reload
    echo -e "${GREEN}✅ Daemon reloaded${NC}"
}

function enable_service() {
    echo -e "${CYAN}⚡ Enabling $SERVICE_NAME service...${NC}"
    systemctl enable "$SERVICE_NAME"
    if systemctl is-enabled "$SERVICE_NAME" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Service enabled (will start on boot)${NC}"
    else
        echo -e "${RED}❌ Failed to enable service${NC}"
        return 1
    fi
}

function start_service() {
    echo -e "${CYAN}🚀 Starting $SERVICE_NAME service...${NC}"
    systemctl start "$SERVICE_NAME"
    sleep 2
    if systemctl is-active "$SERVICE_NAME" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Service started successfully${NC}"
        show_status
    else
        echo -e "${RED}❌ Failed to start service${NC}"
        show_logs
        return 1
    fi
}

function stop_service() {
    echo -e "${YELLOW}🛑 Stopping $SERVICE_NAME service...${NC}"
    systemctl stop "$SERVICE_NAME"
    if ! systemctl is-active "$SERVICE_NAME" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Service stopped${NC}"
    else
        echo -e "${RED}❌ Failed to stop service${NC}"
        return 1
    fi
}

function restart_service() {
    echo -e "${CYAN}🔄 Restarting $SERVICE_NAME service...${NC}"
    systemctl restart "$SERVICE_NAME"
    sleep 2
    if systemctl is-active "$SERVICE_NAME" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Service restarted successfully${NC}"
        show_status
    else
        echo -e "${RED}❌ Failed to restart service${NC}"
        show_logs
        return 1
    fi
}

function show_status() {
    echo -e "${CYAN}📊 Service Status:${NC}"
    systemctl status "$SERVICE_NAME" --no-pager -l
    
    echo ""
    echo -e "${CYAN}🌐 Service Endpoints:${NC}"
    if systemctl is-active "$SERVICE_NAME" >/dev/null 2>&1; then
        echo -e "   Dashboard: ${GREEN}http://localhost:8095${NC}"
        echo -e "   Status: ${GREEN}RUNNING${NC}"
        
        # Test if service is responding
        if curl -s http://localhost:8095 >/dev/null 2>&1; then
            echo -e "   Health: ${GREEN}RESPONDING${NC}"
        else
            echo -e "   Health: ${YELLOW}STARTING...${NC}"
        fi
    else
        echo -e "   Status: ${RED}STOPPED${NC}"
    fi
}

function show_logs() {
    echo -e "${CYAN}📋 Recent Service Logs:${NC}"
    journalctl -u "$SERVICE_NAME" --no-pager -l -n 20
}

function uninstall_service() {
    echo -e "${RED}🗑️  Uninstalling $SERVICE_NAME service...${NC}"
    
    # Stop and disable
    systemctl stop "$SERVICE_NAME" 2>/dev/null
    systemctl disable "$SERVICE_NAME" 2>/dev/null
    
    # Remove service file
    rm -f "$SERVICE_FILE"
    systemctl daemon-reload
    
    echo -e "${GREEN}✅ Service uninstalled${NC}"
}

# Main execution based on command line arguments
case "${1:-status}" in
    "install")
        check_root
        install_service
        daemon_reload
        ;;
    "daemon-reload")
        check_root
        daemon_reload
        ;;
    "enable")
        check_root
        enable_service
        ;;
    "start")
        check_root
        start_service
        ;;
    "stop")
        check_root
        stop_service
        ;;
    "restart")
        check_root
        restart_service
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs
        ;;
    "uninstall")
        check_root
        uninstall_service
        ;;
    "full-install")
        check_root
        install_service
        daemon_reload
        enable_service
        start_service
        ;;
    *)
        echo "Usage: $0 {install|daemon-reload|enable|start|stop|restart|status|logs|uninstall|full-install}"
        echo ""
        echo "Commands:"
        echo "  install      - Create systemd service file"
        echo "  daemon-reload - Reload systemd daemon"
        echo "  enable       - Enable service to start on boot"
        echo "  start        - Start the service"
        echo "  stop         - Stop the service"
        echo "  restart      - Restart the service"
        echo "  status       - Show service status"
        echo "  logs         - Show recent service logs"
        echo "  uninstall    - Remove the service"
        echo "  full-install - Complete installation (install + enable + start)"
        exit 1
        ;;
esac

echo ""
echo -e "${YELLOW}🔥 Codex Dashboard systemd management complete!${NC}"