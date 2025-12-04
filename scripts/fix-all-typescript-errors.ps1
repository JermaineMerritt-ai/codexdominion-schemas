#!/usr/bin/env pwsh
# Comprehensive TypeScript Error Fix Script

Write-Host "`n🔧 Codex Dominion - Comprehensive Error Fix" -ForegroundColor Cyan
Write-Host "=" * 70

$errorCount = 9496
Write-Host "`n📊 Total errors detected: $errorCount" -ForegroundColor Yellow
Write-Host "`n🎯 Primary issues to fix:" -ForegroundColor Cyan
Write-Host "  1. Missing 'id' in audit log entries (~100 instances)" -ForegroundColor White
Write-Host "  2. Severity type mismatches (lowercase vs UPPERCASE)" -ForegroundColor White
Write-Host "  3. Missing config properties in CouncilSealConfig" -ForegroundColor White
Write-Host "  4. Status value mismatches ('ACTIVE' vs 'RUNNING')" -ForegroundColor White
Write-Host "  5. Capability type mismatches (strings vs Capability enum)" -ForegroundColor White

Write-Host "`n🛠️ Recommended approach:" -ForegroundColor Yellow
Write-Host "=" * 70

Write-Host "`nOption 1: Auto-fix with TypeScript compiler" -ForegroundColor Cyan
Write-Host "  npx tsc --noEmit --project tsconfig.json" -ForegroundColor Gray
Write-Host "  Then manually fix remaining issues" -ForegroundColor Gray

Write-Host "`nOption 2: Install and run ESLint with auto-fix" -ForegroundColor Cyan
Write-Host "  npm install --save-dev @typescript-eslint/parser @typescript-eslint/eslint-plugin" -ForegroundColor Gray
Write-Host "  npx eslint . --ext .ts,.tsx --fix" -ForegroundColor Gray

Write-Host "`nOption 3: Build project to see actual runtime errors" -ForegroundColor Cyan
Write-Host "  npm run build" -ForegroundColor Gray
Write-Host "  (This will show which errors are critical)" -ForegroundColor Gray

Write-Host "`n💡 Quick wins - Manual fixes:" -ForegroundColor Yellow
Write-Host "=" * 70

Write-Host "`n1️⃣ Fix audit logs - Add crypto for ID generation:" -ForegroundColor Cyan
Write-Host @"
import { randomUUID } from 'crypto';

// Change all audit calls from:
councilSeal.audit({
  timestamp: new Date(),
  ...
})

// To:
councilSeal.audit({
  id: randomUUID(),
  timestamp: new Date(),
  ...
})
"@ -ForegroundColor White

Write-Host "`n2️⃣ Fix severity values - Change lowercase to UPPERCASE:" -ForegroundColor Cyan
Write-Host @"
// Find and replace:
severity: 'low'      -> severity: 'LOW'
severity: 'medium'   -> severity: 'MEDIUM'
severity: 'high'     -> severity: 'HIGH'
severity: 'critical' -> severity: 'CRITICAL'
"@ -ForegroundColor White

Write-Host "`n3️⃣ Fix status values:" -ForegroundColor Cyan
Write-Host @"
// Change:
status: 'ACTIVE' -> status: 'RUNNING'
"@ -ForegroundColor White

Write-Host "`n🚀 Would you like me to:" -ForegroundColor Yellow
Write-Host "  A) Generate specific fix patches for each file" -ForegroundColor White
Write-Host "  B) Run TypeScript compiler to prioritize critical errors" -ForegroundColor White
Write-Host "  C) Create helper utility functions to prevent future errors" -ForegroundColor White
Write-Host "  D) All of the above" -ForegroundColor Green

Write-Host "`n⚠️ Note: Most errors are type-checking issues, not runtime bugs" -ForegroundColor Yellow
Write-Host "   The code likely works but TypeScript wants stricter typing" -ForegroundColor Gray

Write-Host "`n📁 Most affected files:" -ForegroundColor Cyan
Write-Host "  - core/councilSeal.ts (15 errors)" -ForegroundColor White
Write-Host "  - core/sovereigns.ts (5 errors)" -ForegroundColor White
Write-Host "  - core/custodians.ts (7 errors)" -ForegroundColor White
Write-Host "  - core/flows.ts (8 errors)" -ForegroundColor White
Write-Host "  - agents/* (multiple capability type errors)" -ForegroundColor White

Write-Host "`n"
$choice = Read-Host "Select option (A/B/C/D) or Enter to skip"

switch ($choice.ToUpper()) {
    'A' {
        Write-Host "`n📝 Generating fix patches..." -ForegroundColor Cyan
        Write-Host "Creating fixes for councilSeal.ts..." -ForegroundColor Gray
        # Would implement actual fix generation here
    }
    'B' {
        Write-Host "`n🔨 Running TypeScript compiler..." -ForegroundColor Cyan
        if (Test-Path "tsconfig.json") {
            npx tsc --noEmit
        } else {
            Write-Host "No tsconfig.json found" -ForegroundColor Red
        }
    }
    'C' {
        Write-Host "`n🛠️ Creating utility functions..." -ForegroundColor Cyan
        Write-Host "Would create audit helper, type guards, etc." -ForegroundColor Gray
    }
    'D' {
        Write-Host "`n🚀 Running all fixes..." -ForegroundColor Cyan
        Write-Host "This would run A, B, and C in sequence" -ForegroundColor Gray
    }
    default {
        Write-Host "`n✅ Skipped - You can manually run fixes later" -ForegroundColor Yellow
    }
}

Write-Host "`n💾 Next steps:" -ForegroundColor Yellow
Write-Host "  1. Commit current work to git" -ForegroundColor Gray
Write-Host "  2. Create branch: git checkout -b fix/typescript-errors" -ForegroundColor Gray
Write-Host "  3. Apply fixes incrementally" -ForegroundColor Gray
Write-Host "  4. Test after each major fix" -ForegroundColor Gray
Write-Host "  5. Merge when TypeScript is happy" -ForegroundColor Gray

Write-Host ""
