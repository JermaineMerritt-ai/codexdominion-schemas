// =============================================================================
// Codex Dominion - Simplified Azure Infrastructure (Bicep)
// =============================================================================
// Basic deployment without private networking
// Use for development/testing environments

targetScope = 'resourceGroup'

// =============================================================================
// Parameters
// =============================================================================

@description('Base name prefix for resources')
param baseName string = 'codex'

@description('Azure region')
param location string = 'eastus'

@description('PostgreSQL admin username')
param pgAdminUser string = 'pgadmin'

@secure()
@description('PostgreSQL admin password')
param pgAdminPassword string

@description('PostgreSQL database name')
param pgDbName string = 'codexdb'

@description('PostgreSQL server name')
param pgName string = '${baseName}-pg'

@description('PostgreSQL version')
param pgVersion string = '14'

@description('App Service Plan name')
param appServicePlanName string = '${baseName}-plan'

@description('App Service Plan SKU')
param appServiceSku string = 'B1'

@description('Backend Web App name')
param webAppName string = '${baseName}-backend-app'

@description('Static Web App name')
param swaName string = '${baseName}-frontend'

@description('Static Web App SKU')
param swaSku string = 'Free'

@description('Redis cache name')
param redisName string = '${baseName}-redis'

@description('Redis SKU')
param redisSku string = 'Basic'

@description('Redis size')
param redisSize string = 'c0'

@description('Key Vault name')
param keyVaultName string = '${baseName}-kv'

@description('App Insights name')
param appInsightsName string = '${baseName}-insights'

@description('Container Registry name')
param acrName string = '${baseName}acr'

@description('Backend Docker image')
param dockerImage string

@description('Allowed origins for CORS')
param allowedOrigins string = 'https://CodexDominion.app'

@description('Backend port')
param backendPort int = 8080

// =============================================================================
// Resources
// =============================================================================

// App Service Plan
resource plan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: appServicePlanName
  location: location
  kind: 'linux'
  sku: {
    name: appServiceSku
    tier: (appServiceSku == 'B1' || appServiceSku == 'B2') ? 'Basic' : 'Standard'
  }
  properties: {
    reserved: true
  }
}

// Backend Web App
resource webapp 'Microsoft.Web/sites@2023-12-01' = {
  name: webAppName
  location: location
  kind: 'app,linux,container'
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'DOCKER|${dockerImage}'
      appSettings: [
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'false'
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_URL'
          value: 'https://${acrName}.azurecr.io'
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_USERNAME'
          value: acr.name
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_PASSWORD'
          value: acr.listCredentials().passwords[0].value
        }
        {
          name: 'DATABASE_URL'
          value: 'postgresql://${pgAdminUser}:${pgAdminPassword}@${pgName}.postgres.database.azure.com:5432/${pgDbName}?sslmode=require'
        }
        {
          name: 'REDIS_URL'
          value: 'rediss://:${redis.listKeys().primaryKey}@${redisName}.redis.cache.windows.net:6380'
        }
        {
          name: 'KEY_VAULT_URI'
          value: kv.properties.vaultUri
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: insights.properties.ConnectionString
        }
        {
          name: 'PORT'
          value: string(backendPort)
        }
        {
          name: 'ALLOWED_ORIGINS'
          value: allowedOrigins
        }
      ]
    }
  }
}

// PostgreSQL Flexible Server
resource postgres 'Microsoft.DBforPostgreSQL/flexibleServers@2023-03-01-preview' = {
  name: pgName
  location: location
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    administratorLogin: pgAdminUser
    administratorLoginPassword: pgAdminPassword
    version: pgVersion
    storage: {
      storageSizeGB: 32
    }
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    highAvailability: {
      mode: 'Disabled'
    }
  }
}

// PostgreSQL Database
resource pgDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2023-03-01-preview' = {
  name: pgDbName
  parent: postgres
  properties: {
    charset: 'UTF8'
    collation: 'en_US.utf8'
  }
}

// PostgreSQL Firewall Rule (allow Azure services)
resource pgFirewall 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2023-03-01-preview' = {
  name: 'AllowAzureServices'
  parent: postgres
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

// Redis Cache
resource redis 'Microsoft.Cache/Redis@2023-08-01' = {
  name: redisName
  location: location
  properties: {
    sku: {
      name: redisSku
      family: 'C'
      capacity: (redisSize == 'c0' || redisSize == 'C0') ? 0 : 1
    }
    enableNonSslPort: false
    minimumTlsVersion: '1.2'
    publicNetworkAccess: 'Enabled'
  }
}

// Key Vault
resource kv 'Microsoft.KeyVault/vaults@2023-02-01' = {
  name: keyVaultName
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: {
      name: 'standard'
      family: 'A'
    }
    enabledForTemplateDeployment: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    publicNetworkAccess: 'Enabled'
    accessPolicies: []
  }
}

// Application Insights
resource insights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    RetentionInDays: 30
  }
}

// Static Web App
resource swa 'Microsoft.Web/staticSites@2023-12-01' = {
  name: swaName
  location: location
  sku: {
    name: swaSku
    tier: swaSku
  }
  properties: {
    buildProperties: {
      appLocation: '/'
      apiLocation: 'api'
      outputLocation: 'build'
    }
  }
}

// Container Registry
resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: acrName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
    publicNetworkAccess: 'Enabled'
  }
}

// =============================================================================
// Outputs
// =============================================================================

output webAppUrl string = 'https://${webapp.properties.defaultHostName}'
output staticWebAppUrl string = 'https://${swa.properties.defaultHostname}'
output postgresHost string = '${pgName}.postgres.database.azure.com'
output redisHost string = '${redisName}.redis.cache.windows.net'
output keyVaultUri string = kv.properties.vaultUri
output acrLoginServer string = acr.properties.loginServer
output appInsightsConnectionString string = insights.properties.ConnectionString
