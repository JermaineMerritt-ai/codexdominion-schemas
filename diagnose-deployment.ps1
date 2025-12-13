# Sovereign Bridge Deployment Diagnostics
# Automatically diagnoses and reports deployment issues

Write-Host "\n*** SOVEREIGN BRIDGE DEPLOYMENT DIAGNOSTICS ***" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

# 1. Check GitHub Actions Workflow Status
Write-Host "`n[1/5] Checking GitHub Actions workflow..." -ForegroundColor Yellow
try {
    $runs = Invoke-RestMethod -Uri "https://api.github.com/repos/JermaineMerritt-ai/codexdominion-schemas/actions/runs?per_page=5" -Headers @{Accept="application/vnd.github.v3+json"}
    $sovereignRuns = $runs.workflow_runs | Where-Object { $_.name -like "*Sovereign*" }

    if ($sovereignRuns) {
        $latest = $sovereignRuns | Select-Object -First 1
        Write-Host "  ✓ Found workflow runs" -ForegroundColor Green
        Write-Host "    Status: $($latest.status)" -ForegroundColor $(if($latest.status -eq "completed"){"Green"}else{"Yellow"})
        Write-Host "    Conclusion: $($latest.conclusion)" -ForegroundColor $(if($latest.conclusion -eq "success"){"Green"}elseif($latest.conclusion -eq "failure"){"Red"}else{"Yellow"})
        Write-Host "    URL: $($latest.html_url)" -ForegroundColor Blue

        if ($latest.conclusion -eq "failure") {
            Write-Host "  ✗ DEPLOYMENT FAILED - Check logs at URL above" -ForegroundColor Red
        }
        elseif ($latest.status -eq "in_progress") {
            Write-Host "  ⏳ Deployment still in progress..." -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ✗ No Sovereign Bridge workflows found" -ForegroundColor Red
    }
} catch {
    Write-Host "  ✗ Error accessing GitHub API: $($_.Exception.Message)" -ForegroundColor Red
}

# 2. Test Azure Static Web App Homepage
Write-Host "`n[2/5] Testing Azure Static Web App homepage..." -ForegroundColor Yellow
try {
    $homepage = Invoke-WebRequest -Uri "https://mango-wave-0fcc4e40f.3.azurestaticapps.net" -UseBasicParsing -TimeoutSec 10
    if ($homepage.StatusCode -eq 200) {
        Write-Host "  [OK] Homepage accessible (HTTP $($homepage.StatusCode))" -ForegroundColor Green
    }
} catch {
    Write-Host "  [ERROR] Homepage error: $($_.Exception.Message)" -ForegroundColor Red
}

# 3. Test API Endpoint (GET)
Write-Host "`n[3/5] Testing API endpoint (GET)..." -ForegroundColor Yellow
try {
    $apiTest = Invoke-WebRequest -Uri "https://mango-wave-0fcc4e40f.3.azurestaticapps.net/api/agent-commands?taskId=test_123" -UseBasicParsing -TimeoutSec 10
    if ($apiTest.StatusCode -eq 200 -or $apiTest.StatusCode -eq 404) {
        Write-Host "  ✓ API endpoint responding (HTTP $($apiTest.StatusCode))" -ForegroundColor Green
        if ($apiTest.Content -like "*Azure Static Web Apps*") {
            Write-Host "  ⚠ Getting Azure 404 page - API not deployed yet" -ForegroundColor Yellow
        } else {
            Write-Host "  ✓ API is deployed and responding!" -ForegroundColor Green
        }
    }
} catch {
    $errorResponse = $_.Exception.Response
    if ($errorResponse) {
        $reader = New-Object System.IO.StreamReader($errorResponse.GetResponseStream())
        $content = $reader.ReadToEnd()
        if ($content -like "*Azure Static Web Apps*") {
            Write-Host "  ⚠ API endpoint returns Azure 404 - Not deployed" -ForegroundColor Yellow
        } else {
            Write-Host "  ✗ API error: $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "  ✗ Connection error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 4. Check Local Files
Write-Host "`n[4/5] Verifying local configuration..." -ForegroundColor Yellow
$files = @{
    "API Route" = "apps\sovereign-bridge\app\api\agent-commands\route.ts"
    "Next Config" = "apps\sovereign-bridge\next.config.js"
    "Static Web App Config" = "apps\sovereign-bridge\staticwebapp.config.json"
    "Workflow" = ".github\workflows\deploy-sovereign-bridge-azure.yml"
}

foreach ($name in $files.Keys) {
    $path = Join-Path $PSScriptRoot $files[$name]
    if (Test-Path $path) {
        Write-Host "  ✓ $name exists" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $name missing: $path" -ForegroundColor Red
    }
}

# 5. Check Azure Resource
Write-Host "`n[5/5] Checking Azure Static Web App resource..." -ForegroundColor Yellow
try {
    $azCheck = az staticwebapp list --query "[?name=='codex-sovereign-bridge']" 2>&1
    if ($azCheck -and $azCheck -notlike "*ERROR*") {
        Write-Host "  ✓ Azure Static Web App resource exists" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Could not verify Azure resource (az CLI may not be installed)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠ Azure CLI check skipped" -ForegroundColor Yellow
}

# Summary and Recommendations
Write-Host "`n" + ("=" * 60) -ForegroundColor Gray
Write-Host "*** DIAGNOSTICS SUMMARY ***" -ForegroundColor Cyan

if ($sovereignRuns) {
    $latest = $sovereignRuns | Select-Object -First 1

    if ($latest.conclusion -eq "success") {
        Write-Host "`n✓ Deployment succeeded but API not accessible yet" -ForegroundColor Yellow
        Write-Host "`nPossible causes:" -ForegroundColor White
        Write-Host "  1. Azure propagation delay (wait 5-10 more minutes)" -ForegroundColor Gray
        Write-Host "  2. API folder not deployed correctly" -ForegroundColor Gray
        Write-Host "  3. Routing configuration issue in staticwebapp.config.json" -ForegroundColor Gray
        Write-Host "`nRecommended actions:" -ForegroundColor White
        Write-Host "  - Wait 10 minutes and test again" -ForegroundColor Cyan
        Write-Host "  - Check Azure portal deployment logs" -ForegroundColor Cyan
        Write-Host "  - Verify .next/standalone folder was created" -ForegroundColor Cyan
    }
    elseif ($latest.conclusion -eq "failure") {
        Write-Host "`n✗ Deployment FAILED" -ForegroundColor Red
        Write-Host "`nRecommended actions:" -ForegroundColor White
        Write-Host "  1. Check workflow logs: $($latest.html_url)" -ForegroundColor Cyan
        Write-Host "  2. Look for errors in:" -ForegroundColor Gray
        Write-Host "     - Install root dependencies step" -ForegroundColor Gray
        Write-Host "     - Build Sovereign Bridge step" -ForegroundColor Gray
        Write-Host "     - Deploy to Azure step" -ForegroundColor Gray
        Write-Host "  3. Common issues:" -ForegroundColor Gray
        Write-Host "     - workspace:* dependency errors - need root npm install" -ForegroundColor Gray
        Write-Host "     - Next.js build errors - check TypeScript/ESLint issues" -ForegroundColor Gray
        Write-Host "     - Azure deploy errors - check secret is correct" -ForegroundColor Gray
    }
    elseif ($latest.status -eq "in_progress") {
    Write-Host "\n[*] Deployment IN PROGRESS" -ForegroundColor Yellow
        Write-Host "\nRecommended actions:" -ForegroundColor White
        Write-Host "  - Wait 5-10 minutes for build to complete" -ForegroundColor Cyan
        Write-Host "  - Monitor at: $($latest.html_url)" -ForegroundColor Cyan
    }
} else {
    Write-Host "\n[X] No deployment workflows found" -ForegroundColor Red
    Write-Host "\nRecommended actions:" -ForegroundColor White
    Write-Host "  - Manually trigger workflow at:" -ForegroundColor Cyan
    Write-Host "    https://github.com/JermaineMerritt-ai/codexdominion-schemas/actions/workflows/deploy-sovereign-bridge-azure.yml" -ForegroundColor Blue
}

Write-Host "`n" + ("=" * 60) -ForegroundColor Gray
Write-Host "\n*** Diagnostics complete! ***" -ForegroundColor Cyan
