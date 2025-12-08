# Post-Deployment Verification Guide

This guide provides commands to verify your Azure infrastructure after deployment.

## Prerequisites

- Infrastructure deployed via `deploy-private-infrastructure.yml` workflow
- DNS records populated (automatic in workflow)
- App Service running with VNet integration

## 1. Verify Private DNS Records (From Local Machine)

```bash
# Check if DNS A records exist and show their IPs
az network private-dns record-set a show -g codex-rg \
  -z privatelink.postgres.database.azure.com -n codex-pg

az network private-dns record-set a show -g codex-rg \
  -z privatelink.redis.cache.windows.net -n codex-redis

az network private-dns record-set a show -g codex-rg \
  -z privatelink.vaultcore.azure.net -n codex-kv
```

**Expected Output:** Each should show an IP address like `10.10.2.x`

## 2. SSH into App Service

```bash
# Open interactive SSH session to App Service
az webapp ssh --name codex-backend-app --resource-group codex-rg
```

## 3. Test DNS Resolution (Inside App Service SSH)

Once connected via SSH, run these commands:

```bash
# Check DNS resolution inside App Service
nslookup codex-pg.postgres.database.azure.com
# Expected: 10.10.2.x (private IP)

nslookup codex-redis.redis.cache.windows.net
# Expected: 10.10.2.y (private IP)

nslookup codex-kv.vaultcore.azure.net
# Expected: 10.10.2.z (private IP)
```

**What to look for:**
- ✅ Should return private IP addresses (10.10.2.x range)
- ❌ If returns public IP or no result, DNS configuration failed

## 4. Test PostgreSQL Connectivity (Inside App Service SSH)

```bash
# Install psql client if not present
apt-get update && apt-get install -y postgresql-client

# Test PostgreSQL connectivity (replace password if needed)
PG_CONN="postgresql://codexadmin:${PG_ADMIN_PASSWORD}@codex-pg.postgres.database.azure.com:5432/codexdb?sslmode=require"
psql "$PG_CONN" -c '\l'   # lists databases
psql "$PG_CONN" -c 'SELECT version();'   # shows PostgreSQL version
```

**Expected:** Should connect successfully and list databases

## 5. Test Redis Connectivity (Inside App Service SSH)

```bash
# Install redis-cli if not present
apt-get install -y redis-tools

# Test Redis connectivity
redis-cli -u $REDIS_URL ping
# Expected: PONG

# Test set/get
redis-cli -u $REDIS_URL SET test "Hello from VNet"
redis-cli -u $REDIS_URL GET test
# Expected: "Hello from VNet"
```

## 6. Verify Key Vault Secret Resolution (Inside App Service SSH)

```bash
# App Service should automatically resolve Key Vault references
echo $DATABASE_URL
# Expected: Full PostgreSQL connection string from Key Vault

echo $REDIS_URL
# Expected: Full Redis connection string from Key Vault

# Check if secrets are properly loaded (not showing @Microsoft.KeyVault)
env | grep -E 'DATABASE_URL|REDIS_URL'
```

**What to look for:**
- ✅ Actual secret values (not `@Microsoft.KeyVault(SecretUri=...)`)
- ❌ If still shows `@Microsoft.KeyVault`, managed identity or access policy failed

## 7. Test Application Health Endpoint

```bash
# From local machine
curl https://codex-backend-app.azurewebsites.net/health

# From inside App Service SSH
curl http://localhost:8000/health
```

**Expected:** JSON response with status information

## 8. Check VNet Integration Status

```bash
# From local machine
az webapp vnet-integration list \
  --name codex-backend-app \
  --resource-group codex-rg
```

**Expected:** Should show integration with `codex-vnet` subnet

## 9. Verify Private Endpoint Status

```bash
# Check private endpoint provisioning state
az network private-endpoint show \
  --name codex-pg-pe \
  --resource-group codex-rg \
  --query provisioningState

az network private-endpoint show \
  --name codex-redis-pe \
  --resource-group codex-rg \
  --query provisioningState

az network private-endpoint show \
  --name codex-kv-pe \
  --resource-group codex-rg \
  --query provisioningState
```

**Expected:** All should return `"Succeeded"`

## 10. Check Application Insights Telemetry

```bash
# Get recent traces
az monitor app-insights query \
  --app codex-insights \
  --resource-group codex-rg \
  --analytics-query "traces | take 10 | project timestamp, message"
```

## Troubleshooting

### DNS Not Resolving to Private IP

```bash
# Check DNS zone VNet link
az network private-dns link vnet list \
  --resource-group codex-rg \
  --zone-name privatelink.postgres.database.azure.com

# Re-run DNS finalizer workflow if needed
```

### PostgreSQL Connection Timeout

```bash
# Check firewall rules (should be none for private endpoint)
az postgres flexible-server firewall-rule list \
  --resource-group codex-rg \
  --name codex-pg

# Verify private endpoint connection
az postgres flexible-server show \
  --resource-group codex-rg \
  --name codex-pg \
  --query network
```

### Key Vault Access Denied

```bash
# Check App Service managed identity
az webapp identity show \
  --name codex-backend-app \
  --resource-group codex-rg

# Check Key Vault access policies
az keyvault show \
  --name <your-kv-name> \
  --resource-group codex-rg \
  --query properties.accessPolicies
```

### App Service Not Starting

```bash
# Check logs
az webapp log tail \
  --name codex-backend-app \
  --resource-group codex-rg

# Check container logs
az webapp log show \
  --name codex-backend-app \
  --resource-group codex-rg
```

## Success Criteria

✅ All DNS queries return private IPs (10.10.2.x)
✅ PostgreSQL connection successful from App Service
✅ Redis PING returns PONG
✅ Key Vault secrets resolved in environment variables
✅ Application health endpoint returns 200 OK
✅ All private endpoints show `provisioningState: "Succeeded"`
✅ VNet integration active on App Service
✅ Application Insights receiving telemetry

## Next Steps

Once verification is complete:
1. Deploy frontend: `frontend-deploy.yml` workflow
2. Run database migrations: `db-migrate.yml` workflow
3. Test end-to-end application flow
4. Set up monitoring alerts in Azure Monitor
