# Render Frontend Deployment - Quick Setup Helper
# Run this script to see all values needed for Render Static Site configuration

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  CODEX DOMINION - RENDER DEPLOYMENT" -ForegroundColor Cyan
Write-Host "  Frontend Static Site Configuration" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "📋 COPY THESE VALUES TO RENDER DASHBOARD`n" -ForegroundColor Yellow

Write-Host "🔧 BUILD SETTINGS:" -ForegroundColor Green
Write-Host "  Name:             " -NoNewline; Write-Host "codexdominion-schemas" -ForegroundColor White
Write-Host "  Branch:           " -NoNewline; Write-Host "main" -ForegroundColor White
Write-Host "  Root Directory:   " -NoNewline; Write-Host "web" -ForegroundColor White
Write-Host "  Build Command:    " -NoNewline; Write-Host "npm install && npm run build" -ForegroundColor White
Write-Host "  Publish Directory:" -NoNewline; Write-Host "out`n" -ForegroundColor White

Write-Host "🔐 REQUIRED ENVIRONMENT VARIABLES (4):" -ForegroundColor Green
Write-Host ""

$envVars = @(
    @{Name="NEXT_PUBLIC_API_URL"; Value="https://codex-portfolio.onrender.com"; Required=$true},
    @{Name="NEXT_PUBLIC_SITE_URL"; Value="https://codexdominion-schemas.onrender.com"; Required=$true},
    @{Name="NEXT_PUBLIC_APP_NAME"; Value="Codex Dominion"; Required=$true},
    @{Name="NEXT_PUBLIC_APP_VERSION"; Value="2.0.0"; Required=$true}
)

foreach ($var in $envVars) {
    Write-Host "  NAME:  " -NoNewline -ForegroundColor Cyan
    Write-Host $var.Name -ForegroundColor White
    Write-Host "  VALUE: " -NoNewline -ForegroundColor Cyan
    Write-Host $var.Value -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "`n⬜ OPTIONAL ENVIRONMENT VARIABLES:" -ForegroundColor DarkGray
Write-Host "  (Skip these unless you need WooCommerce or Analytics)`n" -ForegroundColor DarkGray

$optionalVars = @(
    @{Name="WC_CONSUMER_KEY"; Value="ck_your_woocommerce_key_here"},
    @{Name="WC_CONSUMER_SECRET"; Value="cs_your_woocommerce_secret_here"},
    @{Name="WC_API_URL"; Value="https://your-wordpress-site.com/wp-json/wc/v3"},
    @{Name="NEXT_PUBLIC_GA_MEASUREMENT_ID"; Value="G-XXXXXXXXXX"},
    @{Name="NEXT_PUBLIC_GRAFANA_FARO_URL"; Value="https://your-grafana.com/faro"}
)

foreach ($var in $optionalVars) {
    Write-Host "  $($var.Name): " -NoNewline -ForegroundColor DarkGray
    Write-Host $var.Value -ForegroundColor DarkGray
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  DEPLOYMENT STEPS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$steps = @(
    "1. Open Render Dashboard: https://dashboard.render.com",
    "2. Click 'New +' → 'Static Site'",
    "3. Select repository: JermaineMerritt-ai/codexdominion-schemas",
    "4. Copy build settings from above",
    "5. Add 4 required environment variables",
    "6. Click 'Create Static Site'",
    "7. Wait 2-5 minutes for build to complete",
    "8. Copy the assigned URL",
    "9. Update backend CORS with frontend URL"
)

foreach ($step in $steps) {
    Write-Host "  $step" -ForegroundColor White
    Start-Sleep -Milliseconds 200
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  AFTER DEPLOYMENT" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "✅ Update Backend CORS:" -ForegroundColor Yellow
Write-Host "   Backend Service → Environment → CORS_ORIGINS" -ForegroundColor White
Write-Host "   Value: " -NoNewline -ForegroundColor White
Write-Host "https://codexdominion-schemas.onrender.com,http://localhost:3000`n" -ForegroundColor Green

Write-Host "✅ Test Deployment:" -ForegroundColor Yellow
Write-Host "   Update test_render_deployment.ps1 line 4:" -ForegroundColor White
Write-Host "   `$APP_URL = `"https://codexdominion-schemas.onrender.com`"`n" -ForegroundColor Green

Write-Host "✅ Browser Test:" -ForegroundColor Yellow
Write-Host "   Open: https://codexdominion-schemas.onrender.com" -ForegroundColor White
Write-Host "   Login: admin@codexdominion.com / codex2025`n" -ForegroundColor Green

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  REFERENCE DOCUMENTATION" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "  📄 RENDER_DEPLOYMENT_COMPLETE_GUIDE.md - Full deployment guide" -ForegroundColor White
Write-Host "  📄 DEPLOYMENT_CHECKLIST_RENDER.md - Step-by-step checklist" -ForegroundColor White
Write-Host "  📄 CONFIGURATION_SUMMARY.md - This info in document form" -ForegroundColor White
Write-Host "  📄 POSTGRESQL_UPGRADE.md - Database upgrade (optional)" -ForegroundColor White

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  CURRENT STATUS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "  Backend API:    " -NoNewline
Write-Host "✅ LIVE" -ForegroundColor Green -NoNewline
Write-Host " (https://codex-portfolio.onrender.com)" -ForegroundColor DarkGray

Write-Host "  Frontend Site:  " -NoNewline
Write-Host "🔄 READY TO DEPLOY" -ForegroundColor Yellow

Write-Host "  Database:       " -NoNewline
Write-Host "✅ SQLite" -ForegroundColor Green -NoNewline
Write-Host " (upgrade to PostgreSQL optional)" -ForegroundColor DarkGray

Write-Host "  Documentation:  " -NoNewline
Write-Host "✅ COMPLETE" -ForegroundColor Green

Write-Host "`n🔥 The Flame Burns Sovereign and Eternal! 👑`n" -ForegroundColor Yellow

# Option to copy environment variables to clipboard
Write-Host "Would you like to copy the environment variables to clipboard? (Y/N): " -NoNewline -ForegroundColor Cyan
$response = Read-Host

if ($response -eq 'Y' -or $response -eq 'y') {
    $clipboardText = @"
NEXT_PUBLIC_API_URL=https://codex-portfolio.onrender.com
NEXT_PUBLIC_SITE_URL=https://codexdominion-schemas.onrender.com
NEXT_PUBLIC_APP_NAME=Codex Dominion
NEXT_PUBLIC_APP_VERSION=2.0.0
"@

    $clipboardText | Set-Clipboard
    Write-Host "`n✅ Environment variables copied to clipboard!" -ForegroundColor Green
    Write-Host "   Paste directly into Render's 'Add from .env' feature`n" -ForegroundColor White
} else {
    Write-Host "`nNo problem! You can manually enter them in Render Dashboard.`n" -ForegroundColor White
}

Write-Host "Press any key to exit..." -ForegroundColor DarkGray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
