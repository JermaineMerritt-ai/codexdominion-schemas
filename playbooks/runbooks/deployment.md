# Deployment Runbook

## Overview
Standard operating procedure for deploying Codex Dominion to production.

## Pre-Deployment Checklist

### 1. Code Quality
- [ ] All tests passing (`npm test` in web/ and api/)
- [ ] No linting errors (`npm run lint`)
- [ ] TypeScript compilation successful (`npm run build`)
- [ ] Dependencies updated and audited (`npm audit`)
- [ ] Git branch up to date with `main`

### 2. Environment Configuration
- [ ] `.env` files configured for production
- [ ] Database connection string validated
- [ ] WooCommerce API keys confirmed working
- [ ] Webhook secrets match between WooCommerce and API
- [ ] SSL certificates valid (check expiry: `certbot certificates`)

### 3. Database
- [ ] Backup created: `cd infra/docker && ./backup.sh`
- [ ] Backup verified: `ls -lh backups/`
- [ ] Migration scripts ready (if schema changes)

### 4. Monitoring
- [ ] Grafana dashboards loading
- [ ] Prometheus targets all healthy
- [ ] Alert rules configured
- [ ] On-call engineer notified

## Deployment Methods

### Method 1: GitHub Actions (Recommended)

1. **Trigger Deployment**
   ```bash
   git checkout main
   git pull origin main
   git push origin main  # Push triggers CI/CD
   ```

2. **Monitor Pipeline**
   - Visit https://github.com/JermaineMerritt-ai/codexdominion-schemas/actions
   - Watch build, test, and deploy stages
   - Check for green checkmarks

3. **Verify Deployment**
   ```bash
   # Check Kubernetes rollout status
   kubectl rollout status deployment/web-deployment
   kubectl rollout status deployment/api-deployment
   ```

4. **Smoke Tests**
   - Homepage loads: https://codexdominion.app
   - API health: https://api.codexdominion.app/health
   - WordPress admin: https://codexdominion.app/wp-admin
   - Test checkout flow
   - Test webhook delivery

### Method 2: Manual Docker Compose

1. **SSH to Server**
   ```bash
   ssh root@74.208.123.158
   cd /root/codex-dominion
   ```

2. **Pull Latest Code**
   ```bash
   git pull origin main
   ```

3. **Rebuild Containers**
   ```bash
   docker-compose build --no-cache web api
   docker-compose up -d
   ```

4. **Check Container Health**
   ```bash
   docker-compose ps
   docker logs codex-web --tail 50
   docker logs codex-api --tail 50
   ```

### Method 3: Kubernetes Manual

1. **Build & Push Images**
   ```bash
   # Web
   cd web
   docker build -t codexdominion/web:v1.2.0 .
   docker push codexdominion/web:v1.2.0

   # API
   cd api
   docker build -t codexdominion/api:v1.2.0 .
   docker push codexdominion/api:v1.2.0
   ```

2. **Update Kubernetes**
   ```bash
   kubectl set image deployment/web-deployment web=codexdominion/web:v1.2.0
   kubectl set image deployment/api-deployment api=codexdominion/api:v1.2.0
   ```

3. **Watch Rollout**
   ```bash
   kubectl rollout status deployment/web-deployment
   kubectl rollout status deployment/api-deployment
   ```

## Post-Deployment Verification

### 1. Functional Tests
- [ ] Homepage renders correctly
- [ ] Product pages load
- [ ] Add to cart works
- [ ] Checkout flow completes
- [ ] User can subscribe
- [ ] Lead magnet download works

### 2. API Tests
```bash
# Health check
curl https://api.codexdominion.app/health

# Webhook endpoint
curl https://api.codexdominion.app/webhooks/health

# Test subscription webhook (use WooCommerce test delivery)
```

### 3. Monitoring Checks
- [ ] Grafana showing live data
- [ ] Prometheus scraping all targets
- [ ] No error spikes in logs
- [ ] Response times normal (<500ms p95)
- [ ] Database connections healthy

### 4. WordPress Checks
- [ ] Can log in to wp-admin
- [ ] WooCommerce dashboard loading
- [ ] Products visible in storefront
- [ ] Orders processing correctly

## Rollback Procedure

### If Deployment Fails:

**Kubernetes Rollback:**
```bash
kubectl rollout undo deployment/web-deployment
kubectl rollout undo deployment/api-deployment
kubectl rollout status deployment/web-deployment
```

**Docker Compose Rollback:**
```bash
# SSH to server
ssh root@74.208.123.158

# Check previous images
docker images codexdominion/web
docker images codexdominion/api

# Edit docker-compose.yml to use previous tag
nano docker-compose.yml

# Redeploy
docker-compose down
docker-compose up -d

# Verify
docker-compose ps
```

**Database Rollback:**
```bash
# Restore from backup
docker exec -i codex-db mariadb -u root -proot_pass codex_db < backups/codex_db_2025-12-06_14-30-00.sql

# Verify restore
docker exec -it codex-db mariadb -u root -proot_pass -e "USE codex_db; SHOW TABLES;"
```

## Troubleshooting

### Issue: Containers not starting
```bash
# Check logs
docker logs codex-web
docker logs codex-api

# Check disk space
df -h

# Check memory
free -m

# Restart container
docker-compose restart web api
```

### Issue: Database connection failed
```bash
# Test database
docker exec -it codex-db mariadb -u root -proot_pass -e "SELECT 1"

# Check credentials in .env
cat .env | grep DATABASE

# Restart database
docker-compose restart db
```

### Issue: 502 Bad Gateway
```bash
# Check nginx
docker logs codex-nginx

# Check upstream services
docker-compose ps

# Restart nginx
docker-compose restart nginx
```

### Issue: Webhooks not firing
1. Check WooCommerce webhook status (should be "Active")
2. View delivery logs in WooCommerce admin
3. Verify API endpoint accessible: `curl https://api.codexdominion.app/webhooks/health`
4. Check webhook secret matches: `cat api/.env | grep WC_WEBHOOK_SECRET`
5. Test manual delivery from WooCommerce admin

## Performance Optimization

### After Deployment:

1. **Clear Caches**
   ```bash
   # Next.js cache
   curl -X POST https://codexdominion.app/api/revalidate?secret=your_secret

   # WordPress object cache
   docker exec -it codex-wordpress wp cache flush

   # Redis cache
   docker exec -it codex-redis redis-cli FLUSHALL
   ```

2. **Warm Up Cache**
   ```bash
   # Visit key pages
   curl https://codexdominion.app
   curl https://codexdominion.app/shop
   curl https://codexdominion.app/subscriptions
   ```

3. **Monitor Metrics**
   - Check Grafana for response time spikes
   - Watch Prometheus for error rates
   - Monitor database slow query log

## Communication

### Notify Stakeholders:
- [ ] Post in #deployments Slack channel
- [ ] Update status page (if applicable)
- [ ] Email customers if downtime expected
- [ ] Document changes in changelog

### Deployment Message Template:
```
✅ Deployment Complete - v1.2.0

Changes:
- Added webhook handler for subscription management
- Improved checkout flow performance
- Fixed product image loading issue

Testing:
- All smoke tests passed
- No errors in monitoring
- Response times normal

Rollback plan: Ready if needed
Next monitoring check: 1 hour
```

## Scheduled Maintenance

### Best Times to Deploy:
- **Tuesday-Thursday:** 10am-2pm EST (low traffic)
- **Avoid:** Friday afternoons, weekends, holidays
- **Advance notice:** 48 hours for major changes

### Maintenance Window Template:
```
🔧 Scheduled Maintenance

When: Thursday, Dec 12, 2025 at 10:00 AM EST
Duration: 30 minutes
Impact: 5 minutes downtime expected
Reason: Database migration and feature deployment

We'll send an update when complete.
```

---

**Last Updated:** December 6, 2025
**Owner:** DevOps Team
**Review Frequency:** Monthly
