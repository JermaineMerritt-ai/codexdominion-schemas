#!/bin/bash
# =============================================================================
# CODEX DOMINION - SERVER SECURITY HARDENING SCRIPT
# =============================================================================
# Purpose: Configure firewall, fail2ban, and security settings
# Generated: 2025-12-03
# Run this on the IONOS server after initial deployment
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🔒 CODEX DOMINION - SECURITY HARDENING"
echo "======================================="
echo ""

# =============================================================================
# Step 1: Configure UFW Firewall
# =============================================================================
echo "🛡️  Step 1: Configuring UFW Firewall..."
echo "----------------------------------------"

# Install UFW if not present
if ! command -v ufw &> /dev/null; then
    sudo apt update
    sudo apt install -y ufw
fi

# Reset UFW to default
sudo ufw --force reset

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (IMPORTANT: Don't lock yourself out!)
sudo ufw allow 22/tcp comment 'SSH'

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp comment 'HTTP'
sudo ufw allow 443/tcp comment 'HTTPS'

# Allow PostgreSQL only from localhost (more secure)
sudo ufw allow from 127.0.0.1 to any port 5432 comment 'PostgreSQL localhost'

# Allow Redis only from localhost
sudo ufw allow from 127.0.0.1 to any port 6379 comment 'Redis localhost'

# Enable UFW
echo "y" | sudo ufw enable

# Show status
sudo ufw status verbose

echo -e "${GREEN}✓ Firewall configured${NC}"
echo ""

# =============================================================================
# Step 2: Install and Configure Fail2Ban
# =============================================================================
echo "🚫 Step 2: Setting up Fail2Ban..."
echo "-----------------------------------"

# Install fail2ban
sudo apt install -y fail2ban

# Create local configuration
sudo tee /etc/fail2ban/jail.local > /dev/null << 'EOF'
[DEFAULT]
# Ban time: 1 hour
bantime = 3600
# Find time window: 10 minutes
findtime = 600
# Max retry attempts
maxretry = 5
# Ignore localhost
ignoreip = 127.0.0.1/8 ::1

# Email notifications (configure SMTP first)
destemail = admin@codexdominion.app
sender = fail2ban@codexdominion.app
action = %(action_mwl)s

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3
bantime = 7200

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 5

[nginx-noscript]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 6

[nginx-badbots]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 2

[nginx-noproxy]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 2

[nginx-limit-req]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 10
EOF

# Restart fail2ban
sudo systemctl restart fail2ban
sudo systemctl enable fail2ban

# Check status
sudo fail2ban-client status

echo -e "${GREEN}✓ Fail2Ban configured${NC}"
echo ""

# =============================================================================
# Step 3: Secure SSH Configuration
# =============================================================================
echo "🔑 Step 3: Hardening SSH Configuration..."
echo "------------------------------------------"

# Backup original SSH config
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# Apply security settings
sudo tee -a /etc/ssh/sshd_config > /dev/null << 'EOF'

# Security Hardening - Added by Codex Dominion
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
ChallengeResponseAuthentication no
UsePAM yes
X11Forwarding no
PrintMotd no
AcceptEnv LANG LC_*
MaxAuthTries 3
MaxSessions 5
ClientAliveInterval 300
ClientAliveCountMax 2
AllowUsers www-data
EOF

# Restart SSH (be careful!)
echo -e "${YELLOW}⚠️  Restarting SSH service...${NC}"
sudo systemctl restart sshd

echo -e "${GREEN}✓ SSH hardened${NC}"
echo ""

# =============================================================================
# Step 4: Set Secure File Permissions
# =============================================================================
echo "📂 Step 4: Setting Secure File Permissions..."
echo "-----------------------------------------------"

# Application directory
sudo chown -R www-data:www-data /var/www/codexdominion.app
sudo find /var/www/codexdominion.app -type d -exec chmod 755 {} \;
sudo find /var/www/codexdominion.app -type f -exec chmod 644 {} \;

# Executable scripts
sudo chmod 755 /var/www/codexdominion.app/deployment/*.sh 2>/dev/null || true

# Sensitive files
sudo chmod 600 /var/www/codexdominion.app/.env.production
sudo chmod 600 /var/www/codexdominion.app/.db_credentials 2>/dev/null || true

# Log directory
sudo chown -R www-data:www-data /var/log/codexdominion
sudo chmod 755 /var/log/codexdominion
sudo chmod 644 /var/log/codexdominion/*.log 2>/dev/null || true

echo -e "${GREEN}✓ File permissions secured${NC}"
echo ""

# =============================================================================
# Step 5: Configure Automatic Security Updates
# =============================================================================
echo "🔄 Step 5: Enabling Automatic Security Updates..."
echo "---------------------------------------------------"

sudo apt install -y unattended-upgrades apt-listchanges

# Configure unattended upgrades
sudo tee /etc/apt/apt.conf.d/50unattended-upgrades > /dev/null << 'EOF'
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
    "${distro_id}ESMApps:${distro_codename}-apps-security";
    "${distro_id}ESM:${distro_codename}-infra-security";
};
Unattended-Upgrade::AutoFixInterruptedDpkg "true";
Unattended-Upgrade::MinimalSteps "true";
Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";
Unattended-Upgrade::Automatic-Reboot-Time "03:00";
EOF

# Enable automatic updates
sudo tee /etc/apt/apt.conf.d/20auto-upgrades > /dev/null << 'EOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";
EOF

echo -e "${GREEN}✓ Automatic updates enabled${NC}"
echo ""

# =============================================================================
# Step 6: Install Additional Security Tools
# =============================================================================
echo "🛠️  Step 6: Installing Security Tools..."
echo "-------------------------------------------"

# Install security packages
sudo apt install -y \
    aide \
    rkhunter \
    lynis \
    logwatch

# Initialize AIDE database (file integrity monitoring)
echo "Initializing AIDE database (this may take a while)..."
sudo aideinit || true

echo -e "${GREEN}✓ Security tools installed${NC}"
echo ""

# =============================================================================
# Step 7: Configure Log Rotation
# =============================================================================
echo "📝 Step 7: Configuring Log Rotation..."
echo "----------------------------------------"

sudo tee /etc/logrotate.d/codexdominion > /dev/null << 'EOF'
/var/log/codexdominion/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 www-data www-data
    sharedscripts
    postrotate
        systemctl reload codexdominion-api > /dev/null 2>&1 || true
    endscript
}
EOF

echo -e "${GREEN}✓ Log rotation configured${NC}"
echo ""

# =============================================================================
# Step 8: Disable Unnecessary Services
# =============================================================================
echo "🔇 Step 8: Disabling Unnecessary Services..."
echo "----------------------------------------------"

# List of services to disable (adjust based on your needs)
SERVICES_TO_DISABLE="bluetooth cups avahi-daemon"

for service in $SERVICES_TO_DISABLE; do
    if systemctl is-enabled "$service" 2>/dev/null; then
        sudo systemctl stop "$service" 2>/dev/null || true
        sudo systemctl disable "$service" 2>/dev/null || true
        echo "  Disabled: $service"
    fi
done

echo -e "${GREEN}✓ Unnecessary services disabled${NC}"
echo ""

# =============================================================================
# Step 9: Configure System Limits
# =============================================================================
echo "⚙️  Step 9: Configuring System Limits..."
echo "-----------------------------------------"

sudo tee -a /etc/security/limits.conf > /dev/null << 'EOF'
# Codex Dominion - Resource Limits
www-data soft nofile 65536
www-data hard nofile 65536
www-data soft nproc 4096
www-data hard nproc 4096
EOF

echo -e "${GREEN}✓ System limits configured${NC}"
echo ""

# =============================================================================
# Step 10: Security Audit
# =============================================================================
echo "🔍 Step 10: Running Security Audit..."
echo "---------------------------------------"

echo "Running Lynis security audit..."
sudo lynis audit system --quick --no-colors > /tmp/lynis-audit.txt 2>&1 || true
echo "  Audit report saved to: /tmp/lynis-audit.txt"

echo -e "${GREEN}✓ Security audit complete${NC}"
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "======================================="
echo -e "${GREEN}🔒 SECURITY HARDENING COMPLETE!${NC}"
echo "======================================="
echo ""
echo "✅ Completed Tasks:"
echo "  [✓] UFW Firewall configured (ports 22, 80, 443)"
echo "  [✓] Fail2Ban installed and configured"
echo "  [✓] SSH hardened (no root login, key-only auth)"
echo "  [✓] File permissions secured"
echo "  [✓] Automatic security updates enabled"
echo "  [✓] Security tools installed (AIDE, rkhunter, lynis)"
echo "  [✓] Log rotation configured"
echo "  [✓] Unnecessary services disabled"
echo "  [✓] System resource limits set"
echo "  [✓] Security audit completed"
echo ""
echo -e "${YELLOW}⚠️  Important Reminders:${NC}"
echo "  1. Save your SSH key securely - password auth is now disabled"
echo "  2. Review Fail2Ban logs: sudo tail -f /var/log/fail2ban.log"
echo "  3. Check firewall status: sudo ufw status"
echo "  4. Review security audit: cat /tmp/lynis-audit.txt"
echo "  5. Test SSH connection before logging out!"
echo ""
echo "🔧 Useful Commands:"
echo "  sudo fail2ban-client status"
echo "  sudo ufw status verbose"
echo "  sudo lynis audit system"
echo "  sudo rkhunter --check"
echo ""
