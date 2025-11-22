# IONOS Codex Dashboard Deployment Checklist
# Complete guide for deploying to IONOS Linux servers

## 🔥 PRE-DEPLOYMENT CHECKLIST

### 1. Local Files to Upload
```
✅ Required Files for IONOS Upload:
   📄 app.py                          # Main Streamlit dashboard
   📄 codex_ledger.json               # Sacred ledger database  
   📄 omega_seal.py                   # Omega seal system
   📄 ionos_codex_deploy.sh           # Deployment script
   📄 ionos_codex_dashboard.service   # Systemd service file
   📄 ionos_nginx_codex.conf          # Nginx configuration
   📄 ionos_systemctl_commands.sh     # Your systemctl commands
```

### 2. IONOS Server Requirements
```
✅ IONOS Server Specifications:
   🖥️  OS: Ubuntu 20.04+ / Debian 11+
   🧠 RAM: Minimum 2GB (Recommended 4GB+)
   💾 Storage: Minimum 20GB
   🌐 Network: Public IP with domain pointing
   🔐 Access: SSH key or password access
```

## 🚀 DEPLOYMENT STEPS

### Step 1: Upload Files to IONOS
```bash
# From your Windows machine, upload files to IONOS:
scp app.py codex_ledger.json omega_seal.py user@your-ionos-server.com:/tmp/
scp ionos_*.sh ionos_*.service ionos_*.conf user@your-ionos-server.com:/tmp/
```

### Step 2: Run Initial Deployment
```bash
# SSH into your IONOS server
ssh user@your-ionos-server.com

# Make deployment script executable
chmod +x /tmp/ionos_codex_deploy.sh

# Run deployment (this sets up everything)
/tmp/ionos_codex_deploy.sh
```

### Step 3: Copy Application Files
```bash
# Copy your application files to the correct location
sudo cp /tmp/app.py /opt/codex-dominion/app/
sudo cp /tmp/codex_ledger.json /opt/codex-dominion/app/
sudo cp /tmp/omega_seal.py /opt/codex-dominion/app/

# Set proper ownership
sudo chown codex:codex /opt/codex-dominion/app/*
```

### Step 4: Install Systemd Service
```bash
# Copy service file
sudo cp /tmp/ionos_codex_dashboard.service /etc/systemd/system/codex-dashboard.service
```

### Step 5: Configure Nginx
```bash
# Copy nginx configuration
sudo cp /tmp/ionos_nginx_codex.conf /etc/nginx/sites-available/codex-dashboard
sudo ln -sf /etc/nginx/sites-available/codex-dashboard /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### Step 6: Run Your Systemctl Commands
```bash
# Make the systemctl command script executable
chmod +x /tmp/ionos_systemctl_commands.sh

# Execute your exact systemctl commands
sudo /tmp/ionos_systemctl_commands.sh
```

### Step 7: Test and Reload Nginx
```bash
# Your nginx commands
sudo nginx -t && sudo systemctl reload nginx

# Or use the nginx manager
chmod +x /tmp/ionos_nginx_manager.sh
sudo /tmp/ionos_nginx_manager.sh test-and-reload
```

## 🎯 YOUR EXACT SYSTEMCTL COMMANDS

After deployment, these are your commands that will work on IONOS Linux:

```bash
# 1. Reload systemd daemon
sudo systemctl daemon-reload

# 2. Enable service for boot startup  
sudo systemctl enable codex-dashboard

# 3. Start the service
sudo systemctl start codex-dashboard

# 4. Check service status
sudo systemctl status codex-dashboard

# 5. Test and reload nginx configuration
sudo nginx -t && sudo systemctl reload nginx
```

## 🔧 MANAGEMENT COMMANDS

### Service Management
```bash
# Stop service
sudo systemctl stop codex-dashboard

# Restart service  
sudo systemctl restart codex-dashboard

# View logs
sudo journalctl -u codex-dashboard -f

# Check if service is running
sudo systemctl is-active codex-dashboard
```

### Application Updates
```bash
# Upload new files
scp app.py codex_ledger.json user@server:/opt/codex-dominion/app/

# Restart service
sudo systemctl restart codex-dashboard
```

## 🌐 DNS & SSL SETUP

### 1. Point Domain to IONOS Server
```
Domain: codex.aistorelab.com
A Record: [YOUR-IONOS-SERVER-IP]
```

### 2. Setup SSL Certificate
```bash
# After DNS is configured
sudo certbot --nginx -d codex.aistorelab.com
```

## 📊 MONITORING & HEALTH CHECKS

### Check Service Health
```bash
# Service status
sudo systemctl status codex-dashboard

# Application health
curl -f http://localhost:8095/_stcore/health

# Port status  
netstat -tlnp | grep :8095

# Recent logs
sudo journalctl -u codex-dashboard --no-pager -n 20
```

## 🎉 FINAL VERIFICATION

After deployment, your Codex Dashboard will be available at:
- 🌐 Public: https://codex.aistorelab.com
- 🔒 Internal: http://localhost:8095

### Success Indicators:
✅ `sudo systemctl status codex-dashboard` shows "active (running)"
✅ `curl http://localhost:8095` returns HTTP 200
✅ Port 8095 is listening (`netstat -tlnp | grep :8095`)
✅ Domain resolves and loads the dashboard
✅ SSL certificate is valid (if configured)

## 🆘 TROUBLESHOOTING

### Common Issues:
1. **Service won't start**: Check logs with `sudo journalctl -u codex-dashboard`
2. **Port not accessible**: Check firewall with `sudo ufw status`  
3. **Domain not loading**: Verify DNS settings and nginx config
4. **Permission errors**: Ensure files are owned by `codex` user

### Emergency Commands:
```bash
# Reset and restart everything
sudo systemctl stop codex-dashboard
sudo systemctl daemon-reload  
sudo systemctl start codex-dashboard
sudo systemctl status codex-dashboard
```

🔥 Your Codex Dominion will rule the IONOS realm! 🔥