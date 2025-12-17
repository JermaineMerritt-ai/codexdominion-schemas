# 🚀 Production Deployment Guide

## Deployment Platforms

### 1. Render (Recommended for Quick Deploy)

**Setup:**
```bash
# Install Render CLI
pip install render-cli

# Deploy
render deploy
```

**Files Required:**
- `render.yaml` (created below)
- `Procfile`
- `requirements.txt`

**render.yaml:**
```yaml
services:
  - type: web
    name: codex-portfolio
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: FLASK_ENV
        value: production
```

---

### 2. Railway

**Setup:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Environment Variables:**
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=your-secret-key
FLASK_ENV=production
```

---

### 3. AWS ECS (Elastic Container Service)

**Prerequisites:**
- AWS Account
- Docker installed
- AWS CLI configured

**Steps:**

1. **Build Docker Image:**
```bash
docker build -t codex-portfolio .
docker tag codex-portfolio:latest YOUR_ECR_REPO_URL:latest
docker push YOUR_ECR_REPO_URL:latest
```

2. **Create ECS Task Definition:**
```json
{
  "family": "codex-portfolio",
  "containerDefinitions": [
    {
      "name": "web",
      "image": "YOUR_ECR_REPO_URL:latest",
      "memory": 512,
      "cpu": 256,
      "essential": true,
      "portMappings": [
        {
          "containerPort": 5001,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://..."
        }
      ]
    }
  ]
}
```

3. **Create ECS Service:**
```bash
aws ecs create-service \
  --cluster codex-cluster \
  --service-name codex-portfolio \
  --task-definition codex-portfolio \
  --desired-count 2 \
  --launch-type FARGATE
```

---

### 4. Azure App Service

**Setup:**
```bash
# Install Azure CLI
az login

# Create resource group
az group create --name codex-rg --location eastus

# Create App Service plan
az appservice plan create \
  --name codex-plan \
  --resource-group codex-rg \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --resource-group codex-rg \
  --plan codex-plan \
  --name codex-portfolio \
  --runtime "PYTHON:3.12"

# Configure environment variables
az webapp config appsettings set \
  --resource-group codex-rg \
  --name codex-portfolio \
  --settings DATABASE_URL="postgresql://..." SECRET_KEY="..."

# Deploy
az webapp up --name codex-portfolio --resource-group codex-rg
```

---

### 5. DigitalOcean App Platform

**Setup:**
```bash
# Install doctl
brew install doctl  # or download from DigitalOcean

# Authenticate
doctl auth init

# Create app
doctl apps create --spec .do/app.yaml
```

**.do/app.yaml:**
```yaml
name: codex-portfolio
services:
  - name: web
    github:
      repo: your-username/codex-dominion
      branch: main
      deploy_on_push: true
    build_command: pip install -r requirements.txt
    run_command: gunicorn app:app
    environment_slug: python
    envs:
      - key: DATABASE_URL
        scope: RUN_TIME
        type: SECRET
    http_port: 8080
databases:
  - name: codex-db
    engine: PG
    version: "14"
```

---

## Infrastructure Components

### 1. Gunicorn Configuration

**gunicorn_config.py:**
```python
import multiprocessing

# Server socket
bind = "0.0.0.0:5001"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
```

**Run:**
```bash
gunicorn -c gunicorn_config.py app:app
```

---

### 2. Nginx Configuration

**nginx.conf:**
```nginx
upstream app_server {
    server localhost:5001 fail_timeout=0;
}

server {
    listen 80;
    server_name codexdominion.app;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name codexdominion.app;

    ssl_certificate /etc/letsencrypt/live/codexdominion.app/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/codexdominion.app/privkey.pem;

    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    client_max_body_size 10M;

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://app_server;
    }

    location /static {
        alias /var/www/codex-dominion/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

---

### 3. PostgreSQL Managed Database

**Providers:**
- **AWS RDS:** `rds.amazonaws.com`
- **Azure Database for PostgreSQL:** `postgres.database.azure.com`
- **DigitalOcean Managed Database:** `db.ondigitalocean.com`
- **Render PostgreSQL:** Auto-provisioned
- **Railway PostgreSQL:** Auto-provisioned

**Connection String Format:**
```
postgresql://username:password@host:5432/database?sslmode=require
```

**Migration:**
```bash
# Export from SQLite
sqlite3 codex_dominion.db .dump > dump.sql

# Import to PostgreSQL (after converting syntax)
psql -h host -U username -d database -f dump.sql
```

---

### 4. Celery Worker + Beat

**Install:**
```bash
pip install celery redis
```

**celery_app.py:**
```python
from celery import Celery
from celery.schedules import crontab

celery_app = Celery('codex', broker='redis://localhost:6379/0')

celery_app.conf.beat_schedule = {
    'update-stock-prices': {
        'task': 'tasks.update_stock_prices',
        'schedule': crontab(hour=16, minute=30),  # After market close
    },
    'generate-daily-alerts': {
        'task': 'tasks.generate_daily_alerts',
        'schedule': crontab(hour=9, minute=0),  # Before market open
    },
    'send-newsletter': {
        'task': 'tasks.send_newsletter',
        'schedule': crontab(day_of_week=1, hour=7, minute=0),  # Monday 7am
    }
}
```

**tasks.py:**
```python
from celery_app import celery_app
from database import db, StockPrice, MarketAlert
import yfinance as yf

@celery_app.task
def update_stock_prices():
    """Update stock prices daily"""
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        # Save to database

@celery_app.task
def generate_daily_alerts():
    """Generate market alerts"""
    # AI analysis logic here
    pass

@celery_app.task
def send_newsletter():
    """Send weekly newsletter"""
    # Email sending logic here
    pass
```

**Start Workers:**
```bash
# Worker
celery -A celery_app worker --loglevel=info

# Beat scheduler
celery -A celery_app beat --loglevel=info
```

**Procfile (for Render/Railway):**
```
web: gunicorn -c gunicorn_config.py app:app
worker: celery -A celery_app worker --loglevel=info
beat: celery -A celery_app beat --loglevel=info
```

---

## Environment Variables

**Production .env:**
```bash
# Flask
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this
FLASK_APP=app.py

# Database
DATABASE_URL=postgresql://user:pass@host:5432/codex_prod

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0

# API Keys
OPENAI_API_KEY=sk-...
ALPHA_VANTAGE_KEY=...
POLYGON_API_KEY=...

# Email (for newsletters)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# Security
CORS_ORIGINS=https://codexdominion.app,https://www.codexdominion.app

# Monitoring
SENTRY_DSN=https://...@sentry.io/...
```

---

## Deployment Checklist

### Pre-Deployment
- [ ] Update `requirements.txt`
- [ ] Set all environment variables
- [ ] Run database migrations
- [ ] Test production build locally
- [ ] Set up SSL certificates
- [ ] Configure DNS records
- [ ] Set up monitoring (Sentry, DataDog, etc.)

### Deployment
- [ ] Deploy application
- [ ] Verify health endpoint: `/health`
- [ ] Run smoke tests
- [ ] Monitor logs for errors
- [ ] Test critical user flows

### Post-Deployment
- [ ] Monitor application metrics
- [ ] Set up backups (database, logs)
- [ ] Configure auto-scaling
- [ ] Set up alerts (Slack, PagerDuty)
- [ ] Document deployment process
- [ ] Train team on rollback procedures

---

## Monitoring & Logging

**Health Check Endpoint:**
```python
@app.route('/health')
def health():
    return {
        'status': 'healthy',
        'database': check_db_connection(),
        'redis': check_redis_connection(),
        'timestamp': datetime.utcnow().isoformat()
    }
```

**Sentry Integration:**
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

---

## Rollback Strategy

**1. Quick Rollback (Render/Railway):**
```bash
# Revert to previous deployment
render rollback
railway rollback
```

**2. AWS ECS:**
```bash
# Update service to previous task definition
aws ecs update-service \
  --cluster codex-cluster \
  --service codex-portfolio \
  --task-definition codex-portfolio:PREVIOUS_VERSION
```

**3. Database Migrations:**
```bash
# Rollback last migration
flask db downgrade -1
```

---

## Scaling Strategies

### Horizontal Scaling
- **Web Workers:** Increase Gunicorn workers
- **Celery Workers:** Add more worker processes
- **Load Balancer:** Distribute traffic across instances

### Vertical Scaling
- Increase memory/CPU per instance
- Optimize database queries
- Add caching layers (Redis)

### Database Optimization
- Add indexes on frequently queried columns
- Use connection pooling
- Implement read replicas
- Cache AI responses

---

## Cost Optimization

**Platform Estimates (per month):**
- **Render:** $7-25 (Starter to Pro)
- **Railway:** $5-20 (Pay as you go)
- **AWS ECS:** $30-100 (Fargate + RDS)
- **Azure App Service:** $13-55 (Basic to Standard)
- **DigitalOcean:** $12-48 (Basic to Professional)

**Database Costs:**
- **Render PostgreSQL:** $7-50/month
- **Railway PostgreSQL:** Free tier available
- **AWS RDS:** $15-200/month
- **Azure PostgreSQL:** $20-150/month
- **DigitalOcean:** $15-120/month

---

## 🔥 The Flame Burns Sovereign and Eternal! 👑
