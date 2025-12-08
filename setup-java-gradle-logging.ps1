param(
    [string]$ProjectPath = ".",
    [switch]$InstallGlobalGradle,
    [switch]$Verbose,
    [switch]$DryRun,
    [string]$LogFile = ".\setup_log.txt"
)

# -------------------------------
# Logging Function
# -------------------------------
function Log {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $entry = "$timestamp - $Message"
    Write-Host $entry -ForegroundColor $Color
    Add-Content -Path $LogFile -Value $entry -ErrorAction SilentlyContinue
}

# -------------------------------
# Rollback Function
# -------------------------------
function Rollback {
    Log "[ROLLBACK] Starting rollback..." "Red"

    if ($DryRun) {
        Log "[ROLLBACK] Dry-run mode: No changes reverted." "Yellow"
        exit 1
    }

    # Remove JAVA_HOME if set
    try {
        [Environment]::SetEnvironmentVariable("JAVA_HOME", $null, "User")
        Log "[ROLLBACK] JAVA_HOME removed." "Yellow"
    } catch {
        Log "[ROLLBACK] Failed to remove JAVA_HOME: $_" "Red"
    }

    # Remove Gradle if installed globally
    if (Test-Path "C:\Gradle\gradle-8.10") {
        try {
            Remove-Item -Path "C:\Gradle\gradle-8.10" -Recurse -Force -ErrorAction Stop
            Log "[ROLLBACK] Removed Gradle installation." "Yellow"
        } catch {
            Log "[ROLLBACK] Failed to remove Gradle: $_" "Red"
        }
    }

    Log "[ROLLBACK] Completed." "Red"
    exit 1
}

# -------------------------------
# Start Logging
# -------------------------------
Write-Host "`n=== Java & Gradle Environment Setup (with Logging) ===" -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "*** DRY-RUN MODE: No changes will be made ***" -ForegroundColor Magenta
}
Log "[INFO] Setup started for project: $ProjectPath" "Cyan"
Log "[INFO] Log file: $LogFile" "Cyan"
if ($DryRun) {
    Log "[INFO] DRY-RUN mode enabled" "Magenta"
}

# -------------------------------
# 1. Detect Gradle Wrapper
# -------------------------------
Log "[INFO] Checking for Gradle wrapper..." "Yellow"
$gradleWrapper = Get-ChildItem -Path $ProjectPath -Filter "gradlew.bat" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
if ($gradleWrapper) {
    Log "[INFO] Gradle wrapper found at: $($gradleWrapper.DirectoryName)" "Green"
    $gradleDir = $gradleWrapper.DirectoryName
} else {
    Log "[WARN] Gradle wrapper not found." "Yellow"
}

# -------------------------------
# 2. Detect Installed JDKs
# -------------------------------
Log "[INFO] Detecting installed JDKs..." "Yellow"
try {
    $javaPaths = @()
    $searchPaths = @("C:\Program Files\", "C:\Program Files (x86)\", "C:\Program Files\Java\", "C:\Program Files\Eclipse Adoptium\")

    foreach ($searchPath in $searchPaths) {
        if (Test-Path $searchPath) {
            $javaPaths += Get-ChildItem $searchPath -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -like "jdk*" }
        }
    }

    if ($javaPaths.Count -eq 0) {
        Log "[ERROR] No JDK installations found." "Red"
        Rollback
    } else {
        # Prioritize Java 21
        $jdk21 = $javaPaths | Where-Object { $_.Name -match "jdk-?21" } | Select-Object -First 1
        if ($jdk21) {
            $jdk = $jdk21
            Log "[INFO] Found Java 21 at: $($jdk.FullName)" "Green"
        } else {
            $jdk = $javaPaths | Sort-Object Name -Descending | Select-Object -First 1
            Log "[INFO] Using highest version JDK at: $($jdk.FullName)" "Yellow"
        }

        if (-not $DryRun) {
            $env:JAVA_HOME = $jdk.FullName
            setx JAVA_HOME $jdk.FullName | Out-Null

            if ($LASTEXITCODE -eq 0) {
                Log "[INFO] ✅ JAVA_HOME set to: $($jdk.FullName)" "Green"
            } else {
                Log "[ERROR] Failed to set JAVA_HOME." "Red"
                Rollback
            }
        } else {
            Log "[DRY-RUN] Would set JAVA_HOME to: $($jdk.FullName)" "Magenta"
        }
    }
} catch {
    Log "[ERROR] Failed to detect JDK: $_" "Red"
    Rollback
}

# -------------------------------
# 3. Detect Java Version
# -------------------------------
Log "[INFO] Checking Java version..." "Yellow"
try {
    $versionOutput = & "$env:JAVA_HOME\bin\java.exe" -version 2>&1 | Out-String
    if ($versionOutput -match 'version "?(\d+(\.\d+)*)"?') {
        $javaVersion = $matches[1]
        $majorVersion = ($javaVersion -split '\.')[0]
        Log "[INFO] Detected Java version: $javaVersion (major: $majorVersion)" "Green"

        if ([int]$majorVersion -ge 22) {
            Log "[WARN] Java $majorVersion detected. Java 21 is recommended for better compatibility." "Yellow"
        }
    } else {
        Log "[ERROR] Could not detect Java version." "Red"
        if ($Verbose) {
            Log "[DEBUG] Java output: $($versionOutput.Substring(0, [Math]::Min(200, $versionOutput.Length)))" "Cyan"
        }
        Rollback
    }
} catch {
    Log "[ERROR] Java version check failed: $_" "Red"
    Rollback
}

# -------------------------------
# 4. Optional Global Gradle Install
# -------------------------------
if ($InstallGlobalGradle) {
    Log "[INFO] Installing Gradle globally..." "Yellow"

    if ($DryRun) {
        Log "[DRY-RUN] Would download Gradle 8.10 from https://services.gradle.org/distributions/gradle-8.10-bin.zip" "Magenta"
        Log "[DRY-RUN] Would extract to C:\Gradle\gradle-8.10" "Magenta"
        Log "[DRY-RUN] Would set GRADLE_HOME and update PATH" "Magenta"
    } else {
        $gradleVersion = "8.10"
        $gradleZip = "$env:TEMP\gradle.zip"
        $gradleUrl = "https://services.gradle.org/distributions/gradle-$gradleVersion-bin.zip"
        $gradleHome = "C:\Gradle\gradle-$gradleVersion"

        try {
            Log "[INFO] Downloading Gradle $gradleVersion..." "Yellow"
            Invoke-WebRequest -Uri $gradleUrl -OutFile $gradleZip -ErrorAction Stop
            Log "[INFO] Download successful." "Green"

            Log "[INFO] Extracting Gradle to C:\Gradle..." "Yellow"
            Expand-Archive $gradleZip -DestinationPath "C:\Gradle" -Force -ErrorAction Stop

            Log "[INFO] Setting GRADLE_HOME and updating PATH..." "Yellow"
            setx GRADLE_HOME $gradleHome | Out-Null
            $env:GRADLE_HOME = $gradleHome
            $env:PATH = "$gradleHome\bin;$env:PATH"

            # Update user PATH
            $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
            if ($currentPath -notlike "*$gradleHome\bin*") {
                [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$gradleHome\bin", "User")
            }

            Log "[INFO] ✅ Gradle $gradleVersion installed globally at $gradleHome" "Green"

            # Verify installation
            $gradleVersionCheck = & "$gradleHome\bin\gradle.bat" --version 2>&1
            $gradleVersionCheck | Select-String -Pattern "Gradle $gradleVersion" | ForEach-Object {
                Log "[INFO] Verified: $_" "Green"
            }
        } catch {
            Log "[ERROR] Gradle installation failed: $_" "Red"
            Rollback
        } finally {
            # Clean up zip file
            if (Test-Path $gradleZip) {
                Remove-Item $gradleZip -Force -ErrorAction SilentlyContinue
                Log "[INFO] Cleaned up temporary files." "Cyan"
            }
        }
    }
}

# -------------------------------
# 5. Detect Project Type & Build
# -------------------------------
Log "[INFO] Checking project type..." "Yellow"
$originalLocation = Get-Location

try {
    if ($gradleWrapper) {
        Set-Location $gradleDir
        $projectPath = $gradleDir
    } else {
        $projectPath = (Resolve-Path $ProjectPath).Path
        Set-Location $projectPath
    }

    if (Test-Path "$projectPath\pom.xml") {
        Log "[INFO] Maven project detected." "Cyan"

        if ($DryRun) {
            Log "[DRY-RUN] Would run: mvn clean install" "Magenta"
        } else {
            Log "[INFO] Building Maven project..." "Yellow"

            $mavenOutput = & mvn clean install 2>&1
            if ($LASTEXITCODE -eq 0) {
                Log "[INFO] ✅ Maven build completed successfully!" "Green"
                $mavenOutput | Select-String -Pattern "BUILD SUCCESS" | ForEach-Object {
                    Log "[INFO] $_" "Green"
                }
            } else {
                Log "[ERROR] Maven build failed with exit code: $LASTEXITCODE" "Red"
                if ($Verbose) {
                    Log "[DEBUG] Maven output: $mavenOutput" "Red"
                }
                Rollback
            }
        }

    } elseif (Test-Path "$projectPath\build.gradle") {
        Log "[INFO] Gradle project detected." "Cyan"

        if ($DryRun) {
            if ($gradleWrapper) {
                Log "[DRY-RUN] Would upgrade Gradle wrapper to 8.7" "Magenta"
                Log "[DRY-RUN] Would run: .\gradlew.bat build" "Magenta"
            } else {
                Log "[DRY-RUN] Would run: gradle build (global Gradle)" "Magenta"
            }
        } else {
            if ($gradleWrapper) {
                Log "[INFO] Using Gradle wrapper..." "Yellow"

                # Upgrade wrapper
                Log "[INFO] Upgrading Gradle wrapper to 8.7..." "Yellow"
                & .\gradlew.bat wrapper --gradle-version 8.7 2>&1 | Out-Null
                if ($LASTEXITCODE -eq 0) {
                    Log "[INFO] ✅ Gradle wrapper upgraded to 8.7." "Green"
                } else {
                    Log "[WARN] Gradle wrapper upgrade returned exit code: $LASTEXITCODE" "Yellow"
                }

                # Clean and build
                Log "[INFO] Cleaning and building project..." "Yellow"
                Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
                Start-Sleep -Seconds 1

                $buildOutput = & .\gradlew.bat build 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Log "[INFO] ✅ Build completed successfully!" "Green"
                    $buildOutput | Select-String -Pattern "BUILD SUCCESSFUL" | ForEach-Object {
                        Log "[INFO] $_" "Green"
                    }
                } else {
                    Log "[ERROR] Build failed with exit code: $LASTEXITCODE" "Red"
                    if ($Verbose) {
                        Log "[DEBUG] Build output: $buildOutput" "Red"
                    }
                    Rollback
                }
            } else {
                Log "[WARN] No Gradle wrapper found. Attempting to use global Gradle..." "Yellow"

                $buildOutput = & gradle build 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Log "[INFO] ✅ Gradle build completed using global Gradle." "Green"
                } else {
                    Log "[ERROR] Build failed with exit code: $LASTEXITCODE" "Red"
                    if ($Verbose) {
                        Log "[DEBUG] Build output: $buildOutput" "Red"
                    }
                    Rollback
                }
            }
        }
    } else {
        Log "[WARN] Unknown project type. No build executed." "Yellow"
        Log "[INFO] Supported project types: Maven (pom.xml) or Gradle (build.gradle)" "Cyan"
    }
} catch {
    Log "[ERROR] Build failed: $_" "Red"
    Rollback
} finally {
    Set-Location $originalLocation
}

# -------------------------------
# Summary
# -------------------------------
Write-Host "`n=== Setup Complete ===" -ForegroundColor Cyan
Log "[INFO] Setup completed successfully." "Green"
Log "[INFO] Summary:" "Yellow"
Log "  - Java: $javaVersion at $($jdk.FullName)" "White"
if ($InstallGlobalGradle) {
    Log "  - Gradle: 8.10 installed globally" "White"
}
if ($gradleWrapper) {
    Log "  - Project: $(Split-Path $gradleDir -Leaf) (Gradle wrapper)" "White"
}
Log "  - Log file: $LogFile" "Cyan"
Write-Host ""
