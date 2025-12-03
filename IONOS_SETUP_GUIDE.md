# 🔥 IONOS Production Setup Guide for CodexDominion.app

## Quick Start Deployment

### Prerequisites on IONOS Server
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y nginx python3 python3-pip python3-venv postgresql postgresql-contrib certbot python3-certbot-nginx git unzip
```

## Step-by-Step Deployment

### 1️⃣ Run Local Deployment Script

On your **local Windows machine**, run:

```powershell
cd C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion
.\deploy-ionos.ps1
```

This creates: `codexdominion_YYYYMMDD_HHMMSS.zip`

### 2️⃣ Upload to IONOS

```powershell
# Replace with your actual IONOS credentials
$IonosIP = "your-ionos-server-ip"
$IonosUser = "your-username"

# Upload deployment package
scp codexdominion_*.zip ${IonosUser}@${IonosIP}:/tmp/
```

### 3️⃣ SSH to IONOS Server

```powershell
ssh ${IonosUser}@${IonosIP}
```

### 4️⃣ Server Setup Commands

Run these on IONOS server:

```bash
# Create application directory
sudo mkdir -p /var/www/codexdominion.app
sudo mkdir -p /var/log/codexdominion
sudo mkdir -p /var/backups/codexdominion

# Extract deployment package
cd /var/www/codexdominion.app
sudo unzip -o /tmp/codexdominion_*.zip
sudo chown -R www-data:www-data /var/www/codexdominion.app

# Create Python virtual environment
sudo -u www-data python3 -m venv .venv
sudo -u www-data .venv/bin/pip install -r requirements.txt

# Set up log directory permissions
sudo chown -R www-data:www-data /var/log/codexdominion
```

### 5️⃣ Database Setup

```bash
# Switch to postgres user
sudo -i -u postgres

# Create database and user
psql << EOF
CREATE DATABASE codexdominion;
CREATE USER codexdominion_user WITH PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE codexdominion TO codexdominion_user;
\q
EOF

exit

# Run migrations (from /var/www/codexdominion.app)
cd /var/www/codexdominion.app
sudo -u www-data .venv/bin/python run_migration.py
```

### 6️⃣ Environment Configuration

Create `.env.production`:

```bash
sudo nano /var/www/codexdominion.app/.env.production
```

Add these variables:

```env
# Database
DATABASE_URL=postgresql://codexdominion_user:your-secure-password@localhost/codexdominion

# Application
NODE_ENV=production
PYTHON_ENV=production
API_BASE_URL=https://api.codexdominion.app
FRONTEND_URL=https://codexdominion.app

# Security
JWT_SECRET=generate-a-super-secret-key-here-use-openssl-rand-hex-32
SECRET_KEY=another-secret-key-for-sessions
ALLOWED_ORIGINS=https://codexdominion.app,https://www.codexdominion.app,https://api.codexdominion.app

# Optional: API Keys (if needed)
GITHUB_TOKEN=your_github_token_if_needed
OPENAI_API_KEY=your_openai_key_if_needed

# Logging
LOG_LEVEL=INFO
```

Set proper permissions:
```bash
sudo chown www-data:www-data /var/www/codexdominion.app/.env.production
sudo chmod 600 /var/www/codexdominion.app/.env.production
```

### 7️⃣ Install Systemd Service

```bash
# Copy service file from your uploaded files or create it
sudo nano /etc/systemd/system/codexdominion-api.service
```

Paste the content from `codexdominion-api.service`, then:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable codexdominion-api

# Start the service
sudo systemctl start codexdominion-api

# Check status
sudo systemctl status codexdominion-api
```

### 8️⃣ Configure Nginx

```bash
# Copy nginx configuration
sudo nano /etc/nginx/sites-available/codexdominion.app
```

Paste the content from `nginx-codexdominion.conf`, then:

```bash
# Test nginx configuration
sudo nginx -t

# Enable site
sudo ln -s /etc/nginx/sites-available/codexdominion.app /etc/nginx/sites-enabled/

# Remove default site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Restart nginx
sudo systemctl restart nginx
```

### 9️⃣ SSL Certificate with Let's Encrypt

```bash
# Install certbot (if not already installed)
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d codexdominion.app -d www.codexdominion.app -d api.codexdominion.app

# Follow the prompts - select option 2 for redirect HTTP to HTTPS

# Test auto-renewal
sudo certbot renew --dry-run
```

### 🔟 DNS Configuration

In your IONOS domain control panel for **codexdominion.app**:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | YOUR_IONOS_SERVER_IP | 3600 |
| A | www | YOUR_IONOS_SERVER_IP | 3600 |
| A | api | YOUR_IONOS_SERVER_IP | 3600 |
| CNAME | www | codexdominion.app | 3600 |

Wait 5-30 minutes for DNS propagation.

## Verification

### Test Backend API

```bash
# On server
curl http://localhost:8000/health

# From internet (after DNS propagates)
curl https://api.codexdominion.app/health
```

### Test Frontend

```bash
# From internet
curl https://codexdominion.app
```

### Check Logs

```bash
# API logs
sudo journalctl -u codexdominion-api -f

# Nginx logs
sudo tail -f /var/log/nginx/codexdominion-access.log
sudo tail -f /var/log/nginx/codexdominion-error.log

# Application logs
sudo tail -f /var/log/codexdominion/api.log
```

## Troubleshooting

### Service won't start

```bash
# Check service status
sudo systemctl status codexdominion-api

# Check Python path
sudo -u www-data /var/www/codexdominion.app/.venv/bin/python --version

# Test uvicorn manually
sudo -u www-data /var/www/codexdominion.app/.venv/bin/uvicorn src.backend.main:app --host 0.0.0.0 --port 8000
```

### Nginx errors

```bash
# Test configuration
sudo nginx -t

# Check error logs
sudo tail -100 /var/log/nginx/error.log
```

### Database connection issues

```bash
# Test database connection
sudo -u www-data psql -h localhost -U codexdominion_user -d codexdominion -c "SELECT version();"
```

### Permission issues

```bash
# Fix permissions
sudo chown -R www-data:www-data /var/www/codexdominion.app
sudo chmod -R 755 /var/www/codexdominion.app
sudo chmod 600 /var/www/codexdominion.app/.env.production
```

## Maintenance Commands

### Update Deployment

```bash
# Backup current version
sudo tar -czf /var/backups/codexdominion/backup_$(date +%Y%m%d_%H%M%S).tar.gz -C /var/www/codexdominion.app .

# Upload and extract new version
# (repeat steps 2-4)

# Restart services
sudo systemctl restart codexdominion-api
sudo systemctl reload nginx
```

### View Service Status

```bash
sudo systemctl status codexdominion-api
sudo systemctl status nginx
```

### Restart Services

```bash
sudo systemctl restart codexdominion-api
sudo systemctl restart nginx
```

### Monitor Resources

```bash
# CPU and memory
htop

# Disk space
df -h

# Service resource usage
systemctl status codexdominion-api
```

## Security Checklist

- ✅ SSL/TLS enabled with Let's Encrypt
- ✅ Firewall configured (ufw or iptables)
- ✅ SSH key authentication (disable password auth)
- ✅ Environment variables secured (600 permissions)
- ✅ Database password is strong
- ✅ JWT secret is cryptographically secure
- ✅ Nginx rate limiting configured
- ✅ Security headers enabled
- ✅ Log files properly secured

## Firewall Setup (Optional but Recommended)

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check status
sudo ufw status
```

## Monitoring Setup (Optional)

Install monitoring tools:

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs -y

# View real-time logs
sudo journalctl -u codexdominion-api -f
```

## Backup Strategy

Create automated backups:

```bash
# Create backup script
sudo nano /usr/local/bin/backup-codexdominion.sh
```

Add:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/codexdominion"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Backup application
tar -czf $BACKUP_DIR/app_$TIMESTAMP.tar.gz -C /var/www/codexdominion.app .

# Backup database
sudo -u postgres pg_dump codexdominion > $BACKUP_DIR/db_$TIMESTAMP.sql

# Keep only last 7 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
```

Make executable:
```bash
sudo chmod +x /usr/local/bin/backup-codexdominion.sh

# Add to crontab (daily at 2 AM)
echo "0 2 * * * /usr/local/bin/backup-codexdominion.sh" | sudo crontab -
```

---

## 🔥 Your Site is Live! 🔥

**URLs:**
- 🌐 Frontend: https://codexdominion.app
- 🔌 API: https://api.codexdominion.app
- 📊 Health Check: https://api.codexdominion.app/health

**Next Steps:**
1. Monitor logs for first 24 hours
2. Set up automated backups
3. Configure monitoring/alerting
4. Test all features in production
5. Share with users!

✨ **CodexDominion.app is now eternal!** ✨
