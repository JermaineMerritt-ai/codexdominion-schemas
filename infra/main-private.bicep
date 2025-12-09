// =============================================================================
// Codex Dominion - Azure Infrastructure as Code (Bicep)
// =============================================================================
// Minimal deployment - only data services (no compute quota needed)

targetScope = 'resourceGroup'

// =============================================================================
// Parameters
// =============================================================================

param baseName string = 'codex'
param location string = 'eastus'

param pgAdminUser string = 'pgadmin'
@secure()
param pgAdminPassword string
param pgDbName string = 'codexdb'
param pgName string = '${baseName}-pg'
param pgVersion string = '14'

param redisName string = '${baseName}-redis'
param redisSku string = 'Basic'

param keyVaultName string = '${baseName}-kv'
param appInsightsName string = '${baseName}-insights'
param acrName string = '${baseName}acr'

// =============================================================================
// Resources - Data Services Only (No Compute Quota Required)
// =============================================================================

resource postgres 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
  name: pgName
  location: location
  properties: {
    administratorLogin: pgAdminUser
    administratorLoginPassword: pgAdminPassword
    version: pgVersion
    storage: {
      storageSizeGB: 32
    }
  }
}

resource redis 'Microsoft.Cache/Redis@2023-08-01' = {
  name: redisName
  location: location
  properties: {
    sku: {
      name: redisSku
      family: 'C'
      capacity: 0
    }
    enableNonSslPort: false
    minimumTlsVersion: '1.2'
  }
}

resource kv 'Microsoft.KeyVault/vaults@2022-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: {
      name: 'standard'
      family: 'A'
    }
    accessPolicies: []
  }
}

resource insights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
  }
}

resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: acrName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
}

// =============================================================================
// Outputs
// =============================================================================

output postgresHost string = '${pgName}.postgres.database.azure.com'
output redisHost string = '${redisName}.redis.cache.windows.net'
output keyVaultUri string = kv.properties.vaultUri
output acrLoginServer string = acr.properties.loginServer
