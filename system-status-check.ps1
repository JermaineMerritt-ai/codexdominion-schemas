# Comprehensive System Status Check Script
$ErrorActionPreference = "Continue"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "SYSTEM STATUS CHECK - FULL DIAGNOSTIC" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$results = @{
    github = @{ status = "unknown"; details = @() }
    azure = @{ status = "unknown"; details = @() }
    dashboard = @{ status = "unknown"; details = @() }
    overall = "unknown"
}

# [1/4] GitHub Actions Status
Write-Host "[1/4] Checking GitHub Actions..." -ForegroundColor Yellow
try {
    $repo = "JermaineMerritt-ai/codex-dominion"
    $response = Invoke-RestMethod -Uri "https://api.github.com/repos/$repo/actions/runs?per_page=10" -Headers @{"Accept"="application/vnd.github.v3+json"} -ErrorAction Stop

    $success = ($response.workflow_runs | Where-Object { $_.conclusion -eq "success" }).Count
    $total = $response.workflow_runs.Count

    Write-Host "  ✅ Recent Workflows: $success/$total successful" -ForegroundColor Green
    $results.github.status = "healthy"
    $results.github.details += "Recent success rate: $([math]::Round(($success/$total)*100, 1))%"
} catch {
    Write-Host "  ⚠️  GitHub API: Unable to fetch (may need authentication)" -ForegroundColor Yellow
    $results.github.status = "warning"
    $results.github.details += "API access limited"
}

# [2/4] Azure Container Status
Write-Host "`n[2/4] Checking Azure Container..." -ForegroundColor Yellow
try {
    $containerState = az container show --resource-group codex-rg --name codex-backend --query "instanceView.state" -o tsv 2>&1
    $containerIP = az container show --resource-group codex-rg --name codex-backend --query "ipAddress.ip" -o tsv 2>&1

    if ($containerState -eq "Running") {
        Write-Host "  ✅ Container: Running" -ForegroundColor Green
        Write-Host "  ✅ IP Address: $containerIP" -ForegroundColor Green
        $results.azure.status = "healthy"
        $results.azure.details += "State: Running"

        # Check health endpoint
        try {
            $health = Invoke-RestMethod -Uri "http://codex-api.eastus2.azurecontainer.io:8000/health" -TimeoutSec 5
            Write-Host "  ✅ Health Check: $($health.status)" -ForegroundColor Green
            $results.azure.details += "Health: $($health.status)"
        } catch {
            Write-Host "  ⚠️  Health endpoint not responding" -ForegroundColor Yellow
            $results.azure.details += "Health: unreachable"
        }

        # Check for errors in logs
        $logs = az container logs --resource-group codex-rg --name codex-backend --tail 50 2>&1
        $errors = $logs | Select-String -Pattern "ERROR|CRITICAL|FATAL" -CaseSensitive:$false

        if ($errors.Count -eq 0) {
            Write-Host "  ✅ Logs: Clean (no errors)" -ForegroundColor Green
            $results.azure.details += "Logs: No critical errors"
        } else {
            Write-Host "  ⚠️  Found $($errors.Count) error entries in logs" -ForegroundColor Yellow
            $results.azure.details += "Logs: $($errors.Count) errors found"
        }
    } else {
        Write-Host "  ❌ Container: $containerState" -ForegroundColor Red
        $results.azure.status = "unhealthy"
        $results.azure.details += "State: $containerState"
    }
} catch {
    Write-Host "  ❌ Azure CLI Error: $_" -ForegroundColor Red
    $results.azure.status = "error"
    $results.azure.details += "Azure CLI error"
}

# [3/4] Dashboard Tabs Test
Write-Host "`n[3/4] Testing Dashboard Tabs..." -ForegroundColor Yellow
$dashboard = "http://localhost:5000"
$tabs = @(
    @{path="/"; name="Home"},
    @{path="/ai-agents"; name="AI Agents"},
    @{path="/social"; name="Social Media"},
    @{path="/revenue"; name="Revenue"},
    @{path="/affiliate"; name="Affiliate"},
    @{path="/ecommerce"; name="E-Commerce"},
    @{path="/copilot"; name="Copilot"},
    @{path="/avatar"; name="Avatar"},
    @{path="/council"; name="Council"},
    @{path="/chatbot"; name="Chatbot"},
    @{path="/algorithm"; name="Algorithm AI"},
    @{path="/autopublish"; name="Auto-Publish"}
)

$working = 0
$failed = @()

foreach ($tab in $tabs) {
    try {
        $response = Invoke-WebRequest -Uri "$dashboard$($tab.path)" -Method Head -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            $working++
        } else {
            $failed += $tab.name
        }
    } catch {
        $failed += $tab.name
    }
}

if ($working -eq $tabs.Count) {
    Write-Host "  ✅ All $($tabs.Count) tabs working!" -ForegroundColor Green
    $results.dashboard.status = "healthy"
    $results.dashboard.details += "All tabs accessible"
} elseif ($working -gt 0) {
    Write-Host "  ⚠️  Partial: $working/$($tabs.Count) tabs working" -ForegroundColor Yellow
    Write-Host "     Failed: $($failed -join ', ')" -ForegroundColor Gray
    $results.dashboard.status = "partial"
    $results.dashboard.details += "$working/$($tabs.Count) tabs accessible"
} else {
    Write-Host "  ⚠️  Dashboard not running (start with .\START_DASHBOARD.ps1)" -ForegroundColor Yellow
    $results.dashboard.status = "offline"
    $results.dashboard.details += "Dashboard not accessible"
}

# [4/4] Generate System Health Report
Write-Host "`n[4/4] Generating Health Report..." -ForegroundColor Yellow

# Determine overall status
$healthyCount = ($results.Values | Where-Object { $_.status -eq "healthy" }).Count
if ($healthyCount -eq 3) {
    $results.overall = "excellent"
    $overallIcon = "✅"
    $overallColor = "Green"
} elseif ($healthyCount -ge 2) {
    $results.overall = "good"
    $overallIcon = "✅"
    $overallColor = "Green"
} elseif ($healthyCount -ge 1) {
    $results.overall = "fair"
    $overallIcon = "⚠️"
    $overallColor = "Yellow"
} else {
    $results.overall = "critical"
    $overallIcon = "❌"
    $overallColor = "Red"
}

# Summary Report
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "HEALTH REPORT SUMMARY" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Overall Status: $overallIcon $($results.overall.ToUpper())" -ForegroundColor $overallColor
Write-Host ""
Write-Host "Component Status:" -ForegroundColor White
Write-Host "  GitHub Actions: $($results.github.status)" -ForegroundColor $(if ($results.github.status -eq "healthy") { "Green" } else { "Yellow" })
Write-Host "  Azure Container: $($results.azure.status)" -ForegroundColor $(if ($results.azure.status -eq "healthy") { "Green" } elseif ($results.azure.status -eq "warning") { "Yellow" } else { "Red" })
Write-Host "  Master Dashboard: $($results.dashboard.status)" -ForegroundColor $(if ($results.dashboard.status -eq "healthy") { "Green" } elseif ($results.dashboard.status -eq "partial") { "Yellow" } else { "Gray" })

Write-Host "`n========================================`n" -ForegroundColor Cyan

# Save detailed report
$reportData = @{
    timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    overall_status = $results.overall
    components = @{
        github = $results.github
        azure = $results.azure
        dashboard = $results.dashboard
    }
}

$reportData | ConvertTo-Json -Depth 10 | Out-File "system_health_report.json"
Write-Host "📊 Detailed report saved: system_health_report.json" -ForegroundColor Gray
Write-Host ""

return $results
