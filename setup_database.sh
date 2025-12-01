#!/bin/bash
# Codex Dominion - Google Cloud SQL PostgreSQL Setup (Bash)
# ==========================================================
# Complete database infrastructure for your treasury system

set -e

PROJECT_ID="${1}"
INSTANCE_NAME="${2:-codex-ledger}"
DATABASE_NAME="${3:-codex}"
USERNAME="${4:-codex_user}"
PASSWORD="${5:-codex_pass}"
REGION="${6:-us-central1}"

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Usage: ./setup_database.sh PROJECT_ID [INSTANCE_NAME] [DATABASE_NAME] [USERNAME] [PASSWORD] [REGION]"
    echo "   Example: ./setup_database.sh my-project codex-ledger codex codex_user codex_pass us-central1"
    exit 1
fi

echo "🗄️ Setting up Codex Dominion PostgreSQL Infrastructure"
echo "===================================================="
echo "📋 Project: $PROJECT_ID"
echo "🏢 Instance: $INSTANCE_NAME"
echo "🗃️ Database: $DATABASE_NAME"
echo "👤 User: $USERNAME"
echo "🌍 Region: $REGION"
echo ""

# Set project
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling Google Cloud SQL APIs..."
gcloud services enable sqladmin.googleapis.com
gcloud services enable sql-component.googleapis.com

# Create PostgreSQL instance (your exact commands)
echo "🏗️ Creating PostgreSQL instance..."
echo "Command: gcloud sql instances create $INSTANCE_NAME --database-version=POSTGRES_15 --tier=db-f1-micro --region=$REGION"

gcloud sql instances create $INSTANCE_NAME \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=$REGION

echo "✅ PostgreSQL instance created!"

# Create database (your exact command)
echo "🗃️ Creating database..."
echo "Command: gcloud sql databases create $DATABASE_NAME --instance=$INSTANCE_NAME"

gcloud sql databases create $DATABASE_NAME \
  --instance=$INSTANCE_NAME

echo "✅ Database created!"

# Create user (your exact command)
echo "👤 Creating database user..."
echo "Command: gcloud sql users create $USERNAME --instance=$INSTANCE_NAME --password=$PASSWORD"

gcloud sql users create $USERNAME \
  --instance=$INSTANCE_NAME \
  --password=$PASSWORD

echo "✅ Database user created!"

# Get connection info
echo ""
echo "📊 Database Connection Information:"
echo "================================="

CONNECTION_NAME=$(gcloud sql instances describe $INSTANCE_NAME --format="value(connectionName)")
IP_ADDRESS=$(gcloud sql instances describe $INSTANCE_NAME --format="value(ipAddresses[0].ipAddress)")

echo "🔌 Connection Name: $CONNECTION_NAME"
echo "🌐 IP Address: $IP_ADDRESS"
echo "🗃️ Database: $DATABASE_NAME"
echo "👤 Username: $USERNAME"
echo "🔑 Password: $PASSWORD"
echo ""

# Create connection string for Cloud Run
CLOUD_RUN_CONNECTION_STRING="postgresql://$USERNAME:$PASSWORD@/$DATABASE_NAME?host=/cloudsql/$CONNECTION_NAME"

echo "🚀 Cloud Run Configuration:"
echo "==========================="
echo "Environment Variables to add to your Cloud Run deployment:"
echo ""
echo "DATABASE_URL=$CLOUD_RUN_CONNECTION_STRING"
echo "INSTANCE_CONNECTION_NAME=$CONNECTION_NAME"
echo "DB_USER=$USERNAME"
echo "DB_PASS=$PASSWORD"
echo "DB_NAME=$DATABASE_NAME"
echo ""

# Update deployment command
echo "📝 Updated Deployment Command:"
echo "============================="
echo "Use this enhanced command to deploy with PostgreSQL:"
echo ""
echo "gcloud run deploy codex-dashboard \\"
echo "  --image gcr.io/$PROJECT_ID/codex-dashboard \\"
echo "  --platform managed \\"
echo "  --region $REGION \\"
echo "  --allow-unauthenticated \\"
echo "  --memory 512Mi \\"
echo "  --cpu 1 \\"
echo "  --add-cloudsql-instances $CONNECTION_NAME \\"
echo "  --set-env-vars \"DATABASE_URL=$CLOUD_RUN_CONNECTION_STRING,INSTANCE_CONNECTION_NAME=$CONNECTION_NAME\""
echo ""

echo "✅ PostgreSQL infrastructure ready!"
echo "💰 Your treasury system can now use enterprise-grade PostgreSQL!"
echo ""
echo "🔥 Next steps:"
echo "1. Deploy your application with the updated command above"
echo "2. Your \$5,125.48 treasury will automatically migrate to PostgreSQL"
echo "3. Enjoy enterprise-grade database reliability!"