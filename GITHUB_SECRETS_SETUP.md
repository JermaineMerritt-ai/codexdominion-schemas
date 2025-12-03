# GitHub Repository Secrets Setup Guide

This document lists all required GitHub repository secrets for Codex Dominion workflows to function properly.

## 🔐 Required Secrets by Category

### 1. Deployment Secrets (VPS/Server)
Required for: `codex-deployment.yaml`, `codex-dual-deployment.yaml`, `super-action-ai.yaml`

- **`VPS_HOST`** - Your VPS server hostname or IP address (e.g., `98.19.211.133`)
- **`VPS_USER`** - SSH username for VPS access (e.g., `root` or `ubuntu`)
- **`VPS_KEY`** - Private SSH key for VPS authentication (full PEM format)

### 2. IONOS Cloud Secrets
Required for: `terraform-plan.yml`

- **`IONOS_USERNAME`** - IONOS Cloud API username/email
- **`IONOS_PASSWORD`** - IONOS Cloud API password
- **`IONOS_TOKEN`** - IONOS Cloud API token (if using token-based auth)

### 3. Azure Container Registry
Required for: `docker-build-push.yml`

- **`ACR_LOGIN_SERVER`** - Azure Container Registry login server (e.g., `codexdominion.azurecr.io`)
- **`AZURE_CREDENTIALS`** - Azure service principal credentials (JSON format)

### 4. Super Action AI
Required for: `super-action-ai-deployment.yaml`

- **`SUPER_AI_TOKEN`** - Authentication token for Super Action AI service
- **`DEPLOY_URL`** - Deployment target URL for AI services

### 5. AWS Credentials
Required for: `super-action-ai-deployment.yaml` and various deployment workflows

- **`AWS_ACCESS_KEY_ID`** - AWS IAM access key ID
- **`AWS_SECRET_ACCESS_KEY`** - AWS IAM secret access key
- **`AWS_REGION`** - AWS region (e.g., `us-east-1`)

### 6. Schema & Code Validation
Required for: `multi-schemas-check.yml`, `multi-repo-schema-validation.yml`, `go-live-hygiene-sweep.yml`, `multi-repo-hygiene-sweep.yml`

- **`CODE_DEPEND_ON_SCHEMAS`** - Set to `"true"` to enable schema validation checks

### 7. Notifications & Monitoring
Optional but recommended:

- **`SLACK_WEBHOOK_URL`** - Slack webhook URL for deployment notifications
- **`DISCORD_WEBHOOK_URL`** - Discord webhook URL for alerts

### 8. Additional Integration Secrets

- **`CLOUDFLARE_API_TOKEN`** - Cloudflare API token (may already be in terraform.tfvars)
- **`GCP_SERVICE_ACCOUNT_KEY`** - Google Cloud Platform service account key (JSON)
- **`GITHUB_TOKEN`** - Automatically provided by GitHub Actions (no setup needed)

---

## 📝 How to Add Secrets

### Via GitHub Web Interface:

1. Navigate to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Enter the **Name** (exactly as listed above)
5. Enter the **Value** (sensitive data)
6. Click **Add secret**

### Via GitHub CLI:

```bash
# Install GitHub CLI if needed: https://cli.github.com/

# Authenticate
gh auth login

# Add a secret
gh secret set SECRET_NAME --body "secret-value"

# Add a secret from a file (e.g., SSH key)
gh secret set VPS_KEY < ~/.ssh/vps_private_key

# Add multiline secret (e.g., Azure credentials)
gh secret set AZURE_CREDENTIALS < azure-credentials.json
```

---

## 🔍 Verify Secrets Are Set

Run this command to list all secrets (values are hidden):

```bash
gh secret list
```

---

## 🚨 Security Best Practices

1. **Never commit secrets to Git** - Use `.gitignore` for sensitive files
2. **Rotate credentials regularly** - Update secrets every 90 days
3. **Use least privilege** - Grant only necessary permissions
4. **Monitor secret usage** - Review workflow runs for unauthorized access
5. **Use environment-specific secrets** - Separate prod/dev/staging secrets

---

## 📋 Current Status

| Secret Name | Required For | Status |
|-------------|--------------|--------|
| VPS_HOST | Deployments | ⚠️ Not configured |
| VPS_USER | Deployments | ⚠️ Not configured |
| VPS_KEY | Deployments | ⚠️ Not configured |
| IONOS_USERNAME | Terraform | ⚠️ Not configured |
| IONOS_PASSWORD | Terraform | ⚠️ Not configured |
| ACR_LOGIN_SERVER | Docker | ⚠️ Not configured |
| SUPER_AI_TOKEN | AI Services | ⚠️ Not configured |
| DEPLOY_URL | AI Services | ⚠️ Not configured |
| AWS_ACCESS_KEY_ID | AWS Services | ⚠️ Not configured |
| AWS_SECRET_ACCESS_KEY | AWS Services | ⚠️ Not configured |
| CODE_DEPEND_ON_SCHEMAS | Schema Validation | ⚠️ Not configured |
| GITHUB_TOKEN | All Workflows | ✅ Auto-provided |

---

## 🛠️ Quick Setup Script

Save this as `setup-secrets.sh` and run it:

```bash
#!/bin/bash

# VPS Deployment
gh secret set VPS_HOST --body "98.19.211.133"
gh secret set VPS_USER --body "root"
gh secret set VPS_KEY < ~/.ssh/vps_key

# IONOS Cloud
gh secret set IONOS_USERNAME --body "your-ionos-email@example.com"
gh secret set IONOS_PASSWORD --body "your-ionos-password"

# Azure Container Registry
gh secret set ACR_LOGIN_SERVER --body "codexdominion.azurecr.io"
gh secret set AZURE_CREDENTIALS < azure-credentials.json

# Super Action AI
gh secret set SUPER_AI_TOKEN --body "your-super-ai-token"
gh secret set DEPLOY_URL --body "https://your-deploy-url.com"

# AWS
gh secret set AWS_ACCESS_KEY_ID --body "AKIAIOSFODNN7EXAMPLE"
gh secret set AWS_SECRET_ACCESS_KEY --body "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
gh secret set AWS_REGION --body "us-east-1"

# Schema Validation
gh secret set CODE_DEPEND_ON_SCHEMAS --body "true"

echo "✅ All secrets configured!"
```

Make it executable and run:
```bash
chmod +x setup-secrets.sh
./setup-secrets.sh
```

---

## 📞 Support

If you encounter issues setting up secrets:
1. Check GitHub Actions workflow logs for specific error messages
2. Verify secret names match exactly (case-sensitive)
3. Ensure values are properly formatted (no extra whitespace)
4. Test with workflow_dispatch trigger before production use

---

**Last Updated**: December 2, 2025
