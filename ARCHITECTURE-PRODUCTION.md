# Production Architecture - Codex Dominion E-Commerce Platform

This document replaces the previous constellation architecture with the production-ready e-commerce system.

## System Overview

Codex Dominion is a modern JAMstack e-commerce platform selling Christian printables, homeschool resources, and wedding planning materials through a headless WordPress/WooCommerce backend with Next.js frontend.

**See detailed architecture diagrams, data flows, and technical specifications in:**
- `README.md` - Quick start guide
- `playbooks/runbooks/deployment.md` - Deployment procedures
- `playbooks/incidents/outage-response.md` - Incident response
- `playbooks/rollouts/go-live-checklist.md` - Launch checklist

## Technology Stack

### Frontend
- Next.js 14 with TypeScript
- React 18
- Tailwind CSS
- WooCommerce REST API client

### Backend
- WordPress 6.x + WooCommerce 8.x
- Express.js API for webhooks
- Custom WordPress plugins (3)

### Database
- MariaDB 11 (WordPress/WooCommerce)
- Redis 7 (sessions, cache)
- PostgreSQL 15 (future: user entitlements)

### Infrastructure
- Docker Compose (local + staging)
- Kubernetes (production)
- nginx (reverse proxy, SSL)
- Certbot (SSL certificates)

### Monitoring
- Prometheus (metrics collection)
- Grafana (dashboards)
- Grafana Faro (RUM)
- Google Analytics 4

### CI/CD
- GitHub Actions
- Automated build, test, deploy
- Rollback capability

## Directory Structure

```
codexdominion/
├─ infra/            # Infrastructure & DevOps
├─ web/              # Next.js storefront
├─ api/              # REST/Webhooks (Express)
├─ wordpress-plugin/ # Auto-bundles, subscriptions, schema helpers
├─ apps/             # Flutter/React Native (future)
├─ content/          # Launch assets, lead magnets, emails
├─ playbooks/        # Runbooks, incident response, rollout plans
└─ README.md         # Main documentation
```

## Quick Start

```bash
# Start infrastructure
cd infra/docker
docker-compose up -d

# Access services
# WordPress: http://localhost:8080
# API: http://localhost:4000
# Web: http://localhost:3000
# Grafana: http://localhost:3001
```

**Full setup instructions:** See `README.md`

## Key Features

- 6 product niches (Kids Bible, Homeschool, Wedding, etc.)
- 10 auto-generated product bundles
- 5 subscription plans ($7.99-$19.99/month)
- 4 lead magnets with email capture
- Social media automation (6 platforms)
- Analytics dashboard (10 metrics panels)
- Webhook-based subscription management
- Real-time notifications

## Production Status

**90% Complete**

Remaining:
- WordPress initial setup + WooCommerce installation
- Webhook configuration (7 webhooks)
- Database schema for entitlements
- Shop pages (category, product detail)
- Media assets (product photos, social graphics)

## Deployment

**Production Server:** IONOS VPS 74.208.123.158

Deploy command:
```bash
cd infra/docker
./deploy-complete-system.sh
```

**See full deployment guide:** `playbooks/runbooks/deployment.md`

## Monitoring

- **Grafana:** https://codexdominion.app/grafana
- **Prometheus:** http://74.208.123.158:9090
- **API Health:** https://api.codexdominion.app/health
- **WordPress Admin:** https://codexdominion.app/wp-admin

## Support

- Email: support@codexdominion.app
- Documentation: `README.md`, `playbooks/`
- Emergency: See `playbooks/incidents/outage-response.md`

---

**Last Updated:** December 6, 2025
**Version:** 1.0.0 (Production Ready)
