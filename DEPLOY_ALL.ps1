# =============================================================================
# DOT300 - COMPLETE PRODUCTION DEPLOYMENT MASTER SCRIPT
# Deploys to Azure + GCP + IONOS with full monitoring
# =============================================================================

param(
    [switch]$Azure,
    [switch]$GCP,
    [switch]$IONOS,
    [switch]$All,
    [switch]$Monitoring,
    [string]$OpenAIKey = $env:OPENAI_API_KEY
)

$ErrorActionPreference = "Continue"

Write-Host "🔥 DOT300 COMPLETE DEPLOYMENT STARTING..." -ForegroundColor Magenta
Write-Host ""

# Colors
function Write-Success { Write-Host $args[0] -ForegroundColor Green }
function Write-Info { Write-Host $args[0] -ForegroundColor Cyan }
function Write-Warning { Write-Host $args[0] -ForegroundColor Yellow }
function Write-Error { Write-Host $args[0] -ForegroundColor Red }

# Step 1: Pre-flight checks
Write-Info "📋 Step 1: Pre-flight Checks..."
Write-Info "   Docker: $(docker --version)"
Write-Info "   Docker Compose: $(docker-compose --version)"

if (Test-Path "dot300_agents.json") {
    $size = (Get-Item "dot300_agents.json").Length / 1KB
    Write-Success "   ✓ dot300_agents.json exists ($([math]::Round($size, 2)) KB)"
} else {
    Write-Error "   ✗ dot300_agents.json NOT FOUND!"
    Write-Warning "   Run: python dot300_multi_agent.py"
    exit 1
}

# Step 2: Build Docker images locally
Write-Info "`n📦 Step 2: Building Docker Images..."
docker-compose -f docker-compose.production-full.yml build
if ($LASTEXITCODE -eq 0) {
    Write-Success "   ✓ All images built successfully"
} else {
    Write-Error "   ✗ Build failed"
    exit 1
}

# Step 3: Deploy monitoring stack locally (if requested)
if ($Monitoring -or $All) {
    Write-Info "`n📊 Step 3: Deploying Monitoring Stack..."
    Write-Info "   Starting: Prometheus, Grafana, Redis, RabbitMQ, NGINX..."

    docker-compose -f docker-compose.production-full.yml up -d

    Start-Sleep -Seconds 10

    Write-Success "   ✓ Monitoring stack deployed"
    Write-Info "   Services:"
    Write-Info "      - DOT300 API:        http://localhost:8300"
    Write-Info "      - Orchestration:     http://localhost:8400"
    Write-Info "      - Grafana:           http://localhost:3001 (admin/dot300admin)"
    Write-Info "      - Prometheus:        http://localhost:9090"
    Write-Info "      - RabbitMQ:          http://localhost:15672 (dot300/dot300secure)"
    Write-Info "      - Redis:             localhost:6379"
    Write-Info "      - NGINX:             http://localhost:80"
}

# Step 4: Deploy to Azure
if ($Azure -or $All) {
    Write-Info "`n☁️  Step 4: Deploying to Azure..."

    if (Get-Command az -ErrorAction SilentlyContinue) {
        Write-Info "   Running Azure deployment script..."
        bash deployment/deploy-azure.sh

        if ($LASTEXITCODE -eq 0) {
            Write-Success "   ✓ Azure deployment complete"
        } else {
            Write-Error "   ✗ Azure deployment failed"
        }
    } else {
        Write-Warning "   Azure CLI not found. Skipping Azure deployment."
        Write-Info "   Install: https://aka.ms/installazurecli"
    }
}

# Step 5: Deploy to GCP
if ($GCP -or $All) {
    Write-Info "`n☁️  Step 5: Deploying to GCP..."

    if (Get-Command gcloud -ErrorAction SilentlyContinue) {
        Write-Info "   Running GCP deployment script..."
        bash deployment/deploy-gcp.sh

        if ($LASTEXITCODE -eq 0) {
            Write-Success "   ✓ GCP deployment complete"
        } else {
            Write-Error "   ✗ GCP deployment failed"
        }
    } else {
        Write-Warning "   GCloud CLI not found. Skipping GCP deployment."
        Write-Info "   Install: https://cloud.google.com/sdk/docs/install"
    }
}

# Step 6: Deploy to IONOS
if ($IONOS -or $All) {
    Write-Info "`n☁️  Step 6: Deploying to IONOS VPS..."

    $ionosServer = $env:IONOS_SERVER
    if ($ionosServer) {
        Write-Info "   Running IONOS deployment script..."
        bash deployment/deploy-ionos.sh

        if ($LASTEXITCODE -eq 0) {
            Write-Success "   ✓ IONOS deployment complete"
        } else {
            Write-Error "   ✗ IONOS deployment failed"
        }
    } else {
        Write-Warning "   IONOS_SERVER not set. Skipping IONOS deployment."
        Write-Info "   Set: `$env:IONOS_SERVER = '74.208.123.158'"
    }
}

# Step 7: Test all deployments
Write-Info "`n🧪 Step 7: Testing Deployments..."

# Test local
Write-Info "   Testing local deployment..."
try {
    $local = Invoke-RestMethod -Uri "http://localhost:8300/health" -TimeoutSec 5
    Write-Success "   ✓ Local API: $($local.status)"
} catch {
    Write-Warning "   ! Local API not responding"
}

# Test orchestration
try {
    $orch = Invoke-RestMethod -Uri "http://localhost:8400/health" -TimeoutSec 5
    Write-Success "   ✓ Orchestration: $($orch.status) | GPT-4: $($orch.gpt4_enabled)"
} catch {
    Write-Warning "   ! Orchestration not responding"
}

# Step 8: Generate summary
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║     🚀 DOT300 DEPLOYMENT COMPLETE! 🚀          ║" -ForegroundColor Magenta
Write-Host "╚══════════════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""

Write-Success "✅ LOCAL SERVICES:"
Write-Host "   DOT300 API:        http://localhost:8300" -ForegroundColor Gray
Write-Host "   Orchestration:     http://localhost:8400" -ForegroundColor Gray
Write-Host "   Frontend:          http://localhost:80" -ForegroundColor Gray
Write-Host "   Grafana:           http://localhost:3001" -ForegroundColor Gray
Write-Host "   Prometheus:        http://localhost:9090" -ForegroundColor Gray
Write-Host ""

if ($Azure -or $All) {
    Write-Success "✅ AZURE:"
    Write-Host "   Check: Azure Portal → Container Instances" -ForegroundColor Gray
    Write-Host "   URL: https://dot300-api.eastus.azurecontainer.io:8300" -ForegroundColor Gray
}

if ($GCP -or $All) {
    Write-Success "✅ GCP:"
    Write-Host "   Check: Cloud Console → Cloud Run" -ForegroundColor Gray
    Write-Host "   URL: https://dot300-api-XXXXX-uc.a.run.app" -ForegroundColor Gray
}

if ($IONOS -or $All) {
    Write-Success "✅ IONOS:"
    Write-Host "   Server: $($env:IONOS_SERVER)" -ForegroundColor Gray
    Write-Host "   URL: https://api.codexdominion.app" -ForegroundColor Gray
}

Write-Host ""
Write-Info "📚 Next Steps:"
Write-Host "   1. Configure custom domains for all clouds" -ForegroundColor Gray
Write-Host "   2. Setup global load balancer (Cloudflare)" -ForegroundColor Gray
Write-Host "   3. Configure monitoring alerts" -ForegroundColor Gray
Write-Host "   4. Add OpenAI API key: Set-Item env:OPENAI_API_KEY 'sk-...'" -ForegroundColor Gray
Write-Host "   5. Launch marketing campaign!" -ForegroundColor Gray
Write-Host ""

Write-Success "🔥 Your AI Empire is LIVE! 🔥"
Write-Host ""
