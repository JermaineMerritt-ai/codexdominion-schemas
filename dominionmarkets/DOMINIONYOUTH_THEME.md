# DominionYouth Theme Specification

## 🎯 Overview

**Purpose:** Youthful, gamified interface for financial education platform targeting ages 13-22

**Design Philosophy:**
- **Vibrant:** Energetic colors that appeal to Gen Z aesthetic
- **Playful:** Rounded corners, friendly micro-interactions
- **Educational:** Clear visual hierarchy that guides learning
- **Safe:** Practice environment with no real money

**Target Audience:**
- Youth ages 13-22
- Students learning financial concepts
- First-time investors (practice only)
- Parents/guardians monitoring progress

---

## 🎨 COLOR SYSTEM

### Primary Colors

**Neon Teal (#00D9C0)**
- **Use:** Headers, navigation, success states, badge backgrounds
- **RGB:** 0, 217, 192
- **HSL:** 173°, 100%, 43%
- **Accessible on:** White text (AAA), Dark backgrounds (AAA)
- **Gradient variant:** `linear-gradient(135deg, #00D9C0 0%, #00B8A0 100%)`

**Coral Accent (#FF9580)**
- **Use:** Call-to-action buttons, achievement highlights, positive portfolio gains
- **RGB:** 255, 149, 128
- **HSL:** 8°, 100%, 75%
- **Accessible on:** White text (AA), Dark text (AAA)
- **Gradient variant:** `linear-gradient(135deg, #FF9580 0%, #FF7A61 100%)`

**Purple Accent (#9D4EDD)** (Secondary)
- **Use:** Premium features, advanced content, special challenges
- **RGB:** 157, 78, 221
- **HSL:** 273°, 68%, 59%
- **Accessible on:** White text (AAA)

### Semantic Colors

**Success:** `#00D9C0` (Neon Teal)
**Warning:** `#FFB547` (Amber)
**Error:** `#FF6B6B` (Coral Red)
**Info:** `#5B8DEF` (Sky Blue)

### Backgrounds

**Primary Background:** `#FFFFFF` (White)
**Secondary Background:** `#F5F5F5` (Light Gray)
**Card Background:** `#FFFFFF` with subtle Neon Teal border
**Overlay Background:** `rgba(0, 217, 192, 0.05)` (very subtle teal tint)

### Neutrals

**Dark Text:** `#0F172A` (Midnight)
**Medium Text:** `#64748B` (Slate)
**Light Text:** `#94A3B8` (Light Slate)
**Divider:** `#E2E8F0` (Very Light Gray)

---

## ✍️ TYPOGRAPHY

**Primary Font:** Inter (same as DominionMarkets)
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

**Monospace Font:** Roboto Mono (numbers, XP, scores)
```css
font-family: 'Roboto Mono', 'Courier New', monospace;
```

### Type Scale (Youth Variant)

| Token | Size | Weight | Line Height | Use Case |
|-------|------|--------|-------------|----------|
| `text-xs` | 12px | 400 | 1.4 | Metadata, timestamps |
| `text-sm` | 14px | 400 | 1.5 | Body text, labels |
| `text-base` | **17px** | 400 | 1.6 | Standard body text (larger for readability) |
| `text-lg` | 19px | 500 | 1.5 | Subheadings, emphasis |
| `text-xl` | 22px | 600 | 1.4 | Section titles |
| `text-2xl` | 26px | 700 | 1.3 | Page titles |
| `text-3xl` | 34px | 700 | 1.2 | Hero headings |
| `text-4xl` | 40px | 700 | 1.2 | XP display, big numbers |

**Note:** Base font size increased from 16px to 17px for youth readability

---

## 🧩 COMPONENT LIBRARY

### 1. Learning Badge

**Purpose:** Gamified achievement badge for completed education modules

**Visual Design:**
```
┌──────────────────┐
│   🏆 GOLD       │
│                 │
│  Earned: 12/24  │
│  100 XP         │
└──────────────────┘
```

**Specs:**
- **Width:** 120px
- **Height:** 140px
- **Background:** Neon Teal (#00D9C0) gradient
- **Border radius:** 16px (very rounded)
- **Icon size:** 48px × 48px (emoji or SVG)
- **Shadow:** `0px 4px 12px rgba(0, 217, 192, 0.3)`

**Badge Levels:**

| Level | Color | Icon | XP Required |
|-------|-------|------|-------------|
| Bronze | `#CD7F32` | 🥉 | 10 XP |
| Silver | `#C0C0C0` | 🥈 | 30 XP |
| Gold | `#FFD700` | 🏆 | 100 XP |
| Platinum | `#E5E4E2` | 💎 | 200 XP |

**Figma Component:**
```typescript
interface LearningBadge {
  level: 'bronze' | 'silver' | 'gold' | 'platinum';
  name: string;           // 'Module Master', 'Stock Scholar'
  earned: boolean;        // true = unlocked, false = locked
  earnedDate: string;     // 'Dec 24, 2025' or null
  xp: number;             // 100
  icon: string;           // '🏆' or SVG path
  description: string;    // 'Complete all 8 modules'
  progress?: {            // Optional progress tracking
    current: number;      // 5
    total: number;        // 8
  };
}
```

**Interactions:**
- **Hover:** Lift 4px, increase shadow
- **Click:** Show badge details modal (requirements, progress, earn date)
- **Locked state:** Grayscale filter, "🔒 Locked" text, reduced opacity (0.5)
- **Unlock animation:** Scale from 0 → 1.2 → 1.0 over 500ms, confetti burst effect

**States:**
- **Locked:** Grayscale, 50% opacity, lock icon
- **In Progress:** Color, progress bar (0-100%)
- **Earned:** Full color, glow effect, earned date displayed
- **Recently Earned:** Subtle pulse animation for 10 seconds

---

### 2. Mock Portfolio

**Purpose:** Safe practice portfolio for youth to simulate investing without real money

**Visual Design:**
```
┌───────────────────────────────────────────┐
│ 📊 MY PRACTICE PORTFOLIO                  │
│                                           │
│ Total Value: $10,000.00 (Starting)        │
│ Current Value: $10,485.20                 │
│ Gain: +$485.20 (+4.85%) 🎉                │
│                                           │
│ Holdings:                                 │
│ ┌───────────────────────────────────────┐ │
│ │ AAPL | 10 shares | $1,752.30        │ │
│ │ Gain: +$52.30 (+3.1%)               │ │
│ └───────────────────────────────────────┘ │
│ ┌───────────────────────────────────────┐ │
│ │ TSLA | 5 shares | $1,215.75         │ │
│ │ Loss: -$18.25 (-1.5%)               │ │
│ └───────────────────────────────────────┘ │
│                                           │
│ [Add Stock] [View Performance]            │
└───────────────────────────────────────────┘
```

**Specs:**
- **Width:** 100% (responsive)
- **Padding:** 24px
- **Background:** White (#FFFFFF)
- **Border:** 2px solid Neon Teal (#00D9C0)
- **Border radius:** 12px
- **Positive gains:** Coral Accent (#FF9580)
- **Negative losses:** Coral Red (#FF6B6B)
- **Starting balance:** $10,000 (virtual currency)

**Figma Component:**
```typescript
interface MockPortfolio {
  userId: string;
  startingBalance: number;     // 10000
  currentValue: number;         // 10485.20
  holdings: MockHolding[];
  createdDate: string;          // '2025-12-01'
  lastUpdated: string;          // '2025-12-24T10:30:00Z'
}

interface MockHolding {
  symbol: string;               // 'AAPL'
  shares: number;               // 10
  avgBuyPrice: number;          // 170.00
  currentPrice: number;         // 175.23
  totalValue: number;           // 1752.30
  gainLoss: number;             // +52.30
  gainLossPercent: number;      // +3.1
  purchaseDate: string;         // '2025-12-15'
}
```

**Interactions:**
- **"Add Stock" button:** Opens search modal for virtual purchases
  - Search by symbol or company name
  - Shows current price
  - User enters number of shares (max: remaining balance)
  - Confirmation: "Buy 10 shares of AAPL at $175.23?"
  - Virtual transaction completes instantly
- **"View Performance" button:** Opens chart showing portfolio value over time
  - Line chart (7-day, 30-day, All time)
  - Highlights gains/losses
  - Shows individual holding contributions
- **Click holding:** Show stock details (price history, news, why it moved)
- **Hover holding:** Tooltip with buy date, quantity, % of portfolio
- **Swipe to delete (mobile):** Remove holding from portfolio

**Safety Features:**
- **Virtual currency only:** Clearly labeled "This is a practice portfolio"
- **No real money:** Red banner: "⚠️ No real money is used. This is for learning."
- **Daily reset option:** "Start Fresh" button to reset to $10,000
- **Parent/guardian reporting:** Optional weekly email summary
- **Educational tooltips:** "Learn why" explanations for gains/losses
- **Age verification:** Requires birthdate (13+ only)

**Educational Elements:**
- **Performance metrics:** Total return %, best/worst performers, diversification score
- **Learning prompts:** "Why did AAPL go up today? Read verified news 📰"
- **Challenge integration:** "Add 3 tech stocks to earn Bronze badge 🥉"
- **Risk warnings:** "Your portfolio is 80% tech. Diversify to reduce risk."

---

### 3. Challenge Card

**Purpose:** Gamified challenge to encourage platform engagement

**Visual Design:**
```
┌────────────────────────────────────────┐
│ 🎯 WEEK 2 CHALLENGE                   │
│                                        │
│ Build Your First Mock Portfolio        │
│ Add 5 holdings to practice portfolio   │
│                                        │
│ Progress: ████████░░░░ 3/5             │
│ Reward: 20 XP + Bronze Badge 🥉         │
│                                        │
│ [Continue Challenge]                   │
└────────────────────────────────────────┘
```

**Specs:**
- **Width:** 100%
- **Padding:** 20px
- **Background:** White with Neon Teal border
- **Border:** 2px solid #00D9C0
- **Border radius:** 12px
- **Progress bar:** Neon Teal fill, Light Gray background
- **Hover:** Lift 2px, shadow increase

**Figma Component:**
```typescript
interface Challenge {
  id: string;
  week: number;                 // 2
  title: string;                // 'Build Your First Mock Portfolio'
  description: string;          // 'Add 5 holdings...'
  progress: {
    current: number;            // 3
    total: number;              // 5
  };
  rewards: {
    xp: number;                 // 20
    badges: string[];           // ['bronze']
  };
  status: 'active' | 'completed' | 'locked';
  dueDate?: string;             // Optional deadline
}
```

**Interactions:**
- **Click card:** Open challenge details page
- **"Continue Challenge" button:** Navigate to relevant feature
- **Progress updates:** Real-time updates as user progresses
- **Completion animation:** Confetti + "Challenge Complete!" modal

---

### 4. XP Progress Bar

**Purpose:** Display user's experience points and level

**Visual Design:**
```
┌──────────────────────────────────────────┐
│ Level 5 │ ████████████░░░░░░ 485/600 XP │
└──────────────────────────────────────────┘
```

**Specs:**
- **Height:** 32px
- **Fill color:** Neon Teal (#00D9C0) gradient
- **Background:** `#E2E8F0` (Light Gray)
- **Border radius:** 16px (pill shape)
- **Text:** Roboto Mono, 14px, white text inside bar
- **Animation:** Smooth fill on XP gain (500ms ease-out)

**Figma Component:**
```typescript
interface XPProgress {
  level: number;                // 5
  currentXP: number;            // 485
  nextLevelXP: number;          // 600
  totalXP: number;              // 2485 (all-time)
}
```

**Interactions:**
- **Hover:** Show tooltip "485/600 XP to Level 6"
- **XP gain animation:** Pulse effect + number count-up
- **Level up:** Special animation + "Level Up!" modal

---

### 5. Education Module Card

**Purpose:** Display education module with completion status

**Visual Design:**
```
┌────────────────────────────────────────┐
│ 📚 MODULE 1                           │
│                                        │
│ What is a Stock?                       │
│ Learn the basics of stock ownership    │
│                                        │
│ Duration: 3-5 minutes                  │
│ Reward: 10 XP + Quiz                   │
│                                        │
│ [Start Module] ✅ Completed            │
└────────────────────────────────────────┘
```

**Specs:**
- **Width:** 100% or 320px (grid layout)
- **Padding:** 20px
- **Background:** White
- **Border:** 1px solid #E2E8F0 (neutral), 2px solid Neon Teal (active/completed)
- **Border radius:** 12px

**States:**
- **Locked:** Grayscale, lock icon 🔒
- **Available:** Default colors, "Start Module" button
- **In Progress:** Orange accent, "Continue" button
- **Completed:** Green checkmark ✅, "Review" button

---

## 🎭 MICRO-INTERACTIONS

### Badge Unlock Animation
```
Duration: 800ms
Sequence:
1. Badge scales from 0 → 1.2 (300ms, ease-out)
2. Confetti burst (200ms)
3. Badge scales 1.2 → 1.0 (300ms, bounce)
4. Glow pulse (2s, fade out)
```

### XP Gain Animation
```
Duration: 500ms
Sequence:
1. "+20 XP" text floats up from action (300ms, ease-out)
2. XP bar fills (300ms, ease-in-out)
3. Text fades out (200ms)
Sound: Soft "ding" (optional)
```

### Challenge Completion
```
Duration: 1.5s
Sequence:
1. Progress bar fills to 100% (500ms)
2. Card border flashes Neon Teal (300ms)
3. Confetti burst + success modal (700ms)
Sound: Celebration chime
```

### Portfolio Gain Flash
```
Duration: 300ms
Trigger: Price update shows gain
Effect: Coral Accent background flash, fade to normal
```

### Button Hover (Youth Style)
```
Animation: Scale 1.05, shadow elevation
Duration: 150ms
Easing: ease-out
Border radius: 12px (more rounded than standard 8px)
```

---

## ♿ ACCESSIBILITY

**WCAG 2.1 AA Compliance:**
- Neon Teal (#00D9C0) on white: 4.5:1 (AA for text ≥18px)
- Coral Accent (#FF9580) on white: 4.5:1 (AA)
- Dark text (#0F172A) on white: 15:1 (AAA)

**Youth-Specific Considerations:**
- Larger base font (17px vs 16px) for readability
- High contrast mode option
- Reduced motion mode (disable all animations)
- Screen reader friendly labels
- Keyboard navigation for all interactions

---

## 📱 RESPONSIVE DESIGN

**Mobile (≤767px):**
- Single column layout
- Full-width cards
- Bottom sheet modals (not center popups)
- Touch-friendly targets (min 44px × 44px)

**Tablet (768-1023px):**
- 2-column grid for badges/challenges
- Sidebar navigation collapses to hamburger
- Portfolio table switches to card layout

**Desktop (≥1024px):**
- 3-4 column grid for badges
- Persistent sidebar navigation
- Full portfolio table view
- Hover states active

---

## 🎨 WIDGET SPECIFICATIONS

### Learning Badges Dashboard Section

**Layout:**
```
┌─────────────────────────────────────────────────┐
│ 🏆 MY BADGES                      View All →    │
├─────────────────────────────────────────────────┤
│                                                 │
│  [Bronze]  [Silver]  [Gold]  [🔒 Platinum]     │
│   Badge 1   Badge 2  Badge 3   Locked          │
│                                                 │
│  Progress: 3/4 badges earned                    │
│  Next unlock: Complete all 8 modules            │
└─────────────────────────────────────────────────┘
```

**Specs:**
- Section height: Auto (min 240px)
- Grid: 4 columns (desktop), 2 columns (mobile)
- Gap: 16px
- Background: White card on Warm Sand page
- Padding: 24px

---

### Mock Portfolio Dashboard Section

**Layout:**
```
┌─────────────────────────────────────────────────┐
│ 📊 MY PRACTICE PORTFOLIO           Manage →     │
├─────────────────────────────────────────────────┤
│                                                 │
│  Current Value: $10,485.20                      │
│  Gain: +$485.20 (+4.85%) 🎉                     │
│                                                 │
│  Top Performer: AAPL (+3.1%)                    │
│  Needs Attention: TSLA (-1.5%)                  │
│                                                 │
│  [View Full Portfolio] [Add Stock]              │
└─────────────────────────────────────────────────┘
```

**Specs:**
- Section height: Auto (min 200px)
- Chart: Mini line chart showing 7-day performance
- Background: White card with Neon Teal accent border
- Padding: 24px

---

### Active Challenges Section

**Layout:**
```
┌─────────────────────────────────────────────────┐
│ 🎯 ACTIVE CHALLENGES                            │
├─────────────────────────────────────────────────┤
│                                                 │
│  Week 2: Build Your Portfolio                   │
│  Progress: ████████░░░░ 3/5                     │
│  Reward: 20 XP + Bronze Badge                   │
│  [Continue →]                                   │
│                                                 │
│  Week 3: 7-Day Finance Challenge                │
│  Progress: ██░░░░░░░░░░ 1/7                     │
│  Reward: 50 XP + Silver Badge                   │
│  [Start →]                                      │
└─────────────────────────────────────────────────┘
```

**Specs:**
- Section height: Auto
- Card per challenge: Min 120px
- Stack vertically (no horizontal scroll)
- Background: White cards with colored borders (active = Neon Teal, locked = gray)

---

## 🚀 IMPLEMENTATION NOTES

**Tailwind Config Overrides (youth theme):**
```javascript
// tailwind.config.youth.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'youth-teal': '#00D9C0',
        'youth-coral': '#FF9580',
        'youth-purple': '#9D4EDD',
        'youth-amber': '#FFB547',
      },
      fontSize: {
        'base': '17px',  // Youth override (16px standard)
      },
      borderRadius: {
        'youth': '12px',  // More rounded than standard 8px
      },
    },
  },
};
```

**Component Naming Convention:**
- Prefix all DominionYouth components with `Youth-`
- Example: `<YouthBadge />`, `<YouthMockPortfolio />`, `<YouthChallenge />`

**Data Storage:**
- All mock portfolio data stored separately from real DominionMarkets portfolios
- Clear database separation: `youth_portfolios` table vs `portfolios` table
- No cross-contamination between real and practice data

**Safety Disclaimers:**
- Every page footer: "DominionYouth is an educational platform. No real money is used."
- First-time login: Full-screen modal explaining virtual currency
- Parent dashboard: Optional parental controls and progress reports

---

**Last Updated:** December 24, 2025
**Status:** Specification complete, ready for design + development
**Owner:** DominionYouth Product Team
