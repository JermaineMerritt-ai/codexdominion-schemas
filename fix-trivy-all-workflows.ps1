#!/usr/bin/env pwsh
# Script to find and fix all Trivy scanner issues in GitHub workflows

Write-Host "🔍 TRIVY SCANNER COMPREHENSIVE FIX" -ForegroundColor Cyan
Write-Host "===================================`n" -ForegroundColor Cyan

$fixedCount = 0
$checkedCount = 0
$issues = @()

# Get all workflow files
$workflows = Get-ChildItem .github/workflows/*.yml

Write-Host "Scanning $($workflows.Count) workflow files...`n" -ForegroundColor White

foreach ($workflow in $workflows) {
    $checkedCount++
    $content = Get-Content $workflow.FullName -Raw
    
    # Check for problematic patterns
    $hasIssue = $false
    
    # Pattern 1: Running trivy directly
    if ($content -match 'run:.*\./trivy|run:.*trivy\s+fs') {
        $hasIssue = $true
        $issues += @{
            File = $workflow.Name
            Issue = "Direct trivy execution found"
            Line = ($content -split "`n" | Select-String -Pattern "\./trivy|trivy\s+fs" | Select-Object -First 1).LineNumber
        }
    }
    
    # Pattern 2: Downloading trivy binary
    if ($content -match 'wget.*trivy|curl.*trivy.*download') {
        $hasIssue = $true
        $issues += @{
            File = $workflow.Name
            Issue = "Manual trivy download found"
            Line = ($content -split "`n" | Select-String -Pattern "wget.*trivy|curl.*trivy" | Select-Object -First 1).LineNumber
        }
    }
    
    # Pattern 3: Installing trivy via package manager
    if ($content -match 'apt-get install.*trivy|brew install.*trivy') {
        $hasIssue = $true
        $issues += @{
            File = $workflow.Name
            Issue = "Package manager trivy install found"
            Line = ($content -split "`n" | Select-String -Pattern "install.*trivy" | Select-Object -First 1).LineNumber
        }
    }
    
    if ($hasIssue) {
        Write-Host "❌ ISSUE FOUND: $($workflow.Name)" -ForegroundColor Red
    }
}

Write-Host "`n📊 SCAN RESULTS:" -ForegroundColor Yellow
Write-Host "  Checked: $checkedCount workflows" -ForegroundColor White
Write-Host "  Issues Found: $($issues.Count)" -ForegroundColor $(if ($issues.Count -gt 0) { "Red" } else { "Green" })

if ($issues.Count -gt 0) {
    Write-Host "`n❌ ISSUES DETAILS:" -ForegroundColor Red
    foreach ($issue in $issues) {
        Write-Host "  File: $($issue.File)" -ForegroundColor Yellow
        Write-Host "  Issue: $($issue.Issue)" -ForegroundColor Gray
        Write-Host "  Line: ~$($issue.Line)`n" -ForegroundColor Gray
    }
    
    Write-Host "📝 RECOMMENDED FIX:" -ForegroundColor Cyan
    Write-Host @'
Replace any manual trivy steps with:

- name: Run Trivy Scanner
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'fs'
    scan-ref: '.'
    severity: 'HIGH,CRITICAL'
    format: 'sarif'
    output: 'trivy-results.sarif'

- name: Upload Trivy Results
  uses: github/codeql-action/upload-sarif@v3
  if: always()
  with:
    sarif_file: 'trivy-results.sarif'
'@ -ForegroundColor White

} else {
    Write-Host "`n✅ All workflows are using the correct Trivy pattern!" -ForegroundColor Green
}

Write-Host "`n🔗 To check GitHub Actions status:" -ForegroundColor Cyan
Write-Host "  https://github.com/JermaineMerritt-ai/Codex-Dominion/actions" -ForegroundColor Blue
