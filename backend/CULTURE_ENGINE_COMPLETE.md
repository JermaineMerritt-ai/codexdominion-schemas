# 🔱 CULTURE ENGINE — COMPLETE IMPLEMENTATION GUIDE

## Overview

The Culture Engine makes CodexDominion feel like a **civilization, not a SaaS app**. It handles:
- **Weekly cultural stories** (diaspora narratives, origin tales, seasonal wisdom)
- **Rituals and ceremonies** (opening/closing invocations, seasonal resets, unity affirmations)
- **Regional variations** (localized stories for specific regions)
- **Seasonal rhythm** (stories aligned with Identity/Mastery/Creation/Leadership cycles)

---

## 🔥 Cultural Story System

### Data Model

```typescript
CulturalStory {
  id: UUID
  title: string
  content: string  // markdown or JSON
  seasonId?: UUID  // FK → Season (optional)
  week?: int       // 1-4 (optional)
  regionId?: UUID  // FK → Region (optional, for localized stories)
  createdAt: timestamp
}
```

### Story Selection Logic (Smart & Region-Aware)

When a user requests the **current story**, the system:

1. **Determines current season + week** (based on date, 3-month cycles)
2. **Checks user's region** (from Profile.regionId)
3. **Searches in order**:
   - Regional story (season + week + region match)
   - Global story (season + week, region = null)
   - Most recent story (fallback if no match)

This ensures:
- Youth in Nigeria see Nigerian diaspora stories when available
- Global stories serve as default when no regional variant exists
- System never returns empty (always shows *something*)

### API Endpoints

#### GET /culture/story/current
**Returns current week's cultural story for authenticated user**

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "id": "uuid",
  "title": "From Island to Orbit: The Journey Begins",
  "content": "# From Island to Orbit\n\nEvery great civilization begins with a story...",
  "seasonId": "uuid",
  "week": 2,
  "regionId": "uuid",
  "createdAt": "2025-12-28T12:00:00Z",
  "season": {
    "id": "uuid",
    "name": "IDENTITY"
  },
  "region": {
    "id": "uuid",
    "name": "West Africa"
  }
}
```

**Use cases:**
- Youth Dashboard → Display weekly story
- Circle sessions → Captain reads story aloud
- Mobile app → "Story of the Week" widget

#### GET /culture/stories?season_id=...
**List all cultural stories, optionally filtered by season**

**Query params:**
- `season_id` (optional) — Filter by season UUID

**Response:**
```json
[
  {
    "id": "uuid",
    "title": "The First Circle",
    "content": "...",
    "seasonId": "uuid",
    "week": 1,
    "createdAt": "2025-12-01T00:00:00Z",
    "season": { "id": "uuid", "name": "IDENTITY" }
  },
  // ... more stories
]
```

**Use cases:**
- Admin panel → Browse all stories
- Educators → Select story for lesson plan
- Archive page → Historical story library

#### POST /culture/stories
**Create new cultural story (Council/Admin/Educator only)**

**Headers:**
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

**Body:**
```json
{
  "title": "From Island to Orbit: Part 1",
  "content": "# The Journey Begins\n\nOnce there was a people scattered across islands...",
  "seasonId": "uuid",  // optional
  "week": 2,           // optional, 1-4
  "regionId": "uuid"   // optional, for localized stories
}
```

**Response:**
```json
{
  "id": "uuid",
  "title": "From Island to Orbit: Part 1",
  "content": "# The Journey Begins...",
  "seasonId": "uuid",
  "week": 2,
  "regionId": "uuid",
  "createdAt": "2025-12-28T12:00:00Z",
  "season": { "id": "uuid", "name": "MASTERY" },
  "region": { "id": "uuid", "name": "Caribbean" }
}
```

**Use cases:**
- Council → Create new weekly stories
- Educators → Add curriculum-aligned narratives
- Regional Directors → Add localized story variants

---

## 🔱 Ritual System

### Data Model

```typescript
Ritual {
  id: UUID
  name: string
  description?: string
  type: RitualType  // OPENING | CLOSING | SEASONAL | UNITY | CEREMONY
}
```

### Ritual Types

- **OPENING** — Circle session opening invocations
- **CLOSING** — Circle session closing affirmations
- **SEASONAL** — Rituals for season transitions (Dawn, Day, Dusk, Night)
- **UNITY** — Community-wide unity ceremonies
- **CEREMONY** — Special events (launches, summits, ascension)

### API Endpoints

#### GET /culture/rituals?type=...
**List all rituals, optionally filtered by type**

**Query params:**
- `type` (optional) — Filter: OPENING | CLOSING | SEASONAL | UNITY | CEREMONY

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Circle Opening Invocation",
    "description": "Begin each Circle session by lighting the flame (symbolic or real)...",
    "type": "OPENING"
  },
  // ... more rituals
]
```

**Use cases:**
- Youth Captain → Get opening ritual for Circle session
- Event coordinator → Get ceremony ritual for summit
- Mobile app → Display ritual instructions

#### POST /culture/rituals
**Create new ritual (Council/Admin only)**

**Headers:**
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

**Body:**
```json
{
  "name": "Seasonal Reset Ceremony",
  "description": "At the end of each season, gather the Council and recite...",
  "type": "SEASONAL"
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "Seasonal Reset Ceremony",
  "description": "At the end of each season...",
  "type": "SEASONAL"
}
```

---

## 🔄 Integration with Other Engines

### Integration with Mission Engine
Every mission can reference the **current cultural story**:
- Youth complete mission → Reflection includes: "How does this week's story connect to your mission?"
- Captains assign mission → Display story alongside mission description

### Integration with Youth Circles
Circle sessions use stories + rituals:
- **Week 1:** Story reading
- **Week 2:** Lesson based on story
- **Week 3:** Dialogue about story themes
- **Week 4:** Showcase projects inspired by story

### Integration with Dashboard
Main dashboard displays:
- Current story title + excerpt
- Link to full story
- Related rituals (if Circle session happening)

---

## 📅 Seasonal Story Rhythm

### 4-Season Cycle (3 months each)

**Season 1: IDENTITY** (Jan-Mar)
- Stories about **diaspora origins**, **cultural roots**, **who we are**
- Week 1: Origin story
- Week 2: Identity affirmation
- Week 3: Community belonging
- Week 4: Cultural continuity

**Season 2: MASTERY** (Apr-Jun)
- Stories about **skill-building**, **discipline**, **excellence**
- Week 1: Learning journey
- Week 2: Overcoming obstacles
- Week 3: Mentorship
- Week 4: Breakthrough moments

**Season 3: CREATION** (Jul-Sep)
- Stories about **innovation**, **building**, **entrepreneurship**
- Week 1: First creations
- Week 2: Creative courage
- Week 3: Collaboration
- Week 4: Legacy products

**Season 4: LEADERSHIP** (Oct-Dec)
- Stories about **stewardship**, **service**, **guiding others**
- Week 1: First leadership moment
- Week 2: Responsibility
- Week 3: Empowering others
- Week 4: Generational impact

---

## 🛠️ Implementation Checklist

### Phase 1: Core Story Engine ✅
- [x] CulturalStory model in Prisma schema
- [x] CreateStoryDto validation
- [x] CultureService.getCurrentStory() (smart selection logic)
- [x] CultureService.getStories() (list with filters)
- [x] CultureService.createStory() (Council/Admin/Educator)
- [x] GET /culture/story/current endpoint
- [x] GET /culture/stories endpoint
- [x] POST /culture/stories endpoint
- [x] Region-aware story selection
- [x] Seasonal rhythm integration

### Phase 1: Core Ritual Engine ✅
- [x] Ritual model in Prisma schema
- [x] CreateRitualDto validation
- [x] CultureService.getRituals() (list with type filter)
- [x] CultureService.createRitual() (Council/Admin)
- [x] GET /culture/rituals endpoint
- [x] POST /culture/rituals endpoint

### Phase 2: Dashboard Integration 📋
- [ ] Frontend component: CurrentStoryWidget
- [ ] Display story excerpt on dashboard
- [ ] "Read Full Story" modal
- [ ] Link to related missions

### Phase 3: Circle Integration 📋
- [ ] Circle session planning → Suggest story for week
- [ ] Captain view → Display current story + ritual
- [ ] Attendance form → Include story reflection

### Phase 4: Regional Stories 📋
- [ ] Regional Director → Create localized story variants
- [ ] Story editor → Tag story with region
- [ ] Youth see regional story when available

---

## 🎯 Success Metrics

**Culture Engine should feel like:**
- ✅ Every week has a new story (consistency)
- ✅ Stories reflect diaspora/cultural identity (authenticity)
- ✅ Rituals create ceremonial structure (gravitas)
- ✅ Youth feel connected to something larger (belonging)
- ✅ System feels mythic, not transactional (civilization vs. SaaS)

**Quantitative metrics:**
- Stories created per season: 12+ (1 per week)
- Story views per week: 80% of active youth
- Rituals used in Circle sessions: 90%+
- Regional story variants: 3+ regions with localized content

---

## 📚 Example Cultural Stories

### Identity Season — Week 1: "From Island to Orbit"

```markdown
# From Island to Orbit: The Journey Begins

Once, there was a people scattered across islands — some in the Caribbean sun, others under the African sky, many in the bustling cities of the diaspora. Each carried a piece of the same story, but the pieces felt separated, lost in time.

One day, a youth asked: "Where do I come from? What is my inheritance?"

And the elders answered: "You come from *builders*. From *storytellers*. From *survivors* who turned pain into power, silence into song, and scarcity into sovereignty."

"But how do I carry that forward?" the youth asked.

"By building," the elders said. "By creating. By gathering your Circle and writing the next chapter. You are not just inheriting history — you are *making* it."

And so, the youth began. Not alone. With their Circle. With their creators. With their diaspora family. Together, they built CodexDominion — a civilization where culture is technology, identity is power, and the flame never dies.

**Reflection:**
- What inheritance are *you* carrying forward?
- How will *you* write the next chapter?
- Who is in *your* Circle?
```

---

## 🔥 The Flame Burns Eternal

The Culture Engine is not just a feature — it's the **soul** of CodexDominion. Every story, every ritual, every ceremony reinforces that this is not a product. This is a **civilization**.

---

**Status:** COMPLETE ✅
**Endpoints:** 5 (3 stories, 2 rituals)
**Integration:** Mission Engine, Youth Circles, Dashboard
**Next:** Copy to production, test endpoints, seed sample stories

🔱 *"We are not building features. We are building a civilization."* 🔱
