# 🚀 CODEX DASHBOARD SERVICE DEPLOYMENT GUIDE

## Overview
This guide provides the exact systemctl commands you requested and their Windows equivalents for comprehensive service management.

## 🐧 Linux Commands (IONOS Server)

### Your Exact Requested Commands:
```bash
# Check service status
systemctl status codex-dashboard.service

# Check if service is enabled for boot
systemctl is-enabled codex-dashboard.service
```

### Complete Service Management:
```bash
# Service Control
sudo systemctl start codex-dashboard.service      # Start service
sudo systemctl stop codex-dashboard.service       # Stop service  
sudo systemctl restart codex-dashboard.service    # Restart service
sudo systemctl reload codex-dashboard.service     # Reload configuration

# Boot Configuration
sudo systemctl enable codex-dashboard.service     # Enable auto-start at boot
sudo systemctl disable codex-dashboard.service    # Disable auto-start

# Monitoring and Logs
journalctl -u codex-dashboard.service -f          # Follow logs in real-time
journalctl -u codex-dashboard.service -n 50       # Show last 50 log entries
journalctl -u codex-dashboard.service --since "1 hour ago"  # Recent logs

# Custom Status Command
codex-status                                       # Enhanced status display
```

## 🪟 Windows Equivalents (Local Testing)

### PowerShell Service Management:
```powershell
# Your Linux commands translated to Windows:
.\codex-service.ps1 -Action status     # systemctl status codex-dashboard.service
.\codex-service.ps1 -Action enabled    # systemctl is-enabled codex-dashboard.service

# Additional Windows commands:
.\codex-service.ps1 -Action start      # sudo systemctl start codex-dashboard.service
.\codex-service.ps1 -Action stop       # sudo systemctl stop codex-dashboard.service
.\codex-service.ps1 -Action restart    # sudo systemctl restart codex-dashboard.service
.\codex-service.ps1 -Action install    # Install Windows service
.\codex-service.ps1 -Action uninstall  # Remove Windows service
```

### Native Windows Commands:
```cmd
# Direct Windows service management:
sc query CodexDashboard               # Check service status
sc start CodexDashboard               # Start service
sc stop CodexDashboard                # Stop service
net start CodexDashboard              # Alternative start command
net stop CodexDashboard               # Alternative stop command
```

## 📋 Deployment Steps

### 1. IONOS Server Setup
```bash
# Upload files to server
scp codex-dashboard.service user@aistorelab.com:/tmp/
scp codex-service-manager.sh user@aistorelab.com:/tmp/

# Connect to server
ssh user@aistorelab.com

# Run service installation
sudo cp /tmp/codex-dashboard.service /etc/systemd/system/
sudo chmod +x /tmp/codex-service-manager.sh
sudo /tmp/codex-service-manager.sh

# Verify installation
systemctl status codex-dashboard.service
systemctl is-enabled codex-dashboard.service
```

### 2. Windows Development Setup
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install Windows service
.\codex-service.ps1 -Action install

# Test your equivalent commands
.\codex-service.ps1 -Action status
.\codex-service.ps1 -Action enabled
```

## 🔍 Expected Outputs

### systemctl status codex-dashboard.service
```
● codex-dashboard.service - Codex Dashboard - Digital Sovereignty Platform
   Loaded: loaded (/etc/systemd/system/codex-dashboard.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2024-01-15 10:30:25 UTC; 2h 15min ago
     Docs: https://github.com/codex-dominion/dashboard
 Main PID: 12345 (python)
    Tasks: 4 (limit: 4915)
   Memory: 125.5M
      CPU: 45.123s
   CGroup: /system.slice/codex-dashboard.service
           └─12345 /opt/codex-dominion/.venv/bin/python /opt/codex-dominion/sovereignty_dashboard.py

Jan 15 10:30:25 aistorelab systemd[1]: Started Codex Dashboard - Digital Sovereignty Platform.
Jan 15 10:30:26 aistorelab codex-dashboard[12345]: 🚀 Codex Dashboard starting...
Jan 15 10:30:27 aistorelab codex-dashboard[12345]: ✅ Dashboard running on port 8095
```

### systemctl is-enabled codex-dashboard.service
```
enabled
```

### Windows PowerShell Output
```
🚀 CODEX DASHBOARD SERVICE MANAGEMENT
====================================

📊 Checking Windows Service Status...
✅ Service found: Codex Dashboard - Digital Sovereignty Platform
   Status: Running
   Start Type: Automatic
✅ Service is enabled (Auto start)

🌐 Testing Dashboard Connectivity...
✅ Dashboard responding on port 8095

💻 Process Information...
   🔥 PID: 5432
   📈 Memory: 128.45 MB
   ⏱️ CPU Time: 00:02:15.123
```

## 🛠️ Troubleshooting

### Common Issues and Solutions:

1. **Service Not Found**
   ```bash
   # Linux: Install service
   sudo ./codex-service-manager.sh
   
   # Windows: Install service
   .\codex-service.ps1 -Action install
   ```

2. **Permission Denied**
   ```bash
   # Linux: Check user permissions
   sudo chown -R codex:codex /opt/codex-dominion
   
   # Windows: Run as Administrator
   ```

3. **Port Already in Use**
   ```bash
   # Check what's using port 8095
   sudo lsof -i :8095
   sudo netstat -tulpn | grep :8095
   ```

4. **Service Failed to Start**
   ```bash
   # Check logs
   journalctl -u codex-dashboard.service -n 50
   
   # Check Python environment
   sudo -u codex /opt/codex-dominion/.venv/bin/python --version
   ```

## 🌍 Access URLs

After successful deployment:

- **Local Development**: http://localhost:8095
- **Production**: https://aistorelab.com (via nginx proxy)
- **Direct Production**: http://aistorelab.com:8095

## 📊 Health Monitoring

### Automated Checks:
```bash
# Create monitoring script
cat > /usr/local/bin/codex-health-check.sh << 'EOF'
#!/bin/bash
if curl -f -s http://localhost:8095/health > /dev/null 2>&1; then
    echo "✅ Codex Dashboard: Healthy"
else
    echo "❌ Codex Dashboard: Unhealthy"
    systemctl restart codex-dashboard.service
fi
EOF

chmod +x /usr/local/bin/codex-health-check.sh

# Add to cron for regular checks
echo "*/5 * * * * /usr/local/bin/codex-health-check.sh" | crontab -
```

## 🔐 Security Configuration

The systemd service includes comprehensive security hardening:
- Namespace isolation
- System call filtering  
- Resource limits
- Privilege restrictions
- Read-only system protection

## ✨ Summary

Your requested commands are now ready:

**Linux (IONOS Server):**
- `systemctl status codex-dashboard.service`
- `systemctl is-enabled codex-dashboard.service`

**Windows (Development):**
- `.\codex-service.ps1 -Action status`
- `.\codex-service.ps1 -Action enabled`

The service is configured for production deployment with comprehensive monitoring, security, and automatic restart capabilities.