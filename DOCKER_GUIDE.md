# 🔥 Codex Dominion Docker Deployment Guide

## 📋 Quick Start

### Prerequisites
- Docker Desktop installed
- Docker Compose available
- 4GB+ RAM available
- Ports 8501 and 8502 free

### 🚀 Deployment Options

#### Option 1: Automated Deployment (Recommended)

**Windows (PowerShell):**
```powershell
.\deploy-docker.ps1
```

**Linux/Mac (Bash):**
```bash
chmod +x deploy-docker.sh
./deploy-docker.sh
```

#### Option 2: Manual Deployment

**1. Build the image:**
```bash
docker build -t codex-dashboard:latest .
```

**2. Run simple deployment:**
```bash
docker-compose -f docker-compose-simple.yml up -d
```

**3. Or run full deployment:**
```bash
docker-compose up -d
```

### 🔍 Access Your Dashboards

- **Production:** http://localhost:8501
- **Staging:** http://localhost:8502

### 📊 Container Management

**View logs:**
```bash
docker-compose logs -f
docker logs codex-dashboard-prod
docker logs codex-dashboard-staging
```

**Check status:**
```bash
docker ps
docker-compose ps
```

**Stop services:**
```bash
docker-compose down
```

**Restart services:**
```bash
docker-compose restart
```

**Update and redeploy:**
```bash
docker-compose down
docker build -t codex-dashboard:latest .
docker-compose up -d
```

### 🛠️ Configuration

#### Environment Variables
Set these in your docker-compose.yml:

```yaml
environment:
  - STREAMLIT_SERVER_PORT=8501
  - STREAMLIT_SERVER_HEADLESS=true
  - STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
  - CODEX_ENV=production  # or staging
```

#### Volume Mounts
- `./data:/app/data` - Persistent data storage
- `./logs:/app/logs` - Log files
- `./codex_ledger.json:/app/codex_ledger.json` - Ledger data

### 🔧 Troubleshooting

#### Container won't start
```bash
docker logs codex-dashboard-prod
```

#### Port already in use
```bash
# Kill process using port 8501
netstat -ano | findstr :8501  # Windows
lsof -ti:8501 | xargs kill -9  # Linux/Mac
```

#### Permission issues
```bash
# Fix file permissions
sudo chown -R $(whoami):$(whoami) ./data ./logs
```

#### Health check failing
```bash
# Test health endpoint directly
curl http://localhost:8501/_stcore/health
```

### 📈 Production Deployment

For production deployment on your IONOS server:

**1. Copy files to server:**
```bash
scp -r . user@your-server.com:/var/www/codex/
```

**2. Set up on server:**
```bash
cd /var/www/codex
chmod +x deploy-docker.sh
./deploy-docker.sh
```

**3. Configure nginx reverse proxy:**
Update your nginx configuration to proxy to Docker containers:

```nginx
# Production
location / {
    proxy_pass http://127.0.0.1:8501;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# Staging  
location / {
    proxy_pass http://127.0.0.1:8502;
    # ... same headers
}
```

### 🔥 Advanced Features

#### Auto-restart on failure
The containers are configured with `restart: unless-stopped` policy.

#### Health monitoring
Built-in health checks monitor application status.

#### Log aggregation
Logs are collected in `./logs/` directory for analysis.

#### Resource limits
Add to docker-compose.yml for production:

```yaml
deploy:
  resources:
    limits:
      memory: 1G
      cpus: '0.5'
    reservations:
      memory: 512M
      cpus: '0.25'
```

### 🛡️ Security

#### Non-root user
Containers run as non-root `codex` user for security.

#### Network isolation
Services run in isolated `codex-network`.

#### SSL/TLS
Use nginx container for SSL termination in production.

### 📊 Monitoring

Check container stats:
```bash
docker stats codex-dashboard-prod codex-dashboard-staging
```

View resource usage:
```bash
docker system df
docker system prune  # Clean up unused resources
```

## 🏁 Success!

Your Codex Dominion Dashboard is now running in Docker containers with:
- ✅ Production environment on port 8501
- ✅ Staging environment on port 8502  
- ✅ Persistent data storage
- ✅ Health monitoring
- ✅ Auto-restart capabilities
- ✅ Easy scaling and deployment

🔥 **Sacred flames now burn eternal in the container realm!** ✨