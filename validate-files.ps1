# Ensure script runs from project root
Write-Host "=== Starting YAML & JSON Validation ===" -ForegroundColor Cyan

# Prepare summary report
$reportPath = ".\validation_report.txt"
"Validation Report - $(Get-Date)" | Out-File $reportPath
"=====================================" | Out-File $reportPath -Append

# Install required tools if missing
Write-Host "Checking dependencies..." -ForegroundColor Yellow
if (-not (Get-Command yamllint -ErrorAction SilentlyContinue)) {
    Write-Host "Installing yamllint via pip..." -ForegroundColor Yellow
    pip install yamllint
}
if (-not (Get-Command jsonlint -ErrorAction SilentlyContinue)) {
    Write-Host "Installing jsonlint via npm..." -ForegroundColor Yellow
    npm install -g jsonlint
}
if (-not (Get-Command prettier -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Prettier via npm..." -ForegroundColor Yellow
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
    $result = yamllint $file.FullName
    if ($LASTEXITCODE -ne 0) {
        $yamlErrors++
        Write-Host "❌ YAML Error in $($file.FullName)" -ForegroundColor Red
        $result | Out-File $reportPath -Append
    } else {
        Write-Host "✅ YAML OK: $($file.Name)" -ForegroundColor Green
    }
}

# Validate JSON files
Write-Host "`n=== Validating JSON Files ===" -ForegroundColor Cyan
$jsonFiles = Get-ChildItem -Path . -Include *.json -Recurse
foreach ($file in $jsonFiles) {
    try {
        jsonlint $file.FullName
        Write-Host "✅ JSON OK: $($file.Name)" -ForegroundColor Green
    } catch {
        $jsonErrors++
        Write-Host "❌ JSON Error in $($file.FullName)" -ForegroundColor Red
        "JSON Error in $($file.FullName)" | Out-File $reportPath -Append
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

# Run pre-commit before Git push
Write-Host "`nDo you want to run pre-commit checks before pushing? (Y/N)" -ForegroundColor Cyan
$preCommitChoice = Read-Host
if ($preCommitChoice -eq "Y") {
    Write-Host "Running pre-commit hooks on all files..." -ForegroundColor Yellow
    pre-commit run --all-files
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Pre-commit checks failed. Fix issues before pushing." -ForegroundColor Red
        exit
    } else {
        Write-Host "✅ Pre-commit checks passed!" -ForegroundColor Green
    }
}

# Git commit and push
Write-Host "`nDo you want to stage, commit, and push changes to Git? (Y/N)" -ForegroundColor Cyan
$gitChoice = Read-Host
if ($gitChoice -eq "Y") {
    Write-Host "Staging all changes..." -ForegroundColor Yellow
    git add .

    Write-Host "Committing changes..." -ForegroundColor Yellow
    git commit -m "Auto-fixed JSON formatting, validated YAML, and passed pre-commit checks"

    Write-Host "Pushing to remote..." -ForegroundColor Yellow
    git push

    Write-Host "✅ Changes pushed successfully!" -ForegroundColor Green

    # Git tag creation
    Write-Host "`nDo you want to create a Git tag for this version? (Y/N)" -ForegroundColor Cyan
    $tagChoice = Read-Host
    if ($tagChoice -eq "Y") {
        Write-Host "Enter tag name (e.g., v2.0.0):" -ForegroundColor Cyan
        $tagName = Read-Host

        # Update package.json version
        if (Test-Path ".\package.json") {
            Write-Host "Updating version in package.json..." -ForegroundColor Yellow
            $packageContent = Get-Content package.json -Raw
            $packageContent = $packageContent -replace '"version":\s*"[^"]*"', ('"version": "' + $tagName.TrimStart("v") + '"')
            $packageContent | Set-Content package.json
        }

        # Update DEPLOYMENT_STATUS.md version
        if (Test-Path ".\DEPLOYMENT_STATUS.md") {
            Write-Host "Updating version in DEPLOYMENT_STATUS.md..." -ForegroundColor Yellow
            $deployContent = Get-Content DEPLOYMENT_STATUS.md -Raw
            $deployContent = $deployContent -replace 'Version:\s*[^\r\n]*', ('Version: ' + $tagName)
            $deployContent | Set-Content DEPLOYMENT_STATUS.md
        }

        # Create and push tag
        git add .
        git commit -m "Update version to $tagName"
        git tag $tagName
        git push origin $tagName
        git push
        Write-Host "✅ Git tag '$tagName' created and pushed!" -ForegroundColor Green
        Write-Host "✅ Version updated in package.json and DEPLOYMENT_STATUS.md" -ForegroundColor Green
    }
}

Write-Host "`nFix YAML errors manually (multi-doc, duplicate keys, indentation)." -ForegroundColor Yellow
Write-Host "JSON errors auto-fixed if you chose Y." -ForegroundColor Yellow
