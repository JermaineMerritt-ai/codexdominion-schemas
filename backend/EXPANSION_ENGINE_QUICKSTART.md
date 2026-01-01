# Ambassador & Expansion Engine - Quick Reference

## 🌍 Three Core Entities

### 1. **Region** - Geographic/Cultural Area
- Represents territories like "Barbados", "Jamaica", "NYC Diaspora"
- Has assigned Regional Director
- Contains multiple schools and circles
- Tracks timezone for scheduling

### 2. **School** - Partner Organization
- Community centers, youth groups, schools
- Linked to a region
- Has contact person for partnerships
- Tracks student profiles and ambassador visits

### 3. **AmbassadorOutreach** - Field Activity Log
- Documents visits, meetings, events
- Links ambassador → school → region
- Types: VISIT, MEETING, EVENT
- Tracks date and detailed notes

---

## 🔗 Quick Endpoint Reference

### Regions
```bash
# List all regions with counts
GET /api/v1/regions

# Get region details + schools + circles
GET /api/v1/regions/:id

# Create region (ADMIN only)
POST /api/v1/regions
{ "name": "Trinidad", "country": "Trinidad & Tobago", "timezone": "America/Port_of_Spain", "directorId": "uuid" }

# Update region (ADMIN / REGIONAL_DIRECTOR)
PATCH /api/v1/regions/:id
{ "name": "Updated Name", "directorId": "new-director-uuid" }
```

### Schools
```bash
# List schools (optionally filter by region)
GET /api/v1/schools?regionId=uuid

# Get school details
GET /api/v1/schools/:id

# Create school (ADMIN / AMBASSADOR)
POST /api/v1/schools
{ "regionId": "uuid", "name": "Harrison College", "address": "...", "contactPerson": "Principal Name" }

# Update school (ADMIN / AMBASSADOR / REGIONAL_DIRECTOR)
PATCH /api/v1/schools/:id
{ "name": "Updated Name", "contactPerson": "New Contact" }
```

### Outreach
```bash
# List outreach records (filter by region, school, ambassador, type)
GET /api/v1/outreach?regionId=uuid&schoolId=uuid&ambassadorId=uuid&type=VISIT

# Get outreach details
GET /api/v1/outreach/:id

# Log outreach activity (AMBASSADOR / REGIONAL_DIRECTOR / ADMIN)
POST /api/v1/outreach
{ "regionId": "uuid", "schoolId": "uuid", "type": "VISIT", "notes": "Met with 15 students...", "date": "2025-01-28" }

# Update outreach (own records only)
PATCH /api/v1/outreach/:id
{ "notes": "Updated notes", "type": "MEETING" }
```

---

## 🎭 Role-Based Access

| Action | ADMIN | REGIONAL_DIRECTOR | AMBASSADOR | Public |
|--------|-------|-------------------|------------|--------|
| View regions | ✅ | ✅ | ✅ | ✅ |
| Create region | ✅ | ❌ | ❌ | ❌ |
| Update region | ✅ | ✅ (own region) | ❌ | ❌ |
| Delete region | ✅ | ❌ | ❌ | ❌ |
| View schools | ✅ | ✅ | ✅ | ✅ |
| Create school | ✅ | ✅ | ✅ | ❌ |
| Update school | ✅ | ✅ | ✅ | ❌ |
| Delete school | ✅ | ❌ | ❌ | ❌ |
| View outreach | ✅ | ✅ | ✅ | ✅ |
| Log outreach | ✅ | ✅ | ✅ | ❌ |
| Edit outreach | ✅ | ✅ (own records) | ✅ (own records) | ❌ |
| Delete outreach | ✅ | ✅ (own records) | ✅ (own records) | ❌ |

---

## 📊 Common Query Patterns

### Get all schools in Barbados
```bash
GET /api/v1/regions?name=Barbados  # Get region ID
GET /api/v1/schools?regionId=barbados-region-001
```

### Get ambassador's outreach history
```bash
# Login as ambassador → get user ID from token
GET /api/v1/outreach?ambassadorId=YOUR_USER_ID
```

### Get all visits to a specific school
```bash
GET /api/v1/outreach?schoolId=SCHOOL_UUID&type=VISIT
```

### Regional Director's dashboard data
```bash
GET /api/v1/regions/YOUR_REGION_ID  # Get region + counts
GET /api/v1/schools?regionId=YOUR_REGION_ID  # Get all schools
GET /api/v1/outreach?regionId=YOUR_REGION_ID  # Get all outreach
```

---

## 🔐 Authentication Flow

```bash
# 1. Login as ambassador
curl -X POST http://localhost:4000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"ambassador.bridgetown@codexdominion.app","password":"password123"}'

# Response: { "accessToken": "eyJ...", "user": {...} }

# 2. Use token for authenticated requests
curl -X POST http://localhost:4000/api/v1/outreach \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{
    "regionId": "barbados-region-001",
    "schoolId": "school-uuid",
    "type": "VISIT",
    "notes": "Initial school visit",
    "date": "2025-01-28"
  }'
```

---

## 🌟 Key Features

### Auto-Injection
- **Ambassador ID**: Automatically injected from JWT when logging outreach
- No need to pass `ambassadorId` in POST /outreach

### Ownership Validation
- Ambassadors can only edit/delete their own outreach records
- Regional Directors can update regions they manage
- Admins have full access

### Foreign Key Validation
- Creating a school requires valid `regionId`
- Creating outreach requires valid `regionId` and optional `schoolId`
- Updating region with `directorId` verifies user exists

### Aggregated Counts
- Regions return `schoolCount`, `circleCount`, `outreachCount`
- Schools return `profileCount`, `outreachCount`
- Useful for dashboards and analytics

---

## 🎯 Common Use Cases

### Use Case 1: Onboard New School
1. GET /regions → Find region ID
2. POST /schools → Create school with regionId
3. POST /outreach → Log initial visit with schoolId

### Use Case 2: Track Ambassador Activity
1. Login as ambassador → Get user ID
2. GET /outreach?ambassadorId=YOUR_ID → View all your visits
3. POST /outreach → Log new visit

### Use Case 3: Regional Director Dashboard
1. GET /regions/:id → Get region overview
2. GET /schools?regionId=YOUR_REGION → List schools
3. GET /outreach?regionId=YOUR_REGION → List all outreach

### Use Case 4: School Engagement Report
1. GET /schools/:id → Get school details + outreachCount
2. GET /outreach?schoolId=SCHOOL_ID → List all visits/meetings
3. Analyze notes for follow-up actions

---

## 📁 File Structure

```
backend/src/
├── regions/
│   ├── regions.module.ts
│   ├── regions.controller.ts
│   ├── regions.service.ts
│   ├── dto/region.dto.ts
│   └── entities/region.entity.ts
├── schools/
│   ├── schools.module.ts
│   ├── schools.controller.ts
│   ├── schools.service.ts
│   ├── dto/school.dto.ts
│   └── entities/school.entity.ts
└── outreach/
    ├── outreach.module.ts
    ├── outreach.controller.ts
    ├── outreach.service.ts
    ├── dto/outreach.dto.ts
    └── entities/outreach.entity.ts
```

---

## 🔧 Seed Data

Run seeding script:
```bash
cd backend
npx ts-node prisma/seed-expansion.ts
```

This creates:
- 3 regions (Barbados, Jamaica, NYC Diaspora)
- 5 schools
- 2 regional directors
- 2 ambassadors
- 6 outreach records

---

**🔥 The expansion engine is live! Go forth and conquer regions!**
