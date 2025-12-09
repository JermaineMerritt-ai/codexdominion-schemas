# Azure Subscription Setup

Your Azure subscription requires manual setup before deployment can succeed.

## Required Actions

### 1. Register Resource Providers

Run these commands in Azure Cloud Shell or Azure CLI (requires Subscription Owner/Contributor role):

```bash
# Register required resource providers
az provider register --namespace Microsoft.DBforPostgreSQL
az provider register --namespace Microsoft.Cache
az provider register --namespace Microsoft.KeyVault
az provider register --namespace Microsoft.Insights
az provider register --namespace Microsoft.ContainerRegistry

# Check registration status
az provider show --namespace Microsoft.DBforPostgreSQL --query "registrationState"
az provider show --namespace Microsoft.Cache --query "registrationState"
az provider show --namespace Microsoft.KeyVault --query "registrationState"
az provider show --namespace Microsoft.Insights --query "registrationState"
az provider show --namespace Microsoft.ContainerRegistry --query "registrationState"
```

Wait until all show `"Registered"` status (usually takes 1-2 minutes).

### 2. Request Compute Quota (Optional - for App Service/Functions)

Your subscription currently has 0 quota for compute resources. To deploy App Service or Function Apps later:

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Subscriptions** → Select your subscription
3. Click **Usage + quotas** in left menu
4. Search for:
   - "Free VMs" or "Basic VMs" for App Service
   - "Dynamic VMs" for Azure Functions
5. Click **Request increase**
6. Request at least 1 VM quota for your preferred region (eastus)

**Current Deployment**: Uses only data services (PostgreSQL, Redis, Key Vault, ACR, Application Insights) which don't require compute quota.

## After Setup

Once resource providers are registered, re-run the GitHub Actions workflow:
- Go to Actions → "Provision Infra and Finalize Private DNS"
- Click "Run workflow"

The deployment should succeed!
