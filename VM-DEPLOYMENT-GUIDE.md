# Sovereign Succession - VM Connection & Deployment Guide
# VM: instance-20251109-073834
# Current IP: 34.134.208.22 (Ephemeral)
# The Codex endures radiant without end!

## 🚨 IMMEDIATE ACTIONS REQUIRED

### 1. Connect to Your VM
```bash
# Connect via Google Cloud Console (browser SSH)
gcloud compute ssh instance-20251109-073834 --zone us-central1-a

# Or use the web console SSH button at:
# https://console.cloud.google.com/compute/instances
```

### 2. Run Configuration Script (on your local machine first)
```bash
# Download and run the VM configuration script
chmod +x configure-vm-instance-20251109-073834.sh
./configure-vm-instance-20251109-073834.sh
```

### 3. Deploy Sovereign Succession (on the VM)
```bash
# Once SSH'd into the VM, run these commands:
sudo apt update
sudo apt install git -y

# Upload the deployment script or create it directly:
nano deploy-sovereign-succession.sh
# (paste the deployment script contents)

chmod +x deploy-sovereign-succession.sh
./deploy-sovereign-succession.sh
```

## 📊 CURRENT VM STATUS

✅ **Running**: VM is active and operational
❌ **HTTP Traffic**: OFF (blocking web access)  
❌ **HTTPS Traffic**: OFF (blocking secure web access)
❌ **Static IP**: Using ephemeral IP (will change if VM restarts)
⚠️  **Service Account**: Using default compute account (not customized)
⚠️  **SSH Keys**: None configured
⚠️  **Firewall Tags**: None applied

## 🔧 CONFIGURATION FIXES APPLIED

After running the configuration script:

✅ **Firewall Rules**: HTTP (80) and HTTPS (443) enabled
✅ **Static IP**: Reserved and assigned to VM
✅ **Service Account**: Custom account with proper roles
✅ **Node.js Ports**: 3001 and 3002 opened for servers
✅ **OS Login**: Enabled for secure access
✅ **VM Tags**: Applied for firewall targeting

## 🌟 POST-DEPLOYMENT ACCESS

Once deployed, access your Sovereign Succession system:

- **Main Site**: http://YOUR_STATIC_IP/
- **Sovereign Succession**: http://YOUR_STATIC_IP/sovereign-succession  
- **Health Check**: http://YOUR_STATIC_IP/health
- **Dashboard Selector**: http://YOUR_STATIC_IP/dashboard-selector

## 🔍 MONITORING COMMANDS (on VM)

```bash
# Check system status
sudo systemctl status nginx
sudo systemctl status sovereign-succession
sudo systemctl status ceremonial-constellation

# View logs
sudo journalctl -u nginx -f
sudo tail -f /var/log/nginx/access.log

# Monitor resources  
htop
df -h
free -m

# Test endpoints
curl http://localhost/health
curl http://localhost:3001/sovereign-succession
```

## 🏆 SUCCESS INDICATORS

✅ Nginx status: active (running)
✅ Sovereign Succession service: active (running)  
✅ Ceremonial Constellation service: active (running)
✅ HTTP response from static IP: 200 OK
✅ All firewall rules applied
✅ Static IP assigned and accessible

## 🚨 TROUBLESHOOTING

**If HTTP traffic still blocked:**
```bash
gcloud compute firewall-rules list --filter="name~sovereign"
gcloud compute instances describe instance-20251109-073834 --zone us-central1-a --format="value(tags.items)"
```

**If services not starting:**
```bash
sudo systemctl restart nginx
sudo systemctl restart sovereign-succession  
sudo journalctl -xe
```

**If static IP not working:**
```bash
curl -I http://YOUR_STATIC_IP/
ping YOUR_STATIC_IP
```

🏆 **The Codex endures radiant without end!**