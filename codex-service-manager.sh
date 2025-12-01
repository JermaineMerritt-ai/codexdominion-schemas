#!/bin/bash
# 🚀 CODEX DASHBOARD SERVICE MANAGEMENT SCRIPT
# Create, configure, and manage codex-dashboard.service on IONOS server

set -e

echo "🚀 CODEX DASHBOARD SERVICE MANAGEMENT"
echo "===================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
SERVICE_NAME="codex-dashboard"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
USER="codex"
GROUP="codex"
WORKING_DIR="/opt/codex-dominion"
PYTHON_PATH="$WORKING_DIR/.venv/bin/python"
APP_SCRIPT="$WORKING_DIR/sovereignty_dashboard.py"
PORT=8095

echo -e "${BLUE}🌟 Configuring Codex Dashboard systemd service...${NC}"

# Function to check if running as root or with sudo
check_sudo() {
    if [[ $EUID -eq 0 ]]; then
        echo -e "${GREEN}✅ Running with root privileges${NC}"
    elif sudo -n true 2>/dev/null; then
        echo -e "${GREEN}✅ Sudo access available${NC}"
    else
        echo -e "${RED}❌ This script requires sudo privileges${NC}"
        exit 1
    fi
}

# Function to create system user for service
create_service_user() {
    echo -e "${YELLOW}👤 Setting up service user...${NC}"

    if id "$USER" &>/dev/null; then
        echo -e "${GREEN}✅ User '$USER' already exists${NC}"
    else
        echo -e "${YELLOW}📝 Creating system user '$USER'...${NC}"
        sudo useradd --system --home-dir $WORKING_DIR --shell /bin/bash --comment "Codex Dashboard Service" $USER
        echo -e "${GREEN}✅ User '$USER' created${NC}"
    fi

    # Ensure user owns the application directory
    sudo mkdir -p $WORKING_DIR
    sudo chown -R $USER:$GROUP $WORKING_DIR
}

# Function to create systemd service file
create_service_file() {
    echo -e "${YELLOW}📄 Creating systemd service file...${NC}"

    sudo tee $SERVICE_FILE > /dev/null << EOF
[Unit]
Description=Codex Dashboard - Digital Sovereignty Platform
Documentation=https://github.com/codex-dominion/dashboard
After=network.target network-online.target
Wants=network-online.target
Requires=network.target

[Service]
Type=simple
User=$USER
Group=$GROUP
WorkingDirectory=$WORKING_DIR
Environment=PATH=$WORKING_DIR/.venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=PYTHONPATH=$WORKING_DIR
Environment=PYTHONUNBUFFERED=1
Environment=CODEX_ENV=production
Environment=PORT=$PORT
ExecStart=$PYTHON_PATH $APP_SCRIPT
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
KillSignal=SIGINT
TimeoutStartSec=30
TimeoutStopSec=30
Restart=always
RestartSec=10
StartLimitIntervalSec=60
StartLimitBurst=3

# Security settings
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=$WORKING_DIR
PrivateTmp=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes

# Resource limits
LimitNOFILE=65536
LimitNPROC=4096

[Install]
WantedBy=multi-user.target
EOF

    echo -e "${GREEN}✅ Service file created at $SERVICE_FILE${NC}"
}

# Function to reload systemd and configure service
configure_service() {
    echo -e "${YELLOW}⚙️ Configuring systemd service...${NC}"

    # Reload systemd daemon
    sudo systemctl daemon-reload
    echo -e "${GREEN}✅ Systemd daemon reloaded${NC}"

    # Enable service to start at boot
    sudo systemctl enable $SERVICE_NAME.service
    echo -e "${GREEN}✅ Service enabled for startup at boot${NC}"
}

# Function to check service status
check_service_status() {
    echo -e "${YELLOW}📊 Checking service status...${NC}"

    # Check if service is enabled
    if sudo systemctl is-enabled $SERVICE_NAME.service >/dev/null 2>&1; then
        enabled_status=$(sudo systemctl is-enabled $SERVICE_NAME.service)
        echo -e "${GREEN}✅ Service enabled status: $enabled_status${NC}"
    else
        echo -e "${RED}❌ Service is not enabled${NC}"
    fi

    # Check if service is active
    if sudo systemctl is-active $SERVICE_NAME.service >/dev/null 2>&1; then
        active_status=$(sudo systemctl is-active $SERVICE_NAME.service)
        echo -e "${GREEN}✅ Service active status: $active_status${NC}"
    else
        echo -e "${YELLOW}⚠️ Service is not currently active${NC}"
    fi

    # Show detailed status
    echo -e "${CYAN}📋 Detailed service status:${NC}"
    sudo systemctl status $SERVICE_NAME.service --no-pager || true
}

# Function to start service
start_service() {
    echo -e "${YELLOW}🚀 Starting Codex Dashboard service...${NC}"

    if sudo systemctl start $SERVICE_NAME.service; then
        echo -e "${GREEN}✅ Service started successfully${NC}"

        # Wait a moment for service to initialize
        sleep 5

        # Check if it's running
        if sudo systemctl is-active $SERVICE_NAME.service >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Service is running${NC}"

            # Test connectivity
            echo -e "${CYAN}🔍 Testing service connectivity...${NC}"
            if curl -s "http://localhost:$PORT" >/dev/null 2>&1; then
                echo -e "${GREEN}✅ Service is responding on port $PORT${NC}"
            else
                echo -e "${YELLOW}⚠️ Service may still be starting up...${NC}"
            fi
        else
            echo -e "${RED}❌ Service failed to start${NC}"
        fi
    else
        echo -e "${RED}❌ Failed to start service${NC}"
        echo -e "${YELLOW}📋 Service logs:${NC}"
        sudo journalctl -u $SERVICE_NAME.service -n 20 --no-pager
    fi
}

# Function to create management commands
create_management_commands() {
    echo -e "${YELLOW}🔧 Creating service management commands...${NC}"

    # Create codex-status command
    sudo tee /usr/local/bin/codex-status > /dev/null << 'EOF'
#!/bin/bash
# 🚀 CODEX DASHBOARD STATUS CHECKER

echo "🚀 CODEX DASHBOARD SERVICE STATUS"
echo "================================="
echo ""

# Check service status
echo "📊 Service Status:"
if systemctl is-enabled codex-dashboard.service >/dev/null 2>&1; then
    enabled_status=$(systemctl is-enabled codex-dashboard.service)
    echo "   ✅ Enabled: $enabled_status"
else
    echo "   ❌ Enabled: disabled"
fi

if systemctl is-active codex-dashboard.service >/dev/null 2>&1; then
    active_status=$(systemctl is-active codex-dashboard.service)
    echo "   ✅ Active: $active_status"
else
    echo "   ❌ Active: inactive"
fi

echo ""

# Check port connectivity
echo "🌐 Connectivity Test:"
if curl -s "http://localhost:8095" >/dev/null 2>&1; then
    echo "   ✅ Dashboard accessible on port 8095"
else
    echo "   ❌ Dashboard not responding on port 8095"
fi

echo ""

# Show recent logs
echo "📋 Recent Service Logs:"
journalctl -u codex-dashboard.service -n 5 --no-pager --since "5 minutes ago" 2>/dev/null || echo "   No recent logs available"

echo ""

# Resource usage
echo "💻 Resource Usage:"
if systemctl is-active codex-dashboard.service >/dev/null 2>&1; then
    pid=$(systemctl show --property MainPID --value codex-dashboard.service)
    if [ "$pid" != "0" ] && [ -n "$pid" ]; then
        mem=$(ps --no-headers -o rss -p $pid 2>/dev/null || echo "0")
        cpu=$(ps --no-headers -o %cpu -p $pid 2>/dev/null || echo "0")
        echo "   📈 Memory: ${mem}KB"
        echo "   🔥 CPU: ${cpu}%"
    else
        echo "   ⚠️ Process information not available"
    fi
else
    echo "   ⚠️ Service not running"
fi

echo ""
echo "🔧 Management Commands:"
echo "   Start: sudo systemctl start codex-dashboard.service"
echo "   Stop: sudo systemctl stop codex-dashboard.service"
echo "   Restart: sudo systemctl restart codex-dashboard.service"
echo "   Status: systemctl status codex-dashboard.service"
echo "   Logs: journalctl -u codex-dashboard.service -f"
echo ""
echo "🚀 CODEX DASHBOARD STATUS COMPLETE!"
EOF

    sudo chmod +x /usr/local/bin/codex-status
    echo -e "${GREEN}✅ codex-status command created${NC}"
}

# Function to test service commands
test_service_commands() {
    echo -e "${YELLOW}🧪 Testing service management commands...${NC}"

    echo -e "${CYAN}1. Testing systemctl status:${NC}"
    if sudo systemctl status $SERVICE_NAME.service --no-pager >/dev/null 2>&1; then
        echo -e "${GREEN}   ✅ systemctl status: WORKING${NC}"
    else
        echo -e "${YELLOW}   ⚠️ systemctl status: Service may not be running${NC}"
    fi

    echo -e "${CYAN}2. Testing systemctl is-enabled:${NC}"
    if sudo systemctl is-enabled $SERVICE_NAME.service >/dev/null 2>&1; then
        echo -e "${GREEN}   ✅ systemctl is-enabled: WORKING${NC}"
    else
        echo -e "${RED}   ❌ systemctl is-enabled: FAILED${NC}"
    fi

    echo -e "${CYAN}3. Testing codex-status command:${NC}"
    if codex-status >/dev/null 2>&1; then
        echo -e "${GREEN}   ✅ codex-status: WORKING${NC}"
    else
        echo -e "${RED}   ❌ codex-status: FAILED${NC}"
    fi
}

# Function to display final status
show_final_status() {
    echo ""
    echo -e "${GREEN}✨ CODEX DASHBOARD SERVICE SETUP COMPLETE! ✨${NC}"
    echo ""

    echo -e "${PURPLE}🚀 Service Management Commands:${NC}"
    echo -e "${CYAN}   # Check service status (your exact commands)${NC}"
    echo -e "${WHITE}   systemctl status codex-dashboard.service${NC}"
    echo -e "${WHITE}   systemctl is-enabled codex-dashboard.service${NC}"
    echo ""
    echo -e "${CYAN}   # Service control commands${NC}"
    echo -e "${WHITE}   sudo systemctl start codex-dashboard.service${NC}"
    echo -e "${WHITE}   sudo systemctl stop codex-dashboard.service${NC}"
    echo -e "${WHITE}   sudo systemctl restart codex-dashboard.service${NC}"
    echo -e "${WHITE}   sudo systemctl enable codex-dashboard.service${NC}"
    echo -e "${WHITE}   sudo systemctl disable codex-dashboard.service${NC}"
    echo ""
    echo -e "${CYAN}   # Monitoring commands${NC}"
    echo -e "${WHITE}   codex-status${NC}"
    echo -e "${WHITE}   journalctl -u codex-dashboard.service -f${NC}"
    echo -e "${WHITE}   journalctl -u codex-dashboard.service -n 50${NC}"
    echo ""

    echo -e "${BLUE}🌍 Dashboard Access:${NC}"
    echo -e "${GREEN}   🚀 http://localhost:8095${NC}"
    echo -e "${GREEN}   🌐 https://aistorelab.com (via nginx proxy)${NC}"
    echo ""

    # Show current status
    echo -e "${YELLOW}📊 Current Status:${NC}"
    codex-status
}

# Main execution flow
main() {
    check_sudo
    create_service_user
    create_service_file
    configure_service
    create_management_commands
    check_service_status
    start_service
    test_service_commands
    show_final_status
}

# Execute main function
main "$@"