# SECTION 18 — SYSTEM DEPENDENCIES & ARCHITECTURE

**DominionMarkets Platform Architecture**  
Version 1.0 | December 24, 2025

---

## Overview

DominionMarkets is built as a **modular, service-oriented platform** that integrates:

- ✅ Real-time market data
- ✅ Verified news & fact-checking
- ✅ Identity-aware insights (Diaspora/Youth/Creator/Legacy)
- ✅ Portfolio management & analytics
- ✅ Real-time alerts & notifications
- ✅ Premium billing & subscription management
- ✅ Cross-ecosystem connections (Codex Dominion integration)

---

## System Architecture Diagram

```
Frontend (Web + Mobile)
        |
        v
Backend API Gateway
        |
        |-- Identity Service
        |-- Portfolio Service
        |-- Markets Service
        |-- News Verification Engine
        |-- Alerts Service
        |-- Analytics Engine
        |-- Cultural Alpha Engine™
        |-- Sovereign Portfolio DNA™
        |-- Billing Service
        |-- Cross-Promotion Engine
        |
        v
External Providers
        |-- Stock Data Provider
        |-- News Aggregation Pipeline
        |-- Earnings Calendar Provider
        |-- Payment Processor
        |-- CodexDominion SSO
```

---

## Document Structure

This document defines:
1. **Core Services** — Essential platform functionality
2. **Supporting Services** — Infrastructure & utilities
3. **External Dependencies** — Third-party APIs & data sources
4. **Data Flows** — How information moves through the system
5. **Identity Integration** — How identity affects all services
6. **Premium Integration** — Tier-based feature access
7. **Reliability Principles** — Fault tolerance & graceful degradation

---

## 18.1 Core Services

### 18.1.1 Market Data Service

**Purpose**: Real-time and historical market data aggregation

**Responsibilities**:
- Fetch real-time stock quotes (price, volume, change)
- Historical price data (daily, intraday)
- Market movers (gainers, losers, volume spikes)
- Sector performance & heatmaps
- Earnings calendar
- Market hours detection

**Technology Stack**:
- Next.js API Routes (`/api/markets/*`)
- External APIs: Alpha Vantage, Polygon, IEX Cloud
- Redis caching (5-minute TTL for quotes)
- WebSocket for real-time updates (future)

**Endpoints**:
```typescript
GET /api/markets/quote?symbol=AAPL
GET /api/markets/movers?type=gainers|losers
GET /api/markets/heatmap?sector=all
GET /api/markets/earnings?date=2025-12-24
GET /api/markets/history?symbol=AAPL&range=1M
```

**Data Models**:
```typescript
interface StockQuote {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  marketCap: number;
  timestamp: Date;
}

interface MarketMover {
  symbol: string;
  name: string;
  price: number;
  changePercent: number;
  volume: number;
  sector: string;
}

interface EarningsEvent {
  symbol: string;
  company: string;
  date: Date;
  time: 'BMO' | 'AMC' | 'TBD';
  estimate: number | null;
  actual: number | null;
}
```

**Caching Strategy**:
- Real-time quotes: 5 minutes (market hours), 1 hour (after hours)
- Historical data: 24 hours
- Earnings calendar: 6 hours
- Movers list: 15 minutes

**Error Handling**:
- Rate limit exceeded → Show cached data + warning
- API down → Fallback to secondary provider
- Invalid symbol → Return 404 with suggestion API
- Network timeout → Show TimeoutError component

---

### 18.1.2 News Verification Service

**Purpose**: Curated, fact-checked financial news with source credibility

**Responsibilities**:
- Fetch news articles from trusted sources
- Fact-checking via FactCheck.org, Snopes, PolitiFact
- Source credibility scoring (0-100)
- Related news clustering
- Bias detection & labeling
- Timeline view for developing stories

**Technology Stack**:
- Next.js API Routes (`/api/news/*`)
- External APIs: NewsAPI, Benzinga, Financial Modeling Prep
- Fact-checking APIs: FactCheck.org, ClaimReview schema
- PostgreSQL for news archive
- Elasticsearch for full-text search (future)

**Endpoints**:
```typescript
GET /api/news/feed?symbol=AAPL&limit=20
GET /api/news/verify?articleId=123
GET /api/news/sources?verified=true
GET /api/news/timeline?symbol=TSLA&days=7
GET /api/news/related?articleId=123
```

**Data Models**:
```typescript
interface NewsArticle {
  id: string;
  title: string;
  summary: string;
  content: string;
  source: NewsSource;
  relatedSymbols: string[];
  publishedAt: Date;
  verificationStatus: 'verified' | 'unverified' | 'disputed';
  credibilityScore: number; // 0-100
  biasLabel: 'neutral' | 'left' | 'right' | 'center' | null;
  factChecks: FactCheck[];
}

interface NewsSource {
  id: string;
  name: string;
  domain: string;
  trustScore: number; // 0-100
  isVerified: boolean;
  category: 'mainstream' | 'financial' | 'independent';
}

interface FactCheck {
  claim: string;
  verdict: 'true' | 'false' | 'mixed' | 'unverified';
  source: string; // FactCheck.org, Snopes, etc.
  explanation: string;
  url: string;
}
```

**Verification Flow**:
1. Article ingested from source
2. Extract key claims using NLP
3. Query fact-checking APIs
4. Calculate credibility score (source trust + fact-checks)
5. Label bias using Media Bias/Fact Check database
6. Store with verification metadata

**Error Handling**:
- Fact-check API down → Show article with "Verification unavailable"
- Low credibility score → Show warning badge
- Disputed claims → Show red flag with explanation
- No sources available → Show NoSourcesEmpty state

---

### 18.1.3 Identity Service

**Purpose**: User identity management with Diaspora/Youth/Creator/Legacy profiles

**Responsibilities**:
- Identity selection & persistence
- Identity-specific messaging (loading, empty, errors)
- Identity-aware recommendations
- Identity switching with data migration
- Identity profile customization

**Technology Stack**:
- Next.js API Routes (`/api/identity/*`)
- PostgreSQL for user profiles
- Redis for session identity cache
- Context API for frontend identity state

**Endpoints**:
```typescript
GET /api/identity/current
POST /api/identity/select
GET /api/identity/preferences
PUT /api/identity/preferences
GET /api/identity/recommendations?type=stocks|news
```

**Data Models**:
```typescript
type IdentityType = 'diaspora' | 'youth' | 'creator' | 'legacy';

interface Identity {
  id: string;
  userId: string;
  type: IdentityType;
  displayName: string;
  description: string;
  preferences: IdentityPreferences;
  createdAt: Date;
  lastActive: Date;
}

interface IdentityPreferences {
  defaultView: 'dashboard' | 'markets' | 'portfolio';
  favoriteSymbols: string[];
  watchlist: string[];
  alertSettings: AlertPreferences;
  newsCategories: string[];
  riskTolerance: 'conservative' | 'moderate' | 'aggressive';
}

interface IdentityRecommendation {
  type: 'stock' | 'news' | 'insight';
  title: string;
  description: string;
  reasoning: string; // Why this fits identity
  actionLabel: string;
  actionUrl: string;
}
```

**Identity Characteristics**:

**Diaspora**:
- Focus: Caribbean, African, international markets
- Tone: Community-focused, cultural awareness
- Recommendations: Emerging markets, diaspora-friendly companies
- Loading message: "Loading regional insights…"
- Empty message: "Add your first Caribbean or international stock"

**Youth**:
- Focus: Learning, growth stocks, crypto, tech
- Tone: Educational, encouraging, beginner-friendly
- Recommendations: Growth stocks, ETFs, educational content
- Loading message: "Loading your learning dashboard…"
- Empty message: "Start learning with your first stock"

**Creator**:
- Focus: Creator economy, platform stocks, influencer brands
- Tone: Entrepreneurial, trend-aware, platform-focused
- Recommendations: Creator platforms (META, GOOG, SPOT), brand stocks
- Loading message: "Loading creator-economy data…"
- Empty message: "Add a creator-economy stock"

**Legacy**:
- Focus: Dividends, blue chips, long-term value
- Tone: Conservative, wealth-building, generational
- Recommendations: Dividend aristocrats, S&P 500, bonds
- Loading message: "Loading long-term indicators…"
- Empty message: "Add a dividend stock for long-term growth"

**Error Handling**:
- Identity switch failed → Rollback to previous identity
- Invalid identity type → Default to Diaspora
- Profile load error → Use default preferences

---

### 18.1.4 Portfolio Service

**Purpose**: Portfolio tracking, analytics, and performance monitoring

**Responsibilities**:
- Portfolio CRUD operations
- Position tracking (shares, cost basis, current value)
- Gain/loss calculations (total, daily, percent)
- Sector allocation analysis
- Performance metrics (return, volatility, Sharpe ratio)
- Multi-portfolio support (Premium+)
- CSV export (Premium+)

**Technology Stack**:
- Next.js API Routes (`/api/portfolio/*`)
- PostgreSQL for portfolio data
- Redis for portfolio summary cache
- Background jobs for daily snapshots

**Endpoints**:
```typescript
GET /api/portfolio/list
GET /api/portfolio/:id
POST /api/portfolio
PUT /api/portfolio/:id
DELETE /api/portfolio/:id
GET /api/portfolio/:id/holdings
POST /api/portfolio/:id/holdings
PUT /api/portfolio/:id/holdings/:holdingId
DELETE /api/portfolio/:id/holdings/:holdingId
GET /api/portfolio/:id/analytics (Premium)
GET /api/portfolio/:id/export (Premium)
```

**Data Models**:
```typescript
interface Portfolio {
  id: string;
  userId: string;
  name: string;
  description: string | null;
  isDefault: boolean;
  createdAt: Date;
  updatedAt: Date;
}

interface Holding {
  id: string;
  portfolioId: string;
  symbol: string;
  shares: number;
  costBasis: number; // Average cost per share
  purchaseDate: Date;
  currentPrice: number; // Updated from market data
  currentValue: number; // shares × currentPrice
  totalGain: number; // currentValue - (shares × costBasis)
  totalGainPercent: number;
  dayGain: number;
  dayGainPercent: number;
  sector: string;
}

interface PortfolioSummary {
  totalValue: number;
  totalCost: number;
  totalGain: number;
  totalGainPercent: number;
  dayGain: number;
  dayGainPercent: number;
  holdingsCount: number;
  sectorAllocation: SectorAllocation[];
}

interface SectorAllocation {
  sector: string;
  value: number;
  percent: number;
  holdings: number;
}
```

**Analytics (Premium)**:
- Risk metrics (beta, standard deviation, Sharpe ratio)
- Performance vs. benchmarks (S&P 500, Nasdaq)
- Correlation matrix
- Drawdown analysis
- Tax loss harvesting opportunities

**Error Handling**:
- Invalid symbol → Reject with suggestion
- Negative shares → Validation error
- Cost basis missing → Require before adding
- Market data unavailable → Use last known price
- Premium feature on Free tier → Show PremiumGate

---

### 18.1.5 Alerts Service

**Purpose**: Real-time price alerts, news alerts, earnings reminders

**Responsibilities**:
- Alert creation & management
- Real-time price monitoring (WebSocket or polling)
- Alert triggering logic
- Push notifications (web, mobile)
- Email notifications
- Alert history & analytics (Premium)

**Technology Stack**:
- Next.js API Routes (`/api/alerts/*`)
- PostgreSQL for alert definitions
- Redis pub/sub for real-time triggering
- Background worker for price monitoring
- Web Push API for notifications
- SendGrid/AWS SES for email

**Endpoints**:
```typescript
GET /api/alerts/list
GET /api/alerts/:id
POST /api/alerts
PUT /api/alerts/:id
DELETE /api/alerts/:id
GET /api/alerts/history (Premium)
POST /api/alerts/:id/test
```

**Data Models**:
```typescript
type AlertType = 'price' | 'news' | 'earnings' | 'volume';
type AlertCondition = 'above' | 'below' | 'change_percent';

interface Alert {
  id: string;
  userId: string;
  symbol: string;
  type: AlertType;
  condition: AlertCondition;
  value: number;
  isActive: boolean;
  notifyPush: boolean;
  notifyEmail: boolean;
  createdAt: Date;
  triggeredAt: Date | null;
  triggerCount: number;
}

interface AlertTrigger {
  id: string;
  alertId: string;
  triggeredAt: Date;
  price: number;
  message: string;
  wasDelivered: boolean;
}
```

**Alert Logic**:
```typescript
// Price above threshold
if (currentPrice > alert.value && alert.condition === 'above') {
  triggerAlert(alert);
}

// Price below threshold
if (currentPrice < alert.value && alert.condition === 'below') {
  triggerAlert(alert);
}

// Percent change
if (Math.abs(changePercent) > alert.value && alert.condition === 'change_percent') {
  triggerAlert(alert);
}
```

**Notification Channels**:
1. **Web Push** — Browser notifications (requires permission)
2. **Email** — Sent to user email
3. **In-app** — Badge on Alerts page
4. **Mobile** — Push to iOS/Android app (future)

**Error Handling**:
- Invalid alert value → Validation error
- Symbol not found → Reject with suggestion
- Push permission denied → Fall back to email
- Email delivery failed → Retry 3 times, log failure
- Alert limit reached (Free: 5, Premium: 50) → Show upgrade prompt

---

### 18.1.6 Cultural Alpha Engine™

**Purpose**: Identity-specific market insights and cultural context analysis

**Responsibilities**:
- Generate identity-aware market insights
- Analyze cultural trends affecting markets
- Track diaspora-relevant companies and sectors
- Youth-focused growth opportunity identification
- Creator economy trend analysis
- Legacy wealth-building strategies
- Cultural event impact analysis (holidays, celebrations)
- Regional market intelligence

**Technology Stack**:
- Next.js API Routes (`/api/cultural-alpha/*`)
- Machine learning models (TensorFlow.js)
- PostgreSQL for insight storage
- Redis for cached insights
- External APIs: Google Trends, Twitter API (cultural sentiment)

**Endpoints**:
```typescript
GET /api/cultural-alpha/insights?identity=diaspora
GET /api/cultural-alpha/trending?identity=youth
GET /api/cultural-alpha/opportunities?identity=creator
GET /api/cultural-alpha/events?region=caribbean
GET /api/cultural-alpha/sectors?identity=legacy
```

**Data Models**:
```typescript
interface CulturalInsight {
  id: string;
  identity: IdentityType;
  category: 'market' | 'trend' | 'event' | 'opportunity';
  title: string;
  description: string;
  symbols: string[]; // Related stocks
  regions: string[]; // Caribbean, Africa, etc.
  impact: 'low' | 'medium' | 'high';
  timeframe: 'short' | 'medium' | 'long';
  confidence: number; // 0-100
  sources: InsightSource[];
  publishedAt: Date;
  expiresAt: Date;
}

interface InsightSource {
  type: 'news' | 'social' | 'financial' | 'academic';
  title: string;
  url: string;
  credibilityScore: number;
}

interface CulturalTrend {
  trend: string;
  identity: IdentityType;
  growthRate: number; // % growth
  relatedSymbols: string[];
  description: string;
  chartData: TrendDataPoint[];
}
```

**Identity-Specific Insights**:

**Diaspora**:
- Caribbean economic developments (Jamaica, Trinidad, Barbados)
- African market opportunities (Nigeria, Ghana, South Africa)
- Diaspora remittance trends
- Pan-African company growth
- Regional banking sector analysis
- Tourism & hospitality trends

**Youth**:
- Emerging tech trends (AI, blockchain, green tech)
- Gig economy opportunities
- Student loan impact on markets
- Gen Z spending patterns
- Social media platform growth
- Gaming & esports sector

**Creator**:
- Creator platform earnings trends
- Influencer brand partnerships
- Platform monetization changes
- Content creation tool providers
- Creator economy ETFs
- Brand collaboration opportunities

**Legacy**:
- Dividend safety analysis
- Multi-generational wealth strategies
- Estate planning considerations
- Blue chip stability indicators
- Recession-resistant sectors
- Long-term compound growth opportunities

**ML Models**:
```typescript
// Cultural sentiment analysis
interface SentimentModel {
  analyzeText(text: string): Promise<{
    sentiment: 'positive' | 'negative' | 'neutral';
    confidence: number;
    culturalContext: string[];
  }>;
}

// Trend prediction
interface TrendPredictor {
  predictTrend(historicalData: TrendDataPoint[]): Promise<{
    prediction: 'rising' | 'falling' | 'stable';
    confidence: number;
    factors: string[];
  }>;
}
```

**Caching Strategy**:
- Insights: 6 hours (updated 4x daily)
- Trends: 1 hour (market hours), 12 hours (after hours)
- Events: 24 hours
- Opportunities: 4 hours

**Error Handling**:
- ML model unavailable → Use cached insights
- API rate limit → Show stale data with timestamp
- Invalid identity → Default to Diaspora insights
- No insights available → Show "Check back soon" message

---

### 18.1.7 Sovereign Portfolio DNA™

**Purpose**: Identity-aware portfolio construction and optimization

**Responsibilities**:
- Generate identity-aligned portfolio recommendations
- Portfolio risk scoring based on identity preferences
- Sector allocation suggestions (identity-specific)
- Rebalancing recommendations
- Tax-efficient strategies by identity
- Diversification analysis
- Identity-aware asset allocation models

**Technology Stack**:
- Next.js API Routes (`/api/portfolio-dna/*`)
- Modern Portfolio Theory (MPT) algorithms
- Monte Carlo simulations for risk analysis
- PostgreSQL for portfolio models
- Redis for calculation cache

**Endpoints**:
```typescript
GET /api/portfolio-dna/recommendations?identity=diaspora&risk=moderate
POST /api/portfolio-dna/analyze
GET /api/portfolio-dna/allocation?identity=youth
GET /api/portfolio-dna/rebalance?portfolioId=123
GET /api/portfolio-dna/risk-score?portfolioId=123
```

**Data Models**:
```typescript
interface PortfolioDNA {
  id: string;
  userId: string;
  identity: IdentityType;
  riskTolerance: 'conservative' | 'moderate' | 'aggressive';
  timeHorizon: 'short' | 'medium' | 'long'; // < 5y, 5-10y, > 10y
  targetAllocation: AllocationModel;
  currentAllocation: AllocationModel;
  rebalanceNeeded: boolean;
  recommendations: PortfolioRecommendation[];
  riskMetrics: RiskMetrics;
}

interface AllocationModel {
  stocks: number; // % allocation
  bonds: number;
  cash: number;
  alternatives: number;
  international: number;
  sectors: SectorAllocation[];
}

interface PortfolioRecommendation {
  action: 'buy' | 'sell' | 'hold' | 'rebalance';
  symbol: string;
  shares: number;
  reasoning: string;
  identityAlignment: number; // 0-100
  expectedReturn: number;
  risk: 'low' | 'medium' | 'high';
  timeframe: string;
}

interface RiskMetrics {
  portfolioBeta: number;
  volatility: number; // Standard deviation
  sharpeRatio: number;
  maxDrawdown: number;
  correlationScore: number; // Diversification measure
  identityFitScore: number; // 0-100
}
```

**Identity-Specific Allocation Models**:

**Diaspora (Moderate Risk)**:
```typescript
{
  stocks: 60,
  bonds: 25,
  cash: 10,
  alternatives: 5,
  international: 40, // Higher international exposure
  sectors: {
    caribbean: 15,
    africa: 10,
    usLargeCap: 25,
    emerging: 15,
    other: 35
  }
}
```

**Youth (Aggressive Risk)**:
```typescript
{
  stocks: 85,
  bonds: 5,
  cash: 5,
  alternatives: 5,
  international: 20,
  sectors: {
    technology: 35,
    growth: 25,
    crypto: 10,
    greenEnergy: 15,
    other: 15
  }
}
```

**Creator (Moderate-Aggressive Risk)**:
```typescript
{
  stocks: 75,
  bonds: 10,
  cash: 10,
  alternatives: 5,
  international: 15,
  sectors: {
    creatorPlatforms: 30,
    entertainment: 20,
    advertising: 15,
    ecommerce: 10,
    other: 25
  }
}
```

**Legacy (Conservative Risk)**:
```typescript
{
  stocks: 50,
  bonds: 35,
  cash: 10,
  alternatives: 5,
  international: 15,
  sectors: {
    dividendAristocrats: 35,
    blueChips: 30,
    bonds: 20,
    utilities: 10,
    other: 5
  }
}
```

**Portfolio Optimization Algorithm**:
```typescript
class PortfolioDNAEngine {
  async optimizePortfolio(
    currentHoldings: Holding[],
    identity: IdentityType,
    riskTolerance: string,
    targetValue: number
  ): Promise<PortfolioRecommendation[]> {
    // 1. Get identity-specific allocation model
    const targetModel = this.getAllocationModel(identity, riskTolerance);
    
    // 2. Calculate current allocation
    const currentAllocation = this.calculateAllocation(currentHoldings);
    
    // 3. Identify gaps
    const gaps = this.calculateGaps(currentAllocation, targetModel);
    
    // 4. Generate buy/sell recommendations
    const recommendations = this.generateRecommendations(gaps, identity);
    
    // 5. Optimize for tax efficiency
    const optimized = this.optimizeForTaxes(recommendations);
    
    // 6. Score by identity alignment
    return this.scoreByIdentity(optimized, identity);
  }

  private scoreByIdentity(
    recommendations: PortfolioRecommendation[],
    identity: IdentityType
  ): PortfolioRecommendation[] {
    return recommendations.map(rec => {
      // Score based on identity characteristics
      let score = 50; // Base score

      if (identity === 'diaspora') {
        if (rec.symbol.match(/JBG|MTN|SBUX/)) score += 30;
        if (rec.symbol.includes('emerging')) score += 20;
      } else if (identity === 'youth') {
        if (rec.symbol.match(/NVDA|TSLA|COIN/)) score += 30;
        if (rec.reasoning.includes('growth')) score += 20;
      } else if (identity === 'creator') {
        if (rec.symbol.match(/META|GOOG|SPOT/)) score += 30;
        if (rec.reasoning.includes('creator')) score += 20;
      } else if (identity === 'legacy') {
        if (rec.symbol.match(/JNJ|PG|KO/)) score += 30;
        if (rec.reasoning.includes('dividend')) score += 20;
      }

      return { ...rec, identityAlignment: Math.min(100, score) };
    });
  }
}
```

**Rebalancing Logic**:
```typescript
async function shouldRebalance(portfolio: Portfolio): Promise<boolean> {
  const drift = calculateAllocationDrift(portfolio);
  
  // Rebalance if any allocation drifts > 5%
  return Object.values(drift).some(d => Math.abs(d) > 5);
}

function calculateAllocationDrift(portfolio: Portfolio): Record<string, number> {
  const current = portfolio.currentAllocation;
  const target = portfolio.targetAllocation;
  
  return {
    stocks: current.stocks - target.stocks,
    bonds: current.bonds - target.bonds,
    cash: current.cash - target.cash,
    alternatives: current.alternatives - target.alternatives
  };
}
```

**Premium Features** (Pro tier):
- Monte Carlo simulations (1000 iterations)
- Tax loss harvesting suggestions
- Multi-scenario planning
- Advanced risk analytics
- Correlation matrix
- Backtesting against historical data

**Error Handling**:
- Invalid risk tolerance → Default to moderate
- Insufficient holdings → Suggest starter portfolio
- Market data unavailable → Use cached models
- Calculation timeout → Show partial results

---

### 18.1.8 Billing Service

**Purpose**: Subscription management, payment processing, tier enforcement

**Responsibilities**:
- Subscription CRUD (create, upgrade, downgrade, cancel)
- Payment processing via Stripe
- Invoice generation
- Usage tracking (API calls, exports, alerts)
- Tier enforcement (Free/Premium/Pro)
- Billing history

**Technology Stack**:
- Next.js API Routes (`/api/billing/*`)
- Stripe API for payments
- PostgreSQL for subscriptions
- Webhook handler for Stripe events
- Cron job for subscription renewals

**Endpoints**:
```typescript
GET /api/billing/subscription
POST /api/billing/subscribe
PUT /api/billing/upgrade
POST /api/billing/cancel
GET /api/billing/invoices
GET /api/billing/usage
POST /api/billing/portal (redirects to Stripe portal)
```

**Data Models**:
```typescript
type SubscriptionTier = 'free' | 'premium' | 'pro';
type SubscriptionStatus = 'active' | 'canceled' | 'past_due' | 'trialing';

interface Subscription {
  id: string;
  userId: string;
  tier: SubscriptionTier;
  status: SubscriptionStatus;
  stripeCustomerId: string;
  stripeSubscriptionId: string;
  currentPeriodStart: Date;
  currentPeriodEnd: Date;
  cancelAtPeriodEnd: boolean;
  createdAt: Date;
  updatedAt: Date;
}

interface TierLimits {
  tier: SubscriptionTier;
  portfolios: number; // Free: 1, Premium: 5, Pro: unlimited
  alerts: number; // Free: 5, Premium: 50, Pro: 500
  exportLimit: number; // Free: 0, Premium: 10/mo, Pro: unlimited
  apiCalls: number; // Free: 1000/day, Premium: 10k/day, Pro: 100k/day
  features: {
    advancedCharts: boolean;
    analytics: boolean;
    apiAccess: boolean;
    whiteLabel: boolean;
  };
}

interface Invoice {
  id: string;
  subscriptionId: string;
  amount: number;
  currency: string;
  status: 'paid' | 'pending' | 'failed';
  invoiceUrl: string;
  paidAt: Date | null;
  createdAt: Date;
}
```

**Tier Features**:

**Free**:
- 1 portfolio
- 5 alerts
- Basic charts
- Standard news feed
- No CSV export
- No analytics

**Premium ($9.99/month)**:
- 5 portfolios
- 50 alerts
- Advanced charts
- Verified news with fact-checks
- 10 CSV exports/month
- Portfolio analytics
- AI insights
- Earnings alerts

**Pro ($29.99/month)**:
- Unlimited portfolios
- 500 alerts
- All Premium features
- API access (100k calls/day)
- Institutional-grade analytics
- White-label embedding
- Priority support

**Webhook Handling** (Stripe events):
- `customer.subscription.created` → Activate subscription
- `customer.subscription.updated` → Update tier/status
- `customer.subscription.deleted` → Downgrade to Free
- `invoice.payment_succeeded` → Record payment
- `invoice.payment_failed` → Mark past due, send email

**Error Handling**:
- Payment failed → Show BillingError, retry link
- Subscription canceled → Graceful downgrade, keep data
- Usage limit exceeded → Show upgrade prompt
- Stripe API down → Show cached billing info, disable upgrades

---

## 18.2 Supporting Services

### 18.1.9 Cross-Promotion Engine

**Purpose**: Behavioral tracking and intelligent cross-promotion (from Section 16)

**Responsibilities**:
- Track user behavior across modules
- Generate personalized recommendations
- Cross-module promotion logic
- Identity-aware messaging
- Conversion tracking
- A/B testing for promotions

**Technology Stack**:
- Next.js API Routes (`/api/promotions/*`)
- PostgreSQL for behavior data
- Redis for recommendation cache
- ML models for personalization

**Endpoints**:
```typescript
GET /api/promotions/recommendations?userId=123
POST /api/promotions/track
GET /api/promotions/conversions
PUT /api/promotions/dismiss
```

**Data Models**:
```typescript
intodexDominionId: string | null; // SSO integration
  createdAt: Date;
  lastLoginAt: Date;
}

interface Session {
  id: string;
  userId: string;
  token: string;
  expiresAt: Date;
  createdAt: Date;
}
```

**CodexDominion SSO Integration**:
```typescript
// OAuth configuration for CodexDominion
const codexDominionProvider = {
  id: 'codex-dominion',
  name: 'CodexDominion',
  type: 'oauth',
  authorization: {
    url: 'https://codexdominion.app/oauth/authorize',
    params: { scope: 'email profile identity' }
  },
  token: 'https://codexdominion.app/oauth/token',
  userinfo: 'https://codexdominion.app/oauth/userinfo',
  profile(profile) {
    return {
      id: profile.id,
      email: profile.email,
      name: profile.name,
      image: profile.avatar,
      codexIdentity: profile.sovereign_identity
    };
  }
};
```

**Cross-Platform Benefits**:
- Single login for DominionMarkets + CodexDominion
- Shared user profile data
- Unified identity system
- Cross-platform analytics
- Sovereign Council integrationargetModule: string;
  message: string;
  identity: IdentityType | 'all';
  priority: number;
  conditions: PromotionCondition[];
}
```

**See Section 16** for full implementation details.

---

## 18.2 Core Internal Services

These are the backbone of DominionMarkets — the internal services that power all features.

---

### A. Identity Service

**Purpose**: Store and manage user identity (Diaspora, Youth, Creator, Legacy)

**Responsibilities**:
- Identity selection
- Identity switching
- Identity-based personalization
- Identity-based cross-promotion

**Used By**:
- Dashboard
- Markets
- Portfolio
- News
- Alerts
- Premium

**Technology Stack**:
- Next.js API Routes (`/api/identity/*`)
- PostgreSQL for user profiles
- Redis for session identity cache
- Context API for frontend identity state

**Data Models**:
```typescript
interface User {
  id: string;
  email: string;
  passwordHash: string;
  name: string;
  avatarUrl: string | null;
  emailVerified: boolean;
  createdAt: Date;
  lastLoginAt: Date;
}

interface Session {
  id: string;
  userId: string;
  token: string;
  expiresAt: Date;
  createdAt: Date;
}
```

---

### 18.2.2 Notification Service

**Purpose**: Cross-channel notifications (push, email, in-app)

**Responsibilities**:
- Send web push notifications
- Send email notifications
- Queue notifications (Redis)
- Notification preferences
- Delivery tracking

**TechnologStock Data Provider

**Primary: Alpha Vantage**
- **Purpose**: Real-time quotes, historical data, earnings
- **Rate Limit**: 5 calls/minute (free), 75/minute (premium)
- **Cost**: Free tier available, $49.99/month premium
- **Fallback**: Polygon, IEX Cloud
- **Coverage**: Global stocks, forex, crypto

**Secondary: Polygon**
- **Purpose**: Real-time data, options, crypto
- **Rate Limit**: Unlimited (paid plan)
- **Cost**: $99/month starter
- **Use Case**: High-frequency updates for Premium users
- **Coverage**: US stocks, options, crypto

**Tertiary: IEX Cloud**
- **Purpose**: Fundamental data, company info
- **Rate Limit**: 50k messages/month (free)
- **Cost**: Free tier, $9/month paid
- **Use Case**: Company profiles, sector data
- **Coverage**: US stocks, ETFs
```

---

### 18.2.3 Search Service
Aggregation Pipeline

**Primary: NewsAPI**
- **Purpose**: General financial news
- **Rate Limit**: 100 requests/day (free), 1000/day (paid)
- **Cost**: Free tier, $449/month business
- **Coverage**: 80,000+ sources
- **Filters**: Language, domain, date range

**Secondary: Benzinga**
- **Purpose**: Real-time market news, analyst ratings
- **Rate Limit**: Varies by plan
- **Cost**: $99/month startup
- **Use Case**: Breaking news, earnings coverage
- **Latency**: < 1 second (real-time)

**Tertiary: Financial Modeling Prep**
- **Purpose**: Financial news, SEC filings
- **Rate Limit**: 250 requests/day (free)
- **Cost**: Free tier, $14/month premium
- **Coverage**: US stocks, SEC EDGAR filings

**Pipeline Processing**:
1. **Ingest** — Fetch from all providers (parallel)
2. **Deduplicate** — Remove duplicate articles (fuzzy matching)
3. **Fact-Check** — Run through verification engine
4. **Score** — Calculate credibility (0-100)
5. **Tag** — Extract symbols, sectors, entities
6. **Store** — Save to PostgreSQL with metadata
7. **Cache** — Redis cache for fast retrieval
8. **Notify** — Alert users with relevant news alerts

**Purpose**: User behavior tracking, feature usage, performance monitoring

**Responsibilities**:
- Page view tracking
- Feature usage metrics
- Error tracking (Sentry)
- Performance monitoring (Web Vitals)
- Conversion funnel tracking

**Technology Stack**:
- Google Analytics 4
- Grafana Faro for RUM
- Sentry for error tracking
- Custom events via `/api/analytics/track`

---

### 18.2.5 Cache Service

**Purpose**: Distributed caching for performance

**Responsibilities**:
- Cache API responses (market data, news)
- Session storage
- Rate limit tracking
- Pub/sub for real-time updates

**Technology Stack**:
- Redis for caching
- Redis pub/sub for real-time
- TTL-based invalidation

**Caching Strategy**:
```typescript
// Cache hierarchy
L1: Browser cache (service worker)
L2: CDN cache (Vercel edge)
L3: Redis cache (5 min - 24 hours)
L4: Database (source of truth)
```

---

## 18.3 External Dependencies
Earnings Calendar Provider

**Primary: Alpha Vantage Earnings Calendar**
- **Purpose**: Upcoming earnings dates, estimates
- **Rate Limit**: 5 calls/minute (free)
- **Cost**: Included in Alpha Vantage subscription
- **Data**: Date, time (BMO/AMC), estimate, actual

**Secondary: Benzinga Earnings Calendar**
- **Purpose**: Real-time earnings updates
- **Cost**: $99/month startup plan
- **Data**: Full earnings call transcripts (Premium)

**Integration**:
```typescript
async function fetchEarningsCalendar(date: Date): Promise<EarningsEvent[]> {
  try {
    // Try primary provider
    const data = await alphaVantage.getEarnings(date);
    retur5 Payment Processor
  } catch (error) {
    // Fallback to secondary
    const data = await benzinga.getEarnings(date);
    return data;
  }
}
```

**Caching**: 6 hours (updated 4x daily)
6 CodexDominion SSO

**Purpose**: Single Sign-On integration with Codex Dominion ecosystem

**OAuth 2.0 Flow**:
1. User clicks "Login with CodexDominion"
2. Redirect to CodexDominion OAuth page
3. User authorizes DominionMarkets
4. CodexDominion redirects back with auth code
5. Exchange code for access token
6. Fetch 8ser profile from CodexDominion API
7. Create/update user in DominionMarkets
8. Establish session

**Endpoints**:
- **Authorize**: `https://codexdominion.app/oauth/authorize`
- **Token**: `https://codexdominion.app/oauth/token`
- **Userinfo**: `https://codexdominion.app/oauth/userinfo`
- **Revoke**: `https://codexdominion.app/oauth/revoke`

**Scopes**:
- `email` — User email address
- `profile` — Name, avatar, bio
- `identity` — Sovereign identity type
- `treasury` — Treasury balance (read-only)
- `agents` — User's AI agents (list)

**Benefits**:
- Unified login across ecosystem
- Shared sovereign identity
- Cross-platform analytics
- Agent marketplace integration
- Council membership sync

**Error Handling**:
- CodexDominion down → Fall back to email/password
- Token expired → Automatic refresh
- Scope denied → Request minimum scopes
- Invalid token → Re-authenticate

---

### 18.3.7
---

### 18.3.4 
### 18.3.1 Market Data Providers

**Primary: Alpha Vantage**
- **Purpose**: Real-time quotes, historical data, earnings
- **Rate Limit**: 5 calls/minute (free), 75/minute (premium)
- **Cost**: Free tier available, $49.99/month premium
- **Fallback**: Polygon, IEX Cloud

**Secondary: Polygon**
- **Purpose**: Real-time data, options, crypto
- **Rate Limit**: Unlimited (paid plan)
- **Cost**: $99/month starter
- **Use Case**: High-frequency updates for Premium users

**Tertiary: IEX Cloud**
- **Purpose**: Fundamental data, company info
- **Rate Limit**: 50k messages/month (free)
- **Cost**: Free tier, $9/month paid
- **Use Case**: Company profiles, sector data

**Error Handling**:
- Primary down → Automatic failover to secondary
- All down → Show cached data + warning banner
- Rate limit exceeded → Queue requests, show delay warning

---

### 18.3.2 News Providers

**Primary: NewsAPI**
- **Purpose**: General financial news
- **Rate Limit**: 100 requests/day (free), 1000/day (paid)
- **Cost**: Free tier, $449/month business
- **Coverage**: 80,000+ sources

**Secondary: Benzinga**
- **Purpose**: Real-time market news, analyst ratings
- **Rate Limit**: Varies by plan
- **Cost**: $99/month startup
- **Use Case**: Breaking news, earnings coverage

**Tertiary: Financial Modeling Prep**
- **Purpose**: Financial news, SEC filings
- **Rate Limit**: 250 requests/day (free)
- **Cost**: Free tier, $14/month premium

---

### 18.3.3 Fact-Checking APIs

**FactCheck.org**
- **Purpose**: Political and financial claim verification
- **API**: ClaimReview schema via API
- **Cost**: Free (non-profit)

**Snopes**
- **Purpose**: General fact-checking
- **API**: Limited public API
- **Cost**: Free for non-commercial

**PolitiFact**
- **Purpose**: Political claims affecting markets
- **API**: RSS feeds + scraping
- **Cost**: Free

---

### 18.3.4 Payment Processing

**Stripe**
- **Purpose**: Subscription billing, payment processing
- **Integration**: Stripe Checkout, Customer Portal, Webhooks
- **Cost**: 2.9% + $0.30 per transaction
- **Features**: Recurring billing, invoice generation, tax calculation

---

### 18.3.5 Email Service

**SendGrid**
- **Purpose**: Transactional emails (alerts, auth, billing)
- **Rate Limit**: 100 emails/day (free), 40k/month (paid)
- **Cost**: Free tier, $19.95/month essentials
- **Deliverability**: 99%+ inbox rate

---

### 18.3.6 Monitoring & Logging

**Sentry**
- **Purpose**: Error tracking, performance monitoring
- **Cost**: Free tier (5k errors/month), $26/month team
- **Features**: Source maps, release tracking, user feedback

**Grafana Faro**
- **Purpose**: Real User Monitoring (RUM), Web Vitals
- **Cost**: Self-hosted (free) or Grafana Cloud (paid)
- **Metrics**: LCP, FID, CLS, page load time

---

## 18.4 Data Flows

### 18.4.1 Dashboard Load Flow

```
User → Dashboard Page
  ↓
Identity Service (get current identity)
  ↓
Parallel Fetch:
  - Market Data Service (movers, indices)
  - Portfolio Service (summary)
  - News Service (feed)
  - Alerts Service (active alerts)
  ↓
Cache Check (Redis)
  ↓
  If cached → Return immediately
  If not cached → Fetch from APIs
    ↓
    Market API (Alpha Vantage)
    News API (NewsAPI)
    Database (Portfolio, Alerts)
  ↓
Transform data (identity-aware messages)
  ↓
Cache result (Redis, 5-15 min TTL)
  ↓
Return to client
  ↓
Render dashboard with identity-specific UI
```

---

### 18.4.2 Stock Detail Flow

```
User → Stock Detail Page (/stock/AAPL)
  ↓
Market Data Service
  ↓
Parallel Fetch:
  - Quote (real-time price)
  - Historical data (chart)
  - News (symbol-specific)
  - Earnings calendar
  - Company profile
  ↓
Cache Check (Redis)
  ↓
Fetch from APIs if not cached:
  - Alpha Vantage (quote, historical)
  - NewsAPI (news)
  - IEX Cloud (company info)
  ↓
Fact-check news articles
  ↓
Cache results (Redis, 5-60 min TTL)
  ↓
Return to client
  ↓
Render stock detail page
```

---

### 18.4.3 Alert Trigger Flow

```
Background Worker (every 1 minute)
  ↓
Fetch active alerts from database
  ↓
Group alerts by symbol
  ↓
Fetch current prices (batch request)
  ↓
Evaluate alert conditions:
  - Price above threshold
  - Price below threshold
  - Percent change threshold
  ↓
  If condition met:
    ↓
    Notification Service
      ↓
      Send web push notification
      Send email notification
      Create in-app notification
      ↓
    Update alert (triggeredAt, triggerCount)
      ↓
    If one-time alert → Deactivate
    If recurring → Reset for next trigger
```

---

### 18.4.4 Premium Upgrade Flow

```
User → Click "Upgrade to Premium"
  ↓
Billing Service
  ↓
Check current subscription
  ↓
Create Stripe Checkout Session
  ↓
Redirect to Stripe Checkout
  ↓
User enters payment details
  ↓
Stripe processes payment
  ↓
Stripe webhook → /api/webhooks/stripe
  ↓
Verify webhook signature
  ↓
Process event (subscription.created)
  ↓
Update subscription in database
  ↓
Grant premium features
  ↓
Send confirmation email
  ↓
Redirect to dashboard with premium access
```

---

### 18.4.5 News Verification Flow

```
News Service → Ingest article
  ↓
Extract key claims (NLP)
  ↓
Query fact-checking APIs:
  - FactCheck.org
  - Snopes
  - PolitiFact
  ↓
Calculate credibility score:
  - Source trust score (0-100)
  - Fact-check results (verified/disputed)
  - Article age (recency bonus)
  ↓
Label bias (Media Bias/Fact Check)
  ↓
Store article with metadata:
  - verificationStatus
  - credibilityScore
  - biasLabel
  - factChecks[]
  ↓
Display with verification badge
```

---

## 18.5 Identity Integration

### 18.5.1 Identity Context Provider

**Frontend Implementation**:
```typescript
// contexts/IdentityContext.tsx
'use client';

import { createContext, useContext, useState, useEffect } from 'react';

type IdentityType = 'diaspora' | 'youth' | 'creator' | 'legacy';

interface IdentityContext {
  identity: IdentityType;
  setIdentity: (identity: IdentityType) => void;
  preferences: IdentityPreferences;
  updatePreferences: (prefs: Partial<IdentityPreferences>) => void;
}

const IdentityContext = createContext<IdentityContext | undefined>(undefined);

export function IdentityProvider({ children }: { children: React.ReactNode }) {
  const [identity, setIdentity] = useState<IdentityType>('diaspora');
  const [preferences, setPreferences] = useState<IdentityPreferences>({});

  useEffect(() => {
    // Load identity from API
    fetch('/api/identity/current')
      .then(res => res.json())
      .then(data => {
        setIdentity(data.type);
        setPreferences(data.preferences);
      });
  }, []);

  const updateIdentity = async (newIdentity: IdentityType) => {
    await fetch('/api/identity/select', {
      method: 'POST',
      body: JSON.stringify({ identity: newIdentity })
    });
    setIdentity(newIdentity);
  };

  return (
    <IdentityContext.Provider value={{ identity, setIdentity: updateIdentity, preferences }}>
      {children}
    </IdentityContext.Provider>
  );
}

export const useIdentity = () => {
  const context = useContext(IdentityContext);
  if (!context) throw new Error('useIdentity must be used within IdentityProvider');
  return context;
};
```

---

### 18.5.2 Identity-Aware Components

**Usage Pattern**:
```typescript
import { useIdentity } from '@/contexts/IdentityContext';

export function DashboardPage() {
  const { identity } = useIdentity();

  if (loading) {
    return <IdentityLoading identity={identity} />;
  }

  if (portfolios.length === 0) {
    return <NoPortfolioEmpty identity={identity} />;
  }

  return <Dashboard data={data} identity={identity} />;
}
```

---

### 18.5.3 Identity-Aware Recommendations

**Backend Logic**:
```typescript
// /api/identity/recommendations
export async function GET(req: Request) {
  const { identity } = await getSessionIdentity(req);

  const recommendations = {
    diaspora: [
      { symbol: 'MTN', reason: 'Leading African telecom' },
      { symbol: 'JBG', reason: 'Jamaican banking leader' }
    ],
    youth: [
      { symbol: 'VOO', reason: 'S&P 500 ETF for beginners' },
      { symbol: 'NVDA', reason: 'Growth stock leader' }
    ],
    creator: [
      { symbol: 'META', reason: 'Creator monetization platform' },
      { symbol: 'SPOT', reason: 'Audio creator economy' }
    ],
    legacy: [
      { symbol: 'JNJ', reason: 'Dividend aristocrat 60+ years' },
      { symbol: 'PG', reason: 'Stable dividend growth' }
    ]
  };

  return Response.json(recommendations[identity]);
}
```

---

## 18.6 Premium Integration

### 18.6.1 Tier Middleware

**Backend Enforcement**:
```typescript
// middleware/requirePremium.ts
export function requirePremium(handler: Handler) {
  return async (req: Request) => {
    const subscription = await getSubscription(req);

    if (subscription.tier === 'free') {
      return Response.json(
        { error: 'Premium subscription required' },
        { status: 403 }
      );
    }

    return handler(req);
  };
}

// Usage
export const GET = requirePremium(async (req) => {
  // Premium-only logic
});
```

---

### 18.6.2 Frontend Premium Gates

**Usage Pattern**:
```typescript
import { useSubscription } from '@/hooks/useSubscription';
import { PremiumGateAnalytics } from '@/components/gates/PremiumGateStates';

export function PortfolioPage() {
  const { tier } = useSubscription();
  const [showGate, setShowGate] = useState(false);

  const handleViewAnalytics = () => {
    if (tier === 'free') {
      setShowGate(true);
    } else {
      // Show analytics
    }
  };

  return (
    <>
      <button onClick={handleViewAnalytics}>
        View Analytics
        {tier === 'free' && <PremiumBadge />}
      </button>

      {showGate && (
        <PremiumGateAnalytics
          onUpgrade={() => router.push('/pricing')}
          onClose={() => setShowGate(false)}
        />
      )}
    </>
  );
}
```

---

### 18.6.3 Usage Tracking

**Backend Tracking**:
```typescript
// /api/billing/usage
export async function trackUsage(userId: string, type: 'export' | 'api_call' | 'alert') {
  const subscription = await getSubscription(userId);
  const limits = getTierLimits(subscription.tier);

  const usage = await incrementUsage(userId, type);

  if (usage[type] > limits[type]) {
    throw new Error('Usage limit exceeded');
  }

  return usage;
}
```

---

## 18.7 Reliability Principles

### 18.7.1 Graceful Degradation

**Principle**: System remains functional even when dependencies fail

**Implementation**:
- Market data unavailable → Show cached data + warning
- News service down → Show "News unavailable, try again later"
- Authentication service slow → Allow limited guest access
- Payment processing down → Queue upgrades, process later

**Example**:
```typescript
async function fetchMarketData(symbol: string) {
  try {
    // Try primary provider
    const data = await alphaVantage.getQuote(symbol);
    return data;
  } catch (error) {
    try {
      // Fallback to secondary
      const data = await polygon.getQuote(symbol);
      return data;
    } catch (fallbackError) {
      // Use cached data
      const cached = await cache.get(`quote:${symbol}`);
      if (cached) {
        return { ...cached, isStale: true };
      }
      throw new Error('Market data unavailable');
    }
  }
}
```

---

### 18.7.2 Circuit Breaker Pattern

**Principle**: Prevent cascading failures by cutting off failing services

**Implementation**:
```typescript
class CircuitBreaker {
  private failureCount = 0;
  private lastFailureTime: number | null = null;
  private state: 'closed' | 'open' | 'half-open' = 'closed';

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      if (Date.now() - this.lastFailureTime! > 60000) {
        this.state = 'half-open';
      } else {
        throw new Error('Circuit breaker is open');
      }
    }

    try {
      const result = await fn();
      if (this.state === 'half-open') {
        this.state = 'closed';
        this.failureCount = 0;
      }
      return result;
    } catch (error) {
      this.failureCount++;
      this.lastFailureTime = Date.now();
      if (this.failureCount >= 5) {
        this.state = 'open';
      }
      throw error;
    }
  }
}

const alphaVantageBreaker = new CircuitBreaker();

async function getQuote(symbol: string) {
  return alphaVantageBreaker.execute(() => 
    fetch(`https://www.alphavantage.co/query?symbol=${symbol}`)
  );
}
```

---

### 18.7.3 Retry Logic

**Principle**: Temporary failures should be retried with exponential backoff

**Implementation**:
```typescript
async function fetchWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  baseDelay = 1000
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries - 1) throw error;
      
      const delay = baseDelay * Math.pow(2, attempt);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  throw new Error('Max retries exceeded');
}

// Usage
const data = await fetchWithRetry(() => 
  fetch('/api/markets/quote?symbol=AAPL')
);
```

---

### 18.7.4 Rate Limiting

**Principle**: Protect APIs from overload and abuse

**Implementation**:
```typescript
// middleware/rateLimit.ts
import { Redis } from 'ioredis';

const redis = new Redis();

export async function rateLimit(
  userId: string,
  maxRequests: number,
  windowSeconds: number
): Promise<{ allowed: boolean; remaining: number }> {
  const key = `rate_limit:${userId}`;
  const current = await redis.incr(key);
  
  if (current === 1) {
    await redis.expire(key, windowSeconds);
  }

  const allowed = current <= maxRequests;
  const remaining = Math.max(0, maxRequests - current);

  return { allowed, remaining };
}

// Usage in API route
export async function GET(req: Request) {
  const userId = await getUserId(req);
  const { allowed, remaining } = await rateLimit(userId, 100, 60);

  if (!allowed) {
    return Response.json(
      { error: 'Rate limit exceeded' },
      { 
        status: 429,
        headers: { 'X-RateLimit-Remaining': '0' }
      }
    );
  }

  return Response.json(data, {
    headers: { 'X-RateLimit-Remaining': remaining.toString() }
  });
}
```

---

### 18.7.5 Health Checks

**Principle**: Monitor service health and dependencies

**Implementation**:
```typescript
// /api/health
export async function GET() {
  const checks = await Promise.allSettled([
    checkDatabase(),
    checkRedis(),
    checkMarketDataAPI(),
    checkNewsAPI(),
    checkStripe()
  ]);

  const results = {
    status: checks.every(c => c.status === 'fulfilled') ? 'healthy' : 'degraded',
    timestamp: new Date().toISOString(),
    checks: {
      database: checks[0].status === 'fulfilled' ? 'up' : 'down',
      redis: checks[1].status === 'fulfilled' ? 'up' : 'down',
      marketData: checks[2].status === 'fulfilled' ? 'up' : 'down',
      news: checks[3].status === 'fulfilled' ? 'up' : 'down',
      billing: checks[4].status === 'fulfilled' ? 'up' : 'down'
    }
  };

  const statusCode = results.status === 'healthy' ? 200 : 503;
  return Response.json(results, { status: statusCode });
}

async function checkDatabase() {
  await prisma.$queryRaw`SELECT 1`;
}

async function checkRedis() {
  await redis.ping();
}

async function checkMarketDataAPI() {
  const res = await fetch('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=demo');
  if (!res.ok) throw new Error('Market data API unreachable');
}
```

---

### 18.7.6 Monitoring & Alerting

**Metrics to Track**:
- API response times (p50, p95, p99)
- Error rates by endpoint
- Cache hit rates
- External API failure rates
- Database connection pool usage
- Memory/CPU usage

**Alerting Rules**:
- Error rate > 5% for 5 minutes → Page on-call engineer
- API response time p95 > 3s for 10 minutes → Warning
- External API down > 15 minutes → Critical alert
- Database connection pool exhausted → Critical alert
- Stripe webhook failures > 3 → Page billing team

---

## 18.8 Deployment Architecture

### 18.8.1 Production Stack

**Frontend**:
- **Platform**: Vercel (Next.js optimized)
- **CDN**: Vercel Edge Network (global)
- **SSL**: Automatic via Vercel
- **Environment**: `production`

**Backend APIs**:
- **Platform**: Vercel Serverless Functions
- **Runtime**: Node.js 18+
- **Timeout**: 10 seconds (free), 60 seconds (pro)
- **Memory**: 1024 MB
- **Cold start**: ~200ms

**Database**:
- **Primary**: PostgreSQL (Supabase or Neon)
- **Connection Pooling**: PgBouncer (500 connections)
- **Backups**: Daily automated snapshots
- **Region**: US East (primary), EU West (replica)

**Cache**:
- **Platform**: Upstash Redis (serverless)
- **Region**: Global edge locations
- **Persistence**: AOF (append-only file)
- **Max memory**: 1GB (scales with usage)

**Background Jobs**:
- **Platform**: Vercel Cron (scheduled functions)
- **Jobs**:
  - Alert monitoring (every 1 minute)
  - News ingestion (every 5 minutes)
  - Portfolio snapshots (every 15 minutes)
  - Subscription renewals (daily)

---

### 18.8.2 Staging EnvirEngine with fact-checking
- [ ] Identity Service with context provider
- [ ] Portfolio Service with analytics
- [ ] Alerts Service with real-time monitoring
- [ ] Cultural Alpha Engine™ with ML models
- [ ] Sovereign Portfolio DNA™ with optimization
- [ ] Billing Service with Stripe integration
- [ ] Cross-Promotion Engine (Section 16 complete)
- **URL**: staging.dominionmarkets.com
- **Database**: Separate PostgreSQL instance
- **APIs**: Sandbox/test endpoints (Stripe test mode)
- **Deployment**: Auto-deploy from `develop` branch

---
Stock Data Provider (Alpha Vantage, Polygon, IEX)
- [ ] News Aggregation Pipeline (NewsAPI, Benzinga, FMP)
- [ ] Earnings Calendar Provider (Alpha Vantage, Benzinga)
- [ ] FactCheck.org integration
- [ ] Payment Processor (Stripe webhooks)
- [ ] CodexDominion SSO (OAuth 2.0)h hot reload

**Setup**:
```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Start Redis (Docker)
docker run -d -p 6379:6379 redis

# Start PostgreSQL (Docker)
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres

# Run migrations
npm run db:migrate

# Seed database
npm run db:seed
```

**Environment Variables** (`.env.local`):
```env
DATABASE_URL=postgresql://localhost:5432/dominionmarkets
REDIS_URL=redis://localhost:6379
ALPHA_VANTAGE_API_KEY=demo
NEWS_API_KEY=test_key
STRIPE_SECRET_KEY=sk_test_xxx
NEXTAUTH_SECRET=dev_secret
NEXTAUTH_URL=http://localhost:3000
```

---

## 18.9 Security Considerations

### 18.9.1 API Security

- ✅ **Authentication**: JWT tokens via NextAuth
- ✅ **Authorization**: Role-based access control (RBAC)
- ✅ **Rate Limiting**: Per-user and per-IP limits
- ✅ **Input Validation**: Zod schemas for all inputs
- ✅ **SQL Injection**: Prisma ORM (parameterized queries)
- ✅ **XSS Protection**: React auto-escaping + CSP headers
- ✅ **CSRF Protection**: SameSite cookies + CSRF tokens

---

### 18.9.2 Data Privacy

- ✅ **Encryption at Rest**: Database encryption via provider
- ✅ **Encryption in Transit**: TLS 1.3 for all connections
- ✅ **PII Handling**: Minimal collection, secure storage
- ✅ **Data Retention**: User data deleted 30 days after account closure
- ✅ **GDPR Compliance**: Data export, right to deletion
- ✅ **Audit Logging**: All sensitive actions logged

---

### 18.9.3 Financial Data Security

- ✅ **PCI Compliance**: Stripe handles all card data (no storage)
- ✅ **Webhook Verification**: HMAC signature validation
- ✅ **API Key Rotation**: Quarterly rotation policy
- ✅ **Access Logs**: All billing API calls logged
- ✅ **Fraud Detection**: Stripe Radar for payment fraud

---

## 18.10 Scalability Plan

### 18.10.1 Horizontal Scaling

**Current**: Serverless functions (auto-scale)
**Future**: Kubernetes cluster with autoscaling

**Scaling Triggers**:
- CPU > 70% for 5 minutes
- Memory > 80% for 5 minutes
- Request queue > 100

---

### 18.10.2 Database Scaling

**Current**: Single PostgreSQL instance (Supabase)
**Future**:
- Read replicas (5x) for heavy read workloads
- Write sharding by user ID
- TimescaleDB for time-series market data

---

### 18.10.3 Caching Strategy

**Current**: Redis with TTL-based invalidation
**Future**:
- CDN caching for static assets
- Service Worker caching for offline support
- GraphQL with DataLoader for batch requests

---

## 18.11 Implementation Checklist

### Core Services
- [ ] Market Data Service API routes
- [ ] News Verification Service with fact-checking
- [ ] Identity Service with context provider
- [ ] Portfolio Service with analytics
- [ ] Alerts Service with real-time monitoring
- [ ] Billing Service with Stripe integration

### Supporting Services
- [ ] Authentication Service (NextAuth setup)
- [ ] Notification Service (push + email)
- [ ] Search Service (Algolia or PostgreSQL FTS)
- [ ] Analytics Service (GA4 + Grafana Faro)
- [ ] Cache Service (Redis setup)

### External Integrations
- [ ] Alpha Vantage API client
- [ ] NewsAPI client
- [ ] FactCheck.org integration
- [ ] Stripe subscription webhooks
- [ ] SendGrid email templates

### Reliability
- [ ] Circuit breaker implementation
- [ ] Retry logic with exponential backoff
- [ ] Rate limiting middleware
- [ ] Health check endpoint
- [ ] Error tracking (Sentry)
- [ ] Performance monitoring (Grafana Faro)

### Security
- [ ] API authentication (JWT)
- [ ] Input validation (Zod)
- [ ] SQL injection prevention (Prisma ORM)
- [ ] XSS protection (CSP headers)
- [ ] CSRF protection (tokens)
- [ ] Webhook signature verification

### Deployment
- [ ] Vercel production deployment
- [ ] Environment variable configuration
- [ ] Database migrations
- [ ] Redis instance setup
- [ ] Cron jobs for background tasks
- [ ] Monitoring dashboards

---

## 18.12 Next Steps

**After Section 18**:
1. **Section 19**: API Routes Implementation (all endpoints with Zod validation)
2. **Section 20**: External API Clients (Alpha Vantage, NewsAPI, Stripe)
3. **Section 21**: Real-time Features (WebSocket, Server-Sent Events)
4. **Section 22**: Testing Strategy (unit, integration, e2e tests)
5. **Section 23**: Performance Optimization (caching, code splitting, image optimization)

---

**Architecture Status**: SPECIFIED ✅  
**Implementation Status**: PENDING 🔄  
**Last Updated**: December 24, 2025
