# Quick Deployment Status Check

Write-Host "`n🔍 Checking Deployment Status...`n" -ForegroundColor Cyan

# Test main dashboard
$mainDashboard = try {
    $response = Invoke-WebRequest -Uri "https://yellow-tree-0ed102210.3.azurestaticapps.net/main-dashboard" -TimeoutSec 5 -ErrorAction Stop
    "✅ LIVE (Status: $($response.StatusCode), Size: $($response.Content.Length) bytes)"
} catch {
    "❌ 404 - Still deploying"
}

# Test root page
$rootPage = try {
    $response = Invoke-WebRequest -Uri "https://yellow-tree-0ed102210.3.azurestaticapps.net/" -TimeoutSec 5 -ErrorAction Stop
    if ($response.Content -like "*Congratulations on your new site*") {
        "⏳ Default placeholder page (not deployed yet)"
    } else {
        "✅ LIVE (Status: $($response.StatusCode), Size: $($response.Content.Length) bytes)"
    }
} catch {
    "❌ Error: $($_.Exception.Message)"
}

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "Main Dashboard: " -NoNewline; Write-Host $mainDashboard -ForegroundColor $(if ($mainDashboard -like '*LIVE*') { 'Green' } else { 'Yellow' })
Write-Host "Root Page:      " -NoNewline; Write-Host $rootPage -ForegroundColor $(if ($rootPage -like '*LIVE*') { 'Green' } else { 'Yellow' })
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

if ($mainDashboard -like '*404*' -or $rootPage -like '*placeholder*') {
    Write-Host "`n⏳ Deployment is still in progress (usually takes 3-5 minutes)" -ForegroundColor Yellow
    Write-Host "`n📊 Check workflow status at:" -ForegroundColor Cyan
    Write-Host "   https://github.com/JermaineMerritt-ai/codexdominion-schemas/actions" -ForegroundColor Cyan
    Write-Host "`n💡 Look for the latest workflow run with name:" -ForegroundColor Cyan
    Write-Host "   'Deploy frontend to yellow-tree Azure Static Web App'" -ForegroundColor White
    Write-Host "`n   🟠 Orange dot = Running" -ForegroundColor Yellow
    Write-Host "   ✅ Green check = Success (deployment complete)" -ForegroundColor Green
    Write-Host "   ❌ Red X = Failed (check logs)" -ForegroundColor Red
} else {
    Write-Host "`n✅ DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
    Write-Host "`n🎉 Your main dashboard is now live at:" -ForegroundColor Cyan
    Write-Host "   https://yellow-tree-0ed102210.3.azurestaticapps.net/main-dashboard" -ForegroundColor White
    Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
    Write-Host "   1. Test your dashboard in a browser" -ForegroundColor White
    Write-Host "   2. Update DNS in Google Domains (optional)" -ForegroundColor White
    Write-Host "   3. See DEPLOYMENT_TROUBLESHOOTING.md for DNS setup" -ForegroundColor White
}

Write-Host ""
