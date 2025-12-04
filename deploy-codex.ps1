# =============================================================================
# CODEX DOMINION - PowerShell Deployment Script
# =============================================================================
# Windows-native deployment script
# =============================================================================

param(
    [Parameter(Mandatory=$false)]
    [string]$ServerIP,

    [Parameter(Mandatory=$false)]
    [string]$Username,

    [Parameter(Mandatory=$false)]
    [string]$SSHKey = "$HOME\.ssh\id_rsa"
)

Write-Host "🔥 CODEX DOMINION - WINDOWS DEPLOYMENT 🔥" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Prompt for credentials if not provided
if (-not $ServerIP) {
    $ServerIP = Read-Host "Enter IONOS Server IP Address"
}
if (-not $Username) {
    $Username = Read-Host "Enter IONOS Username"
}

Write-Host ""
Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Server: $ServerIP"
Write-Host "  User:   $Username"
Write-Host "  SSH Key: $SSHKey"
Write-Host ""

# Set environment variables
$env:IONOS_SERVER = $ServerIP
$env:IONOS_USER = $Username
$env:SSH_KEY = $SSHKey

# Check if Git Bash or WSL is available
$bashPath = $null
$isWSL = $false

# Check for Git Bash first (preferred for Windows paths)
if (Test-Path "C:\Program Files\Git\bin\bash.exe") {
    $bashPath = "C:\Program Files\Git\bin\bash.exe"
    Write-Host "✓ Found Git Bash: $bashPath" -ForegroundColor Green
} elseif (Test-Path "C:\Program Files (x86)\Git\bin\bash.exe") {
    $bashPath = "C:\Program Files (x86)\Git\bin\bash.exe"
    Write-Host "✓ Found Git Bash: $bashPath" -ForegroundColor Green
} elseif (Get-Command "wsl.exe" -ErrorAction SilentlyContinue) {
    Write-Host "✓ Found WSL" -ForegroundColor Green
    $bashPath = "wsl"
    $isWSL = $true
} else {
    Write-Host "✗ Neither Git Bash nor WSL found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install one of the following:" -ForegroundColor Yellow
    Write-Host "  1. Git Bash: https://git-scm.com/download/win"
    Write-Host "  2. WSL: Run 'wsl --install' in admin PowerShell"
    Write-Host ""
    exit 1
}

Write-Host ""
$confirm = Read-Host "Ready to deploy? (Y/N)"
if ($confirm -ne 'Y' -and $confirm -ne 'y') {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Starting deployment..." -ForegroundColor Cyan
Write-Host ""

# Run the bash deployment script
if ($isWSL) {
    # Convert Windows path to WSL path (/mnt/c/...)
    $wslPath = $PWD.Path -replace '^([A-Z]):', { "/mnt/$($_.Groups[1].Value.ToLower())" } -replace '\\', '/'
    $wslSSHKey = $SSHKey -replace '^([A-Z]):', { "/mnt/$($_.Groups[1].Value.ToLower())" } -replace '\\', '/'
    wsl bash -c "cd '$wslPath' && export IONOS_SERVER='$ServerIP' && export IONOS_USER='$Username' && export SSH_KEY='$wslSSHKey' && bash deploy-ionos.sh"
} else {
    # Convert Windows path to Git Bash format (/c/...)
    $gitBashPath = $PWD.Path -replace '^([A-Z]):', { "/$($_.Groups[1].Value.ToLower())" } -replace '\\', '/'
    $sshKeyPath = $SSHKey -replace '^([A-Z]):', { "/$($_.Groups[1].Value.ToLower())" } -replace '\\', '/'
    & $bashPath -c "cd '$gitBashPath' && export IONOS_SERVER='$ServerIP' && export IONOS_USER='$Username' && export SSH_KEY='$sshKeyPath' && bash deploy-ionos.sh"
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your application is now live at:" -ForegroundColor Cyan
    Write-Host "  https://codexdominion.app"
    Write-Host "  https://api.codexdominion.app"
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "✗ Deployment encountered errors" -ForegroundColor Red
    Write-Host "Check the output above for details" -ForegroundColor Yellow
    Write-Host ""
}
