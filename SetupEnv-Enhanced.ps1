param(
    [string]$ProjectPath = ".",
    [switch]$InstallGlobalGradle,
    [switch]$Verbose,
    [switch]$DryRun,
    [string]$LogFile = ".\setup_log.txt"
)

# -------------------------------
# Logging Function with Auto-Color
# -------------------------------
function Log {
    param(
        [string]$Message,
        [string]$Color = ""
    )

    $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $entry = "$timestamp - $Message"

    # Auto-detect color from message prefix if not specified
    if (-not $Color) {
        if ($Message -like "*[INFO]*") {
            $Color = "Green"
        } elseif ($Message -like "*[WARN]*") {
            $Color = "Yellow"
        } elseif ($Message -like "*[ERROR]*") {
            $Color = "Red"
        } elseif ($Message -like "*[ROLLBACK]*") {
            $Color = "Magenta"
        } elseif ($Message -like "*[DRY-RUN]*") {
            $Color = "Cyan"
        } elseif ($Message -like "*[DEBUG]*") {
            $Color = "Gray"
        } else {
            $Color = "White"
        }
    }

    # Output to console with color
    Write-Host $entry -ForegroundColor $Color

    # Always log to file
    Add-Content -Path $LogFile -Value $entry -ErrorAction SilentlyContinue
}

# -------------------------------
# Rollback Function
# -------------------------------
function Rollback {
    Log "[ROLLBACK] Starting rollback..."

    if ($DryRun) {
        Log "[ROLLBACK] Dry-run mode: No changes reverted."
        exit 1
    }

    # Remove JAVA_HOME if set
    try {
        [Environment]::SetEnvironmentVariable("JAVA_HOME", $null, "User")
        Log "[ROLLBACK] JAVA_HOME removed."
    } catch {
        Log "[ERROR] [ROLLBACK] Failed to remove JAVA_HOME: $_"
    }

    # Remove Gradle if installed globally
    if (Test-Path "C:\Gradle\gradle-8.10") {
        try {
            Remove-Item -Path "C:\Gradle\gradle-8.10" -Recurse -Force -ErrorAction Stop
            Log "[ROLLBACK] Removed Gradle installation."
        } catch {
            Log "[ERROR] [ROLLBACK] Failed to remove Gradle: $_"
        }
    }

    Log "[ROLLBACK] Completed."
    exit 1
}

# -------------------------------
# Start Setup
# -------------------------------
if ($DryRun) {
    Write-Host "`n*** DRY-RUN MODE: No changes will be made ***`n" -ForegroundColor Cyan
}

Write-Host "`n=== Java & Gradle Environment Setup (Enhanced) ===`n" -ForegroundColor Cyan
Log "[INFO] Setup started for project: $ProjectPath"
Log "[INFO] Log file: $LogFile"

# -------------------------------
# 1. Detect Gradle Wrapper
# -------------------------------
Log "[INFO] Checking for Gradle wrapper..."
$gradleWrapper = Get-ChildItem -Path $ProjectPath -Filter "gradlew.bat" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if ($gradleWrapper) {
    Log "[INFO] Gradle wrapper found at: $($gradleWrapper.DirectoryName)"
    $gradleDir = $gradleWrapper.DirectoryName
} else {
    Log "[WARN] Gradle wrapper (gradlew.bat) not found."
    $gradleDir = $null
}

# -------------------------------
# 2. Detect Installed JDKs
# -------------------------------
Log "[INFO] Detecting installed JDKs..."

$jdkSearchPaths = @(
    "C:\Program Files\Java",
    "C:\Program Files\Eclipse Adoptium",
    "C:\Program Files\Microsoft",
    "C:\Program Files (x86)\Java"
)

$jdkFound = $null

foreach ($searchPath in $jdkSearchPaths) {
    if (Test-Path $searchPath) {
        $javaPaths = Get-ChildItem -Path $searchPath -Directory -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -match "jdk" }

        if ($javaPaths) {
            if ($Verbose) {
                Log "[DEBUG] Found JDK paths in ${searchPath}: $($javaPaths.Name -join ', ')"
            }

            # Prioritize Java 21
            $jdk21 = $javaPaths | Where-Object { $_.Name -match "jdk-?21" } | Select-Object -First 1

            if ($jdk21) {
                $jdkFound = $jdk21
                Log "[INFO] Found Java 21 at: $($jdkFound.FullName)"
                break
            } elseif (-not $jdkFound) {
                $jdkFound = $javaPaths | Sort-Object Name -Descending | Select-Object -First 1
            }
        }
    }
}

if (-not $jdkFound) {
    Log "[ERROR] No JDK installations found in standard locations."
    Rollback
}

# Set JAVA_HOME
if ($DryRun) {
    Log "[DRY-RUN] Would set JAVA_HOME to: $($jdkFound.FullName)"
} else {
    try {
        $env:JAVA_HOME = $jdkFound.FullName
        [Environment]::SetEnvironmentVariable("JAVA_HOME", $jdkFound.FullName, "User")
        Log "[INFO] ✅ JAVA_HOME set to: $($jdkFound.FullName)"
    } catch {
        Log "[ERROR] Failed to set JAVA_HOME: $_"
        Rollback
    }
}

# -------------------------------
# 3. Verify Java Version
# -------------------------------
Log "[INFO] Checking Java version..."

if ($DryRun) {
    Log "[DRY-RUN] Would check Java version at: $($jdkFound.FullName)\bin\java.exe"
} else {
    try {
        $javaExe = Join-Path $env:JAVA_HOME "bin\java.exe"

        if (-not (Test-Path $javaExe)) {
            Log "[ERROR] Java executable not found at: $javaExe"
            Rollback
        }

        $versionOutput = & $javaExe -version 2>&1 | Out-String

        if ($Verbose) {
            Log "[DEBUG] Raw java -version output: $versionOutput"
        }

        if ($versionOutput -match 'version\s+"?(\d+(\.\d+)*)"?') {
            $javaVersion = $matches[1]
            $majorVersion = $javaVersion.Split('.')[0]
            Log "[INFO] Detected Java version: $javaVersion (major: $majorVersion)"
        } else {
            Log "[ERROR] Could not parse Java version from output."
            Rollback
        }
    } catch {
        Log "[ERROR] Java version check failed: $_"
        if ($Verbose) {
            Log "[DEBUG] Exception details: $($_.Exception.Message)"
        }
        Rollback
    }
}

# -------------------------------
# 4. Optional Global Gradle Install
# -------------------------------
if ($InstallGlobalGradle) {
    Log "[INFO] Installing Gradle globally..."

    $gradleVersion = "8.10"
    $gradleUrl = "https://services.gradle.org/distributions/gradle-$gradleVersion-bin.zip"
    $gradleZip = "gradle-$gradleVersion.zip"
    $gradleInstallPath = "C:\Gradle\gradle-$gradleVersion"

    if ($DryRun) {
        Log "[DRY-RUN] Would download Gradle $gradleVersion from: $gradleUrl"
        Log "[DRY-RUN] Would extract to: $gradleInstallPath"
        Log "[DRY-RUN] Would set GRADLE_HOME and update PATH"
    } else {
        try {
            # Download
            Log "[INFO] Downloading Gradle $gradleVersion..."
            Invoke-WebRequest -Uri $gradleUrl -OutFile $gradleZip -UseBasicParsing
            Log "[INFO] Download successful."

            # Extract
            Log "[INFO] Extracting Gradle to C:\Gradle..."
            if (-not (Test-Path "C:\Gradle")) {
                New-Item -ItemType Directory -Path "C:\Gradle" -Force | Out-Null
            }
            Expand-Archive -Path $gradleZip -DestinationPath "C:\Gradle" -Force

            # Set environment variables
            Log "[INFO] Setting GRADLE_HOME and updating PATH..."
            $env:GRADLE_HOME = $gradleInstallPath
            [Environment]::SetEnvironmentVariable("GRADLE_HOME", $gradleInstallPath, "User")

            $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
            $gradleBinPath = "$gradleInstallPath\bin"

            if ($currentPath -notlike "*$gradleBinPath*") {
                [Environment]::SetEnvironmentVariable("Path", "$currentPath;$gradleBinPath", "User")
                $env:Path = "$env:Path;$gradleBinPath"
            }

            Log "[INFO] ✅ Gradle $gradleVersion installed globally at $gradleInstallPath"

            # Verify installation
            $gradleCmd = Get-Command gradle -ErrorAction SilentlyContinue
            if ($gradleCmd) {
                $gradleVerOutput = & gradle --version 2>&1 | Select-String "Gradle" | Select-Object -First 1
                Log "[INFO] Verified: $gradleVerOutput"
            }

            # Cleanup
            Remove-Item -Path $gradleZip -Force -ErrorAction SilentlyContinue
            Log "[INFO] Cleaned up temporary files."

        } catch {
            Log "[ERROR] Gradle installation failed: $_"
            if ($Verbose) {
                Log "[DEBUG] Exception: $($_.Exception.Message)"
            }
            Rollback
        }
    }
}

# -------------------------------
# 5. Detect Project Type & Build
# -------------------------------
Log "[INFO] Checking project type..."

try {
    $pomPath = Join-Path $ProjectPath "pom.xml"
    $gradlePath = Join-Path $ProjectPath "build.gradle"

    if (Test-Path $pomPath) {
        Log "[INFO] Maven project detected."

        if ($DryRun) {
            Log "[DRY-RUN] Would run: mvn clean compile"
        } else {
            Log "[INFO] Running Maven build..."
            Push-Location $ProjectPath

            try {
                $mavenOutput = mvn clean compile 2>&1

                if ($LASTEXITCODE -eq 0) {
                    Log "[INFO] ✅ Maven build completed successfully!"

                    # Show BUILD SUCCESS line if present
                    $successLine = $mavenOutput | Select-String "BUILD SUCCESS" | Select-Object -First 1
                    if ($successLine) {
                        Log "[INFO] $successLine"
                    }
                } else {
                    Log "[ERROR] Maven build failed with exit code: $LASTEXITCODE"
                    if ($Verbose) {
                        Log "[DEBUG] Maven output: $mavenOutput"
                    }
                    Pop-Location
                    Rollback
                }
            } finally {
                Pop-Location
            }
        }

    } elseif (Test-Path $gradlePath) {
        Log "[INFO] Gradle project detected."

        if ($gradleDir) {
            Log "[INFO] Using Gradle wrapper..."

            if ($DryRun) {
                Log "[DRY-RUN] Would upgrade Gradle wrapper to 8.7"
                Log "[DRY-RUN] Would run: .\gradlew.bat build"
            } else {
                Push-Location $gradleDir

                try {
                    # Upgrade wrapper
                    Log "[INFO] Upgrading Gradle wrapper to 8.7..."
                    $wrapperOutput = .\gradlew.bat wrapper --gradle-version 8.7 2>&1

                    if ($LASTEXITCODE -eq 0) {
                        Log "[INFO] ✅ Gradle wrapper upgraded to 8.7."
                    } else {
                        Log "[WARN] Wrapper upgrade had issues (exit code: $LASTEXITCODE)"
                    }

                    # Build
                    Log "[INFO] Cleaning and building project..."
                    $buildOutput = .\gradlew.bat clean build 2>&1

                    if ($LASTEXITCODE -eq 0) {
                        Log "[INFO] ✅ Build completed successfully!"

                        # Show BUILD SUCCESSFUL line if present
                        $successLine = $buildOutput | Select-String "BUILD SUCCESSFUL" | Select-Object -First 1
                        if ($successLine) {
                            Log "[INFO] $successLine"
                        }
                    } else {
                        Log "[ERROR] Gradle build failed with exit code: $LASTEXITCODE"
                        if ($Verbose) {
                            Log "[DEBUG] Gradle output: $buildOutput"
                        }
                        Pop-Location
                        Rollback
                    }
                } finally {
                    Pop-Location
                }
            }
        } else {
            Log "[WARN] No Gradle wrapper found. Attempting to use global Gradle..."

            if ($DryRun) {
                Log "[DRY-RUN] Would run: gradle build"
            } else {
                $gradleCmd = Get-Command gradle -ErrorAction SilentlyContinue

                if (-not $gradleCmd) {
                    Log "[ERROR] Global Gradle not found. Please use -InstallGlobalGradle or add a Gradle wrapper."
                    Rollback
                }

                Push-Location $ProjectPath

                try {
                    $buildOutput = gradle clean build 2>&1

                    if ($LASTEXITCODE -eq 0) {
                        Log "[INFO] ✅ Gradle build completed using global Gradle."
                    } else {
                        Log "[ERROR] Gradle build failed with exit code: $LASTEXITCODE"
                        Pop-Location
                        Rollback
                    }
                } finally {
                    Pop-Location
                }
            }
        }

    } else {
        Log "[WARN] Unknown project type. No pom.xml or build.gradle found."
        Log "[INFO] Skipping build step."
    }

} catch {
    Log "[ERROR] Build process failed: $_"
    if ($Verbose) {
        Log "[DEBUG] Exception: $($_.Exception.Message)"
    }
    Rollback
}

# -------------------------------
# Completion Summary
# -------------------------------
Write-Host "`n=== Setup Complete ===`n" -ForegroundColor Green
Log "[INFO] Setup completed successfully."
Log "[INFO] Summary:"
Log "  - Java: $javaVersion at $($jdkFound.FullName)"

if ($InstallGlobalGradle) {
    Log "  - Gradle: $gradleVersion installed globally"
}

if ($gradleDir) {
    Log "  - Project: $(Split-Path $ProjectPath -Leaf) (Gradle wrapper)"
} elseif (Test-Path $pomPath) {
    Log "  - Project: $(Split-Path $ProjectPath -Leaf) (Maven)"
}

Log "  - Log file: $LogFile"

if ($DryRun) {
    Write-Host "`n*** DRY-RUN COMPLETED: No actual changes were made ***`n" -ForegroundColor Cyan
}
