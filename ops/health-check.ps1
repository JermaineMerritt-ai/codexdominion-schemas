# Codex Dominion - Health Check Script (PowerShell)
# Validates all services are operational and meet governance thresholds

param(
    [string]$FrontendUrl = $env:FRONTEND_URL ?? "http://localhost:3000",
    [string]$BackendUrl = $env:BACKEND_URL ?? "http://localhost:8001",
    [int]$Timeout = 5
)

$ErrorActionPreference = "Continue"

# Counters
$script:Passed = 0
$script:Failed = 0
$script:Warnings = 0

function Write-Log { Write-Host "[HEALTH] $args" -ForegroundColor Blue }
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

function Test-ServiceEndpoint {
    param(
        [string]$Name,
        [string]$Url,
        [int]$ExpectedStatus = 200
    )

    Write-Log "Checking ${Name}..."

    try {
        $response = Invoke-WebRequest -Uri $Url -TimeoutSec $Timeout -UseBasicParsing

        if ($response.StatusCode -eq $ExpectedStatus) {
            Write-CheckSuccess "${Name} responding (HTTP $($response.StatusCode))"

            # Try to parse JSON
            try {
                $json = $response.Content | ConvertFrom-Json
                Write-Host ($json | ConvertTo-Json -Compress) -ForegroundColor DarkGray
            } catch {}

            return $true
        } else {
            Write-CheckError "${Name} returned HTTP $($response.StatusCode), expected ${ExpectedStatus}"
            return $false
        }
    } catch {
        Write-CheckError "${Name} not responding at ${Url}: $($_.Exception.Message)"
        return $false
    }
}

function Test-Performance {
    param(
        [string]$Name,
        [string]$Url,
        [int]$ThresholdMs = 300
    )

    Write-Log "Measuring ${Name} response time..."

    try {
        $sw = [System.Diagnostics.Stopwatch]::StartNew()
        $response = Invoke-WebRequest -Uri $Url -TimeoutSec $Timeout -UseBasicParsing
        $sw.Stop()

        $timeMs = $sw.ElapsedMilliseconds

        if ($timeMs -le $ThresholdMs) {
            Write-CheckSuccess "${Name} response time: ${timeMs}ms (threshold: ${ThresholdMs}ms)"
            return $true
        } else {
            Write-CheckWarning "${Name} response time: ${timeMs}ms exceeds threshold ${ThresholdMs}ms"
            return $false
        }
    } catch {
        Write-CheckError "${Name} performance check failed: $($_.Exception.Message)"
        return $false
    }
}

function Test-DiskSpace {
    Write-Log "Checking disk space..."

    $drive = Get-PSDrive -Name C
    $usedPercent = [math]::Round(($drive.Used / ($drive.Used + $drive.Free)) * 100, 1)

    if ($usedPercent -lt 80) {
        Write-CheckSuccess "Disk usage: ${usedPercent}%"
        return $true
    } elseif ($usedPercent -lt 90) {
        Write-CheckWarning "Disk usage: ${usedPercent}% (approaching limit)"
        return $false
    } else {
        Write-CheckError "Disk usage: ${usedPercent}% (critical)"
        return $false
    }
}

function Test-Memory {
    Write-Log "Checking memory usage..."

    try {
        $os = Get-CimInstance Win32_OperatingSystem
        $totalMemory = $os.TotalVisibleMemorySize
        $freeMemory = $os.FreePhysicalMemory
        $usedPercent = [math]::Round((($totalMemory - $freeMemory) / $totalMemory) * 100, 1)

        if ($usedPercent -lt 80) {
            Write-CheckSuccess "Memory usage: ${usedPercent}%"
            return $true
        } elseif ($usedPercent -lt 90) {
            Write-CheckWarning "Memory usage: ${usedPercent}% (high)"
            return $false
        } else {
            Write-CheckError "Memory usage: ${usedPercent}% (critical)"
            return $false
        }
    } catch {
        Write-CheckWarning "Memory check failed: $($_.Exception.Message)"
        return $false
    }
}

Write-Host ""
Write-Host "============================================"
Write-Host "    CODEX DOMINION - HEALTH CHECK"
Write-Host "============================================"
Write-Host ""

# Frontend checks
Test-ServiceEndpoint -Name "Frontend Homepage" -Url $FrontendUrl -ExpectedStatus 200
Test-ServiceEndpoint -Name "Frontend API Route" -Url "$FrontendUrl/api/health" -ExpectedStatus 200
Test-Performance -Name "Frontend" -Url $FrontendUrl -ThresholdMs 300

# Backend checks
Test-ServiceEndpoint -Name "Backend Health" -Url "$BackendUrl/health" -ExpectedStatus 200
Test-ServiceEndpoint -Name "Backend API" -Url "$BackendUrl/api/v1/status" -ExpectedStatus 200
Test-Performance -Name "Backend API" -Url "$BackendUrl/health" -ThresholdMs 300

# System resources
Test-DiskSpace
Test-Memory

# Summary
Write-Host ""
Write-Host "============================================"
Write-Host "             HEALTH CHECK SUMMARY"
Write-Host "============================================"
Write-Host "Passed:   $script:Passed" -ForegroundColor Green
Write-Host "Warnings: $script:Warnings" -ForegroundColor Yellow
Write-Host "Failed:   $script:Failed" -ForegroundColor Red
Write-Host ""

if ($script:Failed -gt 0) {
    Write-Host "Health check FAILED" -ForegroundColor Red
    exit 1
} elseif ($script:Warnings -gt 0) {
    Write-Host "Health check PASSED with warnings" -ForegroundColor Yellow
    exit 0
} else {
    Write-Host "Health check PASSED" -ForegroundColor Green
    exit 0
}
