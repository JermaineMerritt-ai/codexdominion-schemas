# Windows Firewall Configuration for Codex Dominion
# Run this script as Administrator

Write-Host "🔥 CODEX DOMINION FIREWALL CONFIGURATION" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Check if running as Administrator
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
$isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ ERROR: This script must be run as Administrator" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Running with Administrator privileges" -ForegroundColor Green
Write-Host ""

# Configure firewall rules
try {
    Write-Host "🌐 Configuring HTTP (Port 80)..." -ForegroundColor Yellow
    netsh advfirewall firewall add rule name="Codex Dominion HTTP" dir=in action=allow protocol=TCP localport=80
    Write-Host "✅ Port 80 (HTTP) allowed" -ForegroundColor Green

    Write-Host "🔒 Configuring HTTPS (Port 443)..." -ForegroundColor Yellow
    netsh advfirewall firewall add rule name="Codex Dominion HTTPS" dir=in action=allow protocol=TCP localport=443
    Write-Host "✅ Port 443 (HTTPS) allowed" -ForegroundColor Green

    Write-Host "⚡ Configuring API Port (8000)..." -ForegroundColor Yellow
    netsh advfirewall firewall add rule name="Codex Dominion API" dir=in action=allow protocol=TCP localport=8000
    Write-Host "✅ Port 8000 (API) allowed" -ForegroundColor Green

    Write-Host "📊 Configuring Dashboard Ports..." -ForegroundColor Yellow
    netsh advfirewall firewall add rule name="Codex Dominion Dashboard" dir=in action=allow protocol=TCP localport=8501
    netsh advfirewall firewall add rule name="Codex Dominion Portfolio" dir=in action=allow protocol=TCP localport=8503
    Write-Host "✅ Ports 8501, 8503 (Dashboards) allowed" -ForegroundColor Green

    Write-Host "🔄 Configuring Proxy Port (3000)..." -ForegroundColor Yellow
    netsh advfirewall firewall add rule name="Codex Dominion Proxy" dir=in action=allow protocol=TCP localport=3000
    Write-Host "✅ Port 3000 (Proxy) allowed" -ForegroundColor Green

} catch {
    Write-Host "❌ ERROR: Failed to configure firewall rules" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎯 FIREWALL CONFIGURATION COMPLETE!" -ForegroundColor Green
Write-Host "=" * 40 -ForegroundColor Green

# Display current firewall rules for our ports
Write-Host "📋 Current Firewall Rules:" -ForegroundColor Cyan
netsh advfirewall firewall show rule name="Codex Dominion HTTP"
netsh advfirewall firewall show rule name="Codex Dominion HTTPS"
netsh advfirewall firewall show rule name="Codex Dominion API"
netsh advfirewall firewall show rule name="Codex Dominion Dashboard"
netsh advfirewall firewall show rule name="Codex Dominion Portfolio"
netsh advfirewall firewall show rule name="Codex Dominion Proxy"

Write-Host ""
Write-Host "✨ Your Codex Dominion services are now accessible:" -ForegroundColor Green
Write-Host "🌐 HTTP: Port 80" -ForegroundColor White
Write-Host "🔒 HTTPS: Port 443" -ForegroundColor White
Write-Host "⚡ API: Port 8000" -ForegroundColor White
Write-Host "📊 Main Dashboard: Port 8501" -ForegroundColor White
Write-Host "💼 Portfolio: Port 8503" -ForegroundColor White
Write-Host "🔄 Proxy: Port 3000" -ForegroundColor White

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
