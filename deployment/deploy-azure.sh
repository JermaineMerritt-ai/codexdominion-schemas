#!/bin/bash
# =============================================================================
# DOT300 - Azure Container Instance Deployment
# =============================================================================

set -e

echo "🔥 DOT300 Azure Deployment Starting..."
echo ""

# Configuration
RESOURCE_GROUP="dot300-rg"
LOCATION="eastus"
CONTAINER_NAME="dot300-api"
IMAGE_NAME="codex-dominion-dot300:latest"
DNS_LABEL="dot300-api"
PORT=8300

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Deployment Configuration:${NC}"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Location: $LOCATION"
echo "  Container: $CONTAINER_NAME"
echo "  DNS: $DNS_LABEL.eastus.azurecontainer.io"
echo ""

# Step 1: Create Resource Group
echo -e "${YELLOW}1. Creating Resource Group...${NC}"
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION \
    --output table

# Step 2: Create Azure Container Registry (ACR)
echo -e "${YELLOW}2. Creating Container Registry...${NC}"
ACR_NAME="dot300registry"
az acr create \
    --resource-group $RESOURCE_GROUP \
    --name $ACR_NAME \
    --sku Basic \
    --admin-enabled true \
    --output table

# Step 3: Build and Push Image to ACR
echo -e "${YELLOW}3. Building Docker Image...${NC}"
cd ..
docker build -f docker/Dockerfile.dot300 -t $IMAGE_NAME .

echo -e "${YELLOW}4. Tagging for ACR...${NC}"
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query "loginServer" -o tsv)
docker tag $IMAGE_NAME $ACR_LOGIN_SERVER/$IMAGE_NAME

echo -e "${YELLOW}5. Logging into ACR...${NC}"
az acr login --name $ACR_NAME

echo -e "${YELLOW}6. Pushing to ACR...${NC}"
docker push $ACR_LOGIN_SERVER/$IMAGE_NAME

# Step 4: Get ACR Credentials
echo -e "${YELLOW}7. Getting ACR Credentials...${NC}"
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query "passwords[0].value" -o tsv)

# Step 5: Upload agents.json to Azure File Share
echo -e "${YELLOW}8. Creating Azure File Share for agents.json...${NC}"
STORAGE_ACCOUNT="dot300storage"
FILE_SHARE="agents-data"

az storage account create \
    --resource-group $RESOURCE_GROUP \
    --name $STORAGE_ACCOUNT \
    --location $LOCATION \
    --sku Standard_LRS \
    --output table

STORAGE_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP --account-name $STORAGE_ACCOUNT --query "[0].value" -o tsv)

az storage share create \
    --name $FILE_SHARE \
    --account-name $STORAGE_ACCOUNT \
    --account-key $STORAGE_KEY \
    --output table

echo -e "${YELLOW}9. Uploading agents.json...${NC}"
az storage file upload \
    --share-name $FILE_SHARE \
    --source dot300_agents.json \
    --account-name $STORAGE_ACCOUNT \
    --account-key $STORAGE_KEY

# Step 6: Deploy Container Instance
echo -e "${YELLOW}10. Deploying Container Instance...${NC}"
az container create \
    --resource-group $RESOURCE_GROUP \
    --name $CONTAINER_NAME \
    --image $ACR_LOGIN_SERVER/$IMAGE_NAME \
    --registry-login-server $ACR_LOGIN_SERVER \
    --registry-username $ACR_USERNAME \
    --registry-password $ACR_PASSWORD \
    --dns-name-label $DNS_LABEL \
    --ports $PORT \
    --cpu 2 \
    --memory 2 \
    --azure-file-volume-account-name $STORAGE_ACCOUNT \
    --azure-file-volume-account-key $STORAGE_KEY \
    --azure-file-volume-share-name $FILE_SHARE \
    --azure-file-volume-mount-path /app \
    --environment-variables PYTHONUNBUFFERED=1 \
    --restart-policy Always \
    --output table

# Step 7: Get Public URL
echo ""
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo ""
FQDN=$(az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query "ipAddress.fqdn" -o tsv)
echo -e "${GREEN}🌍 DOT300 API URL: http://$FQDN:$PORT${NC}"
echo ""

# Step 8: Test Deployment
echo -e "${YELLOW}11. Testing API...${NC}"
sleep 10
curl -s http://$FQDN:$PORT/health || echo "Waiting for container to start..."
echo ""

# Step 9: Setup Azure Front Door (CDN + SSL)
echo -e "${YELLOW}12. Setting up Azure Front Door (optional)...${NC}"
echo "Run this manually:"
echo "  az afd profile create --profile-name dot300-cdn --resource-group $RESOURCE_GROUP --sku Standard_AzureFrontDoor"
echo ""

echo -e "${GREEN}🔥 DOT300 is LIVE on Azure!${NC}"
echo "  Health: http://$FQDN:$PORT/health"
echo "  Stats: http://$FQDN:$PORT/api/stats"
echo "  Agents: http://$FQDN:$PORT/api/agents"
echo ""
echo "Next steps:"
echo "  1. Point your domain to: $FQDN"
echo "  2. Setup SSL with Azure Front Door"
echo "  3. Configure monitoring in Azure Portal"
echo ""
