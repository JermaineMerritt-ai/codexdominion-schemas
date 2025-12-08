param(
    [string]$ProjectPath = ".",
    [switch]$InstallGlobalGradle,
    [switch]$Verbose
)

Write-Host "`n=== Java & Gradle Environment Setup ===" -ForegroundColor Cyan

# -------------------------------
# 1. Detect Gradle Wrapper
# -------------------------------
Write-Host "`n[INFO] Checking for Gradle wrapper..." -ForegroundColor Yellow
$gradleWrapper = Get-ChildItem -Path $ProjectPath -Filter "gradlew.bat" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
if ($gradleWrapper) {
    Write-Host "[INFO] Gradle wrapper found at: $($gradleWrapper.DirectoryName)" -ForegroundColor Green
    $gradleDir = $gradleWrapper.DirectoryName
} else {
    Write-Host "[WARN] Gradle wrapper not found. Consider creating one or installing Gradle globally." -ForegroundColor Yellow
}

# -------------------------------
# 2. Detect Installed JDKs
# -------------------------------
Write-Host "`n[INFO] Detecting installed JDKs..." -ForegroundColor Yellow
$javaPaths = @()
$searchPaths = @("C:\Program Files\", "C:\Program Files (x86)\", "C:\Program Files\Java\", "C:\Program Files\Eclipse Adoptium\")

foreach ($searchPath in $searchPaths) {
    if (Test-Path $searchPath) {
        $javaPaths += Get-ChildItem $searchPath -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -like "jdk*" }
    }
}

if ($javaPaths.Count -eq 0) {
    Write-Error "[ERROR] No JDK installations found."
    exit 1
} else {
    # Prioritize Java 21
    $jdk21 = $javaPaths | Where-Object { $_.Name -match "jdk-?21" } | Select-Object -First 1
    if ($jdk21) {
        $jdk = $jdk21
        Write-Host "[INFO] Found Java 21 at: $($jdk.FullName)" -ForegroundColor Green
    } else {
        $jdk = $javaPaths | Sort-Object Name -Descending | Select-Object -First 1
        Write-Host "[INFO] Using highest version JDK at: $($jdk.FullName)" -ForegroundColor Yellow
    }

    $env:JAVA_HOME = $jdk.FullName
    setx JAVA_HOME $jdk.FullName | Out-Null

    if ($LASTEXITCODE -eq 0) {
        Write-Host "[INFO] ✅ JAVA_HOME set to: $($jdk.FullName)" -ForegroundColor Green
    } else {
        Write-Error "[ERROR] Failed to set JAVA_HOME environment variable."
    }
}

# -------------------------------
# 3. Detect Java Version
# -------------------------------
Write-Host "`n[INFO] Checking Java version..." -ForegroundColor Yellow
$versionOutput = & "$env:JAVA_HOME\bin\java.exe" -version 2>&1 | Out-String
if ($versionOutput -match 'version "?(\d+(\.\d+)*)"?') {
    $javaVersion = $matches[1]
    $majorVersion = ($javaVersion -split '\.')[0]
    Write-Host "[INFO] Detected Java version: $javaVersion (major: $majorVersion)" -ForegroundColor Green

    if ([int]$majorVersion -ge 22) {
        Write-Host "[WARN] Java $majorVersion detected. Java 21 is recommended for better compatibility." -ForegroundColor Yellow
    }
} else {
    Write-Host "[WARN] Could not detect Java version from output." -ForegroundColor Yellow
    Write-Host "[INFO] Java output: $($versionOutput.Substring(0, [Math]::Min(200, $versionOutput.Length)))" -ForegroundColor Cyan
}

# -------------------------------
# 4. Optional Global Gradle Install
# -------------------------------
if ($InstallGlobalGradle) {
    Write-Host "`n[INFO] Installing Gradle globally..." -ForegroundColor Yellow
    $gradleVersion = "8.10"
    $gradleZip = "$env:TEMP\gradle.zip"
    $gradleUrl = "https://services.gradle.org/distributions/gradle-$gradleVersion-bin.zip"
    $gradleHome = "C:\Gradle\gradle-$gradleVersion"

    try {
        Write-Host "[INFO] Downloading Gradle $gradleVersion..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $gradleUrl -OutFile $gradleZip -ErrorAction Stop
        Write-Host "[INFO] Download successful." -ForegroundColor Green

        Write-Host "[INFO] Extracting Gradle to C:\Gradle..." -ForegroundColor Yellow
        Expand-Archive $gradleZip -DestinationPath "C:\Gradle" -Force -ErrorAction Stop

        Write-Host "[INFO] Setting GRADLE_HOME and updating PATH..." -ForegroundColor Yellow
        setx GRADLE_HOME $gradleHome | Out-Null
        $env:GRADLE_HOME = $gradleHome
        $env:PATH = "$gradleHome\bin;$env:PATH"

        # Update user PATH
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        if ($currentPath -notlike "*$gradleHome\bin*") {
            [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$gradleHome\bin", "User")
        }

        Write-Host "[INFO] ✅ Gradle $gradleVersion installed globally at $gradleHome" -ForegroundColor Green

        # Verify installation
        $gradleVersionCheck = & "$gradleHome\bin\gradle.bat" --version 2>&1
        $gradleVersionCheck | Select-String -Pattern "Gradle $gradleVersion" | ForEach-Object {
            Write-Host "[INFO] $_" -ForegroundColor Green
        }
    } catch {
        Write-Error "[ERROR] Gradle installation failed: $_"
        Write-Host "[INFO] Please install Gradle manually from: https://gradle.org/releases/" -ForegroundColor Yellow
    } finally {
        # Clean up zip file
        if (Test-Path $gradleZip) {
            Remove-Item $gradleZip -Force -ErrorAction SilentlyContinue
        }
    }
}

# -------------------------------
# 5. Detect Project Type & Build
# -------------------------------
Write-Host "`n[INFO] Checking project type..." -ForegroundColor Yellow
$originalLocation = Get-Location

if ($gradleWrapper) {
    Set-Location $gradleDir
    $projectPath = $gradleDir
} else {
    $projectPath = (Resolve-Path $ProjectPath).Path
    Set-Location $projectPath
}

if (Test-Path "$projectPath\pom.xml") {
    Write-Host "[INFO] Maven project detected." -ForegroundColor Cyan
    Write-Host "[INFO] Building Maven project..." -ForegroundColor Yellow

    try {
        $mavenOutput = & mvn clean install 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[INFO] ✅ Maven build completed successfully!" -ForegroundColor Green
            $mavenOutput | Select-String -Pattern "BUILD SUCCESS" | ForEach-Object {
                Write-Host "[INFO] $_" -ForegroundColor Green
            }
        } else {
            Write-Error "[ERROR] Maven build failed with exit code: $LASTEXITCODE"
            if ($Verbose) {
                Write-Host $mavenOutput -ForegroundColor Red
            }
        }
    } catch {
        Write-Error "[ERROR] Maven build execution failed: $_"
    }

} elseif (Test-Path "$projectPath\build.gradle") {
    Write-Host "[INFO] Gradle project detected." -ForegroundColor Cyan

    if ($gradleWrapper) {
        Write-Host "[INFO] Using Gradle wrapper..." -ForegroundColor Yellow

        # Upgrade wrapper
        Write-Host "[INFO] Upgrading Gradle wrapper to 8.7..." -ForegroundColor Yellow
        try {
            & .\gradlew.bat wrapper --gradle-version 8.7 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "[INFO] ✅ Gradle wrapper upgraded to 8.7." -ForegroundColor Green
            } else {
                Write-Host "[WARN] Gradle wrapper upgrade returned exit code: $LASTEXITCODE" -ForegroundColor Yellow
            }
        } catch {
            Write-Error "[ERROR] Gradle wrapper upgrade failed: $_"
        }

        # Clean and build
        Write-Host "[INFO] Cleaning and building project..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1

        try {
            $buildOutput = & .\gradlew.bat build 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "[INFO] ✅ Build completed successfully!" -ForegroundColor Green
                $buildOutput | Select-String -Pattern "BUILD SUCCESSFUL" | ForEach-Object {
                    Write-Host "[INFO] $_" -ForegroundColor Green
                }
            } else {
                Write-Error "[ERROR] Build failed with exit code: $LASTEXITCODE"
                if ($Verbose) {
                    Write-Host $buildOutput -ForegroundColor Red
                }
            }
        } catch {
            Write-Error "[ERROR] Build execution failed: $_"
        }
    } else {
        Write-Host "[WARN] No Gradle wrapper found. Attempting to use global Gradle..." -ForegroundColor Yellow

        try {
            $buildOutput = & gradle build 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "[INFO] ✅ Build completed successfully!" -ForegroundColor Green
            } else {
                Write-Error "[ERROR] Build failed with exit code: $LASTEXITCODE"
                if ($Verbose) {
                    Write-Host $buildOutput -ForegroundColor Red
                }
            }
        } catch {
            Write-Error "[ERROR] Build execution failed: $_"
            Write-Host "[INFO] Consider installing Gradle globally with -InstallGlobalGradle flag." -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "[WARN] Unknown project type. No build executed." -ForegroundColor Yellow
    Write-Host "[INFO] Supported project types: Maven (pom.xml) or Gradle (build.gradle)" -ForegroundColor Cyan
}

Set-Location $originalLocation

Write-Host "`n=== Setup Complete ===" -ForegroundColor Cyan
Write-Host "[INFO] Summary:" -ForegroundColor Yellow
Write-Host "  - Java: $javaVersion at $($jdk.FullName)" -ForegroundColor White
if ($InstallGlobalGradle) {
    Write-Host "  - Gradle: 8.10 installed globally" -ForegroundColor White
}
if ($gradleWrapper) {
    Write-Host "  - Project: $(Split-Path $gradleDir -Leaf) (Gradle wrapper)" -ForegroundColor White
}
Write-Host ""
