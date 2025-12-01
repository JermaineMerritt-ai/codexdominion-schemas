@echo off
REM Set JAVA_HOME to your OpenJDK 25 path
set JAVA_HOME=C:\Users\JMerr\OneDrive\Documents\.vscode\codex_project\openJdk-25
set PATH=%JAVA_HOME%\bin;%PATH%

REM Navigate to project directory
cd C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\codexdominion-schemas\templates\kubernetes-ovh-java

REM Run Maven build with profiles
mvn clean install -Pskip-tests,native-access --no-transfer-progress --fail-at-end

pause
