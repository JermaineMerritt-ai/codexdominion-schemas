# 🚀 QUICK START: Launch Codex Dominion in 3 Hours

**Target**: Production deployment at codexdominion.app
**Time Required**: 2-3 hours
**Status**: ✅ System ready, only secrets needed

---

## ⚡ FAST TRACK (Complete These 4 Steps)

### Step 1: Set Production Secrets (10 minutes)

**1.1 Generate Keys:**
```powershell
# Generate SECRET_KEY (already done for you):
# SECRET_KEY=PgoniCuZqAdzFJDcExQmNjGU1a0tT5B3Sf47vY8sw9WhLbe2krROV6pHlIKXyM

# Generate JWT_SECRET:
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | ForEach-Object {[char]$_})

# Generate API_KEY:
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

**1.2 Update `.env.production`:**
```bash
# Edit file
code .env.production

# Replace these lines:
SECRET_KEY=PgoniCuZqAdzFJDcExQmNjGU1a0tT5B3Sf47vY8sw9WhLbe2krROV6pHlIKXyM
JWT_SECRET=[paste JWT_SECRET from above]
API_KEY=[paste API_KEY from above]
DATABASE_URL=postgresql://codex:[YOUR_DB_PASSWORD]@localhost:5432/codexdominion_prod
REDIS_PASSWORD=[YOUR_SECURE_REDIS_PASSWORD]
```

**1.3 Update `frontend/.env.production`** (verify these are set):
```bash
NEXT_PUBLIC_API_URL=https://api.codexdominion.app
NEXT_PUBLIC_SITE_URL=https://codexdominion.app
```

---

### Step 2: Setup SSL Certificates (30-60 minutes)

**Option A: Let's Encrypt (Recommended)**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificates
sudo certbot certonly --nginx -d codexdominion.app -d www.codexdominion.app
sudo certbot certonly --nginx -d api.codexdominion.app

# Certificates will be saved to:
# /etc/letsencrypt/live/codexdominion.app/fullchain.pem
# /etc/letsencrypt/live/codexdominion.app/privkey.pem
```

**Option B: Manual Upload (if using hosting provider)**
1. Purchase SSL certificate from provider
2. Upload via hosting control panel
3. Note certificate paths

**Verify SSL:**
```bash
curl -I https://codexdominion.app
```

---

### Step 3: Setup Database (20 minutes)

**3.1 Install PostgreSQL** (skip if already installed):
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**3.2 Create Production Database:**
```bash
# Switch to postgres user
sudo -u postgres psql

# Run these commands in psql:
CREATE DATABASE codexdominion_prod;
CREATE USER codex WITH ENCRYPTED PASSWORD 'your_secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE codexdominion_prod TO codex;
\q
```

**3.3 Test Connection:**
```bash
psql -U codex -d codexdominion_prod -h localhost -W
# Enter password when prompted
# If connected successfully, type: \q to exit
```

---

### Step 4: Verify DNS (5 minutes)

**Check DNS Records:**
```bash
nslookup codexdominion.app
nslookup api.codexdominion.app
nslookup www.codexdominion.app
```

**Required DNS Records** (set via domain registrar):
```
Type    Name                Value           TTL
A       codexdominion.app   [SERVER_IP]     3600
A       www                 [SERVER_IP]     3600
A       api                 [SERVER_IP]     3600
```

---

## 🚀 LAUNCH (30 minutes)

### Pre-Launch Checklist
```bash
# 1. Verify you're in project root
cd /path/to/codex-dominion

# 2. Ensure Docker is running
docker ps

# 3. Load environment variables
export $(cat .env.production | grep -v '^#' | xargs)

# 4. Test database connection
psql $DATABASE_URL -c "SELECT 1;"

# 5. Verify secrets are set
cat .env.production | grep "SECRET_KEY"
```

### Deploy Using Automated Script
```powershell
# Recommended: Use the automated launch script
.\launch-production.ps1

# Or dry-run first to see what it will do:
.\launch-production.ps1 -DryRun

# Skip pre-flight checks (not recommended):
.\launch-production.ps1 -SkipChecks
```

### Manual Deployment (Alternative)
```bash
# Build and start all services
docker-compose -f docker-compose.production.yml build
docker-compose -f docker-compose.production.yml up -d

# Wait for services to start
sleep 30

# Check all containers are running
docker ps

# View logs
docker-compose -f docker-compose.production.yml logs -f
```

### Verify Deployment
```bash
# Test main site
curl -I https://codexdominion.app

# Test API
curl https://api.codexdominion.app/health

# Check container health
docker ps --filter "health=healthy"
```

---

## 📊 Post-Launch (First Hour)

### Monitor System
```bash
# View live logs
docker-compose -f docker-compose.production.yml logs -f

# Check resource usage
docker stats

# Monitor specific service
docker logs codex-dashboard -f
```

### Test Critical Features
1. **Dashboard**: Visit https://codexdominion.app
2. **Capsules**: Visit https://codexdominion.app/capsules
3. **Signals**: Visit https://codexdominion.app/signals
4. **API Health**: Visit https://api.codexdominion.app/health

### Watch for Issues
```bash
# Check for errors
docker-compose logs | grep -i error

# Check disk space
df -h

# Check memory usage
free -m
```

---

## 🆘 TROUBLESHOOTING

### Issue: Container won't start
```bash
# Check container logs
docker logs [container_name]

# Restart specific service
docker-compose -f docker-compose.production.yml restart [service_name]

# Rebuild and restart
docker-compose -f docker-compose.production.yml up -d --build [service_name]
```

### Issue: "Connection refused" errors
```bash
# Check if port is listening
netstat -tuln | grep [PORT_NUMBER]

# Check firewall
sudo ufw status

# Allow required ports
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### Issue: SSL certificate errors
```bash
# Verify certificate files exist
ls -la /etc/letsencrypt/live/codexdominion.app/

# Test SSL
openssl s_client -connect codexdominion.app:443 -servername codexdominion.app

# Renew certificate
sudo certbot renew
```

### Issue: Database connection fails
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U codex -d codexdominion_prod -h localhost

# Check DATABASE_URL format
echo $DATABASE_URL
```

---

## 🔄 ROLLBACK PROCEDURE

If critical issues occur:

```bash
# Option 1: Use automated script
.\launch-production.ps1 -RollbackMode

# Option 2: Manual rollback
docker-compose -f docker-compose.production.yml down
git checkout [previous-stable-tag]
docker-compose -f docker-compose.production.yml up -d --build
```

---

## 📞 QUICK COMMANDS REFERENCE

```bash
# Start all services
docker-compose -f docker-compose.production.yml up -d

# Stop all services
docker-compose -f docker-compose.production.yml down

# View logs
docker-compose -f docker-compose.production.yml logs -f

# Restart service
docker-compose -f docker-compose.production.yml restart [service]

# Rebuild service
docker-compose -f docker-compose.production.yml up -d --build [service]

# Check service health
docker ps --format "table {{.Names}}\t{{.Status}}"

# Database backup
pg_dump codexdominion_prod > backup_$(date +%Y%m%d).sql

# Restore database
psql codexdominion_prod < backup_20251207.sql
```

---

## ✅ SUCCESS CHECKLIST

After launch, verify these are all ✅:

- [ ] https://codexdominion.app loads (status 200)
- [ ] https://api.codexdominion.app/health returns OK
- [ ] All Docker containers show "healthy" status
- [ ] No critical errors in logs
- [ ] Dashboard displays correctly
- [ ] Capsules page loads
- [ ] Signals page loads
- [ ] SSL certificate valid (no browser warnings)
- [ ] DNS resolves correctly for all domains

---

## 🎯 TIMELINE SUMMARY

| Step | Task | Time | Status |
|------|------|------|--------|
| 1 | Set production secrets | 10 min | ⏳ TODO |
| 2 | Setup SSL certificates | 30-60 min | ⏳ TODO |
| 3 | Setup database | 20 min | ⏳ TODO |
| 4 | Verify DNS | 5 min | ⏳ TODO |
| 5 | Deploy with Docker Compose | 30 min | ⏳ TODO |
| 6 | Post-launch monitoring | 1 hour | ⏳ TODO |
| **TOTAL** | **End-to-end launch** | **2-3 hours** | ⏳ TODO |

---

## 📚 FULL DOCUMENTATION

For detailed information, see:
- `PRODUCTION_DEPLOYMENT_CHECKLIST.md` - Complete checklist
- `PRODUCTION_READINESS_SUMMARY.md` - System status and approval
- `CSS_REFACTORING_STRATEGY.md` - Post-launch code improvements
- `launch-production.ps1` - Automated deployment script

---

**Ready to launch?** Start with Step 1 above! 🚀

**Need help?** Check the troubleshooting section or review full documentation.

**Estimated Time to Live**: 2-3 hours from now! 🎉
