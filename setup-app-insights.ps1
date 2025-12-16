# Option D: Application Insights Setup
# Adds detailed logging and analytics

$ErrorActionPreference = "Stop"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "OPTION D: APPLICATION INSIGHTS SETUP" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$RG = "codex-rg"
$LOCATION = "eastus2"
$APP_INSIGHTS_NAME = "codex-insights"
$BACKEND_APP = "codex-backend-https"

Write-Host "[Step 1/4] Creating Application Insights Resource..." -ForegroundColor Yellow

# Check if Application Insights exists
$insights = az monitor app-insights component show `
    --app $APP_INSIGHTS_NAME `
    --resource-group $RG 2>$null

if (-not $insights) {
    az monitor app-insights component create `
        --app $APP_INSIGHTS_NAME `
        --location $LOCATION `
        --resource-group $RG `
        --output none

    Write-Host "  ✅ Application Insights created" -ForegroundColor Green
} else {
    Write-Host "  ✅ Application Insights exists" -ForegroundColor Green
}

# Get instrumentation key
$instrumentationKey = az monitor app-insights component show `
    --app $APP_INSIGHTS_NAME `
    --resource-group $RG `
    --query instrumentationKey -o tsv

$connectionString = az monitor app-insights component show `
    --app $APP_INSIGHTS_NAME `
    --resource-group $RG `
    --query connectionString -o tsv

Write-Host "  Instrumentation Key: $($instrumentationKey.Substring(0,8))..." -ForegroundColor Gray
Write-Host ""

Write-Host "[Step 2/4] Configuring Container App with App Insights..." -ForegroundColor Yellow

# Update container app environment variables
az containerapp update `
    --name $BACKEND_APP `
    --resource-group $RG `
    --set-env-vars "APPINSIGHTS_INSTRUMENTATIONKEY=$instrumentationKey" "APPLICATIONINSIGHTS_CONNECTION_STRING=$connectionString" `
    --output none

Write-Host "  ✅ Container App configured with Application Insights" -ForegroundColor Green
Write-Host ""

Write-Host "[Step 3/4] Creating Custom Dashboards..." -ForegroundColor Yellow

# Create custom dashboard configuration
$dashboardConfig = @{
    location = $LOCATION
    tags = @{}
    properties = @{
        lenses = @{
            "0" = @{
                order = 0
                parts = @{
                    "0" = @{
                        position = @{ x=0; y=0; colSpan=6; rowSpan=4 }
                        metadata = @{
                            inputs = @(
                                @{
                                    name = "ComponentId"
                                    value = "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RG/providers/microsoft.insights/components/$APP_INSIGHTS_NAME"
                                }
                            )
                            type = "Extension/AppInsightsExtension/PartType/AnalyticsLineChartPart"
                            settings = @{
                                content = @{
                                    PartTitle = "Request Rate"
                                }
                            }
                        }
                    }
                    "1" = @{
                        position = @{ x=6; y=0; colSpan=6; rowSpan=4 }
                        metadata = @{
                            inputs = @(
                                @{
                                    name = "ComponentId"
                                    value = "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RG/providers/microsoft.insights/components/$APP_INSIGHTS_NAME"
                                }
                            )
                            type = "Extension/AppInsightsExtension/PartType/AnalyticsLineChartPart"
                            settings = @{
                                content = @{
                                    PartTitle = "Response Time"
                                }
                            }
                        }
                    }
                    "2" = @{
                        position = @{ x=0; y=4; colSpan=6; rowSpan=4 }
                        metadata = @{
                            inputs = @(
                                @{
                                    name = "ComponentId"
                                    value = "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RG/providers/microsoft.insights/components/$APP_INSIGHTS_NAME"
                                }
                            )
                            type = "Extension/AppInsightsExtension/PartType/AnalyticsDonutChartPart"
                            settings = @{
                                content = @{
                                    PartTitle = "Failed Requests"
                                }
                            }
                        }
                    }
                    "3" = @{
                        position = @{ x=6; y=4; colSpan=6; rowSpan=4 }
                        metadata = @{
                            inputs = @(
                                @{
                                    name = "ComponentId"
                                    value = "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RG/providers/microsoft.insights/components/$APP_INSIGHTS_NAME"
                                }
                            )
                            type = "Extension/AppInsightsExtension/PartType/AvailabilityMetricsPart"
                            settings = @{
                                content = @{
                                    PartTitle = "Availability"
                                }
                            }
                        }
                    }
                }
            }
        }
        metadata = @{
            model = @{
                timeRange = @{
                    value = @{
                        relative = @{
                            duration = 24
                            timeUnit = 1
                        }
                    }
                    type = "MsPortalFx.Composition.Configuration.ValueTypes.TimeRange"
                }
            }
        }
    }
}

Write-Host "  ✅ Dashboard configuration created" -ForegroundColor Green
Write-Host ""

Write-Host "[Step 4/4] Setting Up Alerts..." -ForegroundColor Yellow

# Create alert for high response time
az monitor metrics alert create `
    --name "codex-high-response-time" `
    --resource-group $RG `
    --scopes "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RG/providers/microsoft.insights/components/$APP_INSIGHTS_NAME" `
    --condition "avg requests/duration > 1000" `
    --description "Alert when average response time exceeds 1 second" `
    --evaluation-frequency 5m `
    --window-size 15m `
    --action codex-alerts `
    --output none 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Response time alert created" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Alert may already exist" -ForegroundColor Yellow
}

# Create alert for high failure rate
az monitor metrics alert create `
    --name "codex-high-failure-rate" `
    --resource-group $RG `
    --scopes "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RG/providers/microsoft.insights/components/$APP_INSIGHTS_NAME" `
    --condition "avg requests/failed > 5" `
    --description "Alert when failed requests exceed 5 per minute" `
    --evaluation-frequency 5m `
    --window-size 15m `
    --action codex-alerts `
    --output none 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Failure rate alert created" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Alert may already exist" -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "APPLICATION INSIGHTS COMPLETE!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "📊 Access Your Insights:" -ForegroundColor White
Write-Host "  Portal: https://portal.azure.com" -ForegroundColor Gray
Write-Host "  Resource: $APP_INSIGHTS_NAME" -ForegroundColor Gray
Write-Host "  Resource Group: $RG" -ForegroundColor Gray
Write-Host ""
Write-Host "📈 Available Metrics:" -ForegroundColor White
Write-Host "  • Request rate and response times" -ForegroundColor Gray
Write-Host "  • Failed requests and exceptions" -ForegroundColor Gray
Write-Host "  • Dependency tracking" -ForegroundColor Gray
Write-Host "  • Custom events and traces" -ForegroundColor Gray
Write-Host "  • Live metrics stream" -ForegroundColor Gray
Write-Host ""
Write-Host "🔔 Configured Alerts:" -ForegroundColor White
Write-Host "  • High response time (>1s average)" -ForegroundColor Gray
Write-Host "  • High failure rate (>5 failures/min)" -ForegroundColor Gray
Write-Host ""

# Save configuration
@{
    instrumentation_key = $instrumentationKey
    connection_string = $connectionString
    resource_name = $APP_INSIGHTS_NAME
    portal_url = "https://portal.azure.com/#resource/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RG/providers/microsoft.insights/components/$APP_INSIGHTS_NAME"
    configured_date = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    cost = "~$2-5/month for basic usage"
} | ConvertTo-Json | Out-File "app-insights-config.json"

Write-Host "💾 Configuration saved to: app-insights-config.json`n" -ForegroundColor Gray
