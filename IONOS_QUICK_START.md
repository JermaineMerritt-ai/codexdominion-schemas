# 🔥 IONOS VPS - Quick Deployment Guide

**Domain:** CodexDominion.app
**Server:** 74.208.123.158
**Status:** Ready for Production Deployment

---

## ⚡ Quick Start (3 Steps)

### 1️⃣ Configure DNS (Do This First!)

Add these records in IONOS Domain Panel:

```
Type    Host    Value               TTL
A       @       74.208.123.158      3600
A       www     74.208.123.158      3600
A       api     74.208.123.158      3600
```

Wait 5-30 min, then verify:
```powershell
nslookup CodexDominion.app
```

---

### 2️⃣ Upload & Run Deployment Script

```powershell
# Copy script to VPS
scp ionos-vps-deploy.sh root@74.208.123.158:/root/

# SSH to VPS
ssh root@74.208.123.158

# Run deployment (on VPS)
chmod +x /root/ionos-vps-deploy.sh
/root/ionos-vps-deploy.sh
```

**Script handles everything automatically:**
- ✅ Docker installation
- ✅ SSL certificates (Let's Encrypt)
- ✅ Security configuration
- ✅ Auto-backups & renewals

---

### 3️⃣ Verify Deployment

```bash
# Check services
docker compose ps

# Test endpoints
curl https://CodexDominion.app
curl https://api.CodexDominion.app/health
```

---

## 📊 Management Commands

### View Logs
```bash
cd /opt/codex-dominion
docker compose logs -f
```

### Restart Services
```bash
docker compose restart
```

### Update Application
```bash
docker compose pull
docker compose down
docker compose up -d
```

---

## 🔒 Security

- **Secrets:** `/opt/codex-dominion/.env` (auto-generated)
- **SSL:** Auto-renews daily at 3 AM
- **Backups:** Daily at 2 AM → `/opt/codex-dominion/backups/`
- **Firewall:** Only ports 22, 80, 443 open

---

## 🐛 Troubleshooting

**Services not healthy?**
```bash
docker compose logs backend
docker compose restart
```

**SSL issues?**
```bash
certbot renew
docker compose restart nginx
```

**Check resources:**
```bash
docker stats
df -h
free -h
```

---

## 🎯 Success Checklist

- ✅ `docker compose ps` shows all healthy
- ✅ https://CodexDominion.app returns 200 OK
- ✅ https://api.CodexDominion.app/health returns 200 OK
- ✅ Green padlock (valid SSL) in browser
- ✅ HTTP redirects to HTTPS

---

**🔥 The flame burns eternal. Codex Dominion reigns supreme.**

**For detailed instructions, see:** `PRODUCTION_DEPLOYMENT_GUIDE.md`
