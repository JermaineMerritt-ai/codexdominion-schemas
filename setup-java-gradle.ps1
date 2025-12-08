param([switch]$InstallGlobalGradle)

Write-Host "=== Java & Gradle Environment Setup ===" -ForegroundColor Cyan

# Install Gradle globally if requested
if ($InstallGlobalGradle) {
    Write-Host "Installing Gradle globally..." -ForegroundColor Yellow
    $gradleVersion = "8.10"
    $gradleZip = "$env:TEMP\gradle.zip"
    $gradleUrl = "https://services.gradle.org/distributions/gradle-$gradleVersion-bin.zip"
    $gradleHome = "C:\Gradle\gradle-$gradleVersion"

    try {
        Write-Host "Downloading Gradle $gradleVersion..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $gradleUrl -OutFile $gradleZip -ErrorAction Stop
        Write-Host "Download successful." -ForegroundColor Green

        Write-Host "Extracting Gradle to C:\Gradle..." -ForegroundColor Yellow
        Expand-Archive $gradleZip -DestinationPath "C:\Gradle" -Force -ErrorAction Stop

        Write-Host "Setting GRADLE_HOME and updating PATH..." -ForegroundColor Yellow
        setx GRADLE_HOME $gradleHome | Out-Null
        $env:GRADLE_HOME = $gradleHome
        $env:PATH = "$gradleHome\bin;$env:PATH"

        # Also update system PATH
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        if ($currentPath -notlike "*$gradleHome\bin*") {
            [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$gradleHome\bin", "User")
        }

        Write-Host "✅ Gradle $gradleVersion installed globally at $gradleHome" -ForegroundColor Green

        # Verify installation
        $gradleVersionCheck = & "$gradleHome\bin\gradle.bat" --version 2>&1
        Write-Host "Gradle version check:" -ForegroundColor Cyan
        $gradleVersionCheck | Select-String -Pattern "Gradle" | ForEach-Object { Write-Host $_.Line -ForegroundColor Green }
    } catch {
        Write-Error "Gradle installation failed: $_"
        Write-Host "Please install Gradle manually from: https://gradle.org/releases/" -ForegroundColor Yellow
    } finally {
        # Clean up zip file
        if (Test-Path $gradleZip) {
            Remove-Item $gradleZip -Force -ErrorAction SilentlyContinue
        }
    }
}

# Check current Java version
Write-Host "Checking current Java version..." -ForegroundColor Yellow
$javaVersionOutput = & java -version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Java not found. Will attempt to detect and configure..." -ForegroundColor Yellow
    $installJava = $true
} else {
    # Detect Java version from output
    if ($javaVersionOutput -match 'version "(\d+(\.\d+)*)') {
        $detectedVersion = $matches[1]
        # Extract major version
        $majorVersion = $detectedVersion -split '\.' | Select-Object -First 1
        Write-Host "Detected Java version: $detectedVersion (major: $majorVersion)" -ForegroundColor Green

        if ([int]$majorVersion -ge 22) {
            Write-Host "Java $majorVersion detected. Java 21 is recommended for compatibility." -ForegroundColor Yellow
            $installJava = $true
        } else {
            Write-Host "Java version is compatible." -ForegroundColor Green
            $installJava = $false
        }
    } else {
        Write-Host "Could not parse Java version. Proceeding with detection..." -ForegroundColor Yellow
        $installJava = $true
    }
}

# Install Java 21 if needed
if ($installJava) {
    $javaInstallerUrl = "https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.exe"
    $javaInstallerPath = "$env:TEMP\jdk21.exe"
    Write-Host "Downloading Java 21 installer..." -ForegroundColor Yellow

    try {
        Invoke-WebRequest -Uri $javaInstallerUrl -OutFile $javaInstallerPath -ErrorAction Stop
        Write-Host "Download successful." -ForegroundColor Green

        Write-Host "Installing Java 21 (this may take a few minutes)..." -ForegroundColor Yellow
        $process = Start-Process -FilePath $javaInstallerPath -ArgumentList "/s" -Wait -PassThru

        if ($process.ExitCode -eq 0) {
            Write-Host "Java 21 installed successfully!" -ForegroundColor Green
        } else {
            Write-Error "Java installation failed with exit code: $($process.ExitCode)"
            Write-Host "Please install Java 21 manually from: https://adoptium.net/temurin/releases/?version=21" -ForegroundColor Yellow
        }
    } catch {
        Write-Error "Download failed: $_"
        Write-Host "Please download Java 21 manually from: https://adoptium.net/temurin/releases/?version=21" -ForegroundColor Yellow
    }
}

# Find all installed JDKs under Program Files
Write-Host "Detecting installed JDKs..." -ForegroundColor Yellow
$javaPaths = @()
$searchPaths = @("C:\Program Files\", "C:\Program Files (x86)\", "C:\Program Files\Java\", "C:\Program Files\Eclipse Adoptium\")

foreach ($searchPath in $searchPaths) {
    if (Test-Path $searchPath) {
        $javaPaths += Get-ChildItem $searchPath -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -like "jdk*" }
    }
}

if ($javaPaths.Count -eq 0) {
    Write-Host "No JDK installations found automatically." -ForegroundColor Red
    Write-Host "Please install Java 21 manually." -ForegroundColor Yellow
} else {
    # Pick the highest version (prioritize Java 21)
    $jdk21 = $javaPaths | Where-Object { $_.Name -match "jdk-?21" } | Select-Object -First 1
    if ($jdk21) {
        $jdk = $jdk21
        Write-Host "Found Java 21 at: $($jdk.FullName)" -ForegroundColor Green
    } else {
        $jdk = $javaPaths | Sort-Object Name -Descending | Select-Object -First 1
        Write-Host "Java 21 not found. Using highest version at: $($jdk.FullName)" -ForegroundColor Yellow
    }

    Write-Host "Setting JAVA_HOME to $($jdk.FullName)" -ForegroundColor Yellow
    $env:JAVA_HOME = $jdk.FullName
    setx JAVA_HOME $jdk.FullName | Out-Null

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ JAVA_HOME environment variable set successfully." -ForegroundColor Green
    } else {
        Write-Error "Failed to set JAVA_HOME environment variable."
    }

    $env:PATH = "$($jdk.FullName)\bin;$env:PATH"
    Write-Host "PATH updated for current session." -ForegroundColor Green
}

# Detect Gradle wrapper in any subdirectory
Write-Host "Searching for Gradle wrapper..." -ForegroundColor Yellow
$gradleWrapper = Get-ChildItem -Path . -Filter "gradlew.bat" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
if ($gradleWrapper) {
    Write-Host "Gradle wrapper found at: $($gradleWrapper.DirectoryName)" -ForegroundColor Green
    $originalLocation = Get-Location
    $projectPath = $gradleWrapper.DirectoryName
    Set-Location $projectPath

    # Detect project type
    if (Test-Path "$projectPath\pom.xml") {
        Write-Host "Maven project detected." -ForegroundColor Cyan

        Write-Host "Building Maven project..." -ForegroundColor Yellow
        try {
            $mavenOutput = & mvn clean install 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Maven build completed successfully!" -ForegroundColor Green
                $mavenOutput | Select-String -Pattern "BUILD SUCCESS" | ForEach-Object { Write-Host $_.Line -ForegroundColor Green }
            } else {
                Write-Error "Maven build failed with exit code: $LASTEXITCODE"
                Write-Host $mavenOutput -ForegroundColor Red
            }
        } catch {
            Write-Error "Maven build execution failed: $_"
        }

    } elseif (Test-Path "$projectPath\build.gradle") {
        Write-Host "Gradle project detected." -ForegroundColor Cyan

        # Upgrade Gradle wrapper
        Write-Host "Upgrading Gradle wrapper to latest version (8.7)..." -ForegroundColor Yellow
        try {
            & .\gradlew.bat wrapper --gradle-version 8.7 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Gradle wrapper upgraded to 8.7." -ForegroundColor Green
            } else {
                Write-Warning "Gradle wrapper upgrade returned exit code: $LASTEXITCODE"
            }
        } catch {
            Write-Error "Gradle wrapper upgrade failed: $_"
        }

        # Clean and rebuild project
        Write-Host "Cleaning and rebuilding project..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1

        try {
            $buildOutput = & .\gradlew.bat build 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Build completed successfully!" -ForegroundColor Green
                # Show summary line if available
                $buildOutput | Select-String -Pattern "BUILD SUCCESSFUL" | ForEach-Object { Write-Host $_.Line -ForegroundColor Green }
            } else {
                Write-Error "Build failed with exit code: $LASTEXITCODE"
                Write-Host $buildOutput -ForegroundColor Red
            }
        } catch {
            Write-Error "Build execution failed: $_"
        }

    } else {
        Write-Host "Unknown project type in $projectPath" -ForegroundColor Yellow
    }

    Set-Location $originalLocation
} else {
    Write-Host "Gradle wrapper not found. Consider creating one or installing Gradle globally." -ForegroundColor Yellow
}

Write-Host "=== Setup Complete ===" -ForegroundColor Cyan
