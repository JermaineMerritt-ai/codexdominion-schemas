# 🇧🇧 Barbados Government Dashboard — Technical Specification

**National Command Interface for Youth Development Intelligence**

**Status**: Technical Specification — Ready for Frontend Implementation  
**Date**: December 30, 2025  
**Target Users**: Government of Barbados (Ministries + National Programs)  
**Architecture**: Next.js Frontend + NestJS Backend + Intelligence API V1

---

## Executive Summary

The **Barbados Government Dashboard** is the sovereign control room for national youth development — a single pane of glass integrating:
- 7 Core Engines (Youth, Circle, Mission, Curriculum, Culture, Creator, Expansion)
- 6 Government Engines (Global Gov, Education & Workforce, Cultural Diplomacy, Biotech, Public Health, Economic Dev)
- Intelligence API V1 (47-rule system across 7 domains)
- National programs (Youth Circles, Creator Challenge, Biotech Lab, Diaspora Bridge, Workforce Accelerator)
- Real-time analytics and forecasts

**This is not a dashboard. This is a national operating system interface.**

---

## I. Dashboard Architecture

### Technical Stack

**Frontend**:
- Framework: Next.js 14+ (App Router, TypeScript)
- UI Library: Tailwind CSS + shadcn/ui components
- Charts: Recharts or Chart.js
- Maps: Mapbox or Leaflet (parish boundaries)
- State: React Context + React Query (API caching)

**Backend Integration**:
- API: NestJS REST API at `/api/v1/*`
- Auth: JWT with role-based access (ADMIN, COUNCIL roles for government users)
- Intelligence: `/intelligence/feed`, `/intelligence/alerts`, `/intelligence/recommendations`, `/intelligence/forecasts`, `/intelligence/opportunities`
- Analytics: `/analytics/overview`, `/analytics/regions`, `/analytics/missions`, `/analytics/circles`, `/analytics/dashboard`
- Domain APIs: `/circles`, `/missions`, `/schools`, `/regions`, `/ambassador-outreach`, `/culture/stories`, `/artifacts`, `/creator-challenges`

**Data Sovereignty**:
- All data filtered by `country_id = "barbados"` or `region_id IN (barbados_regions)`
- Role-based scoping: Government users see national data (global scope within Barbados)
- Privacy: Aggregated insights only (no individual youth data exposed without consent)

---

### Role-Based Access Control

**Government Role Types**:

| Role | Access Level | Scope | Panels Visible |
|------|--------------|-------|----------------|
| **GOVERNMENT_ADMIN** | Full national access | All Barbados data | All 11 panels |
| **MINISTRY_DIRECTOR** | Ministry-specific | Ministry programs + national overview | Panels 1, 2, 3, 11 + ministry-specific panels |
| **PROGRAM_MANAGER** | Program-specific | Single program data | Panels 1, 2 (filtered to program) |
| **REGIONAL_COORDINATOR** | Region-specific | Parish/region data | Panels 1, 3, 4 (region-scoped) |

**Implementation**:
```typescript
// JWT payload includes:
interface GovernmentUser {
  user_id: string;
  roles: ['GOVERNMENT_ADMIN' | 'MINISTRY_DIRECTOR' | 'PROGRAM_MANAGER'];
  ministry_id?: string; // If ministry-scoped
  program_ids?: string[]; // If program-scoped
  region_ids?: string[]; // If region-scoped
  country_id: 'barbados';
}
```

---

## II. The 11 Dashboard Panels

### Panel 1: National Intelligence Feed

**Purpose**: Real-time national heartbeat showing rising trends, declining metrics, urgent issues, and emerging opportunities.

**API Endpoints**:
```typescript
GET /api/v1/intelligence/feed
  ?limit=20
  &country_id=barbados
  &status=ACTIVE
  &priority=CRITICAL,IMPORTANT

// Example response:
{
  "insights": [
    {
      "id": "uuid",
      "type": "ALERT",
      "domain": "CIRCLES",
      "priority": "CRITICAL",
      "title": "Youth engagement dropped 12% in two parishes",
      "message": "Christ Church and St. Philip show declining attendance...",
      "context": {
        "regions": ["christ_church", "st_philip"],
        "attendance_drop_percent": 12,
        "affected_circles": 8
      },
      "audience_role": "GOVERNMENT_ADMIN",
      "created_at": "2025-12-30T10:00:00Z"
    },
    {
      "id": "uuid",
      "type": "OPPORTUNITY",
      "domain": "CREATORS",
      "priority": "INFO",
      "title": "Creator activity rising — 14 new artifacts this week",
      "message": "National Creator Challenge momentum building...",
      "context": {
        "artifacts_count": 14,
        "top_creators": ["zion_id", "maya_id"],
        "challenge_id": "q1_2026_challenge"
      },
      "created_at": "2025-12-30T09:30:00Z"
    }
  ],
  "totalCount": 45
}
```

**UI Components**:
- **Feed List**: Scrollable list of insights with color-coded priority badges
  - CRITICAL: Red border + icon
  - IMPORTANT: Yellow border + icon
  - INFO: Blue border + icon
- **Type Filters**: Tabs for ALL | ALERTS | RECOMMENDATIONS | FORECASTS | OPPORTUNITIES
- **Domain Filters**: Dropdown for CIRCLES | YOUTH | MISSIONS | CURRICULUM | CULTURE | CREATORS | EXPANSION
- **Real-time Updates**: Poll every 30 seconds or use WebSocket for live updates

**Visualizations**:
- Insight timeline (horizontal timeline showing when insights were generated)
- Domain distribution pie chart (how many insights per domain)
- Priority distribution bar chart

**User Actions**:
- Click insight → Open detailed modal with full context
- Acknowledge insight → POST `/intelligence/insights/:id/acknowledge`
- Resolve insight → POST `/intelligence/insights/:id/resolve`
- Filter by date range, region, domain, type

---

### Panel 2: National Programs Panel

**Purpose**: Ministry-friendly view of all government-linked programs with performance metrics and youth reach.

**API Endpoints**:
```typescript
GET /api/v1/governments/programs
  ?country_id=barbados
  &status=ACTIVE

// Example response:
{
  "programs": [
    {
      "id": "youth_circles_network",
      "name": "Barbados Youth Circles Network",
      "ministry_id": "youth_ministry",
      "status": "ACTIVE",
      "metrics": {
        "youth_enrolled": 10000,
        "circles_active": 200,
        "mission_completion_rate": 0.72,
        "attendance_rate": 0.80,
        "regional_coverage": 0.95 // 95% of regions covered
      },
      "start_date": "2026-01-01",
      "budget": 500000,
      "kpis": [
        { "name": "Youth Enrollment", "target": 10000, "actual": 10000, "status": "ON_TRACK" },
        { "name": "Attendance Rate", "target": 0.80, "actual": 0.80, "status": "ON_TRACK" }
      ]
    },
    {
      "id": "national_creator_challenge",
      "name": "Barbados National Creator Challenge",
      "ministry_id": "culture_ministry",
      "status": "ACTIVE",
      "metrics": {
        "creators_enrolled": 2000,
        "artifacts_submitted": 450,
        "showcases_completed": 1,
        "pathways_created": 50 // scholarships, internships, placements
      }
    }
  ]
}

GET /api/v1/intelligence/feed
  ?domain=GOVERNMENT
  ?audience_scope_id=program:youth_circles_network
```

**UI Components**:
- **Program Cards**: Grid of program cards with key metrics
  - Program name + ministry badge
  - Youth reach (enrollment, participation)
  - Performance indicators (completion rates, engagement)
  - Budget vs actual spending
  - KPI status badges (ON_TRACK, AT_RISK, OFF_TRACK)
- **Program Selector**: Dropdown to focus on single program
- **Ministry Filter**: Filter programs by ministry

**Visualizations**:
- Program comparison chart (bar chart comparing programs by youth reach)
- KPI progress bars (target vs actual)
- Regional distribution map (where each program operates)
- Timeline view (program milestones)

**User Actions**:
- Click program → Open detailed program dashboard
- Export program report → Download PDF with metrics
- View program intelligence → Filter intelligence feed to program

---

### Panel 3: Regional Performance Panel

**Purpose**: Map-based view of Barbados by parish showing youth engagement, circle health, mission completion, and cultural momentum.

**API Endpoints**:
```typescript
GET /api/v1/analytics/regions
  ?country_id=barbados

// Example response:
{
  "regions": [
    {
      "id": "st_michael",
      "name": "St. Michael",
      "metrics": {
        "youth_enrolled": 3500,
        "circles_active": 70,
        "attendance_rate": 0.85,
        "mission_completion_rate": 0.78,
        "cultural_resonance_score": 82,
        "expansion_readiness": "HIGH"
      },
      "intelligence_summary": {
        "alerts": 2,
        "recommendations": 5,
        "opportunities": 3
      }
    },
    {
      "id": "christ_church",
      "name": "Christ Church",
      "metrics": {
        "youth_enrolled": 2200,
        "circles_active": 45,
        "attendance_rate": 0.68, // LOW - trigger alert
        "mission_completion_rate": 0.60, // LOW
        "cultural_resonance_score": 70,
        "expansion_readiness": "MEDIUM"
      },
      "intelligence_summary": {
        "alerts": 5, // HIGH alerts
        "recommendations": 8,
        "opportunities": 1
      }
    }
  ]
}

GET /api/v1/intelligence/feed
  ?domain=CIRCLES,EXPANSION
  ?audience_scope_id=region:christ_church
```

**UI Components**:
- **Interactive Map**: Mapbox/Leaflet map of Barbados with parish boundaries
  - Color-coded parishes by performance (green = high, yellow = medium, red = low)
  - Click parish → Show regional dashboard modal
- **Regional Leaderboard**: Table ranking parishes by performance
  - Columns: Parish, Youth Enrolled, Attendance Rate, Mission Completion, Cultural Resonance
  - Sortable by any metric
- **Regional Comparison Chart**: Line chart showing trends over time for all parishes

**Visualizations**:
- Heatmap (darker = higher engagement)
- Bar chart comparison (side-by-side parish comparison)
- Trend lines (month-over-month changes per parish)

**User Actions**:
- Click parish on map → Open regional detail modal
- Filter by metric (attendance, missions, culture)
- Export regional report → Download CSV/PDF
- View regional intelligence → Show alerts/recommendations for selected parish

---

### Panel 4: School & Outreach Panel

**Purpose**: National view of all schools and outreach activity showing active, dormant, and high-potential schools plus ambassador activity.

**API Endpoints**:
```typescript
GET /api/v1/schools
  ?country_id=barbados
  &include=region,circles,ambassador_outreach

// Example response:
{
  "schools": [
    {
      "id": "school_uuid",
      "name": "Harrison College",
      "region_id": "st_michael",
      "status": "ACTIVE",
      "metrics": {
        "circles_active": 5,
        "youth_enrolled": 200,
        "last_outreach_date": "2025-12-15",
        "outreach_frequency": 4, // times per month
        "circle_health_avg": 78
      },
      "intelligence_summary": {
        "alerts": 0,
        "recommendations": 2,
        "opportunities": 1
      }
    },
    {
      "id": "school_uuid_2",
      "name": "St. George Secondary",
      "region_id": "st_george",
      "status": "DORMANT", // No circles, no recent outreach
      "metrics": {
        "circles_active": 0,
        "youth_enrolled": 0,
        "last_outreach_date": "2025-10-01", // 90 days ago - ALERT
        "outreach_frequency": 0
      },
      "intelligence_summary": {
        "alerts": 2, // "No outreach in 90 days", "High-potential school dormant"
        "recommendations": 1
      }
    }
  ],
  "totalSchools": 30,
  "activeSchools": 25,
  "dormantSchools": 5
}

GET /api/v1/ambassador-outreach
  ?country_id=barbados
  &limit=50

// Example response:
{
  "outreach": [
    {
      "id": "outreach_uuid",
      "school_id": "school_uuid",
      "ambassador_id": "ambassador_uuid",
      "date": "2025-12-20",
      "type": "INITIAL_VISIT",
      "notes": "Met with principal, 3 teachers interested in circles",
      "follow_up_required": true,
      "next_steps": "Schedule captain training session"
    }
  ]
}
```

**UI Components**:
- **School Status Cards**: Grid of school cards color-coded by status
  - ACTIVE (green): Has circles, recent outreach
  - DORMANT (yellow): No circles, outreach >30 days ago
  - HIGH_POTENTIAL (blue): Strong interest signals, ready for activation
- **Outreach Timeline**: Chronological view of all outreach activity
  - Ambassador avatar + school name + date + outcome
- **School Selector**: Dropdown to filter by region or status

**Visualizations**:
- School activation funnel (outreach → circles → youth enrolled)
- Ambassador activity heatmap (which ambassadors are most active)
- Geographic distribution (map of schools by status)

**User Actions**:
- Click school → Open school detail modal (circles, youth, outreach history)
- Log outreach visit → POST `/ambassador-outreach` (if user is ambassador)
- View school intelligence → Filter intelligence feed to school
- Export school report → Download CSV of all schools

---

### Panel 5: Culture & Identity Panel

**Purpose**: National cultural intelligence view showing story engagement, regional resonance, cultural momentum, and diaspora alignment.

**API Endpoints**:
```typescript
GET /api/v1/culture/story/current

// Example response:
{
  "story": {
    "id": "story_uuid",
    "title": "The Bajan Fishermen's Legacy",
    "season_id": "identity_season",
    "week_number": 3,
    "content": "...",
    "engagement_metrics": {
      "views": 8500,
      "completion_rate": 0.75,
      "regional_resonance": {
        "st_michael": 0.85,
        "christ_church": 0.68,
        "st_james": 0.90 // HIGHEST - trigger opportunity
      },
      "youth_reactions": {
        "loved": 3200,
        "inspired": 1800,
        "shared": 450
      }
    }
  }
}

GET /api/v1/analytics/culture
  ?country_id=barbados

// Example response:
{
  "cultural_metrics": {
    "stories_published": 12,
    "avg_engagement_rate": 0.72,
    "cultural_artifacts_created": 450,
    "diaspora_connections": 1200,
    "cultural_momentum_score": 78 // 0-100 scale
  },
  "top_stories": [
    { "title": "The Bajan Fishermen's Legacy", "engagement_rate": 0.90 },
    { "title": "Kadooment Origins", "engagement_rate": 0.88 }
  ],
  "regional_resonance": [
    { "region": "St. James", "score": 0.90 },
    { "region": "St. Michael", "score": 0.85 }
  ]
}

GET /api/v1/intelligence/opportunities
  ?domain=CULTURE
  ?country_id=barbados
```

**UI Components**:
- **Current Story Card**: Featured card showing this week's cultural story
  - Story title + excerpt
  - Engagement metrics (views, completion rate)
  - Regional resonance heatmap
- **Cultural Momentum Gauge**: Circular gauge showing national cultural momentum (0-100)
- **Story Archive**: Scrollable list of past stories with engagement scores
- **Diaspora Connection Stats**: Number of diaspora youth engaged, cross-region collaborations

**Visualizations**:
- Regional resonance map (which parishes resonate with which stories)
- Story engagement timeline (weekly engagement trends)
- Cultural artifact gallery (top youth-created cultural artifacts)

**User Actions**:
- Click story → Read full story + see detailed engagement
- View cultural intelligence → Filter to CULTURE domain
- Export cultural report → Download quarterly cultural impact report

---

### Panel 6: Creator & Innovation Panel

**Purpose**: National innovation pipeline view showing rising creators, artifact submissions, innovation clusters, and challenge participation.

**API Endpoints**:
```typescript
GET /api/v1/artifacts
  ?country_id=barbados
  &limit=50
  &sort=created_at:desc

// Example response:
{
  "artifacts": [
    {
      "id": "artifact_uuid",
      "creator_id": "zion_uuid",
      "creator_name": "Zion Thompson",
      "title": "Barbados Heritage AR App",
      "type": "APP",
      "challenge_id": "q1_2026_challenge",
      "created_at": "2025-12-28",
      "quality_score": 92, // peer review + judge score
      "views": 450,
      "reactions": { "loved": 120, "inspired": 80 }
    }
  ],
  "totalArtifacts": 2000
}

GET /api/v1/creator-challenges
  ?country_id=barbados
  &status=ACTIVE

// Example response:
{
  "challenges": [
    {
      "id": "q1_2026_challenge",
      "name": "Barbados Digital Innovation Challenge",
      "season_id": "creation_season",
      "start_date": "2025-12-01",
      "end_date": "2026-02-28",
      "metrics": {
        "participants": 450,
        "submissions": 180,
        "completion_rate": 0.40
      }
    }
  ]
}

GET /api/v1/intelligence/opportunities
  ?domain=CREATORS
  ?country_id=barbados
```

**UI Components**:
- **Rising Creators Leaderboard**: Table of top 50 creators by quality score
  - Creator name, region, artifact count, quality score
  - "Rising Star" badge for new creators with high scores
- **Artifact Gallery**: Grid of featured artifacts with thumbnails
  - Filter by type (DESIGN, VIDEO, WRITING, APP, MUSIC, ART, INNOVATION)
- **Challenge Performance Card**: Current challenge metrics
  - Participants, submissions, completion rate
  - Progress bar to end date

**Visualizations**:
- Creator geographic distribution (map showing where creators are from)
- Artifact type breakdown (pie chart of artifact types)
- Challenge funnel (participants → submissions → placements)

**User Actions**:
- Click creator → View creator profile + portfolio
- Click artifact → View artifact detail page
- View creator intelligence → Filter to CREATORS domain
- Export creator report → Download CSV of all creators + artifacts

---

### Panel 7: Workforce & Skills Panel

**Purpose**: National workforce intelligence view showing youth skill development, digital literacy, career pathway readiness, and skills gaps.

**API Endpoints**:
```typescript
GET /api/v1/analytics/workforce
  ?country_id=barbados

// Example response:
{
  "workforce_metrics": {
    "youth_in_training": 2000,
    "certifications_earned": 500,
    "job_placements": 200,
    "avg_skill_acquisition_rate": 0.18, // 18% increase month-over-month
    "digital_literacy_score": 72 // 0-100 scale
  },
  "top_skills": [
    { "skill": "Web Development", "youth_count": 450, "growth_rate": 0.25 },
    { "skill": "Data Analysis", "youth_count": 320, "growth_rate": 0.20 },
    { "skill": "Digital Marketing", "youth_count": 280, "growth_rate": 0.15 }
  ],
  "skills_gaps": [
    { "skill": "Cybersecurity", "demand": "HIGH", "supply": "LOW" },
    { "skill": "Biotech Lab Techniques", "demand": "MEDIUM", "supply": "LOW" }
  ],
  "career_pathways": [
    { "pathway": "Tech Careers", "youth_enrolled": 800, "placement_rate": 0.30 },
    { "pathway": "Creative Industries", "youth_enrolled": 600, "placement_rate": 0.25 }
  ]
}

GET /api/v1/intelligence/forecasts
  ?domain=WORKFORCE
  ?country_id=barbados
```

**UI Components**:
- **Skills Dashboard**: Grid of skill cards showing acquisition trends
  - Skill name, youth count, growth rate
  - Trend arrow (up/down)
- **Skills Gap Matrix**: Table showing demand vs supply
  - Color-coded cells (green = balanced, yellow = moderate gap, red = severe gap)
- **Career Pathways Cards**: Cards for each pathway showing enrollment + placement rates

**Visualizations**:
- Skill acquisition timeline (line chart showing monthly skill growth)
- Skills gap heatmap (demand vs supply matrix)
- Placement funnel (training → certification → job placement)

**User Actions**:
- Click skill → View youth enrolled in skill, training programs
- View workforce intelligence → Filter to WORKFORCE domain
- Export workforce report → Download quarterly workforce report

---

### Panel 8: Biotech & STEM Panel (Optional Activation)

**Purpose**: National science & innovation intelligence view showing youth biotech participation, lab partners, bio-projects, and safety compliance.

**API Endpoints**:
```typescript
GET /api/v1/analytics/biotech
  ?country_id=barbados

// Example response:
{
  "biotech_metrics": {
    "youth_enrolled": 500,
    "labs_active": 5,
    "projects_completed": 45,
    "safety_compliance_score": 95,
    "innovation_pathways_created": 20
  },
  "top_projects": [
    {
      "id": "project_uuid",
      "title": "Marine Microplastic Detection",
      "lab_id": "lab_uuid",
      "youth_count": 12,
      "status": "IN_PROGRESS"
    }
  ],
  "lab_partners": [
    { "name": "UWI Biotech Lab", "projects": 15, "youth_served": 200 },
    { "name": "BIDC Innovation Hub", "projects": 10, "youth_served": 150 }
  ]
}

GET /api/v1/intelligence/opportunities
  ?domain=BIOTECH
  ?country_id=barbados
```

**UI Components**:
- **Biotech Participation Card**: Youth enrolled, labs active, projects completed
- **Lab Partners Table**: List of lab partners with project counts
- **Safety Compliance Gauge**: Circular gauge showing compliance score
- **Project Gallery**: Grid of featured bio-projects

**Visualizations**:
- Youth enrollment trend (line chart)
- Project distribution by lab (bar chart)
- Innovation pathway funnel (enrollment → project → university/career)

**User Actions**:
- Click lab → View lab details + projects
- Click project → View project details + youth participants
- View biotech intelligence → Filter to BIOTECH domain

---

### Panel 9: Government Contracts & Partnerships Panel

**Purpose**: National procurement and partnership view showing active contracts, pending proposals, ministry partnerships, and contract performance.

**API Endpoints**:
```typescript
GET /api/v1/governments/contracts
  ?country_id=barbados

// Example response:
{
  "contracts": [
    {
      "id": "contract_uuid",
      "program_id": "youth_circles_network",
      "ministry_id": "youth_ministry",
      "contract_number": "GOB-YC-2026-001",
      "value": 500000,
      "start_date": "2026-01-01",
      "end_date": "2026-12-31",
      "status": "ACTIVE",
      "kpis": [
        { "name": "Youth Enrollment", "target": 10000, "actual": 10000, "status": "ON_TRACK" },
        { "name": "Circle Activation", "target": 200, "actual": 200, "status": "ON_TRACK" }
      ],
      "milestones": [
        { "name": "Phase 1 Pilot", "date": "2026-03-31", "status": "COMPLETED" },
        { "name": "National Rollout", "date": "2026-06-30", "status": "IN_PROGRESS" }
      ]
    }
  ]
}

GET /api/v1/governments/ministries
  ?country_id=barbados

// Example response:
{
  "ministries": [
    {
      "id": "youth_ministry",
      "name": "Ministry of Youth, Sports & Community Empowerment",
      "programs_count": 3,
      "active_contracts": 2,
      "total_investment": 1200000
    }
  ]
}
```

**UI Components**:
- **Contract Cards**: Grid of contract cards showing contract details
  - Contract number, ministry, program, value
  - KPI status badges (ON_TRACK, AT_RISK, OFF_TRACK)
  - Milestone progress bars
- **Ministry Partnership Table**: Table of ministries with investment amounts
- **Contract Performance Summary**: Overall contract health score

**Visualizations**:
- Contract timeline (Gantt chart showing contract duration + milestones)
- Ministry investment breakdown (pie chart of investment by ministry)
- KPI performance heatmap (contracts × KPIs)

**User Actions**:
- Click contract → Open detailed contract dashboard
- Export contract report → Download PDF with KPI details
- View pending proposals → Show contracts in PENDING status

---

### Panel 10: National Forecasts Panel

**Purpose**: Predictive intelligence view for Barbados showing youth engagement forecasts, mission completion forecasts, cultural resonance forecasts, and expansion forecasts.

**API Endpoints**:
```typescript
GET /api/v1/intelligence/forecasts
  ?country_id=barbados
  &domains=CIRCLES,YOUTH,MISSIONS,CULTURE,CREATORS,EXPANSION

// Example response:
{
  "forecasts": [
    {
      "id": "forecast_uuid",
      "type": "FORECAST",
      "domain": "CIRCLES",
      "title": "Youth engagement projected to grow 15% next quarter",
      "message": "Based on current trends (rising circle attendance, new school activations), national youth engagement projected to reach 85% by Q2 2026.",
      "context": {
        "current_engagement_rate": 0.74,
        "projected_engagement_rate": 0.85,
        "confidence": 0.78, // 78% confidence
        "contributing_factors": [
          "New school activations",
          "Rising cultural resonance",
          "Ambassador effectiveness"
        ]
      },
      "horizon": "3_MONTHS", // 3-month forecast
      "created_at": "2025-12-30"
    },
    {
      "id": "forecast_uuid_2",
      "type": "FORECAST",
      "domain": "EXPANSION",
      "title": "3 new parishes ready for expansion by Q2 2026",
      "message": "St. Philip, St. John, and St. Andrew show high readiness scores...",
      "context": {
        "regions_ready": ["st_philip", "st_john", "st_andrew"],
        "readiness_scores": [0.82, 0.78, 0.75]
      },
      "horizon": "3_MONTHS"
    }
  ]
}
```

**UI Components**:
- **Forecast Cards**: Grid of forecast cards with confidence levels
  - Domain badge, forecast title, horizon badge (3 months, 6 months, 1 year)
  - Confidence meter (0-100%)
  - Contributing factors list
- **Forecast Timeline**: Horizontal timeline showing when forecasts materialize
- **Confidence Filter**: Filter forecasts by confidence level (high/medium/low)

**Visualizations**:
- Forecast trajectory chart (line chart showing current state → projected state)
- Domain forecast distribution (bar chart showing forecasts by domain)
- Confidence heatmap (forecasts × confidence levels)

**User Actions**:
- Click forecast → Open detailed forecast modal with methodology
- Export forecast report → Download quarterly forecast report
- Compare forecasts → Side-by-side comparison of multiple forecasts

---

### Panel 11: National Reporting Panel

**Purpose**: Weekly, monthly, and annual reporting system for governance and compliance.

**API Endpoints**:
```typescript
GET /api/v1/analytics/reports/national
  ?country_id=barbados
  &report_type=WEEKLY|MONTHLY|QUARTERLY|ANNUAL
  &start_date=2025-01-01
  &end_date=2025-12-31

// Example response:
{
  "report": {
    "type": "QUARTERLY",
    "period": "Q4 2025",
    "generated_at": "2025-12-30",
    "sections": [
      {
        "title": "National Youth Development",
        "metrics": {
          "youth_enrolled": 10000,
          "circles_active": 200,
          "attendance_rate": 0.80,
          "mission_completion_rate": 0.72
        },
        "highlights": [
          "Reached 10,000 youth enrollment target",
          "Activated all 30 secondary schools"
        ],
        "challenges": [
          "Attendance declined in 2 parishes"
        ]
      },
      {
        "title": "Cultural Engagement",
        "metrics": {
          "stories_published": 12,
          "cultural_artifacts": 450,
          "diaspora_connections": 1200
        }
      },
      {
        "title": "Innovation & Workforce",
        "metrics": {
          "creators_enrolled": 2000,
          "artifacts_submitted": 500,
          "certifications_earned": 500,
          "job_placements": 200
        }
      }
    ],
    "intelligence_summary": {
      "total_insights": 450,
      "alerts_resolved": 120,
      "recommendations_implemented": 85
    }
  }
}
```

**UI Components**:
- **Report Selector**: Dropdown to select report type and period
  - WEEKLY, MONTHLY, QUARTERLY, ANNUAL
- **Report Sections**: Collapsible sections for each report area
  - National Youth Development
  - Cultural Engagement
  - Innovation & Workforce
  - Program Performance
  - Regional Performance
- **Export Options**: Download as PDF, CSV, or JSON

**Visualizations**:
- Executive summary dashboard (top 10 metrics at a glance)
- Trend comparison (current period vs previous period)
- Ministry-specific reports (filtered by ministry)

**User Actions**:
- Generate report → POST `/analytics/reports/generate`
- Download report → GET `/analytics/reports/:id/download`
- Schedule report → POST `/analytics/reports/schedule` (weekly/monthly auto-generation)
- Email report → POST `/analytics/reports/:id/email` (send to ministry contacts)

---

## III. Dashboard Implementation Guide

### Frontend Architecture

**Directory Structure**:
```
frontend/src/
├── app/
│   ├── dashboard/
│   │   ├── government/
│   │   │   ├── page.tsx              # Main dashboard
│   │   │   ├── intelligence/
│   │   │   │   └── page.tsx          # Panel 1: Intelligence Feed
│   │   │   ├── programs/
│   │   │   │   └── page.tsx          # Panel 2: Programs
│   │   │   ├── regions/
│   │   │   │   └── page.tsx          # Panel 3: Regions
│   │   │   ├── schools/
│   │   │   │   └── page.tsx          # Panel 4: Schools
│   │   │   ├── culture/
│   │   │   │   └── page.tsx          # Panel 5: Culture
│   │   │   ├── creators/
│   │   │   │   └── page.tsx          # Panel 6: Creators
│   │   │   ├── workforce/
│   │   │   │   └── page.tsx          # Panel 7: Workforce
│   │   │   ├── biotech/
│   │   │   │   └── page.tsx          # Panel 8: Biotech
│   │   │   ├── contracts/
│   │   │   │   └── page.tsx          # Panel 9: Contracts
│   │   │   ├── forecasts/
│   │   │   │   └── page.tsx          # Panel 10: Forecasts
│   │   │   └── reports/
│   │   │       └── page.tsx          # Panel 11: Reports
├── components/
│   ├── dashboard/
│   │   ├── IntelligenceFeed.tsx
│   │   ├── ProgramsPanel.tsx
│   │   ├── RegionsMap.tsx
│   │   ├── SchoolsPanel.tsx
│   │   ├── CulturePanel.tsx
│   │   ├── CreatorsPanel.tsx
│   │   ├── WorkforcePanel.tsx
│   │   ├── BiotechPanel.tsx
│   │   ├── ContractsPanel.tsx
│   │   ├── ForecastsPanel.tsx
│   │   └── ReportsPanel.tsx
├── lib/
│   ├── api/
│   │   ├── intelligence.ts       # Intelligence API client
│   │   ├── analytics.ts          # Analytics API client
│   │   ├── governments.ts        # Government API client
│   │   └── domains.ts            # Domain APIs (circles, missions, etc.)
│   └── hooks/
│       ├── useIntelligence.ts    # React Query hook for intelligence
│       ├── useAnalytics.ts       # React Query hook for analytics
│       └── useGovernment.ts      # React Query hook for government data
```

---

### API Client Implementation

**Intelligence API Client** (`lib/api/intelligence.ts`):
```typescript
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000/api/v1';

export interface Insight {
  id: string;
  type: 'ALERT' | 'RECOMMENDATION' | 'FORECAST' | 'OPPORTUNITY';
  domain: 'CIRCLES' | 'YOUTH' | 'MISSIONS' | 'CURRICULUM' | 'CULTURE' | 'CREATORS' | 'EXPANSION';
  priority: 'CRITICAL' | 'IMPORTANT' | 'INFO';
  title: string;
  message: string;
  context: Record<string, any>;
  audience_role: string;
  audience_scope_id?: string;
  status: 'ACTIVE' | 'ACKNOWLEDGED' | 'RESOLVED' | 'DISMISSED';
  created_at: string;
  updated_at: string;
}

export interface IntelligenceFeedResponse {
  insights: Insight[];
  totalCount: number;
}

export const intelligenceApi = {
  // Get intelligence feed
  getFeed: async (params: {
    limit?: number;
    offset?: number;
    domain?: string;
    type?: string;
    status?: string;
    priority?: string;
  }): Promise<IntelligenceFeedResponse> => {
    const response = await axios.get(`${API_BASE_URL}/intelligence/feed`, {
      params: { ...params, country_id: 'barbados' },
      headers: { Authorization: `Bearer ${getToken()}` }
    });
    return response.data;
  },

  // Get alerts
  getAlerts: async (): Promise<IntelligenceFeedResponse> => {
    return intelligenceApi.getFeed({ type: 'ALERT', status: 'ACTIVE' });
  },

  // Get recommendations
  getRecommendations: async (): Promise<IntelligenceFeedResponse> => {
    return intelligenceApi.getFeed({ type: 'RECOMMENDATION', status: 'ACTIVE' });
  },

  // Get forecasts
  getForecasts: async (): Promise<IntelligenceFeedResponse> => {
    return intelligenceApi.getFeed({ type: 'FORECAST', status: 'ACTIVE' });
  },

  // Get opportunities
  getOpportunities: async (): Promise<IntelligenceFeedResponse> => {
    return intelligenceApi.getFeed({ type: 'OPPORTUNITY', status: 'ACTIVE' });
  },

  // Acknowledge insight
  acknowledgeInsight: async (insightId: string): Promise<void> => {
    await axios.post(`${API_BASE_URL}/intelligence/insights/${insightId}/acknowledge`, {}, {
      headers: { Authorization: `Bearer ${getToken()}` }
    });
  },

  // Resolve insight
  resolveInsight: async (insightId: string, resolution: string): Promise<void> => {
    await axios.post(`${API_BASE_URL}/intelligence/insights/${insightId}/resolve`, 
      { resolution },
      { headers: { Authorization: `Bearer ${getToken()}` } }
    );
  }
};

function getToken(): string {
  // Get JWT from localStorage or cookies
  return localStorage.getItem('auth_token') || '';
}
```

---

### React Query Hooks

**useIntelligence Hook** (`lib/hooks/useIntelligence.ts`):
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { intelligenceApi } from '@/lib/api/intelligence';

export function useIntelligenceFeed(params?: {
  domain?: string;
  type?: string;
  status?: string;
  priority?: string;
}) {
  return useQuery({
    queryKey: ['intelligence', 'feed', params],
    queryFn: () => intelligenceApi.getFeed(params || {}),
    refetchInterval: 30000, // Poll every 30 seconds
    staleTime: 10000 // Consider data stale after 10 seconds
  });
}

export function useAcknowledgeInsight() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (insightId: string) => intelligenceApi.acknowledgeInsight(insightId),
    onSuccess: () => {
      // Invalidate intelligence feed to refetch
      queryClient.invalidateQueries({ queryKey: ['intelligence', 'feed'] });
    }
  });
}

export function useResolveInsight() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ insightId, resolution }: { insightId: string; resolution: string }) => 
      intelligenceApi.resolveInsight(insightId, resolution),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['intelligence', 'feed'] });
    }
  });
}
```

---

### Component Example: Intelligence Feed Panel

**IntelligenceFeed Component** (`components/dashboard/IntelligenceFeed.tsx`):
```typescript
'use client';

import { useState } from 'react';
import { useIntelligenceFeed, useAcknowledgeInsight, useResolveInsight } from '@/lib/hooks/useIntelligence';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';

export function IntelligenceFeed() {
  const [selectedType, setSelectedType] = useState<string>('ALL');
  const [selectedDomain, setSelectedDomain] = useState<string | undefined>();

  const { data, isLoading, error } = useIntelligenceFeed({
    type: selectedType === 'ALL' ? undefined : selectedType,
    domain: selectedDomain,
    status: 'ACTIVE'
  });

  const acknowledgeMutation = useAcknowledgeInsight();
  const resolveMutation = useResolveInsight();

  if (isLoading) return <div>Loading intelligence feed...</div>;
  if (error) return <div>Error loading intelligence feed</div>;

  const insights = data?.insights || [];

  return (
    <div className="space-y-4">
      {/* Type Filters */}
      <Tabs value={selectedType} onValueChange={setSelectedType}>
        <TabsList>
          <TabsTrigger value="ALL">All</TabsTrigger>
          <TabsTrigger value="ALERT">Alerts</TabsTrigger>
          <TabsTrigger value="RECOMMENDATION">Recommendations</TabsTrigger>
          <TabsTrigger value="FORECAST">Forecasts</TabsTrigger>
          <TabsTrigger value="OPPORTUNITY">Opportunities</TabsTrigger>
        </TabsList>
      </Tabs>

      {/* Domain Filter */}
      <select 
        value={selectedDomain || ''} 
        onChange={(e) => setSelectedDomain(e.target.value || undefined)}
        className="border rounded px-3 py-2"
      >
        <option value="">All Domains</option>
        <option value="CIRCLES">Circles</option>
        <option value="YOUTH">Youth</option>
        <option value="MISSIONS">Missions</option>
        <option value="CURRICULUM">Curriculum</option>
        <option value="CULTURE">Culture</option>
        <option value="CREATORS">Creators</option>
        <option value="EXPANSION">Expansion</option>
      </select>

      {/* Insights List */}
      <div className="space-y-3">
        {insights.map((insight) => (
          <Card 
            key={insight.id} 
            className={`border-l-4 ${
              insight.priority === 'CRITICAL' ? 'border-l-red-500' :
              insight.priority === 'IMPORTANT' ? 'border-l-yellow-500' :
              'border-l-blue-500'
            }`}
          >
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between">
                <div className="space-y-1">
                  <CardTitle className="text-lg">{insight.title}</CardTitle>
                  <div className="flex gap-2">
                    <Badge variant={insight.type === 'ALERT' ? 'destructive' : 'default'}>
                      {insight.type}
                    </Badge>
                    <Badge variant="outline">{insight.domain}</Badge>
                    <Badge 
                      variant={
                        insight.priority === 'CRITICAL' ? 'destructive' :
                        insight.priority === 'IMPORTANT' ? 'default' :
                        'secondary'
                      }
                    >
                      {insight.priority}
                    </Badge>
                  </div>
                </div>
                <span className="text-sm text-gray-500">
                  {new Date(insight.created_at).toLocaleDateString()}
                </span>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-700 mb-4">{insight.message}</p>
              
              {/* Context Details */}
              {Object.keys(insight.context).length > 0 && (
                <div className="bg-gray-50 rounded p-3 mb-4">
                  <p className="text-xs font-semibold mb-2">Details:</p>
                  <pre className="text-xs">
                    {JSON.stringify(insight.context, null, 2)}
                  </pre>
                </div>
              )}

              {/* Actions */}
              <div className="flex gap-2">
                <Button 
                  size="sm" 
                  variant="outline"
                  onClick={() => acknowledgeMutation.mutate(insight.id)}
                  disabled={acknowledgeMutation.isPending}
                >
                  Acknowledge
                </Button>
                <Button 
                  size="sm"
                  onClick={() => resolveMutation.mutate({ 
                    insightId: insight.id, 
                    resolution: 'Addressed via dashboard action' 
                  })}
                  disabled={resolveMutation.isPending}
                >
                  Resolve
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {insights.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No active insights at this time.
        </div>
      )}
    </div>
  );
}
```

---

## IV. Deployment & Security

### Authentication Flow

1. **Government User Login**:
   - User authenticates via `/api/v1/auth/login` with credentials
   - Backend validates credentials, checks role (GOVERNMENT_ADMIN, MINISTRY_DIRECTOR, etc.)
   - Backend returns JWT access token + refresh token
   - Frontend stores tokens securely (HTTP-only cookies preferred)

2. **Role-Based Authorization**:
   - Every API request includes `Authorization: Bearer <token>` header
   - Backend validates JWT, extracts user roles and scope
   - Backend filters data based on role (GOVERNMENT_ADMIN sees all Barbados data, MINISTRY_DIRECTOR sees ministry data)

3. **Token Refresh**:
   - When access token expires (15-30 minutes), frontend calls `/api/v1/auth/refresh` with refresh token
   - Backend issues new access token
   - Process transparent to user

---

### Data Privacy & Compliance

**Youth Data Protection**:
- Dashboard shows **aggregated insights only** (no individual youth names/data)
- Exception: Government users with explicit consent can drill down to individual youth (e.g., for at-risk youth support)
- Audit trail: All data access logged in `audit_log` table

**Barbados Data Protection Act Compliance**:
- Data residency: All Barbados youth data hosted in-country or on approved cloud infrastructure
- Consent management: Youth/parents consent to data collection during registration
- Data retention: Youth data retained for program duration + 5 years (or as per regulations)
- Right to access: Youth can request their data via `/api/v1/users/me/data`
- Right to erasure: Youth can request data deletion after program completion

---

### Performance Optimization

**API Caching**:
- Intelligence feed: Cache for 30 seconds (use React Query `staleTime`)
- Analytics data: Cache for 5 minutes (updated less frequently)
- Static data (regions, schools): Cache for 1 hour

**Pagination**:
- All list endpoints support `limit` and `offset` parameters
- Default limit: 20 items
- Max limit: 100 items

**Lazy Loading**:
- Dashboard panels load data on-demand (not all at once)
- Use React Suspense for loading states

---

## V. Deployment Checklist

### Phase 1: Backend Setup
- [ ] Deploy NestJS backend to production (Azure/GCP)
- [ ] Configure PostgreSQL database with Barbados data
- [ ] Run migrations: `npx prisma migrate deploy`
- [ ] Seed database with Barbados regions, schools, initial programs
- [ ] Test Intelligence API endpoints: `/intelligence/feed`, `/analytics/overview`
- [ ] Configure CORS to allow frontend domain

### Phase 2: Frontend Development
- [ ] Clone Next.js frontend template
- [ ] Implement 11 dashboard panels (parallel development)
- [ ] Integrate API clients (`lib/api/*.ts`)
- [ ] Add authentication flow (login, JWT storage, token refresh)
- [ ] Implement role-based routing (GOVERNMENT_ADMIN vs MINISTRY_DIRECTOR)
- [ ] Add loading states, error handling, empty states
- [ ] Test on staging environment

### Phase 3: Integration Testing
- [ ] Test all 11 panels with real Barbados data
- [ ] Test role-based access control (different user roles see different data)
- [ ] Test intelligence feed real-time updates
- [ ] Load testing (simulate 100 concurrent government users)
- [ ] Security testing (JWT validation, XSS, CSRF)

### Phase 4: UAT & Training
- [ ] User Acceptance Testing with Ministry of Youth team
- [ ] Gather feedback, iterate on UI/UX
- [ ] Conduct training sessions for government users
- [ ] Create user documentation (dashboard guides, video tutorials)

### Phase 5: Production Launch
- [ ] Deploy frontend to production (Azure Static Web Apps or Vercel)
- [ ] Configure custom domain: `dashboard.codexdominion.bb`
- [ ] Enable SSL/TLS (HTTPS)
- [ ] Set up monitoring (Sentry for errors, Google Analytics for usage)
- [ ] Launch with Ministry of Youth, Education, Culture
- [ ] Announce to CARICOM partners

---

## VI. Success Metrics

### Dashboard Adoption Metrics
- **Daily Active Users**: 50+ government users logging in daily
- **Session Duration**: Average 20+ minutes per session
- **Panel Engagement**: All 11 panels viewed weekly
- **Intelligence Actions**: 80% of CRITICAL alerts acknowledged within 24 hours

### Intelligence System Metrics
- **Insight Generation**: 100+ insights generated weekly
- **Insight Quality**: 70% of insights rated as "useful" by users
- **Resolution Rate**: 60% of CRITICAL alerts resolved within 1 week
- **Forecast Accuracy**: 75% of forecasts materialize as predicted

### National Impact Metrics
- **Program Performance**: All 5 flagship programs meeting KPIs
- **Youth Reach**: 10,000+ youth enrolled by end of Year 1
- **Regional Equity**: <15% variance in youth reach across parishes
- **Ministry Satisfaction**: 4.0/5 average satisfaction score

---

## VII. Conclusion

The **Barbados Government Dashboard** is the national command interface for CodexDominion — integrating 7 core engines, 6 government engines, and the 47-rule Intelligence API into one sovereign control room.

**This is not a dashboard. This is a national operating system interface.**

With 11 comprehensive panels, Barbados gains:
- ✅ Real-time national intelligence (Panel 1)
- ✅ Program performance tracking (Panel 2)
- ✅ Regional equity monitoring (Panel 3)
- ✅ School activation pipeline (Panel 4)
- ✅ Cultural diplomacy intelligence (Panel 5)
- ✅ Innovation pipeline visibility (Panel 6)
- ✅ Workforce readiness forecasts (Panel 7)
- ✅ Biotech/STEM intelligence (Panel 8)
- ✅ Government contract tracking (Panel 9)
- ✅ Predictive forecasts (Panel 10)
- ✅ Automated reporting (Panel 11)

**The Flame Burns in the Command Center.** 🇧🇧🔱

---

**Document Version**: 1.0  
**Last Updated**: December 30, 2025  
**Next Steps**: Frontend implementation sprint (Q1 2026)  
**Contact**: [Engineering Team]
