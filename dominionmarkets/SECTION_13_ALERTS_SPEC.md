# SECTION 13 — ALERTS CENTER (FULL SPECIFICATION)

> **Status**: Design Complete | Implementation Ready  
> **Priority**: High — Personal signal hub for all users  
> **Dependencies**: Stock data API, News Verification Center, Portfolio Module  
> **Last Updated**: December 24, 2025

---

## 13.1 Overview

The **Alerts Center** is the user's personal signal hub for market events, price movements, news, and portfolio changes.

### Design Principles
1. **Simple**: Easy to create and manage alerts
2. **Reliable**: Triggers fire exactly when conditions are met
3. **Identity-Aware**: Alerts tailored to diaspora/youth/creator/legacy personas
4. **Premium-Ready**: Free tier with limits, premium unlocks more
5. **Safe & Descriptive**: No predictions, no advice, factual notifications only

### Key Features
- Price alerts (above/below/percent change)
- News alerts (company mentions, category updates)
- Earnings alerts (upcoming, released)
- Dividend alerts (ex-date, payment date)
- Portfolio alerts (gain/loss thresholds, rebalancing)
- Volume alerts (unusual activity)
- Cultural Alpha alerts (identity-specific opportunities)

---

## 13.2 Alert Types

### A. Price Alerts
**Purpose**: Notify when stock price crosses threshold

**Conditions**:
- Above: `current_price >= target_price`
- Below: `current_price <= target_price`
- Percent Up: `(current - open) / open * 100 >= percent`
- Percent Down: `(current - open) / open * 100 <= -percent`

**Free Tier**: 5 active price alerts  
**Premium**: 50 active price alerts  
**Pro**: Unlimited price alerts

**Example Notifications**:
- "AAPL is now $185.50, above your alert at $185.00"
- "TSLA dropped 5.2%, triggering your alert at -5.0%"

### B. News Alerts
**Purpose**: Notify when verified news mentions company or category

**Conditions**:
- Company mentioned in verified article (min score 75)
- Category match (earnings, M&A, dividends, etc.)
- High verification score (90+) only (premium feature)

**Free Tier**: 3 active news alerts  
**Premium**: 20 active news alerts  
**Pro**: Unlimited news alerts + RSS feed

**Example Notifications**:
- "Verified news: NVDA mentioned in 4 new articles (avg score: 87)"
- "Earnings category: 3 new verified stories"

### C. Earnings Alerts
**Purpose**: Notify about upcoming and released earnings

**Conditions**:
- 7 days before earnings date
- 1 day before earnings date
- When earnings released (real-time)
- When earnings beat/miss estimates (descriptive only)

**Free Tier**: 10 active earnings alerts  
**Premium**: 100 active earnings alerts  
**Pro**: Unlimited + earnings calendar export

**Example Notifications**:
- "GOOGL earnings in 7 days (Jan 30, 2026 after market close)"
- "AMZN released Q4 earnings: Revenue $170B (expected $168B)"

### D. Dividend Alerts
**Purpose**: Notify about dividend events

**Conditions**:
- Dividend announced
- Ex-dividend date approaching (3 days before)
- Payment date approaching (1 day before)
- Dividend increase/decrease (descriptive)

**Free Tier**: 5 active dividend alerts  
**Premium**: 30 active dividend alerts  
**Pro**: Unlimited + dividend calendar

**Example Notifications**:
- "JPM ex-dividend date is Dec 27 (3 days away)"
- "KO declared quarterly dividend: $0.48 per share (+4% from previous)"

### E. Portfolio Alerts
**Purpose**: Notify about portfolio performance milestones

**Conditions**:
- Total portfolio gain/loss threshold
- Individual holding gain/loss threshold
- Sector allocation exceeds X%
- Diversification score below threshold
- Rebalancing suggestion (premium)

**Free Tier**: 3 active portfolio alerts  
**Premium**: 15 active portfolio alerts  
**Pro**: Unlimited + auto-rebalancing suggestions

**Example Notifications**:
- "Your portfolio is up 12.5%, crossing your +10% alert"
- "TSLA position now 25% of portfolio (alert set at 20%)"
- "Technology sector is 45% of portfolio (exceeds 40% threshold)"

### F. Volume Alerts
**Purpose**: Notify about unusual trading activity

**Conditions**:
- Volume > 2x average (unusual activity)
- Volume > 5x average (significant activity)
- Volume spike in specific time window

**Free Tier**: Not available  
**Premium**: 10 active volume alerts  
**Pro**: 50 active volume alerts

**Example Notifications**:
- "TSLA volume is 3.2x average (65M vs 20M avg)"
- "Unusual activity detected in NVDA (5.1x average volume)"

### G. Cultural Alpha Alerts (Identity-Specific)
**Purpose**: Notify about identity-relevant opportunities

**Conditions**:
- Diaspora: International expansion, emerging markets, forex events
- Youth: ETF launches, beginner-friendly companies, educational events
- Creator: Creator economy companies, platform updates, monetization
- Legacy: Dividend aristocrats, blue-chip upgrades, estate planning

**Free Tier**: 2 active Cultural Alpha alerts  
**Premium**: 10 active Cultural Alpha alerts  
**Pro**: Unlimited + personalized recommendations

**Example Notifications** (Diaspora):
- "V expanded payment network to 3 Caribbean countries"
- "Emerging markets ETF (EEM) up 8% this month"

**Example Notifications** (Youth):
- "New low-cost S&P 500 ETF launched: VOO (0.03% fee)"
- "Educational webinar: Getting Started with Index Funds"

**Example Notifications** (Creator):
- "SHOP released new creator tools for digital products"
- "YouTube announced 45% revenue share for Shorts creators"

**Example Notifications** (Legacy):
- "JNJ increased dividend for 61st consecutive year"
- "BRK.B added to dividend aristocrats list"

---

## 13.3 Screen 1 — Alerts Dashboard

### Purpose
Central hub showing all active alerts, recent triggers, and quick creation.

### Layout
```
┌─────────────────────────────────────────────────────┐
│  🔔 Alerts Center                    [+ Create]     │
├─────────────────────────────────────────────────────┤
│  📊 Summary                                          │
│  • 12 active alerts  • 3 triggered today            │
│  • 3 of 5 price alerts used (Free)                  │
├─────────────────────────────────────────────────────┤
│  🔴 Recent Triggers (Last 24 Hours)                 │
│                                                      │
│  [Price Alert]  AAPL → $185.50                      │
│  Above target ($185.00) • 2 hours ago               │
│  ───────────────────────────────────────────────    │
│  [News Alert]  NVDA • 4 new articles                │
│  Verified news (avg score: 87) • 5 hours ago        │
│  ───────────────────────────────────────────────    │
│  [Earnings Alert]  GOOGL • Q4 Earnings Released     │
│  Revenue $86B vs $85B expected • Yesterday          │
├─────────────────────────────────────────────────────┤
│  ⚡ Active Alerts (12)                               │
│                                                      │
│  [Price Alert]  TSLA  ↓ Below $220                  │
│  Current: $245.80 • Created Dec 20                  │
│  [Edit] [Delete] [Pause]                            │
│  ───────────────────────────────────────────────    │
│  [News Alert]  AAPL  📰 Any verified news           │
│  Min score: 80 • Created Dec 18                     │
│  [Edit] [Delete] [Pause]                            │
│  ───────────────────────────────────────────────    │
│  [Dividend Alert]  JPM  💰 Ex-date approaching      │
│  Dec 27 (3 days) • Created Dec 15                   │
│  [Edit] [Delete] [Pause]                            │
├─────────────────────────────────────────────────────┤
│  📜 Alert History  →  [View All]                    │
└─────────────────────────────────────────────────────┘
```

### Content
- **Summary Bar**: Active count, triggered count, tier usage
- **Recent Triggers**: Last 24 hours, sorted by time
- **Active Alerts**: All alerts with status indicators
- **Quick Actions**: Create, Edit, Delete, Pause alerts

### States
- **Empty State**: "No alerts created yet. Create your first alert to get started."
- **Loading State**: Skeleton loaders for alerts
- **Error State**: "Unable to load alerts. Retry."

### Actions
- Tap alert → Alert Detail view
- Create → Open Create Alert modal
- Edit → Open Edit Alert modal
- Delete → Confirmation dialog
- Pause → Toggle alert active/paused

### Premium Gates
- Free tier shows "3 of 5 price alerts used"
- Create button shows upgrade prompt when limit reached
- Upgrade banner: "Upgrade to Premium for 50 alerts per type"

---

## 13.4 Screen 2 — Create Alert Modal

### Purpose
Simple wizard for creating new alerts.

### Step 1: Choose Alert Type
```
┌─────────────────────────────────────────┐
│  Create New Alert                       │
├─────────────────────────────────────────┤
│  Select Alert Type                      │
│                                          │
│  [ 📈 Price Alert ]                     │
│  Get notified when price crosses        │
│  threshold (3 of 5 used) ⚡              │
│                                          │
│  [ 📰 News Alert ]                      │
│  Get notified about verified news       │
│  (3 of 3 used) 🔒 Premium               │
│                                          │
│  [ 💼 Earnings Alert ]                  │
│  Get notified about earnings events     │
│  (5 of 10 used)                         │
│                                          │
│  [ 💰 Dividend Alert ]                  │
│  Get notified about dividend events     │
│  (2 of 5 used)                          │
│                                          │
│  [ 📊 Portfolio Alert ]                 │
│  Get notified about portfolio changes   │
│  (1 of 3 used)                          │
│                                          │
│  [ 🎯 Cultural Alpha ]  💎              │
│  Identity-specific opportunities        │
│  (Premium) 🔒                           │
└─────────────────────────────────────────┘
```

### Step 2A: Configure Price Alert
```
┌─────────────────────────────────────────┐
│  ← Back       Price Alert               │
├─────────────────────────────────────────┤
│  Stock Symbol                            │
│  [AAPL___________] 🔍                   │
│  Apple Inc. • Current: $185.25          │
│                                          │
│  Condition                               │
│  ( ) Above  ( ) Below                   │
│  (•) % Change Up  ( ) % Change Down     │
│                                          │
│  Target                                  │
│  [5______]%                             │
│                                          │
│  Alert Name (Optional)                   │
│  [AAPL +5% Daily Gain____________]     │
│                                          │
│  Notification Preferences               │
│  [✓] Push notification                  │
│  [✓] Email                              │
│  [ ] SMS (Pro only) 🔒                  │
│                                          │
│         [Cancel]  [Create Alert]        │
└─────────────────────────────────────────┘
```

### Step 2B: Configure News Alert
```
┌─────────────────────────────────────────┐
│  ← Back       News Alert                │
├─────────────────────────────────────────┤
│  Watch Type                              │
│  (•) Specific Company                   │
│  ( ) Category (earnings, M&A, etc.)     │
│  ( ) Any verified news (Pro) 🔒         │
│                                          │
│  Stock Symbol                            │
│  [NVDA__________] 🔍                    │
│  NVIDIA Corporation                      │
│                                          │
│  Minimum Verification Score              │
│  [────●────────────] 75                 │
│  (Higher = more sources)                │
│                                          │
│  Notification Preferences               │
│  [✓] Push notification                  │
│  [ ] Email (Premium) 🔒                 │
│  [ ] Daily digest (Pro) 🔒              │
│                                          │
│         [Cancel]  [Create Alert]        │
└─────────────────────────────────────────┘
```

### Step 2C: Configure Portfolio Alert
```
┌─────────────────────────────────────────┐
│  ← Back       Portfolio Alert           │
├─────────────────────────────────────────┤
│  Alert Condition                         │
│  (•) Total Portfolio Gain/Loss          │
│  ( ) Individual Holding                 │
│  ( ) Sector Allocation                  │
│  ( ) Diversification Score              │
│                                          │
│  Threshold                               │
│  (•) Gain above  ( ) Loss below         │
│  [10_____]%                             │
│                                          │
│  Portfolio                               │
│  [My Main Portfolio ▼]                  │
│  Current value: $12,450                 │
│  Current gain: +8.2%                    │
│                                          │
│  Notification Preferences               │
│  [✓] Push notification                  │
│  [✓] Email                              │
│                                          │
│         [Cancel]  [Create Alert]        │
└─────────────────────────────────────────┘
```

### Validation Rules
- Stock symbol must exist
- Target price/percent must be valid number
- At least one notification method selected
- Alert name <= 100 characters

### Error Messages
- "Invalid stock symbol. Please enter a valid ticker."
- "Target must be a positive number."
- "You've reached your alert limit. Upgrade to Premium for more."
- "This stock is not supported yet. Try another."

---

## 13.5 Screen 3 — Alert Detail View

### Purpose
Show full details, trigger history, and management options.

### Layout
```
┌─────────────────────────────────────────────────────┐
│  ← Back to Alerts                                    │
├─────────────────────────────────────────────────────┤
│  📈 Price Alert                      [Edit] [Delete] │
│                                                      │
│  AAPL → Above $185.00                               │
│  Status: 🟢 Active                                   │
│  Created: Dec 20, 2025                              │
│                                                      │
│  Current Status                                     │
│  ┌─────────────────────────────────────┐           │
│  │  Current Price:  $185.25            │           │
│  │  Target Price:   $185.00            │           │
│  │  Difference:     +$0.25 (0.1%)      │           │
│  │  Status:         Triggered ✅        │           │
│  └─────────────────────────────────────┘           │
│                                                      │
│  📊 Trigger History (3 times)                       │
│                                                      │
│  Dec 24, 2025  2:15 PM                              │
│  Price: $185.50 → Above $185.00                     │
│  ───────────────────────────────────────            │
│  Dec 23, 2025  10:30 AM                             │
│  Price: $186.20 → Above $185.00                     │
│  ───────────────────────────────────────            │
│  Dec 21, 2025  3:45 PM                              │
│  Price: $185.10 → Above $185.00                     │
│                                                      │
│  [View Full History →]                              │
│                                                      │
│  ⚙️ Notification Settings                           │
│  • Push notifications: Enabled                      │
│  • Email: Enabled                                   │
│  • Frequency: Immediate                             │
│                                                      │
│  [Pause Alert]  [Delete Alert]                      │
└─────────────────────────────────────────────────────┘
```

### Content
- Alert type badge (Price, News, Earnings, etc.)
- Target condition with current status
- Real-time comparison (current vs target)
- Trigger history with timestamps
- Notification settings
- Management actions

### Actions
- Edit → Open Edit Alert modal
- Delete → Confirmation: "Delete this alert? This cannot be undone."
- Pause → Toggle active/paused status
- View Full History → Navigate to Alert History page

---

## 13.6 Screen 4 — Alert History

### Purpose
Show all triggered alerts with filtering.

### Layout
```
┌─────────────────────────────────────────────────────┐
│  Alert History                                       │
├─────────────────────────────────────────────────────┤
│  Filters:  [All Types ▼] [Last 7 Days ▼] [Search] │
├─────────────────────────────────────────────────────┤
│  Showing 24 triggered alerts                         │
│                                                      │
│  Today                                               │
│  ───────────────────────────────────────            │
│  2:15 PM  [Price] AAPL → $185.50                    │
│           Above target ($185.00)                    │
│                                                      │
│  9:30 AM  [News] NVDA • 4 new articles              │
│           Verified news (avg score: 87)             │
│                                                      │
│  Yesterday                                           │
│  ───────────────────────────────────────            │
│  4:00 PM  [Earnings] GOOGL • Q4 Released            │
│           Revenue $86B vs $85B expected             │
│                                                      │
│  3:15 PM  [Dividend] JPM • Ex-date in 3 days        │
│           Dec 27 approaching                        │
│                                                      │
│  Dec 22, 2025                                        │
│  ───────────────────────────────────────            │
│  11:45 AM [Portfolio] My Main Portfolio             │
│            Total gain crossed +10% threshold        │
│                                                      │
│  [Load More]                                         │
└─────────────────────────────────────────────────────┘
```

### Filters
- Alert Type: All, Price, News, Earnings, Dividend, Portfolio
- Time Range: Today, Last 7 Days, Last 30 Days, All Time
- Search: Search by symbol, alert name, or keyword

### Export (Pro Only)
- CSV export of trigger history
- Include: timestamp, alert type, symbol, condition, trigger value

---

## 13.7 Identity Variations

### A. Diaspora Identity
**Alert Focus**: International exposure, emerging markets, forex

**Pre-configured Templates**:
- Emerging markets ETF (EEM, VWO) price alerts
- Global payment companies (V, MA, PYPL) news alerts
- Caribbean-focused companies dividend alerts
- Currency pair alerts (USD/JMD, USD/TTD) — Premium

**Cultural Alpha Alerts**:
- "V expanded to Caribbean: Payment network live in Jamaica"
- "Remittance fees dropped 15% for US → Caribbean transfers"

### B. Youth Identity
**Alert Focus**: Beginner-friendly, educational, ETFs

**Pre-configured Templates**:
- S&P 500 ETF (SPY, VOO) price alerts
- Index fund dividend alerts (SCHD, VYM)
- Educational webinar alerts (Vanguard, Fidelity)
- Low-cost fund launches

**Cultural Alpha Alerts**:
- "New beginner guide: How to read earnings reports"
- "VOO reduced expense ratio to 0.02% (lowest in market)"

### C. Creator Identity
**Alert Focus**: Creator economy, platforms, monetization

**Pre-configured Templates**:
- Creator platforms (SHOP, ETSY, META) earnings alerts
- Digital product companies news alerts
- Payment processor (SQ, PYPL, STRIPE) updates
- AI tool companies (MSFT, GOOGL) product launches

**Cultural Alpha Alerts**:
- "SHOP launched AI product description generator for creators"
- "YouTube increased Shorts revenue share to 45%"

### D. Legacy-Builder Identity
**Alert Focus**: Dividends, blue-chips, long-term stability

**Pre-configured Templates**:
- Dividend aristocrats (JNJ, PG, KO) dividend alerts
- Blue-chip companies (BRK.B, JPM, WMT) earnings alerts
- High-yield dividend ETFs (SCHD, VYM) price alerts
- Estate planning companies news alerts

**Cultural Alpha Alerts**:
- "JNJ increased dividend for 62nd consecutive year (+5.2%)"
- "Dividend aristocrat ETF (NOBL) outperformed S&P by 2.1% YTD"

---

## 13.8 Premium Gates

### Free Tier Limits
- 5 price alerts
- 3 news alerts
- 10 earnings alerts
- 5 dividend alerts
- 3 portfolio alerts
- 0 volume alerts
- 2 Cultural Alpha alerts
- Push notifications only
- 30-day trigger history

### Premium Tier ($14.99/mo)
- 50 price alerts
- 20 news alerts
- 100 earnings alerts
- 30 dividend alerts
- 15 portfolio alerts
- 10 volume alerts
- 10 Cultural Alpha alerts
- Push + Email notifications
- 90-day trigger history
- Custom alert names
- Alert templates

### Pro Tier ($29.99/mo)
- Unlimited all alert types
- Push + Email + SMS notifications
- Unlimited trigger history
- CSV export of history
- Alert API access
- Advanced conditions (AND/OR logic)
- Auto-rebalancing alerts
- Real-time earnings alerts
- RSS feed for triggered alerts

### Upgrade Prompts
**When limit reached**:
```
┌─────────────────────────────────────┐
│  🔒 Alert Limit Reached             │
├─────────────────────────────────────┤
│  You've used all 5 price alerts.    │
│  Upgrade to Premium for 50 alerts.  │
│                                      │
│  Premium Benefits:                   │
│  ✓ 50 price alerts                  │
│  ✓ Email notifications              │
│  ✓ Custom alert names               │
│  ✓ 90-day history                   │
│                                      │
│  [Upgrade to Premium — $14.99/mo]   │
│  [View All Plans]                   │
└─────────────────────────────────────┘
```

**When accessing Pro feature**:
```
┌─────────────────────────────────────┐
│  🔒 Pro Feature                     │
├─────────────────────────────────────┤
│  SMS notifications require Pro.     │
│                                      │
│  Pro Benefits:                       │
│  ✓ Unlimited alerts                 │
│  ✓ SMS notifications                │
│  ✓ API access                       │
│  ✓ CSV exports                      │
│                                      │
│  [Upgrade to Pro — $29.99/mo]       │
│  [Learn More]                       │
└─────────────────────────────────────┘
```

---

## 13.9 Alert States

### Alert Lifecycle
```
Created → Active → Triggered → Reset → Active
                              ↓
                          Expired/Deleted
```

### States
1. **Active** (🟢): Monitoring for condition
2. **Triggered** (🔔): Condition met, notification sent
3. **Paused** (⏸️): User paused, not monitoring
4. **Expired** (⏳): Time-based alert expired (e.g., earnings date passed)
5. **Deleted** (🗑️): User deleted, no longer exists
6. **Error** (⚠️): System error, needs retry

### State Indicators
- Active: Green dot, "Monitoring"
- Triggered: Bell icon, "Triggered X times"
- Paused: Pause icon, "Paused"
- Expired: Clock icon, "Expired"
- Error: Warning icon, "Check alert settings"

---

## 13.10 Error States

### Alert Creation Errors
**Invalid Stock Symbol**:
```
❌ Invalid Stock Symbol
The ticker "AAPLE" was not found. Did you mean "AAPL"?
```

**Limit Reached**:
```
🔒 Alert Limit Reached
You've used all 5 price alerts (Free tier).
Upgrade to Premium for 50 price alerts.
[Upgrade Now]
```

**Invalid Target**:
```
⚠️ Invalid Target
Price target must be a positive number between $0.01 and $999,999.
```

### Alert Monitoring Errors
**Data Unavailable**:
```
⚠️ Data Temporarily Unavailable
Unable to check alert condition. Will retry automatically.
Alert: AAPL → Above $185.00
```

**API Error**:
```
❌ API Connection Error
Unable to fetch real-time data for TSLA.
Your alert is paused until connection is restored.
[Retry Now]
```

### Empty States
**No Alerts Created**:
```
┌─────────────────────────────────────┐
│         🔔                          │
│   No Alerts Yet                     │
│                                      │
│   Get notified about price changes, │
│   news, earnings, and more.         │
│                                      │
│   [Create Your First Alert]         │
└─────────────────────────────────────┘
```

**No Triggers in History**:
```
┌─────────────────────────────────────┐
│         📭                          │
│   No Triggered Alerts               │
│                                      │
│   Your alerts haven't triggered yet.│
│   We'll notify you when they do.    │
└─────────────────────────────────────┘
```

---

## 13.11 Notification Examples

### Price Alert (Push)
```
📈 AAPL Price Alert
$185.50 → Above your target of $185.00
Tap to view details
```

### News Alert (Email)
```
Subject: 📰 NVDA News Alert — 4 New Articles

Hi [Name],

Your news alert for NVDA triggered:

• 4 new verified articles (avg verification: 87/100)
• "NVIDIA announces new AI chip architecture"
• "NVIDIA partners with automotive manufacturers"
• "Analysts note strong Q4 performance"
• "Supply chain concerns ease for semiconductor sector"

View all articles: [Link to News Verification Center]

---
Descriptive news only. Not financial advice.
Manage alerts: [Link to Alerts Center]
```

### Earnings Alert (Push)
```
💼 GOOGL Earnings Released
Q4 2025: Revenue $86B (expected $85B)
Descriptive data only. Tap for details.
```

### Dividend Alert (SMS — Pro Only)
```
💰 JPM Dividend Alert
Ex-dividend date: Dec 27 (3 days away)
$1.10 per share
```

### Portfolio Alert (Push)
```
📊 Portfolio Alert
Your Main Portfolio crossed +10%
Current gain: +12.5% ($1,250)
Tap to view portfolio
```

### Cultural Alpha Alert — Diaspora (Email)
```
Subject: 🌍 Cultural Alpha Alert — Caribbean Expansion

Hi [Name],

A diaspora-relevant opportunity:

Visa (V) expanded payment network to 3 Caribbean countries:
• Jamaica
• Trinidad & Tobago
• Barbados

This enables easier cross-border payments and remittances.

Current V price: $245.80
View stock details: [Link]

---
Descriptive information only. Not financial advice.
```

---

## 13.12 System Dependencies

### Internal Dependencies
1. **Stock Data Service** (real-time prices, volume)
2. **News Verification Center** (verified article feed)
3. **Portfolio Module** (portfolio performance data)
4. **Identity Service** (user persona, Cultural Alpha targeting)
5. **Notification Service** (push, email, SMS delivery)
6. **User Preferences** (notification settings, tier limits)

### External Dependencies
1. **Alpha Vantage API** (real-time stock data)
2. **Polygon.io API** (market data, earnings dates)
3. **NewsAPI.org** (news aggregation)
4. **Firebase Cloud Messaging** (push notifications)
5. **SendGrid** (email delivery)
6. **Twilio** (SMS delivery — Pro only)
7. **Redis** (alert condition caching)
8. **Celery** (background job queue for monitoring)

### Background Jobs
**Alert Monitoring Job** (runs every 1 minute):
```python
@celery.task
def check_price_alerts():
    """Check all active price alerts against current prices"""
    active_alerts = get_active_price_alerts()
    for alert in active_alerts:
        current_price = get_current_price(alert.symbol)
        if condition_met(alert, current_price):
            trigger_alert(alert)
            send_notification(alert.user_id, alert)
```

**News Monitoring Job** (runs every 5 minutes):
```python
@celery.task
def check_news_alerts():
    """Check for new verified news matching alert criteria"""
    active_alerts = get_active_news_alerts()
    new_articles = get_recent_verified_news(since=5_minutes_ago)
    for alert in active_alerts:
        matching_articles = filter_by_symbol_and_score(
            new_articles, 
            alert.symbol, 
            alert.min_score
        )
        if len(matching_articles) >= alert.article_threshold:
            trigger_alert(alert, matching_articles)
```

**Earnings Monitoring Job** (runs every 1 hour):
```python
@celery.task
def check_earnings_alerts():
    """Check upcoming and released earnings"""
    active_alerts = get_active_earnings_alerts()
    for alert in active_alerts:
        earnings_data = get_earnings_data(alert.symbol)
        
        # 7-day reminder
        if days_until_earnings(earnings_data) == 7:
            trigger_alert(alert, '7_day_reminder', earnings_data)
        
        # 1-day reminder
        elif days_until_earnings(earnings_data) == 1:
            trigger_alert(alert, '1_day_reminder', earnings_data)
        
        # Released (real-time)
        elif earnings_just_released(earnings_data):
            trigger_alert(alert, 'released', earnings_data)
```

---

## 13.13 Database Schema

### Table: `alerts`
```sql
id              UUID PRIMARY KEY
user_id         UUID NOT NULL (FK to users)
alert_type      ENUM ('price', 'news', 'earnings', 'dividend', 'portfolio', 'volume', 'cultural_alpha')
symbol          VARCHAR(10) (stock ticker, nullable for portfolio/cultural alerts)
condition_type  VARCHAR(50) ('above', 'below', 'percent_up', 'percent_down', 'any_news', etc.)
target_value    DECIMAL (price target or percent threshold)
min_verification_score INT (for news alerts, default 75)
alert_name      VARCHAR(100) (optional custom name)
status          ENUM ('active', 'triggered', 'paused', 'expired', 'deleted', 'error')
trigger_count   INT DEFAULT 0
last_triggered_at TIMESTAMP
notification_push   BOOLEAN DEFAULT TRUE
notification_email  BOOLEAN DEFAULT FALSE
notification_sms    BOOLEAN DEFAULT FALSE (Pro only)
created_at      TIMESTAMP DEFAULT NOW()
updated_at      TIMESTAMP DEFAULT NOW()
```

### Table: `alert_triggers`
```sql
id              UUID PRIMARY KEY
alert_id        UUID NOT NULL (FK to alerts)
triggered_at    TIMESTAMP DEFAULT NOW()
trigger_value   DECIMAL (actual price/value when triggered)
trigger_data    JSON (additional context: articles, earnings data, etc.)
notification_sent BOOLEAN DEFAULT FALSE
notification_sent_at TIMESTAMP
```

### Table: `user_alert_preferences`
```sql
user_id         UUID PRIMARY KEY (FK to users)
identity_type   VARCHAR(20) ('diaspora', 'youth', 'creator', 'legacy')
default_notification_push  BOOLEAN DEFAULT TRUE
default_notification_email BOOLEAN DEFAULT FALSE
default_notification_sms   BOOLEAN DEFAULT FALSE
quiet_hours_start TIME (e.g., '22:00:00')
quiet_hours_end   TIME (e.g., '07:00:00')
timezone        VARCHAR(50) DEFAULT 'America/New_York'
digest_frequency ENUM ('never', 'daily', 'weekly') DEFAULT 'never'
created_at      TIMESTAMP DEFAULT NOW()
updated_at      TIMESTAMP DEFAULT NOW()
```

---

## 13.14 API Endpoints

### Alert CRUD
- `GET /api/alerts/` — List all alerts (paginated, filtered)
- `POST /api/alerts/` — Create new alert
- `GET /api/alerts/<id>` — Get alert details
- `PATCH /api/alerts/<id>` — Update alert (edit)
- `DELETE /api/alerts/<id>` — Delete alert
- `POST /api/alerts/<id>/pause` — Pause alert
- `POST /api/alerts/<id>/resume` — Resume alert

### Alert Triggers
- `GET /api/alerts/<id>/triggers` — Get trigger history
- `GET /api/alerts/triggers/recent` — Get recent triggers (all alerts)
- `POST /api/alerts/<id>/test` — Test alert (manual trigger)

### Alert Management
- `GET /api/alerts/summary` — Get usage summary (count by type, tier limits)
- `GET /api/alerts/templates` — Get pre-configured templates (identity-aware)
- `GET /api/alerts/limits` — Get tier limits for current user

### User Preferences
- `GET /api/alerts/preferences` — Get user alert preferences
- `PATCH /api/alerts/preferences` — Update preferences

---

## 13.15 Compliance & Safety

### Notification Language Rules
**Allowed**:
- "AAPL is now $185.50, above your target"
- "GOOGL released Q4 earnings: Revenue $86B"
- "JPM ex-dividend date is Dec 27"
- "Your portfolio crossed +10% gain"

**Forbidden**:
- ❌ "You should buy AAPL now"
- ❌ "This will likely go higher"
- ❌ "Sell before earnings"
- ❌ "Great opportunity to invest"

### Descriptive-Only Enforcement
- All notifications describe events and data
- No predictions or future-tense language
- No recommendations or advice
- No emotional language ("amazing", "terrible")

### Cultural Alpha Compliance
- Identity-relevant opportunities described factually
- No pressure to act
- Clear statement: "Descriptive information only. Not financial advice."

---

## 13.16 Testing Scenarios

### Functional Tests
1. Create price alert → verify appears in active list
2. Stock crosses threshold → verify alert triggers
3. Notification sent → verify push/email delivery
4. Edit alert → verify changes saved
5. Delete alert → verify removed from active list
6. Pause alert → verify not monitoring
7. Resume alert → verify monitoring resumes

### Edge Cases
1. Alert created for invalid symbol → error message
2. Alert created at tier limit → upgrade prompt
3. Stock price equals target exactly → should trigger
4. Alert triggered multiple times in 1 minute → only 1 notification
5. User deletes alert while it's triggering → handle gracefully
6. API down during monitoring → log error, retry automatically

### Premium Gate Tests
1. Free user creates 6th price alert → upgrade prompt
2. Free user tries SMS notification → Pro upgrade prompt
3. Premium user accesses volume alerts → allowed
4. Premium user tries API access → Pro upgrade prompt

---

## 13.17 Implementation Priority

### Phase 1: Core Alerts (Week 1)
- Database models
- Price alerts (above/below)
- Basic UI (dashboard, create modal)
- Push notifications
- Celery monitoring jobs

### Phase 2: News & Earnings (Week 2)
- News alerts (News Verification Center integration)
- Earnings alerts (Alpha Vantage integration)
- Alert history view
- Email notifications

### Phase 3: Premium Features (Week 3)
- Dividend alerts
- Portfolio alerts
- Tier limits enforcement
- Upgrade prompts

### Phase 4: Advanced (Week 4)
- Volume alerts (Premium)
- Cultural Alpha alerts
- SMS notifications (Pro)
- CSV export (Pro)
- Alert templates

---

## 13.18 Success Metrics

### User Engagement
- % of users with ≥1 active alert
- Avg alerts per user (by tier)
- Alert creation rate (per week)
- Alert trigger rate (% of alerts that trigger)

### Notification Effectiveness
- Notification open rate (push)
- Notification click-through rate
- Email open rate
- SMS delivery rate (Pro)

### Premium Conversion
- % of users who upgrade after hitting limit
- Tier upgrade rate (free → premium → pro)
- Alert limit as conversion trigger

### Reliability
- Alert monitoring uptime (target: 99.9%)
- Notification delivery success rate (target: 99%)
- False trigger rate (target: <0.1%)
- Trigger latency (target: <2 minutes from condition met)

---

## 13.19 Future Enhancements

### Advanced Conditions
- AND/OR logic: "AAPL above $180 AND volume > 50M"
- Time-based conditions: "Alert me if TSLA gains 5% before noon"
- Relative conditions: "Alert me if NVDA outperforms SPY by 2%"

### AI-Powered Alerts
- Smart suggestions: "Based on your portfolio, consider setting dividend alerts for JPM and KO"
- Pattern recognition: "AAPL has triggered this alert 5 times in the last month"
- Anomaly detection: "Unusual pattern detected: TSLA volume spiked 10x average"

### Social Features
- Share alert templates with other users
- Community alert templates (most popular)
- Alert performance leaderboard (most accurate triggers)

### Integration
- Webhook support (Pro): POST to custom URL when alert triggers
- Zapier integration: Connect alerts to 1000+ apps
- IFTTT integration: "If AAPL above $200, then turn on smart lights"

---

**END OF SECTION 13 SPECIFICATION**

🔥 **The Alerts Center: Your Personal Signal Hub** 👑
