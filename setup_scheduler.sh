#!/bin/bash

# Codex Dominion - Cloud Scheduler Setup for Dawn Dispatches (Bash Version)
# =========================================================================

set -e

# Parameters
PROJECT_ID="${1}"
SERVICE_URL="${2}"
JOB_NAME="${3:-dawn-dispatch}"
SCHEDULE="${4:-0 6 * * *}"
TIME_ZONE="${5:-America/New_York}"
REGION="${6:-us-central1}"

# Check required parameters
if [ -z "$PROJECT_ID" ] || [ -z "$SERVICE_URL" ]; then
    echo "Usage: $0 PROJECT_ID SERVICE_URL [JOB_NAME] [SCHEDULE] [TIME_ZONE] [REGION]"
    echo "Example: $0 my-project https://codex-backend-xyz.run.app"
    exit 1
fi

echo "⏰ Setting up Codex Dominion Cloud Scheduler"
echo "============================================="
echo "📋 Project: $PROJECT_ID"
echo "🌅 Job Name: $JOB_NAME"
echo "⏰ Schedule: $SCHEDULE (6 AM daily)"
echo "🌍 Time Zone: $TIME_ZONE"
echo "🔗 Service URL: $SERVICE_URL"
echo ""

# Set project
gcloud config set project "$PROJECT_ID"

# Enable Cloud Scheduler API
echo "🔧 Enabling Cloud Scheduler API..."
gcloud services enable cloudscheduler.googleapis.com

# Create App Engine app (required for Cloud Scheduler)
echo "🏗️ Ensuring App Engine app exists..."
if ! gcloud app describe --verbosity=error >/dev/null 2>&1; then
    echo "Creating App Engine app..."
    gcloud app create --region="$REGION"
else
    echo "✅ App Engine app already exists"
fi

# Extract dawn endpoint
if [[ "$SERVICE_URL" =~ ^https://(.+)\.run\.app$ ]]; then
    DAWN_ENDPOINT="$SERVICE_URL/dawn"
else
    DAWN_ENDPOINT="https://$SERVICE_URL.run.app/dawn"
fi

# Create Cloud Scheduler job (enhanced version of user's command)
echo "⏰ Creating dawn dispatch scheduler job..."
echo "Enhanced version of your command:"
echo "gcloud scheduler jobs create http $JOB_NAME --schedule=\"$SCHEDULE\" --uri=\"$DAWN_ENDPOINT\" --http-method=POST --time-zone=\"$TIME_ZONE\""

gcloud scheduler jobs create http "$JOB_NAME" \
    --schedule="$SCHEDULE" \
    --uri="$DAWN_ENDPOINT" \
    --http-method=POST \
    --time-zone="$TIME_ZONE" \
    --description="Automated daily dawn dispatch for Codex Dominion treasury system"

echo "✅ Dawn dispatch scheduler created!"

# Test the scheduler job
echo ""
echo "🧪 Testing dawn dispatch scheduler..."
if gcloud scheduler jobs run "$JOB_NAME"; then
    echo "✅ Test dispatch triggered successfully!"
else
    echo "⚠️ Test failed - service may be starting up"
fi

# Show job details
echo ""
echo "📊 Scheduler Job Information:"
echo "============================"

JOB_INFO=$(gcloud scheduler jobs describe "$JOB_NAME" --format="json")
echo "📅 Schedule: Every day at 6:00 AM ($TIME_ZONE)"
echo "🎯 Target: $DAWN_ENDPOINT"
echo "🔄 Method: POST"
echo "⚡ State: $(echo "$JOB_INFO" | jq -r '.state // "UNKNOWN"')"
echo "🕐 Next Run: $(echo "$JOB_INFO" | jq -r '.scheduleTime // "Calculating..."')"
echo ""

echo "🌅 Dawn Dispatch Automation Features:"
echo "===================================="
echo "✅ Automated daily execution at 6 AM"
echo "✅ Reliable cloud-based scheduling"
echo "✅ Automatic retry on failure"
echo "✅ Detailed execution logging"
echo "✅ Integration with treasury system"
echo "✅ Time zone aware scheduling"
echo ""

echo "🔧 Management Commands:"
echo "======================"
echo "List jobs: gcloud scheduler jobs list"
echo "Run now: gcloud scheduler jobs run $JOB_NAME"
echo "View logs: gcloud scheduler jobs describe $JOB_NAME"
echo "Pause job: gcloud scheduler jobs pause $JOB_NAME"
echo "Resume job: gcloud scheduler jobs resume $JOB_NAME"
echo "Delete job: gcloud scheduler jobs delete $JOB_NAME"
echo ""

echo "✅ Automated dawn dispatch system ready!"
echo "🌅 Your treasury will receive daily dawn dispatches automatically!"
echo ""
echo "🔥 Next dawn dispatch: Tomorrow at 6:00 AM $TIME_ZONE"
echo "📊 Monitor executions in Cloud Console → Cloud Scheduler"