#!/bin/bash
# 🔥 COSMIC DOMINION - SYSTEMD SERVICE INSTALLER 🔥
# Install and manage all cosmic dashboard services

echo "🔥 COSMIC DOMINION SYSTEMD SERVICE INSTALLER 🔥"
echo "================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
USER_NAME="codex"
GROUP_NAME="codex"
PROJECT_DIR="/srv/codex-dominion"
SYSTEMD_DIR="/etc/systemd/system"

# Service configurations
declare -A SERVICES=(
    ["cosmic-dashboard"]="8501"
    ["cosmic-ledger"]="8502"
    ["cosmic-rhythm"]="8503"
)

echo -e "${BLUE}🌟 Starting Cosmic Dominion systemd setup...${NC}"

# 1. Create system user and group
setup_user() {
    echo -e "${YELLOW}👤 Setting up system user and group...${NC}"

    if ! id "$USER_NAME" &>/dev/null; then
        sudo useradd --system --shell /bin/bash --home-dir $PROJECT_DIR --create-home $USER_NAME
        echo -e "${GREEN}✅ Created user: $USER_NAME${NC}"
    else
        echo -e "${GREEN}✅ User already exists: $USER_NAME${NC}"
    fi

    if ! getent group "$GROUP_NAME" &>/dev/null; then
        sudo groupadd $GROUP_NAME
        echo -e "${GREEN}✅ Created group: $GROUP_NAME${NC}"
    else
        echo -e "${GREEN}✅ Group already exists: $GROUP_NAME${NC}"
    fi

    # Add user to group
    sudo usermod -a -G $GROUP_NAME $USER_NAME
}

# 2. Set up project directory
setup_project_directory() {
    echo -e "${YELLOW}📁 Setting up project directory...${NC}"

    # Create directory structure
    sudo mkdir -p $PROJECT_DIR/{logs,data,venv}

    # Set ownership
    sudo chown -R $USER_NAME:$GROUP_NAME $PROJECT_DIR

    # Set permissions
    sudo chmod 755 $PROJECT_DIR
    sudo chmod 775 $PROJECT_DIR/{logs,data}

    echo -e "${GREEN}✅ Project directory configured${NC}"
}

# 3. Install systemd service files
install_services() {
    echo -e "${YELLOW}⚙️ Installing systemd service files...${NC}"

    for service in "${!SERVICES[@]}"; do
        service_file="systemd/${service}.service"
        target_file="$SYSTEMD_DIR/${service}.service"

        if [ -f "$service_file" ]; then
            echo -e "${BLUE}📋 Installing ${service}.service...${NC}"
            sudo cp "$service_file" "$target_file"
            sudo chown root:root "$target_file"
            sudo chmod 644 "$target_file"
            echo -e "${GREEN}✅ Installed: ${service}.service${NC}"
        else
            echo -e "${RED}❌ Service file not found: $service_file${NC}"
        fi
    done
}

# 4. Reload systemd and enable services
enable_services() {
    echo -e "${YELLOW}🔄 Enabling cosmic services...${NC}"

    # Reload systemd daemon
    sudo systemctl daemon-reload

    for service in "${!SERVICES[@]}"; do
        echo -e "${BLUE}🚀 Enabling ${service}...${NC}"

        # Enable service
        if sudo systemctl enable "${service}.service"; then
            echo -e "${GREEN}✅ Enabled: ${service}.service${NC}"
        else
            echo -e "${RED}❌ Failed to enable: ${service}.service${NC}"
        fi
    done
}

# 5. Start services
start_services() {
    echo -e "${YELLOW}▶️ Starting cosmic services...${NC}"

    for service in "${!SERVICES[@]}"; do
        port="${SERVICES[$service]}"
        echo -e "${BLUE}🚀 Starting ${service} on port ${port}...${NC}"

        if sudo systemctl start "${service}.service"; then
            echo -e "${GREEN}✅ Started: ${service}.service${NC}"

            # Check if service is active
            if systemctl is-active --quiet "${service}.service"; then
                echo -e "${GREEN}   ✅ Service is running${NC}"
            else
                echo -e "${RED}   ❌ Service failed to start${NC}"
            fi
        else
            echo -e "${RED}❌ Failed to start: ${service}.service${NC}"
        fi

        sleep 2
    done
}

# 6. Check service status
check_status() {
    echo -e "${YELLOW}📊 Checking service status...${NC}"

    echo -e "${BLUE}🌟 COSMIC DOMINION SERVICE STATUS:${NC}"
    echo "=================================="

    for service in "${!SERVICES[@]}"; do
        port="${SERVICES[$service]}"
        status=$(systemctl is-active "${service}.service")
        enabled=$(systemctl is-enabled "${service}.service")

        if [ "$status" = "active" ]; then
            status_color="${GREEN}"
            status_icon="✅"
        else
            status_color="${RED}"
            status_icon="❌"
        fi

        echo -e "${status_color}${status_icon} ${service}:${NC}"
        echo -e "   Status: ${status_color}${status}${NC}"
        echo -e "   Enabled: ${enabled}"
        echo -e "   Port: ${port}"
        echo -e "   URL: http://localhost:${port}"
        echo ""
    done
}

# 7. Create management script
create_management_script() {
    echo -e "${YELLOW}🛠️ Creating management script...${NC}"

    cat << 'EOF' | sudo tee /usr/local/bin/cosmic-services > /dev/null
#!/bin/bash
# 🔥 COSMIC DOMINION SERVICE MANAGER 🔥

case "$1" in
    start)
        echo "🚀 Starting all cosmic services..."
        sudo systemctl start cosmic-dashboard.service
        sudo systemctl start cosmic-ledger.service
        sudo systemctl start cosmic-rhythm.service
        ;;
    stop)
        echo "🛑 Stopping all cosmic services..."
        sudo systemctl stop cosmic-dashboard.service
        sudo systemctl stop cosmic-ledger.service
        sudo systemctl stop cosmic-rhythm.service
        ;;
    restart)
        echo "🔄 Restarting all cosmic services..."
        sudo systemctl restart cosmic-dashboard.service
        sudo systemctl restart cosmic-ledger.service
        sudo systemctl restart cosmic-rhythm.service
        ;;
    status)
        echo "📊 COSMIC DOMINION SERVICE STATUS:"
        echo "=================================="
        systemctl status cosmic-dashboard.service --no-pager -l
        echo ""
        systemctl status cosmic-ledger.service --no-pager -l
        echo ""
        systemctl status cosmic-rhythm.service --no-pager -l
        ;;
    logs)
        service="${2:-cosmic-dashboard}"
        echo "📋 Logs for ${service}.service:"
        sudo journalctl -u "${service}.service" -f --no-pager
        ;;
    urls)
        echo "🌍 COSMIC DASHBOARD URLS:"
        echo "========================"
        echo "🔥 Main Dashboard: http://localhost:8501"
        echo "📊 Sacred Ledger:  http://localhost:8502"
        echo "🎵 Cosmic Rhythm:  http://localhost:8503"
        ;;
    *)
        echo "🔥 COSMIC DOMINION SERVICE MANAGER 🔥"
        echo "Usage: $0 {start|stop|restart|status|logs|urls}"
        echo ""
        echo "Commands:"
        echo "  start    - Start all cosmic services"
        echo "  stop     - Stop all cosmic services"
        echo "  restart  - Restart all cosmic services"
        echo "  status   - Show service status"
        echo "  logs     - Show logs (specify service name)"
        echo "  urls     - Show service URLs"
        ;;
esac
EOF

    sudo chmod +x /usr/local/bin/cosmic-services
    echo -e "${GREEN}✅ Management script created: cosmic-services${NC}"
}

# 8. Create log rotation configuration
setup_log_rotation() {
    echo -e "${YELLOW}📝 Setting up log rotation...${NC}"

    cat << EOF | sudo tee /etc/logrotate.d/cosmic-dominion > /dev/null
$PROJECT_DIR/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    copytruncate
    notifempty
    su $USER_NAME $GROUP_NAME
}
EOF

    echo -e "${GREEN}✅ Log rotation configured${NC}"
}

# Main installation function
main() {
    echo -e "${PURPLE}🔥 COSMIC DOMINION SYSTEMD INSTALLATION 🔥${NC}"

    # Check if running as root or with sudo
    if [[ $EUID -ne 0 ]]; then
        echo -e "${RED}❌ This script must be run as root or with sudo${NC}"
        exit 1
    fi

    # Run installation steps
    setup_user
    setup_project_directory
    install_services
    enable_services
    start_services
    create_management_script
    setup_log_rotation

    echo ""
    echo -e "${GREEN}✨ COSMIC DOMINION SYSTEMD INSTALLATION COMPLETE! ✨${NC}"
    echo ""

    # Final status check
    check_status

    echo -e "${YELLOW}⚙️ Management Commands:${NC}"
    echo -e "   Start all services: ${GREEN}cosmic-services start${NC}"
    echo -e "   Stop all services: ${GREEN}cosmic-services stop${NC}"
    echo -e "   Check status: ${GREEN}cosmic-services status${NC}"
    echo -e "   View logs: ${GREEN}cosmic-services logs [service-name]${NC}"
    echo -e "   Show URLs: ${GREEN}cosmic-services urls${NC}"

    echo ""
    echo -e "${RED}🔥 THE DIGITAL SOVEREIGNTY IS SYSTEMIZED! 🔥${NC}"
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi