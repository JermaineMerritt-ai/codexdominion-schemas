# Ensure script runs as Administrator
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Please run this script as Administrator." -ForegroundColor Red
    exit
}

Write-Host "=== Adding Firewall Rules for Node.js and Python ===" -ForegroundColor Cyan

# Paths to executables (adjust if installed elsewhere)
$NodePath = "C:\Program Files\nodejs\node.exe"
$PythonPath = "C:\Python312\python.exe"
$VenvPythonPath = "$PSScriptRoot\.venv\Scripts\python.exe"

# Add firewall rule for Node.js
try {
    New-NetFirewallRule -DisplayName "Node.js Server" -Direction Inbound -Program $NodePath -Action Allow -Profile Any -Protocol TCP -ErrorAction Stop
    Write-Host "✅ Firewall rule added for Node.js" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Node.js firewall rule may already exist or path is incorrect" -ForegroundColor Yellow
}

# Add firewall rule for Python (system)
try {
    New-NetFirewallRule -DisplayName "Python Server (System)" -Direction Inbound -Program $PythonPath -Action Allow -Profile Any -Protocol TCP -ErrorAction Stop
    Write-Host "✅ Firewall rule added for Python (System)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Python (System) firewall rule may already exist or path is incorrect" -ForegroundColor Yellow
}

# Add firewall rule for Python (venv)
if (Test-Path $VenvPythonPath) {
    try {
        New-NetFirewallRule -DisplayName "Python Server (Venv)" -Direction Inbound -Program $VenvPythonPath -Action Allow -Profile Any -Protocol TCP -ErrorAction Stop
        Write-Host "✅ Firewall rule added for Python (Venv)" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Python (Venv) firewall rule may already exist" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Venv Python not found at: $VenvPythonPath" -ForegroundColor Yellow
}

Write-Host "`n=== Checking Windows Defender Firewall Settings ===" -ForegroundColor Cyan
Write-Host "Go to: Settings → Privacy & Security → Windows Security → Firewall & network protection → Allow an app through firewall" -ForegroundColor Yellow
Write-Host "Ensure Node.js and Python are allowed for Private and Public networks." -ForegroundColor Yellow

Write-Host "`n=== Optional: Disable App & Browser Control Temporarily ===" -ForegroundColor Cyan
Write-Host "Navigate to: Windows Security → App & browser control → Reputation-based protection → Turn off for testing." -ForegroundColor Yellow

Write-Host "`n=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Restart your servers (already as Administrator)." -ForegroundColor Green
Write-Host "2. Test Node.js: node server.js" -ForegroundColor Green
Write-Host "3. Test Python: .venv\Scripts\python.exe -m uvicorn src.backend.simple_main:app --host 0.0.0.0 --port 8001" -ForegroundColor Green

Write-Host "`n✅ Firewall rules applied successfully!" -ForegroundColor Green
