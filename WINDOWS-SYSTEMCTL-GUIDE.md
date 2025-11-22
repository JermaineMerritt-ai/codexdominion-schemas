# Windows Equivalent of Linux systemctl Commands

## Summary: You're on Windows, so `sudo systemctl` commands don't work.
## Use these Windows equivalents instead:

## =====================================================
## SYSTEMCTL COMMAND TRANSLATION TABLE
## =====================================================

### Original systemctl commands → Windows equivalents:

```bash
# Linux systemctl commands (DON'T WORK ON WINDOWS):
sudo systemctl start codex-dashboard     # ❌ Linux only
sudo systemctl stop codex-dashboard      # ❌ Linux only  
sudo systemctl restart codex-dashboard   # ❌ Linux only
sudo systemctl reload nginx              # ❌ Linux only
sudo systemctl status codex-dashboard    # ❌ Linux only
sudo systemctl enable codex-dashboard    # ❌ Linux only
sudo systemctl daemon-reload             # ❌ Linux only
```

```batch
# Windows equivalents (USE THESE):
.\systemctl.bat start                     # ✅ Start services
.\systemctl.bat stop                      # ✅ Stop services  
.\systemctl.bat restart                   # ✅ Restart services
.\systemctl.bat reload                    # ✅ Reload services
.\systemctl.bat status                    # ✅ Check status
.\systemctl.bat enable                    # ✅ Install as Windows service
.\systemctl.bat daemon-reload             # ✅ Reload config
```

### Or use PowerShell directly:
```powershell
powershell -ExecutionPolicy Bypass -File "codex-systemctl.ps1" status
powershell -ExecutionPolicy Bypass -File "codex-systemctl.ps1" start
powershell -ExecutionPolicy Bypass -File "codex-systemctl.ps1" stop
powershell -ExecutionPolicy Bypass -File "codex-systemctl.ps1" restart
```

## =====================================================
## YOUR CURRENT SERVICE STATUS
## =====================================================

✅ **API (Port 8000)**: RUNNING → http://127.0.0.1:8000/docs
✅ **Dashboard (Port 8501)**: RUNNING → http://127.0.0.1:8501  
✅ **Portfolio (Port 8503)**: RUNNING → http://127.0.0.1:8503

## =====================================================
## FILES CREATED FOR YOU
## =====================================================

1. **systemctl.bat** - Main Windows equivalent of systemctl
2. **codex-systemctl.ps1** - PowerShell service manager  
3. **codex-dashboard-service.ps1** - Individual service control
4. **configure-firewall.ps1** - Windows firewall setup (run as Admin)
5. **configure-firewall.bat** - Batch version of firewall setup

## =====================================================
## QUICK COMMANDS
## =====================================================

**Check what's running:**
```batch
.\systemctl.bat status
```

**Restart everything:**
```batch
.\systemctl.bat restart
```

**Stop all services:**
```batch
.\systemctl.bat stop
```

**Start all services:**
```batch
.\systemctl.bat start
```

## =====================================================
## NOTES
## =====================================================

- You're on Windows 11, not Linux
- `sudo` commands don't exist on Windows
- Use `systemctl.bat` as direct replacement
- All your services are currently running properly
- No nginx needed - services run directly on their ports