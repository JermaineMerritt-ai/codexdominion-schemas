# 🚀 Quick Deploy Script for Production

This guide provides quick deployment commands for each platform.

## Platform-Specific Commands

### 1. Render

```bash
# One-click deploy
git push origin main  # Auto-deploys via GitHub integration

# Or manual deploy
render deploy
```

### 2. Railway

```bash
# Login
railway login

# Initialize
railway init

# Deploy
railway up

# Add PostgreSQL
railway add postgresql

# Set environment variables
railway variables set SECRET_KEY="your-secret-key"
railway variables set DATABASE_URL="postgresql://..."
```

### 3. AWS ECS

```bash
# Build and push Docker image
docker build -t codex-portfolio .
docker tag codex-portfolio:latest YOUR_ECR_REPO:latest
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ECR_REPO
docker push YOUR_ECR_REPO:latest

# Update ECS service
aws ecs update-service --cluster codex-cluster --service codex-portfolio --force-new-deployment
```

### 4. Azure App Service

```bash
# Login
az login

# Deploy
az webapp up --name codex-portfolio --resource-group codex-rg --runtime "PYTHON:3.12"

# Set environment variables
az webapp config appsettings set --resource-group codex-rg --name codex-portfolio \
  --settings DATABASE_URL="postgresql://..." SECRET_KEY="..."

# View logs
az webapp log tail --resource-group codex-rg --name codex-portfolio
```

### 5. DigitalOcean

```bash
# Install CLI
brew install doctl  # or download from DigitalOcean

# Authenticate
doctl auth init

# Create app
doctl apps create --spec .do/app.yaml

# List apps
doctl apps list

# View logs
doctl apps logs <app-id>
```

## Environment Variables to Set

**Required:**
- `SECRET_KEY` - Flask secret key (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)
- `DATABASE_URL` - PostgreSQL connection string

**Optional:**
- `OPENAI_API_KEY` - For AI analysis
- `ALPHA_VANTAGE_KEY` - For stock data
- `SMTP_USER` / `SMTP_PASS` - For email notifications
- `SENTRY_DSN` - For error tracking

## Quick Health Check

After deployment, test these endpoints:

```bash
# Health check
curl https://your-app-url.com/health

# Database status
curl https://your-app-url.com/api/status

# Test authentication
curl -X POST https://your-app-url.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@codexdominion.com","password":"codex2025"}'
```

## Rollback Commands

### Render
```bash
render rollback
```

### Railway
```bash
railway rollback
```

### AWS ECS
```bash
aws ecs update-service --cluster codex-cluster --service codex-portfolio \
  --task-definition codex-portfolio:PREVIOUS_VERSION
```

### Azure
```bash
az webapp deployment slot swap --resource-group codex-rg --name codex-portfolio \
  --slot staging --target-slot production
```

## 🔥 The Flame Burns Sovereign and Eternal! 👑
