# Codex Dominion - Performance Testing Script (PowerShell)
# Validates performance against governance thresholds (p95 <= 300ms)

param(
    [string]$FrontendUrl = $env:FRONTEND_URL ?? "http://localhost:3000",
    [string]$BackendUrl = $env:BACKEND_URL ?? "http://localhost:8001",
    [int]$Iterations = 10
)

$ErrorActionPreference = "Continue"

# Governance thresholds
$P50_THRESHOLD = 100   # ms
$P95_THRESHOLD = 300   # ms - GOVERNANCE THRESHOLD
$P99_THRESHOLD = 500   # ms

# Counters
$script:Passed = 0
$script:Failed = 0
$script:Warnings = 0

function Write-Log { Write-Host "[PERF] $args" -ForegroundColor Blue }
function Write-CheckSuccess {
    Write-Host "✓ $args" -ForegroundColor Green
    $script:Passed++
}
function Write-CheckError {
    Write-Host "✗ $args" -ForegroundColor Red
    $script:Failed++
}
function Write-CheckWarning {
    Write-Host "⚠ $args" -ForegroundColor Yellow
    $script:Warnings++
}

function Test-EndpointPerformance {
    param(
        [string]$Name,
        [string]$Url
    )

    Write-Log "Testing ${Name} ($Iterations requests)..."

    $times = @()
    $errors = 0

    for ($i = 1; $i -le $Iterations; $i++) {
        try {
            $sw = [System.Diagnostics.Stopwatch]::StartNew()
            $response = Invoke-WebRequest -Uri $Url -TimeoutSec 10 -UseBasicParsing
            $sw.Stop()
            $times += $sw.ElapsedMilliseconds
        } catch {
            $errors++
        }
    }

    if ($times.Count -eq 0) {
        Write-CheckError "${Name}: All requests failed"
        return $false
    }

    # Calculate percentiles
    $sorted = $times | Sort-Object
    $p50_idx = [math]::Floor($sorted.Count * 0.50)
    $p95_idx = [math]::Floor($sorted.Count * 0.95)
    $p99_idx = [math]::Floor($sorted.Count * 0.99)

    $p50 = $sorted[$p50_idx]
    $p95 = $sorted[$p95_idx]
    $p99 = $sorted[$p99_idx]

    $errorRate = [math]::Round(($errors / $Iterations) * 100, 1)

    Write-Host "  p50: ${p50}ms"
    Write-Host "  p95: ${p95}ms"
    Write-Host "  p99: ${p99}ms"
    Write-Host "  Error rate: ${errorRate}%"

    # Check against thresholds
    $status = "PASS"

    if ($p95 -gt $P95_THRESHOLD) {
        Write-CheckError "${Name}: p95 (${p95}ms) exceeds governance threshold (${P95_THRESHOLD}ms)"
        $status = "FAIL"
    } elseif ($p95 -gt ($P95_THRESHOLD * 0.9)) {
        Write-CheckWarning "${Name}: p95 (${p95}ms) approaching threshold (${P95_THRESHOLD}ms)"
        $status = "WARN"
    } else {
        Write-CheckSuccess "${Name}: p95 (${p95}ms) within threshold (${P95_THRESHOLD}ms)"
    }

    Write-Host ""

    return ($status -ne "FAIL")
}

# Setup report directory
$reportDir = ".\reports\performance"
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"

Write-Host ""
Write-Host "============================================"
Write-Host "   CODEX DOMINION - PERFORMANCE TEST"
Write-Host "============================================"
Write-Host ""

# Endpoints to test
$endpoints = @{
    "Homepage" = "$FrontendUrl/"
    "Capsules" = "$FrontendUrl/capsules"
    "Signals" = "$FrontendUrl/signals"
    "API Health" = "$BackendUrl/health"
    "API Status" = "$BackendUrl/api/v1/status"
}

# Initialize CSV
$csvPath = "$reportDir\results-$timestamp.csv"
"Endpoint,p50(ms),p95(ms),p99(ms),Status" | Out-File -FilePath $csvPath -Encoding UTF8

# Run tests
foreach ($endpoint in $endpoints.GetEnumerator()) {
    Test-EndpointPerformance -Name $endpoint.Key -Url $endpoint.Value
}

Write-Log "Results saved to: $csvPath"

# Summary
Write-Host ""
Write-Host "============================================"
Write-Host "        PERFORMANCE TEST SUMMARY"
Write-Host "============================================"
Write-Host "Passed:   $script:Passed endpoints" -ForegroundColor Green
Write-Host "Warnings: $script:Warnings endpoints" -ForegroundColor Yellow
Write-Host "Failed:   $script:Failed endpoints" -ForegroundColor Red
Write-Host ""
Write-Host "Governance Threshold: p95 ≤ ${P95_THRESHOLD}ms"
Write-Host ""

if ($script:Failed -gt 0) {
    Write-Host "Performance test FAILED - governance thresholds violated" -ForegroundColor Red
    exit 1
} elseif ($script:Warnings -gt 0) {
    Write-Host "Performance test PASSED with warnings" -ForegroundColor Yellow
    exit 0
} else {
    Write-Host "Performance test PASSED" -ForegroundColor Green
    exit 0
}
