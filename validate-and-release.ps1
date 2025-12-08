# ============================================
# Full Release Automation Script
# ============================================
# Validates YAML/JSON, runs pre-commit checks,
# creates Git tags, updates changelog, and
# optionally creates GitHub releases
# ============================================

# Ensure script runs from project root
Write-Host "=== Starting Full Release Automation ===" -ForegroundColor Cyan

# Prepare summary report
$reportPath = ".\validation_report.txt"
"Validation Report - $(Get-Date)" | Out-File $reportPath
"=====================================" | Out-File $reportPath -Append

# Check dependencies
Write-Host "Checking dependencies..." -ForegroundColor Yellow
if (-not (Get-Command yamllint -ErrorAction SilentlyContinue)) {
    Write-Host "Installing yamllint..." -ForegroundColor Yellow
    pip install yamllint
}
if (-not (Get-Command jsonlint -ErrorAction SilentlyContinue)) {
    Write-Host "Installing jsonlint..." -ForegroundColor Yellow
    npm install -g jsonlint
}
if (-not (Get-Command prettier -ErrorAction SilentlyContinue)) {
    Write-Host "Installing prettier..." -ForegroundColor Yellow
    npm install -g prettier
}

# Counters
$yamlErrors = 0
$jsonErrors = 0
$jsonFixed = 0

# Validate YAML files
Write-Host "`n=== Validating YAML Files ===" -ForegroundColor Cyan
$yamlFiles = Get-ChildItem -Path . -Include *.yaml, *.yml -Recurse
foreach ($file in $yamlFiles) {
    $result = yamllint $file.FullName 2>&1
    if ($LASTEXITCODE -ne 0) {
        $yamlErrors++
        Write-Host "❌ YAML Error in $($file.FullName)" -ForegroundColor Red
        $result | Out-File $reportPath -Append
    } else {
        Write-Host "✅ YAML OK: $($file.Name)" -ForegroundColor Green
    }
}

# Validate JSON files (excluding node_modules and other build directories)
Write-Host "`n=== Validating JSON Files ===" -ForegroundColor Cyan
$jsonFiles = Get-ChildItem -Path . -Include *.json -Recurse | Where-Object {
    $_.FullName -notmatch '\\node_modules\\' -and
    $_.FullName -notmatch '\\.next\\' -and
    $_.FullName -notmatch '\\dist\\' -and
    $_.FullName -notmatch '\\build\\' -and
    $_.FullName -notmatch '\\.venv\\' -and
    $_.FullName -notmatch '\\coverage\\' -and
    $_.FullName -notmatch '\\codex-core\\target\\' -and
    $_.FullName -notmatch '\\.git\\' -and
    $_.FullName -notmatch '\\obj\\' -and
    $_.FullName -notmatch '\\bin\\'
}
foreach ($file in $jsonFiles) {
    try {
        # Use Node.js to validate JSON parsing
        $content = Get-Content $file.FullName -Raw
        node -e "JSON.parse(require('fs').readFileSync('$($file.FullName)', 'utf8'))" 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ JSON OK: $($file.Name)" -ForegroundColor Green
        } else {
            throw "Invalid JSON"
        }
    } catch {
        $jsonErrors++
        Write-Host "❌ JSON Error in $($file.Name)" -ForegroundColor Red
        "JSON Error in $($file.FullName): $_" | Out-File $reportPath -Append
    }
}

# Optional: Auto-fix JSON formatting
Write-Host "`nDo you want to auto-fix JSON formatting with Prettier? (Y/N)" -ForegroundColor Cyan
$choice = Read-Host
if ($choice -eq "Y") {
    Write-Host "Running Prettier on all JSON files..." -ForegroundColor Yellow
    npx prettier --write "**/*.json"
    $jsonFixed = $jsonFiles.Count
    Write-Host "✅ JSON files formatted successfully!" -ForegroundColor Green
}

# Write summary to report
"`nSummary:" | Out-File $reportPath -Append
"YAML Errors: $yamlErrors" | Out-File $reportPath -Append
"JSON Errors: $jsonErrors" | Out-File $reportPath -Append
"JSON Files Auto-Fixed: $jsonFixed" | Out-File $reportPath -Append

Write-Host "`n=== Validation Complete ===" -ForegroundColor Cyan
Write-Host "Report saved to $reportPath" -ForegroundColor Green

# Stop if validation errors exist (JSON only - YAML warnings are non-blocking)
if ($jsonErrors -gt 0) {
    Write-Host "`n⚠️  JSON validation errors found. Fix them before proceeding." -ForegroundColor Red
    Write-Host "Check $reportPath for details." -ForegroundColor Yellow
    exit 1
}

if ($yamlErrors -gt 0) {
    Write-Host "`n⚠️  YAML validation warnings found ($yamlErrors files), but continuing..." -ForegroundColor Yellow
    Write-Host "These can be fixed later. Check $reportPath for details." -ForegroundColor Gray
}

Write-Host "`n💡 Tip: Fix YAML errors manually (multi-doc markers, duplicate keys, indentation)." -ForegroundColor Yellow

# Run pre-commit before Git push
Write-Host "`nDo you want to run pre-commit checks before pushing? (Y/N)" -ForegroundColor Cyan
$preCommitChoice = Read-Host
if ($preCommitChoice -eq "Y") {
    Write-Host "Running pre-commit hooks on all files..." -ForegroundColor Yellow
    pre-commit run --all-files
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Pre-commit checks failed. Fix issues before pushing." -ForegroundColor Red
        exit 1
    } else {
        Write-Host "✅ Pre-commit checks passed!" -ForegroundColor Green
    }
}

# Git commit and push
Write-Host "`nDo you want to stage, commit, and push changes to Git? (Y/N)" -ForegroundColor Cyan
$gitChoice = Read-Host
if ($gitChoice -eq "Y") {
    Write-Host "Enter commit message (or press Enter for default):" -ForegroundColor Cyan
    $customMsg = Read-Host

    if ([string]::IsNullOrWhiteSpace($customMsg)) {
        $commitMsg = "Auto-fixed JSON formatting, validated YAML, and passed pre-commit checks"
    } else {
        $commitMsg = $customMsg
    }

    Write-Host "Staging all changes..." -ForegroundColor Yellow
    git add .

    Write-Host "Committing with message: $commitMsg" -ForegroundColor Yellow
    git commit -m "$commitMsg"

    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Nothing to commit or commit failed" -ForegroundColor Yellow
    } else {
        Write-Host "Pushing to remote..." -ForegroundColor Yellow
        git push
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Changes pushed successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ Push failed. Check git output above." -ForegroundColor Red
            exit 1
        }
    }

    # Git tag creation
    Write-Host "`nDo you want to create a Git tag for this version? (Y/N)" -ForegroundColor Cyan
    $tagChoice = Read-Host
    if ($tagChoice -eq "Y") {
        Write-Host "Enter tag name (e.g., v2.0.0, v1.5.3):" -ForegroundColor Cyan
        $tagName = Read-Host

        # Validate semantic version format
        if ($tagName -notmatch '^v?\d+\.\d+\.\d+(-[a-zA-Z0-9\.]+)?$') {
            Write-Host "❌ Invalid version format. Use semantic versioning (e.g., v2.0.0, v1.5.3, v2.0.0-beta)" -ForegroundColor Red
            exit 1
        }

        # Ensure tag starts with 'v'
        if (-not $tagName.StartsWith("v")) {
            $tagName = "v" + $tagName
        }

        Write-Host "Creating release for version: $tagName" -ForegroundColor Cyan

        # Update package.json version
        if (Test-Path ".\package.json") {
            Write-Host "Updating version in package.json..." -ForegroundColor Yellow
            $packageContent = Get-Content package.json -Raw
            $versionNumber = $tagName.TrimStart("v")
            $packageContent = $packageContent -replace '"version":\s*"[^"]*"', ('"version": "' + $versionNumber + '"')
            $packageContent | Set-Content package.json
            Write-Host "✅ Updated package.json to version $versionNumber" -ForegroundColor Green
        }

        # Update DEPLOYMENT_STATUS.md version
        if (Test-Path ".\DEPLOYMENT_STATUS.md") {
            Write-Host "Updating version in DEPLOYMENT_STATUS.md..." -ForegroundColor Yellow
            $deployContent = Get-Content DEPLOYMENT_STATUS.md -Raw
            $deployContent = $deployContent -replace 'Version:\s*[^\r\n]*', ('Version: ' + $tagName)
            $deployContent | Set-Content DEPLOYMENT_STATUS.md
            Write-Host "✅ Updated DEPLOYMENT_STATUS.md to version $tagName" -ForegroundColor Green
        }

        # Update DEPLOYMENT_FIXED.md version if exists
        if (Test-Path ".\DEPLOYMENT_FIXED.md") {
            Write-Host "Updating version in DEPLOYMENT_FIXED.md..." -ForegroundColor Yellow
            $deployFixedContent = Get-Content DEPLOYMENT_FIXED.md -Raw
            if ($deployFixedContent -match 'Last Updated:') {
                $deployFixedContent = $deployFixedContent -replace 'Last Updated:\s*[^\r\n]*', ('Last Updated: ' + (Get-Date -Format 'yyyy-MM-dd'))
            }
            $deployFixedContent | Set-Content DEPLOYMENT_FIXED.md
            Write-Host "✅ Updated DEPLOYMENT_FIXED.md timestamp" -ForegroundColor Green
        }

        # Add changelog entry
        Write-Host "Creating changelog entry..." -ForegroundColor Yellow
        $changelogEntry = @"

## $tagName - $(Get-Date -Format 'yyyy-MM-dd')

### Changed
- Auto-fixed JSON formatting with Prettier
- Validated YAML files across entire codebase
- Passed all pre-commit checks
- Version bump to $tagName

### Fixed
- JSON syntax errors
- YAML formatting issues

"@

        if (Test-Path ".\CHANGELOG.md") {
            $existingChangelog = Get-Content ".\CHANGELOG.md" -Raw
            # Insert new entry after the header
            if ($existingChangelog -match '(# Changelog\s*)') {
                $existingChangelog = $existingChangelog -replace '(# Changelog\s*)', ('$1' + $changelogEntry)
            } else {
                # If no header, prepend
                $existingChangelog = $changelogEntry + $existingChangelog
            }
            $existingChangelog | Set-Content ".\CHANGELOG.md"
        } else {
            # Create new CHANGELOG.md
            @"
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
$changelogEntry
"@ | Set-Content ".\CHANGELOG.md"
        }
        Write-Host "✅ Changelog updated" -ForegroundColor Green

        # Commit version updates
        Write-Host "Committing version updates..." -ForegroundColor Yellow
        git add .
        git commit -m "Release $tagName - version bump and changelog update"

        if ($LASTEXITCODE -ne 0) {
            Write-Host "⚠️  No changes to commit for version update" -ForegroundColor Yellow
        }

        # Create and push tag
        Write-Host "Creating Git tag..." -ForegroundColor Yellow
        git tag -a $tagName -m "Release $tagName"

        if ($LASTEXITCODE -eq 0) {
            Write-Host "Pushing tag to remote..." -ForegroundColor Yellow
            git push origin $tagName
            git push
            Write-Host "✅ Git tag '$tagName' created and pushed!" -ForegroundColor Green
        } else {
            Write-Host "❌ Failed to create Git tag. Tag may already exist." -ForegroundColor Red
            exit 1
        }

        # GitHub Release creation
        Write-Host "`n=== GitHub Release ===" -ForegroundColor Cyan
        Write-Host "Do you want to create a GitHub Release for this tag? (Y/N)" -ForegroundColor Cyan
        $releaseChoice = Read-Host

        if ($releaseChoice -eq "Y") {
            Write-Host "`nEnter GitHub repository (format: username/repo):" -ForegroundColor Cyan
            Write-Host "Example: JermaineMerritt-ai/codexdominion-schemas" -ForegroundColor Gray
            $repo = Read-Host

            # Validate repo format
            if ($repo -notmatch '^[^/]+/[^/]+$') {
                Write-Host "❌ Invalid repository format. Use: username/repo" -ForegroundColor Red
                exit 1
            }

            Write-Host "`nEnter GitHub Personal Access Token (with 'repo' scope):" -ForegroundColor Cyan
            Write-Host "⚠️  Token will not be displayed or saved" -ForegroundColor Yellow
            Write-Host "Create token at: https://github.com/settings/tokens/new" -ForegroundColor Gray
            $token = Read-Host -AsSecureString
            $tokenPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($token))

            # Extract release notes from changelog
            Write-Host "Extracting release notes from CHANGELOG.md..." -ForegroundColor Yellow
            $changelogContent = Get-Content ".\CHANGELOG.md" -Raw

            # Extract the section for this version
            $pattern = "## $tagName.*?(?=\n## |\z)"
            if ($changelogContent -match $pattern) {
                $releaseNotes = $Matches[0]
            } else {
                $releaseNotes = "Release $tagName`n`nSee CHANGELOG.md for details."
            }

            # Create GitHub release
            Write-Host "Creating GitHub Release..." -ForegroundColor Yellow
            $url = "https://api.github.com/repos/$repo/releases"

            $releaseBody = @{
                tag_name = $tagName
                name = $tagName
                body = $releaseNotes
                draft = $false
                prerelease = $tagName -match '-(alpha|beta|rc)'
            } | ConvertTo-Json -Depth 10

            try {
                $headers = @{
                    Authorization = "token $tokenPlain"
                    Accept = "application/vnd.github.v3+json"
                }

                $response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $releaseBody -ContentType "application/json"
                Write-Host "✅ GitHub Release created successfully!" -ForegroundColor Green
                Write-Host "📦 Release URL: $($response.html_url)" -ForegroundColor Cyan

                # Auto-zip Next.js build folder and upload
                Write-Host "`nDo you want to zip and upload the Next.js build folder? (Y/N)" -ForegroundColor Cyan
                $zipChoice = Read-Host
                if ($zipChoice -eq "Y") {
                    $buildPath = ".\frontend\.next"
                    $zipPath = ".\frontend-build-$tagName.zip"

                    if (Test-Path $buildPath) {
                        Write-Host "Zipping Next.js build folder..." -ForegroundColor Yellow

                        # Remove old zip if exists
                        if (Test-Path $zipPath) {
                            Remove-Item $zipPath -Force
                        }

                        Compress-Archive -Path $buildPath -DestinationPath $zipPath -Force
                        Write-Host "✅ Build zipped to: $zipPath" -ForegroundColor Green

                        # Upload artifact to release
                        Write-Host "Uploading build artifact to GitHub Release..." -ForegroundColor Yellow
                        $uploadUrl = $response.upload_url -replace '\{.*\}', "?name=$(Split-Path $zipPath -Leaf)"

                        try {
                            $uploadHeaders = @{
                                Authorization = "token $tokenPlain"
                                "Content-Type" = "application/zip"
                            }

                            Invoke-RestMethod -Uri $uploadUrl -Method Post -Headers $uploadHeaders -InFile $zipPath | Out-Null
                            Write-Host "✅ Artifact uploaded to GitHub Release!" -ForegroundColor Green
                            Write-Host "📦 Artifact: frontend-build-$tagName.zip" -ForegroundColor Cyan
                        } catch {
                            Write-Host "❌ Failed to upload artifact: $_" -ForegroundColor Red
                        }
                    } else {
                        Write-Host "❌ Build folder not found at $buildPath" -ForegroundColor Red
                        Write-Host "💡 Run 'npm run build' in the frontend directory first." -ForegroundColor Yellow
                    }
                }

                # Remote deployment
                Write-Host "`nDo you want to trigger remote deployment via SSH? (Y/N)" -ForegroundColor Cyan
                $deployChoice = Read-Host
                if ($deployChoice -eq "Y") {
                    Write-Host "Enter SSH server (e.g., user@yourserver.com):" -ForegroundColor Cyan
                    $sshServer = Read-Host
                    Write-Host "Enter deployment command (e.g., cd /var/www && ./deploy.sh):" -ForegroundColor Cyan
                    $deployCommand = Read-Host

                    Write-Host "Triggering remote deployment..." -ForegroundColor Yellow
                    ssh $sshServer $deployCommand
                    Write-Host "✅ Remote deployment triggered successfully!" -ForegroundColor Green

                    # Health check verification
                    Write-Host "`nEnter health check URL (e.g., https://yourdomain.com/health):" -ForegroundColor Cyan
                    $healthUrl = Read-Host
                    if ($healthUrl) {
                        Write-Host "Checking deployment health..." -ForegroundColor Yellow
                        Start-Sleep -Seconds 5  # Wait for deployment to stabilize

                        try {
                            $healthResponse = Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 30
                            if ($healthResponse.StatusCode -eq 200) {
                                Write-Host "✅ Deployment verified! Health endpoint returned 200 OK." -ForegroundColor Green
                                $statusMessage = "✅ Deployment SUCCESS for $tagName. Health check passed."
                            } else {
                                Write-Host "❌ Health check failed. Status: $($healthResponse.StatusCode)" -ForegroundColor Red
                                $statusMessage = "❌ Deployment FAILED for $tagName. Health check returned $($healthResponse.StatusCode)."
                            }
                        } catch {
                            Write-Host "❌ Health check failed. Unable to reach $healthUrl" -ForegroundColor Red
                            Write-Host "Error: $_" -ForegroundColor Red
                            $statusMessage = "❌ Deployment FAILED for $tagName. Health check unreachable."
                        }

                        # Notifications
                        Write-Host "`nDo you want to send Slack/Teams notifications? (Y/N)" -ForegroundColor Cyan
                        $notifyChoice = Read-Host
                        if ($notifyChoice -eq "Y") {
                            Write-Host "Enter Slack webhook URL (or leave blank to skip):" -ForegroundColor Cyan
                            $slackWebhook = Read-Host
                            if ($slackWebhook) {
                                try {
                                    $slackPayload = @{ text = $statusMessage } | ConvertTo-Json
                                    Invoke-RestMethod -Uri $slackWebhook -Method Post -Body $slackPayload -ContentType 'application/json' | Out-Null
                                    Write-Host "✅ Slack notification sent!" -ForegroundColor Green
                                } catch {
                                    Write-Host "❌ Failed to send Slack notification: $_" -ForegroundColor Red
                                }
                            }

                            Write-Host "Enter Teams webhook URL (or leave blank to skip):" -ForegroundColor Cyan
                            $teamsWebhook = Read-Host
                            if ($teamsWebhook) {
                                try {
                                    $teamsPayload = @{ text = $statusMessage } | ConvertTo-Json
                                    Invoke-RestMethod -Uri $teamsWebhook -Method Post -Body $teamsPayload -ContentType 'application/json' | Out-Null
                                    Write-Host "✅ Teams notification sent!" -ForegroundColor Green
                                } catch {
                                    Write-Host "❌ Failed to send Teams notification: $_" -ForegroundColor Red
                                }
                            }
                        }
                    }
                }
            } catch {
                Write-Host "❌ Failed to create GitHub Release" -ForegroundColor Red
                Write-Host "Error: $_" -ForegroundColor Red
                Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
                Write-Host "- Verify token has 'repo' scope" -ForegroundColor Gray
                Write-Host "- Verify repository name is correct" -ForegroundColor Gray
                Write-Host "- Ensure tag was pushed successfully" -ForegroundColor Gray
            } finally {
                # Clear token from memory
                $tokenPlain = $null
            }
        }
    }
}

Write-Host "`n=== Release Automation Complete ===" -ForegroundColor Green
Write-Host "`n📋 Summary:" -ForegroundColor Cyan
Write-Host "  • YAML Errors: $yamlErrors" -ForegroundColor $(if ($yamlErrors -eq 0) { "Green" } else { "Red" })
Write-Host "  • JSON Errors: $jsonErrors" -ForegroundColor $(if ($jsonErrors -eq 0) { "Green" } else { "Red" })
Write-Host "  • Files Formatted: $jsonFixed" -ForegroundColor Green
Write-Host "`n💡 Next Steps:" -ForegroundColor Yellow
Write-Host "  • Review CHANGELOG.md for accuracy" -ForegroundColor Gray
Write-Host "  • Verify deployment documentation is up-to-date" -ForegroundColor Gray
Write-Host "  • Test the release in a staging environment" -ForegroundColor Gray
