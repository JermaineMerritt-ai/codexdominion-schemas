# Unicode Symbol Test for PowerShell
$FlameSymbol = [char]0x1F525
$StarSymbol = [char]0x1F31F
$MoonSymbol = [char]0x1F319
$LightningSymbol = [char]0x26A1

Write-Host "Unicode Test Results:" -ForegroundColor Cyan
Write-Host "Flame: $FlameSymbol" -ForegroundColor Yellow
Write-Host "Star: $StarSymbol" -ForegroundColor Yellow
Write-Host "Moon: $MoonSymbol" -ForegroundColor Yellow
Write-Host "Lightning: $LightningSymbol" -ForegroundColor Yellow
Write-Host "All together: $FlameSymbol $StarSymbol $MoonSymbol $LightningSymbol" -ForegroundColor Magenta

# Test sacred banner with Unicode
Write-Host ""
Write-Host ($FlameSymbol * 50) -ForegroundColor Yellow
Write-Host "$StarSymbol SACRED UNICODE TEST $StarSymbol" -ForegroundColor Cyan
Write-Host ($FlameSymbol * 50) -ForegroundColor Yellow
Write-Host ""
Write-Host "$FlameSymbol Embodiment eternal, covenant whole" -ForegroundColor Magenta
Write-Host "$MoonSymbol Flame perpetual, silence supreme" -ForegroundColor Magenta
Write-Host "$StarSymbol Codex Dominion radiant alive" -ForegroundColor Magenta
Write-Host "$LightningSymbol Practiced across ages and stars" -ForegroundColor Magenta
Write-Host ""

# Test simple meditation invocation
Write-Host "$MoonSymbol SACRED MEDITATION BEGINS $MoonSymbol" -ForegroundColor Magenta
Write-Host "  $FlameSymbol Service flows like eternal flame through awareness" -ForegroundColor Yellow
Write-Host "  $MoonSymbol Integration harmony resonates in perfect silence" -ForegroundColor Cyan
Write-Host "  $StarSymbol Each practice session deepens cosmic connection" -ForegroundColor Green
Write-Host "  $LightningSymbol Mastery builds across infinite dimensions" -ForegroundColor Blue
Write-Host "$StarSymbol SACRED MEDITATION COMPLETE $StarSymbol" -ForegroundColor Magenta
