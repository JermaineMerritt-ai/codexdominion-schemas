# Codex Dawn Dispatch - PowerShell Version
# Simple and reliable daily sovereignty ritual

param(
    [string]$Action = "",
    [string]$CustomProclamation = ""
)

Write-Host "🌅 Codex Dawn Dispatch System" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Yellow

# Change to project directory
$projectRoot = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion"
Set-Location $projectRoot

Write-Host "📁 Working Directory: $projectRoot" -ForegroundColor Green

# Check Python availability
try {
    $pythonCheck = python --version 2>$null
    if ($pythonCheck) {
        Write-Host "🐍 Python: Available" -ForegroundColor Green
    } else {
        Write-Host "❌ Python not found" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Python not available" -ForegroundColor Red
    exit 1
}

# Execute based on action
if ($Action) {
    switch ($Action.ToLower()) {
        "dispatch" {
            Write-Host "🌅 Executing Dawn Dispatch..." -ForegroundColor Cyan
            if ($CustomProclamation) {
                python dawn_dispatch_simple.py dispatch $CustomProclamation
            } else {
                python dawn_dispatch_simple.py dispatch
            }
        }
        "status" {
            Write-Host "📊 Checking Dawn Status..." -ForegroundColor Cyan
            python dawn_dispatch_simple.py status
        }
        "history" {
            Write-Host "📜 Dawn History (from ledger)..." -ForegroundColor Cyan
            if (Test-Path "codex_ledger.json") {
                $ledger = Get-Content "codex_ledger.json" | ConvertFrom-Json
                if ($ledger.dawn_dispatches -and $ledger.dawn_dispatches.Count -gt 0) {
                    $recent = $ledger.dawn_dispatches | Select-Object -Last 5
                    foreach ($dispatch in $recent) {
                        Write-Host "📅 $($dispatch.date) - $($dispatch.proclamation)" -ForegroundColor White
                    }
                } else {
                    Write-Host "📭 No dawn dispatches found" -ForegroundColor Yellow
                }
            } else {
                Write-Host "❌ Ledger not found" -ForegroundColor Red
            }
        }
        "validate" {
            Write-Host "🔍 Validating Ledger..." -ForegroundColor Cyan
            if (Test-Path "codex_ledger.json") {
                try {
                    $ledger = Get-Content "codex_ledger.json" | ConvertFrom-Json
                    $cycles = if ($ledger.cycles) { $ledger.cycles.Count } else { 0 }
                    $dawns = if ($ledger.dawn_dispatches) { $ledger.dawn_dispatches.Count } else { 0 }
                    Write-Host "✅ Ledger valid - Cycles: $cycles, Dawn Dispatches: $dawns" -ForegroundColor Green
                } catch {
                    Write-Host "❌ Ledger validation failed" -ForegroundColor Red
                }
            } else {
                Write-Host "❌ Ledger file not found" -ForegroundColor Red
            }
        }
        default {
            Write-Host "❌ Unknown action: $Action" -ForegroundColor Red
            Write-Host "Available: dispatch, status, history, validate" -ForegroundColor Yellow
        }
    }
} else {
    # Interactive mode
    Write-Host "`nSelect an option:" -ForegroundColor Cyan
    Write-Host "1. Execute Dawn Dispatch" -ForegroundColor White
    Write-Host "2. Check Status" -ForegroundColor White
    Write-Host "3. Show History" -ForegroundColor White
    Write-Host "4. Validate Ledger" -ForegroundColor White
    Write-Host "5. Exit" -ForegroundColor White
    
    $choice = Read-Host "`nEnter choice (1-5)"
    
    switch ($choice) {
        "1" { 
            Write-Host "🌅 Executing Dawn Dispatch..." -ForegroundColor Cyan
            python dawn_dispatch_simple.py dispatch
        }
        "2" { 
            Write-Host "📊 Checking Status..." -ForegroundColor Cyan
            python dawn_dispatch_simple.py status 
        }
        "3" { 
            Write-Host "📜 Loading History..." -ForegroundColor Cyan
            & $PSScriptRoot\dawn-dispatch-simple.ps1 "history"
        }
        "4" { 
            Write-Host "🔍 Validating..." -ForegroundColor Cyan
            & $PSScriptRoot\dawn-dispatch-simple.ps1 "validate"
        }
        "5" { 
            Write-Host "🌅 Session ended. Flame endures eternal." -ForegroundColor Cyan
        }
        default { 
            Write-Host "❌ Invalid choice" -ForegroundColor Red
        }
    }
}

Write-Host "`n🔥 Dawn Dispatch completed." -ForegroundColor Green