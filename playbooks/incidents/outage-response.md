# Incident Response - Service Outage

## Severity Levels

### P0 - Critical (Site Down)
- **Impact:** Complete site outage, no users can access
- **Response Time:** Immediate (< 5 minutes)
- **Examples:** Database crash, server offline, DNS failure

### P1 - High (Major Feature Down)
- **Impact:** Core functionality broken (checkout, subscriptions, API)
- **Response Time:** < 15 minutes
- **Examples:** Payment processing failure, webhook failures, auth issues

### P2 - Medium (Degraded Performance)
- **Impact:** Slow response times, intermittent errors
- **Response Time:** < 1 hour
- **Examples:** High server load, cache issues, CDN problems

### P3 - Low (Minor Issues)
- **Impact:** Non-critical features affected
- **Response Time:** < 4 hours
- **Examples:** Image loading issues, analytics gaps, minor UI bugs

## Immediate Response (First 15 Minutes)

### 1. Assess & Communicate
```bash
# Quick health check
curl https://codexdominion.app
curl https://api.codexdominion.app/health
docker-compose ps
```

**Post in #incidents channel:**
```
🚨 INCIDENT DETECTED - P0
Service: codexdominion.app
Symptom: Site unreachable
Time Detected: 2025-12-06 14:35 EST
Status: Investigating
Incident Commander: [Your Name]
```

### 2. Check Monitoring
- **Grafana:** https://codexdominion.app/grafana
  - Check error rate spike
  - Review response time graphs
  - Look for traffic anomalies

- **Prometheus:** http://74.208.123.158:9090
  - Query: `up{job="web"}` (should be 1)
  - Query: `rate(http_requests_total{status=~"5.."}[5m])` (error rate)

- **Server Resources:**
  ```bash
  ssh root@74.208.123.158
  top  # Check CPU usage
  df -h  # Check disk space
  free -m  # Check memory
  ```

### 3. Quick Fixes (Try First)

**Restart Services:**
```bash
docker-compose restart web api nginx
```

**Clear Caches:**
```bash
docker exec -it codex-redis redis-cli FLUSHALL
docker exec -it codex-wordpress wp cache flush
```

**Check Logs:**
```bash
docker logs codex-web --tail 200
docker logs codex-api --tail 200
docker logs codex-nginx --tail 100
docker logs codex-db --tail 100
```

## Root Cause Analysis

### Database Issues

**Symptoms:** 500 errors, "Connection refused", slow queries

**Diagnosis:**
```bash
# Check database status
docker exec -it codex-db mariadb -u root -proot_pass -e "SHOW PROCESSLIST;"

# Check connections
docker exec -it codex-db mariadb -u root -proot_pass -e "SHOW STATUS LIKE 'Threads_connected';"

# Check slow queries
docker exec -it codex-db cat /var/log/mysql/slow.log
```

**Fix:**
```bash
# Restart database
docker-compose restart db

# If corrupted table
docker exec -it codex-db mariadb -u root -proot_pass -e "USE codex_db; REPAIR TABLE wp_posts;"

# If out of connections
# Edit my.cnf to increase max_connections
```

### Server Resource Exhaustion

**Symptoms:** Slow response, containers crashing, OOM errors

**Diagnosis:**
```bash
# Check disk space (critical if > 90%)
df -h

# Check memory
free -m

# Check Docker stats
docker stats --no-stream

# Check processes
ps aux | sort -rn -k 3 | head -10  # Top CPU
ps aux | sort -rn -k 4 | head -10  # Top memory
```

**Fix:**
```bash
# Clean up disk space
docker system prune -a -f
rm -rf /root/codex-dominion/backups/*.sql  # Keep only recent

# Clean logs
truncate -s 0 /var/log/syslog
docker logs codex-web 2>&1 | tail -1000 > temp.log && cat temp.log > /dev/null

# Restart services
docker-compose restart
```

### Network/DNS Issues

**Symptoms:** Site unreachable, SSL errors, DNS resolution fails

**Diagnosis:**
```bash
# Check DNS
nslookup codexdominion.app
dig codexdominion.app

# Check SSL certificate
openssl s_client -connect codexdominion.app:443 -servername codexdominion.app

# Check nginx
docker exec -it codex-nginx nginx -t
docker logs codex-nginx
```

**Fix:**
```bash
# Restart nginx
docker-compose restart nginx

# Renew SSL if expired
certbot renew --nginx

# Check firewall
ufw status
```

### Application Errors

**Symptoms:** 500 errors, blank pages, JavaScript errors

**Diagnosis:**
```bash
# Check Next.js logs
docker logs codex-web --tail 500 | grep -i error

# Check API logs
docker logs codex-api --tail 500 | grep -i error

# Check WordPress errors
docker exec -it codex-wordpress cat /var/www/html/wp-content/debug.log
```

**Fix:**
```bash
# Rollback deployment (if recent deploy)
kubectl rollout undo deployment/web-deployment

# Rebuild containers
docker-compose build --no-cache web api
docker-compose up -d
```

### High Traffic / DDoS

**Symptoms:** Extreme traffic spike, repeated requests from single IPs

**Diagnosis:**
```bash
# Check nginx access logs
docker logs codex-nginx | awk '{print $1}' | sort | uniq -c | sort -rn | head -20

# Check traffic in Grafana
# Look for sudden request rate increase
```

**Fix:**
```bash
# Rate limit in nginx
# Edit nginx.conf to add:
# limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;

# Block specific IP
docker exec -it codex-nginx nginx -s reload

# Enable Cloudflare (if configured)
# Set security level to "I'm Under Attack"
```

## Recovery Procedures

### Restore from Backup

**Database:**
```bash
# List backups
ls -lh backups/

# Restore
docker exec -i codex-db mariadb -u root -proot_pass codex_db < backups/codex_db_2025-12-06_10-00-00.sql

# Verify
docker exec -it codex-db mariadb -u root -proot_pass -e "USE codex_db; SELECT COUNT(*) FROM wp_posts;"
```

**Files:**
```bash
# Restore WordPress uploads
tar -xzf backups/wp-uploads-2025-12-06.tar.gz -C /var/www/html/wp-content/uploads/
```

### Rollback Deployment
See `playbooks/runbooks/deployment.md` rollback section

## Communication Templates

### Status Update (Every 15 minutes)
```
UPDATE - [Time]
Status: [Investigating / Identified / Fixing / Monitoring]
Impact: [X users affected / X% error rate]
Progress: [What we've tried, what's next]
ETA: [Estimated resolution time]
```

### Resolution Notice
```
✅ INCIDENT RESOLVED - P0

Issue: Database connection failures
Duration: 14:35-15:12 EST (37 minutes)
Root Cause: Database ran out of connections (max_connections=100)
Fix: Increased max_connections to 300, restarted database
Prevention: Added monitoring alert for connection threshold

Impact: ~500 users affected, checkout unavailable
Apology: We sincerely apologize for the disruption

Next Steps:
- Post-mortem meeting scheduled for tomorrow 10am
- Database capacity planning review
- Improved monitoring alerts
```

## Post-Incident Checklist

- [ ] Document timeline in incident log
- [ ] Save relevant logs and metrics
- [ ] Schedule post-mortem meeting (within 48 hours)
- [ ] Write post-mortem report
- [ ] Implement preventive measures
- [ ] Update runbooks based on learnings
- [ ] Test incident response procedures

## Post-Mortem Template

```markdown
# Post-Mortem: [Incident Title]

## Summary
Brief description of what happened

## Timeline
- 14:35 - First alert received
- 14:40 - Incident confirmed, team notified
- 14:45 - Database identified as root cause
- 15:00 - Fix applied
- 15:12 - Incident resolved
- 15:30 - Monitoring confirmed stable

## Root Cause
Deep dive into what caused the issue

## Resolution
What we did to fix it

## Impact
- Users affected: ~500
- Revenue impact: $2,000 estimated
- Duration: 37 minutes

## What Went Well
- Quick detection via monitoring
- Fast team response
- Effective communication

## What Went Wrong
- No alerting for database connection threshold
- Backup restoration procedure not documented
- On-call engineer not immediately available

## Action Items
1. [ ] Add database connection monitoring (Owner: DevOps, Due: Dec 10)
2. [ ] Document backup restoration (Owner: DevOps, Due: Dec 8)
3. [ ] Improve on-call rotation (Owner: Manager, Due: Dec 15)
4. [ ] Add capacity planning for database (Owner: DevOps, Due: Dec 20)

## Lessons Learned
- Always monitor resource limits, not just errors
- Have runbooks ready before incidents happen
- Test backup restoration regularly
```

---

**Last Updated:** December 6, 2025
**Owner:** DevOps Team
**Review Frequency:** After each incident
