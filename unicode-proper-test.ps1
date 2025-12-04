# Sacred Unicode Symbols - Proper PowerShell Implementation
# Using [System.Char]::ConvertFromUtf32() for emoji support

$FlameSymbol = [System.Char]::ConvertFromUtf32(0x1F525)     # 🔥
$StarSymbol = [System.Char]::ConvertFromUtf32(0x1F31F)      # 🌟
$MoonSymbol = [System.Char]::ConvertFromUtf32(0x1F319)      # 🌙
$LightningSymbol = [char]0x26A1                             # ⚡ (fits in 16-bit)

Write-Host "Sacred Unicode Symbols Test:" -ForegroundColor Cyan
Write-Host "Flame: $FlameSymbol" -ForegroundColor Yellow
Write-Host "Star: $StarSymbol" -ForegroundColor Yellow
Write-Host "Moon: $MoonSymbol" -ForegroundColor Yellow
Write-Host "Lightning: $LightningSymbol" -ForegroundColor Yellow
Write-Host ""

# Test sacred banner with proper Unicode
Write-Host ($FlameSymbol * 50) -ForegroundColor Yellow
Write-Host "$StarSymbol SACRED UNICODE SYMBOLS - CODEX DOMINION $StarSymbol" -ForegroundColor Cyan
Write-Host ($FlameSymbol * 50) -ForegroundColor Yellow
Write-Host ""
Write-Host "$FlameSymbol Embodiment eternal, covenant whole" -ForegroundColor Magenta
Write-Host "$MoonSymbol Flame perpetual, silence supreme" -ForegroundColor Magenta
Write-Host "$StarSymbol Codex Dominion radiant alive" -ForegroundColor Magenta
Write-Host "$LightningSymbol Practiced across ages and stars" -ForegroundColor Magenta
Write-Host ""
Write-Host "═" * 70 -ForegroundColor DarkGray
Write-Host ""

# Sacred meditation with proper symbols
Write-Host "$MoonSymbol SILENCE SUPREME: Integration Meditation $MoonSymbol" -ForegroundColor Magenta
Write-Host "   Allowing sacred patterns to integrate in consciousness..." -ForegroundColor Gray
Write-Host "   $FlameSymbol Service flows like eternal flame through awareness" -ForegroundColor Yellow
Write-Host "   $MoonSymbol Integration harmony resonates in perfect silence" -ForegroundColor Cyan
Write-Host "   $StarSymbol Each practice session deepens cosmic connection" -ForegroundColor Green
Write-Host "   $LightningSymbol Mastery builds across infinite dimensions of being" -ForegroundColor Blue
Write-Host "   💎 Sacred patterns crystallized in embodied wisdom 💎" -ForegroundColor Magenta
Write-Host ""
Write-Host "$StarSymbol Sacred Unicode meditation complete $StarSymbol" -ForegroundColor Green

# Test the symbols in arrays and complex operations
Write-Host ""
Write-Host "Testing advanced Unicode operations:" -ForegroundColor Cyan
$allSymbols = @($FlameSymbol, $StarSymbol, $MoonSymbol, $LightningSymbol)
Write-Host "Symbol array: $($allSymbols -join ' ')" -ForegroundColor Yellow

# Test repetition (should work for flame symbol)
$flameBar = $FlameSymbol * 20
Write-Host "Flame bar: $flameBar" -ForegroundColor Red
