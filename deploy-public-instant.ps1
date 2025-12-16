# =============================================================================
# CODEX DOMINION - Instant Public Deployment (ngrok)
# =============================================================================
# Makes your local dashboard accessible from internet in 30 seconds!
# =============================================================================

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🌐 INSTANT PUBLIC ACCESS - Using ngrok" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check if ngrok is installed
$ngrokPath = Get-Command ngrok -ErrorAction SilentlyContinue

if (!$ngrokPath) {
    Write-Host "📥 Installing ngrok..." -ForegroundColor Cyan

    # Download ngrok
    $ngrokUrl = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
    $tempZip = "$env:TEMP\ngrok.zip"
    $ngrokDir = "$env:USERPROFILE\ngrok"

    Write-Host "   Downloading..." -ForegroundColor Gray
    Invoke-WebRequest -Uri $ngrokUrl -OutFile $tempZip -UseBasicParsing

    Write-Host "   Extracting..." -ForegroundColor Gray
    Expand-Archive -Path $tempZip -DestinationPath $ngrokDir -Force

    # Add to PATH for this session
    $env:PATH += ";$ngrokDir"

    Write-Host "✅ ngrok installed to $ngrokDir" -ForegroundColor Green
    Write-Host ""
}

# Check if dashboard is running
Write-Host "🔍 Checking dashboard status..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
    Write-Host "✅ Dashboard is running on localhost:5000" -ForegroundColor Green
} catch {
    Write-Host "❌ Dashboard not running!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Start dashboard first:" -ForegroundColor Yellow
    Write-Host "  .\START_DASHBOARD.bat" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "🚀 Creating public tunnel..." -ForegroundColor Cyan
Write-Host "   Local: http://localhost:5000" -ForegroundColor Gray
Write-Host "   Creating public URL..." -ForegroundColor Gray
Write-Host ""

# Start ngrok in background
Start-Process -FilePath "ngrok" -ArgumentList "http 5000" -WindowStyle Normal

Write-Host "⏳ Waiting for ngrok to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Get public URL from ngrok API
try {
    $ngrokApi = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -Method Get
    $publicUrl = $ngrokApi.tunnels[0].public_url

    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host "  ✨ YOUR DASHBOARD IS NOW PUBLIC!" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Public URL:" -ForegroundColor Cyan
    Write-Host "   $publicUrl" -ForegroundColor White
    Write-Host ""
    Write-Host "📱 Share this URL with anyone!" -ForegroundColor Yellow
    Write-Host "   ✅ Works from any device" -ForegroundColor Green
    Write-Host "   ✅ HTTPS included" -ForegroundColor Green
    Write-Host "   ✅ No configuration needed" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔍 Monitor traffic:" -ForegroundColor Cyan
    Write-Host "   http://localhost:4040" -ForegroundColor Gray
    Write-Host ""
    Write-Host "⚠️  Note: Free ngrok URLs change when you restart" -ForegroundColor Yellow
    Write-Host "   Get static URL: ngrok.com/pricing (free tier available)" -ForegroundColor Gray
    Write-Host ""

    # Open in browser
    Write-Host "🌐 Opening in browser..." -ForegroundColor Cyan
    Start-Process $publicUrl
    Start-Sleep -Seconds 2
    Start-Process "http://localhost:4040"

} catch {
    Write-Host "❌ Could not get ngrok URL" -ForegroundColor Red
    Write-Host "   Check ngrok dashboard: http://localhost:4040" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "💡 Tips:" -ForegroundColor Cyan
Write-Host "   • Keep this window open (ngrok tunnel stays active)" -ForegroundColor Gray
Write-Host "   • Dashboard runs on your machine (full control)" -ForegroundColor Gray
Write-Host "   • Free tier: 1 tunnel, HTTPS, no account needed" -ForegroundColor Gray
Write-Host ""
