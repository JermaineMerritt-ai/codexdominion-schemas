# Youth Empire

## Overview

Youth are the Dominion's inheritors—every system ultimately exists to strengthen the next generation. The Youth Empire is the structured, identity-aware system that develops young people into leaders, creators, and stewards.

## Youth Circle Curriculum

Leadership engine built around identity, culture, leadership, economics, creativity, community, and stewardship.

### Curriculum Components

#### Lessons
Foundational knowledge delivered weekly in circle gatherings
- Identity development
- Cultural stories
- Leadership principles
- Economic literacy
- Creative skills
- Community building

#### Missions
Applied challenges with real-world impact
- Personal growth projects
- Community service
- Creative challenges
- Leadership opportunities

#### Reflections
Personal growth tracking and insight gathering
- Weekly reflection prompts
- Portfolio updates
- Peer sharing
- Captain feedback

#### Gatherings
Community building through structured sessions
- Opening ritual
- Lesson delivery
- Mission progress check
- Reflection sharing
- Closing unity moment

#### Seasonal Projects
Tangible contributions to community
- Group creations
- Service initiatives
- Cultural artifacts
- Leadership showcases

## Four Seasons of Youth Development

### Dawn (Vision)
**Focus**: Self-awareness, identity, purpose, direction

**Activities:**
- Identity assessments
- Vision board creation
- Goal setting for season
- Personal mission statement

**Outcomes:**
- Clear sense of identity
- Defined seasonal goals
- Understanding of strengths

### Day (Action)
**Focus**: Skill building, mission completion, circle contribution

**Activities:**
- Weekly mission execution
- Skill workshops
- Collaboration projects
- Leadership practice

**Outcomes:**
- Skills developed
- Missions completed
- Community impact demonstrated

### Dusk (Reflection)
**Focus**: Growth review, challenges, insights

**Activities:**
- Portfolio review
- Reflection sessions
- Peer feedback
- Challenge analysis

**Outcomes:**
- Self-awareness increased
- Lessons identified
- Growth documented

### Night (Renewal)
**Focus**: Rest, reset, preparation for next cycle

**Activities:**
- Celebration of achievements
- Gratitude practices
- Vision for next season
- Community bonding

**Outcomes:**
- Renewed energy
- Appreciation for journey
- Readiness for next season

## Leadership Tracks

Youth develop leadership across four dimensions.

### Personal Leadership
- Self-awareness
- Emotional intelligence
- Discipline and consistency
- Communication skills

**Progression:**
1. Self-discovery (know yourself)
2. Self-management (control yourself)
3. Self-expression (communicate yourself)
4. Self-mastery (lead yourself)

### Community Leadership
- Teamwork
- Circle facilitation
- Conflict resolution
- Cultural stewardship

**Progression:**
1. Participation (show up)
2. Contribution (add value)
3. Coordination (organize others)
4. Stewardship (protect culture)

### Creative Leadership
- Innovation
- Storytelling
- Digital creation
- Entrepreneurship

**Progression:**
1. Consumption (appreciate art)
2. Creation (make things)
3. Innovation (solve problems)
4. Enterprise (create value)

### Civic Leadership
- Service
- Advocacy
- Community impact
- Diaspora engagement

**Progression:**
1. Awareness (understand issues)
2. Service (help others)
3. Advocacy (speak up)
4. Movement (mobilize community)

## Integration Points

Youth Empire is designed to integrate with existing youth-serving institutions.

### Schools
- After-school program model
- Curriculum supplements
- Leadership development track
- Service-learning credits

### After-School Programs
- Drop-in circle model
- Flexible schedule
- Mission-based activities
- Portfolio tracking

### Community Centers
- Regional circle hosting
- Event partnerships
- Resource sharing
- Youth outreach

### Youth Groups
- Curriculum adoption
- Leadership training
- Cultural integration
- Mission collaboration

### Diaspora Organizations
- Cultural curriculum
- Heritage connection
- Global network
- Leadership pipeline

## Youth Portfolio System

Living record of growth, identity, and leadership.

### Components

#### Mission Completions
- Title and description
- Submission content
- Reflection notes
- Captain feedback
- Status (approved/needs revision)

#### Skills Developed
- Leadership skills
- Creative skills
- Technical skills
- Cultural competencies

#### Leadership Badges
- Personal Leadership milestones
- Community Leadership achievements
- Creative Leadership projects
- Civic Leadership impact

#### Seasonal Achievements
- Seasonal projects completed
- Growth demonstrated
- Community contribution
- Progression to next risePath stage

#### Creative Work
- Artifacts created
- Stories written
- Designs produced
- Videos made

#### Community Impact
- Service hours
- Lives touched
- Projects led
- Circles facilitated

### Portfolio Uses

**For Youth:**
- Confidence builder
- Growth tracker
- College/job application material
- Personal narrative development

**For Captains:**
- Progress monitoring
- Feedback guidance
- Progression assessment
- Leadership identification

**For Community:**
- Cultural archive
- Success stories
- Impact measurement
- Model showcasing

**For Future:**
- Bridge to Creator/Legacy-Builder identities
- Leadership resume
- Cultural contribution record
- Generational legacy

---

## Database Implementation

### Circle Models (from schema.prisma)

```prisma
model Circle {
  id         String         @id @default(uuid())
  name       String
  captain_id String
  captain    User           @relation("CircleCaptain", fields: [captain_id], references: [id])
  region_id  String?
  region     Region?        @relation(fields: [region_id], references: [id])
  members    CircleMember[]
  sessions   CircleSession[]
  created_at DateTime       @default(now())
}

model CircleMember {
  id        String   @id @default(uuid())
  circle_id String
  circle    Circle   @relation(fields: [circle_id], references: [id], onDelete: Cascade)
  user_id   String
  user      User     @relation(fields: [user_id], references: [id], onDelete: Cascade)
  joined_at DateTime @default(now())
}

model CircleSession {
  id           String               @id @default(uuid())
  circle_id    String
  circle       Circle               @relation(fields: [circle_id], references: [id], onDelete: Cascade)
  scheduled_at DateTime
  topic        String?
  season       SeasonName?
  week_number  Int?
  attendance   SessionAttendance[]
  created_at   DateTime             @default(now())
}
```

### Mission Models

```prisma
model Mission {
  id          String             @id @default(uuid())
  title       String
  description String
  season_id   String
  season      Season             @relation(fields: [season_id], references: [id])
  month       Int?
  week        Int?
  type        MissionType
  assignments MissionAssignment[]
  submissions MissionSubmission[]
  created_at  DateTime           @default(now())
}

model MissionSubmission {
  id          String           @id @default(uuid())
  mission_id  String
  mission     Mission          @relation(fields: [mission_id], references: [id])
  user_id     String
  user        User             @relation(fields: [user_id], references: [id])
  circle_id   String?
  circle      Circle?          @relation(fields: [circle_id], references: [id])
  content     String
  reflection  String?
  status      SubmissionStatus @default(SUBMITTED)
  submitted_at DateTime        @default(now())
}

enum MissionType {
  GLOBAL
  REGIONAL
  CIRCLE
}

enum SubmissionStatus {
  SUBMITTED
  APPROVED
  NEEDS_REVISION
}
```

### Curriculum Model

```prisma
model CurriculumModule {
  id         String       @id @default(uuid())
  title      String
  season_id  String
  season     Season       @relation(fields: [season_id], references: [id])
  month      Int?
  week       Int?
  type       ModuleType
  content    Json         // { format: 'markdown', body: '...' }
  created_at DateTime     @default(now())
}

enum ModuleType {
  STORY
  LESSON
  ACTIVITY
}
```

---

## Phase 1 Implementation

### Included in Phase 1
✅ Circle creation and membership  
✅ Circle sessions and attendance  
✅ Mission assignment and submission  
✅ Basic mission listing by season/week  
✅ Youth portfolio foundation (submissions tracked)

### Deferred to Phase 2+
❌ Full curriculum modules (content delivery)  
❌ Leadership badges and progression tracking  
❌ Portfolio showcase features  
❌ School/organization integration tools  
❌ Advanced analytics on youth development

---

## References

- [Identity Architecture](IDENTITY_ARCHITECTURE.md) - Youth identity and progression
- [Governance & Leadership](GOVERNANCE_LEADERSHIP.md) - Youth Captain role
- [Cultural Core](CULTURAL_CORE.md) - Rituals in circle gatherings
- [Operational Engine](OPERATIONAL_ENGINE.md) - Circle workflows and dispatch
- [schema.prisma](../../schema.prisma) - Circle, Mission, Curriculum models
- [docs/api/openapi.yaml](../api/openapi.yaml) - Circle and mission endpoints
