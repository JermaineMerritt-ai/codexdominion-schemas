// =============================================================================
// Codex Dominion - Azure Infrastructure as Code (Bicep)
// =============================================================================
// Simplified deployment for development/testing

targetScope = 'resourceGroup'

// =============================================================================
// Parameters
// =============================================================================

param baseName string = 'codex'
param location string = 'eastus'
param swaLocation string = 'eastus2'

param pgAdminUser string = 'pgadmin'
@secure()
param pgAdminPassword string
param pgDbName string = 'codexdb'
param pgName string = '${baseName}-pg'
param pgVersion string = '14'

param appServicePlanName string = '${baseName}-plan'
param appServiceSku string = 'B1'
param webAppName string = '${baseName}-backend-app'

param swaName string = '${baseName}-frontend'
param swaSku string = 'Free'

param redisName string = '${baseName}-redis'
param redisSku string = 'Basic'
param redisSize string = 'c0'

param keyVaultName string = '${baseName}-kv'
param appInsightsName string = '${baseName}-insights'
param acrName string = '${baseName}acr'
param dockerImage string
param allowedOrigins string = 'https://CodexDominion.app'
param backendPort int = 8080

// =============================================================================
// Resources
// =============================================================================

resource plan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: appServiceSku
    tier: 'Basic'
  }
}

resource webapp 'Microsoft.Web/sites@2022-03-01' = {
  name: webAppName
  location: location
  properties: {
    serverFarmId: plan.id
    siteConfig: {
      linuxFxVersion: 'DOCKER|${dockerImage}'
      appSettings: [
        {
          name: 'DATABASE_URL'
          value: 'Server=${pgName}.postgres.database.azure.com;Database=${pgDbName};User Id=${pgAdminUser};Password=${pgAdminPassword};'
        }
        {
          name: 'ALLOWED_ORIGINS'
          value: allowedOrigins
        }
        {
          name: 'PORT'
          value: string(backendPort)
        }
      ]
    }
  }
}

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
      capacity: int(redisSize[1])
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

resource swa 'Microsoft.Web/staticSites@2022-03-01' = {
  name: swaName
  location: swaLocation
  sku: {
    name: swaSku
    tier: 'Free'
  }
  properties: {
    repositoryUrl: 'https://github.com/JermaineMerritt-ai/Codex-Dominion'
    branch: 'main'
    buildProperties: {
      appLocation: '/'
      apiLocation: 'api'
      outputLocation: 'build'
    }
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

output webAppUrl string = 'https://${webAppName}.azurewebsites.net'
output staticWebAppUrl string = 'https://${swaName}.azurestaticapps.net'
