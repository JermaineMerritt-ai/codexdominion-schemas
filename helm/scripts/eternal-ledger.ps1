# Eternal Ledger - Helm Action Logger (PowerShell)
# Archives every Helm operation for lineage preservation
# Lineage: Preserved | Archive: Enabled

param(
    [Parameter(Position=0)]
    [ValidateSet('install', 'upgrade', 'rollback', 'uninstall', 'log', 'view', 'query', 'backup', 'init', 'help')]
    [string]$Command = 'help',
    
    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$ErrorActionPreference = 'Stop'
$LedgerPath = if ($env:ETERNAL_LEDGER_PATH) { $env:ETERNAL_LEDGER_PATH } else { "$env:ProgramData\eternal-ledger\ledger.json" }
$LedgerDir = Split-Path -Parent $LedgerPath

# Initialize ledger if not exists
function Initialize-Ledger {
    if (-not (Test-Path $LedgerPath)) {
        New-Item -ItemType Directory -Path $LedgerDir -Force | Out-Null
        
        $genesisBlock = @{
            genesis_block = @{
                timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
                principles = @("Archive", "Lineage", "Ceremonial Closure")
                signatures = @{
                    crown = @("Efficiency", "Knowledge", "Commerce", "Companion")
                    council = @("Law", "Healthcare", "Commerce", "Education", "AI", "Family")
                }
            }
            releases = @()
        } | ConvertTo-Json -Depth 10
        
        Set-Content -Path $LedgerPath -Value $genesisBlock -Encoding UTF8
        Write-Host "✓ Eternal Ledger genesis block created at $LedgerPath" -ForegroundColor Green
    }
}

# Log Helm action to Eternal Ledger
function Add-LedgerEntry {
    param(
        [string]$Action,
        [string]$Release,
        [string]$Namespace,
        [string]$Revision = "N/A",
        [string]$ChartVersion = "N/A",
        [string]$Status = "unknown"
    )
    
    Initialize-Ledger
    
    $timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    
    $entry = @{
        action = $Action
        release = $Release
        namespace = $Namespace
        revision = $Revision
        chart_version = $ChartVersion
        status = $Status
        timestamp = $timestamp
        operator = $env:USERNAME
        host = $env:COMPUTERNAME
        signatures = @{
            crown = @("Efficiency", "Knowledge", "Commerce", "Companion")
            council = @("Law", "Healthcare", "Commerce", "Education", "AI", "Family")
        }
        lineage_preserved = $true
    }
    
    # Read existing ledger
    $ledger = Get-Content -Path $LedgerPath -Raw | ConvertFrom-Json
    
    # Append entry
    $ledger.releases += $entry
    
    # Write back
    $ledger | ConvertTo-Json -Depth 10 | Set-Content -Path $LedgerPath -Encoding UTF8
    
    Write-Host "✓ Logged $Action for $Release (revision $Revision) to Eternal Ledger" -ForegroundColor Green
}

# Get latest revision for a release
function Get-LatestRevision {
    param([string]$Release, [string]$Namespace)
    
    try {
        $history = helm history $Release --namespace $Namespace --max 1 -o json 2>$null | ConvertFrom-Json
        return $history[0].revision
    } catch {
        return "unknown"
    }
}

# Get chart version from release
function Get-ChartVersion {
    param([string]$Release, [string]$Namespace)
    
    try {
        $list = helm list --namespace $Namespace -o json 2>$null | ConvertFrom-Json
        $release = $list | Where-Object { $_.name -eq $Release }
        return $release.chart
    } catch {
        return "unknown"
    }
}

# Get release status
function Get-ReleaseStatus {
    param([string]$Release, [string]$Namespace)
    
    try {
        $status = helm status $Release --namespace $Namespace -o json 2>$null | ConvertFrom-Json
        return $status.info.status
    } catch {
        return "unknown"
    }
}

# Helm install with logging
function Invoke-HelmInstall {
    param([string[]]$Args)
    
    $Release = $Args[0]
    $Chart = $Args[1]
    $Namespace = $Args[2]
    $HelmArgs = $Args[3..($Args.Length-1)]
    
    Write-Host "⏳ Installing $Release from $Chart..." -ForegroundColor Cyan
    
    try {
        helm install $Release $Chart --namespace $Namespace --create-namespace @HelmArgs
        
        $Revision = Get-LatestRevision -Release $Release -Namespace $Namespace
        $ChartVersion = Get-ChartVersion -Release $Release -Namespace $Namespace
        $Status = Get-ReleaseStatus -Release $Release -Namespace $Namespace
        
        Add-LedgerEntry -Action "install" -Release $Release -Namespace $Namespace `
            -Revision $Revision -ChartVersion $ChartVersion -Status $Status
        
        Write-Host "✓ Installation complete and logged" -ForegroundColor Green
    } catch {
        Add-LedgerEntry -Action "install_failed" -Release $Release -Namespace $Namespace `
            -Revision "N/A" -ChartVersion "N/A" -Status "failed"
        Write-Host "✗ Installation failed and logged: $_" -ForegroundColor Red
        exit 1
    }
}

# Helm upgrade with logging
function Invoke-HelmUpgrade {
    param([string[]]$Args)
    
    $Release = $Args[0]
    $Chart = $Args[1]
    $Namespace = $Args[2]
    $HelmArgs = $Args[3..($Args.Length-1)]
    
    Write-Host "⏳ Upgrading $Release from $Chart..." -ForegroundColor Cyan
    
    try {
        helm upgrade $Release $Chart --namespace $Namespace @HelmArgs
        
        $Revision = Get-LatestRevision -Release $Release -Namespace $Namespace
        $ChartVersion = Get-ChartVersion -Release $Release -Namespace $Namespace
        $Status = Get-ReleaseStatus -Release $Release -Namespace $Namespace
        
        Add-LedgerEntry -Action "upgrade" -Release $Release -Namespace $Namespace `
            -Revision $Revision -ChartVersion $ChartVersion -Status $Status
        
        Write-Host "✓ Upgrade complete and logged" -ForegroundColor Green
    } catch {
        Add-LedgerEntry -Action "upgrade_failed" -Release $Release -Namespace $Namespace `
            -Revision "N/A" -ChartVersion "N/A" -Status "failed"
        Write-Host "✗ Upgrade failed and logged: $_" -ForegroundColor Red
        exit 1
    }
}

# Helm rollback with logging
function Invoke-HelmRollback {
    param([string[]]$Args)
    
    $Release = $Args[0]
    $Namespace = $Args[1]
    $TargetRevision = if ($Args[2]) { $Args[2] } else { "0" }
    
    Write-Host "⏳ Rolling back $Release to revision $TargetRevision..." -ForegroundColor Cyan
    
    try {
        helm rollback $Release $TargetRevision --namespace $Namespace
        
        $Revision = Get-LatestRevision -Release $Release -Namespace $Namespace
        $ChartVersion = Get-ChartVersion -Release $Release -Namespace $Namespace
        $Status = Get-ReleaseStatus -Release $Release -Namespace $Namespace
        
        Add-LedgerEntry -Action "rollback" -Release $Release -Namespace $Namespace `
            -Revision $Revision -ChartVersion $ChartVersion -Status $Status
        
        Write-Host "✓ Rollback complete and logged" -ForegroundColor Green
    } catch {
        Add-LedgerEntry -Action "rollback_failed" -Release $Release -Namespace $Namespace `
            -Revision $TargetRevision -ChartVersion "N/A" -Status "failed"
        Write-Host "✗ Rollback failed and logged: $_" -ForegroundColor Red
        exit 1
    }
}

# Helm uninstall with logging
function Invoke-HelmUninstall {
    param([string[]]$Args)
    
    $Release = $Args[0]
    $Namespace = $Args[1]
    
    Write-Host "⏳ Uninstalling $Release (preserving history)..." -ForegroundColor Cyan
    
    $Revision = Get-LatestRevision -Release $Release -Namespace $Namespace
    $ChartVersion = Get-ChartVersion -Release $Release -Namespace $Namespace
    
    try {
        helm uninstall $Release --namespace $Namespace --keep-history
        
        Add-LedgerEntry -Action "uninstall" -Release $Release -Namespace $Namespace `
            -Revision $Revision -ChartVersion $ChartVersion -Status "uninstalled"
        
        Write-Host "✓ Uninstall complete and logged (history preserved)" -ForegroundColor Green
    } catch {
        Add-LedgerEntry -Action "uninstall_failed" -Release $Release -Namespace $Namespace `
            -Revision $Revision -ChartVersion $ChartVersion -Status "failed"
        Write-Host "✗ Uninstall failed and logged: $_" -ForegroundColor Red
        exit 1
    }
}

# View ledger contents
function Show-Ledger {
    if (-not (Test-Path $LedgerPath)) {
        Write-Host "✗ No ledger found at $LedgerPath" -ForegroundColor Red
        return
    }
    
    Write-Host "📜 Eternal Ledger Contents:" -ForegroundColor Cyan
    Get-Content -Path $LedgerPath -Raw | ConvertFrom-Json | ConvertTo-Json -Depth 10 | Write-Host
}

# Query ledger by release name
function Find-LedgerEntries {
    param([string]$Release)
    
    if (-not (Test-Path $LedgerPath)) {
        Write-Host "✗ No ledger found at $LedgerPath" -ForegroundColor Red
        return
    }
    
    Write-Host "📜 Ledger entries for release '$Release':" -ForegroundColor Cyan
    
    $ledger = Get-Content -Path $LedgerPath -Raw | ConvertFrom-Json
    $entries = $ledger.releases | Where-Object { $_.release -eq $Release }
    
    if ($entries) {
        $entries | ConvertTo-Json -Depth 10 | Write-Host
    } else {
        Write-Host "No entries found for release '$Release'" -ForegroundColor Yellow
    }
}

# Backup ledger
function Backup-Ledger {
    if (-not (Test-Path $LedgerPath)) {
        Write-Host "✗ No ledger to backup" -ForegroundColor Red
        return
    }
    
    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backupPath = "$LedgerPath.backup.$timestamp"
    
    Copy-Item -Path $LedgerPath -Destination $backupPath
    Write-Host "✓ Ledger backed up to $backupPath" -ForegroundColor Green
}

# Show help
function Show-Help {
    Write-Host @"
Eternal Ledger - Helm Action Logger (PowerShell)
Usage: .\eternal-ledger.ps1 <command> [args...]

Commands:
  install <release> <chart> <namespace> [helm-args...]
      Install a chart and log to ledger
      
  upgrade <release> <chart> <namespace> [helm-args...]
      Upgrade a release and log to ledger
      
  rollback <release> <namespace> [revision]
      Rollback a release and log to ledger
      
  uninstall <release> <namespace>
      Uninstall a release (keep history) and log to ledger
      
  log <action> <release> <namespace> [revision] [chart_version] [status]
      Manually log an action to ledger
      
  view
      View entire ledger contents
      
  query <release>
      Query ledger for specific release
      
  backup
      Create timestamped backup of ledger
      
  init
      Initialize genesis block

Environment Variables:
  ETERNAL_LEDGER_PATH    Path to ledger file (default: C:\ProgramData\eternal-ledger\ledger.json)

Examples:
  # Install with logging
  .\eternal-ledger.ps1 install codexdominion ./codexdominion codexdominion -f working-values.yaml
  
  # Upgrade with logging
  .\eternal-ledger.ps1 upgrade codexdominion ./codexdominion codexdominion -f working-values.yaml --history-max 10
  
  # Rollback with logging
  .\eternal-ledger.ps1 rollback codexdominion codexdominion 3
  
  # View all logged actions
  .\eternal-ledger.ps1 view
  
  # Query specific release
  .\eternal-ledger.ps1 query codexdominion
  
  # Backup ledger
  .\eternal-ledger.ps1 backup

Eternal Principles: Archive · Lineage · Ceremonial Closure
"@ -ForegroundColor White
}

# Main command dispatcher
switch ($Command) {
    'install' {
        Invoke-HelmInstall -Args $Arguments
    }
    'upgrade' {
        Invoke-HelmUpgrade -Args $Arguments
    }
    'rollback' {
        Invoke-HelmRollback -Args $Arguments
    }
    'uninstall' {
        Invoke-HelmUninstall -Args $Arguments
    }
    'log' {
        Add-LedgerEntry -Action $Arguments[0] -Release $Arguments[1] -Namespace $Arguments[2] `
            -Revision $Arguments[3] -ChartVersion $Arguments[4] -Status $Arguments[5]
    }
    'view' {
        Show-Ledger
    }
    'query' {
        Find-LedgerEntries -Release $Arguments[0]
    }
    'backup' {
        Backup-Ledger
    }
    'init' {
        Initialize-Ledger
    }
    default {
        Show-Help
    }
}
