# 🚀 IONOS SERVER DEPLOYMENT INSTRUCTIONS

## 🔐 SSH Authentication Issue Detected

The SCP upload failed due to authentication. Here are your options:

### Option 1: SSH Key Setup (Recommended)
```powershell
# Generate new SSH key
ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\aistorelab_key"

# Display public key to add to server
Get-Content "$env:USERPROFILE\.ssh\aistorelab_key.pub"
```

### Option 2: Alternative Upload Methods

#### A. Use SFTP with Password
```powershell
# Open SFTP session
sftp user@aistorelab.com
# Commands in SFTP:
put codex-dashboard.service /tmp/
put codex-service-manager.sh /tmp/
quit
```

#### B. Use SCP with Specific Key
```powershell
scp -i "$env:USERPROFILE\.ssh\your_key" codex-dashboard.service codex-service-manager.sh user@aistorelab.com:/tmp/
```

#### C. Manual Content Copy
```bash
# SSH first, then create files manually
ssh user@aistorelab.com

# Create service file
sudo nano /etc/systemd/system/codex-dashboard.service
# Copy content from our codex-dashboard.service file

# Create installation script  
nano /tmp/codex-service-manager.sh
# Copy content from our codex-service-manager.sh file
```

### Option 3: Direct Manual Installation

If file upload continues to fail, connect via SSH and run these commands directly:

```bash
# Connect to server
ssh user@aistorelab.com

# Create systemd service file directly
sudo tee /etc/systemd/system/codex-dashboard.service > /dev/null << 'EOF'
[Unit]
Description=Codex Dashboard - Digital Sovereignty Platform
After=network.target network-online.target
Wants=network-online.target
Requires=network.target

[Service]
Type=simple
User=codex
Group=codex
WorkingDirectory=/opt/codex-dominion
Environment=PATH=/opt/codex-dominion/.venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=PYTHONPATH=/opt/codex-dominion
Environment=PYTHONUNBUFFERED=1
Environment=PORT=8095
ExecStart=/opt/codex-dominion/.venv/bin/python /opt/codex-dominion/sovereignty_dashboard.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create user and directories
sudo useradd --system --home-dir /opt/codex-dominion --shell /bin/bash codex
sudo mkdir -p /opt/codex-dominion
sudo chown -R codex:codex /opt/codex-dominion

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable codex-dashboard.service

# Test your commands
systemctl status codex-dashboard.service
systemctl is-enabled codex-dashboard.service
```

## 🎯 Immediate Next Steps

1. **Choose an upload method** from the options above
2. **Connect to your IONOS server**: `ssh user@aistorelab.com`
3. **Run the installation commands**
4. **Verify with your requested commands**:
   - `systemctl status codex-dashboard.service`
   - `systemctl is-enabled codex-dashboard.service`

The service files are ready - just need to get them to the server! 🚀