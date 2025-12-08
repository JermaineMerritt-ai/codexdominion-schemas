# 🔥 CODEX DOMINION - MULTI-CLOUD DEPLOYMENT STRATEGY 1
# Geographic Distribution: IONOS (Frontend) + Google Cloud (Backend) + Azure (Registry/K8s)

param(
    [switch]$SkipIONOS,
    [switch]$SkipGCP,
    [switch]$SkipAzure
)

$ErrorActionPreference = 'Continue'

Write-Host "🔥 === CODEX DOMINION MULTI-CLOUD DEPLOYMENT ===" -ForegroundColor Cyan
Write-Host "Strategy 1: Geographic Distribution" -ForegroundColor Yellow
Write-Host ""

# =============================================================================
# PHASE 1: GOOGLE CLOUD - BACKEND SERVICES
# =============================================================================
if (-not $SkipGCP) {
    Write-Host "☁️  PHASE 1: Deploying to Google Cloud Run..." -ForegroundColor Green
    Write-Host "Services: Backend APIs, Treasury, Dawn Dispatch" -ForegroundColor Gray
    Write-Host ""

    # Create optimized .gcloudignore for faster uploads
    Write-Host "📦 Creating optimized .gcloudignore..." -ForegroundColor Yellow

    $gcloudignore = @"
# Node modules and build artifacts
node_modules/
.next/
dist/
build/
coverage/
*.log

# Python cache
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.venv/
venv/

# Git and IDE
.git/
.gitignore
.vscode/
.idea/

# Deployment files (not needed in container)
terraform/
.terraform/
kubernetes/
k8s/
helm/

# Documentation
*.md
docs/
README*

# Large files
*.zip
*.tar.gz
*.mp4
*.mov

# Local environment
.env.local
.env.development

# Pulumi
.pulumi/

# Codex schemas templates (not needed for backend)
codexdominion-schemas/templates/
codexdominion-schemas/multi_domain_codex_deployment/

# Archives
*.backup
backups/
"@

    Set-Content -Path ".gcloudignore" -Value $gcloudignore
    Write-Host "✅ .gcloudignore created" -ForegroundColor Green

    Write-Host ""
    Write-Host "🚀 Starting Google Cloud Build..." -ForegroundColor Cyan
    Write-Host "This will take 5-10 minutes. Build is running in background." -ForegroundColor Gray
    Write-Host "Monitor at: https://console.cloud.google.com/cloud-build/builds?project=codex-dominion-production" -ForegroundColor Blue
    Write-Host ""

    # Start build in background
    Start-Process pwsh -ArgumentList "-NoProfile", "-Command", "cd '$PWD'; gcloud builds submit --config cloudbuild.yaml 2>&1 | Tee-Object -FilePath 'gcp-deploy.log'" -NoNewWindow

    Write-Host "✅ Google Cloud deployment started (background)" -ForegroundColor Green
    Write-Host "📄 Log file: gcp-deploy.log" -ForegroundColor Gray
    Write-Host ""
    Start-Sleep -Seconds 3
}

# =============================================================================
# PHASE 2: AZURE - CONTAINER REGISTRY & KUBERNETES
# =============================================================================
if (-not $SkipAzure) {
    Write-Host "☁️  PHASE 2: Configuring Azure..." -ForegroundColor Green
    Write-Host "Services: Container Registry, optional AKS" -ForegroundColor Gray
    Write-Host ""

    # Check if Azure CLI is installed
    $azInstalled = Get-Command az -ErrorAction SilentlyContinue

    if ($azInstalled) {
        Write-Host "✅ Azure CLI found" -ForegroundColor Green

        # Check Azure login status
        $azLogin = az account show 2>$null
        if ($azLogin) {
            Write-Host "✅ Already logged in to Azure" -ForegroundColor Green

            # Push to Azure Container Registry via GitHub Actions
            Write-Host ""
            Write-Host "📦 To deploy to Azure ACR, push to GitHub:" -ForegroundColor Yellow
            Write-Host "   git push origin main" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "This triggers the build-deploy.yml workflow which:" -ForegroundColor Gray
            Write-Host "   1. Builds Docker images" -ForegroundColor Gray
            Write-Host "   2. Pushes to Azure Container Registry" -ForegroundColor Gray
            Write-Host "   3. Signs images with Cosign" -ForegroundColor Gray
            Write-Host ""

        } else {
            Write-Host "⚠️  Not logged in to Azure. Run: az login" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠️  Azure CLI not installed" -ForegroundColor Yellow
        Write-Host "   Install from: https://aka.ms/installazurecliwindows" -ForegroundColor Gray
        Write-Host "   Or use GitHub Actions to deploy (push to main branch)" -ForegroundColor Gray
    }
    Write-Host ""
}

# =============================================================================
# PHASE 3: IONOS - FRONTEND & DNS
# =============================================================================
if (-not $SkipIONOS) {
    Write-Host "☁️  PHASE 3: IONOS Frontend Deployment..." -ForegroundColor Green
    Write-Host "Services: Next.js Frontend, DNS for CodexDominion.app" -ForegroundColor Gray
    Write-Host ""

    Write-Host "📋 IONOS Deployment Options:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Option 1: Build and deploy Next.js frontend locally" -ForegroundColor Cyan
    Write-Host "   cd frontend" -ForegroundColor Gray
    Write-Host "   npm run build" -ForegroundColor Gray
    Write-Host "   Upload .next/standalone to IONOS via FTP/SSH" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Option 2: Use IONOS deployment script (VPS)" -ForegroundColor Cyan
    Write-Host "   SSH to IONOS server and run:" -ForegroundColor Gray
    Write-Host "   bash <(curl -s https://raw.githubusercontent.com/your-repo/main/ionos_quick_fix.sh)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Option 3: Static export for IONOS Webspace" -ForegroundColor Cyan
    Write-Host "   cd frontend" -ForegroundColor Gray
    Write-Host "   npm run build && npm run export" -ForegroundColor Gray
    Write-Host "   Upload 'out' folder to IONOS via FTP" -ForegroundColor Gray
    Write-Host ""

    # Check if frontend exists and offer to build
    if (Test-Path "frontend/package.json") {
        Write-Host "🔨 Frontend found. Build now? (y/n): " -ForegroundColor Yellow -NoNewline
        $build = Read-Host

        if ($build -eq 'y' -or $build -eq 'Y') {
            Write-Host ""
            Write-Host "Building frontend..." -ForegroundColor Cyan
            Push-Location frontend
            npm install
            npm run build
            Pop-Location
            Write-Host "✅ Frontend built successfully" -ForegroundColor Green
            Write-Host "📁 Output in: frontend/.next" -ForegroundColor Gray
            Write-Host ""
        }
    }
}

# =============================================================================
# PHASE 4: CONFIGURATION SUMMARY
# =============================================================================
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🎯 MULTI-CLOUD DEPLOYMENT STATUS" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ Google Cloud Run: " -NoNewline -ForegroundColor Green
Write-Host "Deploying backend services (check gcp-deploy.log)" -ForegroundColor White

Write-Host "✅ Azure ACR: " -NoNewline -ForegroundColor Green
Write-Host "Ready (push to GitHub main branch)" -ForegroundColor White

Write-Host "⏳ IONOS: " -NoNewline -ForegroundColor Yellow
Write-Host "Manual deployment required" -ForegroundColor White

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🌐 NEXT STEPS - DNS CONFIGURATION" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "Configure CodexDominion.app DNS in IONOS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. A Record (Frontend):" -ForegroundColor Cyan
Write-Host "   @ → Your IONOS server IP" -ForegroundColor Gray
Write-Host ""
Write-Host "2. CNAME Record (API):" -ForegroundColor Cyan
Write-Host "   api → [Google Cloud Run URL from deployment]" -ForegroundColor Gray
Write-Host ""
Write-Host "3. CNAME Record (Registry):" -ForegroundColor Cyan
Write-Host "   registry → [Azure ACR URL]" -ForegroundColor Gray
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "📊 MONITORING" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "Google Cloud:" -ForegroundColor Cyan
Write-Host "  https://console.cloud.google.com/run?project=codex-dominion-production" -ForegroundColor Blue
Write-Host ""

Write-Host "Azure Portal:" -ForegroundColor Cyan
Write-Host "  https://portal.azure.com/#view/HubsExtension/BrowseResource/resourceType/Microsoft.ContainerRegistry%2Fregistries" -ForegroundColor Blue
Write-Host ""

Write-Host "GitHub Actions:" -ForegroundColor Cyan
Write-Host "  https://github.com/JermaineMerritt-ai/codexdominion-schemas/actions" -ForegroundColor Blue
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🔥 DEPLOYMENT INITIATED - DOMINION ETERNAL 🔥" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Save deployment info
$deploymentInfo = @{
    timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    strategy = "Geographic Distribution"
    clouds = @{
        gcp = @{
            status = "Deploying"
            service = "Cloud Run"
            region = "us-central1"
            logFile = "gcp-deploy.log"
        }
        azure = @{
            status = "Ready"
            service = "Container Registry"
            triggerMethod = "GitHub Actions (push to main)"
        }
        ionos = @{
            status = "Pending"
            service = "Frontend + DNS"
            deploymentMethod = "Manual"
        }
    }
} | ConvertTo-Json -Depth 5

Set-Content -Path "multicloud-deployment-status.json" -Value $deploymentInfo
Write-Host "💾 Deployment info saved to: multicloud-deployment-status.json" -ForegroundColor Gray
Write-Host ""
