# Analytics Engine - Complete Implementation

## Overview

The **Analytics Engine** is the "eyes and mind" of CodexDominion - the intelligence layer that powers the Empire Dashboard and gives leadership real-time visibility into civilization health.

**Status**: ✅ OPERATIONAL - 7 endpoints implemented

---

## Purpose

The Analytics Engine exists to:
- Give leadership real-time visibility
- Measure youth engagement
- Track circle health
- Monitor mission completion
- Surface regional performance
- Highlight creator output
- Support data-driven decision-making and expansion

---

## Architecture

### Data Sources

The engine aggregates data from all CodexDominion 2.0 systems:
- **Users** - Active youth, captains, ambassadors, regional directors
- **Circles** - Membership, sessions, attendance
- **Missions** - Assignments, submissions, completion rates
- **Curriculum** - Module usage, weekly engagement
- **Culture** - Story views, ritual usage (Phase 2)
- **Creator Engine** - Artifacts, challenge submissions
- **Events** - Attendance, regional activity
- **Regions & Schools** - Expansion metrics

### Tech Stack

- **NestJS** - Controller + Service architecture
- **Prisma** - Database queries with aggregations
- **PostgreSQL** - Data storage
- **JWT Auth** - Role-based access control

---

## Endpoints

### 1. GET /api/v1/analytics/overview

**Purpose**: High-level KPIs for Empire Dashboard  
**Access**: Public (no auth required)  
**Returns**: System-wide metrics across all engines

**Response Structure**:
```json
{
  "users": {
    "total": 125,
    "youth": 100,
    "captains": 10,
    "ambassadors": 5,
    "regionalDirectors": 3
  },
  "circles": {
    "total": 15,
    "active": 12,
    "avgSize": 8
  },
  "missions": {
    "total": 24,
    "completedApproved": 180
  },
  "events": {
    "total": 8,
    "upcoming": 3
  },
  "creators": {
    "artifacts": 45
  },
  "expansion": {
    "regions": 5,
    "schools": 12
  },
  "season": {
    "current": "LEADERSHIP",
    "startDate": "2025-10-01",
    "endDate": "2025-12-31"
  },
  "message": "Empire Dashboard metrics loaded successfully",
  "timestamp": "2025-12-29T05:04:29Z"
}
```

**Use Cases**:
- Empire Dashboard homepage
- Leadership overview screen
- Council meetings
- Public stats page

---

### 2. GET /api/v1/analytics/circles

**Purpose**: Circle-by-circle health breakdown  
**Access**: Admin, Council, Regional Director, Youth Captain  
**Returns**: Detailed circle metrics with health status

**Response Structure**:
```json
[
  {
    "id": "circle-123",
    "name": "Kingston Youth Circle",
    "region": "Jamaica",
    "members": 12,
    "sessions": {
      "total": 48,
      "recent": 4,
      "avgAttendance": 9
    },
    "health": "healthy"
  }
]
```

**Health Status Logic**:
- **healthy**: 2+ sessions in last 30 days
- **moderate**: 1 session in last 30 days
- **inactive**: 0 sessions in last 30 days

**Use Cases**:
- Circle captain performance reviews
- Regional director oversight
- Circle support prioritization

---

### 3. GET /api/v1/analytics/missions

**Purpose**: Mission completion tracking  
**Access**: Admin, Council, Regional Director  
**Returns**: Mission-by-mission engagement metrics

**Response Structure**:
```json
[
  {
    "id": "mission-456",
    "title": "Master Your Craft - Week 1",
    "season": "MASTERY",
    "type": "GLOBAL",
    "assigned": 100,
    "submitted": 85,
    "approved": 72,
    "completionRate": 72
  }
]
```

**Use Cases**:
- Mission effectiveness analysis
- Curriculum refinement
- Youth progression tracking

---

### 4. GET /api/v1/analytics/regions

**Purpose**: Regional expansion and activity metrics  
**Access**: Admin, Council, Regional Director  
**Returns**: Region-by-region breakdown

**Response Structure**:
```json
[
  {
    "id": "region-789",
    "name": "Jamaica",
    "country": "Jamaica",
    "circles": 5,
    "schools": 12,
    "members": 60,
    "recentSessions": 20,
    "events": 3,
    "outreachEvents": 8,
    "activity": "high"
  }
]
```

**Activity Level Logic**:
- **high**: 4+ recent sessions
- **moderate**: 2-3 recent sessions
- **low**: 0-1 recent sessions

**Use Cases**:
- Regional director performance
- Expansion planning
- Resource allocation

---

### 5. GET /api/v1/analytics/creators

**Purpose**: Creator economy metrics  
**Access**: Admin, Council  
**Returns**: Artifact output, challenge metrics, top creators

**Response Structure**:
```json
{
  "totalCreators": 25,
  "totalArtifacts": 145,
  "recentSubmissions": 23,
  "artifactsByType": {
    "AUTOMATION": 45,
    "DESIGN": 38,
    "WRITING": 32,
    "VIDEO": 20,
    "APP": 10
  },
  "challenges": [
    {
      "id": "challenge-101",
      "title": "Mastery Season Creator Challenge",
      "season": "MASTERY",
      "submissions": 18,
      "deadline": "2025-03-31"
    }
  ],
  "topCreators": [
    { "email": "creator@example.com", "artifacts": 12 }
  ]
}
```

**Use Cases**:
- Creator performance tracking
- Challenge effectiveness
- Creator recognition

---

### 6. GET /api/v1/analytics/youth

**Purpose**: Youth engagement and progression  
**Access**: Admin, Council, Regional Director, Youth Captain  
**Returns**: Youth participation metrics by Rise Path

**Response Structure**:
```json
{
  "total": 100,
  "inCircles": 85,
  "withMissions": 90,
  "completedMissions": 72,
  "byRisePath": {
    "IDENTITY": 25,
    "MASTERY": 35,
    "CREATION": 25,
    "LEADERSHIP": 15
  },
  "engagementRate": 85
}
```

**Use Cases**:
- Youth engagement analysis
- Rise Path progression tracking
- Circle participation monitoring

---

### 7. GET /api/v1/analytics/events

**Purpose**: Event attendance and engagement  
**Access**: Admin, Council, Regional Director, Ambassador  
**Returns**: Event-by-event attendance metrics

**Response Structure**:
```json
[
  {
    "id": "event-202",
    "title": "Barbados Launch",
    "eventType": "LAUNCH",
    "region": "Barbados",
    "scheduledAt": "2025-03-01T20:00:00Z",
    "registered": 50,
    "present": 48,
    "attendanceRate": 96,
    "hasScript": true
  }
]
```

**Use Cases**:
- Event planning
- Attendance tracking
- Regional engagement
- Ceremony script effectiveness

---

## Integration Points

### Empire Dashboard

The primary consumer of analytics data:
- **Homepage**: Overview metrics
- **Circles Tab**: Circle health grid
- **Missions Tab**: Completion rates
- **Regions Tab**: Expansion map
- **Creators Tab**: Artifact gallery
- **Youth Tab**: Rise Path distribution

### Other Engines

Analytics aggregates from:
1. **Auth Engine** - User roles
2. **Circles Engine** - Sessions, attendance
3. **Missions Engine** - Assignments, submissions
4. **Events Engine** - Event attendance
5. **Creators Engine** - Artifacts, challenges
6. **Regions Engine** - Geographic data
7. **Schools Engine** - School expansion
8. **Culture Engine** - Story engagement (Phase 2)

---

## Role-Based Access

### Public Access
- ✅ `/analytics/overview` - System-wide stats

### Leadership Access
- **Admin + Council**: All endpoints
- **Regional Director**: Circles, missions, regions, youth, events
- **Youth Captain**: Circles, youth
- **Ambassador**: Events

---

## Performance Considerations

### Optimizations Implemented
1. **Parallel Queries**: `Promise.all()` for simultaneous data fetching
2. **Targeted Includes**: Only fetch needed relations
3. **Time-Windowed Filters**: Recent sessions (30 days), recent events (90 days)
4. **Aggregations**: `groupBy()` for average calculations
5. **Indexed Queries**: Leverage Prisma/PostgreSQL indexing

### Caching Strategy (Future)
- **Redis**: Cache overview metrics (15-minute TTL)
- **Computed Metrics**: Pre-calculate heavy aggregations
- **Background Jobs**: Update metrics snapshots hourly

---

## Future Enhancements (Phase 2+)

### Advanced Analytics
1. **Trend Analysis** - Week-over-week, month-over-month comparisons
2. **Predictive Metrics** - Youth churn risk, circle health forecasting
3. **Cohort Analysis** - Youth progression by season/region
4. **Funnel Tracking** - Registration → Circle → Mission → Creator pipeline

### Visualization
1. **Time Series Graphs** - Mission completion over time
2. **Geographic Heatmaps** - Regional activity intensity
3. **Network Graphs** - Circle relationships
4. **Sankey Diagrams** - Rise Path progression flows

### Exports
1. **CSV Downloads** - All metrics tables
2. **PDF Reports** - Monthly leadership reports
3. **API Webhooks** - Real-time metric updates
4. **PowerBI Integration** - Enterprise BI dashboards

### Alerts
1. **Circle Health Alerts** - Notify captain when circle goes inactive
2. **Mission Completion Alerts** - Low completion rate warnings
3. **Event Registration Alerts** - Low registration 48 hours before event
4. **Youth Engagement Alerts** - Youth not in circles or completing missions

---

## Testing

### Manual Testing

```bash
# Test overview
curl http://localhost:4000/api/v1/analytics/overview

# Test circles (requires auth)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:4000/api/v1/analytics/circles

# Test missions (requires auth)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:4000/api/v1/analytics/missions

# Test regions (requires auth)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:4000/api/v1/analytics/regions

# Test creators (requires auth)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:4000/api/v1/analytics/creators

# Test youth (requires auth)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:4000/api/v1/analytics/youth

# Test events (requires auth)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:4000/api/v1/analytics/events
```

### Expected Results

All endpoints should return:
- **Status 200** for successful requests
- **Status 401** for protected endpoints without auth
- **Status 403** for wrong role accessing protected endpoint
- **JSON response** with structured data

---

## Files Created/Modified

### Created
- None (analytics module already existed)

### Modified
1. **`backend/src/analytics/analytics.service.ts`** - 7 query methods (400+ lines)
2. **`backend/src/analytics/analytics.controller.ts`** - 7 REST endpoints with Swagger docs (130+ lines)

---

## Acceptance Criteria

### ✅ Phase 1 Complete

- [x] Overview metrics aggregate from all engines
- [x] Circle health metrics calculated correctly
- [x] Mission completion rates tracked
- [x] Regional expansion metrics available
- [x] Creator output tracked
- [x] Youth engagement measured
- [x] Event attendance tracked
- [x] Role-based access control applied
- [x] Swagger documentation complete
- [x] All endpoints operational

---

## Next Steps

### Immediate (Frontend)
1. Create Empire Dashboard React components
2. Integrate with analytics API
3. Build visualization charts
4. Add real-time updates

### Phase 2 (Advanced)
1. Implement Redis caching
2. Add time-series trend analysis
3. Create PDF report generation
4. Build alerting system

---

**Status**: ✅ Analytics Engine Phase 1 COMPLETE  
**Endpoints**: 7/7 operational  
**Backend**: http://localhost:4000/api/v1/analytics/  
**Documentation**: Swagger at /api-docs  
**Last Updated**: December 29, 2025

🔥 **The Dominion has eyes and wisdom!** 👁️
