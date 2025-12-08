// =============================================================================
// Codex Dominion - Azure Infrastructure as Code (Bicep)
// =============================================================================
// Complete infrastructure deployment for Codex Dominion application
// Provisions: Static Web Apps, App Service, PostgreSQL, Redis, ACR, Monitoring

targetScope = 'resourceGroup'

// =============================================================================
// Parameters
// =============================================================================

@description('Azure region for all resources')
param location string = 'eastus'

@description('Base name prefix for resources')
param baseName string = 'codex'

@description('Environment (dev, staging, prod)')
@allowed(['dev', 'staging', 'prod'])
param environment string = 'prod'

@description('Static Web App name')
param swaName string = '${baseName}-frontend-${environment}'

@description('App Service Plan name')
param appServicePlanName string = '${baseName}-plan-${environment}'

@description('Web App (backend) name')
param webAppName string = '${baseName}-backend-${environment}'

@description('Azure Container Registry name (must be globally unique, alphanumeric)')
param acrName string = '${baseName}acr${environment}'

@description('Docker image tag to deploy')
param dockerImage string = '${baseName}acr${environment}.azurecr.io/codex-backend:latest'

@description('PostgreSQL Flexible Server name')
param pgName string = '${baseName}-pg-${environment}'

@description('PostgreSQL admin username')
param pgAdminUser string = 'codexadmin'

@secure()
@description('PostgreSQL admin password')
param pgAdminPassword string

@description('PostgreSQL version')
@allowed(['12', '13', '14', '15', '16'])
param pgVersion string = '16'

@description('PostgreSQL storage size in GB')
@minValue(32)
@maxValue(16384)
param pgStorageGb int = 32

@description('Redis Cache name')
param redisName string = '${baseName}-redis-${environment}'

@description('Application Insights name')
param appInsightsName string = '${baseName}-insights-${environment}'

@description('Log Analytics Workspace name')
param lawName string = '${baseName}-law-${environment}'

@description('Key Vault name (for secrets management)')
param keyVaultName string = '${baseName}-kv-${environment}'

@description('Static Web Apps SKU')
@allowed(['Free', 'Standard'])
param swaSku string = 'Free'

@description('App Service Plan SKU')
@allowed(['B1', 'B2', 'S1', 'S2', 'P1V2', 'P2V2'])
param appServiceSku string = 'B1'

@description('Redis SKU')
@allowed(['Basic', 'Standard', 'Premium'])
param redisSku string = 'Basic'

@description('Redis capacity (0-6 for Basic/Standard, 1-5 for Premium)')
@minValue(0)
@maxValue(6)
param redisCapacity int = 0

@description('PostgreSQL public access CIDR (use Azure services only for production)')
param pgAllowedIps string = '0.0.0.0-255.255.255.255'

@description('Backend container port')
param backendPort int = 8001

@description('Database name')
param pgDbName string = 'codexdb'

@description('Enable Application Insights')
param enableAppInsights bool = true

@description('Enable Key Vault')
param enableKeyVault bool = false

@description('Tags for all resources')
param tags object = {
  application: 'codex-dominion'
  environment: environment
  managedBy: 'bicep'
  deployedDate: utcNow('yyyy-MM-dd')
}

// =============================================================================
// Variables
// =============================================================================

var acrLoginServer = '${acrName}.azurecr.io'
var redisFamily = redisSku == 'Premium' ? 'P' : 'C'
var appServiceTier = (appServiceSku == 'B1' || appServiceSku == 'B2') ? 'Basic' : ((appServiceSku == 'S1' || appServiceSku == 'S2') ? 'Standard' : 'PremiumV2')

// =============================================================================
// Log Analytics Workspace
// =============================================================================

resource law 'Microsoft.OperationalInsights/workspaces@2022-10-01' = if (enableAppInsights) {
  name: lawName
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
  }
}

// =============================================================================
// Application Insights
// =============================================================================

resource insights 'Microsoft.Insights/components@2020-02-02' = if (enableAppInsights) {
  name: appInsightsName
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: enableAppInsights ? law.id : null
    RetentionInDays: 30
    IngestionMode: 'LogAnalytics'
  }
}

// =============================================================================
// Azure Container Registry
// =============================================================================

resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: acrName
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
    publicNetworkAccess: 'Enabled'
    networkRuleBypassOptions: 'AzureServices'
  }
}

// =============================================================================
// Static Web Apps (Frontend)
// =============================================================================

resource swa 'Microsoft.Web/staticSites@2023-12-01' = {
  name: swaName
  location: location
  tags: tags
  sku: {
    name: swaSku
    tier: swaSku
  }
  properties: {
    buildProperties: {
      appLocation: 'frontend'
      apiLocation: ''
      outputLocation: 'out'
      appBuildCommand: 'npm run build'
    }
    stagingEnvironmentPolicy: 'Enabled'
    allowConfigFileUpdates: true
    provider: 'GitHub'
  }
}

// =============================================================================
// App Service Plan
// =============================================================================

resource plan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: appServicePlanName
  location: location
  tags: tags
  kind: 'linux'
  sku: {
    name: appServiceSku
    tier: appServiceTier
    capacity: 1
  }
  properties: {
    reserved: true
    zoneRedundant: false
  }
}

// =============================================================================
// App Service (Backend)
// =============================================================================

resource webapp 'Microsoft.Web/sites@2023-12-01' = {
  name: webAppName
  location: location
  tags: tags
  kind: 'app,linux,container'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    clientAffinityEnabled: false
    siteConfig: {
      linuxFxVersion: 'DOCKER|${dockerImage}'
      alwaysOn: appServiceSku != 'B1' && appServiceSku != 'B2'
      http20Enabled: true
      minTlsVersion: '1.2'
      ftpsState: 'Disabled'
      healthCheckPath: '/health'
      numberOfWorkers: 1
      appSettings: [
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'false'
        }
        {
          name: 'WEBSITES_PORT'
          value: string(backendPort)
        }
        {
          name: 'PORT'
          value: string(backendPort)
        }
        {
          name: 'ENVIRONMENT'
          value: environment
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_URL'
          value: 'https://${acrLoginServer}'
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
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: enableAppInsights ? insights.properties.InstrumentationKey : ''
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: enableAppInsights ? insights.properties.ConnectionString : ''
        }
        {
          name: 'ALLOWED_ORIGINS'
          value: 'https://${swa.properties.defaultHostname}'
        }
        {
          name: 'CORS_ENABLED'
          value: 'true'
        }
        {
          name: 'DATABASE_URL'
          value: 'postgresql://${pgAdminUser}:${pgAdminPassword}@${pg.properties.fullyQualifiedDomainName}:5432/${pgDbName}?sslmode=require'
        }
        {
          name: 'REDIS_URL'
          value: 'rediss://:${redis.listKeys().primaryKey}@${redis.properties.hostName}:${redis.properties.sslPort}?ssl_cert_reqs=required'
        }
      ]
    }
  }
  dependsOn: [
    pg
    redis
  ]
}

// Configure App Service logging
resource webappLogs 'Microsoft.Web/sites/config@2023-12-01' = {
  name: 'logs'
  parent: webapp
  properties: {
    applicationLogs: {
      fileSystem: {
        level: 'Information'
      }
    }
    httpLogs: {
      fileSystem: {
        retentionInMb: 35
        enabled: true
      }
    }
    detailedErrorMessages: {
      enabled: true
    }
    failedRequestsTracing: {
      enabled: true
    }
  }
}

// =============================================================================
// PostgreSQL Flexible Server
// =============================================================================

resource pg 'Microsoft.DBforPostgreSQL/flexibleServers@2023-06-01-preview' = {
  name: pgName
  location: location
  tags: tags
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    version: pgVersion
    administratorLogin: pgAdminUser
    administratorLoginPassword: pgAdminPassword
    storage: {
      storageSizeGB: pgStorageGb
      autoGrow: 'Enabled'
    }
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    highAvailability: {
      mode: 'Disabled'
    }
    maintenanceWindow: {
      customWindow: 'Disabled'
    }
  }
}

// PostgreSQL database
resource pgDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2023-06-01-preview' = {
  name: pgDbName
  parent: pg
  properties: {
    charset: 'UTF8'
    collation: 'en_US.utf8'
  }
}

// PostgreSQL firewall rules
resource pgFirewallAzure 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2023-06-01-preview' = {
  name: 'allow-azure-services'
  parent: pg
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

resource pgFirewallCustom 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2023-06-01-preview' = if (pgAllowedIps != '0.0.0.0-0.0.0.0') {
  name: 'allow-custom-ips'
  parent: pg
  properties: {
    startIpAddress: split(pgAllowedIps, '-')[0]
    endIpAddress: split(pgAllowedIps, '-')[1]
  }
}

// PostgreSQL configuration
resource pgConfig 'Microsoft.DBforPostgreSQL/flexibleServers/configurations@2023-06-01-preview' = {
  name: 'max_connections'
  parent: pg
  properties: {
    value: '200'
    source: 'user-override'
  }
}

// =============================================================================
// Azure Cache for Redis
// =============================================================================

resource redis 'Microsoft.Cache/Redis@2023-08-01' = {
  name: redisName
  location: location
  tags: tags
  properties: {
    sku: {
      name: redisSku
      family: redisFamily
      capacity: redisCapacity
    }
    enableNonSslPort: false
    minimumTlsVersion: '1.2'
    publicNetworkAccess: 'Enabled'
    redisConfiguration: {
      'maxmemory-policy': 'allkeys-lru'
    }
  }
}

// =============================================================================
// Key Vault (Optional)
// =============================================================================

resource kv 'Microsoft.KeyVault/vaults@2023-07-01' = if (enableKeyVault) {
  name: keyVaultName
  location: location
  tags: tags
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    enablePurgeProtection: true
    networkAcls: {
      defaultAction: 'Allow'
      bypass: 'AzureServices'
    }
  }
}

// Grant Key Vault access to App Service managed identity
resource kvSecretUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (enableKeyVault) {
  name: guid(kv.id, webapp.id, 'Key Vault Secrets User')
  scope: kv
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
    principalId: webapp.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

// Store secrets in Key Vault
resource kvSecretPg 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = if (enableKeyVault) {
  name: 'database-url'
  parent: kv
  properties: {
    value: 'postgresql://${pgAdminUser}:${pgAdminPassword}@${pg.properties.fullyQualifiedDomainName}:5432/${pgDbName}?sslmode=require'
  }
}

resource kvSecretRedis 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = if (enableKeyVault) {
  name: 'redis-url'
  parent: kv
  properties: {
    value: 'rediss://:${redis.listKeys().primaryKey}@${redis.properties.hostName}:${redis.properties.sslPort}?ssl_cert_reqs=required'
  }
}

// =============================================================================
// Outputs
// =============================================================================

@description('Static Web App hostname')
output staticWebAppHostname string = swa.properties.defaultHostname

@description('Static Web App deployment token')
output staticWebAppToken string = swa.listSecrets().properties.apiKey

@description('Backend API URL')
output backendUrl string = 'https://${webapp.properties.defaultHostName}'

@description('Container Registry login server')
output acrLoginServer string = acrLoginServer

@description('Container Registry admin username')
output acrUsername string = acr.listCredentials().username

@description('PostgreSQL FQDN')
output postgresFqdn string = pg.properties.fullyQualifiedDomainName

@description('PostgreSQL connection string')
output postgresConnectionString string = 'postgresql://${pgAdminUser}@${pg.properties.fullyQualifiedDomainName}:5432/${pgDbName}?sslmode=require'

@description('Redis hostname')
output redisHostname string = redis.properties.hostName

@description('Redis SSL port')
output redisSslPort int = redis.properties.sslPort

@description('Application Insights connection string')
output appInsightsConnection string = enableAppInsights ? insights.properties.ConnectionString : ''

@description('Application Insights instrumentation key')
output appInsightsKey string = enableAppInsights ? insights.properties.InstrumentationKey : ''

@description('Key Vault URI')
output keyVaultUri string = enableKeyVault ? kv.properties.vaultUri : ''

@description('Resource Group name')
output resourceGroupName string = resourceGroup().name

@description('App Service managed identity principal ID')
output webAppPrincipalId string = webapp.identity.principalId

// =============================================================================
// Deployment Summary
// =============================================================================

output deploymentSummary object = {
  environment: environment
  region: location
  resources: {
    staticWebApp: swa.name
    appService: webapp.name
    containerRegistry: acr.name
    postgreSQL: pg.name
    redis: redis.name
    applicationInsights: enableAppInsights ? insights.name : 'disabled'
    keyVault: enableKeyVault ? kv.name : 'disabled'
  }
  endpoints: {
    frontend: 'https://${swa.properties.defaultHostname}'
    backend: 'https://${webapp.properties.defaultHostName}'
    database: pg.properties.fullyQualifiedDomainName
    redis: redis.properties.hostName
  }
  costs: {
    estimatedMonthly: appServiceSku == 'B1' ? '$40-50' : '$60-80'
    staticWebApp: swaSku == 'Free' ? '$0' : '$9'
    appService: appServiceSku == 'B1' ? '$13' : '$25+'
    postgresql: '$12-15'
    redis: redisSku == 'Basic' ? '$15' : '$55+'
    containerRegistry: '$5'
  }
}
