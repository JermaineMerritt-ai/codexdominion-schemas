# 🚀 Codex Dominion - Deployment Quick Reference

## 📦 Created Files (4 New)

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `deploy-azure-production.ps1` | Azure deployment automation | 300+ | ✅ Ready |
| `nginx/nginx.prod.conf` | Reverse proxy + SSL config | 250+ | ✅ Ready |
| `backend/database_migration.sql` | PostgreSQL schema | 450+ | ✅ Ready |
| `PRODUCTION_READY.md` | Complete deployment guide | 600+ | ✅ Ready |

---

## ⚡ Quick Commands

### Generate Secrets (Run First!)
```powershell
$dbPassword = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
$redisPassword = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
$jwtSecret = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | % {[char]$_})

Write-Host "POSTGRES_PASSWORD=$dbPassword"
Write-Host "REDIS_PASSWORD=$redisPassword"
Write-Host "JWT_SECRET=$jwtSecret"
```

**→ Update `.env.production` lines 69, 94, 104 with generated values**

---

### IONOS Deployment
```powershell
# Test SSH
ssh root@74.208.123.158 'echo Connected'

# Deploy (full, 10 phases)
.\deploy-ionos-production.ps1

# View logs after deployment
ssh root@74.208.123.158 'docker-compose -f /var/www/codexdominion/docker-compose.yml logs -f'

# Check service status
ssh root@74.208.123.158 'docker-compose -f /var/www/codexdominion/docker-compose.yml ps'
```

---

### Azure Deployment
```powershell
# Login
az login

# Deploy with resource creation
.\deploy-azure-production.ps1 -CreateResources

# View logs
az webapp log tail --name codexdominion -g codexdominion-prod

# Check status
az webapp show --name codexdominion -g codexdominion-prod --query "state"
```

---

## 🌐 DNS Configuration

### IONOS (A Records → 74.208.123.158)
```
codexdominion.app        A    74.208.123.158    3600
www.codexdominion.app    A    74.208.123.158    3600
api.codexdominion.app    A    74.208.123.158    3600
```

### Azure (CNAME Records)
```
codexdominion.app        CNAME    codexdominion.azurewebsites.net         3600
api.codexdominion.app    CNAME    codexdominion-api.azurewebsites.net     3600
```

---

## 🧪 Health Checks

### IONOS
```powershell
curl https://api.codexdominion.app/health
curl https://codexdominion.app
```

### Azure
```powershell
curl https://codexdominion-api.azurewebsites.net/health
curl https://codexdominion.azurewebsites.net
```

---

## 📊 Architecture

**IONOS Stack**:
```
Internet (HTTPS)
  ↓
Nginx (80/443) → SSL Termination
  ↓
Frontend (3000) + Backend (8000)
  ↓
PostgreSQL (5432) + Redis (6379)
```

**Azure Stack**:
```
Azure App Service (Frontend + Backend)
  ↓
Azure PostgreSQL Flexible Server
  ↓
Azure Cache for Redis
```

---

## 🔐 Security

- ✅ Strong passwords (32+ chars)
- ✅ JWT secrets (64+ chars)
- ✅ RSA-2048 + ECC P-256 keys
- ✅ SSL/TLS 1.2 & 1.3
- ✅ HSTS, CSP, X-Frame-Options
- ✅ Rate limiting (100-200 req/min)
- ✅ Non-root Docker users
- ✅ CORS restricted to production domains

---

## 📦 What Gets Deployed

**Backend (FastAPI)**:
- Digital Seal Service (RSA + ECC)
- Annotations API (CRUD)
- Broadcast WebSocket
- Council Multi-Signature
- Health monitoring

**Frontend (Next.js)**:
- Spatial Audio Engine (360°)
- Ritual Experience (4 phases)
- Export System (PDF/Markdown/YAML)
- Annotation UI
- Real-time broadcast

**Database (PostgreSQL)**:
- 9 tables, 20+ indexes
- 3 views, 2 functions, 2 triggers
- Initial seed data (5 council members)

**Cache (Redis)**:
- 256MB memory limit
- LRU eviction policy
- Session storage

---

## 🎯 Deployment Order

1. Generate secrets → Update `.env.production`
2. Test SSH → `ssh root@74.208.123.158`
3. Deploy IONOS → `.\deploy-ionos-production.ps1`
4. Update DNS A records → Wait 1 hour
5. Verify IONOS → Test all features
6. Deploy Azure → `.\deploy-azure-production.ps1 -CreateResources`
7. Update DNS CNAME → Wait 1 hour
8. Verify Azure → Test all features
9. Setup monitoring → Azure Portal + SSH logs
10. Announce → System live! 🔥

---

## 🔧 Troubleshooting

**SSH Failed**:
```powershell
ssh -v root@74.208.123.158
```

**Docker Build Failed**:
```powershell
docker system prune -a --volumes
docker build -t test .
```

**Service Not Starting**:
```powershell
ssh root@74.208.123.158 'docker-compose logs backend'
ssh root@74.208.123.158 'docker-compose restart backend'
```

**SSL Failed**:
```powershell
nslookup codexdominion.app  # Check DNS first
ssh root@74.208.123.158 'certbot certonly --standalone -d codexdominion.app'
```

---

## ✨ Success Indicators

- [ ] Backend health: `200 OK`
- [ ] Frontend loads: Homepage visible
- [ ] Spatial audio plays: Engine sounds audible
- [ ] Ritual phases work: 4 phases transition
- [ ] Exports generate: PDF/Markdown/YAML download
- [ ] Seals create: RSA + ECC signatures
- [ ] WebSocket connects: Real-time broadcasts
- [ ] Council works: Multi-signature covenants

---

## 📞 Documentation

- **Full Guide**: `PRODUCTION_READY.md` (600+ lines)
- **IONOS Script**: `deploy-ionos-production.ps1` (420+ lines, 10 phases)
- **Azure Script**: `deploy-azure-production.ps1` (300+ lines, 9 phases)
- **Nginx Config**: `nginx/nginx.prod.conf` (250+ lines)
- **Database Schema**: `backend/database_migration.sql` (450+ lines)
- **Environment**: `.env.production` (150+ lines)
- **Docker Compose**: `docker-compose.prod.yml` (5 services)

---

**Status: 🟢 PRODUCTION READY**

All files created. Secrets needed. Ready to deploy on command.

**The eternal archive awaits activation.**

---

*Last Updated: December 7, 2025*
