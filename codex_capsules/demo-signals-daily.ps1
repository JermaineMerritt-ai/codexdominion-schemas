# Register Signals Daily Capsule Demo
# This script demonstrates registering and tracking a signals daily capsule

Write-Host "🚀 Codex Capsules - Signals Daily Registration Demo" -ForegroundColor Green
Write-Host ""

# Service URL
$BaseUrl = "http://localhost:8080"

# 1. Check service health
Write-Host "1. Checking Capsules API health..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$BaseUrl/" -Method GET
    Write-Host "✅ Service: $($health.service) v$($health.version)" -ForegroundColor Green
} catch {
    Write-Host "❌ Service not available. Make sure capsules service is running." -ForegroundColor Red
    exit 1
}

# 2. Register the signals daily capsule
Write-Host ""
Write-Host "2. Registering Signals Daily Capsule..." -ForegroundColor Yellow
$capsule = @{
    slug = "signals-daily"
    title = "Daily Signals Engine"
    kind = "engine"
    mode = "custodian"
    entrypoint = "POST https://codex-signals.run.app/signals/daily"
    schedule = "0 6 * * *"
    version = "2.0.0"
    status = "active"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Uri "$BaseUrl/api/capsules" -Method POST -ContentType "application/json" -Body $capsule
    Write-Host "✅ Capsule registered: $($result.slug)" -ForegroundColor Green
    Write-Host "   Title: $($result.title)" -ForegroundColor Cyan
    Write-Host "   Schedule: $($result.schedule) (Daily at 6 AM)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Failed to register capsule: $($_.Exception.Message)" -ForegroundColor Red
}

# 3. Record a successful run
Write-Host ""
Write-Host "3. Recording successful execution..." -ForegroundColor Yellow
$run = @{
    capsule_slug = "signals-daily"
    actor = "system-scheduler"
    status = "success"
    artifact_uri = "https://storage.googleapis.com/codex-artifacts/signals-daily-$(Get-Date -Format 'yyyyMMdd').tar.gz"
    checksum = "sha256:$(Get-Random -Minimum 1000000 -Maximum 9999999)"
} | ConvertTo-Json

try {
    $runResult = Invoke-RestMethod -Uri "$BaseUrl/api/capsules/run" -Method POST -ContentType "application/json" -Body $run
    Write-Host "✅ Run recorded: ID $($runResult.id)" -ForegroundColor Green
    Write-Host "   Status: $($runResult.status)" -ForegroundColor Cyan
    Write-Host "   Artifact: $($runResult.artifact_uri)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Failed to record run: $($_.Exception.Message)" -ForegroundColor Red
}

# 4. Show all capsules
Write-Host ""
Write-Host "4. Listing all registered capsules..." -ForegroundColor Yellow
try {
    $capsules = Invoke-RestMethod -Uri "$BaseUrl/api/capsules" -Method GET
    foreach ($cap in $capsules) {
        Write-Host "   📦 $($cap.slug): $($cap.title) [$($cap.kind)/$($cap.mode)]" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ Failed to list capsules: $($_.Exception.Message)" -ForegroundColor Red
}

# 5. Show performance metrics
Write-Host ""
Write-Host "5. Performance analytics..." -ForegroundColor Yellow
try {
    $performance = Invoke-RestMethod -Uri "$BaseUrl/api/capsules/performance" -Method GET
    foreach ($perf in $performance) {
        $successRate = if ($perf.success_rate) { "{0:P0}" -f $perf.success_rate } else { "N/A" }
        Write-Host "   📊 $($perf.capsule_slug): $($perf.total_runs) runs, $successRate success rate" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ Failed to get performance data: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 Signals Daily Capsule successfully registered and tracked!" -ForegroundColor Green
Write-Host "   Access the API documentation at: $BaseUrl/docs" -ForegroundColor Cyan
Write-Host "   Access the Capsules API docs at: $BaseUrl/api/docs" -ForegroundColor Cyan