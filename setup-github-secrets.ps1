# Setup GitHub Repository Secrets for Codex Dominion
# This script adds all required secrets to your GitHub repository
# Run this script: .\setup-github-secrets.ps1

# Prerequisites: GitHub CLI must be installed
# Install: winget install GitHub.cli
# Authenticate: gh auth login

Write-Host "🔐 Codex Dominion - GitHub Secrets Setup" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if GitHub CLI is installed
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "❌ GitHub CLI not found!" -ForegroundColor Red
    Write-Host "Install with: winget install GitHub.cli" -ForegroundColor Yellow
    Write-Host "Then run: gh auth login" -ForegroundColor Yellow
    exit 1
}

# Check if authenticated
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Not authenticated with GitHub CLI" -ForegroundColor Red
    Write-Host "Run: gh auth login" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ GitHub CLI authenticated" -ForegroundColor Green
Write-Host ""

# Repository information
$repo = "JermaineMerritt-ai/codexdominion-schemas"
Write-Host "Repository: $repo" -ForegroundColor Cyan
Write-Host ""

# Function to add secret
function Add-GitHubSecret {
    param(
        [string]$Name,
        [string]$Description,
        [bool]$Required = $true
    )
    
    $prompt = if ($Required) { "$Description (REQUIRED)" } else { "$Description (Optional)" }
    
    if ($Name -eq "VPS_KEY") {
        Write-Host "📝 $prompt" -ForegroundColor Yellow
        Write-Host "   Paste your private SSH key (Ctrl+D when done or leave empty to skip):" -ForegroundColor Gray
        $value = ""
        while ($true) {
            $line = Read-Host
            if ([string]::IsNullOrWhiteSpace($line)) { break }
            $value += $line + "`n"
        }
    }
    elseif ($Name -eq "AZURE_CREDENTIALS") {
        Write-Host "📝 $prompt" -ForegroundColor Yellow
        Write-Host "   Paste your Azure service principal JSON (or leave empty to skip):" -ForegroundColor Gray
        $value = Read-Host -AsSecureString
        $value = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($value))
    }
    else {
        Write-Host "📝 $prompt" -ForegroundColor Yellow
        if ($Required) {
            while ([string]::IsNullOrWhiteSpace($value)) {
                $value = Read-Host "   Enter value"
            }
        }
        else {
            $value = Read-Host "   Enter value (or leave empty to skip)"
        }
    }
    
    if (-not [string]::IsNullOrWhiteSpace($value)) {
        try {
            $value | gh secret set $Name --repo $repo 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "   ✅ $Name added successfully" -ForegroundColor Green
            }
            else {
                Write-Host "   ❌ Failed to add $Name" -ForegroundColor Red
            }
        }
        catch {
            Write-Host "   ❌ Error adding $Name : $_" -ForegroundColor Red
        }
    }
    else {
        Write-Host "   ⏭️  Skipped $Name" -ForegroundColor Gray
    }
    Write-Host ""
}

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🚀 VPS DEPLOYMENT SECRETS" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Add-GitHubSecret -Name "VPS_HOST" -Description "VPS IP address (e.g., 98.19.211.133)"
Add-GitHubSecret -Name "VPS_USER" -Description "SSH username (e.g., root)"
Add-GitHubSecret -Name "VPS_KEY" -Description "Private SSH key for VPS access"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "☁️  IONOS CLOUD SECRETS" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Add-GitHubSecret -Name "IONOS_USERNAME" -Description "IONOS Cloud email/username"
Add-GitHubSecret -Name "IONOS_PASSWORD" -Description "IONOS Cloud password"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🐳 AZURE CONTAINER REGISTRY" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Add-GitHubSecret -Name "ACR_LOGIN_SERVER" -Description "Azure Container Registry server (e.g., codexdominion.azurecr.io)"
Add-GitHubSecret -Name "AZURE_CREDENTIALS" -Description "Azure service principal JSON"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "☁️  AWS CREDENTIALS" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Add-GitHubSecret -Name "AWS_ACCESS_KEY_ID" -Description "AWS access key ID"
Add-GitHubSecret -Name "AWS_SECRET_ACCESS_KEY" -Description "AWS secret access key"
Add-GitHubSecret -Name "AWS_REGION" -Description "AWS region (e.g., us-east-1)" -Required $false

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🤖 APPLICATION SECRETS" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Add-GitHubSecret -Name "SUPER_AI_TOKEN" -Description "Super Action AI authentication token"
Add-GitHubSecret -Name "DEPLOY_URL" -Description "Deployment target URL"
Add-GitHubSecret -Name "CODE_DEPEND_ON_SCHEMAS" -Description "Enable schema validation (set to 'true')" -Required $false

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "📢 NOTIFICATION WEBHOOKS (Optional)" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

Add-GitHubSecret -Name "SLACK_WEBHOOK_URL" -Description "Slack webhook for deployment notifications" -Required $false
Add-GitHubSecret -Name "DISCORD_WEBHOOK_URL" -Description "Discord webhook for alerts" -Required $false

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "✅ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Verify secrets: gh secret list --repo $repo" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Set local environment variables for Terraform" -ForegroundColor White
Write-Host "   `$env:TF_VAR_db_pass = 'your_secure_password'" -ForegroundColor Gray
Write-Host "   `$env:TF_VAR_cloudflare_api_token = 'your_token'" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Run deployment verification:" -ForegroundColor White
Write-Host "   .\verify-deployment-ready.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Deploy infrastructure:" -ForegroundColor White
Write-Host "   terraform init" -ForegroundColor Gray
Write-Host "   terraform plan" -ForegroundColor Gray
Write-Host "   terraform apply" -ForegroundColor Gray
Write-Host ""
