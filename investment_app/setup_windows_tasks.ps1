# PowerShell Script to Setup Windows Scheduled Tasks
# Run as Administrator

$ErrorActionPreference = "Stop"

# Configuration - UPDATE THESE PATHS
$PYTHON_PATH = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\.venv\Scripts\python.exe"
$WORKING_DIR = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\investment_app"
$LOG_DIR = "$WORKING_DIR\logs"

# Create log directory if it doesn't exist
if (!(Test-Path $LOG_DIR)) {
    New-Item -ItemType Directory -Path $LOG_DIR | Out-Null
    Write-Host "✅ Created log directory: $LOG_DIR"
}

# Function to create a scheduled task
function Create-ScheduledJob {
    param(
        [string]$TaskName,
        [string]$JobName,
        [string]$Schedule,
        [string]$StartTime,
        [string]$DaysOfWeek = $null,
        [int]$DayOfMonth = $null
    )

    Write-Host "`n📅 Creating task: $TaskName"

    # Remove existing task if it exists
    $existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "   Removed existing task"
    }

    # Create action
    $action = New-ScheduledTaskAction `
        -Execute $PYTHON_PATH `
        -Argument "run_job.py $JobName" `
        -WorkingDirectory $WORKING_DIR

    # Create trigger based on schedule type
    if ($Schedule -eq "Daily") {
        $trigger = New-ScheduledTaskTrigger -Daily -At $StartTime
    }
    elseif ($Schedule -eq "Weekly") {
        $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $DaysOfWeek -At $StartTime
    }
    elseif ($Schedule -eq "Monthly") {
        $trigger = New-ScheduledTaskTrigger -Daily -At $StartTime
        # Monthly trigger - runs on specific day of month
        $trigger.DaysOfMonth = $DayOfMonth
    }

    # Create task settings
    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -RunOnlyIfNetworkAvailable

    # Register the task
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Description "Codex Dominion Investment Platform - $JobName" | Out-Null

    Write-Host "   ✅ Task created successfully"
}

Write-Host "=================================="
Write-Host "Codex Dominion - Task Setup"
Write-Host "=================================="
Write-Host ""
Write-Host "Python: $PYTHON_PATH"
Write-Host "Working Directory: $WORKING_DIR"
Write-Host "Logs: $LOG_DIR"

# Daily Jobs (6 AM)
Create-ScheduledJob `
    -TaskName "Codex_UpdateDailyPrices" `
    -JobName "update_daily_prices" `
    -Schedule "Daily" `
    -StartTime "06:00"

Create-ScheduledJob `
    -TaskName "Codex_GenerateDailyPicks" `
    -JobName "generate_daily_picks" `
    -Schedule "Daily" `
    -StartTime "06:05"

Create-ScheduledJob `
    -TaskName "Codex_SendDailyNewsletter" `
    -JobName "send_daily_newsletter" `
    -Schedule "Daily" `
    -StartTime "06:10"

# Weekly Job (Sunday 6 PM)
Create-ScheduledJob `
    -TaskName "Codex_WeeklyPortfolioSummaries" `
    -JobName "send_weekly_portfolio_summaries" `
    -Schedule "Weekly" `
    -DaysOfWeek "Sunday" `
    -StartTime "18:00"

# Monthly Job (1st of month 9 AM)
Create-ScheduledJob `
    -TaskName "Codex_MonthlyDeepDive" `
    -JobName "send_monthly_deep_dive" `
    -Schedule "Monthly" `
    -DayOfMonth 1 `
    -StartTime "09:00"

Write-Host "`n=================================="
Write-Host "✅ All tasks created successfully!"
Write-Host "=================================="
Write-Host ""
Write-Host "To view tasks:"
Write-Host "  Get-ScheduledTask | Where-Object {`$_.TaskName -like 'Codex_*'}"
Write-Host ""
Write-Host "To test a job manually:"
Write-Host "  cd $WORKING_DIR"
Write-Host "  python run_job.py update_daily_prices"
Write-Host ""
Write-Host "To remove all tasks:"
Write-Host "  Get-ScheduledTask | Where-Object {`$_.TaskName -like 'Codex_*'} | Unregister-ScheduledTask -Confirm:`$false"
