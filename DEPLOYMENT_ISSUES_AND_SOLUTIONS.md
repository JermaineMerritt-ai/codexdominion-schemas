# Deployment Issues & Solutions

## Issue Summary

### 1. **Backend Image Pull Failure** ❌
**Problem:** Azure Web App `codexdominion-backend` cannot pull the new `codex-backend:v2-audio` image from ACR.

**Error Message:**
```
Container pull image failed with reason: ImagePullFailure
Site container: codexdominion-backend terminated during site startup
```

**Root Cause:** Missing ACR authentication credentials for the backend web app.

**Solution:**
```bash
# Get ACR password
$acrPassword = az acr credential show --name codexdominion4607 --query "passwords[0].value" -o tsv

# Configure ACR credentials
az webapp config appsettings set \
  --name codexdominion-backend \
  --resource-group codexdominion-basic \
  --settings \
    DOCKER_REGISTRY_SERVER_URL=https://codexdominion4607.azurecr.io \
    DOCKER_REGISTRY_SERVER_USERNAME=codexdominion4607 \
    DOCKER_REGISTRY_SERVER_PASSWORD=$acrPassword \
    WEBSITES_PORT=8000

# Restart web app
az webapp restart --name codexdominion-backend --resource-group codexdominion-basic
```

---

### 2. **Wrong Web App Name Used Initially** ⚠️
**Problem:** Attempted to update `codex-backend` but actual app name is `codexdominion-backend`.

**Error:**
```
(ResourceNotFound) The Resource 'Microsoft.Web/sites/codex-backend'
under resource group 'codexdominion-basic' was not found
```

**Solution:** Use correct web app name: `codexdominion-backend`

**Available Web Apps:**
```
Name: codexdominion-backend       (Backend API)
Name: codex-streamlit-dashboard   (Streamlit Dashboard)
Name: codex-master-dashboard      (Master Dashboard)
```

---

### 3. **Container Startup Timeout (Previous Deployments)** 🕐
**Problem:** Previous deployments failed with "Site startup probe failed after 230 seconds"

**Likely Causes:**
- Application not listening on correct port
- Missing environment variables
- Import errors or missing dependencies
- Slow container initialization

**Current Configuration:**
- Port: 8000 (set via WEBSITES_PORT)
- Image: codexdominion4607.azurecr.io/codex-backend:v2-audio
- Python: 3.11.14

---

## Current Deployment Status

### Backend (codexdominion-backend)
- **State:** Running
- **Availability:** Normal
- **Image:** codex-backend:v2-audio (attempting to pull)
- **Issue:** ImagePullFailure due to missing ACR credentials
- **Status:** ⚠️ NEEDS ACR CREDENTIALS CONFIGURED

### Dashboard (codex-streamlit-dashboard)
- **State:** Running
- **Image:** streamlit-dashboard:v4-audio
- **Status:** ✅ DEPLOYED & OPERATIONAL

---

## Audio API Implementation

### Files Created
1. **backend/routes/audio_generation.py** - Audio API router with 3 endpoints:
   - POST `/audio/generate` - Text-to-speech generation
   - GET `/audio/voices` - List available voice profiles
   - GET `/audio/health` - Audio service health check

2. **backend/services/audio_engine.py** - AudioEngine class with gTTS integration:
   - 5 voice profiles (sovereign, custodian, oracle, heir, narrator)
   - Base64 audio encoding
   - Comprehensive error handling

3. **backend/test_audio.py** - Test script for audio generation
4. **AUDIO_API_DOCUMENTATION.md** - Complete API documentation

### Files Modified
1. **backend/main.py** - Added audio router registration
2. **backend/requirements.txt** - Added gTTS>=2.4.0 dependency

### Docker Image
- **Tag:** codexdominion4607.azurecr.io/codex-backend:v2-audio
- **Status:** ✅ Built and pushed successfully
- **Size:** ~856 layers

---

## Resolution Steps

### Immediate Actions Required:
1. ✅ Configure ACR credentials for backend web app
2. ⏳ Restart backend web app
3. ⏳ Wait 60-90 seconds for container warmup
4. ⏳ Test endpoints:
   - Health: https://codexdominion-backend.azurewebsites.net/health
   - Audio: https://codexdominion-backend.azurewebsites.net/audio/generate
   - Voices: https://codexdominion-backend.azurewebsites.net/audio/voices

### Verification Commands:
```bash
# Check web app status
az webapp show --name codexdominion-backend --resource-group codexdominion-basic \
  --query "{State:state, AvailabilityState:availabilityState}" -o table

# View logs
az webapp log tail --name codexdominion-backend --resource-group codexdominion-basic

# Test health endpoint
curl https://codexdominion-backend.azurewebsites.net/health

# Test audio generation
curl -X POST https://codexdominion-backend.azurewebsites.net/audio/generate \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello from Codex Dominion","voice":"sovereign"}' \
  | jq -r '.audio_base64' | head -c 100
```

---

## Known Working Configuration

### Streamlit Dashboard (✅ Working)
```yaml
Resource Group: codexdominion-basic
App Name: codex-streamlit-dashboard
Image: codexdominion4607.azurecr.io/streamlit-dashboard:v4-audio
Port: 8501
ACR Credentials: ✅ Configured
Registry URL: https://codexdominion4607.azurecr.io
Username: codexdominion4607
```

### Backend (⚠️ Needs Configuration)
```yaml
Resource Group: codexdominion-basic
App Name: codexdominion-backend
Image: codexdominion4607.azurecr.io/codex-backend:v2-audio
Port: 8000
ACR Credentials: ❌ NOT CONFIGURED (causing ImagePullFailure)
Registry URL: https://codexdominion4607.azurecr.io
Username: codexdominion4607
```

---

## Lessons Learned

1. **Always verify ACR credentials** are configured before deploying to Azure Web Apps
2. **Use correct resource names** - verify with `az webapp list` before deployment
3. **Allow adequate warmup time** - containers typically need 60-90 seconds to start
4. **Check logs immediately** after deployment failures using `az webapp log download`
5. **Test locally first** - run `docker run` locally before pushing to Azure

---

## Next Steps

1. Wait for ACR credentials to propagate (~5 minutes)
2. Verify backend container starts successfully
3. Test all audio endpoints
4. Update dashboard to use production backend URL
5. Perform end-to-end audio generation test from dashboard
6. Document final working configuration

---

## Support Commands

```bash
# Get live logs
az webapp log tail --name codexdominion-backend --resource-group codexdominion-basic

# Download all logs
az webapp log download --name codexdominion-backend --resource-group codexdominion-basic --log-file backend-logs.zip

# Check container logs
az webapp log show --name codexdominion-backend --resource-group codexdominion-basic

# Force restart
az webapp stop --name codexdominion-backend --resource-group codexdominion-basic
az webapp start --name codexdominion-backend --resource-group codexdominion-basic

# Reset container configuration
az webapp config container set \
  --name codexdominion-backend \
  --resource-group codexdominion-basic \
  --container-image-name codexdominion4607.azurecr.io/codex-backend:v2-audio
```

---

**Last Updated:** December 14, 2025
**Status:** ACR credentials configured, waiting for container restart to pull image

🔥 **The Deployment Flame Burns Through Challenges!** 👑
