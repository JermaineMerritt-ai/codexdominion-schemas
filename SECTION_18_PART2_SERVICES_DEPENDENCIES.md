# SECTION 18 (Part 2) — CORE SERVICES & EXTERNAL DEPENDENCIES

**Continuation of System Dependencies & Architecture**  
Version 1.0 | December 24, 2025

---

## Data Flow Pattern

```
User Action
    |
    v
Frontend → API Gateway → Relevant Service
    |
    v
Service → External Provider (if needed)
    |
    v
Service → API Gateway → Frontend
```

**Request Flow**: User action triggers frontend → API Gateway routes to service → Service processes (may call external provider) → Response returns through API Gateway → Frontend updates

**Example**: User views Markets page → Frontend calls `/api/markets/movers` → Markets Service fetches from Alpha Vantage → Markets Service returns data → Frontend renders movers list

---

## Identity-Aware Data Flow

```
User Request
   |
   |-- includes identity token
   |
Backend Services
   |
   |-- modify response based on identity
```

**Identity Flow**: Every API request includes user's identity (Diaspora/Youth/Creator/Legacy) → Services personalize responses → Cultural insights, portfolio recommendations, and news filters adapt to identity

**Example**: Diaspora user views Dashboard → Request includes `identity: 'diaspora'` → Cultural Alpha Engine returns Caribbean/African market insights → Portfolio DNA suggests international allocation (40%) → News feed prioritizes diaspora-relevant stories

---

## Subscription Tier Gating

```python
if subscription == Premium:
    unlock premium features
elif subscription == Pro:
    unlock all features
else:
    return free-tier data
```

**Tier Logic**: Every API request checks subscription status → Services enforce tier limits → Premium/Pro users get enhanced features

**Free Tier**:
- 1 portfolio
- 5 alerts
- Basic charts
- Standard news feed

**Premium Tier** ($9.99/month):
- 5 portfolios
- 50 alerts
- Advanced charts
- Analytics dashboard
- Earnings alerts
- Cultural Alpha insights

**Pro Tier** ($24.99/month):
- Unlimited portfolios
- 500 alerts
- API access
- White-label options
- Priority support
- Monte Carlo simulations

**Example**: Free user views Portfolio → Billing Service checks `subscription: 'free'` → Analytics Engine returns basic diversification score only → "Upgrade to Premium" gate blocks advanced risk metrics

---

## API Routes Overview

All API routes follow RESTful conventions:

```
/api/auth/*                    # Authentication & session management
/api/identity/*                # Identity selection & preferences
/api/portfolio/*               # Portfolio CRUD operations
/api/holdings/*                # Holdings management
/api/markets/*                 # Market data, quotes, movers
/api/stocks/*                  # Stock details & fundamentals
/api/news/*                    # News feed & verification
/api/alerts/*                  # Alert management
/api/analytics/*               # Portfolio analytics
/api/subscription/*            # Billing & tier management
/api/cross-promotion/*         # Ecosystem recommendations
```

**Authentication**: All routes (except `/api/auth/login`) require JWT token in `Authorization: Bearer <token>` header

**Identity Context**: Most routes accept optional `?identity=diaspora|youth|creator|legacy` query param to override user's default identity

**Rate Limiting**: 
- Free tier: 100 requests/minute
- Premium tier: 500 requests/minute
- Pro tier: 2000 requests/minute

**Error Response Format**:
All errors follow consistent JSON structure:
```json
{
  "error": true,
  "message": "Human-readable explanation",
  "code": "ERROR_CODE"
}
```

**Common Error Codes**:
- `UNAUTHORIZED` (401) — Invalid or missing token
- `FORBIDDEN` (403) — Insufficient tier permissions
- `NOT_FOUND` (404) — Resource does not exist
- `RATE_LIMIT_EXCEEDED` (429) — Too many requests
- `VALIDATION_ERROR` (400) — Invalid input data
- `INTERNAL_ERROR` (500) — Server error

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

**API Endpoints**:
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
  user_id: string;
  type: IdentityType;
  displayName: string;
  preferences: IdentityPreferences;
  last_updated: Date;
}

interface IdentityPreferences {
  theme?: string;
  newsFilters?: string[];
  marketFocus?: string[];
  culturalInterests?: string[];
}

interface User {
  id: string;
  name: string;
  email: string;
  identity_type: IdentityType;
  subscription_tier: 'free' | 'premium' | 'pro';
  created_at: Date;
  updated_at: Date;
  sso_linked: boolean; // CodexDominion SSO connected
}
```

---

### B. Portfolio Service

**Purpose**: Store and manage user holdings

**Responsibilities**:
- Add/edit/remove holdings
- Calculate allocation
- Provide data to analytics engine

**Used By**:
- Dashboard
- Portfolio module
- AI summaries
- Alerts

**Technology Stack**:
- Next.js API Routes (`/api/portfolio/*`)
- PostgreSQL for portfolio data
- Redis for portfolio summary cache
- Background jobs for daily snapshots

**API Endpoints**:
```typescript
GET /api/portfolio/list
GET /api/portfolio/:id
POST /api/portfolio
GET /api/portfolio/:id/holdings
POST /api/portfolio/:id/holdings
PUT /api/portfolio/:id/holdings/:holdingId
DELETE /api/portfolio/:id/holdings/:holdingId
```

**Data Models**:
```typescript
interface Portfolio {
  id: string;
  user_id: string;
  name: string;
  isDefault: boolean;
  created_at: Date;
  updated_at: Date;
}

interface Holding {
  id: string;
  portfolio_id: string;
  ticker: string;
  shares: number;
  average_cost: number;
  created_at: Date;
  updated_at: Date;
}
```

---

### C. Markets Service

**Purpose**: Provide real-time market data

**Responsibilities**:
- Indices
- Sector heatmaps
- Movers
- Volume spikes
- Earnings calendar

**Used By**:
- Dashboard
- Markets module
- Stock Detail

**Technology Stack**:
- Next.js API Routes (`/api/markets/*`)
- External APIs: Alpha Vantage, Polygon, IEX Cloud
- Redis caching (5-minute TTL for quotes)

**API Endpoints**:
```typescript
GET /api/markets/quote?symbol=AAPL
GET /api/markets/movers?type=gainers|losers
GET /api/markets/heatmap?sector=all
GET /api/markets/earnings?date=2025-12-24
```

**Data Models**:
```typescript
interface Stock {
  ticker: string;
  name: string;
  sector: string;
  market_cap: number;
  exchange: string;
  identity_tags: IdentityType[]; // Which identities this stock is relevant to
}

interface MarketData {
  ticker: string;
  price: number;
  price_change: number;
  percent_change: number;
  volume: number;
  day_range: { low: number; high: number };
  year_range: { low: number; high: number };
  timestamp: Date;
}

interface Quote {
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  timestamp: Date;
}

interface Mover {
  symbol: string;
  name: string;
  price: number;
  changePercent: number;
  volume: number;
}
```

---

### D. News Verification Engine

**Purpose**: Verify news using multi-source aggregation

**Responsibilities**:
- Collect sources
- Assign verification level
- Generate timeline
- Provide identity-aware filters

**Used By**:
- Dashboard
- News module
- Stock Detail

**Technology Stack**:
- Next.js API Routes (`/api/news/*`)
- External APIs: NewsAPI, Benzinga
- Fact-checking APIs: FactCheck.org
- PostgreSQL for news archive

**API Endpoints**:
```typescript
GET /api/news/feed?symbol=AAPL&limit=20
GET /api/news/verify?articleId=123
GET /api/news/sources?verified=true
GET /api/news/timeline?symbol=TSLA&days=7
```

**Data Models**:
```typescript
interface NewsItem {
  id: string;
  headline: string;
  summary: string;
  source_count: number; // Number of sources reporting this story
  verification_level: 'verified' | 'unverified' | 'disputed';
  published_at: Date;
  related_tickers: string[];
}

interface VerificationRecord {
  news_id: string;
  sources: Array<{
    name: string;
    url: string;
    published_at: Date;
    credibility_weight: number; // 0-100
  }>;
  timeline: Array<{
    event: string;
    timestamp: Date;
  }>;
}

interface NewsArticle {
  id: string;
  title: string;
  summary: string;
  source: NewsSource;
  relatedSymbols: string[];
  verificationStatus: 'verified' | 'unverified' | 'disputed';
  credibilityScore: number; // 0-100
}
```

---

### E. Alerts Service

**Purpose**: Manage all user alerts

**Responsibilities**:
- Price alerts
- Volume alerts
- News alerts
- Earnings alerts (Premium)

**Used By**:
- Alerts Center
- Dashboard
- Portfolio

**Technology Stack**:
- Next.js API Routes (`/api/alerts/*`)
- PostgreSQL for alert definitions
- Redis pub/sub for real-time triggering
- Background worker for price monitoring
- Web Push API for notifications

**API Endpoints**:
```typescript
GET /api/alerts/list
POST /api/alerts
PUT /api/alerts/:id
DELETE /api/alerts/:id
POST /api/alerts/:id/test
```

**Data Models**:
```typescript
interface Alert {
  id: string;
  user_id: string;
  ticker: string;
  type: 'price' | 'news' | 'earnings' | 'volume';
  conditions: {
    condition: 'above' | 'below' | 'change_percent';
    value: number;
  };
  created_at: Date;
  last_triggered: Date | null;
}

interface AlertLegacy {
  id: string;
  userId: string;
  symbol: string;
  type: 'price' | 'news' | 'earnings' | 'volume';
  condition: 'above' | 'below' | 'change_percent';
  value: number;
  isActive: boolean;
}
```

---

### F. Analytics Engine

**Purpose**: Generate safe, descriptive analytics

**Responsibilities**:
- Diversification
- Volatility
- Sector concentration
- Identity alignment

**Used By**:
- Portfolio
- Stock Detail
- Dashboard

**Technology Stack**:
- Next.js API Routes (`/api/analytics/*`)
- Modern Portfolio Theory (MPT) algorithms
- PostgreSQL for analytics cache

**API Endpoints**:
```typescript
GET /api/analytics/portfolio/:id
GET /api/analytics/diversification/:portfolioId
GET /api/analytics/risk/:portfolioId
GET /api/analytics/identity-alignment/:portfolioId
```

**Data Models**:
```typescript
interface PortfolioAnalytics {
  diversificationScore: number; // 0-100
  volatility: number;
  sharpeRatio: number;
  sectorConcentration: SectorBreakdown[];
  identityAlignment: number; // 0-100
}
```

---

### G. Cultural Alpha Engine™

**Purpose**: Generate cultural relevance scores

**Responsibilities**:
- Cultural Alpha Score
- Identity-aware cultural insights
- Sector cultural heatmaps

**Used By**:
- Dashboard
- Markets
- Stock Detail
- Portfolio

**Technology Stack**:
- Next.js API Routes (`/api/cultural-alpha/*`)
- Machine learning models (TensorFlow.js)
- PostgreSQL for insight storage
- Redis for cached insights

**API Endpoints**:
```typescript
GET /api/cultural-alpha/insights?identity=diaspora
GET /api/cultural-alpha/trending?identity=youth
GET /api/cultural-alpha/opportunities?identity=creator
GET /api/cultural-alpha/events?region=caribbean
```

**Data Models**:
```typescript
interface CulturalAlpha {
  ticker: string;
  score: number; // 0-100
  signals: {
    youth_trend: number; // 0-100
    diaspora_mentions: number; // 0-100
    creator_influence: number; // 0-100
    innovation_resonance: number; // 0-100
    governance_indicators: number; // 0-100
  };
  updated_at: Date;
}

interface CulturalInsight {
  id: string;
  identity: IdentityType;
  category: 'market' | 'trend' | 'event' | 'opportunity';
  title: string;
  description: string;
  symbols: string[];
  regions: string[];
  impact: 'low' | 'medium' | 'high';
  confidence: number; // 0-100
}
```

**Identity-Specific Focus**:

**Diaspora**:
- Caribbean economic developments
- African market opportunities
- Diaspora remittance trends
- Pan-African company growth

**Youth**:
- Emerging tech trends
- Gig economy opportunities
- Gen Z spending patterns
- Gaming & esports sector

**Creator**:
- Creator platform earnings trends
- Influencer brand partnerships
- Platform monetization changes
- Creator economy ETFs

**Legacy**:
- Dividend safety analysis
- Multi-generational wealth strategies
- Blue chip stability indicators
- Recession-resistant sectors

---

### H. Sovereign Portfolio DNA™

**Purpose**: Provide identity-aware portfolio interpretations

**Responsibilities**:
- Interpret holdings
- Generate descriptive insights
- Align insights with identity

**Used By**:
- Portfolio
- Dashboard
- Stock Detail

**Technology Stack**:
- Next.js API Routes (`/api/portfolio-dna/*`)
- Modern Portfolio Theory (MPT) algorithms
- PostgreSQL for portfolio models
- Redis for calculation cache

**API Endpoints**:
```typescript
GET /api/portfolio-dna/recommendations?identity=diaspora&risk=moderate
POST /api/portfolio-dna/analyze
GET /api/portfolio-dna/allocation?identity=youth
GET /api/portfolio-dna/rebalance?portfolioId=123
```

**Data Models**:
```typescript
interface PortfolioDNA {
  portfolio_id: string;
  identity_type: IdentityType;
  insights: {
    risk_profile: string; // 'conservative' | 'moderate' | 'aggressive'
    sector_balance: number; // 0-100 (diversification score)
    volatility_character: string; // 'stable' | 'moderate' | 'volatile'
    identity_alignment: number; // 0-100 (how well portfolio matches identity)
    cultural_exposure: number; // 0-100 (exposure to identity-relevant sectors)
  };
  generated_at: Date;
}

interface PortfolioDNALegacy {
  id: string;
  userId: string;
  identity: IdentityType;
  riskTolerance: 'conservative' | 'moderate' | 'aggressive';
  targetAllocation: AllocationModel;
  currentAllocation: AllocationModel;
  rebalanceNeeded: boolean;
  recommendations: PortfolioRecommendation[];
}
```

**Identity-Specific Allocation Models**:

**Diaspora (Moderate Risk)**:
- Stocks: 60%
- Bonds: 25%
- International: 40% (higher international exposure)
- Focus: Caribbean, Africa, emerging markets

**Youth (Aggressive Risk)**:
- Stocks: 85%
- Bonds: 5%
- Focus: Technology 35%, growth stocks, green energy

**Creator (Moderate-Aggressive)**:
- Stocks: 75%
- Bonds: 10%
- Focus: Creator platforms 30%, entertainment, advertising

**Legacy (Conservative)**:
- Stocks: 50%
- Bonds: 35%
- Focus: Dividend aristocrats 35%, blue chips, utilities

---

### I. Billing Service

**Purpose**: Manage Premium and Pro subscriptions

**Responsibilities**:
- Subscription status
- Payment method
- Upgrade/downgrade
- Renewal

**Used By**:
- Premium gates
- Settings
- Analytics
- Alerts

**Technology Stack**:
- Next.js API Routes (`/api/billing/*`)
- Stripe API for payments
- PostgreSQL for subscriptions
- Webhook handler for Stripe events

**API Endpoints**:
```typescript
GET /api/billing/subscription
POST /api/billing/subscribe
PUT /api/billing/upgrade
POST /api/billing/cancel
GET /api/billing/invoices
```

**Data Models**:
```typescript
interface Subscription {
  user_id: string;
  tier: 'free' | 'premium' | 'pro';
  renewal_date: Date;
  payment_method: string; // e.g., "card_1234", "pm_5678"
  status: 'active' | 'canceled' | 'past_due' | 'trialing';
}

interface SubscriptionLegacy {
  id: string;
  userId: string;
  tier: 'free' | 'premium' | 'pro';
  status: 'active' | 'canceled' | 'past_due';
  stripeCustomerId: string;
  currentPeriodEnd: Date;
}
```

**Tier Limits**:
- **Free**: 1 portfolio, 5 alerts, basic charts
- **Premium**: 5 portfolios, 50 alerts, advanced charts, analytics
- **Pro**: Unlimited portfolios, 500 alerts, API access, white-label

---

### J. Cross-Promotion Engine

**Purpose**: Deliver identity-aware ecosystem recommendations

**Responsibilities**:
- Identity-based suggestions
- Behavioral refinement
- Ecosystem product linking

**Used By**:
- Dashboard
- News
- Portfolio
- Markets

**Technology Stack**:
- Next.js API Routes (`/api/promotions/*`)
- PostgreSQL for behavior data
- Redis for recommendation cache
- ML models for personalization

**API Endpoints**:
```typescript
GET /api/promotions/recommendations?userId=123
POST /api/promotions/track
GET /api/promotions/conversions
PUT /api/promotions/dismiss
```

**Data Models**:
```typescript
interface Recommendation {
  user_id: string;
  identity_type: IdentityType;
  context: string; // e.g., "viewing_dashboard", "portfolio_empty", "news_engagement"
  product_id: string; // CodexDominion product/module ID
  relevance_score: number; // 0-100
  generated_at: Date;
}

interface Promotion {
  id: string;
  type: 'cross-module' | 'feature' | 'upgrade';
  targetModule: string;
  message: string;
  identity: IdentityType | 'all';
  priority: number;
}
```

**See Section 16** for full implementation details.

---

## 18.3 External Dependencies

These are third-party or ecosystem services DominionMarkets relies on.

---

### A. Stock Data Provider

**Provides**:
- Prices
- Volume
- Indices
- Sector data

**Primary Provider: Alpha Vantage**
- **Rate Limit**: 5 calls/minute (free), 75/minute (premium)
- **Cost**: Free tier, $49.99/month premium
- **Coverage**: Global stocks, forex, crypto
- **Data**: Real-time quotes, historical data, earnings

**Secondary Provider: Polygon**
- **Rate Limit**: Unlimited (paid plan)
- **Cost**: $99/month starter
- **Coverage**: US stocks, options, crypto
- **Use Case**: High-frequency updates for Premium users

**Tertiary Provider: IEX Cloud**
- **Rate Limit**: 50k messages/month (free)
- **Cost**: Free tier, $9/month paid
- **Coverage**: US stocks, ETFs
- **Use Case**: Company profiles, sector data

**Integration Pattern**:
```typescript
async function fetchStockData(symbol: string) {
  try {
    return await alphaVantage.getQuote(symbol);
  } catch (error) {
    try {
      return await polygon.getQuote(symbol);
    } catch (fallbackError) {
      const cached = await cache.get(`quote:${symbol}`);
      if (cached) return { ...cached, isStale: true };
      throw new Error('Stock data unavailable');
    }
  }
}
```

**Error Handling**:
- Primary down → Automatic failover to secondary
- All down → Show cached data + warning banner
- Rate limit exceeded → Queue requests, show delay warning

---

### B. News Aggregation Pipeline

**Provides**:
- Raw news articles
- Source metadata
- Publication timestamps

**Primary Provider: NewsAPI**
- **Rate Limit**: 100 requests/day (free), 1000/day (paid)
- **Cost**: Free tier, $449/month business
- **Coverage**: 80,000+ sources
- **Filters**: Language, domain, date range

**Secondary Provider: Benzinga**
- **Rate Limit**: Varies by plan
- **Cost**: $99/month startup
- **Use Case**: Breaking news, earnings coverage
- **Latency**: < 1 second (real-time)

**Tertiary Provider: Financial Modeling Prep**
- **Rate Limit**: 250 requests/day (free)
- **Cost**: Free tier, $14/month premium
- **Coverage**: US stocks, SEC EDGAR filings

**Pipeline Processing Steps**:
1. **Ingest** — Fetch from all providers (parallel)
2. **Deduplicate** — Remove duplicate articles (fuzzy matching)
3. **Fact-Check** — Run through verification engine
4. **Score** — Calculate credibility (0-100)
5. **Tag** — Extract symbols, sectors, entities
6. **Store** — Save to PostgreSQL with metadata
7. **Cache** — Redis cache for fast retrieval
8. **Notify** — Alert users with relevant news alerts

---

### C. Earnings Calendar Provider

**Provides**:
- Earnings dates
- Earnings results
- Company metadata

**Primary Provider: Alpha Vantage Earnings Calendar**
- **Rate Limit**: 5 calls/minute (free)
- **Cost**: Included in Alpha Vantage subscription
- **Data**: Date, time (BMO/AMC), estimate, actual

**Secondary Provider: Benzinga Earnings Calendar**
- **Cost**: $99/month startup plan
- **Data**: Full earnings call transcripts (Premium)

**Integration Pattern**:
```typescript
async function fetchEarningsCalendar(date: Date) {
  try {
    return await alphaVantage.getEarnings(date);
  } catch (error) {
    return await benzinga.getEarnings(date);
  }
}
```

**Caching**: 6 hours (updated 4x daily)

---

### D. Payment Processor

**Handles**:
- Billing
- Renewals
- Refunds
- Payment methods

**Provider: Stripe**
- **Integration**: Stripe Checkout, Customer Portal, Webhooks
- **Cost**: 2.9% + $0.30 per transaction
- **Features**: Recurring billing, invoice generation, tax calculation

**Webhook Events**:
- `customer.subscription.created` → Activate subscription
- `customer.subscription.updated` → Update tier/status
- `customer.subscription.deleted` → Downgrade to Free
- `invoice.payment_succeeded` → Record payment
- `invoice.payment_failed` → Mark past due, send email

**Integration Pattern**:
```typescript
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  payment_method_types: ['card'],
  line_items: [{ price: 'price_premium', quantity: 1 }],
  success_url: 'https://dominionmarkets.com/success',
  cancel_url: 'https://dominionmarkets.com/pricing'
});
```

---

### E. CodexDominion SSO

**Provides**:
- Unified login
- Account linking
- Ecosystem identity

**OAuth 2.0 Flow**:
1. User clicks "Login with CodexDominion"
2. Redirect to CodexDominion OAuth page
3. User authorizes DominionMarkets
4. CodexDominion redirects back with auth code
5. Exchange code for access token
6. Fetch user profile from CodexDominion API
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
- Unified login across DominionMarkets + CodexDominion
- Shared sovereign identity
- Cross-platform analytics
- Agent marketplace integration
- Council membership sync

**Integration Pattern**:
```typescript
const codexDominionProvider = {
  id: 'codex-dominion',
  name: 'CodexDominion',
  type: 'oauth',
  authorization: {
    url: 'https://codexdominion.app/oauth/authorize',
    params: { scope: 'email profile identity' }
  },
  token: 'https://codexdominion.app/oauth/token',
  userinfo: 'https://codexdominion.app/oauth/userinfo'
};
```

**Error Handling**:
- CodexDominion down → Fall back to email/password login
- Token expired → Automatic refresh
- Scope denied → Request minimum scopes
- Invalid token → Re-authenticate

---

## 18.7 Reliability Principles

DominionMarkets must be:

### 1. Resilient

Graceful fallback when data is missing.

**Implementation**:
- Multi-provider fallback (Alpha Vantage → Polygon → IEX Cloud)
- Cached data with stale indicators
- Error boundaries in frontend
- Partial data display (show what's available)

**Example**: Alpha Vantage down → Polygon provides quotes → If both down → Show cached data with "Market data delayed" banner

---

### 2. Fast

Caching for:
- **Indices** (5-minute TTL)
- **Movers** (5-minute TTL)
- **News summaries** (15-minute TTL)

**Implementation**:
- Redis for hot data
- CDN for static assets
- Database query optimization
- Background jobs for heavy computation

**Target Performance**:
- API response: < 200ms (p95)
- Page load: < 2 seconds
- Chart render: < 500ms

---

### 3. Safe

**No predictions.**  
**No recommendations.**  
**No advice.**

**What We Provide**:
- ✅ Historical performance data
- ✅ Descriptive analytics (diversification, volatility)
- ✅ Identity-aligned insights (cultural relevance)
- ✅ Educational content

**What We Avoid**:
- ❌ "This stock will rise"
- ❌ "You should buy/sell"
- ❌ "Recommended portfolio allocation"
- ❌ Price predictions or forecasts

**Legal Safeguards**:
- Disclaimers on all financial data
- "Not financial advice" footer
- Educational framing for all insights
- No fiduciary relationship

---

### 4. Identity-Aware

Identity modifies insights, not raw data.

**Raw Data (Unchanged by Identity)**:
- Stock prices
- Volume
- Earnings dates
- Company fundamentals

**Identity-Modified Insights**:
- Cultural Alpha scores
- News feed filtering
- Portfolio DNA recommendations
- Cross-promotion suggestions

**Example**: 
- **Raw**: AAPL trades at $180.50
- **Diaspora insight**: "Apple expanding retail in Nigeria"
- **Youth insight**: "Apple Vision Pro targets Gen Z creators"
- **Creator insight**: "Apple's creator tools boost influencer revenue"
- **Legacy insight**: "Apple's dividend history spans 40 years"

---

### 5. Modular

Each service can scale independently.

**Service Independence**:
- Identity Service → 2 replicas (low load)
- Markets Service → 10 replicas (high traffic)
- Cultural Alpha → 5 replicas (ML workload)
- Portfolio Service → 3 replicas (moderate load)

**Benefits**:
- Cost efficiency (scale only what needs it)
- Fault isolation (one service down ≠ full outage)
- Independent deployments
- Technology flexibility (different languages/frameworks per service)

**Scaling Strategy**:
```yaml
# Kubernetes HPA example
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: markets-service
spec:
  minReplicas: 5
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70
```

---

## 20.2 AUTH ENDPOINTS

### POST /auth/login
**Body**:
- `email`
- `password`

**Returns**:
- `user` object
- `session_token`

---

### POST /auth/signup
**Body**:
- `name`
- `email`
- `password`

**Returns**:
- `user` object
- `verification_required: true`

---

### POST /auth/verify-email
**Body**:
- `token`

---

### POST /auth/forgot-password
**Body**:
- `email`

---

### POST /auth/reset-password
**Body**:
- `token`
- `new_password`

---

### POST /auth/sso
**Body**:
- `sso_token`

---

## 20.3 IDENTITY ENDPOINTS

### GET /identity
**Returns**:
- `identity_type`
- `preferences`

---

### POST /identity
**Body**:
- `identity_type`

---

### PATCH /identity/preferences
**Body**:
- `preference_key`
- `value`

---

## 20.4 PORTFOLIO ENDPOINTS

### GET /portfolio
**Returns**:
- List of portfolios (1 for Free, 5 for Premium, unlimited for Pro)

---

### POST /portfolio
**Body**:
- `name`

**Tier**: Premium or Pro only

---

### DELETE /portfolio/{id}
**Tier**: Premium or Pro only

---

## 20.5 HOLDINGS ENDPOINTS

### GET /portfolio/{id}/holdings
**Returns**:
- `holdings` array

---

### POST /portfolio/{id}/holdings
**Body**:
- `ticker`
- `shares`
- `average_cost`

---

### PATCH /holdings/{id}
**Body**:
- `shares`
- `average_cost`

---

### DELETE /holdings/{id}

---

## 20.6 MARKETS ENDPOINTS

### GET /markets/overview
**Returns**:
- `indices`
- `movers`
- `heatmap_preview`
- `earnings_preview`

---

### GET /markets/heatmap
**Note**: Premium unlocks full version

---

### GET /markets/movers
**Note**: Premium unlocks full list

---

### GET /markets/volume-spikes

---

### GET /markets/earnings
**Note**: Premium unlocks full calendar

---

## 20.7 STOCK ENDPOINTS

### GET /stocks/{ticker}
**Returns**:
- Company info
- `identity_tags`
- `cultural_alpha_preview`

---

### GET /stocks/{ticker}/chart
**Query Params**:
- `timeframe`

**Note**: Premium unlocks indicators

---

### GET /stocks/{ticker}/news

---

### GET /stocks/{ticker}/insights
**Tier**: Premium required

---

## 20.8 NEWS ENDPOINTS

### GET /news
**Query Params**:
- `filters` (identity-aware)

---

### GET /news/{id}
**Returns**:
- `headline`
- `summary`
- `verification_level`
- `source_count`
- `related_tickers`

---

### GET /news/{id}/sources
**Tier**: Premium unlocks full list

---

### GET /news/{id}/timeline
**Tier**: Premium unlocks historical

---

## 20.9 ALERTS ENDPOINTS

### GET /alerts

---

### POST /alerts
**Body**:
- `ticker`
- `type`
- `conditions`

**Note**: Premium unlocks advanced conditions

---

### PATCH /alerts/{id}

---

### DELETE /alerts/{id}

---

## 20.10 ANALYTICS ENDPOINTS

### GET /analytics/portfolio/{id}
**Tier**: Premium required

**Returns**:
- `diversification`
- `volatility`
- `sector_concentration`
- `identity_alignment`
- `cultural_exposure`

---

### GET /analytics/portfolio/{id}/pro
**Tier**: Pro only

**Returns**: Advanced analytics including Monte Carlo simulations

---

## 20.11 SUBSCRIPTION ENDPOINTS

### GET /subscription
**Returns**:
- `tier`
- `renewal_date`
- `status`

---

### POST /subscription/upgrade
**Body**:
- `tier`

---

### POST /subscription/payment-method
**Body**:
- `payment_token`

---

## 20.12 CROSS-PROMOTION ENDPOINTS

### GET /cross-promotion
**Query Params**:
- `context` (dashboard, news, portfolio, markets)

**Returns**:
- `recommended_products`
- `relevance_score`

**Note**: Identity-aware recommendations

---

## Service Dependency Matrix

| Service | Depends On | Provides To |
|---------|-----------|-------------|
| Identity Service | PostgreSQL, Redis | All modules |
| Portfolio Service | Markets Service, PostgreSQL | Dashboard, Analytics |
| Markets Service | Stock Data Provider, Redis | Dashboard, Portfolio, Stock Detail |
| News Verification | News Pipeline, Fact-Checking APIs | Dashboard, News module |
| Alerts Service | Markets Service, Notification | Dashboard, Portfolio |
| Analytics Engine | Portfolio Service, Markets Service | Portfolio, Dashboard |
| Cultural Alpha | ML Models, Markets Service | Dashboard, Markets |
| Portfolio DNA | Portfolio Service, Analytics | Portfolio, Dashboard |
| Billing Service | Stripe, PostgreSQL | Premium gates, Settings |
| Cross-Promotion | Identity Service, Behavior Tracking | All modules |

---

## Integration Checklist

### Core Services
- [ ] Identity Service (API routes + context provider)
- [ ] Portfolio Service (CRUD + allocation calc)
- [ ] Markets Service (API integration + caching)
- [ ] News Verification Engine (multi-source + fact-checking)
- [ ] Alerts Service (monitoring + notifications)
- [ ] Analytics Engine (MPT algorithms + scoring)
- [ ] Cultural Alpha Engine™ (ML models + insights)
- [ ] Sovereign Portfolio DNA™ (optimization + recommendations)
- [ ] Billing Service (Stripe integration + webhooks)
- [ ] Cross-Promotion Engine (behavioral tracking + ML)

### External Dependencies
- [ ] Stock Data Provider (Alpha Vantage + fallbacks)
- [ ] News Aggregation Pipeline (3 providers + deduplication)
- [ ] Earnings Calendar Provider (2 providers + caching)
- [ ] Payment Processor (Stripe checkout + webhooks)
- [ ] CodexDominion SSO (OAuth 2.0 + profile sync)

---

**Status**: SPECIFIED ✅  
**Implementation**: PENDING 🔄  
**Last Updated**: December 24, 2025
