# Codex Dominion - Add Windows Firewall Rules for Node.js Development
# This script must be run as Administrator

Write-Host "🔥 Adding Windows Firewall rules for Node.js backend..." -ForegroundColor Cyan

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ This script requires Administrator privileges" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator', then run this script again" -ForegroundColor Yellow
    exit 1
}

# Remove existing rules if they exist (to avoid duplicates)
Write-Host "`nRemoving any existing rules..." -ForegroundColor Gray
Get-NetFirewallRule -DisplayName "Node.js Development Server" -ErrorAction SilentlyContinue | Remove-NetFirewallRule
Get-NetFirewallRule -DisplayName "Port 4000 Development" -ErrorAction SilentlyContinue | Remove-NetFirewallRule
Get-NetFirewallRule -DisplayName "Codex Dominion Backend" -ErrorAction SilentlyContinue | Remove-NetFirewallRule

# Add Node.js executable rule
Write-Host "`n1️⃣ Adding Node.js executable rule..." -ForegroundColor Yellow
try {
    New-NetFirewallRule -DisplayName "Node.js Development Server" `
        -Direction Inbound `
        -Program "C:\Program Files\nodejs\node.exe" `
        -Action Allow `
        -Profile Any `
        -Enabled True | Out-Null
    Write-Host "   ✅ Node.js executable rule added" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Failed to add Node.js rule: $_" -ForegroundColor Red
}

# Add port 4000 specific rule
Write-Host "`n2️⃣ Adding Port 4000 rule..." -ForegroundColor Yellow
try {
    New-NetFirewallRule -DisplayName "Port 4000 Development" `
        -Direction Inbound `
        -LocalPort 4000 `
        -Protocol TCP `
        -Action Allow `
        -Profile Any `
        -Enabled True | Out-Null
    Write-Host "   ✅ Port 4000 rule added" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Failed to add port rule: $_" -ForegroundColor Red
}

# Add comprehensive Codex Dominion rule
Write-Host "`n3️⃣ Adding Codex Dominion backend rule..." -ForegroundColor Yellow
try {
    New-NetFirewallRule -DisplayName "Codex Dominion Backend" `
        -Direction Inbound `
        -LocalPort 3000,4000,8080 `
        -Protocol TCP `
        -Action Allow `
        -Profile Any `
        -Enabled True | Out-Null
    Write-Host "   ✅ Codex Dominion backend rule added (ports 3000, 4000, 8080)" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Failed to add Codex rule: $_" -ForegroundColor Red
}

# Verify rules were added
Write-Host "`n🔍 Verifying firewall rules..." -ForegroundColor Cyan
$rules = Get-NetFirewallRule | Where-Object { $_.DisplayName -like '*Development*' -or $_.DisplayName -like '*Codex*' }
if ($rules) {
    Write-Host "`n✅ Firewall rules successfully added:" -ForegroundColor Green
    $rules | Select-Object DisplayName, Enabled, Direction | Format-Table -AutoSize
} else {
    Write-Host "`n❌ No rules found - something went wrong" -ForegroundColor Red
}

Write-Host "`n🔥 Done! Try starting your backend now." -ForegroundColor Cyan
Write-Host "   Run: npm run start:prod" -ForegroundColor Gray
