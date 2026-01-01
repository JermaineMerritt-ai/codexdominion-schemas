# DOMINIONMARKETS — FEATURE ROADMAP

> **Timeline:** 18 months (Q1 2025 - Q2 2026)  
> **Compliance-First:** Every feature designed with regulatory safety  
> **Integration:** Full CodexDominion ecosystem connection

---

## 🎯 ROADMAP OVERVIEW

### Strategic Goals
1. **Build Trust** — Establish DominionMarkets as reliable financial data source
2. **Educate Users** — Financial literacy for Caribbean creators, youth, diaspora
3. **Generate Revenue** — Freemium model + creator marketplace integration
4. **Compliance First** — Never cross into advisory territory
5. **Caribbean Focus** — Local markets before expanding globally

### Phased Approach
- **Phase 1 (Foundation):** Q1-Q2 2025 — Core data platform (3 months)
- **Phase 2 (Insights):** Q2-Q3 2025 — Advanced analytics (3 months)
- **Phase 3 (Premium):** Q3-Q4 2025 — Monetization features (3 months)
- **Phase 4 (Ecosystem):** Q4 2025-Q2 2026 — Full CodexDominion integration (6 months)

---

## 📋 PHASE 1 — FOUNDATION (Q1-Q2 2025)

**Goal:** Launch minimum viable product with core data features

### 1.1 Real-Time Stock Data Dashboard

**Description:** Live stock price tracking with major exchanges

**Features:**
- Real-time prices (15-minute delay for free tier)
- Current price, change %, change $
- Open, high, low, close (OHLC)
- 52-week high/low
- Market cap, volume
- Previous close

**Data Sources:**
- Alpha Vantage API (free tier: 5 calls/min)
- Polygon.io (backup)
- Yahoo Finance API (supplementary)

**UI Components:**
- Stock search bar (autocomplete)
- Stock detail page
- Price chart (candlestick or line)
- Key metrics grid

**Technical Stack:**
- Frontend: Next.js 14 (React)
- Backend: Python FastAPI
- Database: PostgreSQL (price history)
- Cache: Redis (reduce API calls)

**Compliance:**
- Disclaimer on every page
- Source attribution visible
- Timestamp always shown

---

### 1.2 Market Movers (Top Gainers/Losers)

**Description:** Daily list of biggest movers in major indices

**Features:**
- Top 10 gainers (% increase)
- Top 10 losers (% decrease)
- Most active (by volume)
- Filter by: S&P 500, NASDAQ, Dow, Caribbean exchanges

**Display:**
- Table format (mobile-responsive)
- Color-coded (green=up, red=down)
- Click to view stock detail

**Update Frequency:**
- Refresh every 5 minutes (free tier)
- Real-time (premium tier)

**Compliance:**
- Header: "For informational purposes only"
- No language suggesting action ("Buy these winners!")

---

### 1.3 Sector Heatmaps

**Description:** Visual representation of sector performance

**Features:**
- 11 S&P sectors (Technology, Healthcare, Finance, etc.)
- Size = market cap
- Color = performance (green=up, red=down, gray=neutral)
- Click sector to see top stocks

**Visualization:**
- Treemap chart (D3.js or Recharts)
- Hover for details
- Responsive (mobile adapts to list view)

**Compliance:**
- Label: "Sector Performance Overview"
- No predictive language

---

### 1.4 Watchlists

**Description:** User-created lists of stocks to monitor

**Features:**
- Create unlimited watchlists (free: 3, premium: unlimited)
- Add/remove stocks
- View all watchlist stocks on one page
- Sort by: price, change %, name
- Export watchlist (CSV)

**UI:**
- Drag-and-drop reordering
- Quick-add from stock detail page
- Color-coded change indicators

**Data Storage:**
- PostgreSQL (user_watchlists table)
- User ID + stock symbols

**Compliance:**
- Watchlists are "for tracking only, not recommendations"

---

### 1.5 Basic Portfolio Tracker (Manual Entry)

**Description:** Track portfolio performance without connecting brokerage

**Features:**
- Manual entry: symbol, shares, purchase price, purchase date
- Automatic current price fetch
- Calculate: current value, gain/loss $, gain/loss %
- Total portfolio value
- Total gain/loss

**Why Manual Entry:**
- No brokerage API integration (regulatory complexity)
- User maintains full control
- Privacy-first approach

**UI:**
- Add position form
- Portfolio summary card
- Position list table
- Edit/delete positions

**Compliance:**
- "This tracker is for informational purposes only."
- "We do not store brokerage credentials."
- "We do not provide investment advice."

---

### 1.6 AI Summaries (Descriptive Only)

**Description:** GPT-4 powered summaries of portfolio and market data

**Safe Use Cases:**
- "Your portfolio is 60% technology stocks."
- "You added 3 positions this month."
- "Your largest holding is Apple (25% of portfolio)."
- "Tech sector is up 2% today."

**Not Allowed:**
- "You should diversify."
- "Consider selling tech stocks."
- "This stock looks undervalued."

**Implementation:**
- OpenAI GPT-4 API
- System prompt enforces neutral tone
- Template-based responses (pre-approved phrasing)
- Human review of templates before deployment

**Compliance:**
- All AI output reviewed for compliance
- Disclaimer: "AI-generated summary. Not advice."
- Kill switch if regulatory concerns arise

---

### 1.7 News Aggregation

**Description:** Financial news from multiple sources

**Features:**
- Aggregate headlines from: Bloomberg, Reuters, CNBC, Yahoo Finance, Caribbean Business Report
- Filter by: stock symbol, sector, keyword
- Timestamp and source clearly shown
- Click to read full article (external link)

**UI:**
- News feed (reverse chronological)
- Stock-specific news on stock detail page
- Search news by keyword

**Compliance:**
- No editorializing
- Source always visible
- External links (not hosted content)
- No "hot tips" or "must-read" language

---

## 📊 PHASE 2 — INSIGHTS (Q2-Q3 2025)

**Goal:** Add analytical tools to help users understand their portfolios

### 2.1 Portfolio Allocation Visualization

**Description:** Pie charts and bar charts showing portfolio breakdown

**Visualizations:**
- By sector (Tech, Healthcare, etc.)
- By asset class (Stocks, Bonds, Cash, Crypto)
- By individual holding (% of total)
- By market cap (Large-cap, Mid-cap, Small-cap)

**Interactive:**
- Click slice to see positions in that category
- Toggle between $ value and % allocation
- Compare to benchmark (S&P 500 allocation)

**Compliance:**
- Label charts: "Your Current Allocation"
- No suggestions like "Ideal allocation is..."

---

### 2.2 Diversification Analysis

**Description:** Descriptive metrics about portfolio concentration

**Metrics:**
- Number of holdings
- % in largest holding
- % in top 3 holdings
- % in top 10 holdings
- Herfindahl-Hirschman Index (HHI) for diversification score

**Display:**
- "Your portfolio has 15 holdings."
- "Your largest holding is 25% of total."
- "Your diversification score is 0.12 (0=fully diversified, 1=concentrated)."

**Compliance:**
- No judgment language ("too concentrated")
- Purely descriptive metrics
- Educational tooltips explain what metrics mean

---

### 2.3 Volatility Indicators

**Description:** Show historical volatility of portfolio and individual stocks

**Metrics:**
- Standard deviation (daily returns)
- Beta (vs S&P 500)
- Sharpe ratio (risk-adjusted return)
- Max drawdown (largest peak-to-trough decline)

**Display:**
- "This stock's volatility is higher than the market average."
- "Your portfolio's beta is 1.2 (more volatile than market)."
- Charts: volatility over time

**Compliance:**
- Explain volatility is "historical, not predictive"
- No language like "dangerous" or "safe"

---

### 2.4 Earnings Calendar

**Description:** Upcoming earnings announcements for watchlist/portfolio stocks

**Features:**
- Earnings dates for next 90 days
- Filter by: portfolio holdings, watchlist, all stocks
- Set reminders (email/push notification)
- Historical earnings results

**UI:**
- Calendar view (monthly)
- List view (chronological)
- "Before market open" vs "After market close" labels

**Compliance:**
- "Earnings dates for informational purposes."
- No predictions about earnings outcomes

---

### 2.5 Multi-Source News Verification

**Description:** Cross-check financial news across sources

**How It Works:**
1. Identify same story across multiple sources
2. Compare headlines and key facts
3. Flag discrepancies
4. Show verification badge if 3+ sources confirm

**UI:**
- News card with verification badge:
  - ✓ Confirmed by 3 sources (green)
  - ⚠ Only 1 source, not yet verified (yellow)
  - ⚠ Sources conflict (coral)

**Example:**
```
✓ Confirmed by 3 sources
  • Bloomberg: "Apple reports Q4 earnings beat"
  • Reuters: "Apple Q4 revenue exceeds estimates"
  • CNBC: "Apple beats earnings expectations"
```

**Compliance:**
- Transparent about verification process
- Show all sources, not cherry-pick
- Acknowledge when story is developing

---

### 2.6 Market Sentiment Indicators (Safe, Descriptive)

**Description:** Aggregate sentiment from news and social media (descriptive only)

**Safe Metrics:**
- "70% of news articles mention [stock] positively."
- "Social media mentions increased 200% today."
- "Analyst upgrades: 10, downgrades: 2 (this month)."

**Not Allowed:**
- "Sentiment is bullish, buy now."
- "Negative sentiment means price will drop."

**Data Sources:**
- News API (headline sentiment analysis)
- Twitter/X API (mention volume, not sentiment)
- Analyst rating aggregators (public data)

**Compliance:**
- All sentiment data is "for context only"
- Disclaimer: "Sentiment does not predict future performance."

---

## 💎 PHASE 3 — PREMIUM TOOLS (Q3-Q4 2025)

**Goal:** Monetize through premium subscription tier

### 3.1 Advanced Portfolio Analytics

**Premium Features:**
- Unlimited portfolios (vs 1 free)
- Historical performance tracking (vs 90 days free)
- Custom date range analysis
- Tax lot tracking (for capital gains estimation)
- Dividend tracking

**Pricing:**
- Free: 1 portfolio, 90-day history
- Premium: $9.99/month — Unlimited portfolios, full history
- Pro: $19.99/month — All premium + API access

---

### 3.2 Historical Performance Charts

**Description:** Detailed charts of portfolio/stock performance over time

**Chart Types:**
- Line chart (daily, weekly, monthly, yearly)
- Candlestick (for individual stocks)
- Area chart (cumulative returns)
- Comparison chart (portfolio vs S&P 500)

**Interactivity:**
- Zoom, pan, hover for details
- Adjustable date range
- Export chart as image/PDF

**Premium:**
- Free: Last 90 days
- Premium: All history since account creation

---

### 3.3 Risk Exposure Summaries

**Description:** Understand portfolio risk factors

**Metrics:**
- Geographic exposure (US, International, Caribbean)
- Currency exposure (if holding foreign stocks)
- Sector concentration risk
- Correlation matrix (how stocks move together)

**Display:**
- "Your portfolio is 80% US stocks, 15% Caribbean, 5% European."
- "Your top 3 holdings are highly correlated (move together)."

**Compliance:**
- Descriptive only
- No risk mitigation advice

---

### 3.4 Sector Concentration Summaries

**Description:** Detailed sector allocation analysis

**Features:**
- Compare your sector allocation to S&P 500
- Show % difference (over/underweight)
- Historical sector allocation changes

**Example:**
```
Your Sector Allocation vs S&P 500

Technology:     You: 45% | S&P: 28% | +17% overweight
Healthcare:     You: 20% | S&P: 13% | +7% overweight
Finance:        You: 10% | S&P: 13% | -3% underweight
```

**Compliance:**
- No judgment ("overweight" is descriptive, not prescriptive)
- Educational tooltip: "This shows allocation difference, not what you should do."

---

### 3.5 "Portfolio Health" Descriptive Overview

**Description:** AI-generated summary of portfolio characteristics

**Safe Summary Example:**
> "Your portfolio has 20 holdings across 8 sectors. Technology is your largest sector at 40%. Your portfolio's volatility is similar to the S&P 500. You've made 5 trades this month. Your cash allocation is 10%."

**Not Allowed:**
> "Your portfolio is unhealthy. You should reduce tech exposure."

**Implementation:**
- GPT-4 with strict system prompt
- Template-based with variable insertion
- Legal review of all templates

---

### 3.6 Custom Alerts (Price, Volume, News)

**Description:** Set custom notifications for stock events

**Alert Types:**
- Price: "Alert me if AAPL crosses $200"
- % Change: "Alert me if AAPL moves ±5% in a day"
- Volume: "Alert me if AAPL volume exceeds 100M"
- News: "Alert me when news mentions AAPL"

**Delivery:**
- Email (free: 5 alerts, premium: unlimited)
- Push notification (premium only)
- SMS (pro tier only)

**Compliance:**
- Alerts are informational, not recommendations
- No "Buy alert" or "Sell alert" language

---

## 🔗 PHASE 4 — ECOSYSTEM INTEGRATION (Q4 2025-Q2 2026)

**Goal:** Full integration with CodexDominion creator, youth, diaspora ecosystem

### 4.1 Creator Financial Courses

**Description:** Creators can sell financial education content

**Marketplace Integration:**
- Upload courses to IslandNation Marketplace
- Tag as "Financial Literacy" category
- Promote on DominionMarkets dashboard

**Course Topics (Examples):**
- "Understanding Stock Market Basics"
- "Reading Financial Statements for Beginners"
- "Caribbean Stock Markets 101"
- "Building a Diversified Portfolio"
- "Tax Strategies for Investors"

**Revenue Split:**
- Creator: 85%
- CodexDominion: 15%

**Compliance:**
- All courses reviewed for compliance before approval
- No courses making specific stock recommendations
- Educational content only

---

### 4.2 Youth Financial Literacy Challenges

**Description:** Gamified learning within DominionYouth platform

**Challenge Examples:**

**Week 1: Portfolio Basics**
- Task 1: Create your first watchlist
- Task 2: Track a stock for 7 days
- Task 3: Write a summary of what you learned
- Reward: 100 XP, "Market Explorer" badge

**Week 2: Diversification**
- Task 1: Build a mock portfolio with 5 stocks from different sectors
- Task 2: Calculate your portfolio's diversification score
- Task 3: Compare your allocation to S&P 500
- Reward: 150 XP, "Diversifier" badge

**Week 3: News Literacy**
- Task 1: Find the same news story on 3 sources
- Task 2: Identify any conflicting information
- Task 3: Write a summary of what's confirmed
- Reward: 200 XP, "Fact Checker" badge

**Integration:**
- DominionYouth dashboard shows financial challenges
- Leaderboard for financial literacy learners
- Certificates for completing full 12-week course

---

### 4.3 Diaspora Investment Dashboards

**Description:** Focused dashboards for Caribbean diaspora tracking home markets

**Features:**
- Caribbean stock exchanges (Jamaica, Trinidad, Barbados, etc.)
- Regional company profiles
- Diaspora-focused news (Caribbean business)
- "Support home" stock lists (informational)

**Example Dashboard:**
```
Caribbean Markets Overview

Jamaica Stock Exchange (JSE)
  Top Gainers: [List]
  Top Losers: [List]
  Market Cap: $XX.XB

Trinidad & Tobago Stock Exchange (TTSE)
  [Similar data]

Featured Caribbean Companies
  • Grace Kennedy (Jamaica)
  • Republic Bank (Trinidad)
  • Banks Holdings (Barbados)
```

**Compliance:**
- "For informational purposes. Not recommendations."
- Emphasize research before investing

---

### 4.4 Marketplace Tie-Ins (Financial Products)

**Description:** Creators sell financial-related digital products

**Allowed Products:**
- Stock research templates (Excel/Sheets)
- Investment journal templates
- Portfolio tracking spreadsheets
- Financial calculators
- Educational ebooks
- Market analysis frameworks

**Not Allowed:**
- Stock picks or recommendations
- "Get rich quick" schemes
- Predictions or forecasts
- Managed portfolios

**Review Process:**
- All financial products reviewed by compliance team
- 2-3 day approval process
- Rejection if any advisory language found

---

## 📅 DEVELOPMENT TIMELINE

### Q1 2025 (Months 1-3)
- ✅ Brand identity finalized
- ✅ Compliance legal review
- 🔄 Phase 1 development begins
- 🔄 API integrations (Alpha Vantage, Polygon)
- 🔄 Dashboard UI/UX design

**Deliverables:** Brand guide, legal review, wireframes

---

### Q2 2025 (Months 4-6)
- 🔄 Phase 1 feature development complete
- 🔄 Beta testing with CodexDominion users
- 🔄 Bug fixes and UX improvements
- 🔄 Soft launch (limited access)
- 🔄 Phase 2 development begins

**Deliverables:** MVP launch, user feedback, iteration

---

### Q3 2025 (Months 7-9)
- 🔄 Phase 2 insights features live
- 🔄 Premium tier launched ($9.99/month)
- 🔄 Marketing campaign (social media, email)
- 🔄 Phase 3 premium tools development

**Deliverables:** Premium tier, revenue generation, analytics

---

### Q4 2025 (Months 10-12)
- 🔄 Phase 3 advanced tools complete
- 🔄 Creator marketplace integration
- 🔄 Financial literacy courses go live
- 🔄 Phase 4 ecosystem integration begins

**Deliverables:** Creator revenue, ecosystem synergy

---

### Q1-Q2 2026 (Months 13-18)
- 🔄 Phase 4 full ecosystem integration
- 🔄 DominionYouth financial challenges live
- 🔄 Diaspora dashboards launched
- 🔄 Mobile app (iOS + Android)
- 🔄 International expansion (African diaspora markets)

**Deliverables:** Full platform, mobile apps, market expansion

---

## 💰 REVENUE MODEL

### Free Tier
- 1 portfolio
- 3 watchlists
- 90-day history
- 15-minute delayed data
- Basic alerts (5 max)
- Community features

**Target:** 10,000+ free users by end of Year 1

---

### Premium Tier ($9.99/month)
- Unlimited portfolios
- Unlimited watchlists
- Full historical data
- Real-time data
- Unlimited alerts
- Advanced analytics
- Priority support

**Target:** 1,000+ premium users by end of Year 1 (10% conversion)
**Revenue:** $120K/year from premium subscriptions

---

### Pro Tier ($19.99/month)
- All premium features
- API access (programmatic data)
- SMS alerts
- Export all data (CSV, JSON)
- Custom integrations
- White-label option (for creators)

**Target:** 100+ pro users by end of Year 1
**Revenue:** $24K/year from pro subscriptions

---

### Creator Marketplace (15% commission)
- Creators sell financial courses, templates, tools
- Estimated: $50K GMV in Year 1
- Commission: $7.5K

---

### Total Year 1 Revenue Projection
- Premium: $120K
- Pro: $24K
- Marketplace: $7.5K
- **Total: $151.5K**

---

## 🛡️ COMPLIANCE CHECKPOINTS

Every feature must pass these checks before launch:

### 1. Language Review
- ✅ No advisory language ("should," "must," "recommend")
- ✅ No predictive language ("will," "going to")
- ✅ Descriptive only ("is," "was," "currently")

### 2. Disclaimer Visibility
- ✅ Footer disclaimer on every page
- ✅ Tooltips explain what metrics mean
- ✅ User acknowledges disclaimer on first login

### 3. Data Attribution
- ✅ Source always visible
- ✅ Timestamp always shown
- ✅ External links for full articles

### 4. AI Output Monitoring
- ✅ All AI templates pre-approved by legal
- ✅ Random sampling of AI outputs weekly
- ✅ User reporting system for inappropriate AI responses

### 5. User Education
- ✅ "Learn" section with investing basics
- ✅ Glossary of financial terms
- ✅ "This is not advice" messaging throughout

---

## 📊 SUCCESS METRICS

### User Acquisition
- Free users: 10,000+ (Year 1)
- Premium users: 1,000+ (Year 1)
- Pro users: 100+ (Year 1)

### Engagement
- Daily active users: 20% of total
- Average session duration: 5+ minutes
- Watchlists created: 15,000+
- Portfolios tracked: 12,000+

### Revenue
- MRR: $12.5K by Month 12
- Churn rate: <5% monthly
- LTV:CAC ratio: 4:1

### Compliance
- Zero regulatory complaints
- Zero cease & desist letters
- 100% feature compliance score

---

**🔥 The roadmap is clear. Build trust first. Educate always. Monetize responsibly.** 📊

**Next Steps:** Feature prioritization, developer sprints, compliance reviews
