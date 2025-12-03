# Random Java Project

## Issue Resolution: Java Version Compatibility

### Problem
- Original error: `Unsupported class file major version 69`
- Cause: Java 25 was installed, but Gradle 8.11.1 only supports up to Java 23

### Solution
1. Downloaded and installed portable Java 21 LTS to `C:\Java\jdk-21.0.5+11`
2. Updated `gradle.properties` to use Java 21:
   ```properties
   org.gradle.java.home=C:\\Java\\jdk-21.0.5+11
   ```
3. Set Java compatibility in `build.gradle`:
   ```gradle
   java {
       sourceCompatibility = JavaVersion.VERSION_21
       targetCompatibility = JavaVersion.VERSION_21
   }
   ```

### Building the Project
```powershell
$env:JAVA_HOME = "C:\Java\jdk-21.0.5+11"
.\gradlew.bat clean build
```

### Running the Application
```powershell
$env:JAVA_HOME = "C:\Java\jdk-21.0.5+11"
.\gradlew.bat run
```

## Permanent Fix (Optional)
To avoid setting `JAVA_HOME` every time, add it to your system environment variables:
1. Open System Properties > Environment Variables
2. Add/update `JAVA_HOME` = `C:\Java\jdk-21.0.5+11`
3. Restart VS Code/IDE

## Project Structure
```
random-java/
├── src/main/java/com/codexdominion/
│   └── Main.java
├── build.gradle
├── settings.gradle
├── gradle.properties
└── gradle/wrapper/
```

## Gradle Version
- Gradle: 8.11.1
- Java: 21.0.5 (LTS)
