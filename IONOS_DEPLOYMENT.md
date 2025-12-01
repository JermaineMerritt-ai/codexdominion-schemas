# 🚀 IONOS Deployment Guide for Codex Dominion
# Domain: CodexDominion.app (Google Domains)
# Hosting: IONOS

## 📋 Prerequisites

- IONOS VPS or Dedicated Server
- Domain registered with Google Domains (CodexDominion.app)
- SSH access to IONOS server
- Docker and Docker Compose installed

## 🌐 Domain Configuration (Google Domains)

### DNS Records to Add

```
Type    Name    Value                           TTL
A       @       YOUR_IONOS_SERVER_IP            3600
A       www     YOUR_IONOS_SERVER_IP            3600
A       api     YOUR_IONOS_SERVER_IP            3600
A       monitoring YOUR_IONOS_SERVER_IP         3600
CNAME   *       codexdominion.app               3600
```

### Steps:
1. Go to https://domains.google.com
2. Select `CodexDominion.app`
3. Navigate to **DNS** section
4. Add the A records above (replace YOUR_IONOS_SERVER_IP)
5. Wait 5-10 minutes for propagation

## 🖥️ IONOS Server Setup

### 1. Initial Server Configuration

```bash
# SSH into your IONOS server
ssh root@YOUR_IONOS_SERVER_IP

# Update system
apt update && apt upgrade -y

# Install required packages
apt install -y \
    curl \
    git \
    wget \
    vim \
    htop \
    ufw \
    fail2ban

# Configure firewall
ufw allow 22/tcp   # SSH
ufw allow 80/tcp   # HTTP
ufw allow 443/tcp  # HTTPS
ufw enable

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Verify installations
docker --version
docker-compose --version
```

### 2. Clone Repository

```bash
# Create application directory
mkdir -p /var/www
cd /var/www

# Clone your repository
git clone https://github.com/JermaineMerritt-ai/codexdominion-schemas.git codexdominion
cd codexdominion

# Checkout main branch
git checkout main
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

**Required Environment Variables:**

```bash
# Application
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://api.codexdominion.app
NEXT_PUBLIC_DOMAIN=https://codexdominion.app

# Database
DATABASE_URL=postgresql://codex:YOUR_DB_PASSWORD@postgres:5432/codex_dominion
DB_USER=codex
DB_PASSWORD=YOUR_SECURE_DB_PASSWORD

# Redis
REDIS_URL=redis://redis:6379
REDIS_PASSWORD=YOUR_SECURE_REDIS_PASSWORD

# Security
JWT_SECRET=YOUR_SECURE_JWT_SECRET_MIN_32_CHARS

# AI APIs
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key

# Cloud Storage (Optional)
GCS_BUCKET=codex-artifacts
GCS_PROJECT_ID=your-gcp-project-id

# Monitoring
GRAFANA_USER=admin
GRAFANA_PASSWORD=YOUR_SECURE_GRAFANA_PASSWORD
```

**Generate Secure Secrets:**

```bash
# JWT Secret (32+ characters)
openssl rand -hex 32

# Database Password
openssl rand -base64 32

# Redis Password
openssl rand -base64 32

# Grafana Password
openssl rand -base64 16
```

### 4. SSL Certificate Setup (Let's Encrypt)

```bash
# Install Certbot
apt install -y certbot python3-certbot-nginx

# Stop nginx if running
docker-compose down nginx

# Obtain SSL certificate
certbot certonly --standalone \
    -d codexdominion.app \
    -d www.codexdominion.app \
    -d api.codexdominion.app \
    -d monitoring.codexdominion.app \
    --email your-email@example.com \
    --agree-tos \
    --non-interactive

# Verify certificates
ls -la /etc/letsencrypt/live/codexdominion.app/

# Setup auto-renewal
echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
```

### 5. Build and Deploy

```bash
# Build Docker images
docker-compose -f docker-compose.production.yml build

# Start services
docker-compose -f docker-compose.production.yml up -d

# View logs
docker-compose -f docker-compose.production.yml logs -f

# Check container status
docker-compose -f docker-compose.production.yml ps
```

### 6. Verify Deployment

```bash
# Test frontend
curl https://codexdominion.app

# Test API
curl https://api.codexdominion.app/health

# Test monitoring
curl https://monitoring.codexdominion.app

# Check all containers are healthy
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

## 🔄 Continuous Deployment

### Setup Webhook for Auto-Deploy

```bash
# Create deployment script
cat > /var/www/codexdominion/deploy.sh << 'EOF'
#!/bin/bash
cd /var/www/codexdominion

# Pull latest changes
git fetch --all
git reset --hard origin/main

# Rebuild and restart
docker-compose -f docker-compose.production.yml build
docker-compose -f docker-compose.production.yml up -d

# Cleanup old images
docker system prune -af --volumes

echo "Deployment completed at $(date)"
EOF

chmod +x /var/www/codexdominion/deploy.sh

# Test deployment script
./deploy.sh
```

### GitHub Actions Auto-Deploy

Add this secret to your GitHub repository:
- **Name**: `IONOS_SSH_KEY`
- **Value**: Your IONOS server SSH private key

The existing workflow `.github/workflows/enhanced-codex-cicd.yml` will automatically deploy on push to main.

## 📊 Monitoring Setup

### 1. Access Grafana

```
URL: https://monitoring.codexdominion.app
Username: admin
Password: (from .env GRAFANA_PASSWORD)
```

### 2. Import Dashboards

1. Log into Grafana
2. Go to Dashboards → Import
3. Upload `grafana/codex-dominion-dashboard.json`

### 3. Setup Alerts

Configure alerts in Grafana for:
- High CPU usage (> 80%)
- High memory usage (> 85%)
- Container down
- API errors (> 10/min)
- Response time (> 3s)

## 🔒 Security Hardening

### 1. Nginx Basic Auth for Monitoring

```bash
# Install apache2-utils
apt install -y apache2-utils

# Create password file
htpasswd -c /etc/nginx/.htpasswd admin

# Enter secure password when prompted
```

### 2. Fail2Ban Configuration

```bash
# Create Nginx jail
cat > /etc/fail2ban/jail.d/nginx.conf << EOF
[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 10
findtime = 600
bantime = 7200
EOF

# Restart Fail2Ban
systemctl restart fail2ban
```

### 3. Database Backup

```bash
# Create backup script
cat > /var/www/codexdominion/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/codexdominion"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
docker exec codex-postgres pg_dump -U codex codex_dominion | \
    gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Backup volumes
docker run --rm -v codex-dominion_postgres-data:/data \
    -v $BACKUP_DIR:/backup alpine tar czf \
    /backup/postgres_data_$DATE.tar.gz /data

# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completed at $(date)"
EOF

chmod +x /var/www/codexdominion/backup.sh

# Setup daily backup cron
echo "0 2 * * * /var/www/codexdominion/backup.sh" | crontab -
```

## 🚨 Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose -f docker-compose.production.yml logs [service-name]

# Check container details
docker inspect [container-name]

# Restart specific service
docker-compose -f docker-compose.production.yml restart [service-name]
```

### SSL Certificate Issues

```bash
# Test certificate renewal
certbot renew --dry-run

# Force renewal
certbot renew --force-renewal

# Restart nginx
docker-compose -f docker-compose.production.yml restart nginx
```

### Database Connection Issues

```bash
# Check database logs
docker logs codex-postgres

# Connect to database
docker exec -it codex-postgres psql -U codex -d codex_dominion

# Test connection from backend
docker exec -it codex-backend python -c "import psycopg2; psycopg2.connect('$DATABASE_URL')"
```

### Performance Issues

```bash
# Monitor resources
htop

# Check Docker stats
docker stats

# Optimize containers
docker-compose -f docker-compose.production.yml down
docker system prune -af --volumes
docker-compose -f docker-compose.production.yml up -d
```

## 📞 Support

For deployment issues:
- **Email**: support@codex-dominion.com
- **GitHub Issues**: https://github.com/JermaineMerritt-ai/codexdominion-schemas/issues
- **Documentation**: https://codex-dominion.com/docs

## ✅ Post-Deployment Checklist

- [ ] Domain DNS configured and propagated
- [ ] SSL certificates obtained and installed
- [ ] All environment variables set
- [ ] Docker containers running and healthy
- [ ] Frontend accessible at https://codexdominion.app
- [ ] API accessible at https://api.codexdominion.app
- [ ] Monitoring accessible at https://monitoring.codexdominion.app
- [ ] Database backups configured
- [ ] Firewall rules configured
- [ ] Fail2Ban active
- [ ] Auto-deployment webhook configured
- [ ] Monitoring alerts configured
- [ ] Health checks passing

---

**🎉 Congratulations! Your Codex Dominion is now live on IONOS!**

**Production URL**: https://codexdominion.app

**Deployment Date**: December 1, 2025
