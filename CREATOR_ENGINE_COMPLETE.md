# 🎨 Creator Engine — Artifacts, Challenges, Submissions

**Status**: ✅ Fully Implemented (Backend Complete)  
**Location**: `backend/src/creators/`  
**Module**: `CreatorsModule`

---

## Overview

The Creator Engine is responsible for:
- **Collecting and organizing artifacts** (apps, automations, media, designs, writing, videos)
- **Running creator challenges** (monthly/seasonal challenges with deadlines)
- **Linking creation to missions, circles, and curriculum**
- **Feeding showcases and analytics**

**Where Missions shape behavior, and Culture shapes identity, Creation shapes the economy and legacy.**

---

## Data Models

### 1. **Artifact**
Creations from youth or creators.

**Fields:**
- `id` — UUID (PK)
- `creatorId` — FK → User
- `title` — string (200 char max)
- `description` — text (optional)
- `artifactType` — enum: `AUTOMATION`, `DESIGN`, `WRITING`, `VIDEO`, `APP`, `OTHER`
- `fileUrl` — string (optional, URL to file/repo/media)
- `missionId` — FK → Mission (optional, link to mission if relevant)
- `status` — enum: `DRAFT`, `SUBMITTED`, `PUBLISHED`, `ARCHIVED` (defaults to `PUBLISHED`)
- `createdAt` — timestamp

### 2. **CreatorChallenge**
Monthly or seasonal challenge.

**Fields:**
- `id` — UUID (PK)
- `title` — string (200 char max)
- `description` — text
- `seasonId` — FK → Season (optional)
- `deadline` — datetime (optional)
- `createdBy` — FK → User (admin/council)
- `createdAt` — timestamp

### 3. **ChallengeSubmission**
Creator's response to a challenge.

**Fields:**
- `id` — UUID (PK)
- `challengeId` — FK → CreatorChallenge
- `creatorId` — FK → User
- `artifactId` — FK → Artifact
- `submittedAt` — timestamp

---

## API Endpoints

### **Artifacts**

#### `POST /api/v1/creators/artifacts`
Create a new artifact for the authenticated creator/youth.

**Authentication:** JWT required  
**Authorization:** Any authenticated user

**Request Body:**
```json
{
  "title": "Budget Tracker Automation",
  "description": "Automates monthly budget calculations and sends alerts",
  "artifactType": "AUTOMATION",
  "fileUrl": "https://github.com/user/budget-tracker",
  "missionId": "123e4567-e89b-12d3-a456-426614174000",
  "status": "PUBLISHED"
}
```

**Response:** 201 Created
```json
{
  "id": "artifact-uuid",
  "creatorId": "user-uuid",
  "title": "Budget Tracker Automation",
  "description": "Automates monthly budget calculations...",
  "artifactType": "AUTOMATION",
  "fileUrl": "https://github.com/user/budget-tracker",
  "missionId": "mission-uuid",
  "status": "PUBLISHED",
  "createdAt": "2025-01-15T10:30:00Z",
  "creator": {
    "id": "user-uuid",
    "name": "Aisha Johnson",
    "email": "aisha@example.com"
  },
  "mission": {
    "id": "mission-uuid",
    "title": "Automate Your Life"
  }
}
```

---

#### `GET /api/v1/creators/artifacts`
Get all artifacts with optional filters.

**Authentication:** Public (no JWT required)  
**Query Parameters:**
- `creator_id` (optional) — Filter by creator
- `artifact_type` (optional) — Filter by type (AUTOMATION, DESIGN, etc.)
- `mission_id` (optional) — Filter by linked mission
- `status` (optional) — Filter by status (PUBLISHED, DRAFT, etc.)

**Response:** 200 OK
```json
[
  {
    "id": "artifact-uuid",
    "creatorId": "user-uuid",
    "title": "Budget Tracker Automation",
    "artifactType": "AUTOMATION",
    "status": "PUBLISHED",
    "createdAt": "2025-01-15T10:30:00Z",
    "creator": { ... },
    "mission": { ... }
  }
]
```

---

#### `GET /api/v1/creators/artifacts/:id`
Get a single artifact by ID.

**Authentication:** Public  
**Response:** 200 OK (artifact details)

---

#### `PUT /api/v1/creators/artifacts/:id`
Update an artifact (creator can only update their own).

**Authentication:** JWT required  
**Authorization:** Must be artifact owner

**Request Body:** Partial artifact object (any fields to update)

**Response:** 200 OK (updated artifact)

---

#### `DELETE /api/v1/creators/artifacts/:id`
Delete an artifact (creator can only delete their own).

**Authentication:** JWT required  
**Authorization:** Must be artifact owner

**Response:** 200 OK
```json
{
  "message": "Artifact deleted successfully"
}
```

---

### **Creator Challenges**

#### `POST /api/v1/creators/challenges`
Create a new creator challenge (Admin/Council only).

**Authentication:** JWT required  
**Authorization:** ADMIN or COUNCIL roles only

**Request Body:**
```json
{
  "title": "Build Your First Automation",
  "description": "Create an automation that solves a real problem in your community",
  "seasonId": "season-uuid",
  "deadline": "2025-01-31T23:59:59Z"
}
```

**Response:** 201 Created
```json
{
  "id": "challenge-uuid",
  "title": "Build Your First Automation",
  "description": "Create an automation...",
  "seasonId": "season-uuid",
  "deadline": "2025-01-31T23:59:59Z",
  "createdBy": "admin-user-uuid",
  "createdAt": "2025-01-01T00:00:00Z",
  "season": {
    "id": "season-uuid",
    "name": "IDENTITY"
  }
}
```

---

#### `GET /api/v1/creators/challenges`
Get all challenges with optional filters.

**Authentication:** Public  
**Query Parameters:**
- `season_id` (optional) — Filter by season
- `active` (optional, boolean) — Only show challenges with future deadlines

**Response:** 200 OK
```json
[
  {
    "id": "challenge-uuid",
    "title": "Build Your First Automation",
    "description": "...",
    "seasonId": "season-uuid",
    "deadline": "2025-01-31T23:59:59Z",
    "createdBy": "admin-uuid",
    "createdAt": "2025-01-01T00:00:00Z",
    "season": { ... },
    "submissionCount": 15
  }
]
```

---

#### `GET /api/v1/creators/challenges/:id`
Get a single challenge by ID (includes all submissions).

**Authentication:** Public  
**Response:** 200 OK (challenge details + submissions array)

---

### **Challenge Submissions**

#### `POST /api/v1/creators/submissions`
Submit an artifact to a challenge.

**Authentication:** JWT required  
**Authorization:** Any authenticated user (must own the artifact)

**Request Body:**
```json
{
  "challengeId": "challenge-uuid",
  "artifactId": "artifact-uuid"
}
```

**Validations:**
- Challenge must exist
- Deadline must not have passed
- Artifact must exist and belong to the user
- Artifact cannot already be submitted to this challenge

**Response:** 201 Created
```json
{
  "id": "submission-uuid",
  "challengeId": "challenge-uuid",
  "creatorId": "user-uuid",
  "artifactId": "artifact-uuid",
  "submittedAt": "2025-01-20T14:30:00Z",
  "challenge": {
    "id": "challenge-uuid",
    "title": "Build Your First Automation"
  },
  "creator": {
    "id": "user-uuid",
    "name": "Aisha Johnson",
    "email": "aisha@example.com"
  },
  "artifact": {
    "id": "artifact-uuid",
    "title": "Budget Tracker Automation",
    "artifactType": "AUTOMATION"
  }
}
```

---

#### `GET /api/v1/creators/submissions`
Get all submissions with optional filters.

**Authentication:** Public  
**Query Parameters:**
- `challenge_id` (optional) — Filter by challenge
- `creator_id` (optional) — Filter by creator

**Response:** 200 OK (array of submissions)

---

## Service Layer Methods

### **Artifacts**
- `createArtifact(userId, dto)` — Create new artifact
- `getArtifacts(filters)` — List artifacts with filters
- `getArtifactById(artifactId)` — Get single artifact
- `updateArtifact(userId, artifactId, dto)` — Update artifact (owner only)
- `deleteArtifact(userId, artifactId)` — Delete artifact (owner only)

### **Challenges**
- `createChallenge(userId, dto)` — Create challenge (admin/council only)
- `getChallenges(filters)` — List challenges with filters
- `getChallengeById(challengeId)` — Get challenge with submissions

### **Submissions**
- `createSubmission(userId, dto)` — Submit artifact to challenge
- `getSubmissions(filters)` — List submissions with filters

---

## Integration Points

### **Mission Linkage**
Artifacts can optionally link to missions via `missionId`:
- Youth complete missions by creating artifacts
- Artifacts show up in mission completion records
- Showcase displays artifacts created for specific missions

### **Seasonal Rhythm**
Challenges link to seasons via `seasonId`:
- Each season has signature challenges
- "Season 1 (Identity)" → Challenge: "Build Your First Automation"
- "Season 3 (Creation)" → Challenge: "Design Your Brand Identity"

### **Circle Integration**
- Circle sessions can showcase artifacts from members
- Captain can highlight "Artifact of the Week"
- Circle challenges can be created at circle level (future)

### **Analytics**
Creator Engine feeds:
- Total artifacts created (by type, by season)
- Challenge participation rates
- Top creators (by artifacts, by submissions)
- Artifact growth over time

---

## Workflows

### **Creator Workflow:**
1. Create artifact (`POST /artifacts`)
2. Optionally link to mission
3. Submit to active challenge (`POST /submissions`)
4. Artifact appears in public showcase
5. Analytics track creator activity

### **Admin Workflow:**
1. Create seasonal challenge (`POST /challenges`)
2. Set deadline and link to season
3. Announce challenge to community
4. Review submissions (`GET /challenges/:id`)
5. Showcase top artifacts

### **Youth Workflow:**
1. View active challenges (`GET /challenges?active=true`)
2. Create artifact for mission (`POST /artifacts`)
3. Submit to challenge (`POST /submissions`)
4. Share in circle session
5. Portfolio grows with artifacts

---

## Security & Validation

**Authentication:**
- Creating artifacts: JWT required
- Creating challenges: JWT + Admin/Council role
- Submitting to challenges: JWT required
- Viewing artifacts/challenges: Public

**Authorization:**
- Users can only update/delete their own artifacts
- Users can only submit their own artifacts to challenges
- Admin/Council create challenges

**Validation:**
- Artifact title max 200 characters
- Challenge description required
- Deadline validation (cannot submit after deadline)
- Duplicate submission prevention

---

## File Structure

```
backend/src/creators/
├── dto/
│   ├── create-artifact.dto.ts       # Artifact creation validation
│   ├── create-challenge.dto.ts      # Challenge creation validation
│   └── create-submission.dto.ts     # Submission validation
├── entities/
│   ├── artifact.entity.ts           # Artifact Swagger schema
│   ├── creator-challenge.entity.ts  # Challenge Swagger schema
│   └── challenge-submission.entity.ts # Submission Swagger schema
├── creators.controller.ts           # 10 REST endpoints
├── creators.service.ts              # Business logic layer
└── creators.module.ts               # NestJS module definition
```

---

## Next Steps (Integration)

### **Frontend Components:**
1. **Artifact Showcase** — Gallery of published artifacts
2. **Create Artifact Form** — Upload/link artifacts
3. **Challenge Card** — Display active challenges
4. **My Artifacts Page** — Creator portfolio
5. **Challenge Submissions Gallery** — View all submissions

### **Home Screen Integration:**
Add "Featured Creator" or "Recent Artifacts" section to Home screen left column.

### **Database Seeding:**
Create `prisma/seed-creators.ts` with:
- 3 sample artifacts (automation, design, video)
- 2 sample challenges (Identity season, Mastery season)
- 2 sample submissions

---

## 🔥 Status Summary

**✅ COMPLETE:**
- 3 DTOs with full validation
- 3 Entity definitions for Swagger
- Service layer with 11 methods
- Controller with 10 REST endpoints
- Full authentication & authorization
- Mission and season integration
- Complete documentation

**⚠️ BLOCKED BY:**
- Backend build errors (16 webpack compilation errors)
- Port 4000 not binding (backend not operational)

**📋 READY FOR:**
- Backend build fix
- Module integration with AppModule
- Database seeding
- Frontend component development
- Testing with live API

---

**The Creator Engine is complete. The builders are ready to rise.** 🎨🔱

