# DOMINIONMARKETS — UI SYSTEM

> **Purpose:** Figma-ready, production-ready interface design system  
> **Alignment:** CodexDominion visual language with financial data optimization  
> **Status:** Design specification for implementation

---

## 🎨 DESIGN PRINCIPLES

### 1. Clarity First
Financial data is complex. The UI must reduce cognitive load, not add to it.

### 2. Data Density Without Clutter
Show critical information at a glance. Progressive disclosure for details.

### 3. Trust Through Design
Professional, credible, stable. No flashy animations or gimmicks.

### 4. Responsive by Default
Mobile-first design. Desktop enhances, doesn't replace.

### 5. Accessibility
WCAG 2.1 AA compliant. High contrast. Screen reader friendly.

---

## 📐 LAYOUT & STRUCTURE

### Grid System

**Desktop (≥1200px):**
- **12-column grid**
- Gutter: 24px
- Max content width: 1200px
- Side margins: Auto-center

**Tablet (768px - 1199px):**
- **8-column grid**
- Gutter: 20px
- Max content width: 960px
- Side margins: 24px

**Mobile (≤767px):**
- **4-column grid**
- Gutter: 16px
- Max content width: 100%
- Side margins: 16px

### Spacing Scale

**Base Unit:** 8px (0.5rem)

| Token | Value | Use Case |
|-------|-------|----------|
| `space-xs` | 4px | Icon spacing, micro-adjustments |
| `space-sm` | 8px | Component padding, tight spacing |
| `space-md` | 16px | Standard component spacing |
| `space-lg` | 24px | Card padding, section spacing |
| `space-xl` | 32px | Major section breaks |
| `space-2xl` | 48px | Page section spacing (mobile) |
| `space-3xl` | 64px | Large section dividers |
| `space-4xl` | 80px | Page section spacing (desktop) |

### Section Padding

```css
/* Desktop */
.section {
  padding-top: 80px;
  padding-bottom: 80px;
}

/* Mobile */
@media (max-width: 767px) {
  .section {
    padding-top: 48px;
    padding-bottom: 48px;
  }
}
```

---

## 🎨 COLOR SYSTEM

### Primary Colors

**Deep Caribbean Blue (#003049)**
- **Use:** Headers, primary backgrounds, navigation
- **RGB:** 0, 48, 73
- **HSL:** 198°, 100%, 14%
- **Accessible on:** White text (AAA)

**Caribbean Blue Gradient**
- **Use:** Hero headers, dashboard headers, featured sections
- **Gradient:** Linear, top to bottom
- **Start:** `#003049` (Deep Caribbean Blue)
- **End:** `#005A7D` (Medium Caribbean Blue)
- **CSS:** `background: linear-gradient(180deg, #003049 0%, #005A7D 100%);`
- **Alternative (radial):** `background: radial-gradient(circle at top left, #003049 0%, #005A7D 100%);`
- **Accessible on:** White text (AAA)

**Market Green (#00A896)**
- **Use:** Positive price movement, success states, buy indicators
- **RGB:** 0, 168, 150
- **HSL:** 174°, 100%, 33%
- **Accessible on:** White text (AA), Dark backgrounds (AAA)

**Coral Red (#FF6B6B)**
- **Use:** Negative price movement, alerts, sell indicators
- **RGB:** 255, 107, 107
- **HSL:** 0°, 100%, 71%
- **Accessible on:** White text (AA), Dark text (AA)

**Neon Teal (#00D9C0)**
- **Use:** DominionYouth theme headers, youth badges, gamification elements
- **RGB:** 0, 217, 192
- **HSL:** 173°, 100%, 43%
- **Accessible on:** White text (AAA), Dark backgrounds (AAA)
- **Note:** Youth-focused variant of Market Green - more vibrant, energetic

**Sovereign Gold (#F2C94C)**
- **Use:** Premium highlights, featured content, important badges
- **RGB:** 242, 201, 76
- **HSL:** 45°, 86%, 62%
- **Accessible on:** Dark text only (AAA)

**Coral Accent (#FF9580)**
- **Use:** DominionYouth theme accents, call-to-action buttons, achievement highlights
- **RGB:** 255, 149, 128
- **HSL:** 8°, 100%, 75%
- **Accessible on:** White text (AA), Dark text (AAA)
- **Note:** Softer than Coral Red - playful, approachable for youth audience

### Neutral Colors

**Slate Gray (#4F4F4F)**
- **Use:** Body text, secondary headings
- **RGB:** 79, 79, 79
- **Accessible on:** White backgrounds (AAA)

**Light Gray (#F5F5F5)**
- **Use:** Alternate backgrounds, subtle dividers
- **RGB:** 245, 245, 245

**Warm Sand (#F5F0E8)**
- **Use:** Primary page backgrounds, diaspora-themed sections, warm neutral surfaces
- **RGB:** 245, 240, 232
- **HSL:** 37°, 38%, 93%
- **Accessible on:** Dark text (AAA)
- **Note:** Replaces Light Gray (#F5F5F5) for main backgrounds to create warmer, more inviting feel

**White (#FFFFFF)**
- **Use:** Card backgrounds, panels, clean surfaces
- **RGB:** 255, 255, 255

**Black (#0F172A)** (inherited from CodexDominion)
- **Use:** High contrast text, overlays
- **RGB:** 15, 23, 42

### Semantic Colors

**Success:** `#00A896` (Market Green)
**Warning:** `#F2C94C` (Gold)
**Error:** `#FF6B6B` (Coral Red)
**Info:** `#003049` (Caribbean Blue)

### Color Usage Guidelines

**✅ Do:**
- Use Market Green for positive % changes (`+2.5%`)
- Use Coral Red for negative % changes (`-1.8%`)
- Use Caribbean Blue for neutral data (volume, market cap)
- Use Caribbean Blue Gradient for hero sections and dashboard headers
- Use Warm Sand (#F5F0E8) for main page backgrounds
- Use White (#FFFFFF) for card surfaces on Warm Sand backgrounds
- Use high contrast for text (Slate Gray on White/Sand, White on Caribbean Blue)

**❌ Don't:**
- Mix red and green in same visual element (accessibility)
- Use color alone to convey meaning (add icons/text)
- Use Gold for financial data (reserved for highlights)
- Use gradients on small UI elements (buttons, badges) - solid colors only
- Mix Warm Sand with Light Gray in same view (choose one per page)

---

## 🎨 THEME VARIANTS

### DominionYouth Theme

**Purpose:** Youthful, gamified interface for financial education platform

**Color Overrides:**
- **Primary Header:** Neon Teal (#00D9C0) - solid or subtle gradient
- **Accent/CTA:** Coral Accent (#FF9580)
- **Background:** White (#FFFFFF) or Light Gray (#F5F5F5) - brighter than Warm Sand
- **Success/Badges:** Neon Teal (#00D9C0)
- **Highlights:** Coral Accent (#FF9580)

**Typography:**
- Use same Inter + Roboto Mono stack
- Slightly larger base size for readability (16px → 17px)
- More rounded button corners (8px → 12px)

**Widget-Specific Colors:**
- Learning Badges: Neon Teal background, White icons
- Mock Portfolio: Coral Accent for gains, standard Coral Red for losses
- Challenge Cards: Neon Teal border, Coral Accent highlights
- XP Progress Bars: Neon Teal fill, Light Gray background

---

## 🧩 COMPONENT LIBRARY

### 1. Market Ticker Bar

**Purpose:** Real-time horizontal scrolling ticker showing market movers

**Anatomy:**
```
┌───────────────────────────────────────────────────────────┐
│ ⬆ AAPL $175.23 +2.4% | ⬇ TSLA $243.15 -1.2% | ⬆ NVDA ... │
└───────────────────────────────────────────────────────────┘
```

**Specs:**
- Height: 48px
- Background: `#003049` (Caribbean Blue)
- Text color: `#FFFFFF`
- Positive movement: `#00A896` with ⬆ icon
- Negative movement: `#FF6B6B` with ⬇ icon
- Animation: Smooth horizontal scroll (30 seconds per loop)
- Hover: Pause scrolling

**Figma Component:**
```typescript
// Props
interface MarketTickerItem {
  symbol: string;          // 'AAPL'
  price: number;           // 175.23
  percentChange: number;   // 2.4 or -1.2
}

// States
- Default (scrolling)
- Hover (paused)
- Mobile (slower scroll, 45 seconds)
```

**Micro-animations:**
- Price updates: Fade transition (200ms)
- New data: Pulse effect on symbol (300ms)
- Direction change: Rotate icon (150ms)

---

### 2. Stock Card

**Purpose:** Quick view of single stock performance

**Anatomy:**
```
┌─────────────────────────────┐
│ AAPL          ⬆ +2.4%      │
│ Apple Inc.                  │
│                             │
│ $175.23                     │
│ ▁▂▃▅▇ (mini sparkline)      │
│                             │
│ Vol: 45.2M | Cap: $2.8T    │
└─────────────────────────────┘
```

**Specs:**
- Size: 280px × 200px (desktop), Full width (mobile)
- Border radius: 12px
- Background: `#FFFFFF`
- Border: 1px solid `#E5E5E5`
- Padding: 20px
- Shadow: `0 2px 8px rgba(0, 0, 0, 0.08)`
- Hover: Shadow `0 4px 12px rgba(0, 0, 0, 0.12)`, translate -2px

**Typography:**
- Symbol: 24px bold, `#0F172A`
- Company name: 14px regular, `#4F4F4F`
- Price: 32px bold, `#0F172A`
- % change: 18px medium, `#00A896` or `#FF6B6B`
- Metadata: 12px regular, `#4F4F4F`

**Sparkline:**
- Height: 40px
- Width: 100% (minus padding)
- Stroke: 2px, color matches % change
- Fill: Gradient to transparent
- Time range: Last 24 hours

**States:**
- Default
- Hover (elevated shadow)
- Loading (skeleton)
- Error (fallback message)

---

### 3. Portfolio Card

**Purpose:** Overview of user's portfolio performance

**Anatomy:**
```
┌────────────────────────────────────┐
│ My Portfolio                       │
│                                    │
│ $125,450.32                        │
│ ⬆ +$2,340.21 (+1.9%) Today        │
│                                    │
│ [Pie Chart: Allocation]           │
│ • Tech (45%) • Finance (30%)      │
│ • Healthcare (15%) • Energy (10%) │
│                                    │
│ 12 Holdings | Last updated 2m ago │
└────────────────────────────────────┘
```

**Specs:**
- Size: 400px × 480px (desktop), Full width (mobile)
- Border radius: 12px
- Background: `#FFFFFF`
- Padding: 24px
- Shadow: `0 4px 16px rgba(0, 0, 0, 0.1)`

**Typography:**
- Title: 18px bold, `#0F172A`
- Total value: 36px bold, `#0F172A`
- Daily change: 20px medium, `#00A896` or `#FF6B6B`
- Metadata: 12px regular, `#4F4F4F`

**Pie Chart:**
- Size: 200px diameter
- Sectors: Use color palette (avoid red/green)
  - Tech: `#003049` (Caribbean Blue)
  - Finance: `#00A896` (Market Green)
  - Healthcare: `#F2C94C` (Gold)
  - Energy: `#4F4F4F` (Slate Gray)
- Hover: Highlight sector, show value
- Interactive: Click to filter holdings

**Legend:**
- Position: Below chart
- Format: `• Tech (45%)`
- Dot color: Matches chart sector

**States:**
- Default
- Empty (onboarding state)
- Loading (skeleton with shimmer)
- Error (fallback with retry button)

---

### 4. Watchlist Table

**Purpose:** Sortable table of user's tracked stocks

**Anatomy:**
```
┌──────────────────────────────────────────────────────────┐
│ Symbol | Price    | Change   | Volume  | Mkt Cap | 🔔   │
├──────────────────────────────────────────────────────────┤
│ AAPL   | $175.23  | ⬆ +2.4%  | 45.2M   | $2.8T   | 🔔   │
│ MSFT   | $370.15  | ⬇ -0.8%  | 23.1M   | $2.7T   | —    │
│ GOOGL  | $140.50  | ⬆ +1.2%  | 18.4M   | $1.8T   | 🔔   │
└──────────────────────────────────────────────────────────┘
```

**Specs:**
- Width: 100% (responsive)
- Row height: 56px
- Header background: `#F5F5F5`
- Row background: `#FFFFFF`
- Row hover: `#FAFAFA`
- Border: 1px solid `#E5E5E5`

**Typography:**
- Header: 14px bold, `#4F4F4F`, uppercase
- Symbol: 16px bold, `#0F172A`
- Price: 16px medium, `#0F172A`
- Change: 16px medium, `#00A896` or `#FF6B6B`
- Volume/Cap: 14px regular, `#4F4F4F`

**Sorting:**
- Default: Alphabetical by symbol
- Click header to sort (ascending/descending)
- Indicator: ▲ or ▼ icon next to header

**Alerts Icon (🔔):**
- Active: `#F2C94C` (Gold) with pulse animation
- Inactive: `#E5E5E5` (Light Gray)
- Hover: Tooltip "Price alert set at $180"

**Actions:**
- Click row: Open stock detail modal
- Click alert icon: Open alert settings
- Right-click: Context menu (remove from watchlist, add alert)

**Responsive (Mobile):**
- Hide Volume and Market Cap columns
- Stack symbol + price on one line, change below
- Swipe left on row: Reveal delete button

**States:**
- Default
- Sorting (loading indicator)
- Empty (onboarding prompt)
- Loading (skeleton rows)

---

### 5. News Panel

**Purpose:** Display verified financial news headlines

**Anatomy:**
```
┌─────────────────────────────────────────────────┐
│ 📰 Market News                                  │
├─────────────────────────────────────────────────┤
│ ✅ Verified by 3 sources                        │
│ Apple announces new product line                │
│ Bloomberg, Reuters, CNBC • 2 hours ago          │
├─────────────────────────────────────────────────┤
│ ⚠️ Developing story                             │
│ Fed signals potential rate change               │
│ Reuters, WSJ • 15 minutes ago                   │
├─────────────────────────────────────────────────┤
│ ⚠️ Unverified                                   │
│ Tech sector sees unexpected volatility          │
│ Yahoo Finance • Just now                        │
└─────────────────────────────────────────────────┘
```

**Specs:**
- Width: 100% (or 400px sidebar)
- Item height: Auto (min 100px)
- Background: `#FFFFFF`
- Border radius: 8px
- Padding: 16px per item
- Separator: 1px solid `#E5E5E5`

**Typography:**
- Section title: 18px bold, `#0F172A`
- Headline: 16px medium, `#0F172A`, line-clamp: 2
- Source/time: 12px regular, `#4F4F4F`

**Verification Badges:**
- ✅ Confirmed: `#00A896` background, white text
- ⚠️ Developing: `#F2C94C` background, dark text
- ⚠️ Unverified: `#FF6B6B` background, white text
- Badge size: 20px × 20px icon + text
- Position: Top-left of each news item

**Interaction:**
- Click item: Open news detail modal (multi-source view)
- Hover: Subtle background `#FAFAFA`
- Time format: "Just now" | "5m ago" | "2 hours ago" | "Dec 24"

**States:**
- Default (with news)
- Loading (skeleton items)
- Empty ("No news for this stock")
- Error (retry button)

**Responsive (Mobile):**
- Full width
- Smaller padding (12px)
- Truncate sources to first 2 ("Bloomberg, Reuters +1")

---

### 6. Alerts Drawer

**Purpose:** Manage custom price, volume, and news alerts

**Anatomy:**
```
┌──────────────────────────────────────────┐
│ 🔔 Your Alerts              [+ Add New] │
├──────────────────────────────────────────┤
│ Price Alerts                             │
│ ├─ AAPL above $180 🔔                   │
│ │  Current: $175.23 | Set 2 days ago    │
│ │  [Edit] [Delete]                       │
│ └─ TSLA below $200 🔕                   │
│    Current: $243.15 | Set 5 days ago    │
│    [Edit] [Delete]                       │
├──────────────────────────────────────────┤
│ Volume Alerts                            │
│ ├─ NVDA volume > 50M 🔔                 │
│    Current: 32M | Set today              │
│    [Edit] [Delete]                       │
├──────────────────────────────────────────┤
│ News Alerts                              │
│ ├─ AAPL earnings report 🔔              │
│    Notify on verified news only          │
│    [Edit] [Delete]                       │
└──────────────────────────────────────────┘
```

**Specs:**
- Width: 400px (drawer on right side)
- Background: `#FFFFFF`
- Shadow: `-4px 0 16px rgba(0, 0, 0, 0.1)`
- Padding: 24px
- Animation: Slide in from right (300ms ease-out)

**Typography:**
- Title: 20px bold, `#0F172A`
- Section header: 16px bold, `#4F4F4F`
- Alert text: 14px medium, `#0F172A`
- Metadata: 12px regular, `#4F4F4F`

**Icons:**
- 🔔 Active alert: `#F2C94C` (Gold) with pulse
- 🔕 Inactive alert: `#E5E5E5` (Light Gray)
- + Add New: `#003049` (Caribbean Blue)

**Alert States:**
- Active (condition met): Gold icon, bold text
- Pending (condition not met): Gray icon, normal text
- Triggered (notification sent): Badge "Triggered 5m ago"

**Actions:**
- Click "Add New": Open alert creation modal
- Click "Edit": Inline editing
- Click "Delete": Confirm dialog
- Toggle alert on/off: Click icon

**Alert Types:**

**1. Price Alert:**
- Condition: Above/Below/Equals price
- Example: "AAPL above $180"

**2. Volume Alert:**
- Condition: Volume exceeds threshold
- Example: "NVDA volume > 50M"

**3. News Alert:**
- Trigger: Verified news published about stock
- Filter: Verified only / All news

**4. Earnings Alert:**
- Trigger: Earnings report scheduled
- Reminder: 24 hours before

**Responsive (Mobile):**
- Full screen overlay (not drawer)
- Bottom sheet style
- Swipe down to close

---

### 7. Fact-Check Badge

**Purpose:** Visual indicator of news verification status

**Variants:**

**✅ Multi-Source Verified**
```
┌────────────────────────────┐
│ ✅ Verified by 3 sources   │
└────────────────────────────┘
```
- Background: `#00A896` (Market Green)
- Text: `#FFFFFF`
- Border radius: 4px
- Padding: 4px 8px
- Font: 12px bold

**⚠️ Developing Story**
```
┌────────────────────────────┐
│ ⚠️ Developing Story        │
└────────────────────────────┘
```
- Background: `#F2C94C` (Gold)
- Text: `#0F172A`
- Border radius: 4px
- Padding: 4px 8px
- Font: 12px bold

**⚠️ Conflicting Reports**
```
┌────────────────────────────┐
│ ⚠️ Conflicting Reports     │
└────────────────────────────┘
```
- Background: `#FF6B6B` (Coral Red)
- Text: `#FFFFFF`
- Border radius: 4px
- Padding: 4px 8px
- Font: 12px bold

**ℹ️ Single Source**
```
┌────────────────────────────┐
│ ℹ️ Single Source           │
└────────────────────────────┘
```
- Background: `#E5E5E5` (Light Gray)
- Text: `#4F4F4F`
- Border radius: 4px
- Padding: 4px 8px
- Font: 12px bold

**Usage:**
- Position: Top-left of news item
- Tooltip on hover: Shows source list
- Click: Opens fact-check detail modal

**States:**
- Default
- Hover (tooltip visible)
- Active (modal open)

---

## 📱 RESPONSIVE BREAKPOINTS

```css
/* Mobile (Default) */
@media (max-width: 767px) {
  /* 4-column grid, full-width components */
}

/* Tablet */
@media (min-width: 768px) and (max-width: 1199px) {
  /* 8-column grid, hybrid layouts */
}

/* Desktop */
@media (min-width: 1200px) {
  /* 12-column grid, multi-column layouts */
}

/* Large Desktop */
@media (min-width: 1600px) {
  /* Max width constraint, centered content */
}
```

---

## ✍️ TYPOGRAPHY SYSTEM

### Font Families

**Primary (Body & UI):**
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

**Monospace (Numbers & Data):**
```css
font-family: 'Roboto Mono', 'Courier New', monospace;
```

### Type Scale

| Token | Size | Weight | Line Height | Use Case |
|-------|------|--------|-------------|----------|
| `text-xs` | 12px | 400 | 1.4 | Metadata, timestamps |
| `text-sm` | 14px | 400 | 1.5 | Body text, labels |
| `text-base` | 16px | 400 | 1.6 | Standard body text |
| `text-lg` | 18px | 500 | 1.5 | Subheadings, emphasis |
| `text-xl` | 20px | 600 | 1.4 | Section titles |
| `text-2xl` | 24px | 700 | 1.3 | Page titles |
| `text-3xl` | 32px | 700 | 1.2 | Hero headings |
| `text-4xl` | 36px | 700 | 1.2 | Stock prices |

### Font Weights

- **Regular (400):** Body text, descriptions
- **Medium (500):** Emphasis, buttons
- **Semibold (600):** Subheadings, labels
- **Bold (700):** Headings, prices, symbols

---

## 🎭 MICRO-INTERACTIONS

### Price Updates
```
Animation: Fade transition
Duration: 200ms
Easing: ease-in-out
Trigger: Data refresh
```

### Card Hover
```
Animation: Translate Y -2px, shadow elevation
Duration: 150ms
Easing: ease-out
Trigger: Mouse enter
```

### Button Press
```
Animation: Scale 0.98
Duration: 100ms
Easing: ease-in-out
Trigger: Mouse down
```

### Loading Skeleton
```
Animation: Shimmer gradient
Duration: 1.5s infinite
Easing: linear
Colors: #F5F5F5 → #E5E5E5 → #F5F5F5
```

### Alert Pulse
```
Animation: Scale 1.0 → 1.1 → 1.0
Duration: 2s infinite
Easing: ease-in-out
Trigger: Active alert
```

### Notification Toast
```
Animation: Slide in from top
Duration: 300ms
Easing: ease-out
Auto-dismiss: 5 seconds
```

---

## ♿ ACCESSIBILITY

### Color Contrast

**WCAG 2.1 AA Compliance:**
- Body text (`#4F4F4F`) on white: 8.9:1 (AAA)
- Caribbean Blue (`#003049`) with white text: 10.4:1 (AAA)
- Market Green (`#00A896`) with white text: 2.8:1 (AA Large)
- Coral Red (`#FF6B6B`) with white text: 3.5:1 (AA)

**Never rely on color alone:**
- Use icons (⬆ ⬇) with color for price movement
- Add text labels to charts
- Include tooltips with descriptive text

### Keyboard Navigation

**Tab Order:**
1. Header navigation
2. Main content (cards, tables)
3. Sidebar (news, alerts)
4. Footer

**Shortcuts:**
- `Tab` / `Shift+Tab`: Navigate elements
- `Enter` / `Space`: Activate buttons
- `Esc`: Close modals/drawers
- `/`: Focus search bar

### Screen Readers

**ARIA Labels:**
```html
<div class="stock-card" aria-label="Apple Inc. stock card">
  <span aria-label="Symbol">AAPL</span>
  <span aria-label="Price">$175.23</span>
  <span aria-label="Percent change, up 2.4%">⬆ +2.4%</span>
</div>
```

**Live Regions:**
```html
<div aria-live="polite" aria-atomic="true">
  Stock price updated: AAPL now $175.25
</div>
```

---

## 📦 FIGMA DELIVERABLES

### Components to Build

1. **Market Ticker Bar** (with variants: Default, Mobile)
2. **Stock Card** (with states: Default, Hover, Loading, Error)
3. **Portfolio Card** (with states: Default, Empty, Loading)
4. **Watchlist Table** (with sorting, hover, mobile)
5. **News Panel** (with verification badges)
6. **Alerts Drawer** (with alert types)
7. **Fact-Check Badge** (4 variants)
8. **Buttons** (Primary, Secondary, Ghost, Icon)
9. **Inputs** (Text, Number, Dropdown)
10. **Modals** (Small, Medium, Large, Full-screen)

### Pages to Build

1. **Homepage** (Hero + Features)
2. **Dashboard** (Watchlist + Portfolio + News)
3. **Stock Detail** (Chart + News + Alerts)
4. **Portfolio Page** (Holdings + Performance)
5. **News Feed** (Multi-source verification)
6. **Onboarding Flow** (5 screens)

### Design Tokens Export

**JSON Format:**
```json
{
  "colors": {
    "primary": "#003049",
    "success": "#00A896",
    "error": "#FF6B6B",
    "warning": "#F2C94C"
  },
  "spacing": {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px"
  },
  "typography": {
    "fontSize": {
      "xs": "12px",
      "sm": "14px",
      "base": "16px"
    }
  }
}
```

---

## 🚀 IMPLEMENTATION NOTES

### Tech Stack Recommendation

**Frontend:**
- Next.js 14+ (App Router)
- Tailwind CSS (with custom config)
- shadcn/ui components (customized)
- Recharts or TradingView widgets (charts)

**Design System:**
- Tailwind config with DominionMarkets tokens
- Custom CSS variables for theme switching
- Component library in `components/ui/`

**Example Tailwind Config:**
```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        'dominion-blue': '#003049',
        'market-green': '#00A896',
        'coral-red': '#FF6B6B',
        'gold': '#F2C94C',
        'slate': '#4F4F4F',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['Roboto Mono', 'monospace'],
      },
    },
  },
};
```

### Component Structure (React)

```tsx
// Example: Stock Card
interface StockCardProps {
  symbol: string;
  companyName: string;
  price: number;
  percentChange: number;
  volume: string;
  marketCap: string;
  sparklineData: number[];
}

export const StockCard: React.FC<StockCardProps> = ({
  symbol,
  companyName,
  price,
  percentChange,
  volume,
  marketCap,
  sparklineData,
}) => {
  const isPositive = percentChange >= 0;
  
  return (
    <div className="stock-card">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-2xl font-bold">{symbol}</h3>
          <p className="text-sm text-slate">{companyName}</p>
        </div>
        <span className={`text-lg font-medium ${isPositive ? 'text-market-green' : 'text-coral-red'}`}>
          {isPositive ? '⬆' : '⬇'} {Math.abs(percentChange)}%
        </span>
      </div>
      
      <p className="text-4xl font-bold font-mono mt-4">
        ${price.toFixed(2)}
      </p>
      
      <Sparkline data={sparklineData} color={isPositive ? '#00A896' : '#FF6B6B'} />
      
      <div className="flex justify-between text-xs text-slate mt-4">
        <span>Vol: {volume}</span>
        <span>Cap: {marketCap}</span>
      </div>
    </div>
  );
};
```

---

## 📊 DESIGN SYSTEM CHECKLIST

- [x] Grid system defined (12/8/4 columns)
- [x] Spacing scale established (8px base)
- [x] Color palette documented
- [x] 7 core components specified
- [x] Typography system defined
- [x] Responsive breakpoints set
- [x] Accessibility guidelines included
- [x] Micro-interactions documented
- [x] Figma deliverables listed
- [x] Implementation notes provided

---

**Status:** READY FOR DESIGN ✅  
**Next Steps:** Build Figma library, export design tokens, begin component development  
**Launch Target:** Q1 2025
