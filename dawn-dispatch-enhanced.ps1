# Codex Dawn Dispatch - PowerShell Enhanced Version
# Daily sovereignty ritual with enhanced features

Write-Host "🌅 Codex Dawn Dispatch System" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Yellow

# Change to project directory
$projectRoot = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion"
Set-Location $projectRoot

Write-Host "📁 Working Directory: $projectRoot" -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion) {
        Write-Host "🐍 Python: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ Python not found" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Python not available" -ForegroundColor Red
    exit 1
}

# Function to run dawn dispatch with error handling
function Invoke-DawnDispatch {
    param(
        [string]$CustomProclamation = $null
    )

    try {
        Write-Host "🌅 Initiating Dawn Dispatch..." -ForegroundColor Cyan

        # Check current status first
        Write-Host "📊 Checking current status..." -ForegroundColor Yellow
        python dawn_dispatch_simple.py status

        Write-Host "`n🔥 Executing dawn ritual..." -ForegroundColor Yellow

        if ($CustomProclamation) {
            python dawn_dispatch_simple.py dispatch $CustomProclamation
        } else {
            python dawn_dispatch_simple.py dispatch
        }

        Write-Host "`n✅ Dawn Dispatch completed successfully!" -ForegroundColor Green

        # Show updated status
        Write-Host "`n📈 Updated status:" -ForegroundColor Cyan
        python dawn_dispatch_simple.py status

        return $true
    }
    catch {
        Write-Host "❌ Dawn Dispatch failed: $_" -ForegroundColor Red
        return $false
    }
}

# Function to show dawn history from ledger
function Show-DawnHistory {
    try {
        Write-Host "📜 Dawn Dispatch History" -ForegroundColor Cyan
        Write-Host "========================" -ForegroundColor Yellow

        if (Test-Path "codex_ledger.json") {
            $ledger = Get-Content "codex_ledger.json" | ConvertFrom-Json

            if ($ledger.dawn_dispatches) {
                $recent = $ledger.dawn_dispatches | Select-Object -Last 5

                foreach ($dispatch in $recent) {
                    Write-Host "📅 $($dispatch.date)" -ForegroundColor Green
                    Write-Host "   🕐 $($dispatch.timestamp)" -ForegroundColor Gray
                    Write-Host "   📜 $($dispatch.proclamation)" -ForegroundColor White
                    Write-Host "   🔥 Cycle ID: $($dispatch.cycle_id)" -ForegroundColor Yellow
                    Write-Host ""
                }
            } else {
                Write-Host "📭 No dawn dispatches found in ledger" -ForegroundColor Yellow
            }
        } else {
            Write-Host "❌ Ledger file not found" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "❌ Error reading dawn history: $_" -ForegroundColor Red
    }
}

# Function to validate ledger integrity
function Test-LedgerIntegrity {
    try {
        Write-Host "🔍 Validating ledger integrity..." -ForegroundColor Cyan

        if (Test-Path "codex_ledger.json") {
            $ledger = Get-Content "codex_ledger.json" | ConvertFrom-Json

            $cycleCount = $ledger.cycles.Count
            $proclamationCount = $ledger.proclamations.Count
            $dawnCount = if ($ledger.dawn_dispatches) { $ledger.dawn_dispatches.Count } else { 0 }

            Write-Host "✅ Ledger structure valid" -ForegroundColor Green
            Write-Host "📊 Cycles: $cycleCount" -ForegroundColor White
            Write-Host "📜 Proclamations: $proclamationCount" -ForegroundColor White
            Write-Host "🌅 Dawn Dispatches: $dawnCount" -ForegroundColor White

            if ($ledger.meta) {
                Write-Host "🏷️  Version: $($ledger.meta.version)" -ForegroundColor Gray
                Write-Host "👑 Custodian: $($ledger.meta.custodian_authority)" -ForegroundColor Gray
                Write-Host "🔥 Last Updated: $($ledger.meta.last_updated)" -ForegroundColor Gray
            }

            return $true
        } else {
            Write-Host "❌ Ledger file not found" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Ledger validation failed: $_" -ForegroundColor Red
        return $false
    }
}

# Main execution logic
Write-Host "`n🎯 Dawn Dispatch Options:" -ForegroundColor Cyan
Write-Host "1. Execute Dawn Dispatch" -ForegroundColor White
Write-Host "2. Execute with Custom Proclamation" -ForegroundColor White
Write-Host "3. Show Dawn History" -ForegroundColor White
Write-Host "4. Validate Ledger" -ForegroundColor White
Write-Host "5. Exit" -ForegroundColor White

# Check if arguments were provided
$Action = if ($args.Count -gt 0) { $args[0] } else { "" }
$Proclamation = if ($args.Count -gt 1) { $args[1] } else { "" }

if ($Action) {
    # Command line execution
    switch ($Action.ToLower()) {
        "dispatch" {
            Invoke-DawnDispatch -CustomProclamation $Proclamation
        }
        "status" {
            python dawn_dispatch_simple.py status
        }
        "history" {
            Show-DawnHistory
        }
        "validate" {
            Test-LedgerIntegrity
        }
        default {
            Write-Host "❌ Unknown action: $Action" -ForegroundColor Red
            Write-Host "Available actions: dispatch, status, history, validate" -ForegroundColor Yellow
        }
    }
} else {
    # Interactive mode
    do {
        Write-Host "`nSelect option (1-5): " -NoNewline -ForegroundColor Yellow
        $choice = Read-Host

        switch ($choice) {
            "1" {
                Invoke-DawnDispatch
            }
            "2" {
                Write-Host "Enter custom proclamation: " -NoNewline -ForegroundColor Yellow
                $customProc = Read-Host
                Invoke-DawnDispatch -CustomProclamation $customProc
            }
            "3" {
                Show-DawnHistory
            }
            "4" {
                Test-LedgerIntegrity
            }
            "5" {
                Write-Host "🌅 Dawn Dispatch session ended. May the flame endure eternal." -ForegroundColor Cyan
                break
            }
            default {
                Write-Host "❌ Invalid option. Please select 1-5." -ForegroundColor Red
            }
        }
    } while ($choice -ne "5")
}

Write-Host "`n🔥 The eternal flame protects all operations." -ForegroundColor Green
