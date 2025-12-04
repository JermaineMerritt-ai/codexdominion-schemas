# Ensure script runs as Administrator
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Please run this script as Administrator." -ForegroundColor Red
    exit
}

Write-Host "=== Adding Firewall Rules for Node.js and Python ===" -ForegroundColor Cyan

# Paths to executables (adjust if installed elsewhere)
$NodePath = "C:\Program Files\nodejs\node.exe"
$PythonPath = "C:\Python312\python.exe"

# Add firewall rule for Node.js
try {
    New-NetFirewallRule -DisplayName "Node.js Server" -Direction Inbound -Program $NodePath -Action Allow -Profile Any -Protocol TCP -ErrorAction Stop
    Write-Host "✅ Firewall rule added for Node.js" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Warning: Node.js firewall rule may already exist or path is incorrect." -ForegroundColor Yellow
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Add firewall rule for Python
try {
    New-NetFirewallRule -DisplayName "Python Server" -Direction Inbound -Program $PythonPath -Action Allow -Profile Any -Protocol TCP -ErrorAction Stop
    Write-Host "✅ Firewall rule added for Python" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Warning: Python firewall rule may already exist or path is incorrect." -ForegroundColor Yellow
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "`n=== Verifying Firewall Rules ===" -ForegroundColor Cyan
Get-NetFirewallRule | Where-Object { $_.DisplayName -like "*Node.js*" -or $_.DisplayName -like "*Python*" } | Format-Table DisplayName, Enabled, Direction, Action

Write-Host "`n=== Checking if Ports are Listening (3000, 5000, 8001) ===" -ForegroundColor Cyan
$ports = @(3000, 5000, 8001)
foreach ($port in $ports) {
    $connection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($connection) {
        Write-Host "✅ Port $port is OPEN and listening." -ForegroundColor Green
    } else {
        Write-Host "⚠️ Port $port is NOT listening. Start your server and re-check." -ForegroundColor Yellow
    }
}

Write-Host "`n=== Reminder: Allow Apps Through Windows Defender Firewall ===" -ForegroundColor Cyan
Write-Host "Go to: Settings → Privacy & Security → Windows Security → Firewall & network protection → Allow an app through firewall" -ForegroundColor Yellow
Write-Host "Ensure Node.js and Python are allowed for Private and Public networks." -ForegroundColor Yellow

Write-Host "`n✅ Firewall rules applied and verification complete!" -ForegroundColor Green
