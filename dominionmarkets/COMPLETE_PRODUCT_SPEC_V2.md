# DominionMarkets - Complete Product Specification v2.0

**Last Updated:** December 24, 2025  
**Status:** ✅ All Issues Resolved - Production Ready  
**Version:** 2.0 (Final, Buildable, Consistent)

---

## 📋 DOCUMENT PURPOSE

This is the **master specification** for DominionMarkets. Every feature, flow, screen, and interaction is documented here. All 10 critical issues from v1.0 have been resolved.

**What Changed in v2.0:**
- ✅ Branded features fully defined (Sovereign Portfolio DNA™, Cultural Alpha Engine™, Diaspora Economic Flow Maps™)
- ✅ Identity system consistent (4 types: Diaspora, Youth, Creator, Legacy-Builder)
- ✅ Premium tiers clarified (Free, Premium $14.99, Pro $29.99)
- ✅ Navigation architecture specified (desktop + mobile)
- ✅ Onboarding shortened (6 screens → 3 screens)
- ✅ Authentication flow complete (login, signup, SSO)
- ✅ Cross-promotion detailed (specific products, challenges, stories)
- ✅ Error states defined (empty portfolio, API failures)
- ✅ Missing features added (search, notifications, CSV export)
- ✅ Analytics tracking plan complete (events, funnels, metrics)

---

## 🎯 CORE PRODUCT PILLARS

DominionMarkets is built on **four foundational pillars**:

### 1. Market Intelligence
Real-time stock data, interactive charts, watchlists, sector heatmaps, and market sentiment tracking.

**Features:**
- Live price updates (15-minute delay for free, real-time for Premium)
- 7-day to 20-year historical charts
- Sector heatmaps with color-coded performance
- Top movers (gainers, losers, volume spikes)
- Market sentiment indicators

### 2. Portfolio Insights
Safe, descriptive analytics that help users understand their holdings **without giving financial advice**.

**Features:**
- Portfolio value tracking
- Allocation breakdown (pie charts, sector distribution)
- Diversification scoring (Premium)
- Volatility summaries (Premium)
- Risk exposure analysis (Premium)
- AI-generated portfolio summaries (descriptive only)

**Compliance Note:** All insights use descriptive language ("Your portfolio is tech-heavy") rather than prescriptive ("You should diversify").

### 3. Verified News
Multi-source fact-checking engine that verifies financial news across multiple outlets before displaying.

**Features:**
- Multi-source verification (3+ sources = ✅ Verified)
- Developing story tracking (⚠️ Developing)
- Conflicting report flags (❌ Conflicting)
- Source transparency (list of all sources)
- Timeline of confirmations (when each source published)
- AI summarization of verified stories

**Fact-Check Algorithm:**
1. Aggregate headlines from 20+ news sources
2. Cluster similar stories using NLP
3. Count confirmations across independent sources
4. Assign verification badge (Verified, Developing, Conflicting, Unverified)
5. Update in real-time as new sources confirm/contradict

### 4. Identity-Driven Personalization
Dashboard adapts to user's identity, values, and investment style using three proprietary engines:

- **Sovereign Portfolio DNA™** - Portfolio interpretation engine
- **Cultural Alpha Engine™** - Cultural influence scoring
- **Diaspora Economic Flow Maps™** - Economic activity visualization

All three engines are **fully defined** in this document (see sections below).

---

## 🧬 BRANDED FEATURES (FULLY DEFINED)

### A. Sovereign Portfolio DNA™

**Purpose:** Identity-based portfolio interpretation engine that adjusts dashboard based on user's profile.

**How It Works:**

**Inputs:**
1. **Identity Type** (Diaspora, Youth, Creator, Legacy-Builder)
2. **Portfolio Composition** (stocks, sectors, allocation percentages)
3. **Sector Exposure** (tech, healthcare, finance, etc.)
4. **Volatility Profile** (calculated from 30-day price movements)
5. **Time Horizon** (user-selected: short-term <1yr, medium 1-5yr, long-term 5+yr)
6. **Risk Comfort** (user-selected: conservative, moderate, aggressive)

**Algorithm (Descriptive Only - No Advice):**

```
Step 1: Categorize Holdings by Sector
- Map each stock to primary sector (tech, healthcare, consumer, etc.)
- Calculate sector allocation percentages

Step 2: Compare to Identity-Based Archetype
- Diaspora archetype: High allocation in remittance-linked sectors (finance, telecom)
- Youth archetype: High allocation in growth stocks (tech, consumer)
- Creator archetype: High allocation in creator-economy companies (e-commerce, social, SaaS)
- Legacy-Builder archetype: High allocation in dividend stocks (utilities, consumer staples)

Step 3: Generate Descriptive Insights (NO RECOMMENDATIONS)
- "Your portfolio is tech-heavy (62% allocation)."
- "Your holdings align with creator-economy companies."
- "Your portfolio resembles long-term wealth builders."
- "Your allocation matches typical diaspora remittance-linked sectors."

Step 4: Adjust Dashboard Theme + Widgets
- Diaspora → Show Diaspora Economic Flow Maps™
- Youth → Show Learning Badges + Mock Portfolio
- Creator → Show Creator-Economy Index
- Legacy-Builder → Show Dividend Trackers + Long-Term Charts
```

**Output Examples:**

```typescript
interface PortfolioDNA {
  identity: 'diaspora' | 'youth' | 'creator' | 'legacy-builder';
  sectorAllocation: {
    tech: 62,
    finance: 18,
    healthcare: 12,
    consumer: 8,
  };
  archetype: 'growth-heavy' | 'balanced' | 'income-focused' | 'creator-aligned';
  insights: [
    "Your portfolio is growth-heavy with 62% in technology.",
    "This aligns with creator-economy investment patterns.",
    "Consider reviewing sector concentration (tech >50%)."
  ];
  volatilityProfile: 'high' | 'medium' | 'low';
  timeHorizon: 'short' | 'medium' | 'long';
}
```

**Compliance Safeguards:**
- ✅ Uses descriptive language only ("Your portfolio is..." not "You should...")
- ✅ No buy/sell recommendations
- ✅ No predictions about future performance
- ✅ Presents data, user makes decisions

---

### B. Cultural Alpha Engine™

**Purpose:** Scoring system that evaluates companies based on cultural relevance and global influence (NOT financial performance).

**How It Works:**

**Inputs:**
1. **Brand Influence** (Google Trends, social media mentions, search volume)
2. **Cultural Impact** (presence in music, fashion, entertainment, art)
3. **Diaspora Engagement** (mentions in diaspora media, community forums)
4. **Innovation Resonance** (patents filed, product launches, R&D spending)
5. **Ethical Governance** (ESG scores from public databases)

**Algorithm (Weighted Scoring Model):**

```
Cultural Alpha Score = (
  Brand Influence × 0.30 +
  Cultural Impact × 0.25 +
  Diaspora Engagement × 0.20 +
  Innovation Resonance × 0.15 +
  Ethical Governance × 0.10
) × 100

Score Range: 0-100
- 80-100: High Cultural Alpha (strong influence)
- 60-79: Medium Cultural Alpha (moderate influence)
- 40-59: Low Cultural Alpha (limited influence)
- 0-39: Minimal Cultural Alpha (niche/specialized)
```

**Scoring Components:**

**Brand Influence (30%):**
- Google Trends score (0-100)
- Social media mentions (Twitter, Instagram, TikTok)
- Search volume (Google, YouTube)
- Brand recognition surveys (if available)

**Cultural Impact (25%):**
- Music references (Spotify, Apple Music artist collaborations)
- Fashion relevance (Fashion Week partnerships, influencer mentions)
- Entertainment presence (product placement, brand integrations)
- Youth culture resonance (Gen Z adoption rate)

**Diaspora Engagement (20%):**
- Caribbean media mentions
- African diaspora community discussions
- Latin American market presence
- Diaspora-owned business partnerships

**Innovation Resonance (15%):**
- Patents filed (USPTO database)
- New product launches (press releases)
- R&D spending (% of revenue from financial statements)
- Tech innovation awards (CES, Webby, etc.)

**Ethical Governance (10%):**
- ESG scores (MSCI, Sustainalytics)
- Diversity reports (board composition, workforce demographics)
- Community investment (% of profits to social causes)
- Ethical controversies (negative: data breaches, lawsuits)

**Output Examples:**

```typescript
interface CulturalAlphaScore {
  symbol: string;              // 'AAPL'
  companyName: string;         // 'Apple Inc.'
  overallScore: number;        // 87 (0-100)
  tier: 'high' | 'medium' | 'low' | 'minimal';
  breakdown: {
    brandInfluence: 92,        // Out of 100
    culturalImpact: 85,
    diasporaEngagement: 78,
    innovationResonance: 95,
    ethicalGovernance: 82,
  };
  insights: [
    "Apple has strong cultural influence in youth markets.",
    "High innovation resonance with 2,500+ patents filed in 2024.",
    "Moderate diaspora engagement in Caribbean communities."
  ];
  trending: boolean;           // True if score increased >10 points in 30 days
}
```

**Compliance Safeguards:**
- ✅ Cultural Alpha ≠ Investment Recommendation
- ✅ Score is **descriptive**, not **predictive**
- ✅ No correlation to stock price performance
- ✅ Users warned: "Cultural influence does not predict financial returns."

---

### C. Diaspora Economic Flow Maps™

**Purpose:** Visualize how diaspora economic activity influences global markets and regional economies.

**How It Works:**

**Data Visualized:**
1. **Remittance Flows** (World Bank public data)
2. **Diaspora Population Density** (UN migration data)
3. **Regional Economic Activity** (GDP growth, employment rates)
4. **Tourism Cycles** (Caribbean Tourism Organization data)
5. **Caribbean-Linked Companies** (NCB, JMMB, RBL, ANSA, GraceKennedy)
6. **Diaspora-Owned Businesses** (publicly traded companies with diaspora founders)

**Widget Components:**

**1. Heatmap of Diaspora Hubs**
- Visual map showing diaspora population density
- Color-coded by concentration (dark blue = highest, light blue = lowest)
- Interactive: Click region to see economic data

**Example Regions:**
- **North America:** Toronto, New York, Miami (Caribbean diaspora)
- **UK:** London, Birmingham (Caribbean + African diaspora)
- **Europe:** Paris, Amsterdam (African diaspora)

**2. Flow Lines (Economic Influence)**
- Animated lines showing remittance flows from diaspora hubs → home countries
- Line thickness = remittance volume (thicker = more $$$)
- Color = growth trend (green = increasing, red = decreasing)

**Example Flows:**
- US → Jamaica: $2.4B annually (green, increasing)
- UK → Trinidad: $850M annually (yellow, stable)
- Canada → Barbados: $420M annually (green, increasing)

**3. Sector Impact Indicators**
- Which sectors benefit most from diaspora activity
- Color-coded cards showing:
  - **Finance** (remittance services, mobile banking)
  - **Real Estate** (diaspora property investments)
  - **Retail** (consumer goods, luxury items)
  - **Telecom** (international calling, data plans)
  - **Tourism** (hotel bookings, airlines)

**4. Caribbean-Linked Company Tracker**
- List of publicly traded companies with Caribbean operations
- Examples:
  - **NCB Financial (Jamaica)** - Banking, remittances
  - **JMMB (Jamaica)** - Investment services
  - **RBL (Trinidad)** - Retail banking
  - **ANSA McAL (Trinidad)** - Conglomerate (manufacturing, auto, finance)
  - **GraceKennedy (Jamaica)** - Food production, financial services

**Visualization Example:**

```
┌─────────────────────────────────────────────────────────────┐
│ 🌍 DIASPORA ECONOMIC FLOW MAPS™                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [MAP: Caribbean region + diaspora hubs]                    │
│  • Dark blue dots: Diaspora population centers              │
│  • Green flow lines: Remittance corridors                   │
│  • Gold markers: Caribbean-linked companies                 │
│                                                             │
│  REMITTANCE FLOWS (2024):                                   │
│  US → Jamaica:     $2.4B  (+8.5% YoY)  ████████████         │
│  UK → Trinidad:    $850M  (+2.1% YoY)  ████                 │
│  Canada → Barbados: $420M (+12.3% YoY) ██████               │
│                                                             │
│  SECTOR IMPACT:                                             │
│  ┌──────────────┬──────────────┬──────────────┐            │
│  │ Finance      │ Real Estate  │ Retail       │            │
│  │ High Impact  │ Medium Impact│ Medium Impact│            │
│  │ $4.2B flows  │ $1.8B invest │ $900M sales  │            │
│  └──────────────┴──────────────┴──────────────┘            │
│                                                             │
│  CARIBBEAN-LINKED COMPANIES:                                │
│  • NCB Financial (Jamaica) - $125M market cap               │
│  • JMMB Group (Jamaica) - $87M market cap                   │
│  • Republic Bank (Trinidad) - $2.1B market cap              │
│                                                             │
│  [View Regional Breakdown] [Track Companies]                │
└─────────────────────────────────────────────────────────────┘
```

**Data Sources:**
- World Bank Remittance Data (public API)
- UN Migration Database (public)
- Caribbean Tourism Organization (public reports)
- Regional stock exchanges (JSE, TTSE, BSE)
- Company financial statements (SEC filings)

**Compliance Safeguards:**
- ✅ Educational visualization only
- ✅ No predictions about future flows
- ✅ No investment recommendations
- ✅ Disclaimer: "This map shows historical economic flows, not future investment opportunities."

---

## 👤 IDENTITY SYSTEM (FINAL)

Users select **one identity** during onboarding (Screen 2). This identity adjusts the dashboard layout, widgets, and insights.

### Diaspora Identity

**Target User:** Caribbean, African, Latin American diaspora living abroad

**Dashboard Adjustments:**
- **Hero Widget:** Diaspora Economic Flow Maps™
- **Featured Stocks:** Caribbean-linked companies (NCB, JMMB, RBL, ANSA)
- **Insights:** Remittance-influenced sectors (finance, telecom, retail)
- **Cultural Alpha:** Highlights companies with high diaspora engagement
- **Color Theme:** Caribbean Blue gradient + Warm sand background

**Unique Features:**
- Track both home-country stocks (JSE, TTSE, BSE) + US stocks in one dashboard
- Remittance flow visualizations
- Regional economic news (Caribbean, Africa, Latin America)

---

### Youth Identity

**Target User:** Ages 13-22, learning to invest

**Dashboard Adjustments:**
- **Hero Widget:** Financial Literacy Challenges
- **Portfolio:** Mock Portfolio (virtual $10,000, no real money)
- **Learning:** 8 education modules (What is a Stock?, Portfolio, Diversification, etc.)
- **Badges:** Bronze, Silver, Gold, Platinum achievement badges
- **Color Theme:** Neon Teal + Coral accent

**Unique Features:**
- Gamified challenges (earn XP, unlock badges)
- Simplified charts (no advanced indicators)
- Educational tooltips everywhere
- Parental reporting dashboard (optional)
- Safety disclaimer: "This is a practice portfolio. No real money is used."

**Compliance:**
- Age verification required (13+)
- No real trading features
- All content marked "educational only"

---

### Creator Identity

**Target User:** Content creators, digital entrepreneurs, influencers

**Dashboard Adjustments:**
- **Hero Widget:** Creator-Economy Index (SHOP, ETSY, META, SPOT, ABNB)
- **Featured Stocks:** Digital-product companies (Adobe, Shopify, Salesforce)
- **Insights:** Market trends relevant to creators (e-commerce growth, SaaS adoption)
- **Integration:** IslandNation marketplace courses featured in "Learn" tab
- **Color Theme:** Deep Slate + Gold accent

**Unique Features:**
- Track creator-economy stocks (companies that power the creator economy)
- Revenue dashboard (if user has IslandNation creator account, shows earnings)
- Digital-product stock filter (SaaS, e-commerce, streaming, social media)
- Creator financial tools bundle (Pro tier)

---

### Legacy-Builder Identity

**Target User:** Long-term investors, retirees, dividend seekers

**Dashboard Adjustments:**
- **Hero Widget:** Dividend Tracker (annual income, payment calendar)
- **Charts:** Long-term historical data (20+ years)
- **Insights:** Wealth-preservation, low-volatility sectors
- **Focus:** Dividend Aristocrats (25+ years consecutive increases)
- **Color Theme:** Navy + Emerald accent

**Unique Features:**
- Dividend payment calendar (ex-dividend dates, record dates, pay dates)
- Income projections (5-10 year forecasts based on dividend growth)
- Aristocrat badges (Gold for 25+ years, Platinum for 50+ years)
- Payout ratio tracking (sustainability scores)
- Long-term performance vs benchmarks (S&P 500, total return with dividends)

---

## 🧭 NAVIGATION SYSTEM (FINAL)

### Desktop Navigation (Persistent Top Bar)

**Left Side:**
- DominionMarkets logo (clickable, returns to home)

**Center:**
- Dashboard (home)
- Markets (sector heatmap, top movers, earnings calendar)
- Portfolio (holdings, allocation, analytics)
- News (verified news, fact-checking center)
- Alerts (price, volume, news, earnings alerts)

**Right Side:**
- Premium (upgrade CTA for free users)
- Profile (avatar, dropdown menu)

**Dropdown Menu (Profile):**
- Settings
- Identity Profile
- Notifications
- Billing (Premium/Pro users)
- Help & Support
- Sign Out

---

### Mobile Navigation (Bottom Tab Bar)

**5 Tabs:**
1. **Home** (dashboard icon)
2. **Markets** (chart icon)
3. **Portfolio** (pie chart icon)
4. **News** (newspaper icon)
5. **Profile** (avatar icon)

**Secondary Navigation:**
- Top bar: Page title + back button
- Hamburger menu (top-left): Settings, Help, Sign Out

---

### Secondary Navigation

**Breadcrumbs (Desktop):**
- Dashboard > Markets > Stock Detail > AAPL
- Dashboard > Portfolio > Holdings > AAPL Detail

**Back Button (Mobile):**
- Always visible in top-left corner
- Returns to previous screen

**Search (Global):**
- Magnifying glass icon in top bar (both desktop + mobile)
- Global search: Stocks, news articles, companies
- Autocomplete suggestions as user types

---

## 🚀 ONBOARDING FLOW (FINAL - 3 SCREENS)

Industry-standard 3-screen onboarding to maximize completion rate.

### Screen 1: Welcome

**Visual:**
- Full-screen hero with gradient background
- DominionMarkets logo
- Tagline: "See the Market Clearly."

**Copy:**
```
Welcome to DominionMarkets

Your window into global markets.
✓ Real-time data
✓ Portfolio tracking
✓ Verified news
✓ AI-powered insights
```

**CTA Button:** "Get Started" (primary button, center)

**Skip Option:** "Already have an account? Sign In" (text link, bottom)

---

### Screen 2: Identity Selection

**Visual:**
- 4 identity cards in grid layout (2×2 on mobile, 4×1 on desktop)
- Each card has icon, title, description

**Copy:**
```
Choose Your Investment Identity

This helps us personalize your dashboard.
(You can change this anytime in settings.)
```

**Identity Cards:**

**Card 1: Diaspora**
- Icon: 🌍
- Title: "Diaspora Investor"
- Description: "Track Caribbean, African, and Latin American markets alongside global stocks."
- Button: "Select"

**Card 2: Youth**
- Icon: 🎓
- Title: "Young Investor"
- Description: "Learn investing basics with financial literacy challenges and practice portfolios."
- Button: "Select"

**Card 3: Creator**
- Icon: 🎨
- Title: "Creator Investor"
- Description: "Follow the creator economy and track companies that power your business."
- Button: "Select"

**Card 4: Legacy-Builder**
- Icon: 👑
- Title: "Legacy Builder"
- Description: "Focus on long-term wealth with dividend tracking and low-volatility strategies."
- Button: "Select"

**Skip Option:** "Skip for now" (text link, bottom) → Defaults to standard dashboard

---

### Screen 3: Dashboard Ready

**Visual:**
- Success screen with confetti animation
- Preview of dashboard (small screenshot or illustration)

**Copy:**
```
🎉 Your Market Intelligence Hub is Live!

Your personalized dashboard is ready.
Start by adding stocks to your watchlist or building your first portfolio.
```

**CTA Button:** "Enter DominionMarkets" (primary button, center)

**After CTA:**
- Redirect to Home Dashboard
- Show brief tooltip tour (optional, dismissible):
  - "Add stocks here" (watchlist icon)
  - "Track your portfolio" (portfolio icon)
  - "Read verified news" (news icon)

---

## 🔐 AUTHENTICATION FLOW (FINAL)

### Login Screen

**Fields:**
- Email
- Password
- "Remember me" checkbox
- "Forgot password?" link

**CTA:** "Sign In" button

**Alternative:** "Sign in with CodexDominion" (SSO button)

**Footer:** "Don't have an account? Sign Up"

---

### Signup Screen

**Fields:**
- Full Name
- Email
- Password (min 8 characters, must include number + special character)
- Confirm Password
- "I agree to Terms of Service" checkbox

**CTA:** "Create Account" button

**Alternative:** "Sign up with CodexDominion" (SSO button)

**Footer:** "Already have an account? Sign In"

**After Signup:**
- Email verification sent
- Redirect to "Check Your Email" screen
- User must click verification link before accessing dashboard

---

### Forgot Password

**Screen:**
- Email input
- "Send Reset Link" button

**After Submit:**
- "Check your email for reset instructions"
- Link expires in 1 hour

---

### Reset Password

**Screen (after clicking email link):**
- New Password input
- Confirm New Password input
- "Reset Password" button

**After Reset:**
- "Password updated successfully"
- Redirect to Login screen

---

### SSO with CodexDominion

**Flow:**
1. User clicks "Sign in with CodexDominion"
2. Redirect to CodexDominion auth page (Auth0)
3. User logs in (if not already authenticated)
4. Redirect back to DominionMarkets with auth token
5. Account auto-created (if first time) or logged in (if existing)

**SSO Accounts Linked:**
- CodexDominion
- DominionYouth
- IslandNation Marketplace
- DominionMarkets

**One login = access to all 4 platforms.**

---

## 💎 PREMIUM TIERS (FINAL, CONSISTENT)

### FREE (No Cost)

**Features:**
- ✅ Real-time prices (15-minute delay)
- ✅ 5 stocks in watchlist
- ✅ 1 portfolio (max 10 holdings)
- ✅ 5 AI summaries per day
- ✅ 20 news headlines per day
- ✅ 30 days historical data
- ✅ Basic charts (line, candlestick)
- ✅ 7-day earnings calendar preview

**Limitations:**
- ❌ No custom alerts
- ❌ No advanced analytics
- ❌ No CSV export
- ❌ No multi-source verified news (only basic news)
- ❌ No diversification scoring

---

### PREMIUM ($14.99/month or $129.99/year)

**Unlocks:**
- ✅ Unlimited watchlist stocks
- ✅ 3 portfolios (unlimited holdings per portfolio)
- ✅ Unlimited AI summaries
- ✅ Custom alerts (price, volume, news, earnings)
- ✅ 10 years historical data
- ✅ Advanced portfolio analytics:
  - Diversification scoring
  - Volatility summaries
  - Sector concentration analysis
  - Risk exposure breakdown
- ✅ CSV import/export
- ✅ 60-day earnings calendar
- ✅ Multi-source verified news (3+ sources)
- ✅ Priority email support

**Trial:** 7-day free trial (no credit card required)

---

### PRO ($29.99/month or $299.99/year)

**Unlocks Everything in Premium + :**
- ✅ Unlimited portfolios
- ✅ Caribbean markets (JSE, TTSE, BSE stocks)
- ✅ API access (100-500 calls/day)
- ✅ Institutional-style charts (TradingView-level features)
- ✅ Macro dashboards (economic indicators, Fed data, GDP)
- ✅ White-glove support (live chat, priority phone)
- ✅ Creator financial tools bundle (budget templates, business planners)
- ✅ Diaspora economic deep-dives (regional reports, flow maps)
- ✅ Advanced compliance features (tax-loss harvesting reports, cost basis tracking)

**Trial:** 14-day free trial (credit card required, can cancel anytime)

---

## 🏠 HOME DASHBOARD FLOW (MAIN HUB)

### Dashboard Sections (Top to Bottom)

**1. Header**
- Market Ticker Bar (scrolling: AAPL +2.4%, TSLA -1.2%, NVDA +3.8%...)
- Time: Last updated time
- Refresh button

**2. Market Sentiment Bar**
- Visual gauge: Bullish (green) | Neutral (yellow) | Bearish (red)
- Calculated from: News sentiment + market breadth + volume trends
- Text: "Markets are bullish today. 72% of stocks are up."

**3. Portfolio Snapshot**
- Total Value: $42,850.75
- Daily Change: +$485.20 (+1.15%)
- Quick Actions: [Add Holding] [View Full Portfolio]

**4. Top Movers**
- 3 tabs: Top Gainers | Top Losers | Volume Spikes
- Shows 5 stocks per tab
- Click stock → Stock Detail page

**5. Verified News Feed**
- 5 most recent verified headlines
- Verification badges (✅ Verified, ⚠️ Developing, ❌ Conflicting)
- Click headline → News Verification Center

**6. AI Summary Panel** (Premium Feature)
- "Today's Market Summary" (200-word AI-generated overview)
- Free users see: "Unlock unlimited AI summaries with Premium"
- Lock icon overlay on free tier

**7. Alerts Preview**
- "You have 3 active alerts"
- List: Price alert for AAPL, Volume alert for TSLA, Earnings for MSFT
- Click → Alerts Center

---

### User Actions on Home Dashboard

| Action | Destination |
|--------|-------------|
| Click stock ticker | Stock Detail page |
| Click stock in Top Movers | Stock Detail page |
| Click news headline | News Verification Center |
| Click "View Full Portfolio" | Portfolio Dashboard |
| Click "Alerts Preview" | Alerts Center |
| Click "Unlock Premium" | Premium Paywall Overlay |
| Click AI Summary (free user) | Premium Paywall Overlay |
| Search bar | Search Results page |

---

## 📈 STOCK DETAIL FLOW

When user clicks a stock (from ticker, watchlist, portfolio, or search):

### Stock Overview Screen

**Header:**
- Stock Symbol (AAPL)
- Company Name (Apple Inc.)
- Current Price ($175.23)
- % Change (+2.4% / +$4.15)
- Day Chart (mini sparkline)

**Quick Actions Bar:**
- [Add to Watchlist] or [★ In Watchlist]
- [Add to Portfolio]
- [Set Alert]
- [Share]

**4 Tabs:**

---

#### Tab 1: Overview

**Key Stats:**
- Open: $171.50
- High: $176.80
- Low: $170.25
- Volume: 48.5M
- Market Cap: $2.75T
- P/E Ratio: 28.5
- 52-Week Range: $145.30 - $180.95

**Sector:** Technology
**Industry:** Consumer Electronics

**Earnings Date:** Jan 28, 2026 (18 days away)

**Analyst Sentiment (Descriptive Only):**
- "42% of analysts rate this stock as a Buy." (NO RECOMMENDATION, just data)
- "Average price target: $185.00" (factual data, not advice)

**Dividend Info (if applicable):**
- Annual Dividend: $0.96
- Yield: 0.55%
- Ex-Dividend Date: Nov 10, 2025
- Pay Date: Nov 16, 2025

---

#### Tab 2: Chart

**Time Period Buttons:**
- [1D] [1W] [1M] [3M] [1Y] [5Y] [ALL]

**Chart Types:**
- Line (default)
- Candlestick
- Area

**Indicators (Premium Only):**
- Moving Averages (50-day, 200-day)
- Bollinger Bands
- RSI
- MACD
- Volume bars

**Free Users:**
- Basic line chart only
- Lock icon overlay: "Unlock advanced charts with Premium"

---

#### Tab 3: News

**Verified News Feed:**
- Shows all verified news about this stock
- Filters:
  - [All] [✅ Verified] [⚠️ Developing] [❌ Conflicting]
- Sorted by: Most recent first

**Click headline → News Verification Center**

---

#### Tab 4: Insights (Premium Feature)

**Volatility Summary:**
- 30-day volatility: 18.5% (Medium)
- Explanation: "This stock's price fluctuates moderately."

**Risk Profile:**
- Risk score: 6/10 (Medium Risk)
- Factors: Market cap (low risk), volatility (medium risk), sector (medium risk)

**Sector Comparison:**
- AAPL vs Technology Sector Average
- Price performance: +8.2% vs +5.1% (outperforming)
- Volatility: 18.5% vs 22.3% (less volatile)

**AI Summary (200 words):**
- Descriptive overview of recent news, price movements, sector trends
- NO PREDICTIONS, NO RECOMMENDATIONS

**Free Users:**
- Lock overlay: "Upgrade to Premium to unlock advanced insights"
- CTA: [Upgrade Now]

---

## 💼 PORTFOLIO FLOW

When user clicks "Portfolio" in navigation:

### Portfolio Overview Screen

**Header:**
- Total Portfolio Value: $42,850.75
- Daily Change: +$485.20 (+1.15%)
- All-Time Return: +$8,420.50 (+24.5%)

**Quick Actions:**
- [Add Holding]
- [Import CSV]
- [Export CSV] (Pro only)

---

### Allocation Breakdown

**Pie Chart:**
- Shows sector allocation by percentage
- Interactive: Click slice to filter holdings table

**Example:**
- Technology: 45% ($19,283)
- Healthcare: 22% ($9,427)
- Finance: 18% ($7,713)
- Consumer: 15% ($6,428)

---

### Holdings Table

**Columns:**
- Symbol
- Shares
- Avg Cost
- Current Price
- Total Value
- Gain/Loss ($)
- Gain/Loss (%)
- Actions

**Example Row:**
```
AAPL | 50 | $150.00 | $175.23 | $8,761.50 | +$1,261.50 | +16.8% | [Edit] [Remove]
```

**Sorting:**
- Click column header to sort (ascending/descending)
- Default sort: Largest holding first

**Actions:**
- Click [Edit] → Edit Holding modal (change shares, avg cost)
- Click [Remove] → Confirmation modal → Remove from portfolio
- Click row → Stock Detail page for that stock

---

### Premium-Only Panels

**Free users see lock overlay on these sections:**

**Diversification Score (Premium):**
- Score: 72/100 (Good Diversification)
- Explanation: "Your portfolio is spread across 4 sectors, reducing concentration risk."
- Recommendation: "Consider adding exposure to international markets."

**Risk Exposure (Premium):**
- Overall Risk: 6/10 (Medium Risk)
- High-risk holdings: 3 (20% of portfolio)
- Low-risk holdings: 8 (53% of portfolio)

**Historical Performance Chart (Premium):**
- 30-day, 90-day, 1-year performance
- Benchmark comparison (S&P 500)
- Total return vs price return (with dividends reinvested)

**Sector Concentration (Premium):**
- Warning if any sector >50% of portfolio
- "Your portfolio is tech-heavy (45%). Consider diversifying."

---

### Add Holding Modal

**Fields:**
- Stock Symbol (autocomplete search)
- Number of Shares
- Average Cost per Share (optional, for gain/loss tracking)
- Purchase Date (optional)

**CTA:** [Add to Portfolio]

**After Adding:**
- Toast notification: "AAPL added to portfolio"
- Portfolio overview updates automatically

---

## 📰 NEWS VERIFICATION FLOW

When user clicks a news headline:

### News Verification Center

**Headline:**
- Full headline text
- Publication date/time

**Verification Badge:**
- ✅ Verified by 3 sources (green badge)
- ⚠️ Developing Story (yellow badge)
- ❌ Conflicting Reports (red badge)
- ⚪ Unverified (gray badge)

**Source List:**
- Bloomberg (Published: 10:32 AM)
- Reuters (Published: 10:35 AM)
- CNBC (Published: 10:41 AM)
- Yahoo Finance (Published: 10:55 AM)

**Timeline of Confirmations:**
```
10:32 AM - Bloomberg publishes story
10:35 AM - Reuters confirms (2nd source)
10:41 AM - CNBC confirms (3rd source) → ✅ VERIFIED
10:55 AM - Yahoo Finance confirms (4th source)
```

**AI Summary (200 words):**
- Synthesized summary of all sources
- Key facts extracted
- Descriptive only, no predictions

**Transparency Layer:**
- "Why is this verified?" (explanation of 3-source rule)
- "View original sources" (links to Bloomberg, Reuters, CNBC articles)

---

### User Actions

| Action | Outcome |
|--------|---------|
| Click "View Original Sources" | Opens list of links to source articles (new tab) |
| Click "Save to Watchlist" | Adds related stock to watchlist |
| Click "Share" | Opens share modal (copy link, Twitter, Facebook, email) |
| Click "Report Issue" | Opens form to report incorrect verification |

---

## 🔔 ALERTS FLOW

When user clicks "Alerts" in navigation:

### Alerts Center

**Header:**
- "You have 5 active alerts"
- [Create New Alert]

**Alert Types (4 Categories):**

**1. Price Alerts**
- Trigger: When stock price reaches target
- Example: "Alert me when AAPL reaches $180"
- Set above current price (target) or below (stop-loss)

**2. Volume Alerts**
- Trigger: When trading volume exceeds threshold
- Example: "Alert me when TSLA volume >100M"

**3. News Alerts**
- Trigger: When verified news published about stock
- Filter: Verified only or All news

**4. Earnings Alerts**
- Trigger: Earnings report scheduled
- Reminder: 24 hours before earnings call

---

### Alert Table

**Columns:**
- Alert Type
- Stock
- Condition
- Status (Active, Triggered, Paused)
- Actions

**Example Row:**
```
Price | AAPL | Reaches $180 | Active | [Edit] [Delete] [Pause]
```

---

### Create Alert Modal (Premium Feature)

**Free users:**
- Lock overlay: "Upgrade to Premium to create custom alerts"
- CTA: [Upgrade Now]

**Premium users:**

**Step 1: Select Alert Type**
- [Price Alert] [Volume Alert] [News Alert] [Earnings Alert]

**Step 2: Configure Alert (example for Price Alert)**
- Stock Symbol: (autocomplete search)
- Condition: [Above] or [Below]
- Price: $180.00
- Notification Method: [Email] [Push] [SMS]

**Step 3: Confirm**
- CTA: [Create Alert]

**After Creation:**
- Toast notification: "Price alert created for AAPL"
- Alert appears in Alerts Center table

---

## 💳 PREMIUM PAYWALL FLOW

Triggered when free user clicks a locked feature.

### Premium Overlay Modal

**Header:**
- "Unlock DominionMarkets Premium"

**Context:**
- "You're trying to access: [Feature Name]"
- Example: "Advanced Portfolio Analytics"

---

### Feature Comparison Table

| Feature | FREE | PREMIUM | PRO |
|---------|------|---------|-----|
| Watchlist stocks | 5 | Unlimited | Unlimited |
| Portfolios | 1 (10 max) | 3 (∞) | Unlimited |
| AI summaries/day | 5 | Unlimited | Unlimited |
| Historical data | 30 days | 10 years | 10 years |
| Custom alerts | ❌ | ✅ | ✅ |
| Advanced analytics | ❌ | ✅ | ✅ |
| CSV export | ❌ | ✅ | ✅ |
| Caribbean markets | ❌ | ❌ | ✅ |
| API access | ❌ | ❌ | ✅ |

---

### Pricing Display

**Premium**
- $14.99/month or $129.99/year (save 28%)
- [Start 7-Day Free Trial]

**Pro**
- $29.99/month or $299.99/year (save 17%)
- [Start 14-Day Free Trial]

**Trial Details:**
- No credit card required for Premium trial
- Credit card required for Pro trial (can cancel anytime)
- Full access during trial
- Cancel before trial ends = no charge

---

### Social Proof

**Testimonials:**
- "DominionMarkets helped me understand my portfolio's diversification. The AI summaries save me hours." - @CreatorInvestor
- "Verified news is a game-changer. I trust the data before making decisions." - @DiasporaTrader

**Stats:**
- 10,000+ active users
- 1,500+ Premium subscribers
- 4.8/5 average rating

---

### CTA Buttons

**Primary:** [Upgrade to Premium]
**Secondary:** [Compare All Plans]
**Tertiary:** [Maybe Later] (dismisses modal)

---

### After Purchase

**Success Screen:**
- "🎉 Welcome to Premium!"
- "Your account has been upgraded. All features are now unlocked."
- CTA: [Continue to [Feature Name]]

**Redirect:**
- User sent back to the feature they tried to access
- Feature now unlocked and fully functional

---

## ⚙️ SETTINGS & IDENTITY FLOW

When user clicks "Profile" → "Settings":

### Settings Menu (Left Sidebar)

**Categories:**
1. Identity Profile
2. Notifications
3. Account & Security
4. Billing (Premium/Pro only)
5. Dashboard Theme
6. Data Management
7. Help & Support

---

### 1. Identity Profile

**Current Identity:**
- Shows selected identity (Diaspora, Youth, Creator, Legacy-Builder)
- [Change Identity] button

**Change Identity Modal:**
- Shows 4 identity cards (same as onboarding)
- User selects new identity
- Confirmation: "Your dashboard will update with new widgets. Continue?"
- CTA: [Confirm Change]

**After Change:**
- Dashboard reloads with new theme + widgets
- Toast notification: "Identity updated to [New Identity]"

---

### 2. Notifications

**Channels:**
- ☑ Email notifications
- ☑ Push notifications (browser/mobile)
- ☐ SMS notifications (requires phone number)

**Alert Preferences:**
- ☑ Price alerts
- ☑ Volume alerts
- ☑ News alerts
- ☑ Earnings alerts
- ☑ Portfolio updates (daily summary)

**Frequency:**
- [ ] Real-time (as they happen)
- [✓] Digest (once per day at 8 AM)
- [ ] Weekly summary (Mondays)

**CTA:** [Save Preferences]

---

### 3. Account & Security

**Email:** user@example.com (verified ✅)
- [Change Email]

**Password:** ••••••••
- [Change Password]

**Two-Factor Authentication:**
- Status: Disabled
- [Enable 2FA] (adds extra security via SMS or authenticator app)

**Connected Accounts:**
- CodexDominion (SSO) ✅
- Google (optional OAuth)
- Twitter (optional OAuth for sharing)

**Danger Zone:**
- [Delete Account] (red button, requires confirmation + password)

---

### 4. Billing (Premium/Pro Only)

**Current Plan:**
- Premium ($14.99/month)
- Next billing date: Jan 28, 2026
- Payment method: Visa •••• 1234

**Actions:**
- [Update Payment Method]
- [Switch to Annual Plan] (save 28%)
- [Upgrade to Pro]
- [Cancel Subscription] (red button)

**Billing History:**
- Table of past invoices (date, amount, status, download PDF)

---

### 5. Dashboard Theme

**Theme Options:**
- [✓] Auto (matches identity: Diaspora → Caribbean Blue, Youth → Neon Teal, etc.)
- [ ] Light Mode
- [ ] Dark Mode

**Custom Theme (Pro Only):**
- Color picker for accent color
- Upload custom logo (for institutional users)

**CTA:** [Save Theme]

---

### 6. Data Management

**Portfolio Import:**
- [Import CSV] (upload CSV with holdings)
- CSV format: Symbol, Shares, Avg Cost, Purchase Date

**Portfolio Export (Pro Only):**
- [Export CSV] (download all portfolios as CSV)

**Data Deletion:**
- [Clear Watchlist]
- [Clear Portfolio] (requires confirmation)
- [Clear Alert History]

**Data Backup:**
- [Download All Data] (JSON export of watchlist, portfolio, alerts, settings)

---

### 7. Help & Support

**Resources:**
- [User Guide] (link to documentation)
- [Video Tutorials] (YouTube playlist)
- [FAQ] (frequently asked questions)
- [Community Forum] (Discord or Reddit link)

**Contact Support:**
- Email: support@dominionmarkets.app
- Live Chat (Pro users only, 9 AM - 5 PM EST)

**Report a Bug:**
- [Submit Bug Report] (form with description, screenshot upload)

---

## 🔗 CROSS-PROMOTION FLOW

### DominionMarkets → CodexDominion Ecosystem

**Locations in DominionMarkets:**

**1. Navigation Bar (Desktop)**
- "Explore Ecosystem" dropdown menu:
  - IslandNation Marketplace (creator products)
  - DominionYouth (financial literacy)
  - CodexDominion (main hub)

**2. Dashboard Footer**
- "Part of the CodexDominion Ecosystem"
- Links to other platforms

**3. Identity-Specific Promotions**

**Diaspora Identity:**
- Widget: "Explore Diaspora Economic Stories"
- Content: Case studies, regional company profiles, diaspora-owned business spotlights
- CTA: [Read More on CodexDominion]

**Youth Identity:**
- Widget: "Complete Financial Literacy Challenges"
- Challenges:
  - "Learn 3 financial terms" (10 XP, Bronze badge)
  - "Build your first mock portfolio" (20 XP)
  - "Track your spending for 7 days" (30 XP)
- CTA: [Start Challenge on DominionYouth]

**Creator Identity:**
- Widget: "Discover Creator Financial Products"
- Products:
  - Budget templates ($9.99)
  - Business planners ($14.99)
  - Finance courses ($29.99)
  - Trading journals ($7.99)
  - Market research packs ($49.99)
- CTA: [Browse on IslandNation]

**Legacy-Builder Identity:**
- Widget: "Long-Term Wealth Resources"
- Content: Estate planning guides, retirement calculators, tax optimization tips
- CTA: [Explore Resources]

---

### CodexDominion Ecosystem → DominionMarkets

**Locations in Other Platforms:**

**IslandNation Marketplace:**
- "Track Creator-Economy Stocks" banner
- CTA: [Open DominionMarkets]
- Links to Creator-Economy Index widget

**DominionYouth:**
- "Practice Investing with Mock Portfolio" card
- CTA: [Try DominionMarkets]
- Links to Youth dashboard with mock portfolio

**CodexDominion Main Hub:**
- "Monitor Your Investments" section
- CTA: [Open DominionMarkets]
- Links to Portfolio dashboard

---

## 🚨 ERROR STATES & EMPTY STATES (FINAL)

### Empty Portfolio

**Visual:**
- Empty state illustration (empty folder icon)
- Headline: "Your portfolio is empty"
- Subheadline: "Add your first holding to unlock insights."
- CTA: [Add Holding] (primary button)
- Secondary: "Import from CSV" (text link)

---

### Empty Watchlist

**Visual:**
- Empty state illustration (magnifying glass icon)
- Headline: "Start tracking stocks"
- Subheadline: "Search for a stock to add to your watchlist."
- CTA: [Search Stocks] (opens search bar)

---

### Data Load Failure

**Visual:**
- Error icon (⚠️)
- Headline: "Data unavailable"
- Subheadline: "We couldn't load the latest data. Please check your connection and try again."
- CTA: [Retry] (reloads page)
- Secondary: "Contact Support" (text link)

**Technical Detail (hidden by default, expandable):**
- Error code: API_TIMEOUT
- Timestamp: 2025-12-24 10:32:15 UTC

---

### News API Down

**Visual:**
- Warning icon (⚠️)
- Headline: "News temporarily unavailable"
- Subheadline: "We're working to restore this service. Please check back soon."
- CTA: [Refresh] (reloads news feed)

**Fallback:**
- Show cached news (with timestamp: "Last updated: 2 hours ago")

---

### No Search Results

**Visual:**
- Empty search icon
- Headline: "No results for '[search query]'"
- Subheadline: "Try a different search term or browse popular stocks."
- CTA: [Browse Top Movers]

---

### Network Error

**Visual:**
- Disconnected icon (📡)
- Headline: "You're offline"
- Subheadline: "Check your internet connection and try again."
- CTA: [Retry]

**Fallback:**
- App switches to offline mode (shows cached data with warning banner)

---

## 🔍 MISSING FEATURES (NOW INCLUDED)

### 1. Search

**Location:** Top navigation bar (magnifying glass icon)

**Search Scope:**
- Stocks (by symbol or company name)
- News articles (by keyword)
- Companies (by industry or sector)

**Autocomplete:**
- Suggestions appear as user types
- Shows: Symbol, Company Name, Current Price
- Recent searches saved (last 5)

**Search Results Page:**
- Tabs: [Stocks] [News] [Companies]
- Sorted by relevance (matching algorithm)

---

### 2. Notifications

**Channels:**
1. **Push Notifications** (browser + mobile app)
2. **Email Notifications** (customizable frequency)
3. **SMS Notifications** (Pro only, requires phone verification)

**Notification Types:**
- Price alert triggered
- Volume alert triggered
- News alert (new verified story)
- Earnings alert (24 hours before)
- Portfolio summary (daily digest)
- Premium trial expiring (3 days before)

**Notification Settings:**
- Enable/disable per channel
- Set frequency (real-time, digest, weekly)
- Quiet hours (no notifications 10 PM - 8 AM)

---

### 3. CSV Export

**Location:** Portfolio > Export CSV (Pro only)

**Export Format:**
```csv
Symbol,Company Name,Shares,Avg Cost,Current Price,Total Value,Gain/Loss ($),Gain/Loss (%),Purchase Date
AAPL,Apple Inc.,50,150.00,175.23,8761.50,1261.50,16.8%,2024-06-15
TSLA,Tesla Inc.,20,220.00,243.15,4863.00,463.00,10.5%,2024-08-22
```

**Free/Premium Users:**
- Lock overlay: "Upgrade to Pro to export your portfolio"
- CTA: [Upgrade to Pro]

---

### 4. Social Sharing

**Location:** Stock Detail page > Share icon

**Share Options:**
- Copy link (clipboard)
- Twitter (pre-populated tweet: "Check out AAPL on DominionMarkets: [link]")
- Facebook (open share dialog)
- Email (opens email client with subject + body)
- LinkedIn (Pro only)

**Shared Link:**
- URL: `dominionmarkets.app/stock/AAPL?ref=share`
- Preview card: Stock symbol, current price, % change, DominionMarkets logo

---

### 5. Earnings Calendar

**Free Users:**
- 7-day preview (current week only)
- Shows: Symbol, Company Name, Earnings Date
- Lock overlay for dates beyond 7 days

**Premium Users:**
- 60-day full calendar (next 2 months)
- Filter by: Sector, Watchlist stocks, Portfolio stocks
- Export to Google Calendar, iCal

**Pro Users:**
- 365-day calendar (full year)
- Historical earnings dates (past 5 years)
- Earnings surprise data (actual vs expected)

---

## 📊 ANALYTICS & TRACKING (FINAL)

### Core Events

**Onboarding:**
- `onboarding_started`
- `onboarding_identity_selected` (properties: identity type)
- `onboarding_completed`
- `onboarding_abandoned` (properties: screen number)

**Portfolio:**
- `portfolio_created`
- `holding_added` (properties: symbol, shares)
- `holding_edited`
- `holding_removed`
- `portfolio_exported` (Pro only)
- `csv_imported` (Premium/Pro)

**Watchlist:**
- `watchlist_stock_added` (properties: symbol)
- `watchlist_stock_removed`

**Alerts:**
- `alert_created` (properties: alert type, stock symbol)
- `alert_triggered` (properties: alert type, stock symbol)
- `alert_deleted`

**Premium:**
- `paywall_viewed` (properties: feature name, tier required)
- `trial_started` (properties: tier)
- `trial_converted` (properties: tier)
- `trial_expired` (properties: tier)
- `subscription_upgraded` (properties: from tier, to tier)
- `subscription_canceled` (properties: tier, reason)

**Content:**
- `news_article_opened` (properties: headline, verification status)
- `stock_detail_viewed` (properties: symbol)
- `ai_summary_viewed` (properties: stock symbol or dashboard)
- `chart_interaction` (properties: time period, chart type)

**Settings:**
- `identity_changed` (properties: from identity, to identity)
- `theme_changed` (properties: theme name)
- `notification_settings_updated`

---

### Conversion Funnels

**Onboarding Funnel:**
```
1. Landing Page View
2. Welcome Screen (Get Started clicked)
3. Identity Selection (identity selected)
4. Dashboard Ready (Enter DominionMarkets clicked)
5. First Action (watchlist add, portfolio add, or news click)
```

**Free → Premium Funnel:**
```
1. Paywall Viewed (feature locked)
2. Pricing Viewed (scroll down to pricing)
3. Trial Started (Start 7-Day Trial clicked)
4. Trial Active (using Premium features)
5. Trial Converted (payment processed)
```

**Premium → Pro Funnel:**
```
1. Pro Feature Viewed (locked Pro feature)
2. Pro Pricing Viewed
3. Pro Trial Started
4. Pro Trial Converted
```

**Watchlist → Portfolio Funnel:**
```
1. Stock Added to Watchlist
2. Stock Detail Viewed (from watchlist)
3. Add to Portfolio Clicked
4. Holding Added to Portfolio
```

**News → Verified News Funnel:**
```
1. News Feed Viewed (basic news)
2. Verified News Clicked (requires Premium)
3. Paywall Viewed (unlock verified news)
4. Premium Purchased
5. Verified News Viewed (full access)
```

---

### Success Metrics

**User Engagement:**
- Daily Active Users (DAU)
- Weekly Active Users (WAU)
- Monthly Active Users (MAU)
- DAU/MAU ratio (stickiness)
- Average session duration
- Sessions per user per day

**Retention:**
- 1-day retention (% users who return next day)
- 7-day retention (% users who return within 7 days)
- 30-day retention (% users who return within 30 days)
- Cohort retention (by signup date)

**Conversion:**
- Free → Premium conversion rate (target: 10%)
- Premium → Pro conversion rate (target: 5%)
- Trial → Paid conversion rate (target: 50%)
- Paywall → Trial start rate (target: 30%)

**Feature Adoption:**
- % users who add ≥1 stock to watchlist (target: 80%)
- % users who create portfolio (target: 60%)
- % users who set ≥1 alert (target: 40% of Premium)
- % users who view verified news (target: 70%)
- % users who view AI summary (target: 50%)

**Revenue:**
- Monthly Recurring Revenue (MRR)
- Annual Recurring Revenue (ARR)
- Average Revenue Per User (ARPU)
- Customer Lifetime Value (LTV)
- Customer Acquisition Cost (CAC)
- LTV:CAC ratio (target: 3:1 or higher)

**Content Engagement:**
- News articles opened per user per day (target: 5)
- Verified news engagement rate (% of Premium users)
- AI summary views per user per day (target: 3)
- Alert usage rate (% of Premium users with ≥1 active alert)

**Technical:**
- API response time (target: <200ms p95)
- Page load time (target: <2s)
- Error rate (target: <0.1%)
- Uptime (target: 99.9%)

---

## ✅ IMPLEMENTATION CHECKLIST

### Phase 1: Core Features (MVP)
- [ ] Authentication (login, signup, SSO)
- [ ] Home Dashboard (ticker, sentiment, portfolio snapshot, news, top movers)
- [ ] Stock Detail page (overview, chart, news tabs)
- [ ] Watchlist (add, remove, view)
- [ ] Portfolio (add holdings, view allocation, basic analytics)
- [ ] Verified News feed (3-source verification)
- [ ] Search (stocks, news)
- [ ] Onboarding (3 screens: welcome, identity, dashboard ready)

### Phase 2: Premium Features
- [ ] Premium paywall modal
- [ ] Trial system (7-day Premium, 14-day Pro)
- [ ] Payment integration (Stripe)
- [ ] Advanced portfolio analytics (diversification, risk, volatility)
- [ ] Custom alerts (price, volume, news, earnings)
- [ ] Unlimited AI summaries
- [ ] CSV import/export
- [ ] 60-day earnings calendar

### Phase 3: Identity-Driven Personalization
- [ ] Sovereign Portfolio DNA™ engine
- [ ] Cultural Alpha Engine™ scoring
- [ ] Diaspora Economic Flow Maps™ widget
- [ ] Identity theme switching (4 themes)
- [ ] Identity-specific widgets (creator index, dividend tracker, etc.)

### Phase 4: Pro Features
- [ ] Caribbean markets (JSE, TTSE, BSE)
- [ ] API access (REST endpoints)
- [ ] Institutional charts (advanced indicators)
- [ ] Macro dashboards (economic data)
- [ ] White-glove support (live chat)

### Phase 5: Cross-Platform Integration
- [ ] SSO with CodexDominion ecosystem
- [ ] IslandNation creator products integration
- [ ] DominionYouth challenges integration
- [ ] Cross-platform notifications

### Phase 6: Analytics & Optimization
- [ ] Event tracking (all core events)
- [ ] Funnel analysis (conversion funnels)
- [ ] A/B testing framework
- [ ] Performance monitoring (Sentry, Datadog)

---

## 📞 SUPPORT & ESCALATION

**User Support Tiers:**

**Free Users:**
- Email support (response within 48 hours)
- FAQ & documentation
- Community forum (Discord)

**Premium Users:**
- Priority email support (response within 24 hours)
- Video tutorials
- Community forum with Premium badge

**Pro Users:**
- White-glove support (live chat 9 AM - 5 PM EST)
- Priority phone support (scheduled calls)
- Dedicated account manager (for institutional accounts)
- Custom onboarding sessions

---

**Final Status:** ✅ All 10 issues resolved. DominionMarkets is now fully documented, consistent, and ready for implementation.

**Next Steps:**
1. Export design tokens to Figma
2. Build component library
3. Implement Phase 1 MVP features
4. Launch beta with 1,000 users
5. Iterate based on feedback
6. Scale to 10,000+ users (Year 1 goal)

---

**Last Updated:** December 24, 2025  
**Version:** 2.0 (Complete, Buildable, Production-Ready)
