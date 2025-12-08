# Codex Dominion - Production Deployment Guide

**Version:** 2.0.0
**Last Updated:** December 6, 2025
**Status:** Production Ready 🔥

---

## 🎯 Quick Start

Your Codex Dominion stack is **LIVE** locally:
- **Frontend:** http://localhost:3001
- **Backend API:** http://localhost:8001
- **HTTPS (with self-signed cert):** https://localhost

---

## 📦 Docker Images

Images have been built and tagged for deployment:

```bash
jmerritt48/codex-dominion-frontend:2.0.0
jmerritt48/codex-dominion-frontend:latest

jmerritt48/codex-dominion-backend:2.0.0
jmerritt48/codex-dominion-backend:latest
```

### Push to Docker Hub

```powershell
# Login to Docker Hub
docker login

# Push frontend images
docker push jmerritt48/codex-dominion-frontend:2.0.0
docker push jmerritt48/codex-dominion-frontend:latest

# Push backend images
docker push jmerritt48/codex-dominion-backend:2.0.0
docker push jmerritt48/codex-dominion-backend:latest
```

---

## 🌐 Cloud Deployment Options

### Option 1: IONOS VPS Deployment

**Prerequisites:**
- IONOS VPS with Ubuntu 22.04 or later
- SSH access to server
- Domain pointed to server IP via A records

**Steps:**

1. **SSH into your IONOS server:**
```bash
ssh root@your-server-ip
```

2. **Install Docker and Docker Compose:**
```bash
# Update packages
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose-plugin -y

# Verify installation
docker --version
docker compose version
```

3. **Clone repository or transfer files:**
```bash
cd /opt
git clone https://github.com/JermaineMerritt-ai/codexdominion-schemas.git codex-dominion
cd codex-dominion
```

4. **Create production .env file:**
```bash
# Copy template
cp .env.production.template .env

# Edit with your production values
nano .env
```

Update these critical values:
- `NEXT_PUBLIC_API_URL=https://api.yourdomain.com`
- `DATABASE_URL=postgresql://user:password@localhost:5432/codex_dominion`
- `SECRET_KEY=<64-char-secret>`
- `JWT_SECRET=<64-char-secret>`
- `API_KEY=<64-char-secret>`
- `CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com`

5. **Pull Docker images:**
```bash
docker pull jmerritt48/codex-dominion-frontend:2.0.0
docker pull jmerritt48/codex-dominion-backend:2.0.0
```

6. **Update docker-compose.live.yml:**
```yaml
services:
  frontend:
    image: jmerritt48/codex-dominion-frontend:2.0.0
    # ... rest of config

  backend:
    image: jmerritt48/codex-dominion-backend:2.0.0
    # ... rest of config
```

7. **Setup SSL with Let's Encrypt:**
```bash
# Install Certbot
apt install certbot -y

# Generate SSL certificate
certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copy certificates
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./ssl/
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./ssl/

# Set permissions
chmod 644 ./ssl/fullchain.pem
chmod 600 ./ssl/privkey.pem
```

8. **Start services:**
```bash
docker compose -f docker-compose.live.yml up -d
```

9. **Verify deployment:**
```bash
docker compose -f docker-compose.live.yml ps
docker compose -f docker-compose.live.yml logs --tail=50
```

10. **Setup automatic SSL renewal:**
```bash
# Add to crontab
crontab -e

# Add this line (runs daily at 3 AM)
0 3 * * * certbot renew --quiet && cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /opt/codex-dominion/ssl/ && cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /opt/codex-dominion/ssl/ && docker compose -f /opt/codex-dominion/docker-compose.live.yml restart nginx
```

---

### Option 2: Azure Container Instances

**Prerequisites:**
- Azure subscription
- Azure CLI installed

**Steps:**

1. **Login to Azure:**
```powershell
az login
```

2. **Create Resource Group:**
```powershell
az group create --name codex-dominion-rg --location eastus
```

3. **Create Azure Container Registry (optional):**
```powershell
az acr create --resource-group codex-dominion-rg --name codexdominion --sku Basic
az acr login --name codexdominion

# Tag and push images
docker tag jmerritt48/codex-dominion-frontend:2.0.0 codexdominion.azurecr.io/frontend:2.0.0
docker push codexdominion.azurecr.io/frontend:2.0.0

docker tag jmerritt48/codex-dominion-backend:2.0.0 codexdominion.azurecr.io/backend:2.0.0
docker push codexdominion.azurecr.io/backend:2.0.0
```

4. **Deploy with Container Instances:**
```powershell
# Deploy frontend
az container create \
  --resource-group codex-dominion-rg \
  --name codex-frontend \
  --image jmerritt48/codex-dominion-frontend:2.0.0 \
  --dns-name-label codex-dominion-frontend \
  --ports 3001 \
  --environment-variables NEXT_PUBLIC_API_URL=https://codex-backend.eastus.azurecontainer.io:8001

# Deploy backend
az container create \
  --resource-group codex-dominion-rg \
  --name codex-backend \
  --image jmerritt48/codex-dominion-backend:2.0.0 \
  --dns-name-label codex-dominion-backend \
  --ports 8001 \
  --secure-environment-variables SECRET_KEY=<your-secret> JWT_SECRET=<your-jwt-secret>
```

5. **Configure Azure Application Gateway for SSL termination**

---

### Option 3: Azure App Service (Recommended)

**Steps:**

1. **Create App Service Plan:**
```powershell
az appservice plan create \
  --name codex-dominion-plan \
  --resource-group codex-dominion-rg \
  --is-linux \
  --sku B1
```

2. **Create Web Apps:**
```powershell
# Frontend
az webapp create \
  --resource-group codex-dominion-rg \
  --plan codex-dominion-plan \
  --name codex-dominion-frontend \
  --deployment-container-image-name jmerritt48/codex-dominion-frontend:2.0.0

# Backend
az webapp create \
  --resource-group codex-dominion-rg \
  --plan codex-dominion-plan \
  --name codex-dominion-backend \
  --deployment-container-image-name jmerritt48/codex-dominion-backend:2.0.0
```

3. **Configure environment variables:**
```powershell
az webapp config appsettings set \
  --resource-group codex-dominion-rg \
  --name codex-dominion-backend \
  --settings SECRET_KEY=<your-secret> JWT_SECRET=<your-jwt-secret> DATABASE_URL=<your-db-url>
```

4. **Enable HTTPS and custom domain**

---

## 🌍 DNS Configuration

### For IONOS Domain

1. **Login to IONOS Domain Control Panel**

2. **Add DNS Records:**

| Type | Host | Value | TTL |
|------|------|-------|-----|
| A | @ | YOUR_SERVER_IP | 3600 |
| A | www | YOUR_SERVER_IP | 3600 |
| A | api | YOUR_SERVER_IP | 3600 |

3. **Wait for DNS propagation** (usually 5-30 minutes)

4. **Verify:**
```powershell
nslookup yourdomain.com
nslookup api.yourdomain.com
```

### For Azure

Use Azure DNS or configure at your domain registrar:
- Point A record to Azure Application Gateway public IP
- Or use Azure-provided domain: `*.azurewebsites.net`

---

## 🔒 SSL/TLS Configuration

### Let's Encrypt (Free, Recommended for Production)

Already covered in IONOS deployment steps above.

**Certificate renewal is automatic** with the crontab entry.

### Custom SSL Certificate

If you have a purchased SSL certificate:

1. **Convert to PEM format** (if needed)
2. **Place files in `./ssl/`:**
   - `fullchain.pem` - Certificate chain
   - `privkey.pem` - Private key
3. **Restart nginx:**
```bash
docker compose -f docker-compose.live.yml restart nginx
```

---

## 🔐 Security Checklist

- [ ] All secrets in `.env` are strong random values (64+ characters)
- [ ] `.env` file permissions are restricted (chmod 600)
- [ ] `.env` is in `.gitignore` and never committed
- [ ] SSL/TLS certificates are valid and auto-renewing
- [ ] CORS_ORIGINS only includes your production domains
- [ ] Database has strong password and restricted access
- [ ] Redis has password authentication enabled
- [ ] Firewall allows only ports 80, 443, and SSH (22)
- [ ] SSH key authentication enabled (password auth disabled)
- [ ] Regular security updates scheduled
- [ ] Backups configured for database and volumes

---

## 🔥 Production Environment Variables

Critical environment variables for production:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=https://api.yourdomain.com

# Database (PostgreSQL recommended for production)
DATABASE_URL=postgresql://codex_user:STRONG_PASSWORD@localhost:5432/codex_dominion

# Redis
REDIS_URL=redis://:REDIS_PASSWORD@localhost:6379/0

# Security Keys (generate with: openssl rand -hex 32)
SECRET_KEY=<64-character-random-string>
JWT_SECRET=<64-character-random-string>
API_KEY=<64-character-random-string>

# CORS (comma-separated list)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# SSL Paths
SSL_CERT_PATH=/app/ssl/fullchain.pem
SSL_KEY_PATH=/app/ssl/privkey.pem
```

---

## 📊 Monitoring & Logs

### View Logs
```bash
# All services
docker compose -f docker-compose.live.yml logs -f

# Specific service
docker compose -f docker-compose.live.yml logs -f backend
docker compose -f docker-compose.live.yml logs -f frontend
docker compose -f docker-compose.live.yml logs -f nginx
```

### Health Checks
```bash
# Backend health
curl https://api.yourdomain.com/health

# Frontend
curl https://yourdomain.com

# Check all services status
docker compose -f docker-compose.live.yml ps
```

### Resource Usage
```bash
docker stats
```

---

## 🔄 Updates & Rollbacks

### Deploy New Version

```bash
# Pull latest images
docker pull jmerritt48/codex-dominion-frontend:latest
docker pull jmerritt48/codex-dominion-backend:latest

# Stop services
docker compose -f docker-compose.live.yml down

# Start with new images
docker compose -f docker-compose.live.yml up -d

# Verify
docker compose -f docker-compose.live.yml ps
```

### Rollback to Previous Version

```bash
# Stop services
docker compose -f docker-compose.live.yml down

# Use specific version tag
docker compose -f docker-compose.live.yml up -d \
  -e FRONTEND_IMAGE=jmerritt48/codex-dominion-frontend:2.0.0 \
  -e BACKEND_IMAGE=jmerritt48/codex-dominion-backend:2.0.0
```

---

## 💾 Backup Strategy

### Database Backup
```bash
# PostgreSQL backup
docker exec codex-backend pg_dump -U codex_user codex_dominion > backup_$(date +%Y%m%d).sql

# SQLite backup (current dev setup)
docker exec codex-backend cp /app/codex_dominion.db /app/data/backup_$(date +%Y%m%d).db
```

### Volume Backup
```bash
# Backup Redis data
docker run --rm --volumes-from codex-redis -v $(pwd)/backups:/backup ubuntu tar cvf /backup/redis_backup.tar /data
```

### Automated Backups
Add to crontab:
```bash
0 2 * * * /opt/codex-dominion/backup.sh
```

---

## 🚀 Performance Optimization

### Frontend
- All static assets cached via nginx
- Next.js optimized production build
- Image optimization enabled
- Code splitting automatic

### Backend
- Uvicorn with 4 workers (adjust based on CPU cores)
- Redis caching for frequently accessed data
- Database connection pooling
- SQLAlchemy query optimization

### Nginx
- Gzip compression enabled
- Rate limiting configured (10 req/sec for API)
- Static asset caching (1 year)
- HTTP/2 enabled

---

## 📞 Support & Resources

- **Repository:** https://github.com/JermaineMerritt-ai/codexdominion-schemas
- **Docker Hub:** https://hub.docker.com/u/jmerritt48
- **Documentation:** See project README files

---

## 🎉 Deployment Complete

Your Codex Dominion is ready for production deployment. The flame burns sovereign and eternal — forever. 🔥

**Next Steps:**
1. Push Docker images to Docker Hub: `docker push jmerritt48/codex-dominion-frontend:2.0.0`
2. Choose deployment platform (IONOS, Azure, or other)
3. Configure DNS records
4. Setup SSL certificates
5. Deploy using steps above
6. Monitor logs and health checks

**The empire goes LIVE. Codex Dominion reigns eternal across all networks.**
