# Codex Dominion - Canary Deployment Guide

## Overview

This guide covers the progressive canary deployment strategy for Codex Dominion, ensuring safe rollouts with automated health checks and instant rollback capabilities.

---

## 🎯 Deployment Strategy

### Progressive Traffic Shifting

```
1% → 5% → 20% → 100%
10m   20m   30m   continuous
```

Each phase includes automated validation before proceeding to the next.

---

## 📦 Scope Definition

### Frontend Services
- **Next.js Application** (Port 3000)
- **Static Assets** (CDN/local)
- **Client API Routes** (`/api/client/*`)

**Affected Modules:**
- `frontend/pages/**`
- `frontend/components/**`
- `frontend/api/**`

### Backend Services
- **FastAPI Core** (Port 8001)
- **Uvicorn Workers** (4 workers)
- **API Endpoints** (`/api/v1/*`)

**Affected Modules:**
- `src/backend/api/**`
- `src/backend/services/**`
- `src/backend/models/**`

### High-Risk Modules (Require Council Approval)

| Module | Risk Level | Approval Required | Additional Checks |
|--------|-----------|-------------------|-------------------|
| `src/backend/auth/**` | 🔴 Critical | Council:2 | Security audit |
| `src/backend/payments/**` | 🔴 Critical | Council:2 | PCI compliance + fraud detection |
| `src/backend/avatars/**` | 🔴 Critical | Council:2 | Privacy review |
| `**/migrations/**` | 🔴 Critical | Council:2 | Rollback plan required |

---

## 📊 Traffic Routing

### Header-Based Routing (Testing)
```bash
# Route specific requests to canary
curl -H "X-Canary-Version: v2" https://codexdominion.app/api/endpoint
```

### Percentage-Based Routing (Production)
- **Algorithm:** Weighted round-robin
- **Sticky Sessions:** Enabled (24h)
- **Cookie:** `codex-canary-id`

### User Segment Routing

| Segment | Traffic % | Criteria |
|---------|-----------|----------|
| Internal Team | 100% | `@jermaineMerritt`, `@team-members` |
| Beta Testers | 100% | `user.beta_tester == true` |
| Premium Users | 50% | `user.subscription_tier == 'premium'` |
| General Users | Progressive | Phase-based (1% → 100%) |

---

## 📈 Metrics Collection

### Latency Monitoring

| Percentile | Warning | Critical | Governance Threshold |
|-----------|---------|----------|---------------------|
| p50 | 100ms | 200ms | - |
| p95 | 250ms | **300ms** | **300ms** ⚠️ |
| p99 | 400ms | 500ms | - |

**Acceptable Degradation:** 10% from baseline
**Comparison:** Real-time vs. stable version

### Error Rate Monitoring

| Window | Warning | Critical | Governance Threshold |
|--------|---------|----------|---------------------|
| 5m | 1.0% | **5.0%** | **5.0%** ⚠️ |
| 15m | 1.0% | 5.0% | - |
| 1h | 1.0% | 5.0% | - |
| 24h | 1.0% | **5.0%** | **5.0%** ⚠️ |

**By Status Code:**
- **4xx:** Warning 2.0%, Critical 5.0%
- **5xx:** Warning 0.5%, Critical 2.0%

### Conversion Rate Monitoring

Critical paths with baseline targets:

```yaml
/checkout:
  baseline: 85.5%
  min_acceptable: 80.0%

/signup:
  baseline: 65.0%
  min_acceptable: 60.0%

/api/payments/process:
  baseline: 99.5%
  min_acceptable: 98.0%
```

**Alert Threshold:** -2% warning, -5% critical

### Margin Impact Monitoring

**Metrics Tracked:**
- Average order value
- Payment success rate
- Refund rate
- Processing cost per transaction

**Thresholds:** -3% warning, -5% critical
**Stakeholders:** @finance-team, @council-stewards

### System Health

| Metric | Warning | Critical |
|--------|---------|----------|
| CPU Usage | 70% | 85% |
| Memory Usage | 75% | 90% |
| Disk I/O | 80% | 95% |
| DB Connections | 80% | 95% |
| Queue Depth | 1000 | 5000 |

---

## 🚨 Abort Conditions

### Automatic Rollback Triggers

| Condition | Duration | Action |
|-----------|----------|--------|
| Error rate ≥ 5% | 5m | Immediate rollback |
| p95 latency > 300ms | 10m | Immediate rollback |
| Conversion rate drop ≥ 5% | 15m | Immediate rollback |
| 5xx errors ≥ 2% | 5m | Immediate rollback |
| DB connection pool ≥ 95% | 3m | Immediate rollback |
| Memory usage ≥ 90% | 5m | Immediate rollback |

### Manual Kill Switch

**Authorized Roles:**
- Council members
- Platform stewards
- Ops guardians

**Procedure:**
```bash
# Authenticate
export KILL_SWITCH_TOKEN="your-bearer-token"

# Execute kill switch (requires confirmation)
curl -X POST https://api.codexdominion.app/ops/canary/abort \
  -H "Authorization: Bearer $KILL_SWITCH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "High error rate detected",
    "confirmed": true,
    "operator": "@jermaineMerritt"
  }'
```

**Audit Trail:** All kill switch actions are logged immutably.

### Business Rule Triggers

| Condition | Duration | Action | Stakeholders |
|-----------|----------|--------|--------------|
| Payment failure rate > 1% | 10m | Pause & alert | @payments-team, @council-stewards |
| Customer complaints > 10 | 1h | Pause & review | @customer-success, @council-stewards |

---

## 🔄 Rollback Procedure

### Instant Rollback (Default)

**Steps:**
1. Route all traffic to stable version (30s timeout)
2. Stop canary pods (1m timeout)
3. Clear canary cache (30s timeout)
4. Notify on-call team (Slack + PagerDuty)
5. Create incident report (auto-generated)

**Total Time:** ~2 minutes

### Gradual Rollback (Optional)

If instant rollback not suitable:
```
20% → 10% → 5% → 1% → 0%
 5m    5m    5m   5m   immediate
```

### Verification

After rollback:
- **Wait period:** 10 minutes
- **Check metrics:**
  - Error rate < 1%
  - p95 latency < 250ms
  - No active incidents

### Post-Rollback Actions (Required within 24h)

1. ✅ Root cause analysis
2. ✅ Incident postmortem
3. ✅ Update runbook
4. ✅ Communicate to team
5. ✅ Update governance documentation

---

## 🏥 Health Checks

### Startup Probe
- **Endpoint:** `/health/startup`
- **Initial Delay:** 10s
- **Period:** 5s
- **Timeout:** 3s
- **Failure Threshold:** 3

### Liveness Probe
- **Endpoint:** `/health/live`
- **Period:** 10s
- **Timeout:** 5s
- **Failure Threshold:** 3

### Readiness Probe
- **Endpoint:** `/health/ready`
- **Period:** 5s
- **Timeout:** 3s
- **Failure Threshold:** 2
- **Success Threshold:** 2

### Custom Health Checks

| Check | Endpoint | Critical |
|-------|----------|----------|
| Database Connectivity | `/health/db` | ✅ Yes |
| External API | `/health/external` | ❌ No |
| Cache Availability | `/health/cache` | ❌ No |
| Payment Gateway | `/health/payments` | ✅ Yes |

---

## 📢 Customer Communications

### When Notice is Required

- ✅ Breaking changes
- ✅ UI redesign
- ✅ Feature deprecation
- ✅ Performance degradation (expected)

### When Notice is NOT Required

- ❌ Bug fixes
- ❌ Performance improvements
- ❌ Internal refactoring
- ❌ Security patches (unless user action needed)

### Communication Templates

#### Scheduled Maintenance
```
Subject: Scheduled System Maintenance

We're deploying improvements to enhance your experience.
You may notice brief performance fluctuations.
No action required on your part.

Time: [DATE] [TIME] [TIMEZONE]
Duration: ~2 hours
Impact: Minimal

Status updates: https://status.codexdominion.app
```

**Channels:** Email + In-app notification
**Advance Notice:** 24 hours

#### Feature Rollout
```
Subject: New Feature Available

We're gradually rolling out [FEATURE_NAME] to all users.
You may see this feature appear in the coming hours.

Learn more: [BLOG_POST_URL]
```

**Channels:** In-app + Blog post
**Advance Notice:** 1 hour

#### Incident Notification
```
Subject: Service Degradation Detected

We've detected an issue and are working to resolve it.
Your data is safe. Updates will be posted every 30 minutes.

Current status: [STATUS]
Affected services: [SERVICES]

Real-time updates: https://status.codexdominion.app
```

**Channels:** Status page + Twitter + Email
**Timing:** Immediate

### Status Page

**URL:** https://status.codexdominion.app
**Auto-Update:** Every 5 minutes

**Components:**
- Frontend Application
- Backend API
- Payment Processing
- Database
- Authentication

---

## ✅ Pre-Deployment Checklist

### Required Approvals by Tier

#### Low Tier
- [ ] CI tests pass
- [ ] Lint checks pass

#### Medium Tier
- [ ] CI tests pass
- [ ] Integration tests pass
- [ ] Security scan pass
- [ ] Steward approval

#### High Tier
- [ ] CI tests pass
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] Security scan pass
- [ ] Compliance review complete
- [ ] Council approval (2 members)
- [ ] Rollback plan documented

### Infrastructure Readiness
- [ ] Canary environment ready
- [ ] Monitoring dashboards configured
- [ ] Alert rules active
- [ ] Rollback procedure tested
- [ ] On-call engineer notified

### Communications
- [ ] Stakeholders notified
- [ ] Status page updated
- [ ] Customer notice sent (if required)

### Backups
- [ ] Database backup verified
- [ ] Configuration backup created
- [ ] Artifact registry snapshot taken

---

## 🧪 Post-Deployment Validation

### Smoke Tests (Automated)

```bash
# Homepage loads
curl -f https://codexdominion.app

# API health check
curl -f https://api.codexdominion.app/health

# Authentication flow
curl -f -H "Authorization: Bearer $TOKEN" \
  https://api.codexdominion.app/auth/verify

# Payment gateway connection
curl -f https://api.codexdominion.app/payments/status
```

### Functional Tests
- User signup flow
- User login flow
- Checkout process
- Avatar management
- API token generation

### Performance Validation (30 minutes)
- p95 latency ≤ baseline + 10%
- Error rate ≤ 0.5%
- Throughput ≥ baseline - 5%

### Monitoring Period (2 hours)
- Check intervals: Every 5 minutes
- Auto-promote if healthy: Yes

---

## 📊 Observability Integration

### Tracing
- **Enabled:** Yes
- **Sample Rate:** 100% during canary
- **Retention:** 7 days
- **Tools:** Jaeger, OpenTelemetry

### Logging
- **Level:** INFO (stable), DEBUG (canary)
- **Structured:** Yes
- **Include Trace ID:** Yes

### Dashboards

#### Canary Overview
**URL:** https://grafana.codexdominion.app/d/canary

**Panels:**
- Traffic Distribution (stable vs. canary)
- Error Rate Comparison
- Latency Percentiles (p50, p95, p99)
- Conversion Funnel

#### Business Metrics
**URL:** https://grafana.codexdominion.app/d/business

**Panels:**
- Revenue per User
- Payment Success Rate
- Customer Satisfaction Score
- Margin Impact

### Alert Channels

| Channel | Purpose | Configuration |
|---------|---------|---------------|
| Slack | Team notifications | `#codex-alerts` |
| PagerDuty | Critical incidents | On-call rotation |
| Email | Stakeholder updates | `oncall@codexdominion.app` |

---

## 🎬 Deployment Commands

### Start Canary Deployment

```bash
# Deploy to canary environment
./deploy-canary.sh --version v2.1.0 --tier medium

# Or use PowerShell
.\deploy-canary.ps1 -Version "v2.1.0" -Tier "medium"
```

### Monitor Canary Progress

```bash
# Watch metrics in real-time
./monitor-canary.sh --version v2.1.0

# Check specific metric
curl https://api.codexdominion.app/ops/canary/metrics?version=v2.1.0
```

### Promote Canary to Stable

```bash
# Auto-promote after validation passes
./promote-canary.sh --version v2.1.0 --auto

# Manual promotion (requires confirmation)
./promote-canary.sh --version v2.1.0 --manual --approver @jermaineMerritt
```

### Abort Canary Deployment

```bash
# Immediate rollback
./abort-canary.sh --version v2.1.0 --reason "High error rate"

# Or use kill switch API
curl -X POST https://api.codexdominion.app/ops/canary/abort \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"version": "v2.1.0", "reason": "High error rate", "confirmed": true}'
```

---

## 🏆 Best Practices

### Before Deployment
1. **Test in staging** - Full canary flow in staging environment
2. **Document changes** - Clear changelog and release notes
3. **Notify stakeholders** - 24h advance notice for high-tier
4. **Review rollback plan** - Ensure rollback tested and ready

### During Deployment
1. **Monitor actively** - Watch dashboards during each phase
2. **Check business metrics** - Not just technical metrics
3. **Listen to customers** - Monitor support channels
4. **Stay available** - On-call team ready to respond

### After Deployment
1. **Validate thoroughly** - Run full test suite
2. **Monitor extended period** - 2h minimum observation
3. **Document learnings** - Update runbooks
4. **Communicate success** - Thank team and stakeholders

### For High-Risk Modules
1. **Double approval** - 2 council members required
2. **Extended monitoring** - 4h observation minimum
3. **Slower rollout** - Consider 1% → 2% → 5% → 10% → 20%
4. **Business validation** - Finance/legal team sign-off

---

## 📚 Additional Resources

- [Governance Documentation](./.governance.yml)
- [Deployment Fixed Guide](../DEPLOYMENT_FIXED.md)
- [System Efficiency Report](../SYSTEM_EFFICIENCY_REPORT.md)
- [Grafana Dashboards](https://grafana.codexdominion.app)
- [Status Page](https://status.codexdominion.app)

---

**Version:** 1.0
**Last Updated:** 2025-12-04
**Owner:** Platform Stewards
**Reviewers:** Council Stewards
