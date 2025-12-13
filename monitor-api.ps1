# Continuous API Deployment Monitor
# Checks every 30 seconds until API is live

$baseUrl = "https://mango-wave-0fcc4e40f.3.azurestaticapps.net"
$maxAttempts = 20  # 10 minutes total
$interval = 30     # seconds

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  SOVEREIGN BRIDGE API MONITOR" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Target: $baseUrl/api/agent-commands" -ForegroundColor Gray
Write-Host "Checking every $interval seconds (max $maxAttempts attempts)`n" -ForegroundColor Gray

for ($i = 1; $i -le $maxAttempts; $i++) {
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] Attempt $i/$maxAttempts..." -ForegroundColor Yellow -NoNewline

    try {
        $response = Invoke-RestMethod -Uri "$baseUrl/api/agent-commands?taskId=test_123" `
            -Method Get `
            -TimeoutSec 10 `
            -ErrorAction Stop

        # Success!
        Write-Host " [SUCCESS]" -ForegroundColor Green
        Write-Host "`n========================================" -ForegroundColor Green
        Write-Host "  API IS LIVE AND RESPONDING!" -ForegroundColor Green
        Write-Host "========================================`n" -ForegroundColor Green

        Write-Host "Response:" -ForegroundColor Cyan
        $response | ConvertTo-Json -Depth 5

        Write-Host "`nRun full test suite:" -ForegroundColor Cyan
        Write-Host "  .\test-api.ps1" -ForegroundColor Yellow

        exit 0

    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__

        if ($statusCode -eq 404) {
            Write-Host " [404 - Still deploying]" -ForegroundColor Yellow
        } elseif ($statusCode -eq 500) {
            Write-Host " [500 - Server error, deployment may have failed]" -ForegroundColor Red
        } else {
            Write-Host " [Error: $($_.Exception.Message)]" -ForegroundColor Red
        }
    }

    if ($i -lt $maxAttempts) {
        Write-Host "  Waiting $interval seconds..." -ForegroundColor Gray
        Start-Sleep -Seconds $interval
    }
}

Write-Host "`n========================================" -ForegroundColor Red
Write-Host "  TIMEOUT - API NOT RESPONDING" -ForegroundColor Red
Write-Host "========================================`n" -ForegroundColor Red

Write-Host "Troubleshooting steps:" -ForegroundColor Yellow
Write-Host "1. Check GitHub Actions:" -ForegroundColor White
Write-Host "   https://github.com/JermaineMerritt-ai/codexdominion-schemas/actions" -ForegroundColor Blue
Write-Host "`n2. Check Azure Portal:" -ForegroundColor White
Write-Host "   https://portal.azure.com - Look for 'codex-sovereign-bridge'" -ForegroundColor Blue
Write-Host "`n3. Run diagnostics:" -ForegroundColor White
Write-Host "   .\diagnose-deployment.ps1" -ForegroundColor Yellow
Write-Host "`n4. View deployment logs in Azure Static Web Apps" -ForegroundColor White

exit 1
