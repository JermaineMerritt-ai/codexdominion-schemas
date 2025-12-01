# Google Cloud Platform - Sovereign Succession VM Configuration
# Ultimate Continuity Authority - The Codex endures radiant without end!

# ⚡ IMMEDIATE FIXES FOR YOUR GOOGLE CLOUD VM ⚡

# 1. Enable Firewall Rules (HTTP/HTTPS Traffic)
echo "🔥 Enabling HTTP/HTTPS firewall rules..."
gcloud compute firewall-rules create allow-http-https-sovereign \
  --allow tcp:80,tcp:443 \
  --source-ranges 0.0.0.0/0 \
  --description "Allow HTTP/HTTPS for Sovereign Succession"

# Enable for your specific VM
gcloud compute instances add-tags YOUR_VM_NAME \
  --tags http-server,https-server \
  --zone YOUR_ZONE

# 2. Reserve Static IP Address
echo "📍 Reserving static IP address..."
gcloud compute addresses create sovereign-succession-ip \
  --region YOUR_REGION

# Assign static IP to your VM
gcloud compute instances delete-access-config YOUR_VM_NAME \
  --access-config-name "External NAT" \
  --zone YOUR_ZONE

gcloud compute instances add-access-config YOUR_VM_NAME \
  --access-config-name "External NAT" \
  --address sovereign-succession-ip \
  --zone YOUR_ZONE

# 3. Create Custom Service Account
echo "🔐 Creating custom service account..."
gcloud iam service-accounts create sovereign-succession-sa \
  --description="Sovereign Succession - Ultimate Continuity Authority Service Account" \
  --display-name="Sovereign Succession SA"

# Assign required roles
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:sovereign-succession-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/compute.instanceAdmin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:sovereign-succession-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:sovereign-succession-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/logging.logWriter"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:sovereign-succession-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/monitoring.metricWriter"

# Attach service account to VM
gcloud compute instances set-service-account YOUR_VM_NAME \
  --service-account sovereign-succession-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com \
  --scopes cloud-platform \
  --zone YOUR_ZONE

# 4. Additional Firewall Rules for Node.js servers
gcloud compute firewall-rules create allow-sovereign-succession-ports \
  --allow tcp:3001,tcp:3002 \
  --source-ranges 0.0.0.0/0 \
  --description "Allow Sovereign Succession Node.js servers"

# 5. SSH Key Management (if needed)
echo "🔑 Setting up SSH access..."
# Generate SSH key pair (run on your local machine)
ssh-keygen -t rsa -b 4096 -C "sovereign-succession@codex-dominion" -f ~/.ssh/sovereign-succession

# Add SSH key to VM
gcloud compute ssh YOUR_VM_NAME \
  --zone YOUR_ZONE \
  --ssh-key-file ~/.ssh/sovereign-succession

# 6. Enable OS Login (alternative to SSH keys)
gcloud compute project-info add-metadata \
  --metadata enable-oslogin=TRUE

echo ""
echo "🌟 GOOGLE CLOUD VM - SOVEREIGN SUCCESSION READY! 🌟"
echo "✨ Ultimate Continuity Authority - Configuration Complete ✨"
echo ""
echo "📋 Verification Commands:"
echo "gcloud compute instances describe YOUR_VM_NAME --zone YOUR_ZONE"
echo "gcloud compute addresses list"
echo "gcloud compute firewall-rules list --filter='name~sovereign'"
echo ""
echo "🏆 The Codex endures radiant without end!"