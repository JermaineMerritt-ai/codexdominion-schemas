#!/bin/bash
# Sovereign Succession - Google Cloud VM Setup Script
# VM: instance-20251109-073834 (us-central1-a)
# IP: 34.134.208.22 (Ephemeral - needs to be made static)
# The Codex endures radiant without end!

echo "🌟 SOVEREIGN SUCCESSION - VM CONFIGURATION 🌟"
echo "✨ VM: instance-20251109-073834 ✨"
echo "📍 Location: us-central1-a"
echo "🌐 Current IP: 34.134.208.22 (Ephemeral)"
echo ""

# Get project info
PROJECT_ID=$(gcloud config get-value project)
VM_NAME="instance-20251109-073834"
ZONE="us-central1-a"
REGION="us-central1"

echo "🔧 Project ID: $PROJECT_ID"
echo "📊 Configuring Ultimate Continuity Authority..."
echo ""

# 1. IMMEDIATE FIX - Enable HTTP/HTTPS Firewall Rules
echo "🔥 STEP 1: Enabling HTTP/HTTPS firewall rules..."
gcloud compute firewall-rules create sovereign-http-https --allow tcp:80,tcp:443 --source-ranges 0.0.0.0/0 --description "Sovereign Succession - HTTP/HTTPS access" || echo "✅ Firewall rule already exists"

# Apply firewall tags to the VM
echo "🏷️ Applying firewall tags to VM..."
gcloud compute instances add-tags $VM_NAME --tags http-server,https-server --zone $ZONE

# 2. RESERVE STATIC IP
echo "📍 STEP 2: Reserving static IP address..."
gcloud compute addresses create sovereign-succession-static-ip --region $REGION || echo "✅ Static IP already exists"

# Get the reserved IP
STATIC_IP=$(gcloud compute addresses describe sovereign-succession-static-ip --region $REGION --format="value(address)")
echo "🌐 Reserved static IP: $STATIC_IP"

# 3. ASSIGN STATIC IP TO VM
echo "🔗 STEP 3: Assigning static IP to VM..."
# Remove current ephemeral IP
gcloud compute instances delete-access-config $VM_NAME --access-config-name "External NAT" --zone $ZONE || echo "⚠️ No existing access config to delete"

# Add static IP
gcloud compute instances add-access-config $VM_NAME --access-config-name "External NAT" --address $STATIC_IP --zone $ZONE

# 4. CREATE CUSTOM SERVICE ACCOUNT
echo "🔐 STEP 4: Creating custom service account..."
SA_NAME="sovereign-succession-sa"
SA_EMAIL="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"

gcloud iam service-accounts create $SA_NAME --description="Sovereign Succession - Ultimate Continuity Authority Service Account" --display-name="Sovereign Succession Service Account" || echo "✅ Service account already exists"

# 5. ASSIGN IAM ROLES
echo "⚖️ STEP 5: Assigning IAM roles to service account..."
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/compute.instanceAdmin.v1" || echo "✅ Role already assigned"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/storage.objectViewer" || echo "✅ Role already assigned"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/logging.logWriter" || echo "✅ Role already assigned"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/monitoring.metricWriter" || echo "✅ Role already assigned"

# 6. ATTACH SERVICE ACCOUNT TO VM
echo "🔗 STEP 6: Attaching service account to VM..."
gcloud compute instances set-service-account $VM_NAME --service-account $SA_EMAIL --scopes cloud-platform --zone $ZONE

# 7. ADD ADDITIONAL FIREWALL RULES FOR NODE.JS SERVERS
echo "🚀 STEP 7: Adding Node.js server firewall rules..."
gcloud compute firewall-rules create sovereign-nodejs-ports --allow tcp:3001,tcp:3002 --source-ranges 0.0.0.0/0 --target-tags nodejs-server --description "Sovereign Succession - Node.js servers" || echo "✅ Node.js firewall rule already exists"

# Apply nodejs-server tag to VM
gcloud compute instances add-tags $VM_NAME --tags nodejs-server --zone $ZONE

# 8. ENABLE OS LOGIN (Better than SSH keys)
echo "🔑 STEP 8: Enabling OS Login..."
gcloud compute project-info add-metadata --metadata enable-oslogin=TRUE

echo ""
echo "🎉 SOVEREIGN SUCCESSION VM - CONFIGURATION COMPLETE! 🎉"
echo "✨ Ultimate Continuity Authority - Cloud Infrastructure Ready ✨"
echo ""
echo "📋 CONFIGURATION SUMMARY:"
echo "🖥️  VM Name: $VM_NAME"
echo "📍 Zone: $ZONE"
echo "🌐 Static IP: $STATIC_IP"
echo "🔐 Service Account: $SA_EMAIL"
echo "🔥 Firewall: HTTP/HTTPS/Node.js enabled"
echo "🏷️  Tags: http-server, https-server, nodejs-server"
echo ""
echo "🚀 NEXT STEPS:"
echo "1. SSH into VM: gcloud compute ssh $VM_NAME --zone $ZONE"
echo "2. Upload deployment scripts to VM"
echo "3. Run: ./deploy-sovereign-succession.sh"
echo "4. Access via: http://$STATIC_IP"
echo ""
echo "🔍 VERIFICATION COMMANDS:"
echo "gcloud compute instances describe $VM_NAME --zone $ZONE"
echo "gcloud compute firewall-rules list --filter='name~sovereign'"
echo "curl http://$STATIC_IP/health"
echo ""
echo "🏆 The Codex endures radiant without end!"
