# GitHub + Vercel Deployment Setup (Windows PowerShell)
# ======================================================

Write-Host "=" -NoNewline -ForegroundColor DarkYellow
Write-Host ("=" * 69) -ForegroundColor DarkYellow
Write-Host "  GITHUB + VERCEL CREDENTIALS SETUP" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor DarkYellow
Write-Host ("=" * 69) -ForegroundColor DarkYellow
Write-Host ""

# Step 1: GitHub Token
Write-Host "STEP 1: GitHub Personal Access Token" -ForegroundColor Cyan
Write-Host "--------------------------------------" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  1. Open: " -NoNewline
Write-Host "https://github.com/settings/tokens/new" -ForegroundColor Blue
Write-Host "  2. Token name: " -NoNewline -ForegroundColor Gray
Write-Host "CodexDominion Deployments" -ForegroundColor White
Write-Host "  3. Expiration: " -NoNewline -ForegroundColor Gray
Write-Host "No expiration (or 1 year)" -ForegroundColor White
Write-Host "  4. Select scopes:" -ForegroundColor Gray
Write-Host "     ✅ repo (Full control of repositories)" -ForegroundColor Green
Write-Host "     ✅ workflow (Update GitHub Actions)" -ForegroundColor Green
Write-Host "  5. Click 'Generate token' and copy it" -ForegroundColor Gray
Write-Host ""

$githubToken = Read-Host "Paste your GitHub token here (or press Enter to skip)"

if ($githubToken) {
    [Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $githubToken, "User")
    Write-Host "✅ GitHub token saved to environment variables" -ForegroundColor Green
} else {
    Write-Host "⏭️  Skipped GitHub token setup" -ForegroundColor Yellow
}
Write-Host ""

# Step 2: Vercel Token
Write-Host "STEP 2: Vercel API Token" -ForegroundColor Cyan
Write-Host "-------------------------" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  1. Open: " -NoNewline
Write-Host "https://vercel.com/account/tokens" -ForegroundColor Blue
Write-Host "  2. Click 'Create Token'" -ForegroundColor Gray
Write-Host "  3. Token name: " -NoNewline -ForegroundColor Gray
Write-Host "CodexDominion Deployments" -ForegroundColor White
Write-Host "  4. Scope: " -NoNewline -ForegroundColor Gray
Write-Host "Full Account" -ForegroundColor White
Write-Host "  5. Click 'Create' and copy the token" -ForegroundColor Gray
Write-Host ""

$vercelToken = Read-Host "Paste your Vercel token here (or press Enter to skip)"

if ($vercelToken) {
    [Environment]::SetEnvironmentVariable("VERCEL_TOKEN", $vercelToken, "User")
    Write-Host "✅ Vercel token saved to environment variables" -ForegroundColor Green
} else {
    Write-Host "⏭️  Skipped Vercel token setup" -ForegroundColor Yellow
}
Write-Host ""

# Step 3: Vercel Team ID (Optional)
Write-Host "STEP 3: Vercel Team ID (Optional)" -ForegroundColor Cyan
Write-Host "----------------------------------" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  If deploying to a Vercel team:" -ForegroundColor Gray
Write-Host "  1. Go to your team settings" -ForegroundColor Gray
Write-Host "  2. Copy the Team ID (looks like: team_xxx...)" -ForegroundColor Gray
Write-Host ""

$vercelTeamId = Read-Host "Paste your Vercel Team ID (or press Enter to skip)"

if ($vercelTeamId) {
    [Environment]::SetEnvironmentVariable("VERCEL_TEAM_ID", $vercelTeamId, "User")
    Write-Host "✅ Vercel Team ID saved" -ForegroundColor Green
} else {
    Write-Host "⏭️  Skipped Team ID (will deploy to personal account)" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "=" -NoNewline -ForegroundColor DarkYellow
Write-Host ("=" * 69) -ForegroundColor DarkYellow
Write-Host "  SETUP COMPLETE" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor DarkYellow
Write-Host ("=" * 69) -ForegroundColor DarkYellow
Write-Host ""

# Test credentials
Write-Host "Testing credentials..." -ForegroundColor Cyan
Write-Host ""

$hasGithub = [Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "User")
$hasVercel = [Environment]::GetEnvironmentVariable("VERCEL_TOKEN", "User")
$hasTeam = [Environment]::GetEnvironmentVariable("VERCEL_TEAM_ID", "User")

if ($hasGithub) {
    Write-Host "✅ GITHUB_TOKEN: Configured" -ForegroundColor Green
} else {
    Write-Host "❌ GITHUB_TOKEN: Not configured" -ForegroundColor Red
}

if ($hasVercel) {
    Write-Host "✅ VERCEL_TOKEN: Configured" -ForegroundColor Green
} else {
    Write-Host "❌ VERCEL_TOKEN: Not configured" -ForegroundColor Red
}

if ($hasTeam) {
    Write-Host "✅ VERCEL_TEAM_ID: Configured (deploying to team)" -ForegroundColor Green
} else {
    Write-Host "ℹ️  VERCEL_TEAM_ID: Not configured (deploying to personal account)" -ForegroundColor Gray
}

Write-Host ""

if ($hasGithub -and $hasVercel) {
    Write-Host "🎉 All required credentials configured!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Close and reopen your terminal to load new environment variables" -ForegroundColor Gray
    Write-Host "  2. Test deployment: " -NoNewline -ForegroundColor Gray
    Write-Host "python test_site_factory.py" -ForegroundColor White
    Write-Host "  3. Deploy real site: " -NoNewline -ForegroundColor Gray
    Write-Host "python website_creation_worker.py" -ForegroundColor White
    Write-Host ""
    Write-Host "🔥 Your deployment pipeline is ready! 👑" -ForegroundColor Yellow
} else {
    Write-Host "⚠️  Some credentials are missing. Run this script again to configure them." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "You can also set them manually in PowerShell:" -ForegroundColor Gray
    Write-Host '  $env:GITHUB_TOKEN = "your_token_here"' -ForegroundColor DarkGray
    Write-Host '  $env:VERCEL_TOKEN = "your_token_here"' -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
