# SECTION 12 — NEWS VERIFICATION CENTER (FULL SPECIFICATION)
**DominionMarkets Trust Engine for Financial News**

**Last Updated:** December 24, 2025  
**Status:** Implementation In Progress

---

## 🎯 Overview

The News Verification Center is DominionMarkets' trust engine — delivering verified, multi-source financial news without predictions, advice, or sensationalism. Every article is scored for accuracy, cross-referenced against multiple sources, and flagged for conflicts or bias.

### Core Principles
1. **Verification Over Speed** - Accuracy trumps being first
2. **Multi-Source Validation** - No single source is gospel
3. **Transparency** - Show the methodology, not just the score
4. **Compliance** - Descriptive reporting only (no advice/predictions)
5. **Identity-Aware** - Relevant topics surfaced for each user type

---

## 📊 Full Flow Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     NEWS INGESTION PIPELINE                   │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌─────────────────────────────────────────┐
         │  1. Article Discovery (RSS/API)         │
         │     - Bloomberg, Reuters, WSJ, etc.     │
         │     - 15+ financial news sources        │
         └─────────────────────────────────────────┘
                              │
                              ▼
         ┌─────────────────────────────────────────┐
         │  2. Content Extraction & Parsing        │
         │     - Title, summary, full text         │
         │     - Author, timestamp, source         │
         │     - Ticker symbols extraction         │
         └─────────────────────────────────────────┘
                              │
                              ▼
         ┌─────────────────────────────────────────┐
         │  3. Multi-Source Verification           │
         │     - Find same story across sources    │
         │     - Compare facts, figures, quotes    │
         │     - Detect conflicts & discrepancies  │
         └─────────────────────────────────────────┘
                              │
                              ▼
         ┌─────────────────────────────────────────┐
         │  4. Verification Scoring (0-100)        │
         │     - Source count: 0-30 points         │
         │     - Agreement: 0-40 points            │
         │     - Source quality: 0-30 points       │
         └─────────────────────────────────────────┘
                              │
                              ▼
         ┌─────────────────────────────────────────┐
         │  5. Compliance Filtering (Premium)      │
         │     - Remove predictions/advice         │
         │     - Flag sensational language         │
         │     - Sentiment analysis (neutral only) │
         └─────────────────────────────────────────┘
                              │
                              ▼
         ┌─────────────────────────────────────────┐
         │  6. Identity-Aware Tagging              │
         │     - Diaspora: Int'l markets, forex    │
         │     - Youth: ETFs, beginner topics      │
         │     - Creator: IPOs, tech stocks        │
         │     - Legacy: Dividends, value stocks   │
         └─────────────────────────────────────────┘
                              │
                              ▼
         ┌─────────────────────────────────────────┐
         │  7. Database Storage & Indexing         │
         │     - PostgreSQL for metadata           │
         │     - Full-text search ready            │
         │     - Ticker associations               │
         └─────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                       USER INTERFACE FLOWS                    │
└──────────────────────────────────────────────────────────────┘

```

---

## 🖼️ Every Screen & State

### Screen 1: News Feed (Main View)

**URL:** `/news`

**States:**
- Loading (skeleton cards)
- Empty (no articles found)
- Filtered (by source, category, ticker, verification level)
- Identity-sorted (diaspora/youth/creator/legacy-builder prioritization)

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  🔍 Search: "Tesla earnings"    [Filters ▼] [Sources ▼]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📰 TOP VERIFIED STORIES                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ✅ 95/100  Fed Raises Interest Rates by 0.25%       │   │
│  │ 🕐 2 hours ago  •  8 sources  •  Bloomberg, Reuters │   │
│  │ The Federal Reserve increased rates for the third   │   │
│  │ consecutive quarter, citing persistent inflation... │   │
│  │ [Read More]                              [Bookmark] │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ⚠️ 62/100  Tesla Stock Surges 10% on Delivery News  │   │
│  │ 🕐 4 hours ago  •  3 sources  •  CNBC, MarketWatch  │   │
│  │ [CONFLICT] Some sources report 8% gain vs 10%       │   │
│  │ [Read More]                              [Bookmark] │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  🎯 RELEVANT FOR YOU (Youth Investor)                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ✅ 88/100  Beginner's Guide to Index Funds          │   │
│  │ 🕐 1 day ago  •  5 sources  •  WSJ, Forbes          │   │
│  │ [Read More]                              [Bookmark] │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Load More Articles]                                       │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
- Verification badge (✅ 95/100, ⚠️ 62/100, ❌ <50)
- Source count & list
- Conflict warnings
- Identity-aware sections
- Filter sidebar (collapsible on mobile)

---

### Screen 2: Article Detail View

**URL:** `/news/<article-id>`

**States:**
- Loading article
- Article loaded + verification panel
- Premium content locked (blur overlay for free users)
- Verification failed (show warnings)
- Related articles loading

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  ← Back to News Feed                          [Bookmark] [Share] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Fed Raises Interest Rates by 0.25%                        │
│  ✅ Verification Score: 95/100  •  8 sources  •  2 hours ago │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 📊 VERIFICATION PANEL                               │   │
│  │ ┌───────────────────────────────────────────────┐   │   │
│  │ │ ✅ Source Count: 8/10 sources (30/30 pts)     │   │   │
│  │ │ ✅ Agreement: 95% consensus (38/40 pts)       │   │   │
│  │ │ ✅ Source Quality: High trust (27/30 pts)     │   │   │
│  │ └───────────────────────────────────────────────┘   │   │
│  │                                                     │   │
│  │ Sources Reporting:                                  │   │
│  │ ✓ Bloomberg (AAA)          ✓ Reuters (AAA)        │   │
│  │ ✓ Wall Street Journal (AA) ✓ Financial Times (AA) │   │
│  │ ✓ CNBC (A)                 ✓ MarketWatch (A)      │   │
│  │ ✓ Yahoo Finance (B)        ✓ Seeking Alpha (B)    │   │
│  │                                                     │   │
│  │ [View Methodology]                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Article Summary:                                           │
│  The Federal Reserve's Federal Open Market Committee        │
│  voted unanimously to increase the federal funds rate       │
│  by 25 basis points to 5.50%-5.75%. This marks the         │
│  third consecutive rate increase this year...               │
│                                                             │
│  Key Facts (Verified):                                      │
│  • Rate increased from 5.25%-5.50% to 5.50%-5.75%          │
│  • Unanimous FOMC vote (12-0)                              │
│  • Inflation target remains 2%                             │
│  • Next meeting scheduled for January 31, 2026            │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🔒 PREMIUM ANALYSIS (Unlock for $14.99/mo)         │   │
│  │ [Blurred preview of AI analysis]                    │   │
│  │ [Upgrade to Premium]                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Related Articles:                                          │
│  • Fed Chair Powell Signals Cautious Approach (✅ 92/100)   │
│  • Market Reacts to Rate Decision (✅ 87/100)               │
│  • Inflation Trends Show Cooling Signs (✅ 90/100)          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
- Verification score badge (large)
- Verification panel (expandable)
- Source list with trust ratings
- Key facts extraction
- Premium AI analysis (gated)
- Related articles carousel

---

### Screen 3: Source Comparison View (Premium)

**URL:** `/news/<article-id>/sources`

**States:**
- Loading sources
- Sources loaded (side-by-side comparison)
- Conflicts highlighted
- Pro users see AI conflict resolution

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  Source Comparison: Fed Rate Decision                      │
│  ⚠️ 2 conflicts detected                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Bloomberg (AAA)          vs    Reuters (AAA)               │
│  ┌─────────────────────────┬─────────────────────────┐     │
│  │ "Fed raises rates       │ "Federal Reserve        │     │
│  │  by 0.25%"              │  hikes rates 25 bps"    │     │
│  │ ✅ Agrees               │ ✅ Agrees               │     │
│  ├─────────────────────────┼─────────────────────────┤     │
│  │ "Unanimous vote 12-0"   │ "Unanimous decision"    │     │
│  │ ✅ Agrees               │ ✅ Agrees               │     │
│  ├─────────────────────────┼─────────────────────────┤     │
│  │ "Inflation at 3.2%"     │ "Inflation at 3.1%"     │     │
│  │ ⚠️ CONFLICT             │ ⚠️ CONFLICT             │     │
│  └─────────────────────────┴─────────────────────────┘     │
│                                                             │
│  🤖 AI Resolution (Pro Only):                               │
│  "Both sources cite different measurement periods.          │
│   Bloomberg references October CPI (3.2%), Reuters          │
│   references September CPI (3.1%). Both are accurate."      │
│                                                             │
│  CNBC (A)                 vs    MarketWatch (A)             │
│  ┌─────────────────────────┬─────────────────────────┐     │
│  │ "Markets rally 2%"      │ "Stocks up 1.8%"        │     │
│  │ ⚠️ Minor conflict       │ ⚠️ Minor conflict       │     │
│  └─────────────────────────┴─────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### Screen 4: Source Trust Center

**URL:** `/news/sources`

**States:**
- All sources list
- User preferences (following/blocked)
- Historical accuracy metrics

**Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  News Sources                [Following (12)] [All (45)]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Tier AAA (Highest Trust)                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Bloomberg                                [Following] │   │
│  │ Trust Score: 98/100  •  Bias: Center                │   │
│  │ Historical Accuracy: 97%  •  2,847 articles verified│   │
│  │ [View Profile]                                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Reuters                                  [Following] │   │
│  │ Trust Score: 97/100  •  Bias: Center                │   │
│  │ Historical Accuracy: 96%  •  3,102 articles verified│   │
│  │ [View Profile]                                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Tier AA (High Trust)                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Wall Street Journal                      [Follow]   │   │
│  │ Trust Score: 94/100  •  Bias: Center-Right          │   │
│  │ Historical Accuracy: 93%  •  1,956 articles verified│   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Show More Sources]                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔬 Verification Logic (Full Algorithm)

### Scoring Formula (0-100 Scale)

```python
def calculate_verification_score(article):
    """
    Multi-factor verification scoring algorithm
    
    Returns: int (0-100)
    """
    
    # Component 1: Source Count (0-30 points)
    # More sources = higher confidence
    source_count = len(article.sources)
    if source_count >= 8:
        source_score = 30
    elif source_count >= 5:
        source_score = 25
    elif source_count >= 3:
        source_score = 20
    elif source_count >= 2:
        source_score = 15
    else:
        source_score = 10
    
    # Component 2: Agreement Level (0-40 points)
    # % of sources agreeing on key facts
    key_facts = extract_key_facts(article)
    agreement_rate = calculate_agreement(key_facts, article.sources)
    if agreement_rate >= 95:
        agreement_score = 40
    elif agreement_rate >= 90:
        agreement_score = 35
    elif agreement_rate >= 80:
        agreement_score = 30
    elif agreement_rate >= 70:
        agreement_score = 25
    elif agreement_rate >= 60:
        agreement_score = 20
    else:
        agreement_score = 15
    
    # Component 3: Source Quality (0-30 points)
    # Weighted by source trust ratings
    source_quality_avg = sum(s.trust_score for s in article.sources) / len(article.sources)
    quality_score = (source_quality_avg / 100) * 30
    
    # Total score
    total_score = source_score + agreement_score + quality_score
    
    return min(int(total_score), 100)
```

### Conflict Detection

```python
def detect_conflicts(article):
    """
    Identify factual discrepancies between sources
    
    Returns: List[Conflict]
    """
    conflicts = []
    
    # Extract numerical claims from each source
    for fact_type in ['numbers', 'percentages', 'dates', 'quotes']:
        claims_by_source = {}
        for source in article.sources:
            claims = extract_claims(source.content, fact_type)
            claims_by_source[source.id] = claims
        
        # Compare claims across sources
        for claim_key in get_common_claim_keys(claims_by_source):
            values = [claims[claim_key] for claims in claims_by_source.values()]
            if not all_agree(values):
                conflicts.append(Conflict(
                    type=fact_type,
                    claim_key=claim_key,
                    values=values,
                    severity='high' if fact_type in ['numbers', 'dates'] else 'low'
                ))
    
    return conflicts
```

### Source Trust Ratings

```python
TRUST_RATINGS = {
    'bloomberg': {'score': 98, 'tier': 'AAA', 'bias': 'center'},
    'reuters': {'score': 97, 'tier': 'AAA', 'bias': 'center'},
    'wsj': {'score': 94, 'tier': 'AA', 'bias': 'center-right'},
    'ft': {'score': 93, 'tier': 'AA', 'bias': 'center'},
    'cnbc': {'score': 87, 'tier': 'A', 'bias': 'center'},
    'marketwatch': {'score': 85, 'tier': 'A', 'bias': 'center'},
    'yahoo_finance': {'score': 78, 'tier': 'B', 'bias': 'center'},
    'seeking_alpha': {'score': 75, 'tier': 'B', 'bias': 'varies'},
    # ... 40+ more sources
}
```

---

## 🎭 Identity Variations

### Diaspora Investors
**Priority Topics:**
- International markets (emerging economies)
- Currency exchange rates
- Cross-border investing
- ADRs (American Depositary Receipts)
- Remittance-related financial news

**UI Adjustments:**
- Badge: "🌍 Relevant for Global Investors"
- Filter: "International Markets" default ON
- Sources: Prioritize Reuters, Financial Times (global focus)

### Youth Investors
**Priority Topics:**
- ETFs and index funds
- Beginner investing guides
- Tech stocks (familiar companies)
- Retirement accounts (401k, IRA basics)
- Student loan financial impact

**UI Adjustments:**
- Badge: "📚 Great for Beginners"
- Explainer tooltips on jargon
- Sources: Forbes, Investopedia prioritized
- Simplified language summaries

### Creator/Entrepreneur
**Priority Topics:**
- IPOs and tech startups
- Creator economy financial news
- Business tax changes
- Small business financing
- Tech sector earnings

**UI Adjustments:**
- Badge: "💡 Creator-Relevant"
- Filter: "Tech & Innovation" default ON
- Sources: TechCrunch, Bloomberg Tech

### Legacy Builders
**Priority Topics:**
- Dividend stocks
- Estate planning changes
- Long-term value investing
- Bond market updates
- Tax-advantaged accounts

**UI Adjustments:**
- Badge: "👑 Legacy Focus"
- Filter: "Income & Preservation" default ON
- Sources: WSJ, Morningstar prioritized

---

## 🔒 Premium Gates

### Free Tier
✅ Access to:
- News feed (all articles)
- Basic verification scores
- Source count
- Bookmark up to 20 articles

❌ Locked:
- AI sentiment analysis
- Bias detection reports
- Historical source accuracy
- Conflict resolution explanations
- Custom alerts

### Premium Tier ($14.99/mo)
✅ Everything in Free, plus:
- AI sentiment analysis per article
- Bias detection (left/center/right indicators)
- Full verification methodology view
- Bookmark unlimited articles
- Email alerts for followed topics

### Pro Tier ($29.99/mo)
✅ Everything in Premium, plus:
- AI conflict resolution explanations
- Historical accuracy tracking per source
- Advanced filtering (by verification score, bias, date range)
- Custom news alerts (ticker-based, keyword-based)
- API access (10,000 requests/month)
- Export articles to PDF

---

## ⚠️ Error & Empty States

### Error States

**1. No Articles Found**
```
┌─────────────────────────────────────┐
│         📭                          │
│   No articles found                 │
│   Try adjusting your filters or     │
│   search for different topics       │
│   [Clear Filters]                   │
└─────────────────────────────────────┘
```

**2. Verification Failed**
```
┌─────────────────────────────────────┐
│         ⚠️                          │
│   Unable to verify this article     │
│   Only 1 source found. We require   │
│   at least 2 sources to generate    │
│   a verification score.             │
│   [View Anyway] [Report Issue]      │
└─────────────────────────────────────┘
```

**3. API Error**
```
┌─────────────────────────────────────┐
│         ❌                          │
│   Failed to load news               │
│   Our news service is temporarily   │
│   unavailable. Please try again.    │
│   [Retry] [View Cached Articles]    │
└─────────────────────────────────────┘
```

**4. Source Conflict (High Severity)**
```
┌─────────────────────────────────────┐
│         🚨                          │
│   Major Conflict Detected           │
│   Sources report conflicting facts: │
│   • Bloomberg: "Stock up 10%"       │
│   • Reuters: "Stock down 5%"        │
│   Verification score lowered to 45. │
│   [View Source Comparison]          │
└─────────────────────────────────────┘
```

### Loading States

**1. Feed Loading**
```
┌─────────────────────────────────────┐
│ ▮▮▮▮▯▯▯▯▯▯  Loading articles...    │
│                                     │
│ [Skeleton card]                     │
│ [Skeleton card]                     │
│ [Skeleton card]                     │
└─────────────────────────────────────┘
```

**2. Article Detail Loading**
```
┌─────────────────────────────────────┐
│ ▮▮▮▯▯▯  Loading verification...    │
│                                     │
│ [Skeleton title]                    │
│ [Skeleton verification panel]       │
│ [Skeleton content]                  │
└─────────────────────────────────────┘
```

### Empty States

**1. No Bookmarks Yet**
```
┌─────────────────────────────────────┐
│         🔖                          │
│   No bookmarked articles yet        │
│   Bookmark articles to read them    │
│   later or reference them quickly.  │
│   [Browse News Feed]                │
└─────────────────────────────────────┘
```

**2. No Sources Followed**
```
┌─────────────────────────────────────┐
│         📰                          │
│   No sources followed yet           │
│   Follow sources to personalize     │
│   your news feed.                   │
│   [Browse Sources]                  │
└─────────────────────────────────────┘
```

---

## 🔧 System Dependencies

### External APIs
1. **NewsAPI.org** - News aggregation
   - Free tier: 100 requests/day
   - Developer tier: $449/mo (unlimited)
   
2. **Alpha Vantage** - Financial news feed
   - Free tier: 5 requests/minute
   - Premium: $49.99/mo (500 req/min)

3. **OpenAI GPT-4** - Sentiment analysis, conflict resolution
   - $0.03 per 1K tokens (input)
   - $0.06 per 1K tokens (output)

### Internal Services
1. **PostgreSQL Database**
   - Tables: news_articles, news_sources, verification_checks, user_bookmarks
   
2. **Redis Cache**
   - Cache verification scores (TTL: 1 hour)
   - Cache article summaries (TTL: 24 hours)

3. **Celery Task Queue**
   - Background verification jobs
   - Source fetching (every 15 minutes)

### Infrastructure Requirements
- **Storage**: ~500MB per 10,000 articles
- **Processing**: 2-5 seconds per article verification
- **API Rate Limits**: 
  - Free users: 100 articles/day
  - Premium: 1,000 articles/day
  - Pro: Unlimited

---

## 📈 Success Metrics

### Verification Quality
- **Target**: 95%+ accuracy on verified articles
- **Benchmark**: Cross-check with fact-checking organizations
- **Method**: Monthly audit of 100 random articles

### User Engagement
- **Target**: 80% of premium users check news daily
- **Target**: Average 5+ articles read per session
- **Target**: 30%+ bookmark rate

### Trust Indicators
- **Target**: 90%+ users trust verification scores
- **Method**: Quarterly user surveys
- **Benchmark**: Compare against traditional news apps

---

## 🚀 Implementation Phases

### Phase 1: Core Engine (Week 1-2)
- [ ] Database models
- [ ] News ingestion pipeline
- [ ] Basic verification algorithm
- [ ] Flask API routes

### Phase 2: UI Foundation (Week 3-4)
- [ ] News feed component
- [ ] Article detail view
- [ ] Verification panel
- [ ] Basic filtering

### Phase 3: Premium Features (Week 5-6)
- [ ] AI sentiment analysis
- [ ] Source comparison view
- [ ] Conflict resolution
- [ ] Premium gates

### Phase 4: Identity Features (Week 7-8)
- [ ] Identity-aware tagging
- [ ] Personalized feed sorting
- [ ] Custom alerts
- [ ] User preferences

### Phase 5: Polish & Launch (Week 9-10)
- [ ] Error states
- [ ] Loading animations
- [ ] Mobile optimization
- [ ] Performance tuning
- [ ] Beta testing

---

## 📝 Compliance Notes

### Content Rules
1. ✅ Descriptive reporting only (what happened)
2. ❌ No predictions ("will rise", "expected to")
3. ❌ No advice ("should buy", "recommend")
4. ❌ No sensationalism ("shocking", "unbelievable")
5. ✅ Attribute all claims to sources

### Disclaimer Template
```
"This news article has been verified against multiple sources 
for factual accuracy. DominionMarkets does not provide financial 
advice or predictions. All information is descriptive and for 
informational purposes only."
```

---

**Status**: 🎯 Ready for Implementation  
**Estimated Completion**: 10 weeks  
**Team Size**: 2-3 developers + 1 QA  

🔥 **The Flame Burns Sovereign and Eternal!** 👑
