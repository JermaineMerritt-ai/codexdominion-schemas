# DOMINIONMARKETS — DASHBOARD WIREFRAMES

> **Purpose:** Wireframe logic and layout specifications for all major dashboards  
> **Format:** Designer-ready blueprint (not pixel-perfect mockups)  
> **Philosophy:** Clean, trustworthy, data-first, culturally intelligent

---

## 🎨 CORE UI PRINCIPLES

### 1. Clean
- **White space is intentional:** Don't fill every pixel
- **One primary action per screen:** Clear hierarchy
- **Remove, don't add:** Question every element

### 2. Trustworthy
- **Show sources:** Never hide where data comes from
- **Use disclaimers:** Be upfront about limitations
- **Consistent design:** Predictability builds confidence

### 3. Data-First
- **Numbers lead:** Make data the hero
- **Context second:** Explain after showing
- **Visual hierarchy:** Most important data is largest/boldest

### 4. Culturally Intelligent
- **Caribbean context:** JSE, TTSE, BSE are first-class citizens
- **Diaspora awareness:** Support multiple currencies and time zones
- **Language choice:** Caribbean English, not Wall Street jargon

### 5. Zero Clutter
- **One task per view:** Don't mix unrelated features
- **Progressive disclosure:** Start simple, reveal complexity on demand
- **Smart defaults:** Pre-populate with sensible choices

### 6. High Contrast
- **WCAG AAA compliant:** 7:1 contrast ratio minimum
- **Clear color coding:** Green = up, Red = down, Blue = neutral
- **Bold typography:** 16px minimum body text

### 7. Accessible
- **Keyboard navigation:** Every action has a shortcut
- **Screen reader friendly:** ARIA labels on all interactive elements
- **Color is not sole indicator:** Use icons + text + color

---

## 📱 PRIMARY SCREENS INVENTORY

### Dashboard Screens (8 Total)

1. **Home Dashboard** - Overview of everything (portfolio + market + news)
2. **Market Overview Dashboard** - Broad market view (sectors, movers, sentiment)
3. **Watchlist Dashboard** - User's tracked stocks with real-time updates
4. **Portfolio Dashboard** - Deep dive into holdings (allocation, risk, performance)
5. **News + Fact-Check Center** - Multi-source verification dashboard
6. **Alerts Center** - Manage all custom alerts (price, volume, news, earnings)
7. **Premium Insights Dashboard** - Advanced analytics (locked for free users)
8. **Settings + Identity Profile** - Account settings, preferences, profile

### Modal/Overlay Screens (6 Total)

1. **Stock Detail Modal** - Deep dive on single stock
2. **Add to Portfolio Modal** - Manual entry or CSV upload
3. **Add to Watchlist Modal** - Search and add stocks
4. **Create Alert Modal** - Configure custom alert
5. **Premium Upgrade Modal** - Conversion flow
6. **Profile Edit Modal** - Update user details

---

## 🏠 DASHBOARD A: HOME DASHBOARD

### Purpose
**First screen after login.** Quick overview of portfolio, market, and news. Get the essentials at a glance.

### Layout Structure (Desktop)

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER: Logo | Home | Market | Watchlist | Portfolio | News    │
│         Alerts (icon) | Premium (badge) | Profile (avatar)      │
├─────────────────────────────────────────────────────────────────┤
│ MARKET TICKER BAR (scrolling, 48px height)                      │
│ ⬆ AAPL $175.23 +2.4% | ⬇ TSLA $243.15 -1.2% | ...             │
├─────────────────────────────────────────────────────────────────┤
│ MARKET SENTIMENT BAR (full width, 80px height)                  │
│ Fear & Greed Index: 65 (Greed) | VIX: 14.2 | Top Sector: Tech  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────────────────────┐  ┌────────────────────────────┐│
│ │ YOUR PORTFOLIO SNAPSHOT     │  │ TOP MOVERS (YOUR HOLDINGS) ││
│ │                             │  │                            ││
│ │ Total Value: $125,450.32    │  │ 1. AAPL   ⬆ +3.2%         ││
│ │ ⬆ +$2,340.21 (+1.9%) Today  │  │ 2. MSFT   ⬆ +1.8%         ││
│ │                             │  │ 3. GOOGL  ⬇ -0.5%         ││
│ │ [Allocation Pie Chart]      │  │ 4. TSLA   ⬇ -2.1%         ││
│ │                             │  │                            ││
│ │ • Tech (45%)                │  │ [View Full Portfolio →]    ││
│ │ • Finance (30%)             │  │                            ││
│ │ • Healthcare (15%)          │  │                            ││
│ │ • Energy (10%)              │  │                            ││
│ │                             │  │                            ││
│ │ Last updated 2m ago         │  │                            ││
│ └─────────────────────────────┘  └────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ VERIFIED NEWS FEED                                          ││
│ │                                                             ││
│ │ ✅ Confirmed by 3 sources                                   ││
│ │ Apple announces new product line                            ││
│ │ Bloomberg, Reuters, CNBC • 2 hours ago                      ││
│ │                                                             ││
│ │ ⚠️ Developing story                                         ││
│ │ Fed signals potential rate change                           ││
│ │ Reuters, WSJ • 15 minutes ago                               ││
│ │                                                             ││
│ │ [View All News →]                                           ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ AI PORTFOLIO SUMMARY                                        ││
│ │                                                             ││
│ │ 🤖 Your portfolio is allocated 45% technology, 30%          ││
│ │    finance, 15% healthcare, and 10% energy. Your largest   ││
│ │    holding is Apple (12% of portfolio). Your portfolio's   ││
│ │    average volatility is 18%.                              ││
│ │                                                             ││
│ │ ⚠️ AI-Generated Content: Descriptive only. Not advice.     ││
│ │                                                             ││
│ │ [Get Advanced AI Insights (Premium) →]                     ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ ACTIVE ALERTS (2)                                           ││
│ │                                                             ││
│ │ 🔔 AAPL above $180 (Current: $175.23)                      ││
│ │ 🔔 NVDA volume > 50M (Current: 32M)                        ││
│ │                                                             ││
│ │ [Manage Alerts →]                                          ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

**Top Section (Fixed):**
1. **Header Navigation** (Height: 64px)
   - Logo (left): DominionMarkets logo + text
   - Nav links (center): Home, Market, Watchlist, Portfolio, News
   - Actions (right): Alerts icon (badge if active), Premium badge, Profile avatar

2. **Market Ticker Bar** (Height: 48px)
   - Auto-scrolling horizontal ticker
   - Format: `[Icon] SYMBOL $PRICE ±CHANGE%`
   - Color: Green for positive, Red for negative
   - Pause on hover

3. **Market Sentiment Bar** (Height: 80px)
   - Fear & Greed Index (0-100 scale with visual gauge)
   - VIX (volatility index)
   - Top sector of the day
   - Background: Gradient based on sentiment (green = greed, red = fear)

**Middle Section (Scrollable):**

4. **Portfolio Snapshot Card** (Left column, 400px width)
   - Total portfolio value (36px bold)
   - Daily change (20px, color-coded)
   - Allocation pie chart (200px diameter)
   - Legend below chart
   - Last updated timestamp

5. **Top Movers Card** (Right column, flexible width)
   - List of top 4 holdings by % change today
   - Format: Rank, Symbol, % Change, Icon
   - Link to full portfolio at bottom

6. **Verified News Feed Card** (Full width)
   - 2-3 latest verified headlines
   - Verification badge (✅ ⚠️)
   - Source list + timestamp
   - "View All News" CTA

7. **AI Portfolio Summary Card** (Full width)
   - Descriptive AI summary (GPT-4 generated)
   - Disclaimer badge
   - Premium upsell CTA if applicable

8. **Active Alerts Preview** (Full width, collapsible)
   - Shows 2 most recent alerts
   - Status: Active (🔔) or Triggered (✅)
   - Current vs. target value
   - "Manage Alerts" link

### Responsive Behavior (Mobile)

**Mobile (<768px):**
- Stack all cards vertically
- Portfolio snapshot: Full width, pie chart 180px
- Top movers: Show top 3 only
- News feed: Show 2 headlines only
- Sentiment bar: Show Fear & Greed Index only (hide VIX and top sector)

---

## 📊 DASHBOARD B: MARKET OVERVIEW DASHBOARD

### Purpose
**Broad market view.** Understand what's happening across sectors, identify opportunities, see trends.

### Layout Structure (Desktop)

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER (same as Home Dashboard)                                 │
├─────────────────────────────────────────────────────────────────┤
│ MARKET TICKER BAR (same as Home)                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ SECTOR HEATMAP (Full width, 400px height)                   ││
│ │                                                             ││
│ │ [Interactive heatmap with color-coded sectors]             ││
│ │ • Technology (+2.5%) — GREEN                               ││
│ │ • Finance (+1.2%) — LIGHT GREEN                            ││
│ │ • Healthcare (-0.3%) — LIGHT RED                           ││
│ │ • Energy (-1.8%) — RED                                     ││
│ │                                                             ││
│ │ Click sector to filter stocks below                         ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────┐  ┌────────────────────────────────┐│
│ │ TOP GAINERS (TODAY)     │  │ TOP LOSERS (TODAY)             ││
│ │                         │  │                                ││
│ │ 1. NVDA  ⬆ +5.8%       │  │ 1. TSLA  ⬇ -4.2%              ││
│ │ 2. AMD   ⬆ +4.3%       │  │ 2. NFLX  ⬇ -3.5%              ││
│ │ 3. PLTR  ⬆ +3.9%       │  │ 3. DIS   ⬇ -2.8%              ││
│ │ 4. SHOP  ⬆ +3.2%       │  │ 4. PYPL  ⬇ -2.1%              ││
│ │ 5. SQ    ⬆ +2.7%       │  │ 5. SNAP  ⬇ -1.9%              ││
│ │                         │  │                                ││
│ │ [View Top 50 →]         │  │ [View Top 50 →]                ││
│ └─────────────────────────┘  └────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ VOLUME SPIKES (Unusual Activity)                            ││
│ │                                                             ││
│ │ AAPL  | Volume: 120M (Avg: 45M) | +167% above average      ││
│ │ TSLA  | Volume: 95M (Avg: 65M)  | +46% above average       ││
│ │ NVDA  | Volume: 88M (Avg: 50M)  | +76% above average       ││
│ │                                                             ││
│ │ 🔔 Set alert for volume spikes                             ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ EARNINGS CALENDAR (Next 7 Days)                             ││
│ │                                                             ││
│ │ Dec 24 | AAPL  | Expected EPS: $2.10 | Market Open         ││
│ │ Dec 25 | MSFT  | Expected EPS: $2.85 | After Close         ││
│ │ Dec 26 | GOOGL | Expected EPS: $1.55 | Market Open         ││
│ │                                                             ││
│ │ [View Full Calendar (Premium) →]                           ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ MARKET SENTIMENT INDICATORS                                 ││
│ │                                                             ││
│ │ Fear & Greed Index: 65 (Greed)                             ││
│ │ [Gauge visualization]                                       ││
│ │                                                             ││
│ │ VIX (Volatility): 14.2 (Low)                               ││
│ │ Put/Call Ratio: 0.85 (Bullish)                             ││
│ │ Advance/Decline: 1,850 / 1,120 (Bullish)                   ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Interactions

**Sector Heatmap:**
- Hover: Show sector name + % change + number of stocks
- Click: Filter stocks below by selected sector
- Color scale: Dark red (-5%) → Light gray (0%) → Dark green (+5%)

**Top Gainers/Losers:**
- Click stock: Open stock detail modal
- "View Top 50" link: Navigate to full list page

**Volume Spikes:**
- Show stocks with 50%+ above average volume
- "Set alert" button: Open alert creation modal

**Earnings Calendar:**
- Free users: See next 7 days (3 events)
- Premium users: See next 60 days (unlimited events)
- Click event: Open stock detail modal

---

## 👀 DASHBOARD C: WATCHLIST DASHBOARD

### Purpose
**Track your favorite stocks.** See real-time prices, changes, and set alerts.

### Layout Structure (Desktop)

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER (same as Home Dashboard)                                 │
├─────────────────────────────────────────────────────────────────┤
│ WATCHLIST TITLE + ACTIONS                                       │
│ My Watchlist (12 stocks)          [+ Add Stock] [Sort by ▼]    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ WATCHLIST TABLE                                             ││
│ │                                                             ││
│ │ Symbol | Price    | Change   | Volume  | Mkt Cap | Alert  ││
│ ├─────────────────────────────────────────────────────────────┤│
│ │ AAPL   | $175.23  | ⬆ +2.4%  | 45.2M   | $2.8T   | 🔔    ││
│ │ MSFT   | $370.15  | ⬇ -0.8%  | 23.1M   | $2.7T   | —     ││
│ │ GOOGL  | $140.50  | ⬆ +1.2%  | 18.4M   | $1.8T   | 🔔    ││
│ │ TSLA   | $243.15  | ⬇ -2.1%  | 65.3M   | $768B   | —     ││
│ │ NVDA   | $495.80  | ⬆ +3.5%  | 50.1M   | $1.2T   | 🔔    ││
│ │ ...    | ...      | ...      | ...     | ...     | ...   ││
│ │                                                             ││
│ │ [Load More] or [View All]                                  ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ QUICK ACTIONS                                               ││
│ │                                                             ││
│ │ [Add All to Portfolio] [Set Price Alerts for All]          ││
│ │ [Export as CSV (Premium)]                                  ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ WATCHLIST NEWS (Stocks you're tracking)                     ││
│ │                                                             ││
│ │ ✅ AAPL: Apple announces new product line                   ││
│ │    Bloomberg, Reuters, CNBC • 2 hours ago                   ││
│ │                                                             ││
│ │ ⚠️ TSLA: Tesla production numbers released                  ││
│ │    Reuters • 1 hour ago                                     ││
│ │                                                             ││
│ │ [View All Watchlist News →]                                ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Features

**Watchlist Limits:**
- Free users: 5 stocks max
- Premium users: Unlimited
- Pro users: Unlimited + multiple watchlists

**Table Sorting:**
- Click column header to sort (ascending/descending)
- Default: Alphabetical by symbol
- Options: Price, % Change, Volume, Market Cap

**Alert Icon (🔔):**
- Gray: No alert set
- Gold + pulsing: Alert active
- Click: Open alert settings modal

**Row Actions:**
- Click row: Open stock detail modal
- Right-click: Context menu (Add to portfolio, Remove from watchlist, Set alert)
- Swipe left (mobile): Reveal delete button

---

## 💼 DASHBOARD D: PORTFOLIO DASHBOARD

### Purpose
**Deep dive into your holdings.** Understand allocation, risk, performance, and get AI insights.

### Layout Structure (Desktop)

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER (same as Home Dashboard)                                 │
├─────────────────────────────────────────────────────────────────┤
│ PORTFOLIO TITLE + ACTIONS                                       │
│ My Portfolio              [+ Add Holding] [Import CSV] [Export] │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────────────────┐  ┌────────────────────────────────┐│
│ │ TOTAL VALUE             │  │ DAILY CHANGE                   ││
│ │                         │  │                                ││
│ │ $125,450.32             │  │ ⬆ +$2,340.21 (+1.9%)          ││
│ │                         │  │                                ││
│ │ Weekly: ⬆ +$4,230       │  │ Weekly: ⬆ +3.5%               ││
│ │ Monthly: ⬆ +$8,120      │  │ Monthly: ⬆ +6.9%              ││
│ └─────────────────────────┘  └────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ ALLOCATION BREAKDOWN                                        ││
│ │                                                             ││
│ │ [Pie Chart: 300px diameter]                                ││
│ │                                                             ││
│ │ By Sector:                                                  ││
│ │ • Technology (45%) — $56,452                               ││
│ │ • Finance (30%) — $37,635                                  ││
│ │ • Healthcare (15%) — $18,817                               ││
│ │ • Energy (10%) — $12,545                                   ││
│ │                                                             ││
│ │ [View by Asset Type] [View by Region] (Premium)            ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ HOLDINGS TABLE                                              ││
│ │                                                             ││
│ │ Symbol | Shares | Value    | Change   | Weight | Actions  ││
│ ├─────────────────────────────────────────────────────────────┤│
│ │ AAPL   | 50     | $8,761   | ⬆ +2.4%  | 7.0%   | [Edit]  ││
│ │ MSFT   | 30     | $11,104  | ⬇ -0.8%  | 8.8%   | [Edit]  ││
│ │ GOOGL  | 80     | $11,240  | ⬆ +1.2%  | 9.0%   | [Edit]  ││
│ │ ...    | ...    | ...      | ...      | ...    | ...     ││
│ │                                                             ││
│ │ Total: 12 holdings | Total value: $125,450.32              ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ RISK EXPOSURE SUMMARY (Premium Feature)                     ││
│ │                                                             ││
│ │ Portfolio Volatility: 18% (Moderate)                        ││
│ │ [Gauge: Low | Moderate | High]                             ││
│ │                                                             ││
│ │ Largest Position: GOOGL (9.0% of portfolio)                ││
│ │ Sector Concentration: Tech (45%) — High exposure           ││
│ │                                                             ││
│ │ [Unlock Advanced Risk Analysis →]                          ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ DIVERSIFICATION SCORE (Premium Feature)                     ││
│ │                                                             ││
│ │ Your Score: 68/100 (Moderate)                              ││
│ │ [Progress bar visualization]                                ││
│ │                                                             ││
│ │ Recommendations:                                            ││
│ │ • Consider adding international stocks                     ││
│ │ • Technology sector is over-represented                    ││
│ │ • Add 2-3 defensive stocks (utilities, consumer staples)   ││
│ │                                                             ││
│ │ ⚠️ Descriptive analysis only. Not investment advice.       ││
│ │                                                             ││
│ │ [Unlock Full Diversification Report →]                     ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ AI PORTFOLIO INSIGHTS (Premium Feature)                     ││
│ │                                                             ││
│ │ 🤖 Your portfolio generated a 1.9% return today, driven    ││
│ │    primarily by technology stocks (+3.2% average). Your    ││
│ │    largest gainer was NVDA (+3.5%), contributing $420 to   ││
│ │    today's gains. Finance and healthcare sectors saw       ││
│ │    modest declines (-0.5% average), limiting losses to     ││
│ │    $120.                                                    ││
│ │                                                             ││
│ │ Your portfolio's volatility remains at 18%, consistent     ││
│ │    with your historical average. Sector concentration is   ││
│ │    45% technology, which is above the market average of    ││
│ │    30%.                                                     ││
│ │                                                             ││
│ │ ⚠️ AI-Generated. Descriptive only. Not advice.             ││
│ │                                                             ││
│ │ [Get Weekly AI Portfolio Report (Premium) →]               ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Features

**Portfolio Limits:**
- Free users: 1 portfolio, 10 holdings max
- Premium users: 3 portfolios, unlimited holdings
- Pro users: Unlimited portfolios

**Manual Entry Only:**
- Privacy-first: No brokerage connections
- User enters: Symbol, Shares, Purchase Price (optional)
- System calculates: Current value, % change, portfolio weight

**Edit Holding:**
- Click [Edit] button: Open inline editor or modal
- Update shares or purchase price
- Delete holding (with confirmation)

**Premium Features (Locked for Free Users):**
- Risk exposure summary
- Diversification score
- Advanced AI insights
- Historical performance charts (1+ year)
- Benchmark comparison (S&P 500, Nasdaq)

---

## 📰 DASHBOARD E: NEWS + FACT-CHECK CENTER

### Purpose
**Multi-source news verification.** See what multiple sources say, identify conflicts, build trust through transparency.

### Layout Structure (Desktop)

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER (same as Home Dashboard)                                 │
├─────────────────────────────────────────────────────────────────┤
│ NEWS CENTER TITLE + FILTERS                                     │
│ Verified News        [All Sources ▼] [All Stocks ▼] [Today ▼]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ STORY CLUSTER #1                                            ││
│ │                                                             ││
│ │ ✅ Verified by 3 sources                                    ││
│ │                                                             ││
│ │ Apple announces new product line                            ││
│ │                                                             ││
│ │ Sources:                                                    ││
│ │                                                             ││
│ │ 📰 Bloomberg | 10:00 AM | 2 hours ago                      ││
│ │    "Apple Inc. announced a new line of..."                 ││
│ │    By Mark Gurman                                           ││
│ │    [Read Full Article ↗]                                    ││
│ │                                                             ││
│ │ 📰 Reuters | 10:05 AM | 2 hours ago                        ││
│ │    "Tech giant Apple unveiled today..."                    ││
│ │    By Stephen Nellis                                        ││
│ │    [Read Full Article ↗]                                    ││
│ │                                                             ││
│ │ 📰 CNBC | 10:10 AM | 2 hours ago                           ││
│ │    "In a surprise announcement, Apple..."                  ││
│ │    By Kif Leswing                                           ││
│ │    [Read Full Article ↗]                                    ││
│ │                                                             ││
│ │ AI Summary:                                                 ││
│ │ "Three sources confirm Apple announced a new product today. ││
│ │  Bloomberg reported at 10:00 AM, Reuters at 10:05 AM, and  ││
│ │  CNBC at 10:10 AM. All three sources agree on the product  ││
│ │  name and release date. Bloomberg and Reuters report the   ││
│ │  price as $999, while CNBC has not yet mentioned price."   ││
│ │                                                             ││
│ │ ⚠️ AI-Generated Summary. Not advice.                       ││
│ │                                                             ││
│ │ [View Full Fact-Check Report →]                            ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ STORY CLUSTER #2                                            ││
│ │                                                             ││
│ │ ⚠️ Developing Story                                         ││
│ │                                                             ││
│ │ Fed signals potential rate change                           ││
│ │                                                             ││
│ │ Sources:                                                    ││
│ │                                                             ││
│ │ 📰 Reuters | 11:45 AM | 15 minutes ago                     ││
│ │    "Federal Reserve officials hinted at..."                ││
│ │    [Read Full Article ↗]                                    ││
│ │                                                             ││
│ │ 📰 WSJ | 11:50 AM | 10 minutes ago                         ││
│ │    "The Fed's latest statement suggests..."                ││
│ │    [Read Full Article ↗]                                    ││
│ │                                                             ││
│ │ AI Summary:                                                 ││
│ │ "Two sources report Fed officials made statements about    ││
│ │  interest rates. Reuters published first at 11:45 AM, WSJ  ││
│ │  followed at 11:50 AM. Both sources agree on timing but    ││
│ │  differ on interpretation. Story is still developing."     ││
│ │                                                             ││
│ │ ⚠️ Story developing. Check back for updates.               ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ STORY CLUSTER #3                                            ││
│ │                                                             ││
│ │ ❌ Conflicting Reports                                      ││
│ │                                                             ││
│ │ Tech sector volatility concerns                             ││
│ │                                                             ││
│ │ Sources:                                                    ││
│ │                                                             ││
│ │ 📰 Source A: "Tech stocks surge 5%"                        ││
│ │ 📰 Source B: "Tech stocks drop 2%"                         ││
│ │                                                             ││
│ │ ⚠️ Sources conflict. Wait for more information.            ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ [Load More Stories]                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Verification Badge System

**✅ Verified by X sources (Green)**
- 3+ sources report same key facts
- No major conflicts detected
- High confidence

**⚠️ Developing Story (Yellow)**
- 2 sources, or facts still emerging
- Minor discrepancies
- Medium confidence

**⚠️ Unverified (Coral)**
- Only 1 source reporting
- Cannot cross-check
- Low confidence

**❌ Conflicting Reports (Red)**
- Sources contradict each other
- User should wait for clarity
- No confidence

### Filter Options

**By Source:**
- All Sources
- Tier 1 Only (Bloomberg, Reuters, AP, WSJ)
- Caribbean Sources Only

**By Stock:**
- All Stocks
- Watchlist Stocks Only
- Portfolio Stocks Only
- Specific Symbol (search)

**By Time:**
- Today
- Last 7 Days
- Last 30 Days

---

## 🔔 DASHBOARD F: ALERTS CENTER

### Purpose
**Manage custom alerts.** Set price, volume, news, and earnings alerts. Get notified when conditions are met.

### Layout Structure (Desktop)

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER (same as Home Dashboard)                                 │
├─────────────────────────────────────────────────────────────────┤
│ ALERTS CENTER TITLE + ACTIONS                                   │
│ Your Alerts (8 active)                    [+ Create New Alert]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ PRICE ALERTS (4)                                            ││
│ │                                                             ││
│ │ ┌─────────────────────────────────────────────────────────┐││
│ │ │ 🔔 AAPL above $180.00                                   │││
│ │ │ Current: $175.23 | Set 2 days ago                       │││
│ │ │ [Edit] [Delete] [Toggle Off]                            │││
│ │ └─────────────────────────────────────────────────────────┘││
│ │                                                             ││
│ │ ┌─────────────────────────────────────────────────────────┐││
│ │ │ 🔕 TSLA below $200.00 (Inactive)                        │││
│ │ │ Current: $243.15 | Set 5 days ago                       │││
│ │ │ [Edit] [Delete] [Toggle On]                             │││
│ │ └─────────────────────────────────────────────────────────┘││
│ │                                                             ││
│ │ [View All Price Alerts →]                                  ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ VOLUME ALERTS (2)                                           ││
│ │                                                             ││
│ │ ┌─────────────────────────────────────────────────────────┐││
│ │ │ 🔔 NVDA volume > 50M                                    │││
│ │ │ Current: 32M | Set today                                │││
│ │ │ [Edit] [Delete] [Toggle Off]                            │││
│ │ └─────────────────────────────────────────────────────────┘││
│ │                                                             ││
│ │ [View All Volume Alerts →]                                 ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ NEWS ALERTS (1)                                             ││
│ │                                                             ││
│ │ ┌─────────────────────────────────────────────────────────┐││
│ │ │ 🔔 AAPL verified news only                              │││
│ │ │ Notify when: Multi-source verified news published       │││
│ │ │ [Edit] [Delete] [Toggle Off]                            │││
│ │ └─────────────────────────────────────────────────────────┘││
│ │                                                             ││
│ │ [View All News Alerts →]                                   ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ EARNINGS ALERTS (1)                                         ││
│ │                                                             ││
│ │ ┌─────────────────────────────────────────────────────────┐││
│ │ │ 🔔 AAPL earnings report                                 │││
│ │ │ Scheduled: Dec 28, 2025 (4 days)                        │││
│ │ │ Reminder: 24 hours before                               │││
│ │ │ [Edit] [Delete] [Toggle Off]                            │││
│ │ └─────────────────────────────────────────────────────────┘││
│ │                                                             ││
│ │ [View All Earnings Alerts →]                               ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ RECENT TRIGGERED ALERTS (Last 7 days)                       ││
│ │                                                             ││
│ │ ✅ AAPL hit $180 • Triggered 3 hours ago                   ││
│ │ ✅ NVDA volume spike • Triggered yesterday                 ││
│ │ ✅ MSFT earnings reminder • Triggered 2 days ago           ││
│ │                                                             ││
│ │ [View Alert History →]                                     ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Alert Types

**1. Price Alert**
- Condition: Above / Below / Equals price
- Example: "AAPL above $180"
- Notification: Push + email

**2. Volume Alert**
- Condition: Volume exceeds threshold
- Example: "NVDA volume > 50M"
- Notification: Push + email

**3. News Alert**
- Trigger: Verified news published about stock
- Filter: Verified only / All news
- Notification: Push + email

**4. Earnings Alert**
- Trigger: Earnings report scheduled
- Reminder: 24 hours before
- Notification: Email (day before)

### Alert Limits

**Free Users:** 0 alerts (Premium feature)  
**Premium Users:** Unlimited alerts  
**Pro Users:** Unlimited + webhook support

---

## 💎 DASHBOARD G: PREMIUM INSIGHTS DASHBOARD

### Purpose
**Advanced analytics for Premium/Pro users.** Unlock institutional-grade tools, risk analysis, and AI insights.

### Layout Structure (Desktop)

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER (same as Home Dashboard)                                 │
├─────────────────────────────────────────────────────────────────┤
│ PREMIUM INSIGHTS TITLE                                          │
│ Premium Insights      [Weekly] [Monthly] [Quarterly] [Custom]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ PORTFOLIO PERFORMANCE (Historical)                          ││
│ │                                                             ││
│ │ [Line chart: 1 year of returns]                            ││
│ │                                                             ││
│ │ Total Return (1Y): ⬆ +18.5%                                ││
│ │ Best Month: March 2025 (+8.2%)                             ││
│ │ Worst Month: August 2025 (-3.1%)                           ││
│ │                                                             ││
│ │ [Compare to S&P 500] [Compare to Nasdaq]                   ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ RISK ANALYSIS (Advanced)                                    ││
│ │                                                             ││
│ │ Portfolio Beta: 1.2 (20% more volatile than market)        ││
│ │ Sharpe Ratio: 1.8 (Good risk-adjusted return)              ││
│ │ Max Drawdown: -12.5% (Moderate)                            ││
│ │                                                             ││
│ │ Volatility by Holding:                                      ││
│ │ • NVDA: High (32%)                                         ││
│ │ • TSLA: High (45%)                                         ││
│ │ • AAPL: Moderate (22%)                                     ││
│ │ • MSFT: Low (18%)                                          ││
│ │                                                             ││
│ │ [Download Full Risk Report (PDF) →]                        ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ SECTOR CONCENTRATION ANALYSIS                               ││
│ │                                                             ││
│ │ Your Portfolio:           Market Average:                   ││
│ │ • Technology: 45%         • Technology: 30%                ││
│ │ • Finance: 30%            • Finance: 15%                   ││
│ │ • Healthcare: 15%         • Healthcare: 12%                ││
│ │ • Energy: 10%             • Energy: 8%                     ││
│ │                                                             ││
│ │ ⚠️ Your technology exposure is 50% above market average.   ││
│ │    Consider diversifying into other sectors.               ││
│ │                                                             ││
│ │ ⚠️ Descriptive analysis. Not advice.                       ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ AI WEEKLY PORTFOLIO REPORT                                  ││
│ │                                                             ││
│ │ 🤖 This week, your portfolio gained 2.3% ($2,890), driven  ││
│ │    primarily by technology stocks which averaged +4.1%.    ││
│ │    Your top performer was NVDA (+6.8%, $780 gain), while   ││
│ │    your largest detractor was TSLA (-3.2%, $380 loss).     ││
│ │                                                             ││
│ │    Sector performance: Technology led (+4.1%), followed by ││
│ │    Healthcare (+1.5%), Finance (+0.8%), and Energy (-0.5%).││
│ │                                                             ││
│ │    Your portfolio's volatility increased to 19% this week, ││
│ │    up from 18% last week. This is driven by increased      ││
│ │    volatility in NVDA and TSLA holdings.                   ││
│ │                                                             ││
│ │    Diversification score remains at 68/100 (Moderate).     ││
│ │    Consider adding international stocks or defensive       ││
│ │    sectors to improve diversification.                     ││
│ │                                                             ││
│ │ ⚠️ AI-Generated Report. Descriptive only. Not advice.      ││
│ │                                                             ││
│ │ [Download Full Report (PDF)] [Email Report]               ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ MACRO MARKET DATA (Pro Feature)                             ││
│ │                                                             ││
│ │ Economic Indicators:                                        ││
│ │ • GDP Growth: 2.5% (Q3 2025)                               ││
│ │ • Inflation (CPI): 3.2% (November 2025)                    ││
│ │ • Unemployment: 3.8%                                        ││
│ │ • Fed Funds Rate: 5.25%                                    ││
│ │                                                             ││
│ │ Commodity Prices:                                           ││
│ │ • Gold: $2,050/oz                                          ││
│ │ • Oil (WTI): $78/barrel                                    ││
│ │ • Copper: $8,500/ton                                       ││
│ │                                                             ││
│ │ [View Full Macro Dashboard (Pro) →]                        ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Premium vs. Pro Features

**Premium Features:**
- Historical performance (1 year)
- Basic risk analysis (volatility, beta)
- Sector concentration
- AI weekly reports

**Pro-Only Features:**
- Historical performance (10 years)
- Advanced risk metrics (Sharpe ratio, max drawdown, Sortino ratio)
- Macro market data (GDP, inflation, commodities)
- Custom chart templates
- Technical indicators (RSI, MACD, Bollinger Bands)

---

## ⚙️ DASHBOARD H: SETTINGS + IDENTITY PROFILE

### Purpose
**Account management.** Update profile, preferences, notifications, and identity.

### Layout Structure (Desktop)

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER (same as Home Dashboard)                                 │
├─────────────────────────────────────────────────────────────────┤
│ SETTINGS TITLE                                                  │
│ Settings                                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ [Sidebar Navigation]         [Main Content Area]               │
│                                                                 │
│ • Profile                    [Active Section Content]           │
│ • Notifications                                                 │
│ • Privacy                                                       │
│ • Billing                                                       │
│ • Identity                                                      │
│ • Support                                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Section: Profile

```
PROFILE SETTINGS

Avatar
[Profile picture upload]
[Change Photo] [Remove]

Name
Jermaine Merritt
[Edit]

Email
jermaine@codexdominion.app
[Verify Email] (if not verified)

Time Zone
EST (UTC-5)
[Change]

Currency Preference
USD ($)
[Change]

[Save Changes]
```

### Section: Notifications

```
NOTIFICATION PREFERENCES

Email Notifications
☑ Price alerts
☑ Volume alerts
☑ News alerts
☑ Earnings reminders
☐ Weekly portfolio summary
☐ Marketing emails

Push Notifications (Mobile)
☑ Price alerts
☑ Breaking news
☐ Daily market summary

[Save Preferences]
```

### Section: Privacy

```
PRIVACY SETTINGS

Portfolio Data
• Your portfolio data is private and never shared
• Manual entry only (no brokerage connections)
• Data stored encrypted in our database

Data Export
[Download Your Data (CSV)]

Account Deletion
[Delete Account] (requires confirmation)

Privacy Policy
[View Privacy Policy]
```

### Section: Billing

```
BILLING & SUBSCRIPTION

Current Plan
Premium ($9.99/month)
Next billing date: January 24, 2026

[Upgrade to Pro] [Cancel Subscription]

Payment Method
Visa ending in 1234
[Update Payment Method]

Billing History
Dec 24, 2025 - $9.99 (Premium)
Nov 24, 2025 - $9.99 (Premium)
[View All Invoices →]
```

### Section: Identity (Caribbean/Diaspora Focus)

```
IDENTITY PROFILE

Cultural Background
Caribbean Diaspora
[Edit]

Home Country
Jamaica 🇯🇲
[Select from dropdown]

Current Location
Toronto, Canada 🇨🇦
[Edit]

Language Preference
English (Caribbean)
[Change]

Interests
☑ Caribbean stock markets (JSE, TTSE, BSE)
☑ Diaspora investment opportunities
☑ Financial literacy education
☐ Youth financial programs

[Save Identity Profile]
```

---

## 📊 RESPONSIVE DESIGN NOTES

### Mobile (<768px)

**Universal Changes:**
- Stack all columns vertically
- Hide secondary navigation (use hamburger menu)
- Reduce font sizes by 10%
- Increase touch targets to 44×44px minimum
- Swipe gestures for list actions (delete, edit)

**Component Adjustments:**
- Tables → Cards (easier scrolling)
- Pie charts → 180px diameter (reduced from 300px)
- News headlines → 2 lines max (truncate with ellipsis)
- Portfolio allocation → Show top 4 sectors only

---

## ✅ DASHBOARD WIREFRAMES CHECKLIST

- [x] 8 primary dashboards documented
- [x] Home Dashboard layout defined
- [x] Market Overview Dashboard layout defined
- [x] Watchlist Dashboard layout defined
- [x] Portfolio Dashboard layout defined
- [x] News + Fact-Check Center layout defined
- [x] Alerts Center layout defined
- [x] Premium Insights Dashboard layout defined
- [x] Settings + Identity Profile layout defined
- [x] Core UI principles documented
- [x] Responsive behavior specified
- [x] Component interactions described
- [x] Premium/Free tier distinctions clarified

---

**Status:** DASHBOARD WIREFRAMES COMPLETE ✅  
**Next Steps:** Create high-fidelity Figma mockups, build React components, user testing  
**Launch Target:** Q2 2025
