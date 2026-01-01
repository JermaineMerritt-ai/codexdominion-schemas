# Intelligence Engine - Result Format Specification

## Overview

The Intelligence Engine now supports **4 types of intelligence** with **audience targeting** and **domain classification** for sophisticated monitoring and insights.

## TypeScript Interface

```typescript
interface RuleEvaluationResult {
  type: "alert" | "recommendation" | "forecast" | "opportunity";
  domain: "youth" | "circles" | "missions" | "curriculum" | "culture" | "creators" | "expansion";
  message: string;
  severity?: "low" | "medium" | "high";
  audience: ("captain" | "director" | "admin" | "council" | "creator" | "educator")[];
  metadata?: Record<string, any>;
}
```

## Intelligence Types

### 🚨 Alert
**Purpose:** Urgent issues requiring immediate attention  
**Use Cases:**
- Attendance drops
- Stale missions
- Inactive youth
- Circle health issues

**Example:**
```json
{
  "type": "alert",
  "domain": "circles",
  "message": "Circle Alpha attendance dropped 22% over 2 weeks",
  "severity": "high",
  "audience": ["captain", "director", "admin"],
  "metadata": {
    "circleId": "abc-123",
    "circleName": "Circle Alpha",
    "dropPercentage": 22,
    "oldAverage": 75,
    "newAverage": 53
  }
}
```

### 💡 Recommendation
**Purpose:** Suggested actions for improvement  
**Use Cases:**
- Circle merging suggestions
- Youth mentorship opportunities
- Mission adjustments
- Resource reallocation

**Example:**
```json
{
  "type": "recommendation",
  "domain": "circles",
  "message": "Circle Beta has only 3 members - consider merging with nearby circles",
  "severity": "medium",
  "audience": ["captain", "director"],
  "metadata": {
    "circleId": "xyz-456",
    "circleName": "Circle Beta",
    "memberCount": 3,
    "suggestedMergeCircles": ["circle-789", "circle-012"],
    "proximityKm": [2.5, 3.8]
  }
}
```

### 📈 Forecast
**Purpose:** Predictive insights about trends  
**Use Cases:**
- Mission completion projections
- Attendance trend predictions
- Growth trajectory analysis
- Seasonal planning insights

**Example:**
```json
{
  "type": "forecast",
  "domain": "missions",
  "message": "Current trend projects 45% mission completion this month",
  "severity": "medium",
  "audience": ["director", "admin"],
  "metadata": {
    "projectedRate": 45,
    "currentRate": 48,
    "trend": "declining",
    "daysRemaining": 15,
    "historicalAverage": 62,
    "confidenceLevel": 0.85
  }
}
```

### 🎯 Opportunity
**Purpose:** Growth opportunities to pursue  
**Use Cases:**
- Youth outreach potential
- Creator engagement opportunities
- Expansion possibilities
- Resource optimization

**Example:**
```json
{
  "type": "opportunity",
  "domain": "youth",
  "message": "5 youth with low attendance could benefit from one-on-one outreach",
  "severity": "low",
  "audience": ["captain", "educator"],
  "metadata": {
    "youthIds": ["user-1", "user-2", "user-3", "user-4", "user-5"],
    "avgAttendance": 35,
    "suggestedAction": "schedule_mentoring_sessions",
    "estimatedEngagementLift": "25%"
  }
}
```

## Domains

- **youth** - Youth engagement, attendance, progression
- **circles** - Circle health, sessions, membership
- **missions** - Mission completion, assignments, submissions
- **curriculum** - Curriculum delivery, content effectiveness
- **culture** - Cultural stories, rituals, engagement
- **creators** - Creator activity, artifacts, challenges
- **expansion** - Regional growth, outreach, scaling

## Audience Roles

- **captain** - Youth Circle captains (frontline leaders)
- **director** - Regional directors (regional oversight)
- **admin** - System administrators (operational control)
- **council** - Council members (strategic governance)
- **creator** - Creator community (builder network)
- **educator** - Curriculum educators (content delivery)

## Severity Levels

- **low** - Informational, no immediate action required
- **medium** - Moderate concern, action recommended soon
- **high** - Critical issue, immediate attention needed

## Implementation Examples

### Implemented Rules

**C2 - Circle Attendance Drop (Alert):**
```typescript
const C2: RuleDefinition = {
  evaluator: async () => {
    // Database analysis...
    if (dropPercentage >= 20) {
      return {
        type: 'alert',
        domain: 'circles',
        message: `Circle ${name} attendance dropped ${drop}% over 2 weeks`,
        severity: 'high',
        audience: ['captain', 'director', 'admin'],
        metadata: { circleId, dropPercentage, oldAverage, newAverage }
      };
    }
  }
};
```

### Stub Examples

**Y1 - Youth Outreach Opportunity:**
```typescript
// type: 'opportunity'
// domain: 'youth'
// message: '5 youth with low attendance could benefit from one-on-one outreach'
// audience: ['captain', 'educator']
```

**C3 - Circle Size Recommendation:**
```typescript
// type: 'recommendation'
// domain: 'circles'
// message: 'Circle Beta has only 3 members - consider merging'
// audience: ['captain', 'director']
```

**M1 - Mission Completion Forecast:**
```typescript
// type: 'forecast'
// domain: 'missions'
// message: 'Current trend projects 45% mission completion this month'
// audience: ['director', 'admin']
```

## API Usage

### Evaluate Single Rule
```bash
curl -X POST http://localhost:8080/api/v1/intelligence/evaluate/C2
```

**Response when triggered:**
```json
{
  "ruleId": "C2",
  "triggered": true,
  "type": "alert",
  "domain": "circles",
  "message": "Circle Alpha attendance dropped 22% over 2 weeks",
  "severity": "high",
  "audience": ["captain", "director", "admin"],
  "metadata": { ... }
}
```

**Response when not triggered:**
```json
{
  "ruleId": "C2",
  "triggered": false
}
```

### Evaluate Weekly Batch
```bash
curl -X POST "http://localhost:8080/api/v1/intelligence/evaluate?trigger=weekly"
```

**Response:**
```json
[
  {
    "ruleId": "C2",
    "type": "alert",
    "domain": "circles",
    "message": "...",
    "severity": "high",
    "audience": ["captain", "director", "admin"],
    "metadata": { ... }
  }
]
```

## Frontend Integration Patterns

### Audience Filtering
```typescript
// Show only intelligence for logged-in user's role
const userRole = currentUser.role; // 'captain' | 'director' | etc.
const relevantIntel = intelligence.filter(item => 
  item.audience.includes(userRole)
);
```

### Type-Based Styling
```typescript
const typeStyles = {
  alert: { icon: '🚨', color: 'red', priority: 1 },
  recommendation: { icon: '💡', color: 'yellow', priority: 2 },
  forecast: { icon: '📈', color: 'blue', priority: 3 },
  opportunity: { icon: '🎯', color: 'green', priority: 4 }
};
```

### Domain Grouping
```typescript
const byDomain = intelligence.reduce((acc, item) => {
  if (!acc[item.domain]) acc[item.domain] = [];
  acc[item.domain].push(item);
  return acc;
}, {});
```

## Next Steps

1. **Implement remaining evaluators** (Y1-Y3, C1, C3, M1-M3)
2. **Connect to AlertsService** for automated alert creation
3. **Add scheduled execution** (cron jobs for daily/weekly/monthly)
4. **Build frontend dashboard** with audience filtering
5. **Add notification system** for high-severity alerts
6. **Implement action tracking** (mark recommendations as completed)

---

**Status:** Enhanced format deployed ✅  
**Last Updated:** December 29, 2025  
**Version:** 2.0
