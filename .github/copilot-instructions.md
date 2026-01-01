# Codex Dominion AI Agent Instructions

## Architecture Overview

**Codex Dominion** is a hybrid polyglot monorepo with a ceremonial naming system, combining Python data/AI dashboards, Next.js/TypeScript frontend, FastAPI backend services, and multi-cloud infrastructure (Azure, GCP, IONOS).

**Status (Dec 2025)**: Production LIVE | Azure Cloud | 52+ Dashboards | $95k/month Revenue Target

### Core Hierarchy ("Council Seal Structure")
```
Council Seal (governance)
├─ Sovereigns (apps/) → application-level execution
├─ Custodians (packages/) → shared libraries and infrastructure
├─ Industry Agents + Avatars → AI-powered automation
└─ Customers → external consumers
```

Key directories:
- **Root directory** - **PRIMARY LOCATION**: 200+ Python scripts (dashboards, utilities, AI tools)
  - `flask_dashboard.py`, `*_dashboard.py` - Streamlit/Flask analytics dashboards
  - `codex_unified_launcher.py` - CLI tool for treasury, dawn dispatch, system operations
  - `system_launcher.py` - Multi-dashboard launcher with port management
  - `codex_ledger.json`, `proclamations.json`, `cycles.json` - JSON-based data stores (legacy 1.0)
- `backend/` - NestJS TypeScript API (Civilization Era 2.0) at `/api/v1`
- `frontend/` - Next.js 14+ application (Empire Dashboard)
- `packages/` - Shared TypeScript packages (identity, ledger, workflow, finance, broadcast, shared-types)
- `infra/`, `k8s/`, `helm/` - Infrastructure manifests
- `.github/workflows/` - 40+ CI/CD workflows for multi-cloud deployment
- `api/`, `codex_capsules/` - Legacy FastAPI services (being phased out)

### Ceremonial Domain Model

The system uses a **"ledger"** data structure (`codex_ledger.json`) with sacred terminology:
- **proclamations** - system decrees/announcements
- **cycles** - operational phases with states (initiated/active/completed)
- **heartbeat** - system health status
- **omega_seal** - completion/authorization flag
- **portals** - interface gateways to subsystems
- **completed_archives** - historical records

Files ending in `_PROCLAMATION.md` or `_ETERNAL.md` are documentation artifacts reflecting this ceremonial style.

### Identity Architecture (Infrastructure Layer)

The system implements a **four-identity model** that determines user experience, access, and progression:

**The Four Identities:**
- **Diaspora** - Global community members (belonging) - receive cultural continuity, economic pathways
- **Youth** - Inheritors in training (becoming) - receive leadership development, curriculum, mentorship
- **Creator** - Builders and innovators (building) - receive tools, dashboards, workflows, revenue systems
- **Legacy-Builder** - Stewards and mentors (stewardship) - receive governance roles, cultural authority

**Identity Progression Model:**
```
Diaspora → Youth (age-eligible) → Creator → Legacy-Builder → Council/Custodian
```
Progression based on contribution, participation, leadership, mastery, and stewardship.

**Identity-Aware Systems:**
Every system (dashboards, workflows, curriculum, notifications, missions) uses identity detection and routing:
- Youth see youth content
- Creators see creator tools
- Diaspora see cultural content
- Legacy-Builders see stewardship frameworks

**Identity Engine (2.0)** handles:
- Detection (registration, onboarding, age/role-based logic)
- Routing (dashboard, curriculum, mission, content routing)
- Expansion (progression tracking, seasonal advancement)
- Integration (governance, culture, economics, operations)

When working with user-facing features, always consider which identity(ies) should access the functionality.

### Governance & Leadership (Stewardship Layer)

The Dominion operates on **stewardship-based governance** with seasonal rhythms rather than corporate calendars.

**Leadership Structure:**
- **The Council** - Primary leadership body with representatives from each identity (Youth, Creator, Diaspora, Legacy-Builder)
  - Upholds Constitution and cultural covenant
  - Guides seasonal missions and identity progression
  - Meets in alignment with seasonal cycles (Dawn/Day/Dusk/Night Council)
- **The Custodian** - Keeper of the flame, responsible for continuity and cultural coherence
  - Narrative, cultural, and constitutional authority
  - Guides Council through stewardship, not command
  - Succession based on stewardship, mastery, contribution
- **The Ambassadors** - External-facing leaders who carry the Dominion's voice to communities
  - Represent, teach curriculum, support circles, guide creators
- **The Circles** - Community units aligned by identity (Youth Circles, Creator Circles, Diaspora Circles, Legacy Circles)
  - Leadership development, curriculum delivery, community building

**Seasonal Governance Model:**
- **Dawn** (Vision) - Set goals, define missions, align identity pathways
- **Day** (Action) - Execute missions, run operations, support circles
- **Dusk** (Reflection) - Review outcomes, gather insights, refine systems
- **Night** (Renewal) - Reset, restore, prepare for next cycle

**Compliance & Audit Framework:**
Audits occur at end of each season, year, and major transitions:
- Identity audits, curriculum audits, financial audits, cultural audits, operational audits
- Ensures ethical stewardship, financial transparency, identity protection, cultural fidelity

**Leadership Roles (Operational Tier):**
- **Youth Captains** - Run Youth Circles, deliver curriculum, guide missions, track progression
- **Ambassadors** - Represent publicly, teach orientation, expand regional presence
- **Regional Directors** - Oversee circles, manage ambassadors, coordinate events, maintain quality
- **Creator Leaders** - Lead creator circles, mentor emerging creators, build cultural assets
- **Educators & Advisors** - Support curriculum, guide youth/creators, uphold continuity

**Leadership Principles (Non-Negotiable):**
1. Stewardship over authority - guide, protect, elevate (not dominate)
2. Identity before infrastructure - decisions must reinforce the four identities
3. Culture as first technology - rituals, stories, symbols before tools
4. Clarity over complexity - speak plainly, move intentionally
5. Continuity over urgency - build for generations, not moments

**Leadership Ascension Path:**
Initiate (learn Constitution/culture) → Steward (lead circles/missions) → Architect (build systems) → Director (oversee regions) → Custodian-Track (long-term stewardship)

**Leadership Oath:**
"I protect the flame. I uphold the culture. I guide with clarity. I build with excellence. I steward with humility. I serve the youth, creators, and diaspora. I move with the seasons. I honor the Dominion."

**Leadership Training Framework:**
Four-module mastery system ensures leaders can run circles, teach curriculum, and communicate with sovereignty
- **Module 1** - Identity & Culture Training (Four Identities, Cultural Covenant, Seasonal Rhythm)
- **Module 2** - Mission & Curriculum Training (Mission Engine, Curriculum Map, Circle Facilitation)
- **Module 3** - Communication & Brand Training (Dominion Voice, Brand Identity, Public Representation)
- **Module 4** - Leadership Execution Training (Weekly Rhythm, Reporting & Metrics, Leadership Scenarios)

Each module includes lessons, exercises, practice scenarios, and mastery checkpoints. Completion requires running one full circle/outreach event, one mission cycle, one cultural ritual, and creating one brand-aligned communication piece.

**Leadership Ascension Ceremony:**
Ritual marking transition from participant to civilization-bearer
- **Purpose**: Unify leaders under one culture, anchor in stewardship, connect to lineage
- **Structure**: Opening (flame lit) → Story of Ascension → Four Identities Invocation → Seasonal Invocation → Leadership Charge → Leadership Oath (spoken together) → Anointing of Roles → Passing of Flame → Closing
- **Setting**: Circle formation, flame symbol, Dominion symbols visible, intentional environment
- **Oath Recited**: "I carry the flame. I rise in identity, mastery, creation, and leadership. I serve my community. I protect our unity. I build our dominion. I lead with culture, purpose, and sovereignty."
- Can be held in physical circles, digital gatherings, retreats, or community spaces

When building governance features, align with seasonal rhythms and identity-based leadership roles.

### Cultural Core (Identity & Narrative Layer)

Culture is the Dominion's foundational technology—the stories, symbols, and rituals that give the system its soul and ensure continuity.

**Core Symbols (appear in UI, curriculum, dashboards, ceremonies):**
- **The Flame** - continuity, inheritance, sovereignty
- **The Circle** - unity, community, identity cycles
- **The Four Seasons** - operational rhythm
- **The Crown** - stewardship (not domination)
- **The Bridge** - diaspora connection

**Core Rituals (create behavioral rhythm):**
- Dawn Dispatch - daily alignment
- Circle Gathering - weekly community
- Seasonal Reset - quarterly renewal
- Custodian's Oath - leadership integrity
- Dominion Reflection - collective wisdom

**Story Types (integrated into curriculum, onboarding, dashboards):**
- Origin Stories, Diaspora Stories, Youth Stories, Creator Stories, Legacy Stories
- Stories transmit values, shape identity, and create emotional connection

**Seasonal Narratives:**
Each season has distinct narrative purpose and shapes all system features:
- **Dawn** (Vision) - clarity, intention, direction
- **Day** (Action) - building, executing, contributing
- **Dusk** (Reflection) - learning, reviewing, refining
- **Night** (Renewal) - rest, restoration, preparation

**The Dominion Voice (all communications follow these principles):**
- **Clarity** - no jargon, no confusion
- **Warmth** - human, grounded, welcoming
- **Sovereignty** - confident, intentional, dignified
- **Continuity** - always connected to the larger story

**Mythic Timeline (directional framework):**
- **1.0** - Origin Era (foundation, early architecture)
- **2.0** - Civilization Era (structure, identity, governance, culture) ← Current
- **3.0** - Network Era (global marketplace, economic engine, diaspora network)
- **4.0** - Legacy Era (generational institutions, academies, archives)

When writing UI copy, notifications, or user-facing content, maintain the Dominion Voice. Symbols should appear consistently across interfaces.

### Youth Empire (Development & Curriculum Layer)

Youth are the Dominion's inheritors—every system ultimately exists to strengthen the next generation. The Youth Empire is the structured, identity-aware system that develops young people into leaders, creators, and stewards.

**Youth Circle Curriculum:**
Leadership engine built around identity, culture, leadership, economics, creativity, community, and stewardship
- **Lessons** - foundational knowledge
- **Missions** - applied challenges and real-world impact
- **Reflections** - personal growth tracking
- **Gatherings** - community building
- **Seasonal Projects** - tangible contributions

**Four Seasons of Youth Development:**
- **Dawn** (Vision) - Self-awareness, identity, purpose, direction
- **Day** (Action) - Skill building, mission completion, circle contribution
- **Dusk** (Reflection) - Growth review, challenges, insights
- **Night** (Renewal) - Rest, reset, preparation for next cycle

**Leadership Tracks:**
- **Personal Leadership** - self-awareness, emotional intelligence, discipline, communication
- **Community Leadership** - teamwork, facilitation, conflict resolution, cultural stewardship
- **Creative Leadership** - innovation, storytelling, digital creation, entrepreneurship
- **Civic Leadership** - service, advocacy, community impact, diaspora engagement

**Integration Points:**
Designed to integrate with schools, after-school programs, community centers, youth groups, diaspora organizations
- Facilitator guides, lesson plans, mission kits, digital dashboards, identity assessments

**Youth Portfolio System:**
Living record of growth, identity, and leadership including:
- Mission completions, reflections, skills, leadership badges, seasonal achievements, creative work, community impact
- Serves as confidence builder, leadership resume, cultural archive, and bridge to Creator/Legacy-Builder identities

When building youth-facing features, prioritize accessibility, cultural grounding, and clear progression pathways.

### Creator Dominion (Builder Economy Layer)

Creators are architects of culture, commerce, and identity—not content producers. The Creator Dominion empowers builders to earn, grow, and ascend within the civilization.

**Creator Identity:**
Sovereign builders who embody innovation, cultural expression, economic agency, leadership, and craftsmanship

**Creator Tools (reduce friction, increase output):**
- Content creation workflows, AI-powered assistants, brand kits, storytelling frameworks
- Product templates, marketing scripts, revenue calculators, portfolio dashboards

**Creator Dashboard (command center):**
- Identity overview, content pipeline, product builder, revenue analytics, audience insights
- Mission tracker, seasonal goals, AI advisor

**Creator Workflows (seasonal alignment):**
- **Dawn** (Vision) - Define creative direction, set seasonal goals, plan product cycles
- **Day** (Action) - Create content, build products, engage audiences, collaborate with circles
- **Dusk** (Reflection) - Review analytics, refine strategy, gather feedback
- **Night** (Renewal) - Rest, reset, prepare for next cycle

**Creator Treasury (economic engine):**
- Revenue tracking, product sales, subscription management, affiliate pathways
- Grants/microfunds, creator-to-creator commerce

**Creator Ascension Path:**
1. Initiate (learning tools) → 2. Builder (consistent production) → 3. Architect (systems/products) → 4. Sovereign (circle leadership) → 5. Legacy-Builder (mentorship)
- Progression based on contribution, consistency, leadership, cultural alignment, economic impact

When building creator features, support workflows that prevent burnout and enable sustainable ascension.

### Operational Engine (Systems & Rhythms Layer)

The Dominion runs on clear, repeatable systems that turn intention into action and culture into continuity. The Operational Engine ensures every identity, circle, mission, and season moves with coherence.

**Core Systems Architecture:**
- **Dashboards** - Identity-aware command centers
- **Workflows** - Structured processes for creators, youth, leaders
- **Templates** - Standardized documents for consistency
- **Checklists** - Operational clarity for recurring tasks
- **Dispatch Cycles** - Daily, weekly, seasonal rhythms
- **Economic Engines** - Portfolio, markets, news systems
- **AI Advisors** - Intelligence layers supporting decisions

**Workflow Types:**
- Identity Workflows (onboarding, progression, advancement)
- Creator Workflows (content, product, revenue, collaboration)
- Youth Workflows (missions, reflections, portfolio updates)
- Leadership Workflows (council cycles, ambassador duties)
- Operational Workflows (dispatch, audits, resets)

**Template & Checklist System:**
Templates reduce friction and ensure quality; checklists prevent drift and ensure excellence
- Curriculum, mission, reflection, product, leadership, seasonal, audit, communication templates
- Daily, weekly, seasonal, mission, creator, youth, leadership checklists

**Three Primary Cycles:**
- **Daily** - Dawn Dispatch, identity tasks, creator actions, youth missions, operational updates
- **Weekly** - Circle gatherings, mission reviews, creator analytics, leadership syncs
- **Seasonal** - Vision setting, mission execution, reflection, renewal

**The Dawn Dispatch:**
Daily heartbeat message aligning identity, mission, culture, operations, and focus—ensures every member starts the day with clarity and purpose

**Dominion Dashboard (Master Command Center):**
- **Tech Stack**: Flask (Python backend), Next.js (React frontend), PostgreSQL, AI integrations (OpenAI/Anthropic)
- **Features**: Identity-aware routing, creator tools, youth missions, portfolio analytics, markets data, news intelligence, seasonal progress, AI advisor, treasury overview
- **Entry Point**: `flask_dashboard.py` (Port 5000) with 52+ integrated dashboards
- **Deployment**: Multi-cloud (Azure primary, GCP, IONOS)

**Community Onboarding (Transition & Activation):**
Structured 7-day "Rise Path" for welcoming new members into the Civilization Era
- **Day 1-2**: Identity discovery (Youth/Creator/Diaspora/Legacy-Builder), cultural foundations (Flame, Circle, Crown, Seasons)
- **Day 3-4**: Mission overview, Circle joining
- **Day 5-6**: First mission step, reflection with Circle
- **Day 7**: Citizen's Oath - "I rise with my identity. I honor my community. I carry the flame. I build with purpose. I walk with unity. I grow with the seasons. I am part of the Dominion."
- **Orientation Experience**: 20-minute intro covering story, four identities, seasonal rhythm, first steps
- **Mission Structure**: Week 1 (Story+Lesson) → Week 2 (Action) → Week 3 (Circle Dialogue) → Week 4 (Showcase+Reflection)

When building operational features, prioritize clarity, repeatability, and seasonal alignment. All workflows should support the daily/weekly/seasonal rhythm.

### Economic Layer (Financial Intelligence & Markets)

The Dominion's economic system is empowerment-focused, not extractive. It's a structured, identity-aware financial nervous system that blends culture, intelligence, and technology.

**Portfolio Architecture (Personal Wealth Engine):**
- Portfolio creation, holdings tracking, trade history, risk profiles, performance analytics, AI-powered insights
- **Identity Integration**: Youth (simplified dashboards, financial literacy), Creators (revenue-linked portfolios), Diaspora (long-term strategies), Legacy-Builders (generational planning)
- Teaches not just investing, but legacy building

**Markets Architecture (Intelligence Layer):**
- Real-time stock data, sector heatmaps, market movers, volatility alerts, earnings calendars
- **Cultural Alpha Engine**: Analyzes cultural trends, diaspora influence, creator movements, youth sentiment, global narratives
- Culture becomes a market signal

**News Architecture (Information Filter):**
- Verified news streams, timeline-based filtering, identity-aware recommendations, cultural context overlays
- AI-powered summaries, misinformation detection
- **Identity-Aware**: Youth (simplified educational), Creators (industry insights), Diaspora (global updates), Legacy-Builders (long-term analysis)
- Ensures informed decision-making without information overload

**Cultural Alpha Engine (Signature Innovation):**
- Transforms cultural patterns into economic insight
- **Inputs**: Diaspora trends, creator movements, youth sentiment, cultural narratives, global events
- **Outputs**: Market signals, product opportunities, creator trends, community insights, economic forecasts
- Culture → Data → Strategy → Sovereignty

**Revenue Streams (Sustainable & Generational):**
- Creator products, youth programs, digital courses, subscriptions, marketplace fees, partnerships, cultural alpha insights, community events
- Revenue supports continuity, not extraction

**Marketplace Vision (3.0 Era):**
Global, identity-aware economic ecosystem with creator storefronts, youth products, diaspora goods, digital assets, cultural alpha insights, community commerce

When building economic features, integrate identity awareness and prioritize financial literacy for all users, especially youth.

### Brand & Messaging System (Voice & Identity Layer)

Brand is identity made visible—culture made legible. The Brand & Messaging System ensures every touchpoint speaks with one unified, sovereign voice.

**The Dominion Identity (Four Pillars):**
- **Sovereignty** - Build systems that empower, not extract
- **Clarity** - Speak plainly, move intentionally, design with purpose
- **Warmth** - Welcome, uplift, humanize every interaction
- **Continuity** - Build for generations, not moments

**Visual Language:**
Designed to feel modern, ancestral, sovereign, warm, and structured
- **Core Elements**: The Flame (continuity), The Circle (unity), The Crown (stewardship), The Seasons (rhythm), The Bridge (diaspora connection)
- **Color System**: Earth, fire, dusk, dawn, night—cultural, grounded, timeless palette

**Naming Conventions (Structured Patterns):**
- **Identity Names**: Youth Circle, Creator Dominion, Diaspora Network, Legacy Path
- **System Names**: Dawn Dispatch, Cultural Alpha Engine, Dominion Dashboard, Seasonal Reset
- **Ceremonial Names**: Custodian's Oath, Circle Gathering, Sovereign Reflection
- Names chosen for clarity, resonance, and continuity

**Messaging Pillars (Reinforce Purpose):**
- **Pillar I** - Identity (who you are inside the Dominion)
- **Pillar II** - Culture (stories, symbols, rituals that bind)
- **Pillar III** - Sovereignty (systems that empower)
- **Pillar IV** - Continuity (generational mission)

**Public Narrative:**
"We are building a sovereign civilization for youth, creators, and the global diaspora—one that blends culture, identity, and technology into a generational engine."
- Appears in: announcements, onboarding, curriculum, dashboards, partnerships, public materials
- Mythic yet grounded, aspirational yet actionable

**Launch Framework (Seasonal Rhythm):**
- **Dawn** (Reveal) - Announce vision, share story, introduce identity
- **Day** (Activation) - Release tools, run missions, engage community
- **Dusk** (Reflection) - Gather insights, refine system, celebrate progress
- **Night** (Renewal) - Rest, reset, prepare for next cycle
- Launches become cultural events, not just product releases

When creating public-facing content, maintain the four identity pillars and use naming conventions consistently. All launches follow the seasonal rhythm.

### Master Archive (Documentation & Continuity Layer)

A civilization survives through memory—not just stories, but structured documentation. The Master Archive preserves the Dominion's past, organizes its present, and prepares its future.

**CodexDominion 1.0 Artifacts (Origin Era):**
Foundational documents from the birth of the Dominion
- Early youth empowerment notes, diaspora mission drafts, creator empowerment concepts
- Cultural stories and symbols, operational sketches, brand fragments
- Early dashboards, pre-2.0 workflows, naming experiments, leadership reflections
- Preserved for historical continuity and cultural grounding—honored, not overwritten

**CodexDominion 2.0 Artifacts (Civilization Era - Current):**
The structured, unified, identity-aware systems defining the present
- Constitution, Identity Charter, Cultural Covenant
- Youth Circle Curriculum, Creator Dominion Framework, Governance Model
- Seasonal System, Operational Engine, Economic Layer, Brand & Messaging System
- Dominion Dashboard architecture, Cultural Alpha Engine
- These form the living structure of the Dominion

**Retired Documents (Archived Lineage):**
Growth requires evolution—outdated systems are archived, not deleted
- Outdated naming conventions, redundant documents, early drafts replaced by 2.0
- Pre-2.0 identity models, legacy workflows, deprecated rituals
- Remain part of the Dominion's lineage for historical reference

**Eternal Documents (Timeless Artifacts):**
Some artifacts transcend eras—they are the Dominion's soul
- Diaspora Mandate, Custodian's Oath, Flame Symbol, Circle Symbol
- Seasonal Rhythm, Dominion Voice, Sovereign Law, Cultural Virtues
- These never retire

**Future Expansion Notes (3.0 & 4.0 Horizon):**
The Dominion always has a horizon
- **3.0** - Network Era (marketplace, global partnerships, creator engines)
- **4.0** - Legacy Era (academies, cultural institutions, multi-region hubs)
- AI-powered identity systems, governance evolution

When working with documentation, respect the archive structure. 1.0 artifacts inform context, 2.0 artifacts are current implementation, Eternal artifacts are immutable principles.

### The Eternal Appendix (Reference & Structural Memory)

The Dominion's reference layer—definitions, symbols, maps, and timelines that ensure clarity and continuity for all who enter the civilization.

**Glossary (Core Terms):**
- **Dominion** - Sovereign civilization built for youth, creators, and diaspora
- **Custodian** - Steward of the Dominion's identity and continuity
- **Council** - Leadership circle guiding the Dominion through each season
- **Circle** - Community unit aligned with identity and mission
- **Identity Engine** - System that personalizes experiences across the Dominion
- **Seasonal Rhythm** - Four-phase cycle (Dawn, Day, Dusk, Night)
- **Cultural Alpha** - Economic insight derived from cultural patterns
- **Dawn Dispatch** - Daily alignment ritual
- **Youth Portfolio** - Record of youth growth and leadership
- **Creator Treasury** - Economic engine for creators
- **Master Archive** - Historical and structural memory

**Symbols Index (Visual Language):**
- **Primary**: The Flame (continuity), The Circle (unity), The Crown (stewardship), The Bridge (diaspora), The Seasons (rhythm)
- **Secondary**: The Path (progression), The Loom (culture), The Compass (direction)
- Appear in curriculum, dashboards, rituals, public identity

**Identity Map (Progression Flow):**
```
Diaspora (belonging) → Youth (becoming) → Creator (building) → 
Legacy-Builder (stewarding) → Council (guiding) → Custodian (protecting)
```

**Seasonal Map (Operational Rhythm):**
- **Dawn** - Set goals, define missions, align identity
- **Day** - Execute, build, contribute
- **Dusk** - Review, refine, learn
- **Night** - Rest, reset, prepare
- Governs curriculum, governance, workflows, missions, operations

**Dominion Timeline (Eras):**
- **1.0** - Origin Era (spark, foundation, early architecture)
- **2.0** - Civilization Era (structure, identity, governance, culture) ← Current
- **3.0** - Network Era (marketplace, economic engine, global network) ← Future
- **4.0** - Legacy Era (institutions, academies, archives, generational systems) ← Future

**Custodian Principles (Guiding Reminders):**
- Protect the flame, build for generations
- Culture is the first technology, identity is the foundation
- Governance must remain cyclical, not static
- Youth are inheritors—center them; Creators are builders—empower them; Diaspora is family—honor them
- Stewardship is sacred—lead with clarity and humility

Use this reference when encountering unfamiliar terms, understanding progression paths, or aligning features with seasonal rhythms.

## Technology Stack

### Frontend
- **Next.js 14+** (App Router, TypeScript) - Empire Dashboard and web interface
- Located in `frontend/` directory
- Consumes REST API from NestJS backend
- Type-safe API client wrappers in `frontend/src/lib/`

### Backend (Civilization Era 2.0)
- **NestJS** (Node.js, TypeScript) - Primary REST API at `/api/v1`
- **Modular Architecture**: Separate modules for auth, users, profiles, seasons, missions, circles, curriculum, culture, creators, regions, events, analytics
- **JWT Authentication**: Access + refresh tokens with role-based guards
- **Swagger Docs**: Auto-generated from decorators at `/api-docs`
- Located in `backend/` directory

### Legacy Systems (1.0 Era)
- **FastAPI** (Python 3.10+) - Legacy API services in `api/`, `codex_capsules/`
- **Streamlit** (1.28+) - Analytics dashboards (`*_dashboard.py` files at root)
- Being phased out in favor of NestJS backend

### Infrastructure
- **Docker Compose** - PostgreSQL for local dev (`backend/docker-compose.yml`), production configs
- **Kubernetes/Helm** - Charts in `helm/codexdominion/`, manifests in `k8s/`
- **Terraform** - IaC in root (`.tf` files)
- **Multi-cloud**: Azure (primary), GCP (Cloud Run/Functions), IONOS VPS

### Data & State
- **PostgreSQL** (Civilization Era 2.0) - Primary database with Prisma ORM
- **Prisma Schema**: Located at `backend/prisma/schema.prisma` (20+ models)
- **Migrations**: Database versioning in `backend/prisma/migrations/`
- **Seeding**: Initial data setup in `backend/prisma/seed.ts`
- **JSON Ledgers** (Legacy 1.0): `codex_ledger.json`, `proclamations.json`, `cycles.json` - Being migrated to PostgreSQL

**2.0 Database Schema (Prisma/PostgreSQL):**
The Civilization Era introduces structured relational data with the following core entities:

**Phase 1 Models (Implement First):** User, Profile, UserRole, Season, Mission, MissionAssignment, MissionSubmission, Circle, CircleMember, CircleSession, SessionAttendance, CulturalStory, MetricSnapshot

**Phase 2+ Models (Future):** CurriculumModule, Artifact, CreatorChallenge, ChallengeSubmission, Ritual, Region, School, AmbassadorOutreach, Event, EventAttendance
- **User** - Identity foundation with roles (YOUTH, YOUTH_CAPTAIN, AMBASSADOR, CREATOR, EDUCATOR, REGIONAL_DIRECTOR, COUNCIL, ADMIN)
- **Profile** - Extended user data including `risePath` (IDENTITY, MASTERY, CREATION, LEADERSHIP), cultural identity, diaspora origin
- **Circle** - Youth community units with captain, members, sessions, and attendance tracking
- **Season** - Seasonal rhythm (IDENTITY, MASTERY, CREATION, LEADERSHIP) driving missions, curriculum, challenges
- **Mission** - Mission Engine with assignments, submissions, and status tracking (GLOBAL, REGIONAL, CIRCLE types)
- **CurriculumModule** - Lesson content (STORY, LESSON, ACTIVITY) with resources
- **Artifact** - Creator outputs (AUTOMATION, DESIGN, WRITING, VIDEO, APP) linked to challenges
- **CreatorChallenge** - Seasonal creator challenges with submissions
- **CulturalStory** - Narrative content tied to seasons and regions
- **Region** - Geographic units with directors, schools, circles, and outreach
- **Event** - Ceremonies, launches, summits, training sessions
- **MetricSnapshot** - Analytics tracking (ACTIVE_YOUTH, MISSIONS_COMPLETED, ARTIFACTS_SUBMITTED, etc.)

Schema location: `schema.prisma` (Prisma ORM)  
Key patterns: Identity roles drive access, seasonal cycles organize content, missions link users→circles→submissions, artifacts link creators→challenges

## NestJS Backend Architecture

### Module Structure (Civilization Era 2.0)

The backend follows NestJS modular architecture with domain-driven design:

```
backend/src/
├── auth/               # JWT authentication (access + refresh tokens)
├── users/              # User management and roles
├── profiles/           # Extended user profiles (risePath, cultural identity)
├── seasons/            # Seasonal rhythm engine (Dawn/Day/Dusk/Night)
├── missions/           # Mission Engine (global, regional, circle missions)
├── circles/            # Youth Circles (creation, membership, sessions, attendance)
├── curriculum/         # Curriculum modules by season/week
├── culture/            # Cultural stories, rituals, symbols
├── creators/           # Creator artifacts, challenges, submissions
├── regions/            # Geographic units, schools, ambassador outreach
├── events/             # Launches, ceremonies, summits, training
├── analytics/          # System metrics and insights
├── common/             # Shared guards, interceptors, decorators, DTOs
├── main.ts             # Application entry point
└── app.module.ts       # Root module
```

### Key Patterns

**Identity-Aware Guards:**
```typescript
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles(UserRole.YOUTH_CAPTAIN, UserRole.AMBASSADOR)
export class CirclesController {
  // Only Youth Captains and Ambassadors can access
}
```

**Seasonal Context Injection:**
```typescript
@Injectable()
export class MissionsService {
  async getCurrentMission(@CurrentSeason() season: Season) {
    // Auto-injected current season from decorator
  }
}
```

**Module Dependencies:**
- **AuthModule** → Used by all protected routes
- **UsersModule** → Exports UsersService for profile/circle membership
- **SeasonsModule** → Provides current season context globally
- **CommonModule** → Shared utilities, guards, decorators

### API Versioning

All endpoints prefixed with `/api/v1`:
- `/api/v1/auth/register`
- `/api/v1/missions/current`
- `/api/v1/circles/{id}/sessions`

### Swagger Documentation

Auto-generated at `/api-docs` from NestJS decorators:
```typescript
@ApiTags('missions')
@ApiBearerAuth()
export class MissionsController {
  @ApiOperation({ summary: 'Get current mission for user' })
  @ApiResponse({ status: 200, type: Mission })
  @Get('current')
  async getCurrent() { }
}
```

### Environment Configuration

`backend/.env.example`:
```
DATABASE_URL="postgresql://codex:codex@localhost:5432/codexdominion"
JWT_SECRET="super-secret-dev-key"
JWT_REFRESH_SECRET="another-secret-key"
JWT_EXPIRATION=15m
JWT_REFRESH_EXPIRATION=7d
PORT=4000
```

## Phase 1 Implementation (MVP Scope)

**CRITICAL**: Phase 1 implements ONLY these engines. Everything else waits for Phase 2+.

### Phase 1 Engines
- **Auth & Identity** - Registration, login, JWT tokens, role-based access
- **Seasons & Missions** - Current season, mission listing, submissions
- **Youth Circles** - Creation, membership, sessions, attendance tracking
- **Culture** - Current story and story listing
- **Analytics** - High-level overview dashboard
- **Minimal Admin** - Mission/circle/story creation for admins

### Phase 1 Endpoints (Backend)

**Auth & Identity:**
- `POST /auth/register` - Create new user account
- `POST /auth/login` - Authenticate and get tokens
- `POST /auth/refresh` - Refresh access token
- `GET /users/me` - Get current user profile
- `PATCH /users/me` - Update current user
- `GET /profiles/me` - Get extended profile
- `PATCH /profiles/me` - Update profile (risePath, cultural identity)

**Seasons & Missions:**
- `GET /seasons` - List all seasons
- `GET /seasons/current` - Get current active season
- `GET /missions` - List missions (filterable by season_id, month)
- `GET /missions/current` - Get mission for current week/season
- `GET /missions/:id` - Get specific mission
- `POST /missions` - Create mission (ADMIN only)
- `POST /missions/:id/assign` - Assign mission to user/circle (ADMIN/YOUTH_CAPTAIN)
- `POST /mission-submissions` - Submit mission work
- `GET /mission-submissions` - List submissions (filter by mission_id, circle_id)

**Youth Circles:**
- `GET /circles` - List all circles
- `POST /circles` - Create circle (ADMIN/AMBASSADOR)
- `GET /circles/:id` - Get circle details
- `PATCH /circles/:id` - Update circle (captain, name, region)
- `POST /circles/:id/members` - Add member to circle
- `DELETE /circles/:id/members/:user_id` - Remove member from circle
- `GET /circles/:id/sessions` - List circle sessions
- `POST /circles/:id/sessions` - Create session
- `POST /circles/:id/sessions/:session_id/attendance` - Record attendance

**Culture:**
- `GET /culture/story/current` - Get current week's cultural story
- `GET /culture/stories` - List stories (filter by season_id)
- `POST /culture/stories` - Create story (ADMIN/COUNCIL)

**Analytics:**
- `GET /analytics/overview` - High-level dashboard (active youth, circles, missions completed, regions)

**Out of Scope for Phase 1:**
- Curriculum modules (endpoints exist in spec but not implemented)
- Creator artifacts and challenges
- Regions, schools, ambassador outreach
- Events and ceremonies
- Advanced analytics beyond overview

### Auth Implementation Strategy

**Token Architecture:**
- **Access Token**:
  - JWT, short-lived (15-30 minutes)
  - Stored in memory/localStorage on frontend
  - Sent as `Authorization: Bearer <token>` header
  - Contains: user_id, email, roles, exp
- **Refresh Token**:
  - Longer-lived (7-30 days)
  - Stored in database `refresh_tokens` table (Phase 1), migrate to HTTP-only cookies later
  - Returned in login/register response body
  - Used only for `/auth/refresh` endpoint

**Login/Register Flow:**
```typescript
// POST /auth/register
1. Validate input (email unique, password strength)
2. Hash password with bcrypt (salt rounds: 10)
3. Create User record with status: ACTIVE
4. Create Profile record with default risePath: IDENTITY
5. Assign default role: YOUTH
6. Generate access token + refresh token
7. Store refresh token in DB
8. Return { user, accessToken, refreshToken }

// POST /auth/login
1. Find user by email
2. Verify password with bcrypt.compare
3. Generate new access token + refresh token
4. Store new refresh token in DB (invalidate old ones optional)
5. Return { user, accessToken, refreshToken }

// POST /auth/refresh
1. Verify refresh token exists in DB and not expired
2. Issue new access token
3. Optionally rotate refresh token
4. Return { accessToken, refreshToken? }
```

**Role-Based Access Control:**
```typescript
// Use NestJS decorators for authorization
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('ADMIN')
@Post('/missions')
createMission() {
  // Only ADMIN can create missions
}

@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('ADMIN', 'YOUTH_CAPTAIN')
@Post('/missions/:id/assign')
assignMission() {
  // ADMIN or YOUTH_CAPTAIN can assign missions
}

// Custom RolesGuard implementation
@Injectable()
export class RolesGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.get<string[]>('roles', context.getHandler());
    if (!requiredRoles) return true;
    
    const request = context.switchToHttp().getRequest();
    const user = request.user; // Injected by JwtAuthGuard
    
    return requiredRoles.some(role => user.roles?.includes(role));
  }
}
```

**Password Security:**
- Use `bcrypt` with 10 salt rounds minimum
- Never store plaintext passwords
- Password requirements: min 8 characters (enforce at validation layer)

**JWT Payload Structure:**
```typescript
interface JwtPayload {
  sub: string;        // user_id (UUID)
  email: string;
  roles: UserRole[];  // Array of assigned roles
  iat: number;        // Issued at timestamp
  exp: number;        // Expiration timestamp
}
```

## Development Workflows

### Primary Entry Points

**CRITICAL**: Always activate virtual environment first:
```powershell
# Windows
.venv\Scripts\activate.ps1

# Linux/Mac  
source .venv/bin/activate
```

**Master Dashboard (PRIMARY INTERFACE)** - Flask with 52+ integrated dashboards:
```powershell
.\START_DASHBOARD.ps1
# OR
python flask_dashboard.py  # Port 5000
```

**Unified CLI Tool** - Treasury, dawn dispatch, and system operations:
```bash
python codex_unified_launcher.py treasury summary --days 30
python codex_unified_launcher.py treasury ingest --stream affiliate --amount 49.99
python codex_unified_launcher.py dawn dispatch
python codex_unified_launcher.py status    # Health check
python codex_unified_launcher.py serve     # Web API on port 8080
```

**System Launcher** - Multi-dashboard launcher with port management:
```python
python system_launcher.py  # Interactive menu for all dashboards
python LAUNCH_SYSTEM.py    # Alternative unified launcher
```

### Running Locally

**NestJS Backend (Civilization Era 2.0):**
```bash
cd backend

# Copy environment variables
cp .env.example .env
# Edit .env with your actual values (DATABASE_URL, JWT secrets)

# Start PostgreSQL
docker-compose up -d postgres

# Install dependencies
npm install  # Note: Uses npm, not pnpm (package-lock.json present)

# Run Prisma migrations
npm run prisma:generate
npm run prisma:migrate

# Seed database (optional)
npm run db:seed

# Start development server
npm run start:dev  # Port 4000 with hot reload (configurable via PORT env var)

# View Swagger docs at http://localhost:4000/api-docs
```

**Next.js Frontend (Empire Dashboard):**
```bash
cd frontend

# Copy environment variables
cp .env.local.example .env.local
# Edit .env.local with API URL and other config

npm install  # Note: Uses npm (package-lock.json present)
npm run dev  # Development server on http://localhost:3000
npm run build  # Production build
npm run export  # Static export for deployment
```

**Legacy Python Dashboards (1.0 Era):**
```bash
# Use Python environment tool first
python -m streamlit run app.py
streamlit run codex_dashboard.py --server.port 8501
python flask_dashboard.py  # Port 5000
```

**Full Stack (Docker):**
```bash
# NestJS + PostgreSQL + Next.js
cd backend
docker-compose up -d

# Legacy stack
docker-compose -f docker-compose.production.yml up
```

### Testing

**NestJS Backend:**
```bash
cd backend
npm run test           # Unit tests
npm run test:e2e       # End-to-end tests
npm run test:cov       # Coverage report
```

**Frontend:**
```bash
cd frontend
npm test               # Jest tests
```

**Legacy Systems:**
- **Python**: Tests in `tests/` directories (unit, integration)
- Run per-language/framework as needed

### Deployment

**Critical**: This project has 40+ GitHub Actions workflows. Key workflows:
- `deploy-complete-frontend.yml` - Deploys Next.js to Azure Static Web Apps
- `deploy-backend.yml`, `backend-deploy.yml` - API services
- Multi-cloud workflows for GCP, IONOS, Azure

**Common deployment commands:**
```powershell
# Windows PowerShell scripts at root:
.\deploy-codex.ps1
.\deploy-azure-production.ps1
.\deploy-ionos-production.ps1

# Bash alternatives:
bash deploy-ionos.sh
bash deploy-gcp.sh
```

**Azure Functions**: Subdirectory `recent_uploads/configs` has Azure Functions tooling. Use task `func: host start` (depends on pip install task).

### Service Management

Windows service scripts (PowerShell): `*-service-manager.ps1`, `systemctl-win.ps1`
Linux systemd units: `.service` and `.timer` files at root

## Project-Specific Conventions

### Critical Reality Check

**IMPORTANT**: This is a **massive monorepo** with 200+ Python scripts at the root level. The ceremonial "Council Seal" architecture described earlier is aspirational/conceptual - the actual file structure is a flat hierarchy with heavy Python usage.

**Actual Structure:**
- Root directory contains the bulk of executable code (Python dashboards, utilities, AI agents)
- `backend/` is NestJS (TypeScript) - modern API layer (2.0 era)
- `frontend/` is Next.js (TypeScript) - web interface (primary)
- `web/` is Next.js (TypeScript) - alternative frontend (legacy/parallel implementation)
- `packages/` contains shared TypeScript libraries
- Everything else (API services, legacy systems, infrastructure) coexists at various levels

**Navigation Strategy:**
- Use `grep_search` heavily - files are not deeply nested
- Dashboard files: `*_dashboard.py`, `flask_dashboard.py`
- Launcher files: `*_launcher.py`, `system_launcher.py`, `LAUNCH_*.bat`, `launch*.py`
- Config files: `*_config.json`, `.env*`, `config/*.json`
- Deployment: `deploy-*.ps1`, `deploy-*.sh`

### Naming Patterns
- **Ceremonial files**: `*_PROCLAMATION.md`, `*_ETERNAL_*.md`, `*_CHARTERED_*.md` are documentation
- **Dashboard scripts**: `*_dashboard.py` (Streamlit apps)
- **Config files**: `*_config.json` (affiliate, pinterest, tiktok, whatsapp, woocommerce configs)
- **Deployment scripts**: `deploy-*.ps1`, `deploy-*.sh`, prefixed with target platform

### Code Organization
- **NestJS Backend**: Modular architecture in `backend/src/` with domain modules
- **Module pattern**: Each domain (auth, missions, circles) has its own module, controller, service, entities
- **Shared code**: Common guards, decorators, DTOs in `backend/src/common/`
- **Prisma integration**: Schema at `backend/prisma/schema.prisma`, auto-generated client
- **TypeScript paths**: Use `@/*` aliases (configured in `backend/tsconfig.json`)
- **Frontend**: Next.js App Router in `frontend/src/` with API client wrappers
- **Legacy monorepo**: `apps/*` and `packages/*` (being phased out)
- **Shared types**: Generated from Prisma schema, shared between backend and frontend

### Data Access Patterns
```python
# Loading ledger (standard pattern):
import json
with open("codex_ledger.json", "r") as f:
    data = json.load(f)

# Updating with metadata:
data["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
with open("codex_ledger.json", "w") as f:
    json.dump(data, f, indent=2)
```

### Environment Variables
- Multiple `.env` files: `.env`, `.env.production`, `.env.azure-subscription2`, `.env.ionos.example`
- No unified `.env` - check per-service directory
- Azure secrets: Use GitHub secrets `AZURE_STATIC_WEB_APPS_API_TOKEN`, stored in `.github-secrets/`

## Key Integration Points

### Multi-Cloud Architecture
- **Azure**: Static Web Apps (frontend), Container Instances (backend)
- **GCP**: Cloud Run, Cloud Functions (`cloud-function/`, `app.yaml` for Python 3.9)
- **IONOS**: VPS deployment via SSH (`IONOS_SERVER`, `IONOS_USER` env vars)

### External Services
- **Stripe**: Payment integration (`STRIPE_*` env vars, `treasury_config.json`)
- **WooCommerce**: E-commerce backend (`woocommerce_config.json`, `woocommerce_sync.py`)
- **Social platforms**: Pinterest, TikTok, Threads, YouTube, WhatsApp (dedicated `*_config.json` files)
- **Stock APIs**: Alpha Vantage, Polygon for `ai_action_stock_analytics.py`

### Service Communication
- **API Gateway**: Node.js proxy at port 8080 (`api-gateway` service)
- **Dashboard ports**: 3000 (main), 8515 (stocks), 8516 (analytics), 8517+ (various dashboards)
- **Redis**: Optional caching layer (`REDIS_URL` in docker-compose)

## Common Tasks

### Adding a New Dashboard
1. Create `new_feature_dashboard.py` at root
2. Import streamlit: `import streamlit as st`
3. Load ledger: `data = load_ledger()` (see `app.py` for pattern)
4. Add to `docker-compose.production.yml` with unique port
5. Update nginx config if deploying to IONOS

### Modifying Ledger Schema
1. Update `codex_ledger.json` structure
2. Check dependent scripts: `grep -r "codex_ledger.json" *.py`
3. Ensure `meta.last_updated` timestamp is always updated
4. Consider backward compatibility - many scripts read this file

### CI/CD Changes
- Workflows trigger on `push` to `main` or `workflow_dispatch`
- Path filters prevent unnecessary runs (e.g., `paths: ['frontend/**']`)
- Secrets required: Check `.github/SECRETS.md` for setup
- Test locally before pushing: Use `act` or manual workflow_dispatch

### Infrastructure Updates
- Docker images: `jmerritt48/*` on Docker Hub (see `docker-compose.production.yml`)
- Kubernetes: Apply with `kubectl apply -f k8s/` or use Helm charts in `helm/codexdominion/`
- Terraform: State in `.terraform/` - use `terraform plan` before `apply`

## Debugging Tips

### Streamlit Issues
- Check port conflicts: Multiple dashboards run simultaneously
- Session state: Use `st.session_state` for state management
- Caching: `@st.cache_data(ttl=300)` pattern (see `enhanced_*_dashboard.py` files)

### Next.js Build Failures
- Static export requires `next.config.js` with `output: 'export'`
- API routes not supported in static export mode
- Check `frontend/out/` directory after build

### Deployment Failures
- **Azure**: Check Static Web App token in GitHub secrets
- **GCP**: Ensure `gcloud` CLI authenticated and project set
- **IONOS**: Verify SSH key and server access before deploy scripts
- **Docker**: Check image names/tags match in compose files

### Ledger Data Corruption
- Backups: `*.backup_*` files (timestamped) exist for ledger files
- Restoration: `restore_proclamations.py`, `smart_archiver.py` scripts
- Validation: `validate_proclamations.py` checks schema integrity

## Documentation References

- [ARCHITECTURE.md](../ARCHITECTURE.md) - Detailed Council Seal structure
- [README.md](../README.md) - Production launch guide
- [QUICK_START.md](../QUICK_START.md) - Deployment commands
- [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md) - Multi-cloud deployment
- Individual README.md files in `packages/*/`, `frontend/`, `infra/`, `tests/`

## Important Gotchas

1. **Ceremonial naming**: Don't refactor `*_PROCLAMATION.md` or ledger terminology without understanding impact
2. **JSON ledgers are source of truth**: Not a traditional database - many scripts depend on exact schema
3. **Multi-language**: Python and TypeScript coexist - use appropriate tooling per file type
4. **Port management**: 20+ services can run simultaneously - track port allocations
5. **Windows paths**: Use backslashes in PowerShell, forward slashes in WSL/Git Bash
6. **Azure Functions require Python 3.9**: Check `app.yaml` runtime version
7. **No single entry point**: Multiple launcher scripts (`launch*.py`, `*.ps1`) - choose correct one for context
