#!/usr/bin/env bash

# Exit immediately if a command fails
set -e

# Define paths
JAVA_HOME="/home/youruser/openJdk-25"   # Change this to your JDK 25 path
PROJECT_PATH="/home/youruser/codex-dominion/codexdominion-schemas/templates/kubernetes-ovh-java"
LOG_FILE="$PROJECT_PATH/build-log.txt"

# Update PATH for Java
export JAVA_HOME
export PATH="$JAVA_HOME/bin:$PATH"

# Navigate to project directory
cd "$PROJECT_PATH"

# Start logging
echo "Build started at $(date)" > "$LOG_FILE"
echo "Starting Maven build..."

# Check Maven installation
if ! command -v mvn &> /dev/null; then
    echo "❌ Maven is not installed. Please install Maven first."
    exit 1
fi

# Run Maven build with profiles
MVN_CMD="mvn clean install -Pskip-tests,native-access --no-transfer-progress --fail-at-end"
echo "Executing: $MVN_CMD"
if $MVN_CMD | tee -a "$LOG_FILE"; then
    echo "✅ Build completed successfully!" | tee -a "$LOG_FILE"
else
    echo "❌ Build failed. Check $LOG_FILE for details." | tee -a "$LOG_FILE"
    exit 1
fi

echo "Log saved to: $LOG_FILE"
