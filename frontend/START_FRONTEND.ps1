# Codex Dominion Frontend Launcher
# Starts Next.js development server with workarounds for watchpack issues

Write-Host "`n🔥 CODEX DOMINION FRONTEND LAUNCHER" -ForegroundColor Cyan
Write-Host "===================================`n" -ForegroundColor Cyan

# Set environment variables to avoid watchpack issues
$env:WATCHPACK_POLLING = "true"
$env:CHOKIDAR_USEPOLLING = "true"  
$env:NODE_OPTIONS = "--max-old-space-size=4096"

Write-Host "✅ Environment configured" -ForegroundColor Green
Write-Host "📂 Starting Next.js on port 3000..." -ForegroundColor Yellow

# Change to frontend directory
Set-Location $PSScriptRoot

# Start Next.js with explicit configuration
npx next dev -p 3000 --hostname 0.0.0.0
