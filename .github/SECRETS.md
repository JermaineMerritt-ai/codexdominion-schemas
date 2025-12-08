# GitHub Secrets Configuration

This document lists the required GitHub Secrets for the CI/CD workflows.

## Required Secrets

### 1. AZURE_CREDENTIALS
Azure Service Principal credentials for authentication.

**Format:** JSON object
```json
{
  "clientId": "<SERVICE_PRINCIPAL_APP_ID>",
  "clientSecret": "<SERVICE_PRINCIPAL_PASSWORD>",
  "subscriptionId": "<AZURE_SUBSCRIPTION_ID>",
  "tenantId": "<AZURE_TENANT_ID>"
}
```

**How to create:**
```bash
az ad sp create-for-rbac \
  --name "codex-dominion-github-actions" \
  --role contributor \
  --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/codex-rg \
  --sdk-auth
```

### 2. PG_ADMIN_PASSWORD
PostgreSQL admin password for database deployments.

**Format:** String (strong password)
```
Example: MyStr0ng!P@ssw0rd#2024
```

**Requirements:**
- Minimum 8 characters
- Contains uppercase, lowercase, numbers, and special characters
- No common words or patterns

### 3. AZURE_STATIC_WEB_APPS_API_TOKEN
Deployment token for Azure Static Web Apps.

**How to get:**
1. Go to Azure Portal → Static Web Apps → codex-frontend-swa
2. Navigate to "Manage deployment token"
3. Copy the token value

**Format:** String (long alphanumeric token)

---

## Setting Secrets in GitHub

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with the exact name listed above

## Verification

After adding secrets, verify they're set correctly:

```bash
# Test Azure login
gh workflow run deploy-private-infrastructure.yml

# Check workflow logs for authentication issues
gh run list --workflow=deploy-private-infrastructure.yml
```

## Security Best Practices

- ✅ Never commit secrets to version control
- ✅ Rotate service principal credentials every 90 days
- ✅ Use separate service principals for dev/staging/prod
- ✅ Enable secret scanning in GitHub repository settings
- ✅ Limit service principal permissions to specific resource groups
- ✅ Monitor Azure Activity Logs for suspicious service principal usage

## Troubleshooting

### "Authentication failed" errors
- Verify `AZURE_CREDENTIALS` JSON format is correct
- Ensure service principal has `Contributor` role on `codex-rg`
- Check subscription ID matches your Azure subscription

### "Invalid token" for Static Web Apps
- Regenerate deployment token from Azure Portal
- Update `AZURE_STATIC_WEB_APPS_API_TOKEN` secret in GitHub

### PostgreSQL password requirements
- Must meet Azure's password complexity requirements
- Cannot contain username or parts of server name
- Use password generator for strong passwords
