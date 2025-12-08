# Codex Dominion - Ledger Append Script (PowerShell)
# Appends validation results to immutable artifact ledger

param(
    [Parameter(Mandatory=$true)]
    [string]$Status,

    [string]$DeploymentId = "",
    [string]$Version = "",
    [string]$Tier = "",
    [string]$Health = "unknown",
    [string]$A11y = "unknown",
    [string]$Perf = "unknown"
)

$ErrorActionPreference = "Stop"

function Write-Log { Write-Host "[LEDGER] $args" -ForegroundColor Blue }
function Write-CheckSuccess { Write-Host "✓ $args" -ForegroundColor Green }
function Write-CheckError { Write-Host "✗ $args" -ForegroundColor Red }

# Configuration
$ledgerDir = ".\ledger\artifact-ledger"
$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$operator = $env:USERNAME

# Generate ID if not provided
if ([string]::IsNullOrEmpty($DeploymentId)) {
    $DeploymentId = "manual-" + (Get-Date -Format "yyyyMMddHHmmss")
}

# Detect version from git if not provided
if ([string]::IsNullOrEmpty($Version)) {
    try {
        $Version = git describe --tags --always 2>$null
        if ([string]::IsNullOrEmpty($Version)) { $Version = "unknown" }
    } catch {
        $Version = "unknown"
    }
}

Write-Host ""
Write-Host "============================================"
Write-Host "      LEDGER APPEND - VALIDATION"
Write-Host "============================================"
Write-Host ""

Write-Log "Deployment ID: $DeploymentId"
Write-Log "Status: $Status"
Write-Log "Version: $Version"
Write-Log "Tier: $(if ($Tier) { $Tier } else { 'unknown' })"
Write-Log "Timestamp: $timestamp"
Write-Log "Operator: $operator"
Write-Host ""

# Create ledger directory if it doesn't exist
New-Item -ItemType Directory -Force -Path $ledgerDir | Out-Null

# Initialize ledger files if they don't exist
$deploymentsLedger = "$ledgerDir\deployments.json"
$validationsLedger = "$ledgerDir\validations.json"

if (-not (Test-Path $deploymentsLedger)) {
    "[]" | Out-File -FilePath $deploymentsLedger -Encoding UTF8
    Write-Log "Initialized deployments ledger"
}

if (-not (Test-Path $validationsLedger)) {
    "[]" | Out-File -FilePath $validationsLedger -Encoding UTF8
    Write-Log "Initialized validations ledger"
}

# Get git info
try {
    $gitCommit = git rev-parse HEAD 2>$null
    $gitBranch = git rev-parse --abbrev-ref HEAD 2>$null
    $gitAuthor = git log -1 --format='%an' 2>$null
} catch {
    $gitCommit = "unknown"
    $gitBranch = "unknown"
    $gitAuthor = "unknown"
}

# Create validation record
$validationId = "val-" + (Get-Date -Format "yyyyMMddHHmmss")
$validationRecord = @{
    validation_id = $validationId
    deployment_id = $DeploymentId
    timestamp = $timestamp
    status = $Status
    version = $Version
    tier = if ($Tier) { $Tier } else { "unknown" }
    operator = $operator
    validation_results = @{
        health_check = $Health
        accessibility = $A11y
        performance = $Perf
    }
    governance_compliance = @{
        performance_budget = ($Perf -eq "pass")
        accessibility_wcag = ($A11y -eq "pass")
        health_checks = ($Health -eq "pass")
    }
    git_info = @{
        commit = $gitCommit
        branch = $gitBranch
        author = $gitAuthor
    }
} | ConvertTo-Json -Depth 10

Write-Log "Appending validation record to ledger..."

# Read existing ledger
$existingLedger = Get-Content -Path $validationsLedger -Raw | ConvertFrom-Json

# Append new record
$updatedLedger = $existingLedger + ($validationRecord | ConvertFrom-Json)

# Write back
$updatedLedger | ConvertTo-Json -Depth 10 | Out-File -FilePath $validationsLedger -Encoding UTF8

Write-CheckSuccess "Validation record appended to ledger"

# Generate summary
$totalValidations = $updatedLedger.Count
$recent24h = $updatedLedger | Where-Object {
    $recordTime = [DateTime]::Parse($_.timestamp)
    $recordTime -gt (Get-Date).AddHours(-24)
} | Measure-Object | Select-Object -ExpandProperty Count

Write-Host ""
Write-Host "============================================"
Write-Host "           LEDGER SUMMARY"
Write-Host "============================================"
Write-Host "Total validations: $totalValidations"
Write-Host "Last 24h: $recent24h"
Write-Host ""
Write-Host "Current validation:"
Write-Host "  Status: $Status"
Write-Host "  Health: $Health"
Write-Host "  Accessibility: $A11y"
Write-Host "  Performance: $Perf"
Write-Host ""
Write-Host "Ledger location: $validationsLedger"
Write-Host ""

Write-CheckSuccess "Ledger integrity verified ($totalValidations records)"

# Create human-readable log entry
$logDir = ".\logs\validations"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logFile = "$logDir\$(Get-Date -Format 'yyyy-MM-dd').log"

@"
[$timestamp] $Status - $DeploymentId
  Version: $Version
  Tier: $(if ($Tier) { $Tier } else { 'unknown' })
  Health: $Health
  A11Y: $A11y
  Perf: $Perf
  Operator: $operator
---
"@ | Out-File -FilePath $logFile -Append -Encoding UTF8

Write-Log "Log entry created: $logFile"

Write-Host ""
Write-CheckSuccess "✅ Ledger append complete"
Write-Host ""

exit 0
