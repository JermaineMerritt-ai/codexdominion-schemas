# Cross-Promotion Engine - Behavioral Integration Guide

## Overview
This guide explains how behavioral tracking refines identity-based cross-promotion in DominionMarkets.

**Core Principle:** Cross-promotion is NEVER random. It's always tied to Identity + Behavior + Context + Goals.

---

## Behavioral Tracking

### What We Track (Non-Sensitive)
✅ **Stocks viewed** - Symbol frequency (AAPL: 5 times, TSLA: 3 times)
✅ **Sectors explored** - Technology, finance, healthcare
✅ **News categories read** - Earnings, markets, analysis
✅ **Portfolio checks** - Daily/weekly frequency
✅ **AI summary usage** - How often user leverages AI insights
✅ **Alert creation patterns** - Volume and types of alerts

### What We DON'T Track
❌ Dollar amounts or specific holdings
❌ Transaction details
❌ Personal identifying information
❌ Cross-site behavior

---

## Behavioral Refinement Examples

### Example 1: Creator Identity + Creator Behavior
**User Profile:**
- Identity: Creator
- Viewed: SHOP (5x), ETSY (3x), META (2x) this week
- Read: 4 creator-economy news articles
- Created: 8 alerts on creator stocks

**Behavioral Score:**
```python
creator_score = (
    creator_stocks_viewed * 2 +  # 10 * 2 = 20
    creator_news_read * 3         # 4 * 3 = 12
) = 32
```

**Result:** Show "Creator Economy Analytics Dashboard" with high priority

### Example 2: Youth Identity + Beginner Behavior
**User Profile:**
- Identity: Youth
- Portfolio value: $800
- Read: 6 beginner articles
- Mock portfolio usage: 10 sessions
- Portfolio checks: 3x today

**Behavioral Score:**
```python
youth_score = (
    beginner_articles_read * 3 +  # 6 * 3 = 18
    mock_portfolio_usage * 4       # 10 * 4 = 40
) = 58
```

**Result:** Show "Paper Trading Simulator" and "First Portfolio Challenge"

### Example 3: Diaspora Identity + Diaspora Behavior
**User Profile:**
- Identity: Diaspora
- Read: 8 diaspora news articles this week
- Holds: 3 international ETFs
- Viewed: Caribbean markets 5x

**Behavioral Score:**
```python
diaspora_score = (
    diaspora_news_read * 3 +           # 8 * 3 = 24
    international_stocks_viewed * 2     # 8 * 2 = 16
) = 40
```

**Result:** Show "Diaspora Flow Maps Pro" and "Caribbean Investment Tracker"

### Example 4: Legacy Identity + Dividend Behavior
**User Profile:**
- Identity: Legacy
- Holds: 5 dividend aristocrats
- Viewed: JNJ, PG, KO (dividend stocks) 12x total
- Read: 5 dividend news articles

**Behavioral Score:**
```python
legacy_score = (
    dividend_stocks_viewed * 2 +  # 12 * 2 = 24
    dividend_news_read * 3         # 5 * 3 = 15
) = 39
```

**Result:** Show "Retirement Income Planner" and "Dividend Aristocrats Tracker"

---

## Placement Location Logic

### Location 1: Dashboard (Right Sidebar)
**Context:** General overview, identity-focused
**Behavior Used:**
- Top 5 stocks viewed this week
- Creator/diaspora/youth/legacy scores
- Alert count

**Example Promotions:**
- Diaspora user + 8 diaspora news read → "Diaspora Flow Maps Pro"
- Youth user + portfolio < $1000 → "First Portfolio Challenge"

### Location 2: News Verification Center
**Context:** Reading specific news article
**Behavior Used:**
- News category being read (earnings, markets, etc.)
- Is diaspora-related article?
- Is creator platform article?

**Example Promotions:**
- Reading diaspora article → "Related diaspora economic story"
- Reading creator earnings → "Creator-economy deep-dive"

### Location 3: Portfolio Module
**Context:** Viewing holdings and analytics
**Behavior Used:**
- Portfolio value
- Dividend stock count
- Creator stock exposure
- Sector concentration

**Example Promotions:**
- 3+ dividend stocks → "Your dividend allocation" + Retirement Planner link
- High creator exposure → "Your creator-economy exposure" + Creator Tracker link

### Location 4: Markets Module
**Context:** Exploring sectors and heatmaps
**Behavior Used:**
- Sectors viewed this session
- Stocks clicked
- International holdings detected

**Example Promotions:**
- Viewing technology sector + creator identity → "AI-tool sector deep-dive"
- Viewing Caribbean companies → "Companies with Caribbean exposure"

### Location 5: Premium Upsell Pages
**Context:** Considering upgrade
**Behavior Used:**
- Feature being locked (CSV export, multi-portfolio, etc.)
- User tier
- Alert count (if hitting limits)

**Example Promotions:**
- Premium CSV export locked → "Download Legacy Portfolio Template" (one-time alternative)
- Alert limit reached → "Try Workflow Automation" (ecosystem solution)

---

## API Integration

### Frontend: Track User Activity
```typescript
// Track stock view
await fetch('/api/promotions/behavior/track', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    activity_type: 'stock_view',
    metadata: { symbol: 'AAPL' }
  })
});

// Track news read
await fetch('/api/promotions/behavior/track', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    activity_type: 'news_read',
    metadata: {
      category: 'earnings',
      is_creator: true,
      is_diaspora: false
    }
  })
});

// Track portfolio check
await fetch('/api/promotions/behavior/track', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    activity_type: 'portfolio_check'
  })
});
```

### Frontend: Get Behavioral Context
```typescript
const behaviorContext = await fetch('/api/promotions/behavior/recent')
  .then(res => res.json());

// Use in promotion selection
const promotions = await fetch(
  `/api/promotions?location=dashboard&identity=creator&tier=free&context=${JSON.stringify(behaviorContext)}`
).then(res => res.json());
```

### Backend: Behavioral Scoring
```python
from services.behavior_tracker import BehaviorTracker

tracker = BehaviorTracker()

# Calculate relevance for a promotion
behavioral_score = tracker.calculate_behavioral_relevance(
    user_id="user_123",
    promotion_identity="creator"
)

# Returns 0-100 based on recent activity
# Higher = better fit
```

---

## Database Schema

### user_behaviors Table
```sql
CREATE TABLE user_behaviors (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    
    -- Activity Counters (rolling 7 days)
    stocks_viewed JSONB,  -- {"AAPL": 5, "TSLA": 3}
    sectors_viewed JSONB,  -- {"technology": 10, "finance": 5}
    news_categories_read JSONB,  -- {"earnings": 8, "markets": 12}
    
    -- Frequency Metrics
    portfolio_checks_today INT DEFAULT 0,
    portfolio_checks_this_week INT DEFAULT 0,
    news_views_this_week INT DEFAULT 0,
    ai_summary_usage_today INT DEFAULT 0,
    alert_count INT DEFAULT 0,
    
    -- Identity Detection Scores
    creator_stocks_viewed INT DEFAULT 0,
    creator_news_read INT DEFAULT 0,
    diaspora_news_read INT DEFAULT 0,
    international_stocks_viewed INT DEFAULT 0,
    beginner_articles_read INT DEFAULT 0,
    mock_portfolio_usage INT DEFAULT 0,
    dividend_stocks_viewed INT DEFAULT 0,
    dividend_news_read INT DEFAULT 0,
    
    last_activity TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

---

## Privacy & Compliance

### What Users See
- Transparent tracking explanation in Settings
- "We track stocks viewed, news read, and activity patterns to improve recommendations"
- "No personal financial data or dollar amounts are tracked"
- Export behavior data (Pro tier)
- Delete all behavior data on account deletion

### What We Never Do
- Share behavior data with third parties
- Track across sites/apps
- Store PII in behavior records
- Track specific holdings or transactions
- Sell or monetize behavior data

---

## Scheduled Jobs

### Daily Reset (Midnight UTC)
```python
from services.behavior_tracker import BehaviorTracker

tracker = BehaviorTracker()
for user_id in active_users:
    tracker.reset_daily_counters(user_id)
```

Resets:
- portfolio_checks_today
- ai_summary_usage_today

### Weekly Reset (Sunday Midnight UTC)
```python
tracker.reset_weekly_counters(user_id)
```

Resets:
- portfolio_checks_this_week
- news_views_this_week

Decays by 50%:
- All identity detection scores (creator, diaspora, youth, legacy)

---

## Testing Behavioral Scoring

### Test Case 1: Creator Behavior Detection
```python
# Simulate creator behavior
tracker.track_stock_view(user_id, 'SHOP')  # 5 times
tracker.track_stock_view(user_id, 'ETSY')  # 3 times
tracker.track_news_read(user_id, 'earnings', is_creator=True)  # 4 times

# Check score
score = tracker.calculate_behavioral_relevance(user_id, 'creator')
assert score >= 20  # Should boost creator promotions
```

### Test Case 2: Youth Behavior Detection
```python
tracker.track_portfolio_check(user_id)  # 3 times today
# Mock portfolio usage tracked separately
behavior.mock_portfolio_usage = 10

score = tracker.calculate_behavioral_relevance(user_id, 'youth')
assert score >= 30  # Should boost youth promotions
```

---

## Summary

**Cross-Promotion = Identity + Behavior + Context + Goals**

- **Identity** determines base eligibility (Diaspora/Youth/Creator/Legacy)
- **Behavior** refines recommendations (what they actually do)
- **Context** determines placement (Dashboard/News/Portfolio/Markets/Premium)
- **Goals** guide CTA copy (explore, learn, track, optimize)

**Result:** Highly relevant, non-intrusive ecosystem connections that feel natural.

🔥 **Behavioral refinement makes cross-promotion smarter, not nosier!**
