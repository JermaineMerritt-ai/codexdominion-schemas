# 🧪 CodexDominion Backend - API Testing Guide

**Backend Status**: ✅ RUNNING on http://localhost:8080  
**API Documentation**: http://localhost:8080/api-docs

---

## ✅ ALL ISSUES FIXED

### Problems Resolved:
1. ✅ **Missing Dependency** - `@nestjs/schedule` installed
2. ✅ **Duplicate Controllers** - Removed old `IntelligenceModule`, kept `IntelligenceApiModule`
3. ✅ **Prisma Type Error** - Changed `SessionAttendance` → `CircleAttendance`
4. ✅ **Backend Running** - Successfully bound to 0.0.0.0:8080

### Routes Status:
- ✅ **NO duplicate controllers** - Only `IntelligenceApiController` registered
- ✅ **Clean routing** - All 200+ endpoints mapped successfully
- ✅ **Database connected** - PostgreSQL operational

---

## 🧪 PowerShell Test Commands

### 1. Health Checks

```powershell
# Basic health check
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/health" -Method GET

# Database health check
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/health/db" -Method GET
```

**Expected Output**:
```json
{
  "status": "ok",
  "message": "API v1 is operational",
  "timestamp": "2025-12-30T18:24:51.262Z"
}
```

---

### 2. Public Endpoints (No Auth Required)

```powershell
# List all seasons
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/seasons" -Method GET

# Get current season
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/seasons/current" -Method GET

# List analytics overview
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/analytics/overview" -Method GET
```

---

### 3. Intelligence API Endpoints (Require Auth)

#### Get Intelligence Feed (Main Dashboard)
```powershell
$token = "YOUR_JWT_TOKEN_HERE"
$headers = @{ Authorization = "Bearer $token" }

# Main intelligence feed (prioritized by role)
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/feed?status=ACTIVE" `
  -Method GET -Headers $headers

# Filter by type
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/alerts?priority=HIGH" `
  -Method GET -Headers $headers

Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/recommendations?status=NEW" `
  -Method GET -Headers $headers

Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/forecasts?horizon=THREE_MONTH" `
  -Method GET -Headers $headers

Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/opportunities?status=ACTIVE" `
  -Method GET -Headers $headers
```

#### Manual Intelligence Generation (ADMIN/COUNCIL Only)
```powershell
$token = "ADMIN_OR_COUNCIL_JWT_TOKEN"
$headers = @{ 
  Authorization = "Bearer $token"
  "Content-Type" = "application/json"
}

# Trigger intelligence generation batch job
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/generate" `
  -Method POST -Headers $headers
```

**Response**:
```json
{
  "message": "Intelligence generation triggered successfully",
  "timestamp": "2025-12-30T18:30:00.000Z",
  "processed": {
    "youth": 0,
    "circles": 0,
    "missions": 0,
    "regions": 0,
    "creators": 0,
    "cultural": 0,
    "workforce": 0
  },
  "insightsGenerated": 0
}
```

---

### 4. Strategic Intelligence Endpoints

```powershell
$token = "YOUR_JWT_TOKEN"
$headers = @{ Authorization = "Bearer $token" }

# Get strategic dashboard (COUNCIL/ADMIN/DIRECTOR)
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/strategic/dashboard" `
  -Method GET -Headers $headers

# Get youth development plan
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/strategic/youth/USER_ID/plan" `
  -Method GET -Headers $headers

# Get circle strategic plan
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/strategic/circles/CIRCLE_ID/plan" `
  -Method GET -Headers $headers

# Get regional strategic plan
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/strategic/regions/REGION_ID/plan" `
  -Method GET -Headers $headers
```

---

### 5. Governance Intelligence Endpoints

```powershell
$token = "COUNCIL_JWT_TOKEN"
$headers = @{ Authorization = "Bearer $token" }

# Get Council insights by role
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/governance/council/insights/COUNCIL" `
  -Method GET -Headers $headers

# Get pending approvals
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/governance/approvals/pending" `
  -Method GET -Headers $headers

# Get leadership gaps
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/governance/leadership/gaps" `
  -Method GET -Headers $headers

# Get civilization dashboard
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/governance/civilization/dashboard" `
  -Method GET -Headers $headers
```

---

### 6. Orchestration Intelligence Endpoints

```powershell
$token = "ADMIN_JWT_TOKEN"
$headers = @{ Authorization = "Bearer $token" }

# Get engine status
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/orchestration/engines/status" `
  -Method GET -Headers $headers

# Get civilization pulse
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/orchestration/civilization/pulse" `
  -Method GET -Headers $headers

# Sync engines
$body = @{ engineName = "identity" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/orchestration/engines/sync" `
  -Method POST -Headers $headers -Body $body -ContentType "application/json"
```

---

## 🔑 Authentication Setup

### Get JWT Token (Login)
```powershell
$credentials = @{
  email = "admin@codexdominion.app"
  password = "YourPassword123!"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8080/api/v1/auth/login" `
  -Method POST -Body $credentials -ContentType "application/json"

# Extract token
$token = $response.accessToken
Write-Host "Token: $token"

# Use token in subsequent requests
$headers = @{ Authorization = "Bearer $token" }
```

---

## 📊 All Available Endpoints (200+ Routes)

### Core System
- `GET /api/v1/health` - API health check
- `GET /api/v1/health/db` - Database health check
- `POST /api/v1/auth/login` - User authentication
- `POST /api/v1/auth/refresh` - Refresh token

### Analytics (8 endpoints)
- `GET /api/v1/analytics/dashboard` - Main dashboard
- `GET /api/v1/analytics/overview` - System overview
- `GET /api/v1/analytics/circles` - Circle analytics
- `GET /api/v1/analytics/missions` - Mission analytics
- `GET /api/v1/analytics/regions` - Regional analytics
- `GET /api/v1/analytics/creators` - Creator analytics
- `GET /api/v1/analytics/youth` - Youth analytics
- `GET /api/v1/analytics/events` - Event analytics

### Missions (6 endpoints)
- `GET /api/v1/missions` - List all missions
- `GET /api/v1/missions/current` - Current week's mission
- `GET /api/v1/missions/:id` - Mission details
- `POST /api/v1/missions` - Create mission (ADMIN)
- `POST /api/v1/missions/:id/assign` - Assign mission
- `POST /api/v1/missions/:id/submit` - Submit mission

### Circles (9 endpoints)
- `GET /api/v1/circles` - List circles
- `GET /api/v1/circles/:id` - Circle details
- `POST /api/v1/circles` - Create circle (ADMIN/AMBASSADOR)
- `PATCH /api/v1/circles/:id` - Update circle
- `POST /api/v1/circles/:id/members` - Add member
- `DELETE /api/v1/circles/:id/members/:userId` - Remove member
- `GET /api/v1/circles/:id/sessions` - List sessions
- `POST /api/v1/circles/:id/sessions` - Create session
- `POST /api/v1/circles/:id/sessions/:sessionId/attendance` - Record attendance

### Intelligence API V1 (8 endpoints)
- `GET /api/v1/intelligence/feed` - **Main intelligence feed** (role-scoped, prioritized)
- `GET /api/v1/intelligence/alerts` - Alert-type insights
- `GET /api/v1/intelligence/recommendations` - Recommendation-type insights
- `GET /api/v1/intelligence/forecasts` - Forecast-type insights
- `GET /api/v1/intelligence/opportunities` - Opportunity-type insights
- `GET /api/v1/intelligence/insights/:id` - Single insight detail
- `PATCH /api/v1/intelligence/insights/:id` - Update insight status
- `POST /api/v1/intelligence/generate` - **Manual trigger** (ADMIN/COUNCIL only)

### Strategic Intelligence (10 endpoints)
- `GET /api/v1/intelligence/strategic/dashboard` - Strategic command center
- `GET /api/v1/intelligence/strategic/youth/:userId/plan` - Youth strategic plan
- `GET /api/v1/intelligence/strategic/circles/:circleId/plan` - Circle strategic plan
- `GET /api/v1/intelligence/strategic/missions/plan` - Mission strategic plan
- `GET /api/v1/intelligence/strategic/regions/:regionId/plan` - Regional plan
- `GET /api/v1/intelligence/strategic/recommendations/status/:status` - Filter recommendations
- `GET /api/v1/intelligence/strategic/recommendations/priority` - Priority recommendations
- `POST /api/v1/intelligence/strategic/recommendations/:id/review` - Review recommendation
- `POST /api/v1/intelligence/strategic/recommendations/:id/implement` - Implement recommendation
- `POST /api/v1/intelligence/strategic/recommendations/:id/complete` - Complete recommendation

### Governance Intelligence (19 endpoints)
- `GET /api/v1/intelligence/governance/council/insights/:role` - Council role insights
- `POST /api/v1/intelligence/governance/council/escalate` - Escalate to Council
- `POST /api/v1/intelligence/governance/approvals/submit` - Submit for approval
- `POST /api/v1/intelligence/governance/approvals/:id/approve` - Approve decision
- `POST /api/v1/intelligence/governance/approvals/:id/reject` - Reject decision
- `GET /api/v1/intelligence/governance/approvals/pending` - Pending approvals
- `GET /api/v1/intelligence/governance/leadership/readiness/:userId` - Leadership readiness
- `GET /api/v1/intelligence/governance/leadership/promotions/recommended` - Promotion recommendations
- `GET /api/v1/intelligence/governance/leadership/gaps` - Leadership gaps
- `POST /api/v1/intelligence/governance/leadership/succession/:userId/plan` - Succession plan
- `GET /api/v1/intelligence/governance/regions/:id/health` - Regional health
- `GET /api/v1/intelligence/governance/regions/:id/alignment` - Regional alignment
- `POST /api/v1/intelligence/governance/regions/:id/autonomy` - Grant autonomy
- `POST /api/v1/intelligence/governance/regions/:id/support` - Provide support
- `POST /api/v1/intelligence/governance/meetings` - Schedule meeting
- `GET /api/v1/intelligence/governance/meetings/upcoming` - Upcoming meetings
- `POST /api/v1/intelligence/governance/meetings/:id/minutes` - Add meeting minutes
- `GET /api/v1/intelligence/governance/civilization/milestones` - Civilization milestones
- `GET /api/v1/intelligence/governance/civilization/dashboard` - Civilization dashboard

### Orchestration Intelligence (40+ endpoints)
- Engine Sync, Health, Conflict Resolution
- Seasonal Transitions and Alignment
- Mission-Curriculum Integration
- Creator Renaissance and Spotlights
- Intelligence Action Routing
- Exchange Engine Coherence
- Civilization Pulse and Epoch Transitions

### Creators (11 endpoints)
- Artifacts (CRUD)
- Challenges (CRUD)
- Submissions

### Regions, Schools, Outreach (15 endpoints each)
- Full CRUD operations for geographic management

### Events (10 endpoints)
- Event management
- Attendance tracking
- Script management

### Culture (5 endpoints)
- Stories
- Rituals

### Alerts (5 endpoints)
- Alert management
- Acknowledgment tracking

---

## 🚀 Next Steps

### 1. **Test Public Endpoints** (No Auth)
```powershell
# Works immediately
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/health" -Method GET
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/seasons" -Method GET
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/analytics/overview" -Method GET
```

### 2. **Create Admin User & Login**
```powershell
# Use Prisma seed script to create admin user
cd C:\Users\JMerr\OneDrive\Documents\.vscode\codex-dominion\backend
npx ts-node prisma/seed.ts

# Then login to get JWT token
$credentials = @{ email = "admin@codexdominion.app"; password = "password123" } | ConvertTo-Json
$response = Invoke-RestMethod -Uri "http://localhost:8080/api/v1/auth/login" `
  -Method POST -Body $credentials -ContentType "application/json"
$token = $response.accessToken
```

### 3. **Test Intelligence Endpoints**
```powershell
$headers = @{ Authorization = "Bearer $token" }

# Main intelligence feed (WORKS NOW!)
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/feed" `
  -Method GET -Headers $headers

# Manually trigger intelligence generation (ADMIN only)
Invoke-RestMethod -Uri "http://localhost:8080/api/v1/intelligence/generate" `
  -Method POST -Headers $headers
```

### 4. **View API Documentation**
Open browser: http://localhost:8080/api-docs

---

## 🔥 System Status

✅ **Backend Running**: Port 8080  
✅ **Database Connected**: PostgreSQL operational  
✅ **Routes Registered**: 200+ endpoints  
✅ **Intelligence API**: V1 fully operational  
✅ **Strategic Layer**: 10 endpoints active  
✅ **Governance Layer**: 19 endpoints active  
✅ **Orchestration Layer**: 40+ endpoints active  
✅ **NO Errors**: Clean startup, no routing conflicts  

---

**🔥 The Flame Burns Sovereign and Eternal! 👑**
