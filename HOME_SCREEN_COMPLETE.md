# 🏠 Home Screen — Empire Dashboard

**Status**: ✅ Fully Implemented (Frontend Ready)  
**Location**: `frontend/src/app/page.tsx`  
**Components**: `frontend/src/components/home/`

---

## Overview

The Home screen is the **primary entry point** for all users in the Codex Dominion Civilization Era. It answers three critical questions instantly:

1. **Who am I?** (Identity, role, season context)
2. **What is my mission this week?** (Mission Engine integration)
3. **What is the cultural rhythm right now?** (Culture Engine + Curriculum + Circles)

---

## Architecture

### 3-Panel Layout

```
┌─────────────────────────────────────────────────────────────┐
│  TOP BAR: Identity + Greeting + Season/Week                 │
├──────────────────────────────┬──────────────────────────────┤
│  LEFT COLUMN (2/3 width)     │  RIGHT COLUMN (1/3 width)    │
│  Civilization Pulse:          │  My Circle + Progress:       │
│  • Current Story              │  • Circle Info               │
│  • Current Mission            │  • Progress Stats            │
│  • Current Curriculum         │  (OR Admin Overview)         │
└──────────────────────────────┴──────────────────────────────┘
```

### Role-Based Views

**YOUTH View:**
- Civilization Pulse (stories, missions, curriculum)
- My Circle (next session, join link)
- My Progress (missions, attendance, streak)

**YOUTH_CAPTAIN View:**
- Civilization Pulse (same as Youth)
- My Circle (members, attendance stats)
- My Progress (same as Youth)
- **Additional Actions**: Schedule Session, Record Attendance

**ADMIN/REGIONAL_DIRECTOR/COUNCIL View:**
- Civilization Pulse (same as all users)
- **Admin Overview Card** (replaces Circle + Progress):
  - Active Youth count
  - Active Circles count
  - Missions completed this week
  - Regions active
  - Quick actions: Manage Missions, Manage Circles, View Content

---

## Components

### 1. **IdentityHeader.tsx**
Top bar showing greeting, role chip, and season/week.

**Props:**
- `userName`: string (from `/users/me`)
- `role`: UserRole enum
- `seasonName`: string (from `/seasons/current`)
- `currentWeek`: number (calculated from season start date)

**Features:**
- Flame icon 🔥
- Role-colored chips (Youth = blue, Captain = purple, Admin = red, etc.)
- Season + Week display

---

### 2. **CurrentStoryCard.tsx**
Displays the Story of the Week from Culture Engine.

**Props:**
- `title`: string
- `content`: string (markdown)
- `seasonName`: string (optional)
- `week`: number (optional)

**Features:**
- 2-3 line excerpt
- "Read Full Story" button opens modal
- Full story modal with close button
- Orange accent (🔥 culture theme)

**API:** `GET /culture/story/current`

---

### 3. **CurrentMissionCard.tsx**
Displays the current week's mission.

**Props:**
- `missionId`: string
- `title`: string
- `description`: string
- `status`: 'not-started' | 'in-progress' | 'submitted' | 'completed'
- `dueDate`: string (optional)

**Features:**
- Status chip with color coding
- "View Mission Details" link → `/missions/{id}`
- "Submit My Work" link → `/missions/{id}/submit` (if not submitted)
- Due date display
- Blue accent (🎯 mission theme)

**API:** `GET /missions/current`

---

### 4. **CurrentCurriculumCard.tsx**
Displays this week's curriculum modules (Story, Lesson, Activity).

**Props:**
- `modules`: Array<{ id, type, title }>
- `seasonName`: string
- `week`: number

**Features:**
- Type chips: STORY (orange), LESSON (purple), ACTIVITY (green)
- Icons: 📖 Story, 📝 Lesson, 🎨 Activity
- "Open Session Guide" button → `/curriculum`
- Purple accent (📚 curriculum theme)

**API:** `GET /curriculum/modules/current`

---

### 5. **MyCircleCard.tsx**
Displays user's primary circle info (youth or captain view).

**Props:**
- `circleId`: string
- `circleName`: string
- `role`: 'YOUTH' | 'YOUTH_CAPTAIN'
- `nextSessionDate`: string (optional)
- `nextSessionTime`: string (optional)
- `memberCount`: number (captain only)
- `lastAttendanceRate`: number (captain only)

**Youth View:**
- Next session date/time
- "Join This Week's Circle" button
- "View Sessions" button

**Captain View:**
- Members count card
- Last session attendance % card
- "Schedule Session" button → `/circles/{id}/schedule-session`
- "Record Attendance" button → `/circles/{id}/attendance`
- Indigo accent (⭕ circle theme)

**API:** `GET /circles` (filter by user membership)

---

### 6. **MyProgressCard.tsx**
Displays user's progress metrics.

**Props:**
- `missionsCompletedThisSeason`: number
- `sessionsAttendedThisMonth`: number
- `currentStreak`: number (weeks)

**Features:**
- Three cards: Missions (blue), Sessions (purple), Streak (orange 🔥)
- Clean, visual layout
- Green accent (📈 progress theme)

**Data Sources:**
- Missions: `/mission-submissions` (count with status=completed)
- Sessions: `/circles/:id/sessions` + attendance records
- Streak: calculated from weekly participation

---

### 7. **AdminOverviewCard.tsx**
Displays system-wide metrics for admins.

**Props:**
- `activeYouth`: number
- `activeCircles`: number
- `missionsCompletedThisWeek`: number
- `regionsActive`: number

**Features:**
- Four metric cards (blue, purple, green, orange)
- Three action buttons:
  - "Manage Missions" → `/admin/missions`
  - "Manage Circles" → `/admin/circles`
  - "View Stories & Curriculum" → `/admin/content`
- Red accent (👑 admin theme)

**API:** `GET /analytics/overview`

---

### 8. **HomeLayout.tsx**
Shell layout component for consistent structure.

**Props:**
- `header`: React.ReactNode (IdentityHeader)
- `leftColumn`: React.ReactNode (Civilization Pulse)
- `rightColumn`: React.ReactNode (Circle/Progress or Admin)

**Features:**
- Responsive grid layout (1 column mobile, 3 columns desktop)
- Left column: 2/3 width (lg:col-span-2)
- Right column: 1/3 width (lg:col-span-1)
- Gray background (#f3f4f6)

---

## API Hooks

**Location**: `frontend/src/lib/hooks/useHomeData.ts`

All hooks use React's `useEffect` for data fetching and provide:
- `data`: fetched data object/array
- `loading`: boolean loading state
- `error`: string error message (if any)

### Hooks List:

1. **`useCurrentUser(token)`** → `GET /users/me`
2. **`useUserProfile(token)`** → `GET /profiles/me`
3. **`useCurrentSeason()`** → `GET /seasons/current`
4. **`useCurrentStory(token)`** → `GET /culture/story/current`
5. **`useCurrentMission(token)`** → `GET /missions/current`
6. **`useCurrentCurriculum(token)`** → `GET /curriculum/modules/current`
7. **`useUserCircles(token)`** → `GET /circles`
8. **`useAnalyticsOverview(token)`** → `GET /analytics/overview`

**Authentication:**  
All hooks accept optional `token` parameter (JWT Bearer token from localStorage).

---

## Data Flow on Page Load

When Home screen mounts:

```typescript
1. Fetch user identity:
   → GET /users/me (name, email, roles)
   → GET /profiles/me (risePath, regionId, progress stats)

2. Fetch season context:
   → GET /seasons/current (name, startDate, endDate)
   → Calculate currentWeek from startDate

3. Fetch civilization pulse:
   → GET /culture/story/current (title, content, week)
   → GET /missions/current (title, description, dueDate)
   → GET /curriculum/modules/current (array of modules)

4. Fetch circle context (if YOUTH or YOUTH_CAPTAIN):
   → GET /circles (user's circles with nextSession)
   → (captain) Calculate attendance stats from sessions

5. Fetch admin analytics (if ADMIN/REGIONAL_DIRECTOR/COUNCIL):
   → GET /analytics/overview (activeYouth, activeCircles, etc.)
```

**Caching Strategy:**  
All data cached client-side for session duration (future: use React Query or SWR for automatic revalidation).

---

## Conditional Rendering Logic

### Role Detection:
```typescript
const getPrimaryRole = () => {
  const roleHierarchy = [
    'COUNCIL',
    'ADMIN',
    'REGIONAL_DIRECTOR',
    'YOUTH_CAPTAIN',
    'CREATOR',
    'YOUTH'
  ];
  return roleHierarchy.find((r) => user.roles.includes(r)) || 'YOUTH';
};
```

### View Selection:
```typescript
const isAdmin = ['ADMIN', 'REGIONAL_DIRECTOR', 'COUNCIL'].includes(primaryRole);
const isYouthCaptain = primaryRole === 'YOUTH_CAPTAIN';
const isYouth = primaryRole === 'YOUTH';

// Right column rendering:
{isAdmin ? (
  <AdminOverviewCard {...} />
) : (
  <>
    <MyCircleCard role={isYouthCaptain ? 'YOUTH_CAPTAIN' : 'YOUTH'} {...} />
    <MyProgressCard {...} />
  </>
)}
```

---

## Styling

**Design System:**
- **Font**: System fonts (clean, readable)
- **Colors**:
  - Culture (Stories): Orange (#f97316)
  - Missions: Blue (#3b82f6)
  - Curriculum: Purple (#a855f7)
  - Circles: Indigo (#6366f1)
  - Progress: Green (#10b981)
  - Admin: Red (#ef4444)
- **Layout**: Tailwind CSS utility classes
- **Spacing**: Consistent 6-unit padding/margins

**Responsive Breakpoints:**
- Mobile: 1 column layout
- Desktop (lg+): 3 column grid (2/3 left, 1/3 right)

---

## Testing Checklist

- [ ] **YOUTH View**:
  - [ ] Identity header displays correctly
  - [ ] Current story loads and modal works
  - [ ] Current mission displays with correct status
  - [ ] Curriculum modules display with type chips
  - [ ] My Circle card shows next session
  - [ ] Progress card displays all metrics

- [ ] **YOUTH_CAPTAIN View**:
  - [ ] Same as Youth view
  - [ ] Circle card shows member count + attendance %
  - [ ] "Schedule Session" and "Record Attendance" buttons visible

- [ ] **ADMIN View**:
  - [ ] Identity header shows ADMIN role
  - [ ] Civilization Pulse same as all users
  - [ ] Admin Overview card replaces Circle/Progress
  - [ ] All 4 metrics display correctly
  - [ ] 3 action buttons link to correct admin pages

- [ ] **Loading States**:
  - [ ] Loading spinner displays while fetching data
  - [ ] Graceful fallbacks for missing data

- [ ] **Error States**:
  - [ ] "Not logged in" message if no auth token
  - [ ] Error messages for failed API calls

- [ ] **Navigation**:
  - [ ] All links work correctly
  - [ ] Modal opens/closes properly

---

## Integration Requirements

### Backend Endpoints (Must Exist):
✅ `/users/me` (Auth module)  
✅ `/profiles/me` (Profiles module)  
✅ `/seasons/current` (Seasons module)  
✅ `/culture/story/current` (Culture module - **IMPLEMENTED**)  
⚠️ `/missions/current` (Missions module - **NEEDS UPDATE**)  
❌ `/curriculum/modules/current` (Curriculum module - **NOT YET IMPLEMENTED**)  
✅ `/circles` (Circles module)  
❌ `/analytics/overview` (Analytics module - **NOT YET IMPLEMENTED**)

### Next Steps:
1. **Fix Backend Build Errors** (16 webpack errors preventing port 4000 binding) - **CRITICAL BLOCKER**
2. Implement `/missions/current` endpoint (currently only `/missions` exists)
3. Implement Curriculum module with `/curriculum/modules/current` endpoint
4. Implement Analytics module with `/analytics/overview` endpoint
5. Test full integration with all components

---

## File Structure

```
frontend/
├── src/
│   ├── app/
│   │   └── page.tsx                    # Home page (main entry)
│   ├── components/
│   │   └── home/
│   │       ├── HomeLayout.tsx          # Shell layout
│   │       ├── IdentityHeader.tsx      # Top bar
│   │       ├── CurrentStoryCard.tsx    # Story of the week
│   │       ├── CurrentMissionCard.tsx  # Current mission
│   │       ├── CurrentCurriculumCard.tsx # Curriculum modules
│   │       ├── MyCircleCard.tsx        # Circle info
│   │       ├── MyProgressCard.tsx      # Progress metrics
│   │       └── AdminOverviewCard.tsx   # Admin dashboard
│   └── lib/
│       └── hooks/
│           └── useHomeData.ts          # API hooks
```

---

## 🔥 Status Summary

**✅ COMPLETE:**
- All 8 React components built
- All 8 API hooks created
- Home page with role-based rendering
- Responsive 3-panel layout
- Loading and error states
- Full documentation

**⚠️ BLOCKED BY:**
- Backend build errors (16 webpack compilation errors)
- Port 4000 not binding (backend not operational)

**📋 NEXT STEPS:**
1. Fix backend build errors (see last terminal output)
2. Start backend successfully on port 4000
3. Test Home screen with live API data
4. Implement missing endpoints (Curriculum, Analytics)
5. Deploy to production

---

**The Home screen is ready. The civilization awaits its people.** 🔱

