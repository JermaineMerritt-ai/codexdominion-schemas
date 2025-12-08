// =============================================================================
// Codex Dominion - Azure Infrastructure as Code (Bicep) - Private Network
// =============================================================================
// Enhanced security deployment with:
// - Private Endpoints for PostgreSQL, Redis, and Key Vault
// - VNet integration for App Service
// - Key Vault for secrets management (private endpoint)
// - No public database/cache/vault access
// - Private DNS zones for all services

targetScope = 'resourceGroup'

// =============================================================================
// Parameters
// =============================================================================

@description('Azure region')
param location string = 'eastus'

@description('Base name for resources')
param baseName string = 'codex'

@description('Static Web App name')
param swaName string = '${baseName}-frontend'

@description('App Service Plan name')
param appServicePlanName string = '${baseName}-plan'

@description('Web App (backend) name')
param webAppName string = '${baseName}-backend-app'

@description('Azure Container Registry name (globally unique, alphanumeric)')
param acrName string = '${baseName}acr'

@description('Docker image to deploy, e.g., codexdominionacr.azurecr.io/codex-backend:prod')
param dockerImage string

@description('PostgreSQL Flexible Server name')
param pgName string = '${baseName}-pg'

@description('PostgreSQL admin username')
param pgAdminUser string = 'codexadmin'

@secure()
@description('PostgreSQL admin password')
param pgAdminPassword string

@description('PostgreSQL version')
param pgVersion string = '16'

@description('Database name')
param pgDbName string = 'codexdb'

@description('Redis Cache name')
param redisName string = '${baseName}-redis'

@description('Application Insights name')
param appInsightsName string = '${baseName}-ai'

@description('Key Vault name')
param keyVaultName string = '${baseName}-kv'

@description('Static Web Apps SKU')
@allowed(['Free','Standard'])
param swaSku string = 'Free'

@description('App Service Plan SKU')
@allowed(['B1','B2','S1','S2'])
param appServiceSku string = 'B1'

@description('Redis SKU')
@allowed(['Basic','Standard','Premium'])
param redisSku string = 'Basic'

@description('Redis size (c0 for Basic)')
param redisSize string = 'c0'

@description('Backend container port')
param backendPort int = 8000

@description('Allowed CORS origins for backend')
param allowedOrigins string = '*'

// =============================================================================
// Variables
// =============================================================================

var acrLoginServer = '${acrName}.azurecr.io'

// =============================================================================
// Resources
// =============================================================================

// ---------------------- Observability ----------------------
resource insights 'Microsoft.Insights/components@2022-06-15' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: { Application_Type: 'web' }
}

// ---------------------- ACR ----------------------
resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: acrName
  location: location
  sku: { name: 'Basic' }
  properties: { adminUserEnabled: true }
}

// ---------------------- Static Web App ----------------------
resource swa 'Microsoft.Web/staticSites@2023-12-01' = {
  name: swaName
  location: location
  sku: { name: swaSku, tier: swaSku }
  properties: {
    buildProperties: { appLocation: 'frontend', outputLocation: '.next' }
  }
}

// ---------------------- Networking (VNet + subnets) ----------------------
resource vnet 'Microsoft.Network/virtualNetworks@2023-05-01' = {
  name: '${baseName}-vnet'
  location: location
  properties: {
    addressSpace: { addressPrefixes: [ '10.10.0.0/16' ] }
    subnets: [
      {
        name: 'appservice-integrationsubnet'
        properties: {
          addressPrefix: '10.10.1.0/24'
          delegations: [
            { name: 'appsvc-delegation', properties: { serviceName: 'Microsoft.Web/serverFarms' } }
          ]
        }
      }
      {
        name: 'private-endpointsubnet'
        properties: {
          addressPrefix: '10.10.2.0/24'
          privateEndpointNetworkPolicies: 'Disabled'
        }
      }
    ]
  }
}

var appSubnetId = '${vnet.id}/subnets/appservice-integrationsubnet'
var peSubnetId = '${vnet.id}/subnets/private-endpointsubnet'

// ---------------------- Private DNS zones ----------------------
resource dnsPg 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.postgres.database.azure.com'
  location: 'global'
}
resource dnsRedis 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.redis.cache.windows.net'
  location: 'global'
}
resource dnsKv 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.vaultcore.azure.net'
  location: 'global'
}

resource dnsPgLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  name: 'pg-vnet-link'
  parent: dnsPg
  location: 'global'
  properties: { registrationEnabled: false, virtualNetwork: { id: vnet.id } }
}
resource dnsRedisLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  name: 'redis-vnet-link'
  parent: dnsRedis
  location: 'global'
  properties: { registrationEnabled: false, virtualNetwork: { id: vnet.id } }
}
resource dnsKvLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  name: 'kv-vnet-link'
  parent: dnsKv
  location: 'global'
  properties: { registrationEnabled: false, virtualNetwork: { id: vnet.id } }
}

// ---------------------- PostgreSQL (Private only) ----------------------
resource pg 'Microsoft.DBforPostgreSQL/flexibleServers@2023-06-01-preview' = {
  name: pgName
  location: location
  sku: { name: 'B1ms', tier: 'Burstable' }
  properties: {
    version: pgVersion
    administratorLogin: pgAdminUser
    administratorLoginPassword: pgAdminPassword
    storage: { storageSizeGB: 32 }
    network: { publicNetworkAccess: 'Disabled' }
    highAvailability: { mode: 'Disabled' }
    backup: { backupRetentionDays: 7, geoRedundantBackup: 'Disabled' }
  }
}

// PostgreSQL Database
resource pgDb 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2023-03-01-preview' = {
  name: pgDbName
  parent: pg
  properties: {
    charset: 'UTF8'
    collation: 'en_US.utf8'
  }
}

// Private Endpoint for PostgreSQL
resource pgPe 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: '${baseName}-pg-pe'
  location: location
  properties: {
    subnet: { id: peSubnetId }
    privateLinkServiceConnections: [
      {
        name: 'pg-conn'
        properties: {
          privateLinkServiceId: pg.id
          groupIds: [ 'postgresqlServer' ]
          requestMessage: 'Private access to PostgreSQL'
        }
      }
    ]
  }
}

// ---------------------- Redis (Private only) ----------------------
resource redis 'Microsoft.Cache/Redis@2023-08-01' = {
  name: redisName
  location: location
  sku: { name: redisSku, family: 'C', capacity: redisSize == 'c0' ? 0 : 1 }
  properties: { enableNonSslPort: false, minimumTlsVersion: '1.2', publicNetworkAccess: 'Disabled' }
}

// Private Endpoint for Redis
resource redisPe 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: '${baseName}-redis-pe'
  location: location
  properties: {
    subnet: { id: peSubnetId }
    privateLinkServiceConnections: [
      {
        name: 'redis-conn'
        properties: {
          privateLinkServiceId: redis.id
          groupIds: [ 'redisCache' ]
          requestMessage: 'Private access to Redis'
        }
      }
    ]
  }
}

// ---------------------- Key Vault (Private endpoint + DNS) ----------------------
resource kv 'Microsoft.KeyVault/vaults@2023-02-01' = {
  name: keyVaultName
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: { name: 'standard', family: 'A' }
    enabledForTemplateDeployment: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    enablePurgeProtection: true
    publicNetworkAccess: 'Disabled'
    // accessPolicies empty; managed via RBAC/MSI + policy below
    accessPolicies: []
  }
}

// Private Endpoint for Key Vault
resource kvPe 'Microsoft.Network/privateEndpoints@2023-05-01' = {
  name: '${baseName}-kv-pe'
  location: location
  properties: {
    subnet: { id: peSubnetId }
    privateLinkServiceConnections: [
      {
        name: 'kv-conn'
        properties: {
          privateLinkServiceId: kv.id
          groupIds: [ 'vault' ]
          requestMessage: 'Private access to Key Vault'
        }
      }
    ]
  }
}

// Private DNS records: bind PE NIC IPs
// Note: Private endpoint NICs are created asynchronously; for fully deterministic A records,
// consider a post-deploy script to fetch NIC IPs and create records.
resource pgPeDns 'Microsoft.Network/privateDnsZones/A@2020-06-01' = {
  name: pgName
  parent: dnsPg
  properties: { ttl: 300, aRecords: [] }
  dependsOn: [ pgPe, dnsPgLink ]
}
resource redisPeDns 'Microsoft.Network/privateDnsZones/A@2020-06-01' = {
  name: redisName
  parent: dnsRedis
  properties: { ttl: 300, aRecords: [] }
  dependsOn: [ redisPe, dnsRedisLink ]
}
resource kvPeDns 'Microsoft.Network/privateDnsZones/A@2020-06-01' = {
  name: keyVaultName
  parent: dnsKv
  properties: { ttl: 300, aRecords: [] }
  dependsOn: [ kvPe, dnsKvLink ]
}

// ---------------------- Secrets (constructed) ----------------------
var pgConnString = 'postgresql://${pgAdminUser}:${pgAdminPassword}@${pgName}.postgres.database.azure.com:5432/${pgDbName}?sslmode=require'
var redisPrimaryKey = redis.listKeys().primaryKey
var redisUrl = 'rediss://:${redisPrimaryKey}@${redisName}.redis.cache.windows.net:6380'

resource kvSecretDatabase 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  name: 'DatabaseUrl'
  parent: kv
  properties: { value: pgConnString }
  dependsOn: [ kvPeDns ]
}
resource kvSecretRedis 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  name: 'RedisUrl'
  parent: kv
  properties: { value: redisUrl }
  dependsOn: [ kvPeDns ]
}

// ---------------------- App Service (Linux, VNet integrated) ----------------------
resource plan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: appServicePlanName
  location: location
  kind: 'linux'
  sku: {
    name: appServiceSku
    tier: (appServiceSku == 'B1' || appServiceSku == 'B2') ? 'Basic' : 'Standard'
    size: appServiceSku
    capacity: 1
  }
  properties: { reserved: true }
}

resource webapp 'Microsoft.Web/sites@2023-12-01' = {
  name: webAppName
  location: location
  kind: 'app,linux'
  identity: { type: 'SystemAssigned' }
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'DOCKER|${dockerImage}'
      vnetRouteAllEnabled: true
      appSettings: [
        { name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE', value: 'false' }
        { name: 'WEBSITES_PORT', value: string(backendPort) }
        { name: 'PORT', value: string(backendPort) }
        { name: 'APPINSIGHTS_INSTRUMENTATIONKEY', value: insights.properties.InstrumentationKey }
        { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: insights.properties.ConnectionString }
        { name: 'ALLOWED_ORIGINS', value: allowedOrigins }
        { name: 'DATABASE_URL', value: '@Microsoft.KeyVault(SecretUri=${kv.properties.vaultUri}secrets/DatabaseUrl)' }
        { name: 'REDIS_URL', value: '@Microsoft.KeyVault(SecretUri=${kv.properties.vaultUri}secrets/RedisUrl)' }
      ]
    }
  }
  dependsOn: [ plan, insights, acr, kvSecretDatabase, kvSecretRedis ]
}

// Grant web app MSI access to Key Vault secrets
resource kvAccess 'Microsoft.KeyVault/vaults/accessPolicies@2023-02-01' = {
  name: 'add'
  parent: kv
  properties: {
    accessPolicies: [
      {
        tenantId: subscription().tenantId
        objectId: webapp.identity.principalId
        permissions: { secrets: [ 'get', 'list' ] }
      }
    ]
  }
  dependsOn: [ webapp ]
}

// VNet integration for App Service
resource webappVnet 'Microsoft.Web/sites/networkConfig@2022-03-01' = {
  name: 'virtualNetwork'
  parent: webapp
  properties: { subnetResourceId: appSubnetId }
  dependsOn: [ webapp, vnet ]
}

// =============================================================================
// Outputs
// =============================================================================

output staticWebAppHostname string = swa.properties.defaultHostname
output staticWebAppToken string = swa.listSecrets().properties.apiKey
output backendUrl string = 'https://${webAppName}.azurewebsites.net'
output acrServer string = acrLoginServer
output acrUsername string = acr.name
output acrPassword string = acr.listCredentials().passwords[0].value
output postgresFqdn string = '${pgName}.postgres.database.azure.com'
output redisHost string = '${redisName}.redis.cache.windows.net'
output keyVaultUri string = kv.properties.vaultUri
output appInsightsConnection string = insights.properties.ConnectionString
output vnetId string = vnet.id
output appSubnetId string = appSubnetId
output peSubnetId string = peSubnetId
