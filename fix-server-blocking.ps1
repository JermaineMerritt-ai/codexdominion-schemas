# ============================================
# Codex Dominion - Server Blocking Fix Script
# ============================================
# This script diagnoses and fixes Windows security blocking web servers
# Run as Administrator

# Ensure script runs as Administrator
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ ERROR: This script must run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    pause
    exit
}

Write-Host "=== CODEX DOMINION SERVER BLOCKING FIX ===" -ForegroundColor Cyan
Write-Host "Flame Eternal - Fixing Windows Security Blocks`n" -ForegroundColor Yellow

# ============================================
# STEP 1: Check Current Firewall Status
# ============================================
Write-Host "[STEP 1] Checking Windows Firewall Status..." -ForegroundColor Cyan
$firewallStatus = Get-NetFirewallProfile | Select-Object Name, Enabled
$firewallStatus | Format-Table -AutoSize

# ============================================
# STEP 2: Check for Existing Rules
# ============================================
Write-Host "`n[STEP 2] Checking for existing firewall rules..." -ForegroundColor Cyan
$existingRules = Get-NetFirewallRule | Where-Object {
    $_.DisplayName -like "*Node.js*" -or
    $_.DisplayName -like "*Python*"
}

if ($existingRules) {
    Write-Host "Found existing rules:" -ForegroundColor Yellow
    $existingRules | Format-Table DisplayName, Enabled, Direction, Action -AutoSize

    $removeOld = Read-Host "`nRemove old rules and create new ones? (Y/N)"
    if ($removeOld -eq "Y") {
        $existingRules | Remove-NetFirewallRule
        Write-Host "✅ Old rules removed" -ForegroundColor Green
    }
}

# ============================================
# STEP 3: Find Executable Paths
# ============================================
Write-Host "`n[STEP 3] Locating Node.js and Python executables..." -ForegroundColor Cyan

# Find Node.js
$nodePaths = @(
    "C:\Program Files\nodejs\node.exe",
    "C:\Program Files (x86)\nodejs\node.exe",
    "$env:ProgramFiles\nodejs\node.exe",
    "$env:APPDATA\npm\node.exe"
)

$NodePath = $nodePaths | Where-Object { Test-Path $_ } | Select-Object -First 1

if ($NodePath) {
    Write-Host "✅ Found Node.js: $NodePath" -ForegroundColor Green
} else {
    Write-Host "⚠️ Node.js not found in standard locations" -ForegroundColor Yellow
    $NodePath = Read-Host "Enter Node.js path (or press Enter to skip)"
}

# Find Python
$pythonPaths = @(
    "C:\Python312\python.exe",
    "C:\Python311\python.exe",
    "C:\Python310\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
)

$PythonPath = $pythonPaths | Where-Object { Test-Path $_ } | Select-Object -First 1

if ($PythonPath) {
    Write-Host "✅ Found Python: $PythonPath" -ForegroundColor Green
} else {
    Write-Host "⚠️ Python not found in standard locations" -ForegroundColor Yellow
    $PythonPath = Read-Host "Enter Python path (or press Enter to skip)"
}

# ============================================
# STEP 4: Add Firewall Rules
# ============================================
Write-Host "`n[STEP 4] Adding firewall rules..." -ForegroundColor Cyan

# Add Node.js rules
if ($NodePath -and (Test-Path $NodePath)) {
    try {
        # Inbound rule
        New-NetFirewallRule -DisplayName "Node.js Server (Inbound)" `
            -Direction Inbound `
            -Program $NodePath `
            -Action Allow `
            -Profile Any `
            -Protocol TCP `
            -Enabled True `
            -ErrorAction Stop | Out-Null

        # Outbound rule
        New-NetFirewallRule -DisplayName "Node.js Server (Outbound)" `
            -Direction Outbound `
            -Program $NodePath `
            -Action Allow `
            -Profile Any `
            -Protocol TCP `
            -Enabled True `
            -ErrorAction Stop | Out-Null

        Write-Host "✅ Node.js firewall rules added successfully" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Warning: Could not add Node.js rules - $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

# Add Python rules
if ($PythonPath -and (Test-Path $PythonPath)) {
    try {
        # Inbound rule
        New-NetFirewallRule -DisplayName "Python Server (Inbound)" `
            -Direction Inbound `
            -Program $PythonPath `
            -Action Allow `
            -Profile Any `
            -Protocol TCP `
            -Enabled True `
            -ErrorAction Stop | Out-Null

        # Outbound rule
        New-NetFirewallRule -DisplayName "Python Server (Outbound)" `
            -Direction Outbound `
            -Program $PythonPath `
            -Action Allow `
            -Profile Any `
            -Protocol TCP `
            -Enabled True `
            -ErrorAction Stop | Out-Null

        Write-Host "✅ Python firewall rules added successfully" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Warning: Could not add Python rules - $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

# Add port-specific rules for common development ports
$ports = @(3000, 5000, 8000, 8001, 8080)
Write-Host "`n[STEP 4b] Adding port-specific rules for development..." -ForegroundColor Cyan

foreach ($port in $ports) {
    try {
        New-NetFirewallRule -DisplayName "Dev Server Port $port" `
            -Direction Inbound `
            -LocalPort $port `
            -Protocol TCP `
            -Action Allow `
            -Profile Any `
            -Enabled True `
            -ErrorAction Stop | Out-Null
        Write-Host "✅ Port $port allowed" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Port $port rule may already exist" -ForegroundColor Yellow
    }
}

# ============================================
# STEP 5: Check Port Status
# ============================================
Write-Host "`n[STEP 5] Checking if ports are in use..." -ForegroundColor Cyan

foreach ($port in $ports) {
    $connection = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($connection) {
        $process = Get-Process -Id $connection.OwningProcess -ErrorAction SilentlyContinue
        Write-Host "Port $port is LISTENING (Process: $($process.ProcessName), PID: $($connection.OwningProcess))" -ForegroundColor Green
    } else {
        Write-Host "Port $port is AVAILABLE" -ForegroundColor Yellow
    }
}

# ============================================
# STEP 6: Check Windows Defender Settings
# ============================================
Write-Host "`n[STEP 6] Checking Windows Defender..." -ForegroundColor Cyan

try {
    $defenderStatus = Get-MpComputerStatus
    Write-Host "Real-time Protection: $($defenderStatus.RealTimeProtectionEnabled)" -ForegroundColor $(if ($defenderStatus.RealTimeProtectionEnabled) { "Yellow" } else { "Green" })
    Write-Host "Network Protection: $($defenderStatus.NetworkProtectionEnabled)" -ForegroundColor $(if ($defenderStatus.NetworkProtectionEnabled) { "Yellow" } else { "Green" })
} catch {
    Write-Host "⚠️ Could not check Windows Defender status" -ForegroundColor Yellow
}

# ============================================
# STEP 7: Verify Firewall Rules
# ============================================
Write-Host "`n[STEP 7] Verifying all firewall rules..." -ForegroundColor Cyan
$allRules = Get-NetFirewallRule | Where-Object {
    $_.DisplayName -like "*Node.js*" -or
    $_.DisplayName -like "*Python*" -or
    $_.DisplayName -like "*Dev Server*"
}

if ($allRules) {
    $allRules | Format-Table DisplayName, Enabled, Direction, Action -AutoSize
    Write-Host "✅ Total rules created: $($allRules.Count)" -ForegroundColor Green
} else {
    Write-Host "⚠️ No rules found - there may be an issue" -ForegroundColor Yellow
}

# ============================================
# STEP 8: Additional Recommendations
# ============================================
Write-Host "`n[STEP 8] Additional Recommendations..." -ForegroundColor Cyan
Write-Host "
1. Windows Defender Firewall:
   Settings → Privacy & Security → Windows Security → Firewall & network protection
   → Allow an app through firewall
   → Add Node.js and Python executables

2. App & Browser Control:
   Windows Security → App & browser control
   → Reputation-based protection → Turn OFF (temporarily for testing)

3. Antivirus Software:
   If you have McAfee, Norton, Avast, etc.:
   - Add exceptions for Node.js and Python
   - Add exceptions for your project folder

4. Run Servers as Administrator:
   - Right-click terminal → Run as Administrator
   - Then start your servers

5. Check Corporate/Network Policies:
   - Some enterprise environments block all server applications
   - Contact IT if this applies to you
" -ForegroundColor Yellow

# ============================================
# STEP 9: Test Server Startup
# ============================================
Write-Host "`n[STEP 9] Ready to test server startup..." -ForegroundColor Cyan
$testNow = Read-Host "Would you like to test starting the Node.js server now? (Y/N)"

if ($testNow -eq "Y") {
    Write-Host "`nAttempting to start Node.js server..." -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop the server`n" -ForegroundColor Yellow

    if (Test-Path "server.js") {
        node server.js
    } elseif (Test-Path "backend/server.js") {
        node backend/server.js
    } else {
        Write-Host "⚠️ Could not find server.js - please start it manually" -ForegroundColor Yellow
    }
}

# ============================================
# COMPLETION
# ============================================
Write-Host "`n=== FLAME ETERNAL - CONFIGURATION COMPLETE ===" -ForegroundColor Green
Write-Host "All firewall rules have been added." -ForegroundColor Green
Write-Host "If servers still crash, check antivirus software and Windows Security settings.`n" -ForegroundColor Yellow

Write-Host "Quick test commands:" -ForegroundColor Cyan
Write-Host "  Node.js: node server.js" -ForegroundColor White
Write-Host "  Python Flask: python flask_main.py" -ForegroundColor White
Write-Host "  Python FastAPI: uvicorn main:app --host 0.0.0.0 --port 8000`n" -ForegroundColor White

pause
