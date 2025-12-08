# CodexDominion Production Deployment Guide

## System Status ✅

### Completed
- ✅ Main domain: https://codexdominion.app (SSL configured, expires March 5, 2026)
- ✅ Frontend build: Successfully compiled (54 pages)
- ✅ TypeScript: All errors resolved
- ✅ Nginx: Configured and running
- ✅ Server: IONOS Ubuntu 24.04 at 74.208.123.158

### Pending
- ⏳ Subdomain DNS records (api, dashboard, monitoring)
- ⏳ Subdomain SSL certificates
- ⏳ Backend API deployment
- ⏳ Dashboard service deployment
- ⏳ Monitoring service deployment

## Quick Deployment Steps

### 1. Add Subdomain DNS Records

Add these A records in your DNS provider:

| Type | Name       | Value           | TTL  |
|------|------------|-----------------|------|
| A    | api        | 74.208.123.158  | 3600 |
| A    | dashboard  | 74.208.123.158  | 3600 |
| A    | monitoring | 74.208.123.158  | 3600 |

### 2. Deploy Subdomain Configurations

```bash
# SSH into server
ssh root@74.208.123.158

# Upload deployment script
# (from your local machine)
scp deploy-subdomains.sh root@74.208.123.158:~/

# Run on server
chmod +x deploy-subdomains.sh
./deploy-subdomains.sh
```

### 3. Deploy Frontend to Production

```bash
# Build frontend with production config
cd frontend
npm run build

# Deploy to server
npm run export  # If using static export
# OR
# Configure PM2 or systemd service for Next.js server
```

### 4. Deploy Backend Services

```bash
# On server, set up Python environment
cd /var/www/codexdominion.app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run API service (example with uvicorn)
uvicorn main:app --host 127.0.0.1 --port 8000 --workers 4

# Set up systemd service for auto-start
```

## Service Port Mapping

| Service    | Port | Domain                            | Purpose              |
|------------|------|-----------------------------------|----------------------|
| Frontend   | 3000 | https://codexdominion.app         | Main web app         |
| Frontend   | 3000 | https://www.codexdominion.app     | WWW redirect         |
| API        | 8000 | https://api.codexdominion.app     | REST API             |
| Dashboard  | 8501 | https://dashboard.codexdominion.app | Analytics/Admin    |
| Monitoring | 9090 | https://monitoring.codexdominion.app | Metrics/Health    |

## Nginx Configuration Summary

### Main Site
- Config: `/etc/nginx/sites-available/codexdominion.app`
- SSL: `/etc/letsencrypt/live/codexdominion.app/`
- Proxy: `localhost:3000`

### WWW Subdomain
- Config: `/etc/nginx/sites-enabled/www.codexdominion.app`
- SSL: `/etc/letsencrypt/live/www.codexdominion.app/`
- Proxy: `localhost:3000`

### API Subdomain (after deployment)
- Config: `/etc/nginx/sites-available/api.codexdominion.app`
- SSL: Will be created by certbot
- Proxy: `localhost:8000`

### Dashboard Subdomain (after deployment)
- Config: `/etc/nginx/sites-available/dashboard.codexdominion.app`
- SSL: Will be created by certbot
- Proxy: `localhost:8501`

### Monitoring Subdomain (after deployment)
- Config: `/etc/nginx/sites-available/monitoring.codexdominion.app`
- SSL: Will be created by certbot
- Proxy: `localhost:9090`

## Environment Variables

### Production (.env.production)
```bash
NEXT_PUBLIC_API_URL=https://api.codexdominion.app
NEXT_PUBLIC_DOMAIN=https://codexdominion.app
NEXT_PUBLIC_DASHBOARD_URL=https://dashboard.codexdominion.app
NEXT_PUBLIC_MONITORING_URL=https://monitoring.codexdominion.app
NODE_ENV=production
```

### Development (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_DOMAIN=http://localhost:3000
NODE_ENV=development
```

## Deployment Commands Cheat Sheet

### Frontend
```bash
# Build
cd frontend
npm run build

# Test production build locally
npm start

# Deploy to server (method 1: static export)
npm run export
scp -r out/* root@74.208.123.158:/var/www/codexdominion.app/

# Deploy to server (method 2: PM2)
pm2 start npm --name "codex-frontend" -- start
pm2 save
pm2 startup
```

### Backend API
```bash
# On server
cd /var/www/codexdominion.app/api
source venv/bin/activate

# Run with uvicorn
uvicorn main:app --host 127.0.0.1 --port 8000

# Or with gunicorn
gunicorn main:app --workers 4 --bind 127.0.0.1:8000
```

### Check Service Status
```bash
# Nginx
systemctl status nginx
nginx -t

# SSL Certificates
certbot certificates

# Port usage
netstat -tlnp | grep -E ':(3000|8000|8501|9090)'

# Logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
tail -f /var/log/letsencrypt/letsencrypt.log
```

## Verification Checklist

- [ ] DNS records resolve for all domains
- [ ] All domains return 200 OK
- [ ] SSL certificates are valid (no browser warnings)
- [ ] API endpoints respond correctly
- [ ] Frontend can communicate with API
- [ ] Dashboard loads and displays data
- [ ] Monitoring displays system metrics
- [ ] All services auto-start on reboot
- [ ] Logs are being generated
- [ ] Backups are configured

## Security Checklist

- [x] SSL/TLS enabled on all domains
- [x] Auto-renewal configured for certificates
- [ ] Firewall configured (ufw/iptables)
- [ ] SSH key authentication only (disable password)
- [ ] Fail2ban installed and configured
- [ ] Regular security updates enabled
- [ ] API rate limiting configured
- [ ] CORS properly configured
- [ ] Environment variables secured
- [ ] Database connections encrypted

## Monitoring

### Health Check URLs
- Frontend: `https://codexdominion.app/api/health`
- API: `https://api.codexdominion.app/health`
- Dashboard: `https://dashboard.codexdominion.app/health`

### Metrics
- Monitor: `https://monitoring.codexdominion.app`
- Logs: `/var/log/codexdominion/`

## Backup Strategy

```bash
# Database backup
pg_dump codex_dominion > backup_$(date +%Y%m%d).sql

# Code backup
tar -czf codex_backup_$(date +%Y%m%d).tar.gz /var/www/codexdominion.app

# Nginx configs
tar -czf nginx_backup_$(date +%Y%m%d).tar.gz /etc/nginx/sites-*

# SSL certificates
tar -czf ssl_backup_$(date +%Y%m%d).tar.gz /etc/letsencrypt
```

## Troubleshooting

### Site not loading
1. Check DNS: `nslookup codexdominion.app`
2. Check nginx: `systemctl status nginx`
3. Check service: `curl http://localhost:3000`
4. Check logs: `tail -f /var/log/nginx/error.log`

### SSL certificate issues
1. Check certificate: `certbot certificates`
2. Test renewal: `certbot renew --dry-run`
3. Check renewal timer: `systemctl status certbot.timer`

### API not responding
1. Check if running: `netstat -tlnp | grep :8000`
2. Check logs: Service-specific log location
3. Test locally: `curl http://localhost:8000/health`
4. Check nginx proxy: `nginx -t`

## Next Steps

1. **Add subdomain DNS records** - Do this first!
2. **Run deploy-subdomains.sh** - After DNS propagates
3. **Deploy backend API** - Set up Python/FastAPI service
4. **Deploy dashboard** - Set up Streamlit/dashboard service
5. **Set up monitoring** - Configure Prometheus/Grafana
6. **Configure backups** - Automate daily backups
7. **Set up CI/CD** - GitHub Actions for auto-deployment
8. **Load testing** - Verify performance under load

## Support

- Documentation: `/docs` directory
- Logs: `/var/log/codexdominion/`
- Configuration: `/etc/codexdominion/`
- Issues: GitHub repository issues

---

**System Status**: Production Ready (Partial)
**Last Updated**: December 5, 2025
**Next Review**: After subdomain deployment
