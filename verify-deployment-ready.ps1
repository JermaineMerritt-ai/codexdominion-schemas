# Codex Dominion - Pre-Deployment Verification Script
# Checks all prerequisites before going live
# Run: .\verify-deployment-ready.ps1

Write-Host ""
Write-Host "🔍 Codex Dominion - Deployment Readiness Check" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$allChecks = @()
$criticalFailed = $false

# Helper function to record check results
function Check-Requirement {
    param(
        [string]$Name,
        [scriptblock]$TestScript,
        [string]$SuccessMessage,
        [string]$FailureMessage,
        [bool]$Critical = $true
    )

    Write-Host "Checking: $Name..." -ForegroundColor Yellow -NoNewline

    try {
        $result = & $TestScript
        if ($result) {
            Write-Host " ✅" -ForegroundColor Green
            Write-Host "  $SuccessMessage" -ForegroundColor Gray
            $script:allChecks += [PSCustomObject]@{
                Check = $Name
                Status = "PASS"
                Critical = $Critical
            }
        }
        else {
            Write-Host " ❌" -ForegroundColor Red
            Write-Host "  $FailureMessage" -ForegroundColor Red
            $script:allChecks += [PSCustomObject]@{
                Check = $Name
                Status = "FAIL"
                Critical = $Critical
            }
            if ($Critical) { $script:criticalFailed = $true }
        }
    }
    catch {
        Write-Host " ❌" -ForegroundColor Red
        Write-Host "  Error: $_" -ForegroundColor Red
        $script:allChecks += [PSCustomObject]@{
            Check = $Name
            Status = "ERROR"
            Critical = $Critical
        }
        if ($Critical) { $script:criticalFailed = $true }
    }

    Write-Host ""
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "📦 REQUIRED TOOLS" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Check-Requirement `
    -Name "Terraform" `
    -TestScript { Get-Command terraform -ErrorAction SilentlyContinue } `
    -SuccessMessage "Terraform is installed: $(terraform version -json | ConvertFrom-Json | Select-Object -ExpandProperty terraform_version)" `
    -FailureMessage "Terraform not found. Install: https://www.terraform.io/downloads"

Check-Requirement `
    -Name "Google Cloud CLI (gcloud)" `
    -TestScript { Get-Command gcloud -ErrorAction SilentlyContinue } `
    -SuccessMessage "gcloud CLI is installed" `
    -FailureMessage "gcloud CLI not found. Install: https://cloud.google.com/sdk/docs/install"

Check-Requirement `
    -Name "Docker" `
    -TestScript { Get-Command docker -ErrorAction SilentlyContinue } `
    -SuccessMessage "Docker is installed: $(docker --version)" `
    -FailureMessage "Docker not found. Install: https://docs.docker.com/get-docker/"

Check-Requirement `
    -Name "kubectl" `
    -TestScript { Get-Command kubectl -ErrorAction SilentlyContinue } `
    -SuccessMessage "kubectl is installed" `
    -FailureMessage "kubectl not found. Install: gcloud components install kubectl" `
    -Critical $false

Check-Requirement `
    -Name "GitHub CLI (gh)" `
    -TestScript { Get-Command gh -ErrorAction SilentlyContinue } `
    -SuccessMessage "GitHub CLI is installed" `
    -FailureMessage "GitHub CLI not found. Install: winget install GitHub.cli" `
    -Critical $false

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "🔐 ENVIRONMENT VARIABLES" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Check-Requirement `
    -Name "TF_VAR_db_pass" `
    -TestScript { -not [string]::IsNullOrWhiteSpace($env:TF_VAR_db_pass) } `
    -SuccessMessage "Database password is set" `
    -FailureMessage "Set: `$env:TF_VAR_db_pass = 'your_secure_password'"

Check-Requirement `
    -Name "TF_VAR_cloudflare_api_token" `
    -TestScript { -not [string]::IsNullOrWhiteSpace($env:TF_VAR_cloudflare_api_token) } `
    -SuccessMessage "Cloudflare API token is set" `
    -FailureMessage "Set: `$env:TF_VAR_cloudflare_api_token = 'your_token'"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "☁️  GCP AUTHENTICATION" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Check-Requirement `
    -Name "GCP Project Configuration" `
    -TestScript {
        $project = gcloud config get-value project 2>$null
        $project -eq "codex-dominion-prod"
    } `
    -SuccessMessage "GCP project is set to: codex-dominion-prod" `
    -FailureMessage "Run: gcloud config set project codex-dominion-prod"

Check-Requirement `
    -Name "GCP Authentication" `
    -TestScript {
        $auth = gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>$null
        -not [string]::IsNullOrWhiteSpace($auth)
    } `
    -SuccessMessage "Authenticated with GCP" `
    -FailureMessage "Run: gcloud auth login"

Check-Requirement `
    -Name "GCP Application Default Credentials" `
    -TestScript {
        Test-Path "$env:APPDATA\gcloud\application_default_credentials.json"
    } `
    -SuccessMessage "Application default credentials exist" `
    -FailureMessage "Run: gcloud auth application-default login"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "🚀 GITHUB REPOSITORY STATUS" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Check-Requirement `
    -Name "Git Repository" `
    -TestScript { Test-Path ".git" } `
    -SuccessMessage "Git repository initialized" `
    -FailureMessage "Not in a git repository"

Check-Requirement `
    -Name "GitHub Remote" `
    -TestScript {
        $remote = git remote get-url origin 2>$null
        $remote -like "*JermaineMerritt-ai/codexdominion-schemas*"
    } `
    -SuccessMessage "GitHub remote configured correctly" `
    -FailureMessage "Check: git remote -v" `
    -Critical $false

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "📋 TERRAFORM STATUS" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Check-Requirement `
    -Name "Terraform Configuration Files" `
    -TestScript {
        (Test-Path "main.tf") -and (Test-Path "variables.tf") -and (Test-Path "terraform.tfvars")
    } `
    -SuccessMessage "Terraform files exist" `
    -FailureMessage "Missing terraform configuration files"

Check-Requirement `
    -Name "Terraform Initialization" `
    -TestScript { Test-Path ".terraform" } `
    -SuccessMessage "Terraform is initialized" `
    -FailureMessage "Run: terraform init" `
    -Critical $false

Check-Requirement `
    -Name "No Exposed Secrets in terraform.tfvars" `
    -TestScript {
        $content = Get-Content "terraform.tfvars" -Raw
        -not ($content -match 'cloudflare_api_token\s*=\s*"[^"]{10,}"' -or $content -match 'db_pass\s*=\s*"[^"]{5,}"')
    } `
    -SuccessMessage "terraform.tfvars contains no exposed secrets" `
    -FailureMessage "Secrets found in terraform.tfvars - must use environment variables"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "📊 SUMMARY" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$passed = ($allChecks | Where-Object { $_.Status -eq "PASS" }).Count
$failed = ($allChecks | Where-Object { $_.Status -ne "PASS" }).Count
$criticalFailures = ($allChecks | Where-Object { $_.Status -ne "PASS" -and $_.Critical }).Count

Write-Host "Total Checks: $($allChecks.Count)" -ForegroundColor White
Write-Host "Passed: $passed" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host "Critical Failures: $criticalFailures" -ForegroundColor $(if ($criticalFailures -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($criticalFailed) {
    Write-Host "❌ DEPLOYMENT NOT READY" -ForegroundColor Red -BackgroundColor Black
    Write-Host ""
    Write-Host "Fix critical failures before deploying." -ForegroundColor Red
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Install missing tools" -ForegroundColor White
    Write-Host "2. Set required environment variables" -ForegroundColor White
    Write-Host "3. Configure GCP authentication" -ForegroundColor White
    Write-Host "4. Run this script again" -ForegroundColor White
    Write-Host ""
    exit 1
}
else {
    Write-Host "✅ DEPLOYMENT READY!" -ForegroundColor Green -BackgroundColor Black
    Write-Host ""
    Write-Host "You can proceed with deployment:" -ForegroundColor Green
    Write-Host ""
    Write-Host "1. Add GitHub secrets:" -ForegroundColor White
    Write-Host "   .\setup-github-secrets.ps1" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Initialize Terraform:" -ForegroundColor White
    Write-Host "   terraform init" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Review infrastructure plan:" -ForegroundColor White
    Write-Host "   terraform plan" -ForegroundColor Gray
    Write-Host ""
    Write-Host "4. Deploy infrastructure:" -ForegroundColor White
    Write-Host "   terraform apply" -ForegroundColor Gray
    Write-Host ""
    Write-Host "5. Commit and push to trigger workflows:" -ForegroundColor White
    Write-Host "   git add ." -ForegroundColor Gray
    Write-Host "   git commit -m 'Security: Remove exposed secrets, prepare for deployment'" -ForegroundColor Gray
    Write-Host "   git push origin main" -ForegroundColor Gray
    Write-Host ""
    exit 0
}
