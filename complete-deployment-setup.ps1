#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Complete Deployment Setup for Codex Dominion
.DESCRIPTION
    Fixes all deployment blockers:
    - Installs GitHub CLI
    - Fixes Terraform PATH
    - Configures GCP project
    - Guides Cloudflare token rotation
    - Sets environment variables
    - Initializes Terraform
#>

param(
    [switch]$SkipGitHubCLI,
    [switch]$SkipTerraform,
    [switch]$SkipGCP
)

$ErrorActionPreference = "Continue"
$WorkspaceRoot = $PSScriptRoot

Write-Host "`n🚀 Codex Dominion - Complete Deployment Setup" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host ""

# Track issues
$issues = @()
$fixed = @()

# ============================================
# 1. Install GitHub CLI
# ============================================
if (-not $SkipGitHubCLI) {
    Write-Host "`n📦 Step 1: GitHub CLI Installation" -ForegroundColor Yellow
    Write-Host "-" * 50
    
    $ghInstalled = Get-Command gh -ErrorAction SilentlyContinue
    if ($ghInstalled) {
        Write-Host "✅ GitHub CLI already installed: $($ghInstalled.Version)" -ForegroundColor Green
        $fixed += "GitHub CLI"
    } else {
        Write-Host "⚙️  Installing GitHub CLI..." -ForegroundColor Cyan
        try {
            # Try winget first
            $result = winget install --id GitHub.cli --exact --accept-source-agreements --accept-package-agreements 2>&1
            
            # Refresh PATH
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
            
            # Verify installation
            $ghInstalled = Get-Command gh -ErrorAction SilentlyContinue
            if ($ghInstalled) {
                Write-Host "✅ GitHub CLI installed successfully" -ForegroundColor Green
                Write-Host "   Version: $($ghInstalled.Version)" -ForegroundColor Gray
                Write-Host "   Path: $($ghInstalled.Source)" -ForegroundColor Gray
                $fixed += "GitHub CLI"
                
                # Authenticate
                Write-Host "`n🔐 Please authenticate with GitHub:" -ForegroundColor Cyan
                Write-Host "   Run: gh auth login" -ForegroundColor White
            } else {
                Write-Host "⚠️  Installation completed but 'gh' not found in PATH" -ForegroundColor Yellow
                Write-Host "   Please restart PowerShell or manually add to PATH" -ForegroundColor Yellow
                $issues += "GitHub CLI not in PATH (restart required)"
            }
        } catch {
            Write-Host "❌ Failed to install GitHub CLI: $_" -ForegroundColor Red
            Write-Host "   Manual install: https://cli.github.com/" -ForegroundColor Yellow
            $issues += "GitHub CLI installation failed"
        }
    }
}

# ============================================
# 2. Fix Terraform PATH
# ============================================
if (-not $SkipTerraform) {
    Write-Host "`n🔧 Step 2: Terraform PATH Configuration" -ForegroundColor Yellow
    Write-Host "-" * 50
    
    # Check if terraform is in PATH
    $tfInPath = Get-Command terraform -ErrorAction SilentlyContinue
    
    if ($tfInPath) {
        Write-Host "✅ Terraform already in PATH" -ForegroundColor Green
        Write-Host "   Version: $(terraform version -json | ConvertFrom-Json | Select-Object -ExpandProperty terraform_version)" -ForegroundColor Gray
        Write-Host "   Path: $($tfInPath.Source)" -ForegroundColor Gray
        $fixed += "Terraform PATH"
    } else {
        # Check if terraform.exe exists in workspace
        $workspaceTf = Join-Path $WorkspaceRoot "terraform.exe"
        if (Test-Path $workspaceTf) {
            Write-Host "⚙️  Found terraform.exe in workspace" -ForegroundColor Cyan
            Write-Host "   Path: $workspaceTf" -ForegroundColor Gray
            
            # Option 1: Add workspace to PATH (temporary)
            Write-Host "`n   Option 1: Add workspace to PATH (current session)" -ForegroundColor White
            $env:Path = "$WorkspaceRoot;$env:Path"
            
            # Verify
            $tfInPath = Get-Command terraform -ErrorAction SilentlyContinue
            if ($tfInPath) {
                Write-Host "✅ Terraform added to PATH (session only)" -ForegroundColor Green
                $fixed += "Terraform PATH (temporary)"
                
                # Offer permanent solution
                Write-Host "`n   💡 To make permanent, run as Administrator:" -ForegroundColor Cyan
                Write-Host '   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";' + $WorkspaceRoot + '", "User")' -ForegroundColor White
            } else {
                Write-Host "⚠️  Failed to add to PATH" -ForegroundColor Yellow
                $issues += "Terraform PATH configuration failed"
            }
        } else {
            Write-Host "❌ terraform.exe not found" -ForegroundColor Red
            Write-Host "   Expected: $workspaceTf" -ForegroundColor Gray
            Write-Host "   Download from: https://www.terraform.io/downloads" -ForegroundColor Yellow
            $issues += "Terraform not found"
        }
    }
}

# ============================================
# 3. Configure GCP Project
# ============================================
if (-not $SkipGCP) {
    Write-Host "`n☁️  Step 3: GCP Project Configuration" -ForegroundColor Yellow
    Write-Host "-" * 50
    
    $gcloudInstalled = Get-Command gcloud -ErrorAction SilentlyContinue
    if (-not $gcloudInstalled) {
        Write-Host "❌ gcloud CLI not found" -ForegroundColor Red
        Write-Host "   Install from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
        $issues += "gcloud CLI not installed"
    } else {
        Write-Host "✅ gcloud CLI found" -ForegroundColor Green
        
        # Get current project
        $currentProject = gcloud config get-value project 2>$null
        Write-Host "   Current project: $currentProject" -ForegroundColor Gray
        
        if ($currentProject -ne "codex-dominion-prod") {
            Write-Host "⚙️  Setting project to codex-dominion-prod..." -ForegroundColor Cyan
            try {
                gcloud config set project codex-dominion-prod 2>&1 | Out-Null
                $newProject = gcloud config get-value project 2>$null
                
                if ($newProject -eq "codex-dominion-prod") {
                    Write-Host "✅ GCP project configured: codex-dominion-prod" -ForegroundColor Green
                    $fixed += "GCP project"
                } else {
                    Write-Host "⚠️  Project may not have switched correctly" -ForegroundColor Yellow
                    $issues += "GCP project configuration uncertain"
                }
            } catch {
                Write-Host "❌ Failed to set GCP project: $_" -ForegroundColor Red
                $issues += "GCP project configuration failed"
            }
        } else {
            Write-Host "✅ Already configured: codex-dominion-prod" -ForegroundColor Green
            $fixed += "GCP project"
        }
        
        # Check authentication
        Write-Host "`n   Checking GCP authentication..." -ForegroundColor Cyan
        $authAccount = gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>$null
        if ($authAccount) {
            Write-Host "✅ Authenticated as: $authAccount" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Not authenticated with GCP" -ForegroundColor Yellow
            Write-Host "   Run: gcloud auth login" -ForegroundColor White
            Write-Host "   And: gcloud auth application-default login" -ForegroundColor White
            $issues += "GCP authentication required"
        }
    }
}

# ============================================
# 4. Cloudflare Token Rotation Guide
# ============================================
Write-Host "`n🔐 Step 4: Cloudflare Token Rotation (CRITICAL)" -ForegroundColor Yellow
Write-Host "-" * 50
Write-Host "⚠️  SECURITY ALERT: Cloudflare token exposed in git history" -ForegroundColor Red
Write-Host "   Exposed token: WuKuLdijG-JVTyTqH8SA7K3rOTBOB8DAePOd14On" -ForegroundColor Red
Write-Host ""
Write-Host "📋 Follow these steps:" -ForegroundColor Cyan
Write-Host "   1. Go to: https://dash.cloudflare.com/profile/api-tokens" -ForegroundColor White
Write-Host "   2. Find the exposed token and DELETE it" -ForegroundColor White
Write-Host "   3. Click 'Create Token'" -ForegroundColor White
Write-Host "   4. Use template: 'Edit zone DNS'" -ForegroundColor White
Write-Host "   5. Select your domain zone" -ForegroundColor White
Write-Host "   6. Click 'Continue to summary' → 'Create Token'" -ForegroundColor White
Write-Host "   7. Copy the NEW token" -ForegroundColor White
Write-Host ""
$newCloudflareToken = Read-Host "Paste NEW Cloudflare API token here (or press Enter to skip)"

if ($newCloudflareToken -and $newCloudflareToken.Length -gt 10) {
    Write-Host "✅ New Cloudflare token captured" -ForegroundColor Green
    $fixed += "Cloudflare token rotation"
} else {
    Write-Host "⚠️  Cloudflare token not updated" -ForegroundColor Yellow
    $issues += "Cloudflare token rotation required"
}

# ============================================
# 5. Environment Variables Setup
# ============================================
Write-Host "`n🔧 Step 5: Environment Variables Configuration" -ForegroundColor Yellow
Write-Host "-" * 50

# Generate secure database password
$dbPass = -join ((65..90) + (97..122) + (48..57) + (33,35,36,37,38,42,43,45,61) | Get-Random -Count 24 | ForEach-Object {[char]$_})

Write-Host "⚙️  Generating secure database password..." -ForegroundColor Cyan
Write-Host "   Generated: $dbPass" -ForegroundColor Gray

# Set environment variables
if ($newCloudflareToken) {
    $env:TF_VAR_cloudflare_api_token = $newCloudflareToken
    Write-Host "✅ Set: TF_VAR_cloudflare_api_token" -ForegroundColor Green
}

$env:TF_VAR_db_pass = $dbPass
Write-Host "✅ Set: TF_VAR_db_pass" -ForegroundColor Green

# Save to .env file
$envFilePath = Join-Path $WorkspaceRoot ".env"
$envContent = @"
# Codex Dominion Environment Variables
# Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

# Terraform Variables
TF_VAR_db_pass=$dbPass
"@

if ($newCloudflareToken) {
    $envContent += "`nTF_VAR_cloudflare_api_token=$newCloudflareToken"
}

try {
    $envContent | Out-File -FilePath $envFilePath -Encoding utf8 -Force
    Write-Host "✅ Environment variables saved to .env" -ForegroundColor Green
    $fixed += "Environment variables"
} catch {
    Write-Host "⚠️  Failed to save .env file: $_" -ForegroundColor Yellow
}

# ============================================
# 6. Initialize Terraform
# ============================================
Write-Host "`n🔨 Step 6: Terraform Initialization" -ForegroundColor Yellow
Write-Host "-" * 50

$tfAvailable = Get-Command terraform -ErrorAction SilentlyContinue
if (-not $tfAvailable) {
    Write-Host "⚠️  Terraform not available in PATH, trying workspace executable..." -ForegroundColor Yellow
    Push-Location $WorkspaceRoot
    $tfAvailable = Test-Path "./terraform.exe"
}

if ($tfAvailable) {
    try {
        Write-Host "⚙️  Running: terraform init" -ForegroundColor Cyan
        
        if (Test-Path "./terraform.exe") {
            $initOutput = .\terraform.exe init 2>&1
        } else {
            $initOutput = terraform init 2>&1
        }
        
        Write-Host $initOutput
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Terraform initialized successfully" -ForegroundColor Green
            $fixed += "Terraform initialization"
        } else {
            Write-Host "⚠️  Terraform init completed with warnings (exit code: $LASTEXITCODE)" -ForegroundColor Yellow
            $issues += "Terraform initialization had warnings"
        }
    } catch {
        Write-Host "❌ Terraform initialization failed: $_" -ForegroundColor Red
        $issues += "Terraform initialization failed"
    }
} else {
    Write-Host "❌ Terraform not available" -ForegroundColor Red
    $issues += "Terraform not available"
}

Pop-Location -ErrorAction SilentlyContinue

# ============================================
# 7. GitHub Secrets Setup
# ============================================
Write-Host "`n🔑 Step 7: GitHub Repository Secrets" -ForegroundColor Yellow
Write-Host "-" * 50

$ghAvailable = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghAvailable) {
    Write-Host "⚠️  GitHub CLI not available yet (may need restart)" -ForegroundColor Yellow
    Write-Host "   After restart, run: .\setup-github-secrets.ps1" -ForegroundColor White
    $issues += "GitHub secrets setup pending (restart required)"
} else {
    Write-Host "✅ GitHub CLI available" -ForegroundColor Green
    
    # Check if authenticated
    $ghAuth = gh auth status 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Already authenticated with GitHub" -ForegroundColor Green
        
        Write-Host "`n   Do you want to run GitHub secrets setup now? (y/n)" -ForegroundColor Cyan
        $runSecretsSetup = Read-Host
        
        if ($runSecretsSetup -eq 'y' -or $runSecretsSetup -eq 'Y') {
            Write-Host "⚙️  Running setup-github-secrets.ps1..." -ForegroundColor Cyan
            $secretsScriptPath = Join-Path $WorkspaceRoot "setup-github-secrets.ps1"
            
            if (Test-Path $secretsScriptPath) {
                & $secretsScriptPath
                $fixed += "GitHub secrets"
            } else {
                Write-Host "❌ setup-github-secrets.ps1 not found" -ForegroundColor Red
                $issues += "GitHub secrets script missing"
            }
        } else {
            Write-Host "⏭️  Skipped - run manually: .\setup-github-secrets.ps1" -ForegroundColor Yellow
            $issues += "GitHub secrets setup pending (user skipped)"
        }
    } else {
        Write-Host "⚠️  Not authenticated with GitHub" -ForegroundColor Yellow
        Write-Host "   Run: gh auth login" -ForegroundColor White
        Write-Host "   Then: .\setup-github-secrets.ps1" -ForegroundColor White
        $issues += "GitHub authentication required"
    }
}

# ============================================
# Summary
# ============================================
Write-Host "`n" -NoNewline
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host "📊 DEPLOYMENT SETUP SUMMARY" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

Write-Host "`n✅ Fixed ($($fixed.Count)):" -ForegroundColor Green
foreach ($item in $fixed) {
    Write-Host "   • $item" -ForegroundColor Green
}

if ($issues.Count -gt 0) {
    Write-Host "`n⚠️  Remaining Issues ($($issues.Count)):" -ForegroundColor Yellow
    foreach ($item in $issues) {
        Write-Host "   • $item" -ForegroundColor Yellow
    }
    
    Write-Host "`n❌ DEPLOYMENT NOT READY" -ForegroundColor Red
    Write-Host "   Please resolve remaining issues before deploying." -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "`n🎉 ALL DEPLOYMENT BLOCKERS RESOLVED!" -ForegroundColor Green
    Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
    Write-Host "   1. Verify: .\verify-deployment-ready.ps1" -ForegroundColor White
    Write-Host "   2. Review: terraform plan" -ForegroundColor White
    Write-Host "   3. Deploy: terraform apply" -ForegroundColor White
    Write-Host ""
    exit 0
}
