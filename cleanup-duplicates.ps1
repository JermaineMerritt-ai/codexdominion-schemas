# ============================================
# Codex Dominion - Duplicate File Cleanup
# ============================================
# Removes duplicate .js files that conflict with .tsx versions

Write-Host "=== CODEX DOMINION DUPLICATE CLEANUP ===" -ForegroundColor Cyan
Write-Host "Flame Eternal - Removing Duplicate Files`n" -ForegroundColor Yellow

$frontendPages = "frontend/pages"

# List of files to remove (keeping .tsx, removing .js)
$duplicatesToRemove = @(
    "alpha-omega-concord.js",
    "balance-renewal.js",
    "blessed-serenity.js",
    "blessed-storefronts.js",
    "capsules-enhanced.js",
    "capsules-simple.js",
    "capsules.js",
    "codex-constellation.js",
    "codex-radiant-peace.js",
    "codex-source-charter.js",
    "compendium-complete.js",
    "compendium-luminous.js",
    "cosmic-sovereignty.js",
    "covenant-eternal.js",
    "custodial-sovereign.js",
    "custodian-eternal.js",
    "dashboard-selector.js",
    "day-zenith.js",
    "dominion-radiant.js",
    "eternal-compendium.js",
    "eternal-light-peace.js",
    "eternal-proclamation.js",
    "eternal-silence.js",
    "eternal-stillness.js",
    "eternal-transcendence.js",
    "festival.js",
    "final-continuum.js",
    "flame-eternal.js",
    "global-induction.js",
    "harvest-serenity.js",
    "heir-pledge.js",
    "index.js",
    "infinite-serenity.js",
    "living-covenant.js",
    "millennial-sovereignty.js",
    "night-endurance.js",
    "omega-charter.js",
    "omega-crown.js",
    "perpetual-sovereignty.js",
    "radiant-serenity.js",
    "seven-crowns-transmission.js",
    "signals-enhanced.js",
    "signals.js",
    "sovereign-decree.js",
    "sovereign-inheritance.js",
    "sovereign-succession.js",
    "supreme-ultimate.js",
    "test-capsules.js",
    "ultimate-dominion.js",
    "unity-continuum.js"
)

$duplicateSubdirs = @{
    "capsule" = @("[slug].js", "[slug].jsx")
    "dashboard" = @("custodian.js", "customer.js", "heir.js")
    "api" = @("capsules.js", "ceremony.js", "festival.js")
    "api/artifacts/[slug]" = @("latest.js")
}

$removedCount = 0
$notFoundCount = 0

# Remove root-level duplicates
Write-Host "[1] Removing root-level duplicate .js files..." -ForegroundColor Cyan
foreach ($file in $duplicatesToRemove) {
    $filePath = Join-Path $frontendPages $file
    if (Test-Path $filePath) {
        try {
            Remove-Item $filePath -Force
            Write-Host "  ✅ Removed: $file" -ForegroundColor Green
            $removedCount++
        } catch {
            Write-Host "  ❌ Failed to remove: $file - $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "  ⚠️  Not found: $file" -ForegroundColor Yellow
        $notFoundCount++
    }
}

# Remove subdirectory duplicates
Write-Host "`n[2] Removing subdirectory duplicate files..." -ForegroundColor Cyan
foreach ($subdir in $duplicateSubdirs.Keys) {
    $subdirPath = Join-Path $frontendPages $subdir
    if (Test-Path $subdirPath) {
        foreach ($file in $duplicateSubdirs[$subdir]) {
            $filePath = Join-Path $subdirPath $file
            if (Test-Path $filePath) {
                try {
                    Remove-Item $filePath -Force
                    Write-Host "  ✅ Removed: $subdir/$file" -ForegroundColor Green
                    $removedCount++
                } catch {
                    Write-Host "  ❌ Failed to remove: $subdir/$file - $($_.Exception.Message)" -ForegroundColor Red
                }
            } else {
                Write-Host "  ⚠️  Not found: $subdir/$file" -ForegroundColor Yellow
                $notFoundCount++
            }
        }
    }
}

Write-Host "`n=== CLEANUP COMPLETE ===" -ForegroundColor Green
Write-Host "Files removed: $removedCount" -ForegroundColor Green
Write-Host "Files not found: $notFoundCount" -ForegroundColor Yellow
Write-Host "`nRestart Next.js dev server to see changes take effect." -ForegroundColor Cyan
