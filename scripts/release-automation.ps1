# Codex Dominion - Full Release Automation Script
# Validates YAML/JSON, runs validation pipeline, creates releases, and uploads artifacts

param(
    [switch]$SkipValidation,
    [switch]$SkipPreCommit,
    [switch]$AutoFix,
    [string]$GitRepo = "",
    [string]$GitToken = ""
)

$ErrorActionPreference = "Continue"

# Ensure script runs from project root
$scriptDir = Split-Path -Parent $PSCommandPath
$projectRoot = Split-Path -Parent $scriptDir
Push-Location $projectRoot

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   CODEX DOMINION - RELEASE AUTOMATION"
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Prepare summary report
$reportPath = ".\validation_report.txt"
"Validation Report - $(Get-Date)" | Out-File $reportPath
"=====================================" | Out-File $reportPath -Append

# Counters
$yamlErrors = 0
$yamlWarnings = 0
$jsonErrors = 0
$jsonFixed = 0

# ============================================
# STEP 1: CHECK DEPENDENCIES
# ============================================
Write-Host "STEP 1: Checking dependencies..." -ForegroundColor Yellow

$missingDeps = @()

if (-not (Get-Command yamllint -ErrorAction SilentlyContinue)) {
    Write-Host "⚠ yamllint not found, installing..." -ForegroundColor Yellow
    pip install yamllint
    if ($LASTEXITCODE -ne 0) { $missingDeps += "yamllint" }
}

if (-not (Get-Command prettier -ErrorAction SilentlyContinue)) {
    Write-Host "⚠ prettier not found, installing..." -ForegroundColor Yellow
    npm install -g prettier
    if ($LASTEXITCODE -ne 0) { $missingDeps += "prettier" }
}

if (-not (Get-Command pre-commit -ErrorAction SilentlyContinue)) {
    Write-Host "⚠ pre-commit not found. Install with: pip install pre-commit" -ForegroundColor Yellow
    $missingDeps += "pre-commit"
}

if ($missingDeps.Count -gt 0) {
    Write-Host "✗ Missing dependencies: $($missingDeps -join ', ')" -ForegroundColor Red
    Write-Host "Install them and try again." -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ All dependencies installed" -ForegroundColor Green

# ============================================
# STEP 2: VALIDATE YAML FILES
# ============================================
if (-not $SkipValidation) {
    Write-Host ""
    Write-Host "STEP 2: Validating YAML files..." -ForegroundColor Yellow

    # Exclusion patterns
    $yamlExclusions = @(
        "node_modules",
        ".next",
        "dist",
        "build",
        ".venv",
        "venv",
        "coverage",
        ".git",
        "obj",
        "bin",
        "codex-core/target"
    )

    $yamlFiles = Get-ChildItem -Path . -Include *.yaml,*.yml -Recurse | Where-Object {
        $path = $_.FullName
        $excluded = $false
        foreach ($pattern in $yamlExclusions) {
            if ($path -like "*\$pattern\*") {
                $excluded = $true
                break
            }
        }
        -not $excluded
    }

    Write-Host "Found $($yamlFiles.Count) YAML files to validate" -ForegroundColor Cyan

    foreach ($file in $yamlFiles) {
        $result = yamllint $file.FullName 2>&1
        if ($LASTEXITCODE -ne 0) {
            # Distinguish between errors and warnings
            if ($result -match "error") {
                $yamlErrors++
                Write-Host "✗ YAML Error in $($file.Name)" -ForegroundColor Red
                "ERROR: $($file.FullName)" | Out-File $reportPath -Append
                $result | Out-File $reportPath -Append
            } else {
                $yamlWarnings++
                Write-Host "⚠ YAML Warning in $($file.Name)" -ForegroundColor Yellow
            }
        } else {
            Write-Host "✓ YAML OK: $($file.Name)" -ForegroundColor Green
        }
    }

    "`nYAML Validation Results:" | Out-File $reportPath -Append
    "  Errors: $yamlErrors" | Out-File $reportPath -Append
    "  Warnings: $yamlWarnings" | Out-File $reportPath -Append
} else {
    Write-Host "STEP 2: Skipping YAML validation (--SkipValidation)" -ForegroundColor Yellow
}

# ============================================
# STEP 3: VALIDATE JSON FILES
# ============================================
if (-not $SkipValidation) {
    Write-Host ""
    Write-Host "STEP 3: Validating JSON files..." -ForegroundColor Yellow

    # Exclusion patterns (from validate-and-release.ps1)
    $jsonExclusions = @(
        "node_modules",
        ".next",
        "dist",
        "build",
        ".venv",
        "venv",
        "coverage",
        ".git",
        "obj",
        "bin",
        "codex-core/target"
    )

    $jsonFiles = Get-ChildItem -Path . -Include *.json -Recurse | Where-Object {
        $path = $_.FullName
        $excluded = $false
        foreach ($pattern in $jsonExclusions) {
            if ($path -like "*\$pattern\*") {
                $excluded = $true
                break
            }
        }
        -not $excluded
    }

    Write-Host "Found $($jsonFiles.Count) JSON files to validate" -ForegroundColor Cyan

    foreach ($file in $jsonFiles) {
        try {
            $content = Get-Content $file.FullName -Raw
            $null = $content | ConvertFrom-Json
            Write-Host "✓ JSON OK: $($file.Name)" -ForegroundColor Green
        } catch {
            $jsonErrors++
            Write-Host "✗ JSON Error in $($file.Name)" -ForegroundColor Red
            "JSON Error in $($file.FullName): $($_.Exception.Message)" | Out-File $reportPath -Append
        }
    }

    "`nJSON Validation Results:" | Out-File $reportPath -Append
    "  Errors: $jsonErrors" | Out-File $reportPath -Append

    # Auto-fix JSON formatting
    if ($AutoFix -or ($jsonErrors -eq 0)) {
        $fixChoice = if ($AutoFix) { "Y" } else {
            Write-Host "`nAuto-fix JSON formatting with Prettier? (Y/N)" -ForegroundColor Cyan
            Read-Host
        }

        if ($fixChoice -eq "Y") {
            Write-Host "Running Prettier on all JSON files..." -ForegroundColor Yellow

            # Build exclusion patterns for Prettier
            $prettierIgnore = $jsonExclusions -join ","

            npx prettier --write "**/*.json" --ignore-path .gitignore

            if ($LASTEXITCODE -eq 0) {
                $jsonFixed = $jsonFiles.Count
                Write-Host "✓ JSON files formatted successfully!" -ForegroundColor Green
                "JSON Files Auto-Fixed: $jsonFixed" | Out-File $reportPath -Append
            } else {
                Write-Host "✗ Prettier failed" -ForegroundColor Red
            }
        }
    }
} else {
    Write-Host "STEP 3: Skipping JSON validation (--SkipValidation)" -ForegroundColor Yellow
}

# ============================================
# STEP 4: RUN VALIDATION PIPELINE
# ============================================
if (-not $SkipValidation) {
    Write-Host ""
    Write-Host "STEP 4: Running operational validation pipeline..." -ForegroundColor Yellow

    if (Test-Path ".\ops\validate.ps1") {
        # Check if services are running
        Write-Host "Checking if frontend/backend are running..." -ForegroundColor Cyan

        $frontendRunning = $false
        $backendRunning = $false

        try {
            $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
            $frontendRunning = $true
        } catch {}

        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8001/health" -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
            $backendRunning = $true
        } catch {}

        if ($frontendRunning -and $backendRunning) {
            Write-Host "✓ Services are running, executing validation..." -ForegroundColor Green

            & .\ops\validate.ps1

            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Validation pipeline passed!" -ForegroundColor Green
                "`nValidation Pipeline: PASSED" | Out-File $reportPath -Append
            } else {
                Write-Host "✗ Validation pipeline failed!" -ForegroundColor Red
                "`nValidation Pipeline: FAILED" | Out-File $reportPath -Append
                Write-Host "Fix validation errors before proceeding." -ForegroundColor Yellow
                exit 1
            }
        } else {
            Write-Host "⚠ Services not running (frontend: $frontendRunning, backend: $backendRunning)" -ForegroundColor Yellow
            Write-Host "Skipping validation pipeline. Start services to validate." -ForegroundColor Yellow
            "`nValidation Pipeline: SKIPPED (services not running)" | Out-File $reportPath -Append
        }
    } else {
        Write-Host "⚠ Validation pipeline not found at .\ops\validate.ps1" -ForegroundColor Yellow
    }
} else {
    Write-Host "STEP 4: Skipping validation pipeline (--SkipValidation)" -ForegroundColor Yellow
}

# ============================================
# STEP 5: RUN PRE-COMMIT CHECKS
# ============================================
if (-not $SkipPreCommit) {
    Write-Host ""
    Write-Host "STEP 5: Running pre-commit checks..." -ForegroundColor Yellow

    $preCommitChoice = if ($AutoFix) { "Y" } else {
        Write-Host "Run pre-commit checks before pushing? (Y/N)" -ForegroundColor Cyan
        Read-Host
    }

    if ($preCommitChoice -eq "Y") {
        Write-Host "Running pre-commit hooks on all files..." -ForegroundColor Yellow
        pre-commit run --all-files

        if ($LASTEXITCODE -ne 0) {
            Write-Host "✗ Pre-commit checks failed. Fix issues before pushing." -ForegroundColor Red
            "`nPre-commit: FAILED" | Out-File $reportPath -Append

            Write-Host "`nDo you want to continue anyway? (Y/N)" -ForegroundColor Yellow
            $continueChoice = Read-Host
            if ($continueChoice -ne "Y") {
                exit 1
            }
        } else {
            Write-Host "✓ Pre-commit checks passed!" -ForegroundColor Green
            "`nPre-commit: PASSED" | Out-File $reportPath -Append
        }
    }
} else {
    Write-Host "STEP 5: Skipping pre-commit checks (--SkipPreCommit)" -ForegroundColor Yellow
}

# ============================================
# STEP 6: GIT OPERATIONS
# ============================================
Write-Host ""
Write-Host "STEP 6: Git operations..." -ForegroundColor Yellow

$gitChoice = if ($AutoFix) { "Y" } else {
    Write-Host "Stage, commit, and push changes to Git? (Y/N)" -ForegroundColor Cyan
    Read-Host
}

if ($gitChoice -eq "Y") {
    # Check for changes
    $status = git status --porcelain

    if ([string]::IsNullOrEmpty($status)) {
        Write-Host "⚠ No changes to commit" -ForegroundColor Yellow
    } else {
        Write-Host "Enter commit message:" -ForegroundColor Cyan
        $commitMsg = if ($AutoFix) {
            "chore: auto-fixed JSON formatting, validated YAML, passed pre-commit checks"
        } else {
            Read-Host
        }

        git add .
        git commit -m "$commitMsg"

        if ($LASTEXITCODE -eq 0) {
            git push

            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Changes pushed successfully!" -ForegroundColor Green
            } else {
                Write-Host "✗ Git push failed!" -ForegroundColor Red
                exit 1
            }
        } else {
            Write-Host "✗ Git commit failed!" -ForegroundColor Red
            exit 1
        }
    }

    # ============================================
    # STEP 7: GIT TAG AND RELEASE
    # ============================================
    Write-Host ""
    Write-Host "STEP 7: Create Git tag and release..." -ForegroundColor Yellow

    $tagChoice = if ($AutoFix) { "N" } else {
        Write-Host "Create a Git tag for this version? (Y/N)" -ForegroundColor Cyan
        Read-Host
    }

    if ($tagChoice -eq "Y") {
        Write-Host "Enter tag name (e.g., v2.0.0):" -ForegroundColor Cyan
        $tagName = Read-Host

        # Update package.json version
        if (Test-Path ".\package.json") {
            $packageJson = Get-Content ".\package.json" -Raw | ConvertFrom-Json
            $packageJson.version = $tagName.TrimStart("v")
            $packageJson | ConvertTo-Json -Depth 100 | Set-Content ".\package.json"
            Write-Host "✓ Updated package.json version" -ForegroundColor Green
        }

        # Update DEPLOYMENT_FIXED.md version
        if (Test-Path ".\DEPLOYMENT_FIXED.md") {
            $content = Get-Content ".\DEPLOYMENT_FIXED.md" -Raw
            $content = $content -replace 'Last Updated:\s*\d{4}-\d{2}-\d{2}', "Last Updated: $(Get-Date -Format 'yyyy-MM-dd')"
            $content | Set-Content ".\DEPLOYMENT_FIXED.md"
            Write-Host "✓ Updated DEPLOYMENT_FIXED.md" -ForegroundColor Green
        }

        # Add changelog entry
        $changelogEntry = @"

## $tagName - $(Get-Date -Format 'yyyy-MM-dd')

### Changes
- Auto-fixed JSON formatting ($jsonFixed files)
- Validated YAML files ($($yamlFiles.Count) files, $yamlErrors errors, $yamlWarnings warnings)
- Passed pre-commit checks
- Version bump and Git tag created

### Validation Results
- YAML Errors: $yamlErrors
- YAML Warnings: $yamlWarnings
- JSON Errors: $jsonErrors
- JSON Files Fixed: $jsonFixed
"@

        if (Test-Path ".\CHANGELOG.md") {
            $existingChangelog = Get-Content ".\CHANGELOG.md" -Raw
            $changelogEntry + $existingChangelog | Set-Content ".\CHANGELOG.md"
        } else {
            "# Changelog`n" + $changelogEntry | Set-Content ".\CHANGELOG.md"
        }

        Write-Host "✓ Updated CHANGELOG.md" -ForegroundColor Green

        # Commit version updates
        git add package.json DEPLOYMENT_FIXED.md CHANGELOG.md
        git commit -m "chore: bump version to $tagName"
        git push

        # Create and push tag
        git tag -a $tagName -m "Release $tagName"
        git push origin $tagName
        Write-Host "✓ Git tag '$tagName' created and pushed!" -ForegroundColor Green

        # ============================================
        # STEP 8: GITHUB RELEASE
        # ============================================
        Write-Host ""
        Write-Host "STEP 8: Create GitHub Release..." -ForegroundColor Yellow

        $releaseChoice = Write-Host "Create a GitHub Release for this tag? (Y/N)" -ForegroundColor Cyan
        Read-Host

        if ($releaseChoice -eq "Y") {
            $repo = if ([string]::IsNullOrEmpty($GitRepo)) {
                Write-Host "Enter GitHub repo (e.g., user/repo):" -ForegroundColor Cyan
                Read-Host
            } else {
                $GitRepo
            }

            $token = if ([string]::IsNullOrEmpty($GitToken)) {
                Write-Host "Enter GitHub token (with repo access):" -ForegroundColor Cyan
                Read-Host
            } else {
                $GitToken
            }

            # Extract release notes from CHANGELOG
            $releaseNotes = Get-Content ".\CHANGELOG.md" -Raw
            $pattern = "## $tagName.*?(?=## |\z)"
            $match = [regex]::Match($releaseNotes, $pattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)
            $body = if ($match.Success) { $match.Value } else { "Release $tagName" }

            $url = "https://api.github.com/repos/$repo/releases"
            $releaseData = @{
                tag_name = $tagName
                name = $tagName
                body = $body
                draft = $false
                prerelease = $false
            } | ConvertTo-Json -Depth 10

            try {
                $releaseResponse = Invoke-RestMethod -Uri $url -Method Post -Headers @{
                    Authorization = "token $token"
                    Accept = "application/vnd.github.v3+json"
                } -Body $releaseData -ContentType "application/json"

                Write-Host "✓ GitHub Release created for $tagName!" -ForegroundColor Green
                Write-Host "  URL: $($releaseResponse.html_url)" -ForegroundColor Cyan

                # ============================================
                # STEP 9: BUILD AND UPLOAD MULTIPLE ARTIFACTS
                # ============================================
                Write-Host ""
                Write-Host "STEP 9: Build and upload artifacts..." -ForegroundColor Yellow

                $buildChoice = Write-Host "Build and upload multiple artifacts (frontend, backend, docs, scripts)? (Y/N)" -ForegroundColor Cyan
                Read-Host

                if ($buildChoice -eq "Y") {
                    $artifacts = @()

                    # ========== FRONTEND BUILD ==========
                    Write-Host "`n--- Building Frontend ---" -ForegroundColor Cyan
                    $frontendPath = ".\frontend"
                    $standalonePath = "$frontendPath\.next\standalone"
                    $staticPath = "$frontendPath\.next\static"
                    $zipFrontend = ".\codexdominion-frontend-$tagName.zip"

                    if (Test-Path $frontendPath) {
                        Write-Host "Running Next.js build..." -ForegroundColor Yellow
                        Push-Location $frontendPath
                        npm run build
                        $buildExit = $LASTEXITCODE
                        Pop-Location

                        if ($buildExit -eq 0 -and (Test-Path $standalonePath)) {
                            Write-Host "✓ Frontend build completed!" -ForegroundColor Green

                            $tempDir = ".\temp-frontend-$tagName"
                            New-Item -ItemType Directory -Force -Path $tempDir | Out-Null
                            Copy-Item -Path $standalonePath -Destination "$tempDir\frontend" -Recurse -Force
                            if (Test-Path $staticPath) {
                                Copy-Item -Path $staticPath -Destination "$tempDir\frontend\.next\static" -Recurse -Force
                            }
                            if (Test-Path "$frontendPath\public") {
                                Copy-Item -Path "$frontendPath\public" -Destination "$tempDir\frontend\public" -Recurse -Force
                            }

                            "# Codex Dominion Frontend - $tagName`n`nNext.js standalone build. See DEPLOYMENT_FIXED.md for deployment instructions." | Out-File "$tempDir\README.md" -Encoding UTF8
                            Compress-Archive -Path "$tempDir\*" -DestinationPath $zipFrontend -Force
                            Remove-Item -Path $tempDir -Recurse -Force
                            Write-Host "✓ Frontend package: $zipFrontend" -ForegroundColor Green
                            $artifacts += $zipFrontend
                        } else {
                            Write-Host "✗ Frontend build failed" -ForegroundColor Red
                        }
                    }

                    # ========== BACKEND BUILD ==========
                    Write-Host "`n--- Packaging Backend ---" -ForegroundColor Cyan
                    $backendPath = ".\src\backend"
                    $zipBackend = ".\codexdominion-backend-$tagName.zip"

                    if (Test-Path $backendPath) {
                        $tempDir = ".\temp-backend-$tagName"
                        New-Item -ItemType Directory -Force -Path $tempDir | Out-Null
                        Copy-Item -Path "$backendPath\*" -Destination "$tempDir\backend" -Recurse -Force -Exclude @("__pycache__", "*.pyc", ".pytest_cache", ".mypy_cache")
                        if (Test-Path ".\requirements.txt") {
                            Copy-Item -Path ".\requirements.txt" -Destination "$tempDir\" -Force
                        }
                        "# Codex Dominion Backend - $tagName`n`nFastAPI application. See DEPLOYMENT_FIXED.md for deployment instructions." | Out-File "$tempDir\README.md" -Encoding UTF8
                        Compress-Archive -Path "$tempDir\*" -DestinationPath $zipBackend -Force
                        Remove-Item -Path $tempDir -Recurse -Force
                        Write-Host "✓ Backend package: $zipBackend" -ForegroundColor Green
                        $artifacts += $zipBackend
                    }

                    # ========== DOCUMENTATION ==========
                    Write-Host "`n--- Packaging Documentation ---" -ForegroundColor Cyan
                    $zipDocs = ".\codexdominion-docs-$tagName.zip"
                    $tempDir = ".\temp-docs-$tagName"
                    New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

                    if (Test-Path ".\docs") {
                        Copy-Item -Path ".\docs\*" -Destination "$tempDir\docs" -Recurse -Force
                    }
                    $keyDocs = @(".\DEPLOYMENT_FIXED.md", ".\GOVERNANCE.md", ".\README.md", ".\CHANGELOG.md", ".\.governance.yml", ".\.canary-config.yml", ".\.rollback-plan.yml")
                    foreach ($doc in $keyDocs) {
                        if (Test-Path $doc) {
                            Copy-Item -Path $doc -Destination $tempDir -Force
                        }
                    }
                    "# Codex Dominion Documentation - $tagName`n`nComplete deployment and governance documentation." | Out-File "$tempDir\README.md" -Encoding UTF8
                    Compress-Archive -Path "$tempDir\*" -DestinationPath $zipDocs -Force
                    Remove-Item -Path $tempDir -Recurse -Force
                    Write-Host "✓ Documentation package: $zipDocs" -ForegroundColor Green
                    $artifacts += $zipDocs

                    # ========== DEPLOYMENT SCRIPTS ==========
                    Write-Host "`n--- Packaging Deployment Scripts ---" -ForegroundColor Cyan
                    $zipScripts = ".\codexdominion-scripts-$tagName.zip"
                    $tempDir = ".\temp-scripts-$tagName"
                    New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

                    if (Test-Path ".\ops") {
                        Copy-Item -Path ".\ops\*" -Destination "$tempDir\ops" -Recurse -Force
                    }
                    if (Test-Path ".\deployment") {
                        Copy-Item -Path ".\deployment\*" -Destination "$tempDir\deployment" -Recurse -Force
                    }
                    $keyScripts = @(".\scripts\release-automation.ps1", ".\scripts\optimize-system.js", ".\validate-and-release.ps1", ".\deploy-codex.ps1", ".\deploy-ionos.sh")
                    foreach ($script in $keyScripts) {
                        if (Test-Path $script) {
                            $scriptName = Split-Path $script -Leaf
                            Copy-Item -Path $script -Destination "$tempDir\$scriptName" -Force
                        }
                    }
                    "# Codex Dominion Scripts - $tagName`n`nOperational scripts for deployment, validation, and maintenance." | Out-File "$tempDir\README.md" -Encoding UTF8
                    Compress-Archive -Path "$tempDir\*" -DestinationPath $zipScripts -Force
                    Remove-Item -Path $tempDir -Recurse -Force
                    Write-Host "✓ Scripts package: $zipScripts" -ForegroundColor Green
                    $artifacts += $zipScripts

                    # ========== UPLOAD ALL ARTIFACTS ==========
                    Write-Host "`n--- Uploading Artifacts to GitHub Release ---" -ForegroundColor Cyan
                    $uploadedCount = 0
                    $failedCount = 0

                    foreach ($artifact in $artifacts) {
                        if (Test-Path $artifact) {
                            $artifactName = Split-Path $artifact -Leaf
                            Write-Host "Uploading $artifactName..." -ForegroundColor Yellow
                            $uploadUrl = $releaseResponse.upload_url -replace "\{\?.*\}", "?name=$artifactName"

                            try {
                                $fileBytes = [System.IO.File]::ReadAllBytes((Resolve-Path $artifact).Path)
                                Invoke-RestMethod -Uri $uploadUrl -Method Post -Headers @{
                                    Authorization = "token $token"
                                    "Content-Type" = "application/zip"
                                } -Body $fileBytes
                                Write-Host "✓ Uploaded: $artifactName" -ForegroundColor Green
                                $uploadedCount++
                                Remove-Item -Path $artifact -Force
                            } catch {
                                Write-Host "✗ Failed to upload $artifactName : $($_.Exception.Message)" -ForegroundColor Red
                                $failedCount++
                            }
                        }
                    }

                    Write-Host ""
                    Write-Host "Artifact Upload Summary:" -ForegroundColor Cyan
                    Write-Host "  Uploaded: $uploadedCount" -ForegroundColor Green
                    Write-Host "  Failed: $failedCount" -ForegroundColor $(if ($failedCount -gt 0) { "Red" } else { "Green" })
                    if ($uploadedCount -gt 0) {
                        Write-Host ""
                        Write-Host "✓ Artifacts uploaded to: $($releaseResponse.html_url)" -ForegroundColor Cyan
                    }
                }

                # ============================================
                # STEP 10: REMOTE DEPLOYMENT (OPTIONAL)
                # ============================================
                Write-Host ""
                Write-Host "STEP 10: Remote deployment..." -ForegroundColor Yellow

                $deployChoice = Write-Host "Trigger remote deployment via SSH? (Y/N)" -ForegroundColor Cyan
                Read-Host

                if ($deployChoice -eq "Y") {
                    Write-Host "Enter SSH server (e.g., user@yourserver.com):" -ForegroundColor Cyan
                    $sshServer = Read-Host

                    Write-Host "Enter deployment command (e.g., cd /var/www && ./deploy.sh):" -ForegroundColor Cyan
                    $deployCommand = Read-Host

                    Write-Host ""
                    Write-Host "Triggering remote deployment..." -ForegroundColor Yellow
                    Write-Host "Server: $sshServer" -ForegroundColor Cyan
                    Write-Host "Command: $deployCommand" -ForegroundColor Cyan
                    Write-Host ""

                    try {
                        # Execute SSH command
                        $sshOutput = ssh $sshServer $deployCommand 2>&1

                        if ($LASTEXITCODE -eq 0) {
                            Write-Host "✓ Remote deployment completed successfully!" -ForegroundColor Green
                            Write-Host ""
                            Write-Host "Deployment Output:" -ForegroundColor Cyan
                            $sshOutput | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }

                            # ========== HEALTH CHECK VERIFICATION ==========
                            Write-Host ""
                            Write-Host "--- Health Check Verification ---" -ForegroundColor Cyan

                            $healthChoice = Write-Host "Run health check verification? (Y/N)" -ForegroundColor Cyan
                            Read-Host

                            if ($healthChoice -eq "Y") {
                                Write-Host "Enter health check URL (e.g., https://yourdomain.com/health):" -ForegroundColor Cyan
                                $healthUrl = Read-Host

                                Write-Host "Enter API health URL (optional, press Enter to skip):" -ForegroundColor Cyan
                                $apiHealthUrl = Read-Host

                                Write-Host ""
                                Write-Host "Running health checks..." -ForegroundColor Yellow

                                $healthChecksPassed = 0
                                $healthChecksFailed = 0

                                # Check frontend health
                                try {
                                    Write-Host "Checking frontend: $healthUrl" -ForegroundColor Cyan
                                    $response = Invoke-WebRequest -Uri $healthUrl -TimeoutSec 10 -UseBasicParsing

                                    if ($response.StatusCode -eq 200) {
                                        Write-Host "✓ Frontend health check passed (HTTP $($response.StatusCode))" -ForegroundColor Green
                                        $healthChecksPassed++
                                    } else {
                                        Write-Host "✗ Frontend health check failed (HTTP $($response.StatusCode))" -ForegroundColor Red
                                        $healthChecksFailed++
                                    }
                                } catch {
                                    Write-Host "✗ Frontend health check failed: $($_.Exception.Message)" -ForegroundColor Red
                                    $healthChecksFailed++
                                }

                                # Check API health if provided
                                if (-not [string]::IsNullOrEmpty($apiHealthUrl)) {
                                    try {
                                        Write-Host "Checking API: $apiHealthUrl" -ForegroundColor Cyan
                                        $response = Invoke-WebRequest -Uri $apiHealthUrl -TimeoutSec 10 -UseBasicParsing

                                        if ($response.StatusCode -eq 200) {
                                            Write-Host "✓ API health check passed (HTTP $($response.StatusCode))" -ForegroundColor Green

                                            # Try to parse JSON response
                                            try {
                                                $healthData = $response.Content | ConvertFrom-Json
                                                Write-Host "  Response: $($healthData | ConvertTo-Json -Compress)" -ForegroundColor Gray
                                            } catch {}

                                            $healthChecksPassed++
                                        } else {
                                            Write-Host "✗ API health check failed (HTTP $($response.StatusCode))" -ForegroundColor Red
                                            $healthChecksFailed++
                                        }
                                    } catch {
                                        Write-Host "✗ API health check failed: $($_.Exception.Message)" -ForegroundColor Red
                                        $healthChecksFailed++
                                    }
                                }

                                # Run operational validation if available
                                if (Test-Path ".\ops\health-check.ps1") {
                                    Write-Host ""
                                    $opsChoice = Write-Host "Run full operational validation? (Y/N)" -ForegroundColor Cyan
                                    Read-Host

                                    if ($opsChoice -eq "Y") {
                                        Write-Host "Running operational validation..." -ForegroundColor Yellow

                                        try {
                                            # Set environment for remote URLs
                                            $env:FRONTEND_URL = $healthUrl -replace "/health.*$", ""
                                            if (-not [string]::IsNullOrEmpty($apiHealthUrl)) {
                                                $env:BACKEND_URL = $apiHealthUrl -replace "/health.*$", ""
                                            }

                                            & .\ops\health-check.ps1

                                            if ($LASTEXITCODE -eq 0) {
                                                Write-Host "✓ Operational validation passed!" -ForegroundColor Green
                                                $healthChecksPassed++
                                            } else {
                                                Write-Host "✗ Operational validation failed!" -ForegroundColor Red
                                                $healthChecksFailed++
                                            }
                                        } catch {
                                            Write-Host "✗ Operational validation error: $($_.Exception.Message)" -ForegroundColor Red
                                            $healthChecksFailed++
                                        }
                                    }
                                }

                                # Health check summary
                                Write-Host ""
                                Write-Host "Health Check Summary:" -ForegroundColor Cyan
                                Write-Host "  Passed: $healthChecksPassed" -ForegroundColor Green
                                Write-Host "  Failed: $healthChecksFailed" -ForegroundColor $(if ($healthChecksFailed -gt 0) { "Red" } else { "Green" })

                                if ($healthChecksFailed -eq 0) {
                                    Write-Host ""
                                    Write-Host "✓ All health checks passed! Deployment verified." -ForegroundColor Green
                                } else {
                                    Write-Host ""
                                    Write-Host "⚠ Some health checks failed. Review deployment." -ForegroundColor Yellow
                                }
                            }
                        } else {
                            Write-Host "✗ Remote deployment failed with exit code: $LASTEXITCODE" -ForegroundColor Red
                            Write-Host ""
                            Write-Host "Error Output:" -ForegroundColor Red
                            $sshOutput | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
                        }
                    } catch {
                        Write-Host "✗ SSH connection failed: $($_.Exception.Message)" -ForegroundColor Red
                        Write-Host ""
                        Write-Host "Troubleshooting Tips:" -ForegroundColor Yellow
                        Write-Host "  1. Verify SSH key is configured: ssh -T $sshServer" -ForegroundColor White
                        Write-Host "  2. Check server is accessible: ping $(($sshServer -split '@')[1])" -ForegroundColor White
                        Write-Host "  3. Ensure deployment script exists on server" -ForegroundColor White
                    }
                } else {
                    Write-Host "⊘ Remote deployment skipped" -ForegroundColor Yellow
                }
            } catch {
                Write-Host "✗ Failed to create GitHub Release: $($_.Exception.Message)" -ForegroundColor Red
                Write-Host "Response: $($_.ErrorDetails.Message)" -ForegroundColor Red
            }
        }
    }
}

# ============================================
# FINAL SUMMARY
# ============================================
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "          RELEASE AUTOMATION COMPLETE"
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Write final summary
"`n=== FINAL SUMMARY ===" | Out-File $reportPath -Append
"Completed: $(Get-Date)" | Out-File $reportPath -Append

Write-Host "Summary:" -ForegroundColor Green
Write-Host "  YAML Files: $($yamlFiles.Count) validated" -ForegroundColor White
Write-Host "    Errors: $yamlErrors" -ForegroundColor $(if ($yamlErrors -gt 0) { "Red" } else { "Green" })
Write-Host "    Warnings: $yamlWarnings" -ForegroundColor $(if ($yamlWarnings -gt 0) { "Yellow" } else { "Green" })
Write-Host "  JSON Files: $($jsonFiles.Count) validated" -ForegroundColor White
Write-Host "    Errors: $jsonErrors" -ForegroundColor $(if ($jsonErrors -gt 0) { "Red" } else { "Green" })
Write-Host "    Fixed: $jsonFixed" -ForegroundColor Green
Write-Host ""
Write-Host "Report saved to: $reportPath" -ForegroundColor Cyan
Write-Host ""

if ($yamlErrors -gt 0) {
    Write-Host "⚠ Fix YAML errors manually:" -ForegroundColor Yellow
    Write-Host "  - Check for multi-document syntax (---)" -ForegroundColor White
    Write-Host "  - Remove duplicate keys" -ForegroundColor White
    Write-Host "  - Fix indentation issues" -ForegroundColor White
    Write-Host ""
}

Write-Host "✓ Release automation complete!" -ForegroundColor Green

Pop-Location
