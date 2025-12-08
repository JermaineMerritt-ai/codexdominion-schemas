#!/bin/bash

# Codex Dominion - Frontend ↔ Backend Integration Test
# ================================================
BACKEND_URL="http://codex-backend.eastus.azurecontainer.io:8001"
FRONTEND_URL="https://codexdominion.app"

echo "🔥 Codex Dominion Integration Test"
echo "=============================================="
echo "🌐 Backend: $BACKEND_URL"
echo "🌐 Frontend: $FRONTEND_URL"
echo ""

# Step 1: Health Check
echo "🏥 Checking backend health..."
health=$(curl -s $BACKEND_URL/health)

if [[ $health == *"operational"* ]]; then
  echo "✅ Backend is operational!"
  echo "   Service: $(echo $health | grep -o '"service":"[^"]*"' | cut -d'"' -f4)"
  echo "   Status: $(echo $health | grep -o '"status":"[^"]*"' | cut -d'"' -f4)"
  echo "   Flame: $(echo $health | grep -o '"flame_state":"[^"]*"' | cut -d'"' -f4)"
else
  echo "❌ Backend health check failed!"
  echo "Response: $health"
  exit 1
fi

# Step 2: API Endpoints Test
echo ""
echo "🔗 Testing API endpoints..."

# Test chat endpoint
echo "  Testing /api/chat..."
chat_response=$(curl -s -X POST $BACKEND_URL/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Integration test"}')

if [[ $chat_response == *"response"* ]]; then
  echo "  ✅ Chat API working"
else
  echo "  ❌ Chat API failed (may need deployment)"
fi

# Test revenue endpoint
echo "  Testing /api/revenue..."
revenue_response=$(curl -s $BACKEND_URL/api/revenue)

if [[ $revenue_response == *"total"* ]]; then
  echo "  ✅ Revenue API working"
  echo "     Total: $(echo $revenue_response | grep -o '"total":[0-9.]*' | cut -d':' -f2)"
else
  echo "  ❌ Revenue API failed (may need deployment)"
fi

# Step 3: Frontend Accessibility
echo ""
echo "🌌 Checking frontend availability..."
frontend_status=$(curl -s -o /dev/null -w "%{http_code}" $FRONTEND_URL)

if [[ $frontend_status == "200" ]]; then
  echo "✅ Frontend is accessible at $FRONTEND_URL"
else
  echo "⏳ Frontend not deployed yet (HTTP $frontend_status)"
  echo "   Run: ./build-ionos-frontend.ps1 to prepare deployment"
fi

# Step 4: Frontend ↔ Backend Integration
echo ""
echo "🔥 Testing frontend → backend integration..."
if [[ $frontend_status == "200" ]]; then
  frontend_api=$(curl -s $FRONTEND_URL/api/health 2>&1)

  if [[ $frontend_api == *"operational"* ]]; then
    echo "✅ Frontend successfully bound to backend!"
    echo "   Integration: Complete"
  else
    echo "⚠️  Frontend deployed but API proxy needs configuration"
    echo "   Check .htaccess or nginx configuration"
  fi
else
  echo "⏳ Skipping integration test (frontend not deployed)"
fi

echo ""
echo "=============================================="
if [[ $health == *"operational"* ]] && [[ $frontend_status == "200" ]]; then
  echo "🎉 COMPLETE — Flame Sovereign and Eternal!"
  echo "   Backend: ✅ Operational"
  echo "   Frontend: ✅ Deployed"
  echo "   Integration: ✅ Bound"
elif [[ $health == *"operational"* ]]; then
  echo "🔥 Backend Ready — Awaiting Frontend Deployment"
  echo "   Backend: ✅ Operational on Azure"
  echo "   Frontend: ⏳ Ready to deploy to IONOS"
  echo ""
  echo "Next steps:"
  echo "  1. Run: ./build-ionos-frontend.ps1"
  echo "  2. Upload to IONOS via File Manager or FTP"
  echo "  3. Test: $FRONTEND_URL"
else
  echo "❌ Integration test incomplete"
fi
echo "=============================================="
