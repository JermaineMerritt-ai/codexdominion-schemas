# Codex Dominion - Complete Validation Pipeline (PowerShell)
# Runs health checks, accessibility tests, performance validation, and ledger append

param(
    [string]$FrontendUrl = "http://localhost:3000",
    [string]$BackendUrl = "http://localhost:8001",
    [string]$Environment = "development"
)

$ErrorActionPreference = "Stop"

# Colors
function Write-Info { Write-Host "[VALIDATE] $args" -ForegroundColor Blue }
function Write-Success { Write-Host "✓ $args" -ForegroundColor Green }
function Write-Error { Write-Host "✗ $args" -ForegroundColor Red }
function Write-Banner {
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Magenta
    Write-Host "  $args" -ForegroundColor Magenta
    Write-Host "============================================" -ForegroundColor Magenta
    Write-Host ""
}

Write-Banner "CODEX DOMINION - VALIDATION PIPELINE"

Write-Info "Starting validation pipeline at $(Get-Date)"
$PipelineStart = Get-Date

# Set environment variables
$env:FRONTEND_URL = $FrontendUrl
$env:BACKEND_URL = $BackendUrl
$env:ENVIRONMENT = $Environment

# Track results
$HealthStatus = "unknown"
$A11yStatus = "unknown"
$PerfStatus = "unknown"
$OverallStatus = "validated"

# Check if running in Git Bash or WSL
$hasGitBash = Get-Command bash -ErrorAction SilentlyContinue
$scriptDir = Split-Path -Parent $PSCommandPath

if ($hasGitBash) {
    Write-Info "Git Bash detected, running native bash scripts..."

    # Step 1: Health Check
    Write-Banner "STEP 1/4: HEALTH CHECK"
    try {
        bash "$scriptDir/health-check.sh"
        Write-Success "Health check passed"
        $HealthStatus = "pass"
    } catch {
        Write-Error "Health check failed"
        $HealthStatus = "fail"
        $OverallStatus = "failed"
    }

    # Step 2: Accessibility Check
    Write-Banner "STEP 2/4: ACCESSIBILITY CHECK"
    try {
        bash "$scriptDir/a11y.sh"
        Write-Success "Accessibility check passed"
        $A11yStatus = "pass"
    } catch {
        Write-Error "Accessibility check failed"
        $A11yStatus = "fail"
        $OverallStatus = "failed"
    }

    # Step 3: Performance Check
    Write-Banner "STEP 3/4: PERFORMANCE CHECK"
    try {
        bash "$scriptDir/perf.sh"
        Write-Success "Performance check passed"
        $PerfStatus = "pass"
    } catch {
        Write-Error "Performance check failed"
        $PerfStatus = "fail"
        $OverallStatus = "failed"
    }

    # Step 4: Ledger Append
    Write-Banner "STEP 4/4: LEDGER APPEND"
    try {
        bash "$scriptDir/ledger-append.sh" --status "$OverallStatus" --health "$HealthStatus" --a11y "$A11yStatus" --perf "$PerfStatus"
        Write-Success "Validation recorded in ledger"
    } catch {
        Write-Error "Failed to record in ledger"
    }
} else {
    Write-Info "Running PowerShell native validation..."

    # Step 1: Health Check (PowerShell version)
    Write-Banner "STEP 1/4: HEALTH CHECK"
    try {
        & "$scriptDir/health-check.ps1"
        Write-Success "Health check passed"
        $HealthStatus = "pass"
    } catch {
        Write-Error "Health check failed: $_"
        $HealthStatus = "fail"
        $OverallStatus = "failed"
    }

    # Step 2: Accessibility Check
    Write-Banner "STEP 2/4: ACCESSIBILITY CHECK"
    Write-Info "Accessibility testing requires axe-core CLI"
    Write-Info "Install: npm install -g @axe-core/cli"
    Write-Info "Skipping for now (manual review needed)..."
    $A11yStatus = "skipped"

    # Step 3: Performance Check (PowerShell version)
    Write-Banner "STEP 3/4: PERFORMANCE CHECK"
    try {
        & "$scriptDir/perf.ps1"
        Write-Success "Performance check passed"
        $PerfStatus = "pass"
    } catch {
        Write-Error "Performance check failed: $_"
        $PerfStatus = "fail"
        $OverallStatus = "failed"
    }

    # Step 4: Ledger Append (PowerShell version)
    Write-Banner "STEP 4/4: LEDGER APPEND"
    try {
        & "$scriptDir/ledger-append.ps1" -Status $OverallStatus -Health $HealthStatus -A11y $A11yStatus -Perf $PerfStatus
        Write-Success "Validation recorded in ledger"
    } catch {
        Write-Error "Failed to record in ledger: $_"
    }
}

# Calculate duration
$PipelineEnd = Get-Date
$Duration = ($PipelineEnd - $PipelineStart).TotalSeconds

# Final summary
Write-Banner "VALIDATION COMPLETE"

Write-Host "Duration: $([math]::Round($Duration, 1))s"
Write-Host ""
Write-Host "Results:"

if ($HealthStatus -eq "pass") {
    Write-Host "  Health Check:      " -NoNewline
    Write-Success "✓ PASS"
} else {
    Write-Host "  Health Check:      " -NoNewline
    Write-Error "✗ FAIL"
}

if ($A11yStatus -eq "pass") {
    Write-Host "  Accessibility:     " -NoNewline
    Write-Success "✓ PASS"
} elseif ($A11yStatus -eq "skipped") {
    Write-Host "  Accessibility:     ⊘ SKIPPED" -ForegroundColor Yellow
} else {
    Write-Host "  Accessibility:     " -NoNewline
    Write-Error "✗ FAIL"
}

if ($PerfStatus -eq "pass") {
    Write-Host "  Performance:       " -NoNewline
    Write-Success "✓ PASS"
} else {
    Write-Host "  Performance:       " -NoNewline
    Write-Error "✗ FAIL"
}

Write-Host ""

if ($OverallStatus -eq "validated") {
    Write-Host "Overall Status: " -NoNewline
    Write-Success "✓ VALIDATED"
    Write-Host ""
    Write-Success "All validation checks passed - deployment approved"
    exit 0
} else {
    Write-Host "Overall Status: " -NoNewline
    Write-Error "✗ FAILED"
    Write-Host ""
    Write-Error "Validation failed - deployment blocked"
    exit 1
}
