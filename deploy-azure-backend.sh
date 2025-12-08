#!/bin/bash
# ============================================================================
# Deploy Codex Dominion Backend to Azure Container Instances
# ============================================================================

RESOURCE_GROUP="codex-dominion-rg"
LOCATION="eastus"
CONTAINER_NAME="codex-backend"
IMAGE_NAME="codex-dominion-backend:latest"
DNS_NAME="codex-backend"

echo "🔥 Deploying Codex Dominion Backend to Azure..."
echo "   Resource Group: $RESOURCE_GROUP"
echo "   Location: $LOCATION"
echo "   Container: $CONTAINER_NAME"

# Create resource group if it doesn't exist
echo "📦 Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Build and push Docker image to Azure Container Registry (ACR)
ACR_NAME="codexdominionacr"
echo "🏗️  Creating Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --location $LOCATION

# Enable admin user for ACR
az acr update -n $ACR_NAME --admin-enabled true

# Get ACR credentials
ACR_SERVER=$(az acr show --name $ACR_NAME --query loginServer --output tsv)
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value --output tsv)

echo "🐳 Logging into ACR: $ACR_SERVER"
docker login $ACR_SERVER -u $ACR_USERNAME -p $ACR_PASSWORD

# Tag and push image
echo "📤 Pushing image to ACR..."
docker tag $IMAGE_NAME $ACR_SERVER/$IMAGE_NAME
docker push $ACR_SERVER/$IMAGE_NAME

# Deploy to Azure Container Instances
echo "🚀 Deploying to Azure Container Instances..."
az container create \
  --resource-group $RESOURCE_GROUP \
  --name $CONTAINER_NAME \
  --image $ACR_SERVER/$IMAGE_NAME \
  --dns-name-label $DNS_NAME \
  --ports 8001 \
  --cpu 2 \
  --memory 4 \
  --registry-login-server $ACR_SERVER \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --environment-variables \
    PYTHON_ENV=production \
    API_HOST=0.0.0.0 \
    API_PORT=8001 \
    DATABASE_URL=sqlite:///./codex_dominion.db \
  --location $LOCATION

# Get the FQDN
FQDN=$(az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query ipAddress.fqdn --output tsv)

echo ""
echo "✅ Deployment complete!"
echo "   Backend URL: http://$FQDN:8001"
echo "   Health check: http://$FQDN:8001/health"
echo "   API Docs: http://$FQDN:8001/docs"
echo ""
echo "🔥 The sovereign flame burns eternal on Azure!"
