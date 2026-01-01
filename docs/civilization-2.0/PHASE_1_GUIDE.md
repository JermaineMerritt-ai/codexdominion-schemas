# Phase 1 Implementation Guide

## Overview

Phase 1 implements the **Minimum Viable Civilization**—the core engines needed to operate youth circles, deliver missions, share culture, and track progress. Everything else waits for Phase 2+.

## Phase 1 Engines (What We Build Now)

### 1. Auth & Identity
- User registration and login
- JWT access + refresh tokens
- Role-based access control (RBAC)
- Profile management with risePath
- Identity detection and routing

### 2. Seasons & Missions
- Seasonal rhythm (IDENTITY, MASTERY, CREATION, LEADERSHIP)
- Mission creation and assignment
- Mission submissions with reflections
- Mission review and approval workflow

### 3. Youth Circles
- Circle creation and management
- Circle membership
- Session scheduling
- Attendance tracking
- Basic circle dashboard

### 4. Culture Engine
- Cultural stories by season/week
- Story listing and filtering
- Current story display
- Story creation for admins

### 5. Analytics Overview
- Active youth count
- Active circles count
- Missions completed this week
- Regions active (basic count)

### 6. Minimal Admin
- Mission creation (ADMIN only)
- Mission assignment (ADMIN/YOUTH_CAPTAIN)
- Circle creation (ADMIN/AMBASSADOR)
- Story creation (ADMIN/COUNCIL)

## Phase 1 Endpoints (Complete List)

### Auth & Identity
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
GET    /api/v1/users/me
PATCH  /api/v1/users/me
GET    /api/v1/profiles/me
PATCH  /api/v1/profiles/me
```

### Seasons & Missions
```
GET    /api/v1/seasons
GET    /api/v1/seasons/current
GET    /api/v1/missions
GET    /api/v1/missions/current
GET    /api/v1/missions/:id
POST   /api/v1/missions
POST   /api/v1/missions/:id/assign
POST   /api/v1/mission-submissions
GET    /api/v1/mission-submissions
```

### Youth Circles
```
GET    /api/v1/circles
POST   /api/v1/circles
GET    /api/v1/circles/:id
PATCH  /api/v1/circles/:id
POST   /api/v1/circles/:id/members
DELETE /api/v1/circles/:id/members/:user_id
GET    /api/v1/circles/:id/sessions
POST   /api/v1/circles/:id/sessions
POST   /api/v1/circles/:id/sessions/:session_id/attendance
```

### Culture
```
GET    /api/v1/culture/story/current
GET    /api/v1/culture/stories
POST   /api/v1/culture/stories
```

### Analytics
```
GET    /api/v1/analytics/overview
```

**Total:** 25 endpoints

## Out of Scope for Phase 1

### Deferred to Phase 2+
❌ Curriculum modules (content delivery system)  
❌ Creator artifacts and challenges (full creator engine)  
❌ Regions, schools, ambassador outreach (geographic expansion)  
❌ Events and ceremonies (event management)  
❌ Advanced analytics (deep insights, charts, trends)  
❌ Portfolio showcase features  
❌ Economic engines (markets, portfolios, Cultural Alpha)  
❌ Dawn Dispatch automation  
❌ AI advisors  
❌ Marketplace

## Phase 1 Database Models

### Must Implement Now
- User
- Profile
- UserRole (enum)
- Season
- SeasonName (enum)
- Mission
- MissionType (enum)
- MissionAssignment
- MissionSubmission
- SubmissionStatus (enum)
- Circle
- CircleMember
- CircleSession
- SessionAttendance
- CulturalStory
- MetricSnapshot
- MetricType (enum)

### Defer to Phase 2+
- CurriculumModule
- ModuleType
- Artifact
- ArtifactType
- CreatorChallenge
- ChallengeSubmission
- Ritual
- RitualType
- Region
- School
- AmbassadorOutreach
- Event
- EventAttendance

## Development Sequence

### Week 1-2: Foundation
1. **Project Setup**
   - NestJS project initialization
   - PostgreSQL + Prisma setup
   - Environment configuration
   - Docker Compose for local dev

2. **Database Schema**
   - Prisma schema (Phase 1 models only)
   - Initial migration
   - Seed script for seasons

3. **Auth Module**
   - JWT strategy
   - Register/login/refresh
   - Bcrypt password hashing
   - RolesGuard implementation

### Week 3-4: Core Engines
4. **Users & Profiles Module**
   - User CRUD
   - Profile management
   - Role assignment
   - Identity detection

5. **Seasons Module**
   - Seasons listing
   - Current season logic
   - Season service

6. **Missions Module**
   - Mission CRUD
   - Assignment logic
   - Submission handling
   - Status tracking

### Week 5-6: Community & Culture
7. **Circles Module**
   - Circle CRUD
   - Membership management
   - Session scheduling
   - Attendance tracking

8. **Culture Module**
   - Story CRUD
   - Current story logic
   - Seasonal filtering

9. **Analytics Module**
   - Overview endpoint
   - Metric snapshot recording
   - Basic counts

### Week 7-8: Integration & Polish
10. **Integration Testing**
    - End-to-end tests
    - API contract validation
    - Error handling refinement

11. **Frontend Integration**
    - API client wrappers
    - Type generation from Prisma
    - Basic dashboards

12. **Documentation**
    - Swagger/OpenAPI complete
    - README updates
    - Deployment guide

## Testing Strategy

### Unit Tests
- Services: Business logic isolated
- Guards: Authorization logic
- Validators: DTO validation
- Target: 70%+ coverage

### Integration Tests
- API endpoints: Request/response contracts
- Database: Prisma queries
- Auth flow: Full registration/login cycle
- Target: All critical paths covered

### E2E Tests
- Full user journeys:
  - Register → Login → Create circle → Assign mission → Submit mission
  - Captain review mission → Approve submission
  - Admin create story → Users view story

## Deployment Checklist

### Pre-Deployment
- [ ] All Phase 1 endpoints implemented
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] E2E tests passing
- [ ] Swagger docs generated
- [ ] Environment variables documented
- [ ] Database migrations tested
- [ ] Seed data script working

### Deployment Steps
1. Provision PostgreSQL database
2. Run migrations (`pnpm prisma migrate deploy`)
3. Seed initial data (seasons, sample users)
4. Deploy backend to cloud (Azure/GCP/IONOS)
5. Configure environment variables
6. Verify health endpoint
7. Test critical flows

### Post-Deployment
- [ ] Health check passes
- [ ] Auth endpoints working
- [ ] Mission flow working
- [ ] Circle creation working
- [ ] Analytics returning data
- [ ] Swagger docs accessible
- [ ] Error monitoring setup
- [ ] Logs accessible

## Success Criteria

### Technical
- All 25 Phase 1 endpoints operational
- <200ms response time (p95)
- 99.9% uptime
- Zero security vulnerabilities
- Database migrations working
- Authentication secure (JWT, bcrypt)

### Functional
- Users can register and login
- Captains can create circles
- Youth can join circles
- Admins can create missions
- Missions can be assigned
- Youth can submit missions
- Cultural stories can be viewed
- Analytics shows basic metrics

### User Experience
- Clear error messages
- Identity-aware UI
- Swagger docs clear
- API responses consistent
- Fast page loads

## Phase 2 Preview

### What Comes Next
- Full curriculum delivery system
- Creator artifacts and challenges
- Regions and ambassador outreach
- Events and ceremonies
- Advanced analytics dashboards
- Portfolio showcase
- Economic engines (markets, portfolios)
- Dawn Dispatch automation
- AI advisors

### Why Phase 1 First
- Validates core architecture
- Establishes patterns
- Gets feedback from real users
- Proves identity-aware systems work
- Builds momentum without overbuilding

---

## References

- [.github/copilot-instructions.md](../../.github/copilot-instructions.md) - Complete architecture
- [schema.prisma](../../schema.prisma) - Full database schema
- [docs/api/openapi.yaml](../api/openapi.yaml) - API specification
- [Identity Architecture](IDENTITY_ARCHITECTURE.md) - Identity system
- [Youth Empire](YOUTH_EMPIRE.md) - Circles and missions
- [Cultural Core](CULTURAL_CORE.md) - Cultural stories
- [Governance & Leadership](GOVERNANCE_LEADERSHIP.md) - Roles and access
