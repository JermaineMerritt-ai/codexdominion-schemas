# Frontend Requirements - Leaderboard & Rankings

**Version:** 1.0  
**Last Updated:** December 24, 2025  
**Backend API:** ✅ Complete  
**Frontend Status:** 📋 Implementation Pending  

## Purpose

This document defines the frontend UI/UX requirements for the CodexDominion leaderboard system, including rank display, animations, badge presentation, and currentUser highlighting.

---

## 1. BACKEND API SUMMARY

### Endpoint: `GET /api/products/leaderboard`

**Query Parameters:**
- `period` (string): `"week"` or `"month"` (default: `"week"`)
- `currentUserId` (string, optional): User ID to highlight and track
- `limit` (number, optional): Max entries to return (default: 50)

**Response Format:**
```json
{
  "period": "week",
  "entries": [
    {
      "rank": 1,
      "userId": "user_123",
      "username": "JaneCreator",
      "totalEarnings": 1460.50,
      "creatorEarnings": 1200.00,
      "referrerEarnings": 260.50,
      "badges": ["top-10", "top-creator", "first-sale", "high-roller"]
    },
    {
      "rank": 2,
      "userId": "user_456",
      "username": "JohnReferrer",
      "totalEarnings": 890.25,
      "creatorEarnings": 0,
      "referrerEarnings": 890.25,
      "badges": ["top-10", "top-referrer", "first-sale"]
    }
  ],
  "currentUser": {
    "rank": 18,
    "userId": "user_789",
    "username": "CurrentUser",
    "totalEarnings": 100.00,
    "creatorEarnings": 80.00,
    "referrerEarnings": 20.00,
    "badges": ["first-sale"]
  },
  "totalUsers": 29
}
```

**Badge Types:**
- `top-10`: Rank ≤ 10
- `top-creator`: #1 in creator earnings
- `top-referrer`: #1 in referrer earnings
- `high-roller`: Total earnings ≥ $1,000
- `first-sale`: Has at least one sale

---

## 2. UI COMPONENTS

### 2.1 Leaderboard Page Layout

```
┌─────────────────────────────────────────────────┐
│  🏆 Leaderboard                                 │
│  ┌─────────┬─────────┐                          │
│  │ Weekly  │ Monthly │  ← Period Toggle         │
│  └─────────┴─────────┘                          │
│                                                  │
│  ┌─────────────────────────────────────────┐    │
│  │ 👤 Your Rank: #18 | Earnings: $100.00  │    │ ← CurrentUser Card
│  │ 🏅 Badges: first-sale                   │    │   (Highlighted)
│  └─────────────────────────────────────────┘    │
│                                                  │
│  ┌───────────────────────────────────────────┐  │
│  │ #1  👑 JaneCreator         $1,460.50     │  │ ← Rank Entry Card
│  │     🏅 top-10 • top-creator • high-roller│  │   (with badges)
│  └───────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────┐  │
│  │ #2  JohnReferrer           $890.25       │  │
│  │     🏅 top-10 • top-referrer              │  │
│  └───────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────┐  │
│  │ #3  MariaDesigner          $650.00       │  │
│  │     🏅 top-10 • first-sale                │  │
│  └───────────────────────────────────────────┘  │
│  ...                                             │
│  ┌───────────────────────────────────────────┐  │
│  │ Load More                                 │  │ ← Pagination
│  └───────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

### 2.2 Component Hierarchy

```
LeaderboardPage
├── PeriodToggle
│   ├── Button (Weekly)
│   └── Button (Monthly)
├── CurrentUserCard
│   ├── Rank Badge
│   ├── Username
│   ├── Earnings Display
│   └── Badge List
├── RankList
│   ├── RankCard (x N entries)
│   │   ├── Rank Number
│   │   ├── Username
│   │   ├── Earnings Display
│   │   └── Badge List
│   └── LoadMoreButton
└── RankUpAnimation (conditional)
```

---

## 3. DESIGN SPECIFICATIONS

### 3.1 CurrentUserCard (Highlighted)

**Purpose:** Make the logged-in user's rank immediately visible

**Visual Treatment:**
- Background: `bg-sovereign-emerald` or `bg-gradient-to-r from-gold-400 to-gold-600`
- Border: `border-2 border-gold-500`
- Shadow: `shadow-lg`
- Font: Bold username, larger rank number
- Icon: 👤 or custom avatar

**States:**
- **Default:** Highlighted with gold gradient
- **Hover:** Slight scale animation (`scale-105`)
- **Rank Change:** Trigger rank-up animation (see §4)

**Content:**
- Rank: `#18` (large, bold)
- Username: `CurrentUser` (bold, 16px)
- Earnings: `$100.00` (formatted currency)
- Badges: Icon grid (see §3.3)

**Responsive:**
- Desktop: Full card with all info
- Mobile: Condensed (rank + earnings on one line, badges below)

### 3.2 RankCard (Standard Entry)

**Purpose:** Display other users in the leaderboard

**Visual Treatment:**
- Background: `bg-sovereign-obsidian` (dark mode) or `bg-white` (light mode)
- Border: `border border-sovereign-slate`
- Hover: `hover:bg-sovereign-slate` + `shadow-md`
- Rank colors:
  - #1: Gold gradient + crown icon 👑
  - #2-3: Silver/bronze accent
  - #4-10: Blue accent (top-10 badge)
  - #11+: Default

**Content:**
- Rank: `#1` (left, bold, color-coded)
- Username: `JaneCreator` (center-left)
- Earnings: `$1,460.50` (right, bold)
- Badges: Icon row below username (see §3.3)

**Responsive:**
- Desktop: Single row with all info
- Mobile: Stack (rank + username on top, earnings + badges below)

### 3.3 Badge Display

**Badge Icons:**
```typescript
const BADGE_ICONS = {
  'top-10': '🏆',
  'top-creator': '🎨',
  'top-referrer': '📢',
  'high-roller': '💰',
  'first-sale': '⭐'
};
```

**Badge Tooltips:**
```typescript
const BADGE_TOOLTIPS = {
  'top-10': 'Top 10 Earner',
  'top-creator': '#1 Creator Earnings',
  'top-referrer': '#1 Referrer Earnings',
  'high-roller': 'Earned $1,000+',
  'first-sale': 'Made First Sale'
};
```

**Visual Treatment:**
- Size: 24px icons
- Spacing: 8px gap between badges
- Hover: Show tooltip with badge name
- Animation: Subtle pulse on new badge earned

**Layout:**
- Horizontal row below username
- Max 5 badges (all current types fit)
- Mobile: Smaller icons (20px), wrap if needed

### 3.4 Period Toggle

**States:**
- **Active:** `bg-gold-500 text-white`
- **Inactive:** `bg-transparent text-gray-600 hover:bg-gray-100`

**Behavior:**
- Click → Fetch new data with period parameter
- Smooth transition (fade-out old list, fade-in new list)
- Loading state: Show skeleton cards

**Accessibility:**
- ARIA role: `tablist` / `tab`
- Keyboard navigation: Arrow keys + Enter

---

## 4. ANIMATIONS

### 4.1 Rank-Up Animation

**Trigger:** When user's rank improves (detected via local storage or API comparison)

**Animation Sequence:**
1. **Confetti Burst:** Multi-color confetti from currentUserCard
2. **Card Pulse:** CurrentUserCard scales up (`scale-110`) then back (`scale-100`)
3. **Rank Number Change:** Old rank fades out, new rank fades in with slide-up motion
4. **Badge Reveal:** If new badge earned, icon pulses 3x with gold glow
5. **Toast Notification:** "🎉 You moved up to rank #15!"

**Implementation (Framer Motion example):**
```tsx
import { motion, AnimatePresence } from 'framer-motion';

const RankUpAnimation = ({ newRank, oldRank, newBadges }) => {
  return (
    <AnimatePresence>
      {/* Confetti Component */}
      <Confetti active={true} duration={3000} />
      
      {/* Card Pulse */}
      <motion.div
        animate={{ scale: [1, 1.1, 1] }}
        transition={{ duration: 0.6, ease: "easeInOut" }}
      >
        <CurrentUserCard rank={newRank} badges={newBadges} />
      </motion.div>
      
      {/* Toast */}
      <Toast message={`🎉 You moved up to rank #${newRank}!`} />
    </AnimatePresence>
  );
};
```

**Timing:**
- Total duration: 3 seconds
- Confetti: 0-3s
- Pulse: 0-0.6s
- Badge reveal: 1-2s
- Toast: 2-5s (auto-dismiss)

**Audio (Optional):**
- Success sound: Short chime (0.5s)
- Mute option in settings

### 4.2 Badge Earned Animation

**Trigger:** New badge appears in user's badge list

**Animation:**
1. Badge icon fades in from 0 opacity
2. Icon pulses 3x with gold glow effect
3. Tooltip appears briefly ("High Roller Unlocked!")
4. Icon settles into badge row

**Implementation:**
```tsx
const BadgeReveal = ({ badgeType, icon, tooltip }) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.5 }}
      animate={{ 
        opacity: 1, 
        scale: [1, 1.2, 1, 1.2, 1],
        boxShadow: [
          '0 0 0px gold',
          '0 0 20px gold',
          '0 0 0px gold',
          '0 0 20px gold',
          '0 0 0px gold'
        ]
      }}
      transition={{ duration: 1.5 }}
      title={tooltip}
    >
      {icon}
    </motion.div>
  );
};
```

### 4.3 List Transitions

**When switching periods (week ↔ month):**
- Fade-out current list (200ms)
- Show loading skeleton cards (3 rows)
- Fetch new data
- Fade-in new list (300ms)
- Stagger animation: Each card appears 50ms after previous

**Implementation (CSS transition):**
```css
.rank-card {
  transition: all 0.3s ease-in-out;
}

.rank-card-enter {
  opacity: 0;
  transform: translateY(20px);
}

.rank-card-enter-active {
  opacity: 1;
  transform: translateY(0);
}
```

---

## 5. INTERACTIONS

### 5.1 CurrentUser Highlighting

**Detection Logic:**
```typescript
const currentUserId = useAuth().userId; // From auth context

useEffect(() => {
  // Fetch leaderboard with currentUserId parameter
  fetch(`/api/products/leaderboard?period=${period}&currentUserId=${currentUserId}`)
    .then(res => res.json())
    .then(data => {
      setCurrentUser(data.currentUser);
      setEntries(data.entries);
    });
}, [period, currentUserId]);
```

**Highlighting:**
- If `currentUser` exists in response, render CurrentUserCard at top
- In main list, if entry.userId === currentUserId, apply highlighted style
- Scroll behavior: On page load, auto-scroll to currentUser's position if rank > 10

### 5.2 Rank Change Detection

**Strategy:** Compare current rank with cached rank from local storage

```typescript
useEffect(() => {
  const cachedRank = localStorage.getItem('userRank');
  const newRank = currentUser?.rank;
  
  if (cachedRank && newRank && parseInt(cachedRank) > newRank) {
    // Rank improved! Trigger animation
    setShowRankUpAnimation(true);
    
    // Check for new badges
    const cachedBadges = JSON.parse(localStorage.getItem('userBadges') || '[]');
    const newBadges = currentUser.badges.filter(b => !cachedBadges.includes(b));
    if (newBadges.length > 0) {
      setNewBadges(newBadges);
    }
  }
  
  // Update cache
  localStorage.setItem('userRank', newRank.toString());
  localStorage.setItem('userBadges', JSON.stringify(currentUser.badges));
}, [currentUser]);
```

**Caveats:**
- Only trigger animation once per session (use session flag)
- Handle edge cases (first visit, rank dropped, etc.)

### 5.3 Load More (Pagination)

**Implementation:**
```typescript
const [limit, setLimit] = useState(50);

const loadMore = () => {
  setLimit(prev => prev + 50);
};

useEffect(() => {
  fetch(`/api/products/leaderboard?period=${period}&limit=${limit}`)
    .then(res => res.json())
    .then(data => setEntries(data.entries));
}, [limit, period]);
```

**UI:**
- Button: "Load More" (only show if totalUsers > current entries length)
- Loading state: Show skeleton cards while fetching
- Infinite scroll (optional): Load more when user scrolls to bottom

---

## 6. RESPONSIVE DESIGN

### Desktop (≥1024px)
```
┌─────────────────────────────────────────────────┐
│  CurrentUserCard (full width)                   │
│  ┌───┬────────────┬──────────┬──────────┐       │
│  │ # │ Username   │ Earnings │ Badges   │       │
│  └───┴────────────┴──────────┴──────────┘       │
└─────────────────────────────────────────────────┘
```

### Tablet (768px-1023px)
```
┌─────────────────────────────────┐
│  CurrentUserCard (condensed)     │
│  ┌───┬──────────┬──────────┐     │
│  │ # │ Username │ $Amount  │     │
│  │   │ Badges   │          │     │
│  └───┴──────────┴──────────┘     │
└─────────────────────────────────┘
```

### Mobile (≤767px)
```
┌───────────────────┐
│  CurrentUser      │
│  #18 | $100.00   │
│  🏅 first-sale    │
│                   │
│  #1 Jane | $1460 │
│  🏆🎨💰⭐         │
└───────────────────┘
```

**Mobile Adjustments:**
- Stack rank + username on top
- Earnings below username (right-aligned)
- Badges as icon grid (2 rows if > 3 badges)
- Period toggle: Full-width buttons
- Font sizes: Reduce by 2px across board

---

## 7. ACCESSIBILITY

### WCAG 2.1 AA Compliance

**Keyboard Navigation:**
- Tab through period toggle, cards, load more button
- Enter/Space to activate buttons
- Arrow keys for period toggle (role="tablist")

**Screen Readers:**
```html
<div role="region" aria-label="Leaderboard Rankings">
  <div role="tablist" aria-label="Time Period">
    <button role="tab" aria-selected="true">Weekly</button>
    <button role="tab" aria-selected="false">Monthly</button>
  </div>
  
  <article aria-label="Your Rank: 18, Earnings: $100.00">
    <!-- CurrentUserCard content -->
  </article>
  
  <ol aria-label="Leaderboard Entries">
    <li aria-label="Rank 1: JaneCreator, Earnings: $1460.50">
      <!-- RankCard content -->
    </li>
  </ol>
</div>
```

**Color Contrast:**
- Gold badges: Ensure 4.5:1 contrast ratio against background
- Text: 7:1 contrast for body text
- CurrentUser highlight: Maintain readability with background gradient

**Focus Indicators:**
- Visible focus ring on all interactive elements
- High contrast mode support

**Motion Preferences:**
```css
@media (prefers-reduced-motion: reduce) {
  .rank-up-animation,
  .badge-reveal {
    animation: none !important;
    transition: none !important;
  }
}
```

---

## 8. PERFORMANCE

### Optimization Strategies

**Data Fetching:**
- Cache leaderboard data for 30 seconds (SWR or React Query)
- Prefetch next page on "Load More" hover
- Debounce period toggle to prevent spam clicks

**Rendering:**
- Virtualize list if entries > 100 (react-window or react-virtuoso)
- Memoize RankCard components
- Lazy load animations (dynamic import)

**Bundle Size:**
- Code-split leaderboard page
- Lazy load Framer Motion (~50KB)
- Use CSS animations for simple transitions

**Example (React Query):**
```typescript
import { useQuery } from '@tanstack/react-query';

const { data, isLoading } = useQuery({
  queryKey: ['leaderboard', period, currentUserId],
  queryFn: () => 
    fetch(`/api/products/leaderboard?period=${period}&currentUserId=${currentUserId}`)
      .then(res => res.json()),
  staleTime: 30000, // 30 seconds
  cacheTime: 300000 // 5 minutes
});
```

---

## 9. ERROR STATES

### API Errors

**No data available:**
```
┌─────────────────────────────────┐
│  🏆 Leaderboard                 │
│                                  │
│  No earnings yet this week.     │
│  Be the first to make a sale!   │
│                                  │
│  [View Products]                │
└─────────────────────────────────┘
```

**Network error:**
```
┌─────────────────────────────────┐
│  ⚠️ Unable to load leaderboard  │
│                                  │
│  Please check your connection   │
│  and try again.                 │
│                                  │
│  [Retry]                        │
└─────────────────────────────────┘
```

**User not ranked (0 earnings):**
- Show currentUserCard with rank "Unranked"
- Message: "Make your first sale to appear on the leaderboard"
- CTA: "Upload Product" button

---

## 10. IMPLEMENTATION CHECKLIST

### Phase 1: Core UI (2-3 days)
- [ ] Create LeaderboardPage component
- [ ] Implement PeriodToggle with state management
- [ ] Build RankCard component with responsive design
- [ ] Build CurrentUserCard with highlighted styling
- [ ] Add badge icons and tooltips
- [ ] Implement basic list rendering
- [ ] Add loading states (skeleton cards)
- [ ] Add error states (network, no data)

### Phase 2: Interactions (1-2 days)
- [ ] Integrate with `/api/products/leaderboard` endpoint
- [ ] Implement period switching with data refresh
- [ ] Add pagination (Load More button)
- [ ] Detect currentUser and highlight in list
- [ ] Implement rank change detection (local storage)
- [ ] Add scroll-to-user behavior

### Phase 3: Animations (1-2 days)
- [ ] Install Framer Motion or animation library
- [ ] Build RankUpAnimation component
- [ ] Build BadgeReveal animation
- [ ] Add confetti effect
- [ ] Add toast notifications
- [ ] Implement list transitions (fade in/out)
- [ ] Add prefers-reduced-motion support

### Phase 4: Polish (1 day)
- [ ] Responsive design testing (mobile, tablet, desktop)
- [ ] Accessibility audit (keyboard nav, screen readers)
- [ ] Color contrast validation
- [ ] Performance optimization (virtualization, caching)
- [ ] Edge case testing (no earnings, first visit, rank drop)
- [ ] Cross-browser testing

### Phase 5: Integration (1 day)
- [ ] Add leaderboard link to navigation
- [ ] Link from dashboard widgets
- [ ] Add leaderboard preview to homepage
- [ ] Update onboarding to mention leaderboard
- [ ] Add analytics tracking (page views, period switches, load more clicks)

---

## 11. TECH STACK RECOMMENDATIONS

### React/Next.js Implementation

**Core Libraries:**
- `@tanstack/react-query`: Data fetching and caching
- `framer-motion`: Animations (rank-up, badge reveal)
- `react-confetti`: Confetti effect
- `react-hot-toast`: Toast notifications

**Optional:**
- `react-window`: List virtualization (if > 100 entries)
- `date-fns`: Date formatting (for "Last 7 days" text)
- `numeral`: Currency formatting ($1,460.50)

**File Structure:**
```
src/
├── pages/
│   └── leaderboard.tsx
├── components/
│   ├── leaderboard/
│   │   ├── LeaderboardPage.tsx
│   │   ├── PeriodToggle.tsx
│   │   ├── CurrentUserCard.tsx
│   │   ├── RankCard.tsx
│   │   ├── BadgeDisplay.tsx
│   │   ├── RankUpAnimation.tsx
│   │   └── LoadMoreButton.tsx
├── hooks/
│   ├── useLeaderboard.ts
│   ├── useRankChange.ts
│   └── useBadgeReveal.ts
├── lib/
│   ├── api.ts (fetch functions)
│   └── constants.ts (badge icons, tooltips)
└── styles/
    └── leaderboard.module.css
```

---

## 12. ANALYTICS TRACKING

Track these events for product insights:

**Page Events:**
- `leaderboard_viewed` (period: week|month)
- `period_toggled` (from: week, to: month)
- `load_more_clicked` (current_count: 50)

**Engagement Events:**
- `rank_card_clicked` (rank: 1, userId: user_123)
- `badge_tooltip_hovered` (badgeType: top-creator)
- `current_user_scrolled_to` (rank: 18)

**Success Events:**
- `rank_up_animation_triggered` (oldRank: 20, newRank: 18)
- `new_badge_earned` (badgeType: high-roller)
- `first_time_ranked` (rank: 45)

**Implementation (example with Google Analytics):**
```typescript
import { trackEvent } from '@/lib/analytics';

// Track page view
useEffect(() => {
  trackEvent('leaderboard_viewed', { period });
}, [period]);

// Track rank-up
useEffect(() => {
  if (showRankUpAnimation) {
    trackEvent('rank_up_animation_triggered', {
      oldRank: cachedRank,
      newRank: currentUser.rank
    });
  }
}, [showRankUpAnimation]);
```

---

## NEXT STEPS

1. **Review and Approve:** Share this spec with design + engineering teams
2. **Figma Mockups:** Create high-fidelity mockups based on §3 (Design Specs)
3. **API Testing:** Verify backend endpoint returns expected data
4. **Sprint Planning:** Allocate 1 week sprint for implementation (Phases 1-5)
5. **Launch:** Deploy behind feature flag, gather user feedback, iterate

---

**End of Frontend Requirements**  
**Related Docs:**
- [CONTENT_GOVERNANCE.md](CONTENT_GOVERNANCE.md) - Copy and messaging
- [BRAND_CONTENT_BIBLE.md](BRAND_CONTENT_BIBLE.md) - Brand voice and tone
- [Backend API Docs](../products_api.py) - Leaderboard endpoint details
