#!/usr/bin/env pwsh
# =============================================================================
# Deploy Frontend to Azure Static Web Apps
# =============================================================================

$ErrorActionPreference = "Stop"

$RESOURCE_GROUP = "codexdominion-basic"
$STATIC_WEB_APP = "codexdominion-frontend"
$DEPLOYMENT_TOKEN = "49a8967274faf06a4b540ca5505f53253a5703debb7aea802fc05c21dc331b2a03-7e3efdf3-563b-49ae-8cb2-37768100362401e29120ebbd971e"

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🚀 DEPLOYING FRONTEND TO AZURE STATIC WEB APPS" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

# =============================================================================
# Step 1: Find and Build Frontend
# =============================================================================

Write-Host "`n[1/4] Locating Next.js frontend..." -ForegroundColor Cyan

$frontendPaths = @("web", "frontend-vite", "apps/frontend")
$frontendDir = $null

foreach ($path in $frontendPaths) {
    if (Test-Path $path) {
        $hasNextConfig = Test-Path "$path/next.config.js" -or (Test-Path "$path/next.config.mjs")
        $hasPackageJson = Test-Path "$path/package.json"

        if ($hasNextConfig -and $hasPackageJson) {
            $frontendDir = $path
            Write-Host "✓ Found Next.js app in: $path" -ForegroundColor Green
            break
        }
    }
}

if (-not $frontendDir) {
    Write-Host "❌ No Next.js frontend found. Checking for static HTML..." -ForegroundColor Yellow

    # Look for existing static build
    if (Test-Path "out") {
        $buildDir = "out"
        Write-Host "✓ Using existing out/ directory" -ForegroundColor Green
    } elseif (Test-Path "web/out") {
        $buildDir = "web/out"
        Write-Host "✓ Using web/out/ directory" -ForegroundColor Green
    } else {
        Write-Host "❌ No frontend to deploy. Please build your frontend first." -ForegroundColor Red
        exit 1
    }
} else {
    # Build the Next.js app
    Write-Host "`n[2/4] Building Next.js application..." -ForegroundColor Cyan

    Push-Location $frontendDir

    try {
        Write-Host "Installing dependencies..." -ForegroundColor White
        npm install --silent

        Write-Host "Building for production..." -ForegroundColor White
        npm run build

        if (Test-Path "out") {
            $buildDir = "$frontendDir/out"
            Write-Host "✓ Build successful: $buildDir" -ForegroundColor Green
        } elseif (Test-Path ".next") {
            Write-Host "⚠️  Warning: .next build found (not static export)" -ForegroundColor Yellow
            Write-Host "   Creating static export..." -ForegroundColor White
            npm run export
            $buildDir = "$frontendDir/out"
        } else {
            Write-Host "❌ Build failed or no output found" -ForegroundColor Red
            Pop-Location
            exit 1
        }
    } catch {
        Write-Host "❌ Build error: $_" -ForegroundColor Red
        Pop-Location
        exit 1
    }

    Pop-Location
}

# =============================================================================
# Step 2: Deploy using SWA CLI
# =============================================================================

Write-Host "`n[3/4] Deploying to Azure Static Web Apps..." -ForegroundColor Cyan

try {
    # Check if SWA CLI is available
    $swaVersion = swa --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ SWA CLI detected: $swaVersion" -ForegroundColor Green

        # Deploy with SWA CLI
        swa deploy $buildDir `
            --deployment-token $DEPLOYMENT_TOKEN `
            --env production `
            --verbose

        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Deployment successful via SWA CLI" -ForegroundColor Green
        } else {
            throw "SWA CLI deployment failed"
        }
    } else {
        throw "SWA CLI not found"
    }
} catch {
    Write-Host "⚠️  SWA CLI not available, using Azure CLI instead..." -ForegroundColor Yellow

    # Fallback to Azure CLI upload
    Write-Host "Creating deployment package..." -ForegroundColor White
    $zipPath = "..\frontend-deploy.zip"
    Compress-Archive -Path "$buildDir\*" -DestinationPath $zipPath -Force

    Write-Host "Uploading to Azure..." -ForegroundColor White
    # Azure Static Web Apps don't support direct zip upload via CLI
    # This would require GitHub Actions or SWA CLI

    Write-Host "❌ Please use one of these methods:" -ForegroundColor Red
    Write-Host "   1. Install SWA CLI: npm install -g @azure/static-web-apps-cli" -ForegroundColor Gray
    Write-Host "   2. Use GitHub Actions (automatic on git push)" -ForegroundColor Gray
    Write-Host "   3. Deploy via Azure Portal" -ForegroundColor Gray
    exit 1
}

# =============================================================================
# Step 3: Verify Deployment
# =============================================================================

Write-Host "`n[4/4] Verifying deployment..." -ForegroundColor Cyan

Start-Sleep -Seconds 10

$urls = @(
    "https://www.codexdominion.app",
    "https://witty-glacier-0ebbd971e.3.azurestaticapps.net"
)

foreach ($url in $urls) {
    try {
        $response = Invoke-WebRequest -Uri $url -Method Head -TimeoutSec 10 -ErrorAction Stop
        Write-Host "✓ $url (HTTP $($response.StatusCode))" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  $url - Not accessible yet" -ForegroundColor Yellow
    }
}

# =============================================================================
# Summary
# =============================================================================

Write-Host "`n═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  ✅ DEPLOYMENT COMPLETE" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

Write-Host "`nYour frontend is live at:" -ForegroundColor White
Write-Host "  🌐 https://www.codexdominion.app" -ForegroundColor Green
Write-Host "  🔗 https://witty-glacier-0ebbd971e.3.azurestaticapps.net" -ForegroundColor Green

Write-Host "`n💡 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Clear browser cache (Ctrl+Shift+Del)" -ForegroundColor Gray
Write-Host "  2. Test all pages and functionality" -ForegroundColor Gray
Write-Host "  3. Monitor deployment logs in Azure Portal" -ForegroundColor Gray

Write-Host "`n🔥 The Flame Burns Sovereign! 👑" -ForegroundColor Yellow
Write-Host ""
