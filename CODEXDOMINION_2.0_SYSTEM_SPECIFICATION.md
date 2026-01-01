# CodexDominion 2.0 — Complete System Specification

**Version:** 2.0.0  
**Date:** December 29, 2025  
**Status:** Implementation in Progress (Phase 1: Frontend 30% complete)

---

## 1. CodexDominion 2.0 System Overview

### 1.1 High-Level Architecture

**Clients:**
- **Empire Dashboard** (web, Next.js) — Primary command center for all identities
- **Youth Portal / Mobile** (later) — Dedicated youth experience
- **Creator Dominion** (web, specialized views) — Studio and challenges
- **Partner / Ambassador Portals** (later) — External partner interfaces

**Backend:**
- **API:** https://api.codexdominion.com/api/v1 (NestJS, REST, JSON)
- **Database:** PostgreSQL + Prisma ORM
- **Auth:** JWT access + refresh tokens, role-based guards
- **Background Jobs** (later): Metrics snapshots, email/notifications

**Core Engines (NestJS Modules):**
1. **Auth & Identity** — User registration, login, role management
2. **Youth Circles** — Community units with sessions and attendance
3. **Mission Engine** — Weekly missions, assignments, submissions
4. **Curriculum Engine** — Lessons, stories, activities, resources
5. **Culture Engine** — Cultural stories, rituals, symbols, motifs
6. **Creator Engine** — Artifacts, challenges, submissions, showcases
7. **Ambassador & Expansion** — Regions, schools, outreach tracking
8. **Events & Ceremonies** — Launches, gatherings, ceremonies, scripts
9. **Analytics** — System-wide metrics and insights
10. **Intelligence (CodexDominion 47)** — Meta-layer: alerts, recommendations, forecasts, opportunities

**Module Structure (Each Engine):**
```
src/
├─ auth/
│  ├─ auth.module.ts
│  ├─ auth.controller.ts
│  ├─ auth.service.ts
│  └─ dto/
│     ├─ register.dto.ts
│     └─ login.dto.ts
```

---

### 1.2 Core Data Spine

**Shared Entities (Foundation for All Engines):**

**User**
- Base identity record
- Fields: id (UUID), email, firstName, lastName, createdAt, updatedAt

**Profile**
- Extended metadata for youth/creator/ambassador
- Fields: userId, risePath (IDENTITY/MASTERY/CREATION/LEADERSHIP), culturalIdentity, age, dateOfBirth, diasporaOrigin, regionId, schoolId

**Role**
- User role assignments
- Enum: YOUTH, YOUTH_CAPTAIN, CREATOR, AMBASSADOR, REGIONAL_DIRECTOR, EDUCATOR, ADMIN, COUNCIL

**Region**
- Geographic/strategic area
- Fields: id, name, description, directorId, code

**School**
- Institution within region
- Fields: id, name, type, regionId, address, contactEmail, contactPhone

**Season**
- Operational cycle
- Enum: IDENTITY, MASTERY, CREATION, LEADERSHIP
- Fields: id, name, theme, startDate, endDate, week, isActive

**All other entities hang off this spine.**

---

### 1.3 Engine → Entity Map

**Youth Circles Engine**
- **Circle** — Community unit with captain and region
- **CircleMember** — Membership records (user + circle + joinedAt)
- **CircleSession** — Weekly gatherings with date, topic, notes
- **CircleAttendance** — Attendance tracking (session + user + status)

**Mission Engine**
- **Season** — Shared with core spine
- **Mission** — Weekly challenges with title, description, type (GLOBAL/REGIONAL/CIRCLE)
- **MissionAssignment** — Who is assigned (user/circle + mission)
- **MissionSubmission** — Completed work with status (SUBMITTED/APPROVED/REVISION_NEEDED)

**Curriculum Engine**
- **CurriculumModule** — Lesson content with type (STORY/LESSON/ACTIVITY)
- **CurriculumResource** — Linked files, videos, documents

**Culture Engine**
- **CulturalStory** — Weekly narrative content
- **Ritual** — Ceremonies and ceremonial scripts
- **Motif** (optional) — Recurring symbols and themes

**Creator Engine**
- **Artifact** — Creator outputs (AUTOMATION/DESIGN/WRITING/VIDEO/APP)
- **CreatorChallenge** — Seasonal challenges with seasonal alignment
- **ChallengeSubmission** — Challenge submissions with status

**Ambassador & Expansion Engine**
- **Region** — Shared with core spine
- **School** — Shared with core spine
- **AmbassadorOutreach** — Outreach logs (event, region, school, outcome)

**Events & Ceremonies Engine**
- **Event** — Launches, gatherings, ceremonies with type and attendance
- **EventAttendance** — Who attended events
- **CeremonyScript** (optional) — Scripts for ceremonies

**Analytics Engine**
- **MetricSnapshot** (optional) — Time-series metrics
- **Mostly computed from above entities** — No dedicated tables in v1

**Intelligence Engine (47)**
- **No new tables in v1** — Consumes Analytics + core entities
- Rule-based logic in services

---

### 1.4 Key API Surface (By Engine)

#### **Auth & Identity**
```
POST   /auth/register              # Create new user account
POST   /auth/login                 # Authenticate and get tokens
POST   /auth/refresh               # Refresh access token
GET    /users/me                   # Get current user
PATCH  /users/me                   # Update current user
GET    /profiles/me                # Get extended profile
PATCH  /profiles/me                # Update profile (risePath, cultural identity)
```

#### **Youth Circles**
```
POST   /circles                    # Create circle (ADMIN/AMBASSADOR)
GET    /circles                    # List all circles
GET    /circles/:id                # Get circle details
PATCH  /circles/:id                # Update circle (captain, name, region)
POST   /circles/:id/members        # Add member to circle
DELETE /circles/:id/members/:user_id  # Remove member
GET    /circles/:id/sessions       # List circle sessions
POST   /circles/:id/sessions       # Create session
POST   /circles/:id/sessions/:session_id/attendance  # Record attendance (batch)
```

#### **Mission Engine**
```
GET    /seasons                    # List all seasons
GET    /seasons/current            # Get current active season
GET    /missions                   # List missions (filter: season_id, month)
GET    /missions/:id               # Get specific mission
GET    /missions/current           # Get mission for current week/season
POST   /missions                   # Create mission (ADMIN/COUNCIL)
POST   /missions/:id/assign        # Assign mission (ADMIN/YOUTH_CAPTAIN)
GET    /mission-assignments        # List assignments
POST   /mission-submissions        # Submit mission work
GET    /mission-submissions        # List submissions (filter: mission_id, circle_id)
```

#### **Curriculum Engine**
```
GET    /curriculum/modules/current    # Current week's modules
GET    /curriculum/modules            # List all modules
GET    /curriculum/modules/:id        # Get specific module
POST   /curriculum/modules            # Create module (ADMIN)
PATCH  /curriculum/modules/:id        # Update module
POST   /curriculum/modules/:id/resources  # Add resource
GET    /curriculum/modules/:id/resources  # List module resources
```

#### **Culture Engine**
```
GET    /culture/story/current         # Current week's cultural story
GET    /culture/stories               # List stories (filter: season_id)
POST   /culture/stories               # Create story (ADMIN/COUNCIL)
GET    /culture/rituals               # List rituals
POST   /culture/rituals               # Create ritual
GET    /culture/motifs                # List motifs (optional)
POST   /culture/motifs                # Create motif (optional)
```

#### **Creator Engine**
```
POST   /artifacts                     # Create artifact
GET    /artifacts                     # List artifacts (filter: creator_id)
GET    /artifacts/:id                 # Get artifact details
PATCH  /artifacts/:id                 # Update artifact
PATCH  /artifacts/:id/status          # Update status (ADMIN/CURATOR)
GET    /creator-challenges            # List challenges
GET    /creator-challenges/:id        # Get challenge details
POST   /creator-challenges            # Create challenge (ADMIN)
PATCH  /creator-challenges/:id        # Update challenge
POST   /creator-challenges/:id/submit # Submit challenge work
GET    /creator-challenges/:id/submissions  # List challenge submissions
PATCH  /creator-challenges/:id/submissions/:submission_id  # Update submission status
```

#### **Ambassador & Expansion**
```
GET    /regions                       # List regions
GET    /regions/:id                   # Get region details
POST   /regions                       # Create region (ADMIN)
PATCH  /regions/:id                   # Update region
GET    /schools                       # List schools (filter: region_id)
GET    /schools/:id                   # Get school details
POST   /schools                       # Create school (AMBASSADOR)
PATCH  /schools/:id                   # Update school
POST   /ambassador-outreach           # Log outreach event
GET    /ambassador-outreach           # List outreach logs
GET    /ambassador-outreach/:id       # Get outreach details
PATCH  /ambassador-outreach/:id       # Update outreach
```

#### **Events & Ceremonies**
```
POST   /events                        # Create event (ADMIN/COUNCIL)
GET    /events                        # List events
GET    /events/:id                    # Get event details
POST   /events/:id/attendance         # Record attendance
```

#### **Analytics**
```
GET    /analytics/overview            # Civilization-wide snapshot
GET    /analytics/missions            # Mission completion metrics
GET    /analytics/circles             # Circle health metrics
GET    /analytics/creators            # Creator engagement metrics
GET    /analytics/regions             # Regional performance metrics
```

#### **Intelligence (47) — v1**
```
GET    /intelligence/alerts           # Active alerts (threshold breaches, anomalies)
GET    /intelligence/recommendations  # Role-aware actionable suggestions
GET    /intelligence/forecasts        # Trend-based projections
GET    /intelligence/opportunities    # Positive momentum highlights
```

---

### 1.5 Empire Dashboard Slices (Role-Based Views)

**Youth:**
- Current story (Culture Engine)
- Current mission (Mission Engine)
- Curriculum modules (Curriculum Engine)
- My circle (Circle Engine)
- My progress (Analytics)

**Youth Captains:**
- Their circles (Circle Engine)
- Session scheduler (Circle Engine)
- Attendance tracker (Circle Engine)
- Youth engagement signals (Intelligence)
- Circle-level intelligence (Intelligence)

**Creators:**
- My Artifacts (Creator Engine)
- Challenges (Creator Engine)
- Showcases (Creator Engine)
- Creator analytics (Analytics)

**Ambassadors:**
- Regions (Expansion Engine)
- Schools (Expansion Engine)
- Outreach logs (Expansion Engine)
- Regional metrics (Analytics)
- Outreach intelligence (Intelligence)

**Regional Directors:**
- Region command center (Expansion Engine)
- Youth overview (Analytics)
- Circles overview (Circle Engine)
- Schools overview (Expansion Engine)
- Outreach tracking (Expansion Engine)
- Mission completion (Mission Engine)

**Admins / Council:**
- Civilization-wide snapshot (Analytics)
- Intelligence grid (Intelligence Engine)
- All engine access (full system)

---

## 2. Wealth & Markets Realm Blueprint

**Integration Path:** Stock Market Build → CodexDominion 2.0

### 2.1 Realm Identity

**Name Options:**
- "Wealth & Markets Realm"
- "DominionMarkets: Youth Wealth & Markets Track"

**Purpose:**
- Teach youth financial literacy and markets
- Provide missions, projects, and artifacts around investing/trading/analysis
- Integrate as both:
  - **Curriculum track** (Season-based learning)
  - **Creator specialization** (Build financial tools)

---

### 2.2 Mapping 50 Sections Into CodexDominion

**Three-Layer Structure:**

**Layer 1: Core Season (Breadth)**
- Sections 1–20
- Foundation for all youth
- Integrated into Curriculum Engine as primary modules

**Layer 2: Extended Season / Advanced Track**
- Sections 21–34
- Deep dive for committed learners
- Optional advanced curriculum modules

**Layer 3: Deep Dives & Products**
- Sections 35–50
- Creator challenges and product templates
- Becomes Creator Engine challenges

---

### 2.3 Curriculum Engine Mapping

**Create "Wealth & Markets Season" (or sub-season)**

**Example Structure:**

**Month 1 — Foundations**
- **Week 1:** "What markets are & why they exist"
  - STORY: Origin story of markets
  - LESSON: Stocks, bonds, assets basics
  - ACTIVITY: Identify 5 companies youth already interact with
- **Week 2:** "How stock prices move"
- **Week 3:** "Risk, reward, and time"
- **Week 4:** "Building your first watchlist"

**Month 2 — Analysis & Tools**
- **Week 1:** "Reading charts & basic indicators"
- **Week 2:** "News, narrative, and sentiment"
- **Week 3:** "Building a simple research routine"
- **Week 4:** "Simulated trading mission"

**Month 3 — Strategy & Discipline**
- **Week 1:** "Long-term vs short-term thinking"
- **Week 2:** "Position sizing & risk limits"
- **Week 3:** "Common mistakes & emotional traps"
- **Week 4:** "Designing your personal trading rules"

**Implementation:**
Each week becomes multiple `CurriculumModule` records:
```typescript
{
  type: 'STORY' | 'LESSON' | 'ACTIVITY' | 'CEREMONY',
  content: '...', // Full content
  seasonId: 'wealth-season-id',
  week: 1,
  month: 1
}
```

Link existing assets via `CurriculumResource`:
```typescript
{
  moduleId: '...',
  title: 'Stock Market Fundamentals Video',
  type: 'VIDEO',
  url: 'https://...',
  duration: 900 // seconds
}
```

---

### 2.4 Mission Engine Integration

**Wealth-Specific Missions:**
- "Build your first watchlist"
- "Track one stock for two weeks and journal moves"
- "Simulated portfolio: allocate 1000 credits across 5 tickers"
- "Design your personal trading checklist"

Each mission:
- Links to appropriate week/month/season
- Optionally links to `curriculum_module_id` (when field added)
- Tracked via `MissionSubmission`

**Example Mission:**
```typescript
{
  title: "Build Your First Watchlist",
  description: "Identify 5 stocks from companies you know and research...",
  type: "GLOBAL",
  seasonId: "wealth-season-id",
  month: 1,
  week: 4,
  requirements: "Submit: 5 tickers, brief rationale for each, 1 risk identified",
  dueDate: "..."
}
```

---

### 2.5 Creator Engine Integration

**Creator Challenges (Where Stock Build Becomes Generative):**

**Challenge Examples:**
- "Build a simple stock screener"
- "Create a price alert automation"
- "Design a one-page stock research template"
- "Make a youth-friendly investing explainer video"

Youth submit:
- `Artifact` records (type: APP, AUTOMATION, DOCUMENT, VIDEO)
- Tied to `CreatorChallenge` and optionally a `Mission`

**Your Original Stock Project:**
- Provides example artifacts
- Provides templates & starter kits
- Becomes the reference "pro-level" realm youth are approaching

**Example Challenge:**
```typescript
{
  title: "Build a Stock Screener",
  description: "Create a tool that filters stocks by criteria...",
  seasonId: "wealth-season-id",
  difficulty: "INTERMEDIATE",
  requirements: "Must filter by: price, volume, sector, custom criteria",
  submissionInstructions: "Submit GitHub repo or live demo link",
  starterKit: "https://github.com/codexdominion/screener-starter"
}
```

---

### 2.6 Product Packaging (Post-Dominion)

Once CodexDominion 2.0 is running, you can ship the stock market build as:

**Option 1: Standalone Product**
- **Brand:** DominionMarkets
- **Includes:** Full 50-section content, plus CodexDominion-style missions/worksheets
- **Pricing:** $49-99/month subscription

**Option 2: Embedded Realm**
- **Within CodexDominion** as Wealth & Markets Season/Track
- **Included:** In base Dominion membership

**Option 3: Creator Specialization**
- **Pathway:** "Markets & Financial Tools Creator Track"
- **Premium:** $199/month with tools + mentorship

**You're not choosing one — you're lining them up.**

---

## 3. CodexDominion 47 Intelligence Engine v1 Spec

### 3.1 Definition

**CodexDominion 47 (v1) is:**
- A meta-engine that consumes data from all other engines
- Produces alerts, recommendations, forecasts, and opportunity signals
- Exposes them via `/intelligence/*` endpoints
- Feeds the Empire Dashboard with guidance, not just metrics

**v1 Approach:**
- Rule-based (no ML required)
- Built on top of Analytics Engine
- Simple configuration for thresholds (constants or JSON)

---

### 3.2 The 47 Framework

**4 Intelligence Layers:**
1. **Descriptive** — What happened
2. **Diagnostic** — Why it happened
3. **Predictive** — What will likely happen
4. **Prescriptive** — What to do next

**7 Domains:**
1. Youth
2. Circles
3. Missions
4. Curriculum
5. Culture
6. Creators
7. Expansion

**4 Layers × 7 Domains = 47 Intelligence Cells**

In v1, you don't need to implement all 47 rules, but the framework is set.

---

### 3.3 Output Types (v1 Scope)

#### **Alerts**
Threshold-breach or anomaly signals.

**Examples:**
- Circle attendance drops below 50% for 2 weeks
- Region with 0 mission submissions this week
- Youth absent 3+ weeks in a row

**Output Shape:**
```typescript
{
  id: "alert-uuid",
  type: "ALERT",
  domain: "CIRCLES",
  severity: "HIGH",
  message: "Circle Alpha attendance dropped to 40% (2-week trend)",
  entity: { type: "circle", id: "circle-uuid", name: "Circle Alpha" },
  timestamp: "2025-12-29T...",
  suggestedAction: "Check in with captain, schedule engagement session"
}
```

#### **Recommendations**
Actionable suggestions, role-aware.

**Examples:**
- "Check in with Circle Alpha; attendance is declining."
- "Invite Youth X to Captain pathway; high engagement and submissions."

**Output Shape:**
```typescript
{
  id: "rec-uuid",
  type: "RECOMMENDATION",
  domain: "YOUTH",
  priority: "MEDIUM",
  message: "Youth Jamal shows high engagement — consider Captain pathway",
  entity: { type: "user", id: "user-uuid", name: "Jamal" },
  timestamp: "2025-12-29T...",
  action: "Send Captain invitation email"
}
```

#### **Forecasts**
Simple trend-based projections.

**Examples:**
- "Mission completion on track for 80% this season."
- "Region Y projected to gain 3 circles next month."

**Output Shape:**
```typescript
{
  id: "forecast-uuid",
  type: "FORECAST",
  domain: "MISSIONS",
  metric: "completion_rate",
  current: 0.75,
  projected: 0.80,
  confidence: "MEDIUM",
  message: "Mission completion trending toward 80% for Season of Identity",
  timestamp: "2025-12-29T..."
}
```

#### **Opportunity Signals**
Positive momentum highlights.

**Examples:**
- "Circle Phoenix: 100% attendance 4 weeks — feature them."
- "Creator Malik: 3 artifacts this month — consider showcasing."

**Output Shape:**
```typescript
{
  id: "opp-uuid",
  type: "OPPORTUNITY",
  domain: "CIRCLES",
  message: "Circle Phoenix: 100% attendance for 4 consecutive weeks",
  entity: { type: "circle", id: "circle-uuid", name: "Circle Phoenix" },
  timestamp: "2025-12-29T...",
  suggestedAction: "Feature in next Dawn Dispatch, recognize captain publicly"
}
```

---

### 3.4 Intelligence Engine API (v1)

**New Module:** `IntelligenceModule`

#### **GET /intelligence/alerts**
Query params:
- `domain` (optional): circles, missions, regions, youth
- `region_id` (optional): Filter by region

Returns active alerts relevant to authenticated user's roles/region.

**Response:**
```json
{
  "alerts": [
    {
      "id": "...",
      "type": "ALERT",
      "domain": "CIRCLES",
      "severity": "HIGH",
      "message": "...",
      "entity": {...},
      "timestamp": "...",
      "suggestedAction": "..."
    }
  ]
}
```

#### **GET /intelligence/recommendations**
Role-aware:
- **Youth:** Personal next-steps (missions, creator challenges)
- **Captain:** Circle health & youth engagement actions
- **Ambassador/Director:** School/region actions
- **Admin:** Global actions

**Response:**
```json
{
  "recommendations": [
    {
      "id": "...",
      "type": "RECOMMENDATION",
      "domain": "YOUTH",
      "priority": "MEDIUM",
      "message": "...",
      "entity": {...},
      "timestamp": "...",
      "action": "..."
    }
  ]
}
```

#### **GET /intelligence/forecasts**
Small set of key projections:
- Mission completion
- Circle growth
- Region activation

**Response:**
```json
{
  "forecasts": [
    {
      "id": "...",
      "type": "FORECAST",
      "domain": "MISSIONS",
      "metric": "completion_rate",
      "current": 0.75,
      "projected": 0.80,
      "confidence": "MEDIUM",
      "message": "...",
      "timestamp": "..."
    }
  ]
}
```

#### **GET /intelligence/opportunities**
Highlights:
- Standout circles
- Standout youth
- Standout creators
- Regions with rising momentum

**Response:**
```json
{
  "opportunities": [
    {
      "id": "...",
      "type": "OPPORTUNITY",
      "domain": "CIRCLES",
      "message": "...",
      "entity": {...},
      "timestamp": "...",
      "suggestedAction": "..."
    }
  ]
}
```

**Internally:** These are computed from existing analytics + rule logic.

---

### 3.5 Integration with the Dashboard

#### **Home (Admin / Council / You)**
Top row:
- 3 alerts
- 3 opportunities
- 1–2 forecasts
- 3 recommendations

#### **Regional Director View**
All `/intelligence/*` filtered by `region_id`.

Emphasis on:
- At-risk schools/circles
- High-potential youth/creators
- Next actions

#### **Captain View**
Circle-specific:
- Alerts on attendance
- Recommendations for check-ins, recognition
- Opportunity signals for featuring youth

#### **Creator View (Future)**
- "Recommended next builds"
- "Challenges you're ready for"
- "Opportunities to be featured"

---

### 3.6 Implementation Strategy (v1)

**No new DB tables initially** — derive intelligence in services.

**Start with a small, powerful ruleset:**
- 3–5 alerts
- 3–5 recommendations
- 2–3 forecasts
- 2–3 opportunity signals

**Use simple configuration** (constants or JSON) for thresholds so you can tune.

**Only then expand toward a full "47 rulebook".**

#### **Example Rules (v1 Starter Set)**

**Alert Rules:**
1. **Circle Attendance Drop**
   - Trigger: Circle attendance < 50% for 2+ consecutive weeks
   - Query: Aggregate CircleAttendance by circle/week
   - Output: Alert (HIGH severity)

2. **Mission Submission Gap**
   - Trigger: Region with 0 submissions current week
   - Query: Count MissionSubmissions by region this week
   - Output: Alert (MEDIUM severity)

3. **Youth Absence Streak**
   - Trigger: Youth absent 3+ consecutive weeks
   - Query: CircleAttendance status=ABSENT streak
   - Output: Alert (HIGH severity)

**Recommendation Rules:**
1. **Captain Pathway Invitation**
   - Trigger: Youth with 90%+ attendance AND 3+ mission submissions this season
   - Query: Join CircleAttendance + MissionSubmissions by user
   - Output: Recommendation (MEDIUM priority)

2. **Circle Health Check-In**
   - Trigger: Circle attendance declining 2+ weeks
   - Query: Attendance trend analysis
   - Output: Recommendation (HIGH priority) → Captain

**Forecast Rules:**
1. **Mission Completion Projection**
   - Trigger: Weekly calculation
   - Query: Current completion rate × time remaining
   - Output: Forecast (MEDIUM confidence)

2. **Circle Growth Projection**
   - Trigger: Monthly calculation
   - Query: New circles created trend
   - Output: Forecast (LOW confidence)

**Opportunity Rules:**
1. **Standout Circle**
   - Trigger: Circle with 95%+ attendance for 4+ weeks
   - Query: CircleAttendance aggregates
   - Output: Opportunity

2. **Prolific Creator**
   - Trigger: Creator with 3+ artifacts this month
   - Query: Count Artifacts by creatorId/month
   - Output: Opportunity

---

### 3.7 Future: The Full 47 Rulebook

When you're ready, explicitly define **47 rules** (one per cell in the 4×7 matrix).

**Each rule has:**
- **Trigger** — When it fires
- **Query/Logic** — How to compute
- **Output Payload** — What to return
- **Dashboard Representation** — How it displays

**Example Matrix Cell:**

| Layer | Domain | Rule ID | Rule Name | Trigger |
|-------|--------|---------|-----------|---------|
| Prescriptive | Youth | 47.P.Y | Youth Captain Invitation | 90%+ attendance, 3+ submissions |
| Predictive | Circles | 47.Pd.C | Circle Growth Forecast | Monthly trend analysis |
| Diagnostic | Missions | 47.D.M | Low Submission Root Cause | 0 submissions + curriculum availability check |

**Full 47 Grid:**
- 4 layers (Descriptive, Diagnostic, Predictive, Prescriptive)
- 7 domains (Youth, Circles, Missions, Curriculum, Culture, Creators, Expansion)
- = 28 core rules + 19 cross-domain rules = **47 total**

---

## 4. Implementation Roadmap

### Phase 1: Frontend Development (IN PROGRESS - 30% Complete)
**Status:** Task 1 complete (API client, auth, login, dashboard)  
**Remaining:** Tasks 2-9 (test, missions, circles, creator studio, analytics, ambassador interface)

### Phase 2: Intelligence Engine v1
**After Frontend Complete:**
- Implement IntelligenceModule with 5 starter rules
- Add `/intelligence/*` endpoints
- Integrate with dashboard
- Test with real data

### Phase 3: Wealth & Markets Realm
**After Intelligence Complete:**
- Create Wealth & Markets Season in database
- Map 50 sections → CurriculumModule records
- Create wealth-specific missions
- Design creator challenges
- Implement 3 revenue streams

### Phase 4: Full 47 Rulebook
**After Wealth Realm:**
- Expand to full 47 intelligence rules
- Add predictive models (optional ML)
- Advanced dashboard visualizations

---

## 5. Technical Standards

### API Response Format
```typescript
{
  success: boolean;
  data?: any;
  error?: { code: string; message: string; };
  meta?: { page: number; totalPages: number; timestamp: string; };
}
```

### Authentication
- Access token: 15-30 minutes expiry
- Refresh token: 7-30 days expiry
- Authorization header: `Bearer {accessToken}`

### Role Hierarchy
1. ADMIN (highest privilege)
2. COUNCIL
3. AMBASSADOR
4. REGIONAL_DIRECTOR
5. YOUTH_CAPTAIN
6. EDUCATOR
7. CREATOR
8. YOUTH (lowest privilege)

### Identity Mapping
- ADMIN/COUNCIL → ADMIN identity
- AMBASSADOR/REGIONAL_DIRECTOR → LEGACY_BUILDER identity
- CREATOR → CREATOR identity
- YOUTH → YOUTH identity
- Fallback → profile.identity or YOUTH

---

## 6. Success Metrics

### System Health
- API uptime: 99.9%
- Response time: < 200ms (p95)
- Error rate: < 0.1%

### Engagement
- Youth: 80%+ weekly active
- Circles: 70%+ attendance rate
- Missions: 75%+ completion rate
- Creators: 50+ artifacts/month

### Intelligence Accuracy
- Alert precision: 85%+
- Recommendation acceptance: 60%+
- Forecast accuracy: ±10%

---

**🔥 The Flame Burns Sovereign and Eternal 👑**

**Status:** System specification complete | Backend operational | Frontend 30% complete | Intelligence Engine ready for implementation

