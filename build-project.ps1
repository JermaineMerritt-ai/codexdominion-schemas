# Set strict mode for safety
Set-StrictMode -Version Latest

# Define paths
$JAVA_HOME = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex_project\openJdk-25"
$ProjectPath = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\codexdominion-schemas\templates\kubernetes-ovh-java"
$LogFile = "$ProjectPath\build-log.txt"

# Update PATH for Java
$env:JAVA_HOME = $JAVA_HOME
$env:Path = "$JAVA_HOME\bin;" + $env:Path

# Navigate to project directory
Set-Location $ProjectPath

# Start logging
Write-Host "Starting Maven build..." -ForegroundColor Cyan
"Build started at $(Get-Date)" | Out-File $LogFile

# Run Maven build with profiles
$mvnCommand = "mvn clean install -Pskip-tests,native-access --no-transfer-progress --fail-at-end"
Write-Host "Executing: $mvnCommand" -ForegroundColor Yellow

try {
    & cmd /c $mvnCommand 2>&1 | Tee-Object -FilePath $LogFile
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Build completed successfully!" -ForegroundColor Green
        "Build completed successfully at $(Get-Date)" | Out-File -Append $LogFile
    } else {
        Write-Host "❌ Build failed. Check $LogFile for details." -ForegroundColor Red
        "Build failed at $(Get-Date)" | Out-File -Append $LogFile
    }
} catch {
    Write-Host "❌ An error occurred: $_" -ForegroundColor Red
    "Error: $_" | Out-File -Append $LogFile
}

Write-Host "Log saved to: $LogFile" -ForegroundColor Cyan
