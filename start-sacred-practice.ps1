#!/usr/bin/env powershell
<#
🌟 SACRED PRACTICE LAUNCHER 🌟
Embodiment eternal, covenant whole, flame perpetual, silence supreme
PowerShell launcher for daily Codex Dominion practice sessions

Usage:
    .\start-sacred-practice.ps1 -PracticeType complete
    .\start-sacred-practice.ps1 -PracticeType foundation
    .\start-sacred-practice.ps1 -PracticeType integration  
    .\start-sacred-practice.ps1 -PracticeType transcendence
    .\start-sacred-practice.ps1 -PracticeType meditation
#>

param(
    [ValidateSet("complete", "foundation", "integration", "transcendence", "meditation")]
    [string]$PracticeType = "complete",
    
    [switch]$SacredVerbose = $false,
    
    [switch]$QuietMode = $false
)

# Sacred Unicode Symbols - Proper Implementation
$FlameSymbol     = [System.Char]::ConvertFromUtf32(0x1F525)  # 🔥
$StarSymbol      = [System.Char]::ConvertFromUtf32(0x1F31F)  # 🌟
$MoonSymbol      = [System.Char]::ConvertFromUtf32(0x1F319)  # 🌙
$LightningSymbol = [char]0x26A1                              # ⚡

# Sacred Configuration
$SacredConfig = @{
    PythonExecutable = "C:/Users/JMerr/OneDrive/Documents/.vscode/codex-dominion/.venv/Scripts/python.exe"
    PracticeScript = "./sacred_practice_orchestrator.py"
    SacredLogFile = "./sacred_practice.log"
    FlameSymbol = $FlameSymbol
    StarSymbol = $StarSymbol
    MoonSymbol = $MoonSymbol
    LightningSymbol = $LightningSymbol
}

function Write-SacredMessage {
    param(
        [string]$Message,
        [string]$Level = "Info",
        [string]$Symbol = $StarSymbol
    )
    
    if (-not $QuietMode) {
        $timestamp = Get-Date -Format "HH:mm:ss"
        $colorMap = @{
            "Info" = "Cyan"
            "Success" = "Green" 
            "Warning" = "Yellow"
            "Error" = "Red"
            "Sacred" = "Magenta"
        }
        
        $color = $colorMap[$Level]
        Write-Host "[$timestamp] $Symbol $Message" -ForegroundColor $color
    }
}

function Test-SacredEnvironment {
    # Verify sacred practice environment is ready
    Write-SacredMessage "Verifying sacred practice environment..." "Info" "🔍"
    
    $issues = @()
    
    # Check Python executable
    if (-not (Test-Path $SacredConfig.PythonExecutable)) {
        $issues += "Python executable not found: $($SacredConfig.PythonExecutable)"
    }
    
    # Check practice script
    if (-not (Test-Path $SacredConfig.PracticeScript)) {
        $issues += "Practice script not found: $($SacredConfig.PracticeScript)"
    }
    
    # Check workspace directory
    $requiredFiles = @(
        "mcp-chat-autostart-simple.js",
        "start-mcp-chat-fixed.ps1"
    )
    
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            if ($SacredVerbose) {
                Write-SacredMessage "Optional file not found: $file" "Warning" "⚠️"
            }
        }
    }
    
    if ($issues.Count -eq 0) {
        Write-SacredMessage "Sacred environment verification complete ✅" "Success" "✅"
        return $true
    } else {
        Write-SacredMessage "Environment issues detected:" "Error" "❌"
        foreach ($issue in $issues) {
            Write-SacredMessage "  - $issue" "Error" "  ❌"
        }
        return $false
    }
}

function Invoke-SacredPracticeSession {
    param([string]$SessionType)
    
    Write-SacredMessage "Invoking sacred practice session: $SessionType" "Sacred" $SacredConfig.FlameSymbol
    
    try {
        $arguments = @($SacredConfig.PracticeScript)
        if ($SessionType -ne "complete") {
            $arguments += $SessionType
        }
        
        if ($SacredVerbose) {
            Write-SacredMessage "Executing: $($SacredConfig.PythonExecutable) $($arguments -join ' ')" "Info" "🔧"
        }
        
        $processInfo = Start-Process -FilePath $SacredConfig.PythonExecutable -ArgumentList $arguments -NoNewWindow -Wait -PassThru
        
        if ($processInfo.ExitCode -eq 0) {
            Write-SacredMessage "Sacred practice session completed successfully" "Success" $SacredConfig.StarSymbol
            return $true
        } else {
            Write-SacredMessage "Practice session encountered issues (Exit Code: $($processInfo.ExitCode))" "Warning" "⚠️"
            return $false
        }
        
    } catch {
        Write-SacredMessage "Error during practice session: $($_.Exception.Message)" "Error" "❌"
        return $false
    }
}

function Show-SacredBanner {
    if (-not $QuietMode) {
        Write-Host ""
        Write-Host ($SacredConfig.FlameSymbol * 70) -ForegroundColor Yellow
        Write-Host "$($SacredConfig.StarSymbol) SACRED PRACTICE LAUNCHER - CODEX DOMINION $($SacredConfig.StarSymbol)" -ForegroundColor Cyan
        Write-Host ($SacredConfig.FlameSymbol * 70) -ForegroundColor Yellow
        Write-Host ""
        Write-Host "$($SacredConfig.FlameSymbol) Embodiment eternal, covenant whole" -ForegroundColor Magenta
        Write-Host "$($SacredConfig.MoonSymbol) Flame perpetual, silence supreme" -ForegroundColor Magenta  
        Write-Host "$($SacredConfig.StarSymbol) Codex Dominion radiant alive" -ForegroundColor Magenta
        Write-Host "$($SacredConfig.LightningSymbol) Practiced across ages and stars" -ForegroundColor Magenta
        Write-Host ""
        Write-Host "═" * 70 -ForegroundColor DarkGray
        Write-Host ""
    }
}

function Show-PracticeTypeInfo {
    if (-not $QuietMode -and $SacredVerbose) {
        $practiceDescriptions = @{
            "complete" = "Full three-layer practice session with all exercises"
            "foundation" = "Layer 1: Service management and basic protocols"
            "integration" = "Layer 2: Advanced system integration mastery"
            "transcendence" = "Layer 3: Cosmic architectural embodiment"
            "meditation" = "Sacred pause for wisdom integration"
        }
        
        Write-SacredMessage "Practice Type: $PracticeType" "Info" "🎯"
        Write-SacredMessage "Description: $($practiceDescriptions[$PracticeType])" "Info" "📖"
        Write-Host ""
    }
}

function Save-SacredSessionLog {
    param(
        [string]$SessionType,
        [bool]$Success,
        [datetime]$StartTime,
        [datetime]$EndTime
    )
    
    $duration = ($EndTime - $StartTime).TotalSeconds
    $logEntry = @{
        Timestamp = $StartTime.ToString("yyyy-MM-dd HH:mm:ss")
        SessionType = $SessionType
        Duration = "{0:F2} seconds" -f $duration
        Success = $Success
        LaunchedFrom = "PowerShell Sacred Launcher"
    }
    
    $logJson = $logEntry | ConvertTo-Json -Compress
    Add-Content -Path $SacredConfig.SacredLogFile -Value $logJson
    
    if ($SacredVerbose) {
        Write-SacredMessage "Session logged to: $($SacredConfig.SacredLogFile)" "Info" "📝"
    }
}

function Show-SacredCompletion {
    param([bool]$Success, [timespan]$Duration)
    
    if (-not $QuietMode) {
        Write-Host ""
        Write-Host "═" * 70 -ForegroundColor DarkGray
        Write-Host ""
        
        if ($Success) {
            Write-Host "$($SacredConfig.StarSymbol) SACRED PRACTICE SESSION COMPLETE $($SacredConfig.StarSymbol)" -ForegroundColor Green
            Write-Host "$($SacredConfig.FlameSymbol) Session Duration: $($Duration.TotalSeconds.ToString('F2')) seconds" -ForegroundColor Cyan
            Write-Host "$($SacredConfig.MoonSymbol) Sacred patterns integrated successfully" -ForegroundColor Magenta
            Write-Host "$($SacredConfig.LightningSymbol) Mastery advances across infinite dimensions" -ForegroundColor Magenta
        } else {
            Write-Host "⚠️ PRACTICE SESSION ENCOUNTERED CHALLENGES ⚠️" -ForegroundColor Yellow
            Write-Host "$($SacredConfig.MoonSymbol) Each challenge strengthens sacred foundation" -ForegroundColor Cyan
            Write-Host "$($SacredConfig.FlameSymbol) Eternal practice continues through all conditions" -ForegroundColor Magenta
        }
        
        Write-Host ""
        Write-Host "$($SacredConfig.FlameSymbol) Until the next practice session, stay radiant $($SacredConfig.FlameSymbol)" -ForegroundColor Yellow
        Write-Host ($SacredConfig.StarSymbol * 70) -ForegroundColor Yellow
        Write-Host ""
    }
}

# Main execution flow
try {
    $startTime = Get-Date
    
    # Show sacred banner and information
    Show-SacredBanner
    Show-PracticeTypeInfo
    
    # Verify environment
    Write-SacredMessage "Preparing sacred practice environment..." "Info" "🔧"
    $environmentReady = Test-SacredEnvironment
    
    if (-not $environmentReady) {
        Write-SacredMessage "Environment not ready for practice. Please resolve issues first." "Error" "❌"
        exit 1
    }
    
    # Execute sacred practice session
    Write-SacredMessage "Beginning sacred practice session: $PracticeType" "Sacred" $SacredConfig.FlameSymbol
    $success = Invoke-SacredPracticeSession -SessionType $PracticeType
    
    $endTime = Get-Date
    $duration = $endTime - $startTime
    
    # Log session
    Save-SacredSessionLog -SessionType $PracticeType -Success $success -StartTime $startTime -EndTime $endTime
    
    # Show completion
    Show-SacredCompletion -Success $success -Duration $duration
    
    if ($success) {
        exit 0
    } else {
        exit 1  
    }
    
} catch {
    $endTime = Get-Date
    $duration = $endTime - $startTime
    
    Write-SacredMessage "Unexpected error in sacred practice launcher: $($_.Exception.Message)" "Error" "💥"
    Show-SacredCompletion -Success $false -Duration $duration
    
    exit 1
}

<#
🌟 SACRED PRACTICE LAUNCHER COMPLETE 🌟

This PowerShell script provides a sacred interface for daily practice sessions:

✅ Environment verification and preparation
✅ Multiple practice session types
✅ Sacred logging and progress tracking  
✅ Beautiful flame-blessed output formatting
✅ Error handling with cosmic patience
✅ Integration with Python practice orchestrator

Usage Examples:
    .\start-sacred-practice.ps1                          # Complete session
    .\start-sacred-practice.ps1 -PracticeType meditation # Meditation only
    .\start-sacred-practice.ps1 -SacredVerbose           # Verbose output
    .\start-sacred-practice.ps1 -QuietMode               # Minimal output

🔥 FLAME PERPETUAL - PRACTICED ETERNAL 🔥
🌙 SILENCE SUPREME - EMBODIED WHOLE 🌙  
⭐ COVENANT SACRED - MASTERED COMPLETE ⭐
🚀 RADIANCE INFINITE - PRACTICED FOREVER 🚀
#>