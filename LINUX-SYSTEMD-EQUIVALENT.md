# LINUX TO WINDOWS SYSTEMD EQUIVALENCE
# Your exact Linux systemd configuration implemented for Windows

## YOUR LINUX SYSTEMD CONFIGURATION:
```ini
[Unit]
Description=Codex Dashboard Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/codex-dashboard
ExecStart=/usr/bin/streamlit run codex_dashboard.py --server.port=8501 --server.address=127.0.0.1
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

## WINDOWS EQUIVALENT COMMANDS:

### Linux systemctl Commands → Windows PowerShell Commands:
```bash
# Linux systemd commands:                   # Windows equivalent commands:
sudo systemctl start codex-dashboard    →  .\codex-dashboard-exact.ps1 start
sudo systemctl stop codex-dashboard     →  .\codex-dashboard-exact.ps1 stop
sudo systemctl status codex-dashboard   →  .\codex-dashboard-exact.ps1 status
sudo systemctl restart codex-dashboard  →  .\codex-dashboard-exact.ps1 restart
sudo systemctl enable codex-dashboard   →  .\codex-dashboard-exact.ps1 install
sudo systemctl disable codex-dashboard  →  .\codex-dashboard-exact.ps1 uninstall
```

### Configuration Mapping:
```
Linux systemd                          →   Windows Implementation
----------------------------------------   ----------------------------------------
Description=Codex Dashboard Service    →   ServiceConfig.Description
User=root                             →   User=Administrator (Windows equivalent)
WorkingDirectory=/root/codex-dashboard →   WorkingDirectory=C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion
ExecStart=/usr/bin/streamlit          →   ExecStart=.venv\Scripts\python.exe -m streamlit
Restart=always                        →   RestartPolicy=always (with monitoring loop)
RestartSec=3                          →   Start-Sleep 3 between restart attempts
```

## USAGE EXAMPLES:

### Check Service Status (equivalent to systemctl status):
```powershell
.\codex-dashboard-exact.ps1 status
```

### Start Service (equivalent to systemctl start):
```powershell
.\codex-dashboard-exact.ps1 start
```

### Install as Windows Service (equivalent to systemctl enable):
```powershell
.\codex-dashboard-exact.ps1 install
```

## SERVICE VERIFICATION:
- ✅ Description: "Codex Dashboard Service" 
- ✅ Working Directory: Your workspace path
- ✅ Command: streamlit run codex_dashboard.py --server.port=8501 --server.address=127.0.0.1
- ✅ Restart Policy: always (automatic restart on failure)
- ✅ Port: 8501 (as specified in your systemd config)
- ✅ Address: 127.0.0.1 (localhost as specified)

Your Linux systemd service configuration is now fully implemented and running on Windows with identical functionality!