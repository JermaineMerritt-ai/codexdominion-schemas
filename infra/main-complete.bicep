// =============================================================================
// Codex Dominion - Complete Azure Infrastructure (Bicep)
// =============================================================================
// Full deployment with compute resources
// Requires quota approval for App Service and Functions

targetScope = 'resourceGroup'

// =============================================================================
// Parameters
// =============================================================================

@description('Base name prefix for resources')
param baseName string = 'codex'

@description('Azure region for most resources')
param location string = 'centralus'

@description('Azure region for Static Web App')
param swaLocation string = 'eastus2'

@description('PostgreSQL admin username')
param pgAdminUser string = 'pgadmin'

@secure()
@description('PostgreSQL admin password')
param pgAdminPassword string

@description('PostgreSQL database name')
param pgDbName string = 'codexdb'

@description('PostgreSQL server name')
param pgName string = '${baseName}-pg-centralus'

@description('PostgreSQL version')
param pgVersion string = '14'

@description('App Service Plan name')
param appServicePlanName string = '${baseName}-plan-centralus'

@description('App Service Plan SKU (B1 recommended)')
param appServiceSku string = 'B1'

@description('Backend Web App name')
param webAppName string = '${baseName}-web-centralus'

@description('Function App name')
param functionAppName string = '${baseName}-functions-centralus'

@description('Storage account name for Functions')
param storageAccountName string = '${baseName}funcstore'

@description('Static Web App name')
param swaName string = '${baseName}-frontend-centralus'

@description('Static Web App SKU')
param swaSku string = 'Free'

@description('Redis cache name')
param redisName string = '${baseName}-redis-centralus'

@description('Redis SKU')
param redisSku string = 'Basic'

@description('Key Vault name')
param keyVaultName string = '${baseName}-kv-centralus'

@description('Application Insights name')
param appInsightsName string = '${baseName}-insights-centralus'

@description('Container Registry name')
param acrName string = '${baseName}acrwestus'

@description('Container Registry resource group')
param acrResourceGroup string = 'codex-rg'

@description('Docker image for backend')
param dockerImage string = 'codexacrwestus.azurecr.io/codex-backend:prod'

@description('Allowed CORS origins')
param allowedOrigins string = 'https://CodexDominion.app'

@description('Backend port')
param backendPort int = 8080

// =============================================================================
// Resources - Compute Layer
// =============================================================================

// App Service Plan (B1 - Basic tier)
resource plan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: appServiceSku
    tier: 'Basic'
    capacity: 1
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

// Web App for Backend Container
resource webapp 'Microsoft.Web/sites@2022-03-01' = {
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
          value: 'https://${acr.properties.loginServer}'
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_USERNAME'
          value: acr.listCredentials().username
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_PASSWORD'
          value: acr.listCredentials().passwords[0].value
        }
        {
          name: 'DATABASE_URL'
          value: 'Server=${postgres.properties.fullyQualifiedDomainName};Database=${pgDbName};User Id=${pgAdminUser};Password=${pgAdminPassword};SslMode=Require;'
        }
        {
          name: 'REDIS_HOST'
          value: redis.properties.hostName
        }
        {
          name: 'REDIS_PORT'
          value: '6380'
        }
        {
          name: 'REDIS_PASSWORD'
          value: redis.listKeys().primaryKey
        }
        {
          name: 'KEY_VAULT_URI'
          value: kv.properties.vaultUri
        }
        {
          name: 'ALLOWED_ORIGINS'
          value: allowedOrigins
        }
        {
          name: 'PORT'
          value: string(backendPort)
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: insights.properties.ConnectionString
        }
      ]
      cors: {
        allowedOrigins: [
          allowedOrigins
          'https://${swa.properties.defaultHostname}'
        ]
        supportCredentials: false
      }
    }
  }
}

// Function App (using App Service Plan)
resource functionApp 'Microsoft.Web/sites@2022-03-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp,linux'
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    siteConfig: {
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=core.windows.net'
        }
        {
          name: 'WEBSITE_CONTENTAZUREFILECONNECTIONSTRING'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=core.windows.net'
        }
        {
          name: 'WEBSITE_CONTENTSHARE'
          value: toLower(functionAppName)
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'DATABASE_URL'
          value: 'Server=${postgres.properties.fullyQualifiedDomainName};Database=${pgDbName};User Id=${pgAdminUser};Password=${pgAdminPassword};SslMode=Require;'
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: insights.properties.ConnectionString
        }
      ]
      linuxFxVersion: 'Python|3.11'
    }
  }
}

// Static Web App for Frontend
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
      appLocation: '/frontend'
      apiLocation: ''
      outputLocation: 'build'
    }
  }
}

// =============================================================================
// Resources - Data Layer
// =============================================================================

// Storage Account for Functions
resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
  }
}

// PostgreSQL Flexible Server
resource postgres 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
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
  }
}

// PostgreSQL Database
resource database 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2022-12-01' = {
  parent: postgres
  name: pgDbName
  properties: {
    charset: 'UTF8'
    collation: 'en_US.utf8'
  }
}

// PostgreSQL Firewall Rule - Allow Azure Services
resource pgFirewallAzure 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2022-12-01' = {
  parent: postgres
  name: 'AllowAzureServices'
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
      capacity: 0
    }
    enableNonSslPort: false
    minimumTlsVersion: '1.2'
    publicNetworkAccess: 'Enabled'
  }
}

// Key Vault
resource kv 'Microsoft.KeyVault/vaults@2022-07-01' = {
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
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// Container Registry (existing resource in different resource group)
resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' existing = {
  name: acrName
  scope: resourceGroup(acrResourceGroup)
}

// Key Vault Access Policies (added after resources to break circular dependency)
resource kvAccessPolicies 'Microsoft.KeyVault/vaults/accessPolicies@2022-07-01' = {
  parent: kv
  name: 'add'
  properties: {
    accessPolicies: [
      {
        tenantId: subscription().tenantId
        objectId: webapp.identity.principalId
        permissions: {
          secrets: ['get', 'list']
        }
      }
      {
        tenantId: subscription().tenantId
        objectId: functionApp.identity.principalId
        permissions: {
          secrets: ['get', 'list']
        }
      }
    ]
  }
}

// =============================================================================
// Outputs
// =============================================================================

output webAppUrl string = 'https://${webapp.properties.defaultHostName}'
output functionAppUrl string = 'https://${functionApp.properties.defaultHostName}'
output staticWebAppUrl string = 'https://${swa.properties.defaultHostname}'
output postgresHost string = postgres.properties.fullyQualifiedDomainName
output redisHost string = redis.properties.hostName
output keyVaultUri string = kv.properties.vaultUri
output acrLoginServer string = acr.properties.loginServer
output appInsightsConnectionString string = insights.properties.ConnectionString
output appInsightsInstrumentationKey string = insights.properties.InstrumentationKey
