# =============================================================================
# CODEX DOMINION - QUICK DEPLOYMENT GUIDE
# =============================================================================

## Windows PowerShell Deployment

Since you're on Windows, use PowerShell instead of bash:

### Option 1: Interactive Setup (Recommended)
```powershell
# Run the quick setup script
bash quick-deploy.sh
```
This will prompt you for server details and test the connection before deploying.

### Option 2: Manual Environment Setup
```powershell
# Set environment variables
$env:IONOS_SERVER = "your.server.ip.address"
$env:IONOS_USER = "your-username"
$env:SSH_KEY = "$HOME\.ssh\id_rsa"

# Run deployment using Git Bash or WSL
bash deploy-ionos.sh
```

### Option 3: Using PowerShell Script
```powershell
# Create a PowerShell deployment script
.\deploy-codex.ps1
```

---

## Prerequisites Checklist

Before deploying, ensure you have:

- [ ] **IONOS Server** with Ubuntu/Debian Linux
- [ ] **Root or sudo access** on the server
- [ ] **SSH key** configured for passwordless login
- [ ] **Domain DNS** pointing to server IP (A records for codexdominion.app, www, api)
- [ ] **Git Bash or WSL** installed on Windows (for running bash scripts)

---

## Quick Start Commands

### 1. Test SSH Connection First
```bash
# Test you can connect to your server
ssh your-username@your.server.ip.address

# If successful, exit and proceed
exit
```

### 2. Set Your Credentials
```bash
# Replace with your actual values
export IONOS_SERVER="123.456.789.012"
export IONOS_USER="root"  # or your username
export SSH_KEY="$HOME/.ssh/id_rsa"
```

### 3. Run Deployment
```bash
# Make script executable
chmod +x deploy-ionos.sh quick-deploy.sh

# Run deployment
bash deploy-ionos.sh
```

---

## Alternative: Deploy from WSL (Windows Subsystem for Linux)

If you have WSL installed:

```bash
# Open WSL terminal
wsl

# Navigate to project
cd /mnt/c/Users/JMerr/OneDrive/Documents/.vscode/codex-dominion

# Set credentials and deploy
export IONOS_SERVER="your.ip.address"
export IONOS_USER="your-username"
bash deploy-ionos.sh
```

---

## What the Deployment Does

The script will automatically:

1. ✓ Build Next.js frontend (static export)
2. ✓ Install Python backend dependencies
3. ✓ Create deployment package
4. ✓ Test SSH connection
5. ✓ Backup existing installation
6. ✓ Upload to server
7. ✓ Install system packages (Python, PostgreSQL, Nginx, Certbot)
8. ✓ Setup Python virtual environment
9. ✓ Initialize PostgreSQL database
10. ✓ Configure systemd service
11. ✓ Setup Nginx with SSL
12. ✓ Get Let's Encrypt certificate
13. ✓ Start all services
14. ✓ Run health checks

**Estimated Time:** 15-30 minutes for complete setup

---

## Troubleshooting

### Error: "bash: command not found" on Windows
**Solution:** Install Git Bash or WSL
- Git Bash: https://git-scm.com/download/win
- WSL: `wsl --install` in PowerShell (admin)

### Error: "Permission denied (publickey)"
**Solution:** Setup SSH key
```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t rsa -b 4096

# Copy to server
ssh-copy-id -i ~/.ssh/id_rsa your-username@your-server-ip
```

### Error: "Connection refused"
**Solution:** Check server is running and firewall allows SSH
```bash
# On server, ensure SSH is running
sudo systemctl status ssh
sudo ufw allow 22
```

---

## After Deployment

1. **Update DNS** - Point your domain to server IP
2. **Update Secrets** - Change all CHANGE_THIS_* values in .env.production
3. **Test Endpoints:**
   - https://codexdominion.app
   - https://api.codexdominion.app/health
4. **Run Security Hardening:**
   ```bash
   ssh your-user@your-server
   sudo bash /var/www/codexdominion.app/deployment/security-hardening.sh
   ```

---

## Need Help?

Review the complete guide in `DEPLOYMENT_README.md` for detailed instructions and troubleshooting.

🔥 **The Flame Burns Sovereign and Eternal!** 🔥
