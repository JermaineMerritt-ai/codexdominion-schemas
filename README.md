# Codex Dominion - Production Launch Guide

## 🏗️ Architecture Overview

Modern JAMstack e-commerce platform with headless WordPress/WooCommerce backend, Next.js frontend, and microservices API.

```
codexdominion/
├─ infra/              # Infrastructure & DevOps
│  ├─ docker/          # Docker Compose, Prometheus, Grafana, nginx
│  ├─ k8s/             # Kubernetes manifests (deployments, services)
│  ├─ terraform/       # IaC for cloud resources (future)
│  └─ ci-cd/           # GitHub Actions workflows
│
├─ web/                # Next.js 14 Storefront
│  ├─ app/             # App router (pages, layouts)
│  ├─ components/      # React components (niches, lead magnets, analytics)
│  ├─ lib/             # WooCommerce API client, utilities
│  └─ public/          # Static assets
│
├─ api/                # Backend API Services
│  ├─ src/
│  │  ├─ webhooks/     # WooCommerce webhook handlers
│  │  ├─ routes/       # REST endpoints
│  │  └─ middleware/   # Auth, validation, logging
│  └─ docs/            # API documentation
│
├─ wordpress-plugin/   # Custom WP Plugins
│  ├─ auto-bundles/    # Automatic product bundling by tags
│  ├─ subscription-seeder/ # Seeds 5 subscription products
│  └─ schema-markup/   # SEO structured data (JSON-LD)
│
├─ apps/               # Mobile Applications
│  ├─ flutter/         # iOS/Android app (future)
│  └─ react-native/    # Cross-platform modules (future)
│
├─ content/            # Marketing & Launch Assets
│  ├─ launch-assets/   # Social media posts, campaigns
│  ├─ lead-magnets/    # Free downloadable products
│  └─ email-templates/ # Automated email sequences
│
├─ playbooks/          # Operations Documentation
│  ├─ runbooks/        # Standard procedures (deployment, backup)
│  ├─ incidents/       # Incident response guides
│  └─ rollouts/        # Feature rollout plans
│
└─ README.md           # This file
```

## 🚀 Quick Start - Local Development

### Prerequisites
- Docker Desktop + Docker Compose
- Node.js 18+ and npm/yarn
- Git

### 1. Clone Repository
```bash
git clone https://github.com/JermaineMerritt-ai/codexdominion-schemas.git
cd codex-dominion
```

### 2. Start Infrastructure
```bash
cd infra/docker
docker-compose up -d wordpress db redis nginx prometheus grafana
```

Access services:
- WordPress: http://localhost:8080
- API: http://localhost:4000
- Web: http://localhost:3000
- Grafana: http://localhost:3001 (admin/admin)
- Prometheus: http://localhost:9090

### 3. Configure WordPress
1. Visit http://localhost:8080 → Complete installation wizard
2. Install WooCommerce plugin
3. Copy plugins from `wordpress-plugin/` to `wp-content/plugins/`
4. Activate: Codex Auto Bundles, Subscription Seeder, Schema Markup
5. Generate WooCommerce REST API keys:
   - WP Admin → WooCommerce → Settings → Advanced → REST API → Add key
   - Copy Consumer Key and Secret

### 4. Configure Environment Variables

**web/.env.local:**
```env
WC_CONSUMER_KEY=ck_your_key_here
WC_CONSUMER_SECRET=cs_your_secret_here
WC_API_URL=http://localhost:8080/wp-json/wc/v3
NEXT_PUBLIC_SITE_URL=http://localhost:3000
NEXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX
NEXT_PUBLIC_GRAFANA_FARO_URL=http://localhost:3001/faro
```

**api/.env:**
```env
WC_WEBHOOK_SECRET=your_webhook_secret_here
GRAFANA_FARO_URL=http://grafana:3000/api/faro
SITE_URL=http://localhost:4000
DATABASE_URL=postgresql://user:password@localhost:5432/codexdb
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
```

### 5. Install Dependencies & Run

**Web (Next.js):**
```bash
cd web
npm install
npm run dev  # Runs on http://localhost:3000
```

**API (Express):**
```bash
cd api
npm install
npm run dev  # Runs on http://localhost:4000
```

### 6. Configure WooCommerce Webhooks
Follow instructions in `api/docs/webhooks-setup.md`:
- Create 7 webhooks in WooCommerce admin
- Point to `http://localhost:4000/webhooks/wc/subscription` and `/wc/order`
- Use webhook secret from `.env`

## 📦 Production Deployment

### Server: IONOS VPS 74.208.123.158

### 1. DNS Configuration
Add A records:
- `codexdominion.app` → 74.208.123.158
- `api.codexdominion.app` → 74.208.123.158
- `www.codexdominion.app` → 74.208.123.158

### 2. Deploy via SSH
```bash
cd infra/docker
./deploy-complete-system.sh
```

This script:
- Copies files to server via SCP
- Runs `docker-compose up -d` on remote
- Configures SSL with Certbot
- Runs health checks
- Starts monitoring stack

### 3. Configure SSL Certificates
```bash
ssh root@74.208.123.158
certbot --nginx -d codexdominion.app -d www.codexdominion.app -d api.codexdominion.app
```

### 4. GitHub Actions CI/CD
Push to `main` branch triggers automated deployment:
1. Build & test Next.js and API
2. Build Docker images
3. Push to registry
4. Deploy to Kubernetes cluster
5. Run smoke tests
6. Rollback on failure

Pipeline defined in `infra/ci-cd/deploy.yml`

## 🎯 Key Features

### E-commerce
- **6 Product Niches:** Kids Bible Stories, Homeschool, Wedding, Memory Verse, Seasonal, Digital Downloads
- **10 Auto-Generated Bundles:** Christmas Mega, Homeschool Starter/Master, Wedding Printables, Activity Mega, etc.
- **5 Subscription Plans:** Kids Bible Monthly ($9.99), Homeschool Monthly ($19.99), Wedding Planning ($14.99), Premium Coloring Club ($7.99), Activity Pack ($12.99)

### Lead Magnets
- 12-Month Christian Wedding Checklist (8-page PDF)
- Christmas Coloring Pack
- Homeschool Getting Started Guide
- Memory Verse Challenge Cards

### Analytics
- **Grafana Dashboard:** 10 panels tracking revenue, LTV, churn, conversion funnel, top products
- **Google Analytics 4:** E-commerce tracking with custom events
- **Prometheus Metrics:** 15-second scraping for web, api, wordpress, nginx, mysql, redis

### Social Media Automation
- **6 Platforms:** Instagram, Facebook, Pinterest, YouTube, TikTok, Email
- **Content Templates:** 6 post types with UTM tracking
- **Posting Schedule:** 17 Instagram posts/week, 20 Pinterest pins/week, 3 YouTube videos/week

### Backend Services
- **Webhook Handlers:** 8 subscription events + 2 order events
- **Entitlements System:** Automatic feature access based on subscription plan
- **Notifications:** Push + email alerts for subscription changes
- **Security:** HMAC SHA256 signature verification

## 🔧 Maintenance

### Daily Checks
```bash
# Check service health
docker-compose ps

# View API logs
docker logs codex-api --tail 100 -f

# Monitor webhook events
docker logs codex-api | grep "Webhook received"

# Check database connections
docker exec -it codex-db mariadb -u root -p -e "SHOW PROCESSLIST;"
```

### Backup Database
```bash
cd infra/docker
./backup.sh  # Creates timestamped SQL dump
```

### Update Dependencies
```bash
# Web
cd web && npm update && npm audit fix

# API
cd api && npm update && npm audit fix

# WordPress plugins (manual via WP Admin)
```

### Rollback Deployment
```bash
# Kubernetes rollback
kubectl rollout undo deployment/web-deployment

# Docker Compose rollback
docker-compose down
docker-compose pull codexdominion/web:previous-tag
docker-compose up -d
```

## 📊 Monitoring URLs

- **Grafana:** https://codexdominion.app/grafana (admin/your_password)
- **Prometheus:** http://74.208.123.158:9090
- **WordPress Admin:** https://codexdominion.app/wp-admin
- **API Health:** https://api.codexdominion.app/health
- **Webhook Health:** https://api.codexdominion.app/webhooks/health

## 🐛 Troubleshooting

### WordPress not accessible
```bash
docker logs codex-wordpress
docker exec -it codex-wordpress wp --info
```

### WooCommerce webhooks failing
1. Check webhook secret matches `.env`
2. Verify API is accessible: `curl https://api.codexdominion.app/health`
3. View webhook delivery logs in WooCommerce admin
4. Check API logs: `docker logs codex-api --tail 200 | grep Webhook`

### Next.js build errors
```bash
cd web
rm -rf .next node_modules
npm install
npm run build
```

### Database connection issues
```bash
# Test database
docker exec -it codex-db mariadb -u root -proot_pass -e "SELECT 1"

# Reset database (DESTRUCTIVE)
docker-compose down -v
docker-compose up -d db
```

## 📚 Documentation

- **API Reference:** `api/docs/` (webhooks, endpoints, authentication)
- **Component Storybook:** `web/storybook/` (UI component library)
- **Runbooks:** `playbooks/runbooks/` (deployment, backup, scaling)
- **Incident Response:** `playbooks/incidents/` (outage, security, data loss)

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/my-feature`
2. Commit changes: `git commit -am 'Add new feature'`
3. Push to branch: `git push origin feature/my-feature`
4. Create Pull Request on GitHub
5. CI/CD runs tests automatically
6. Merge after approval

## 📝 License

Copyright © 2025 Codex Dominion. All rights reserved.

## 🆘 Support

- Email: support@codexdominion.app
- Discord: https://discord.gg/codexdominion
- Docs: https://docs.codexdominion.app

---

**Production Status:** 90% Complete
**Next Steps:** WordPress setup → Webhook configuration → Go-live checklist
**Last Updated:** December 6, 2025
