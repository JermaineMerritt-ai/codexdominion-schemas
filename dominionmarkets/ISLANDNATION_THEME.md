# IslandNation Theme Specification

## 🎯 Overview

**Purpose:** Professional creator marketplace interface for digital products, courses, and creator-economy analytics

**Design Philosophy:**
- **Professional:** Sophisticated, trusted platform for serious creators
- **Aspirational:** Gold accents convey premium value and creator success
- **Data-Driven:** Creator-economy metrics displayed prominently
- **Community:** Collaborative environment for Caribbean diaspora creators

**Target Audience:**
- Content creators (courses, templates, graphics, music)
- Digital entrepreneurs
- Influencers and personal brands
- Caribbean diaspora creatives

---

## 🎨 COLOR SYSTEM

### Primary Colors

**Deep Slate (#1E293B)**
- **Use:** Headers, navigation, primary backgrounds, professional sections
- **RGB:** 30, 41, 59
- **HSL:** 217°, 33%, 17%
- **Accessible on:** White text (AAA), Gold text (AAA)
- **Gradient variant:** `linear-gradient(135deg, #1E293B 0%, #0F172A 100%)`

**Slate Gradient (Professional Headers)**
- **Use:** Hero sections, dashboard headers, featured creator sections
- **Gradient:** Linear, left to right
- **Start:** `#1E293B` (Deep Slate)
- **End:** `#334155` (Medium Slate)
- **CSS:** `background: linear-gradient(90deg, #1E293B 0%, #334155 100%);`

**Sovereign Gold (#F2C94C)**
- **Use:** Premium highlights, creator badges, revenue indicators, featured content
- **RGB:** 242, 201, 76
- **HSL:** 45°, 86%, 62%
- **Accessible on:** Dark text (AAA), Deep Slate backgrounds (AAA)
- **Gradient variant:** `linear-gradient(135deg, #F2C94C 0%, #E5B840 100%)`

**Creator Green (#00A896)** (Secondary)
- **Use:** Sales indicators, revenue growth, positive metrics
- **RGB:** 0, 168, 150
- **HSL:** 174°, 100%, 33%
- **Accessible on:** White text (AA), Dark backgrounds (AAA)

**Caribbean Blue (#003049)** (Tertiary)
- **Use:** Links, informational elements, diaspora-themed sections
- **RGB:** 0, 48, 73
- **HSL:** 198°, 100%, 14%
- **Accessible on:** White text (AAA)

### Semantic Colors

**Success:** `#00A896` (Creator Green)
**Warning:** `#F2C94C` (Gold)
**Error:** `#FF6B6B` (Coral Red)
**Info:** `#5B8DEF` (Sky Blue)
**Revenue:** `#00A896` (Creator Green with gold accents)

### Backgrounds

**Primary Background:** `#F8FAFC` (Very Light Slate)
**Secondary Background:** `#FFFFFF` (White)
**Card Background:** `#FFFFFF` with subtle shadow
**Dark Mode Background:** `#0F172A` (Midnight)
**Overlay Background:** `rgba(30, 41, 59, 0.95)` (Deep Slate with transparency)

### Neutrals

**Dark Text:** `#0F172A` (Midnight)
**Medium Text:** `#475569` (Slate)
**Light Text:** `#94A3B8` (Light Slate)
**Divider:** `#E2E8F0` (Very Light Gray)
**Border:** `#CBD5E1` (Light Slate Border)

---

## ✍️ TYPOGRAPHY

**Primary Font:** Inter (same as DominionMarkets)
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

**Display Font:** Playfair Display (for creator names, featured content)
```css
font-family: 'Playfair Display', Georgia, serif;
```

**Monospace Font:** Roboto Mono (revenue numbers, analytics)
```css
font-family: 'Roboto Mono', 'Courier New', monospace;
```

### Type Scale (Creator Marketplace Variant)

| Token | Size | Weight | Line Height | Use Case |
|-------|------|--------|-------------|----------|
| `text-xs` | 12px | 400 | 1.4 | Metadata, timestamps |
| `text-sm` | 14px | 400 | 1.5 | Body text, descriptions |
| `text-base` | 16px | 400 | 1.6 | Standard body text |
| `text-lg` | 18px | 500 | 1.5 | Product titles, creator names |
| `text-xl` | 20px | 600 | 1.4 | Section titles |
| `text-2xl` | 24px | 700 | 1.3 | Page titles |
| `text-3xl` | 32px | 700 | 1.2 | Hero headings |
| `text-4xl` | 40px | 700 | 1.1 | Revenue numbers, featured metrics |
| `text-display` | 48px | 700 | 1.0 | Landing page hero (Playfair Display) |

**Note:** Creator names use Playfair Display for aspirational, premium feel

---

## 🧩 COMPONENT LIBRARY

### 1. Creator-Economy Index Widget

**Purpose:** Track performance of creator-economy sector stocks and trends

**Visual Design:**
```
┌─────────────────────────────────────────────────────────┐
│ 📈 CREATOR-ECONOMY INDEX                  +5.2% Today   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Index Value: 1,485.32  ↑                               │
│  24h Change: +72.85 (+5.16%)                            │
│                                                         │
│  [7D Chart: Line graph showing upward trend]            │
│                                                         │
│  TOP MOVERS:                                            │
│  ┌────────────────────────────────────────────────┐    │
│  │ SHOP (Shopify)        $98.45   +8.2%  🔥       │    │
│  │ ETSY (Etsy)           $76.23   +6.1%           │    │
│  │ META (Meta Platforms) $385.67  +4.8%           │    │
│  │ SPOT (Spotify)        $245.89  +3.5%           │    │
│  │ ABNB (Airbnb)         $142.33  +2.9%           │    │
│  └────────────────────────────────────────────────┘    │
│                                                         │
│  Index Composition: E-commerce (40%), Social (30%),    │
│  Streaming (20%), Marketplaces (10%)                   │
│                                                         │
│  [View Full Index] [Track in Portfolio]                │
└─────────────────────────────────────────────────────────┘
```

**Specs:**
- **Width:** 100% (responsive)
- **Height:** Auto (min 400px)
- **Background:** White (#FFFFFF)
- **Border:** 1px solid #E2E8F0
- **Border radius:** 12px
- **Padding:** 24px
- **Header background:** Deep Slate gradient
- **Index value color:** Sovereign Gold (#F2C94C)
- **Positive movement:** Creator Green (#00A896)
- **Chart:** 7-day line chart with gradient fill

**Figma Component:**
```typescript
interface CreatorEconomyIndex {
  indexValue: number;              // 1485.32
  change24h: {
    absolute: number;              // +72.85
    percent: number;               // +5.16
  };
  chartData: {
    timestamp: string;             // ISO 8601
    value: number;                 // Index value at timestamp
  }[];
  topMovers: CreatorStock[];
  composition: {
    category: string;              // 'E-commerce', 'Social', etc.
    percentage: number;            // 40
  }[];
  lastUpdated: string;             // '2025-12-24T10:30:00Z'
}

interface CreatorStock {
  symbol: string;                  // 'SHOP'
  name: string;                    // 'Shopify'
  price: number;                   // 98.45
  change: number;                  // +8.2
  featured: boolean;               // true if 🔥 icon
}
```

**Interactions:**
- **Hover on stock:** Show tooltip with full company name, market cap, volume
- **Click stock:** Navigate to stock detail page in DominionMarkets
- **"View Full Index" button:** Opens full creator-economy dashboard
- **"Track in Portfolio" button:** Adds all index stocks to watchlist
- **Chart hover:** Show exact value at timestamp

**Educational Context:**
- **Info icon:** Explains what creator-economy index tracks
- **Composition breakdown:** Pie chart showing sector allocation
- **Why it matters:** "Track companies powering the creator economy"

---

### 2. Digital-Product Stocks Widget

**Purpose:** Highlight publicly-traded companies in digital products, SaaS, and creator tools

**Visual Design:**
```
┌─────────────────────────────────────────────────────────┐
│ 💼 DIGITAL-PRODUCT STOCKS                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  CATEGORY: Creator Tools ▼                              │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ SHOP  Shopify                                    │  │
│  │ $98.45  +8.2%  🔥 HOT                           │  │
│  │ ━━━━━━━━━━━━━━━━━━━ [7D Sparkline]             │  │
│  │ Market Cap: $125B | E-commerce platform         │  │
│  │ [Add to Watchlist] [View Details]               │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ ADBE  Adobe                                      │  │
│  │ $587.32  +2.1%                                  │  │
│  │ ━━━━━━━━━━━━━━━━━━━ [7D Sparkline]             │  │
│  │ Market Cap: $267B | Creative software           │  │
│  │ [Add to Watchlist] [View Details]               │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ CRM  Salesforce                                  │  │
│  │ $245.67  +1.8%                                  │  │
│  │ ━━━━━━━━━━━━━━━━━━━ [7D Sparkline]             │  │
│  │ Market Cap: $238B | CRM + commerce              │  │
│  │ [Add to Watchlist] [View Details]               │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  [Load More] [Filter by Sector]                        │
└─────────────────────────────────────────────────────────┘
```

**Specs:**
- **Width:** 100% (responsive)
- **Height:** Auto (infinite scroll)
- **Card per stock:** 140px height
- **Background:** White (#FFFFFF)
- **Border:** 1px solid #E2E8F0
- **Border radius:** 12px
- **Padding:** 20px per card
- **Positive movement:** Creator Green (#00A896)
- **Featured (🔥 HOT):** Gold accent, pulse animation
- **Sparkline:** 7-day mini chart (60px × 24px)

**Figma Component:**
```typescript
interface DigitalProductStock {
  symbol: string;                  // 'SHOP'
  name: string;                    // 'Shopify'
  price: number;                   // 98.45
  change: number;                  // +8.2
  marketCap: string;               // '$125B'
  description: string;             // 'E-commerce platform'
  category: DigitalProductCategory;
  sparkline: number[];             // 7-day price history
  featured: boolean;               // true if 🔥 HOT
  relevanceScore?: number;         // Algorithm-based (1-100)
}

enum DigitalProductCategory {
  CreatorTools = 'Creator Tools',    // Shopify, Adobe, Canva
  SaaS = 'SaaS',                     // Salesforce, HubSpot
  ECommerce = 'E-Commerce',          // Shopify, Etsy, ABNB
  Streaming = 'Streaming',           // Spotify, Netflix
  Social = 'Social Media',           // META, SNAP, PINS
  Marketplaces = 'Marketplaces',     // Upwork, Fiverr
  PaymentProcessors = 'Payments',    // SQ, PYPL, ADYEN
}
```

**Interactions:**
- **Category dropdown:** Filter stocks by category (Creator Tools, SaaS, E-commerce, etc.)
- **"Add to Watchlist" button:** Adds stock to DominionMarkets watchlist
- **"View Details" button:** Opens stock detail page (news, analytics, charts)
- **Click stock card:** Navigate to full stock page
- **Hover sparkline:** Show 7-day price range tooltip
- **"Load More" button:** Infinite scroll to load more stocks

**Relevance Algorithm:**
```typescript
// Stocks ranked by relevance to creators
function calculateRelevanceScore(stock: DigitalProductStock): number {
  let score = 0;
  
  // Category weighting
  if (stock.category === 'Creator Tools') score += 40;
  if (stock.category === 'E-Commerce') score += 30;
  if (stock.category === 'Streaming') score += 20;
  
  // Performance weighting
  if (stock.change > 5) score += 20;  // Strong growth
  if (stock.change > 10) score += 10; // Exceptional growth
  
  // Market cap (stability)
  if (parseMarketCap(stock.marketCap) > 100_000_000_000) score += 10;
  
  return Math.min(score, 100);
}
```

**Featured (🔥 HOT) Criteria:**
- Stock up ≥5% in 24 hours
- High trading volume (≥2x average)
- Recent creator-relevant news (earnings, product launch, acquisition)
- Manually curated by editorial team

---

### 3. Creator Revenue Dashboard

**Purpose:** Track IslandNation creator earnings and marketplace metrics

**Visual Design:**
```
┌─────────────────────────────────────────────────────────┐
│ 💰 MY CREATOR REVENUE                    This Month     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Total Earnings: $2,485.75  (+18.5% vs last month)     │
│  Payouts: $2,100.00  |  Pending: $385.75               │
│                                                         │
│  [30D Chart: Revenue over time]                         │
│                                                         │
│  TOP PRODUCTS:                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │ Advanced Stock Analysis Course                 │    │
│  │ 42 sales | $1,260.00 (51% of revenue)          │    │
│  └────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────┐    │
│  │ Technical Indicators Template Pack             │    │
│  │ 28 sales | $840.00 (34% of revenue)            │    │
│  └────────────────────────────────────────────────┘    │
│                                                         │
│  MARKETPLACE INSIGHTS:                                  │
│  • Your revenue up 18.5% (marketplace avg: +12.3%)     │
│  • Top category: Finance & Investing (62% of sales)    │
│  • Best day: Dec 15 ($385 in sales)                   │
│                                                         │
│  [Request Payout] [View Analytics]                     │
└─────────────────────────────────────────────────────────┘
```

**Specs:**
- **Width:** 100%
- **Padding:** 24px
- **Background:** White with Gold accent border (2px)
- **Revenue numbers:** Roboto Mono, Gold color
- **Chart:** 30-day line chart with area fill
- **Product cards:** White background, subtle shadow

---

### 4. Creator Profile Card

**Purpose:** Showcase creator on IslandNation marketplace

**Visual Design:**
```
┌──────────────────────────────────────────────┐
│  [Avatar: 80px circle]                       │
│                                              │
│  Caribbean Finance Guru                      │
│  @caribbeanfinance                           │
│                                              │
│  ⭐ 4.9 (142 reviews) | 🏆 Top Creator      │
│                                              │
│  Specialty: Stock Analysis, Portfolio Tools  │
│                                              │
│  📦 12 Products | 💰 $85K+ Earned           │
│  👥 2,485 Students                           │
│                                              │
│  [Follow] [View Products]                    │
└──────────────────────────────────────────────┘
```

**Specs:**
- **Width:** 320px (grid layout)
- **Height:** Auto (min 280px)
- **Background:** White
- **Border:** 1px solid #E2E8F0, 2px Gold on hover
- **Border radius:** 12px
- **Top Creator badge:** Gold background, white text
- **Avatar:** 80px × 80px circle, Gold ring if Top Creator

---

### 5. Marketplace Category Card

**Purpose:** Navigate digital product categories

**Visual Design:**
```
┌─────────────────────────────────┐
│  📚 Finance & Investing         │
│                                 │
│  385 products | 142 creators   │
│  Avg price: $29.99              │
│                                 │
│  Top sellers: Courses, Tools    │
│                                 │
│  [Explore Category →]           │
└─────────────────────────────────┘
```

**Specs:**
- **Width:** 280px (4-column grid on desktop)
- **Height:** 220px
- **Background:** White
- **Icon:** 48px × 48px emoji or SVG
- **Border:** 2px solid #E2E8F0
- **Hover:** Gold border, lift 4px

**Categories:**
- 📚 Finance & Investing
- 🎨 Design & Graphics
- 🎵 Music & Audio
- 📹 Video Production
- ✍️ Writing & Content
- 💻 Code & Development
- 📊 Business Tools
- 🌴 Caribbean Culture

---

## 🎭 MICRO-INTERACTIONS

### Creator-Economy Index Update
```
Animation: Number count-up
Duration: 800ms
Trigger: Data refresh
Easing: ease-out
Effect: Index value animates from old → new value
```

### Stock Card Hover
```
Animation: Scale 1.02, Gold border
Duration: 200ms
Easing: ease-out
```

### Revenue Number Update
```
Animation: Flash Gold background
Duration: 500ms
Trigger: New sale detected
Effect: Revenue number flashes Gold, count-up animation
```

### Top Creator Badge Pulse
```
Animation: Scale 1.0 → 1.05 → 1.0
Duration: 2s infinite
Easing: ease-in-out
```

### Product Card Add to Cart
```
Animation: Slide into cart icon
Duration: 400ms
Easing: cubic-bezier
```

### Featured Stock (🔥 HOT) Pulse
```
Animation: Opacity 0.8 → 1.0 → 0.8
Duration: 1.5s infinite
Easing: ease-in-out
Color: Gold (#F2C94C)
```

---

## ♿ ACCESSIBILITY

**WCAG 2.1 AA Compliance:**
- Deep Slate (#1E293B) with white text: 15:1 (AAA)
- Sovereign Gold (#F2C94C) with Deep Slate: 8.2:1 (AAA)
- Creator Green (#00A896) on white: 4.5:1 (AA)

**Creator-Specific Considerations:**
- High contrast mode for dashboard analytics
- Screen reader friendly revenue announcements
- Keyboard navigation for all marketplace interactions
- ARIA labels for stock performance indicators

---

## 📱 RESPONSIVE DESIGN

**Mobile (≤767px):**
- Single column layout
- Creator-Economy Index: Simplified to top 3 stocks
- Digital-Product Stocks: Card layout (not table)
- Revenue dashboard: Stacked metrics

**Tablet (768-1023px):**
- 2-column grid for product cards
- Sidebar navigation collapses
- Full Creator-Economy Index widget

**Desktop (≥1024px):**
- 4-column grid for marketplace categories
- Persistent sidebar with creator profile
- Full analytics dashboards
- Split view: Products + Stock tracker

---

## 🎨 DASHBOARD LAYOUTS

### IslandNation Home Dashboard (Creator View)

**Sections:**
1. **Hero Header** - Deep Slate gradient, "Welcome back, [Creator Name]"
2. **Revenue Overview** - Creator Revenue Dashboard widget (full width)
3. **Creator-Economy Index** - Half width (left column)
4. **Digital-Product Stocks** - Half width (right column)
5. **Recent Sales** - Activity feed showing product purchases
6. **Marketplace Insights** - Analytics cards (views, clicks, conversion rate)
7. **Recommended Actions** - AI-powered suggestions ("Create a new course", "Run a promotion")

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ Deep Slate Header (Gradient)                            │
├─────────────────────────────────────────────────────────┤
│ Revenue Overview (Full Width)                           │
├──────────────────────────────┬──────────────────────────┤
│ Creator-Economy Index        │ Digital-Product Stocks   │
│ (Left 50%)                   │ (Right 50%)              │
├──────────────────────────────┴──────────────────────────┤
│ Recent Sales (Full Width)                               │
├─────────────────────────────────────────────────────────┤
│ Marketplace Insights (3-column grid)                    │
├─────────────────────────────────────────────────────────┤
│ Recommended Actions (2-column)                          │
└─────────────────────────────────────────────────────────┘
```

---

### IslandNation Marketplace (Buyer View)

**Sections:**
1. **Hero Search** - "Find digital products from Caribbean creators"
2. **Category Grid** - 8 category cards
3. **Featured Creators** - Top Creator profile cards
4. **Trending Products** - Horizontal scroll
5. **Creator-Economy Index** - Sidebar widget
6. **Digital-Product Stocks** - Sidebar widget

---

## 🚀 IMPLEMENTATION NOTES

**Tailwind Config Overrides (IslandNation theme):**
```javascript
// tailwind.config.islandnation.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'slate-deep': '#1E293B',
        'slate-medium': '#334155',
        'creator-gold': '#F2C94C',
        'creator-green': '#00A896',
      },
      fontFamily: {
        'display': ['Playfair Display', 'Georgia', 'serif'],
      },
    },
  },
};
```

**Component Naming Convention:**
- Prefix all IslandNation components with `Island-`
- Example: `<IslandCreatorCard />`, `<IslandEconomyIndex />`, `<IslandProductCard />`

**Data Integrations:**
- **Alpha Vantage API:** Real-time stock data for Creator-Economy Index
- **DominionMarkets API:** Cross-platform watchlist sync
- **Stripe API:** Creator payout processing
- **IslandNation Backend:** Product sales, creator metrics

**Revenue Sharing:**
- Creators: 85%
- Platform (IslandNation): 15%
- Payment processing fees: Deducted from platform share
- Minimum payout threshold: $50

**Cross-Platform Integration:**
- Users can track IslandNation creator stocks in DominionMarkets portfolio
- DominionMarkets "Learn" tab features IslandNation courses
- Shared Auth0 SSO across all CodexDominion platforms

---

**Last Updated:** December 24, 2025
**Status:** Specification complete, ready for design + development
**Owner:** IslandNation Product Team
