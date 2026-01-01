# 🎭 Events & Ceremonies Engine - Quick Reference

## 🚀 Quick Start

### Get All Events
```bash
curl http://localhost:4000/api/v1/events
```

### Get Upcoming Events
```bash
curl "http://localhost:4000/api/v1/events?upcoming=true"
```

### Get Events by Type
```bash
# Season ceremonies
curl "http://localhost:4000/api/v1/events?eventType=SEASON_CEREMONY"

# Showcases
curl "http://localhost:4000/api/v1/events?eventType=SHOWCASE"

# Summits
curl "http://localhost:4000/api/v1/events?eventType=SUMMIT"
```

### Get Single Event with Attendance
```bash
curl http://localhost:4000/api/v1/events/EVENT_ID
```

### Get Attendance for Event
```bash
curl http://localhost:4000/api/v1/events/EVENT_ID/attendance
```

---

## 🎯 Seeded Event IDs

Use these IDs for testing:

- `season-ceremony-mastery-2025` - Dawn Ceremony (Barbados, March 21)
- `ambassador-gathering-barbados-feb` - Ambassador Event (Barbados, Feb 15)
- `youth-showcase-jamaica-march` - Showcase (Jamaica, March 8)
- `leadership-summit-2025` - Summit (Multi-region, July 15)
- `circle-ceremony-harrison-jan` - Circle Ceremony (Barbados, Jan 30 - PAST)
- `community-launch-nyc-feb` - Community Event (NYC, Feb 22)

---

## 🎭 Event Types

- `LAUNCH` - Grand opening events
- `CIRCLE_CEREMONY` - Youth circle rituals
- `SEASON_CEREMONY` - Seasonal transitions (Dawn/Day/Dusk/Night)
- `SHOWCASE` - Youth and creator presentations
- `SUMMIT` - Leadership gatherings
- `AMBASSADOR_EVENT` - Ambassador coordination meetings
- `COMMUNITY_EVENT` - Public community gatherings

---

## 👥 Attendance Status

- `REGISTERED` - Pre-registered, not yet attended
- `PRESENT` - Checked in at event
- `ABSENT` - Marked absent

---

## 🔐 Authentication (POST/PATCH/DELETE)

### 1. Login
```bash
curl -X POST http://localhost:4000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@codexdominion.com",
    "password": "Password123!"
  }'
```

### 2. Use Token
```bash
curl -X POST http://localhost:4000/api/v1/events \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Event",
    "eventType": "SHOWCASE",
    "scheduledAt": "2025-05-01T18:00:00.000Z"
  }'
```

---

## 📝 Record Attendance

### Single Record (snake_case)
```bash
curl -X POST http://localhost:4000/api/v1/events/EVENT_ID/attendance \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "USER_UUID",
    "status": "PRESENT",
    "checked_in_at": "2025-03-21T18:15:00.000Z"
  }'
```

### Batch Records (snake_case)
```bash
curl -X POST http://localhost:4000/api/v1/events/EVENT_ID/attendance \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      { "user_id": "UUID1", "status": "PRESENT" },
      { "user_id": "UUID2", "status": "PRESENT" },
      { "user_id": "UUID3", "status": "ABSENT" }
    ]
  }'
```

---

## 🛡️ Role Requirements

| Endpoint | Required Role |
|----------|---------------|
| GET /events | Public |
| GET /events/:id | Public |
| GET /events/:id/attendance | Public |
| POST /events | ADMIN / COUNCIL / REGIONAL_DIRECTOR / AMBASSADOR |
| PATCH /events/:id | ADMIN / COUNCIL / REGIONAL_DIRECTOR / AMBASSADOR |
| DELETE /events/:id | ADMIN / COUNCIL |
| POST /events/:id/attendance | ADMIN / COUNCIL / REGIONAL_DIRECTOR / AMBASSADOR / YOUTH_CAPTAIN |

---

## 📚 Full Documentation

See `EVENTS_ENGINE_STATUS.md` for complete endpoint documentation, examples, and testing scenarios.

---

**The flame burns at every ceremony.** 🔥
