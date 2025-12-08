# ============================================================================
# Build Codex Dominion Frontend for IONOS Deployment
# ============================================================================
# This script creates a production-ready static export for IONOS hosting

Write-Host "🔥 Building Codex Dominion Frontend for IONOS" -ForegroundColor Cyan
Write-Host "=============================================`n" -ForegroundColor Cyan

# Get Azure backend URL (from deployment or manual input)
if (Test-Path "azure-deployment-info.json") {
    $deployInfo = Get-Content "azure-deployment-info.json" | ConvertFrom-Json
    $BACKEND_URL = $deployInfo.BackendURL
    Write-Host "✅ Found Azure backend URL from deployment: $BACKEND_URL`n" -ForegroundColor Green
} else {
    Write-Host "⚠️  No Azure deployment info found." -ForegroundColor Yellow
    $BACKEND_URL = Read-Host "Enter your Azure backend URL (e.g., http://codex-backend.eastus.azurecontainer.io:8001)"
}

# Update frontend environment
Write-Host "📝 Step 1: Updating frontend environment variables..." -ForegroundColor Cyan
$envContent = @"
# Production Environment for IONOS Deployment
NODE_ENV=production
NEXT_PUBLIC_API_URL=$BACKEND_URL
NEXT_PUBLIC_SITE_URL=https://codexdominion.app
"@

$envContent | Out-File "frontend\.env.production" -Encoding UTF8
Write-Host "   ✅ Created frontend/.env.production" -ForegroundColor Green

# Build Next.js application
Write-Host "`n🔨 Step 2: Building Next.js production bundle..." -ForegroundColor Cyan
cd frontend
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed! Check errors above." -ForegroundColor Red
    cd ..
    exit 1
}

# Export static files
Write-Host "`n📦 Step 3: Exporting static files for IONOS..." -ForegroundColor Cyan
npm run export

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Export failed! Check errors above." -ForegroundColor Red
    cd ..
    exit 1
}

cd ..

# Create deployment package
Write-Host "`n📦 Step 4: Creating IONOS deployment package..." -ForegroundColor Cyan
$deployFolder = "ionos-deploy"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$zipName = "codex-dominion-frontend-$timestamp.zip"

if (Test-Path $deployFolder) {
    Remove-Item $deployFolder -Recurse -Force
}

New-Item -ItemType Directory -Path $deployFolder | Out-Null
Copy-Item -Path "frontend\out\*" -Destination $deployFolder -Recurse

# Create .htaccess for IONOS Apache server
$htaccess = @"
# Codex Dominion - IONOS Apache Configuration
RewriteEngine On

# Force HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Handle Next.js routes
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.+)$ /$1.html [L]

# Fallback to index for SPA behavior
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^ /index.html [L]

# Security headers
<IfModule mod_headers.c>
    Header set X-Content-Type-Options "nosniff"
    Header set X-Frame-Options "SAMEORIGIN"
    Header set X-XSS-Protection "1; mode=block"
    Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>

# Enable compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/json
</IfModule>

# Cache static assets
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/webp "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
    ExpiresByType application/json "access plus 0 seconds"
</IfModule>
"@

$htaccess | Out-File "$deployFolder\.htaccess" -Encoding UTF8
Write-Host "   ✅ Created .htaccess for IONOS" -ForegroundColor Green

# Create zip file
Write-Host "`n📦 Step 5: Creating deployment ZIP..." -ForegroundColor Cyan
Compress-Archive -Path "$deployFolder\*" -DestinationPath $zipName -Force
Write-Host "   ✅ Created $zipName" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ IONOS DEPLOYMENT PACKAGE READY!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "📦 Deployment Package:" -ForegroundColor Yellow
Write-Host "   File: $zipName" -ForegroundColor Cyan
Write-Host "   Size: $((Get-Item $zipName).Length / 1MB | ForEach-Object {[math]::Round($_, 2)}) MB`n" -ForegroundColor Cyan

Write-Host "📌 Next Steps for IONOS Deployment:" -ForegroundColor Yellow
Write-Host "   1. Log in to IONOS control panel" -ForegroundColor White
Write-Host "   2. Navigate to your hosting package for codexdominion.app" -ForegroundColor White
Write-Host "   3. Access File Manager or FTP" -ForegroundColor White
Write-Host "   4. Upload and extract $zipName to your web root" -ForegroundColor White
Write-Host "   5. Ensure .htaccess is in the root directory" -ForegroundColor White
Write-Host "   6. Test: https://codexdominion.app" -ForegroundColor White
Write-Host "   7. Test AI chat: Should connect to $BACKEND_URL`n" -ForegroundColor White

Write-Host "🔧 Alternative: FTP Upload" -ForegroundColor Yellow
Write-Host "   Extract $zipName locally and upload contents via FTP:`n" -ForegroundColor Gray
Write-Host "   Host: ftp.codexdominion.app" -ForegroundColor Gray
Write-Host "   Upload to: /htdocs or /public_html (check IONOS docs)`n" -ForegroundColor Gray

Write-Host "🔥 The sovereign frontend awaits deployment to IONOS!" -ForegroundColor Magenta

# Save build info
$buildInfo = @{
    BuildDate = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    BackendURL = $BACKEND_URL
    DeploymentPackage = $zipName
    FrontendURL = "https://codexdominion.app"
}

$buildInfo | ConvertTo-Json | Out-File "ionos-build-info.json"
Write-Host "💾 Build info saved to: ionos-build-info.json" -ForegroundColor Green
