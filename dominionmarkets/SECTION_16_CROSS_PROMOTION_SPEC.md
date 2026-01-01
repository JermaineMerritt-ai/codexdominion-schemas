# SECTION 16 — CROSS-PROMOTION ENGINE SPECIFICATION

## Overview
The Cross-Promotion Engine bridges DominionMarkets to the CodexDominion ecosystem through identity-aware, contextual product recommendations.

**Core Flow:**
```
Identity → Dashboard Widgets → Contextual Links → Ecosystem Products
```

---

## 1. Identity-Based Product Mapping

**CRITICAL PRINCIPLE: Cross-promotion is NEVER random.**

Every promotion is tied to:
- **Identity** - User's persona (Diaspora, Youth, Creator, Legacy)
- **Behavior** - What they actually do (stocks viewed, news read, portfolio activity)
- **Screen Context** - Where they are in the app (Dashboard, News, Portfolio, Markets, Premium)
- **User Goals** - What they're trying to accomplish

### Diaspora (Global Investors)
**Cross-Promotion Themes:**
- Diaspora economic stories
- Caribbean business insights
- Diaspora Flow Maps deep-dives
- Regional digital products
- Diaspora creator spotlights

**Primary Products:**
- Caribbean Investment Tracker Template ($14.99)
- Global Remittance Calculator (Free)
- Diaspora Flow Maps Pro Subscription ($19.99/mo)
- International Tax Planning Guide ($29.99)
- Multi-Currency Portfolio Tracker ($9.99)

**Contextual Triggers:**
- Portfolio has international stocks → "Track regional exposure"
- News from Caribbean/African markets → "See diaspora-focused analytics"
- Monday morning → "Weekly diaspora market briefing"

**Ecosystem Connections:**
- IslandNation diaspora products
- Diaspora business templates
- Diaspora creator tools

### Youth (Beginners)
**Primary Products:**
- First Portfolio Challenge (Free)
- Investment Basics Mini-Course ($19.99)
- Paper Trading Simulator (Free trial → $4.99/mo)
- Student Budget Planner ($7.99)
- Learn-to-Invest Workbook Bundle ($24.99)

**Contextual Triggers:**
- Portfolio < $1000 → "Start with paper trading"
- Created first alert → "Level up your skills"
- Friday afternoon → "Weekend learning challenge"

### Creator (Entrepreneurs)
**Primary Products:**
- Business Financial Planner ($34.99)
- Creator Revenue Tracker ($12.99)
- Equity Calculator for Founders ($19.99)
- AI Content Strategy Tool ($29.99/mo)
- Creator Economy Analytics Dashboard ($49.99)

**Contextual Triggers:**
- Portfolio has creator economy stocks (SHOP, ETSY, META) → "Track your industry"
- News about creator platforms → "See creator-focused insights"
- Earnings season → "Creator earnings tracker"

### Legacy-Builder (Dividend Focus)
**Primary Products:**
- Retirement Income Planner ($39.99)
- Dividend Aristocrats Tracker ($14.99)
- Estate Planning Checklist (Free)
- Generational Wealth Workbook ($24.99)
- Legacy Portfolio Template ($9.99)

**Contextual Triggers:**
- Portfolio has 3+ dividend stocks → "Optimize dividend strategy"
- Ex-dividend dates approaching → "Track dividend calendar"
- Quarterly earnings → "Dividend sustainability analysis"

---

## 2. Dashboard Widget Placements

### Primary Widget Location: Right Sidebar
**Position:** Below portfolio summary, above news feed
**Max Widgets Shown:** 2 (stacked)
**Rotation:** Every 24 hours or on page refresh

### Widget Types

#### Type A: Product Card (Default)
```
┌─────────────────────────────────────┐
│ 🌍 For Diaspora Investors          │
│                                     │
│ Caribbean Investment Tracker        │
│ Track regional exposure across 20+  │
│ Caribbean markets with real-time    │
│ currency conversion.                │
│                                     │
│ [$14.99] [Learn More →]            │
│ [Dismiss]                           │
└─────────────────────────────────────┘
```

#### Type B: Free Tool Card
```
┌─────────────────────────────────────┐
│ 📊 Free Tool                        │
│                                     │
│ Portfolio Diversification Checker   │
│ See how balanced your holdings are  │
│ across sectors and regions.         │
│                                     │
│ [Try Now — Free →]                  │
│ [Dismiss]                           │
└─────────────────────────────────────┘
```

#### Type C: Service Promotion
```
┌─────────────────────────────────────┐
│ 🔥 From CodexDominion               │
│                                     │
│ Treasury AI — Financial Command     │
│ Automate workflows, track revenue,  │
│ and make sovereign decisions.       │
│                                     │
│ [Explore →]                         │
│ [Not Interested]                    │
└─────────────────────────────────────┘
```

### Secondary Widget Location: In-Page Contextual Links
**Position:** Within specific page sections
**Frequency:** 1 per page load

**Examples:**
- **Portfolio Page:** After holdings table → "Export to CSV with Pro → OR → Download Legacy Portfolio Template"
- **Markets Page:** After heatmap → "Save this view with Creator Analytics Dashboard"
- **News Feed:** After 5 articles → "Get multi-source verification with Premium → OR → Download News Verification Guide (Free)"
- **Alerts Center:** Empty state → "Try Workflow Automation to auto-execute trades"

---

## 3. Contextual Trigger Logic

### Trigger Categories

#### Portfolio-Based Triggers
| Condition | Promotion |
|-----------|-----------|
| Portfolio value < $1000 | Youth: Paper Trading Simulator |
| 3+ dividend stocks | Legacy: Retirement Income Planner |
| 5+ tech stocks | Creator: Creator Economy Analytics |
| International holdings > 20% | Diaspora: Caribbean Investment Tracker |
| Portfolio concentration > 40% one sector | All: Diversification Checker (Free) |

#### Activity-Based Triggers
| Action | Promotion |
|--------|-----------|
| Created 5+ alerts | Workflow Automation Service |
| Viewed 10+ news articles this week | Multi-source verification guide |
| Checked portfolio 3+ times today | Paper trading to practice first |
| Used AI summary 5 times (hit limit) | Premium tier upgrade |
| Exported portfolio (Pro feature locked) | Legacy Portfolio Template (one-time) |

#### Time-Based Triggers
| Time | Promotion |
|------|-----------|
| Monday 7am-10am | Dawn Dispatch briefing service |
| Friday 3pm-6pm | Youth: Weekend learning challenge |
| Earnings season (quarterly) | Earnings tracker templates |
| End of month | Treasury AI for expense tracking |
| Tax season (Jan-Apr) | International Tax Planning Guide |

#### Event-Based Triggers
| Event | Promotion |
|-------|-----------|
| News about Caribbean markets | Diaspora: Regional analytics |
| Creator platform earnings | Creator: Industry tracker |
| Dividend aristocrat cuts dividend | Legacy: Dividend sustainability tool |
| Market volatility > 2% | Risk assessment calculator (Free) |

---

## 4. Premium Tier Integration

### Free Tier (5 alerts, 5 AI/day)
- **Widget Frequency:** 2 widgets on dashboard, 1 in-page link per session
- **Product Focus:** Free tools (50%), Paid templates (30%), Services (20%)
- **Upgrade Prompts:** Subtle mentions when hitting limits ("Need more alerts? Try Workflow Automation OR upgrade")

### Premium Tier ($14.99/mo)
- **Widget Frequency:** 1 widget on dashboard, 1 in-page link per session
- **Product Focus:** Advanced templates (50%), Services (30%), Free tools (20%)
- **Upgrade Prompts:** Focus on Pro features ("Multi-portfolio? Try Pro OR Creator Revenue Tracker")

### Pro Tier ($29.99/mo)
- **Widget Frequency:** 1 widget on dashboard, minimal in-page (0-1 per day)
- **Product Focus:** Premium services (60%), Enterprise tools (30%), Free resources (10%)
- **Upgrade Prompts:** None for internal DominionMarkets, only ecosystem services

---

## 5. Ecosystem Product Catalog

### Category: Templates & Downloads
| Product | Price | Identity Fit | Type |
|---------|-------|--------------|------|
| Caribbean Investment Tracker | $14.99 | Diaspora | Excel/Google Sheets |
| Legacy Portfolio Template | $9.99 | Legacy-Builder | PDF + Spreadsheet |
| Creator Revenue Tracker | $12.99 | Creator | Notion/Excel |
| First Portfolio Workbook | $7.99 | Youth | PDF |
| International Tax Guide | $29.99 | Diaspora | PDF |
| Retirement Income Planner | $39.99 | Legacy-Builder | Excel + PDF |
| Business Financial Planner | $34.99 | Creator | Excel/Google Sheets |
| Student Budget Planner | $7.99 | Youth | Mobile App |

### Category: Free Tools
| Product | Price | Identity Fit | Type |
|---------|-------|--------------|------|
| Diversification Checker | Free | All | Web Tool |
| Global Remittance Calculator | Free | Diaspora | Web Tool |
| Paper Trading Simulator | Free trial | Youth | Web App |
| Estate Planning Checklist | Free | Legacy-Builder | PDF Download |
| Risk Assessment Calculator | Free | All | Web Tool |

### Category: Services & Subscriptions
| Product | Price | Identity Fit | Type |
|---------|-------|--------------|------|
| Treasury AI | $49.99/mo | Creator, Legacy | SaaS |
| Dawn Dispatch | $29.99/mo | Diaspora | Email + Dashboard |
| Workflow Automation | $39.99/mo | All | SaaS |
| Diaspora Flow Maps Pro | $19.99/mo | Diaspora | Dashboard Module |
| Creator Economy Analytics | $49.99/mo | Creator | Dashboard |
| Paper Trading Pro | $4.99/mo | Youth | Mobile + Web |

### Category: Educational Content
| Product | Price | Identity Fit | Type |
|---------|-------|--------------|------|
| Investment Basics Course | $19.99 | Youth | Video Series |
| Learn-to-Invest Workbook Bundle | $24.99 | Youth | PDF Bundle |
| Generational Wealth Workbook | $24.99 | Legacy-Builder | PDF + Videos |
| AI Content Strategy Guide | $29.99 | Creator | PDF + Templates |

---

## 6. Widget Component Structure

### Component Hierarchy
```
<CrossPromotionEngine>
  ├── <DashboardWidgets>
  │   ├── <ProductCard>
  │   ├── <FreeToolCard>
  │   └── <ServicePromotionCard>
  ├── <ContextualLinks>
  │   ├── <InlinePromotion>
  │   └── <UpgradePrompt>
  └── <PromotionErrorStates>
      ├── <LoadError>
      ├── <NoPromotionsAvailable>
      └── <DismissedState>
```

### Props & State Management

#### ProductCard Props
```typescript
interface ProductCardProps {
  product: {
    id: string;
    name: string;
    description: string;
    price: number | null; // null for free
    category: 'template' | 'tool' | 'service' | 'education';
    identityFit: 'diaspora' | 'youth' | 'creator' | 'legacy' | 'all';
    icon: string;
    ctaText: string;
    ctaLink: string;
  };
  onDismiss: (productId: string) => void;
  onImpressionTracked: (productId: string) => void;
  onClickTracked: (productId: string, action: 'learn_more' | 'try_now' | 'dismiss') => void;
}
```

#### Promotion Selection Logic (Backend)
```python
def select_promotions(
    user_id: str,
    user_identity: str,
    user_tier: str,
    location: str,  # 'dashboard' | 'portfolio' | 'markets' | 'news' | 'alerts'
    context: dict  # portfolio_value, stock_count, alert_count, etc.
) -> List[Promotion]:
    """
    Returns 1-2 promotions based on:
    1. Identity fit (Diaspora/Youth/Creator/Legacy)
    2. Contextual triggers (portfolio, activity, time, events)
    3. Tier-appropriate frequency
    4. Dismissed history (hide for 7 days)
    5. Impression cap (max 10 per product per user per month)
    """
```

---

## 7. User Control & Privacy

### Dismissal Options
- **Dismiss this promotion:** Hide for 7 days
- **Not interested in this category:** Hide all templates/services/tools for 30 days
- **Show fewer recommendations:** Reduce widget count by 50%
- **Turn off ecosystem promotions:** Disable entirely in Settings

### Settings Integration
**App Preferences → Ecosystem Recommendations**
```
[ ] Show ecosystem product recommendations
    ├── [x] Dashboard widgets (2 max)
    ├── [x] In-page contextual links (1 per page)
    ├── [ ] Occasional modal promotions (1 per week)
    └── Frequency: [More] [Balanced ✓] [Less]

Dismissed Products: [View & Restore] (12 hidden)
```

### Tracking & Analytics (Privacy-Safe)
**User-level tracking:**
- Impression count per product (for frequency cap)
- Click-through rate (CTR) per identity type
- Dismissal reasons (for improving recommendations)

**No tracking:**
- Cross-site tracking
- Third-party data sharing
- PII in analytics events

---

## 8. Error States

### Load Error
**Scenario:** API fails to fetch promotions
**Display:** Show fallback generic promotion
```
┌─────────────────────────────────────┐
│ Unable to load recommendations      │
│ [Retry] [Dismiss]                   │
└─────────────────────────────────────┘
```

### No Promotions Available
**Scenario:** User dismissed all, or no contextual fit
**Display:** Empty state or hide widget entirely
```
(No widget shown)
```

### Network Timeout
**Scenario:** Slow API response
**Display:** Show loading skeleton → timeout after 3s → hide
```
┌─────────────────────────────────────┐
│ ▁▂▃▄▅ Loading...                    │
└─────────────────────────────────────┘
```

---

## 9. API Endpoints

### GET /api/promotions
**Query Params:**
- `location`: dashboard | portfolio | markets | news | alerts
- `context`: JSON object with portfolio stats, activity metrics

**Response:**
```json
{
  "promotions": [
    {
      "id": "promo_001",
      "product_id": "caribbean_tracker",
      "name": "Caribbean Investment Tracker",
      "description": "Track regional exposure across 20+ Caribbean markets",
      "price": 14.99,
      "currency": "USD",
      "category": "template",
      "identity_fit": "diaspora",
      "icon": "globe",
      "cta_text": "Learn More",
      "cta_link": "https://codexdominion.app/products/caribbean-tracker",
      "widget_type": "product_card"
    }
  ],
  "max_impressions_reached": false
}
```

### POST /api/promotions/impression
**Body:**
```json
{
  "promotion_id": "promo_001",
  "location": "dashboard"
}
```

### POST /api/promotions/click
**Body:**
```json
{
  "promotion_id": "promo_001",
  "action": "learn_more",
  "location": "dashboard"
}
```

### POST /api/promotions/dismiss
**Body:**
```json
{
  "promotion_id": "promo_001",
  "reason": "not_interested" | "already_have" | "too_expensive" | "other",
  "hide_duration_days": 7
}
```

### GET /api/promotions/dismissed
**Response:**
```json
{
  "dismissed": [
    {
      "promotion_id": "promo_001",
      "dismissed_at": "2025-12-20T10:30:00Z",
      "hide_until": "2025-12-27T10:30:00Z",
      "reason": "not_interested"
    }
  ]
}
```

### POST /api/promotions/restore
**Body:**
```json
{
  "promotion_id": "promo_001"
}
```

---

## 10. Implementation Checklist

### Phase 1: Database & Backend
- [ ] Create `promotions` table (catalog)
- [ ] Create `user_promotion_interactions` table (impressions, clicks, dismissals)
- [ ] Create `promotion_rules` table (identity mappings, contextual triggers)
- [ ] Implement promotion selection service
- [ ] Build 6 API endpoints
- [ ] Add impression/click tracking
- [ ] Add dismissal logic with 7-day hide

### Phase 2: Frontend Components
- [ ] Create `ProductCard.tsx`
- [ ] Create `FreeToolCard.tsx`
- [ ] Create `ServicePromotionCard.tsx`
- [ ] Create `InlinePromotion.tsx` (contextual links)
- [ ] Create `DashboardWidgets.tsx` (container)
- [ ] Create `PromotionErrorStates.tsx`
- [ ] Add to Settings: Ecosystem Recommendations toggle

### Phase 3: Integration
- [ ] Wire up dashboard sidebar widgets
- [ ] Add contextual links to Portfolio page
- [ ] Add contextual links to Markets page
- [ ] Add contextual links to News Feed
- [ ] Add contextual links to Alerts Center
- [ ] Connect dismissal to Settings (view dismissed list)
- [ ] Add impression tracking on mount
- [ ] Add click tracking on CTA clicks

### Phase 4: Testing & Refinement
- [ ] Test identity-based filtering (Diaspora sees diaspora products)
- [ ] Test contextual triggers (portfolio triggers correct products)
- [ ] Test tier frequency limits (Free sees more, Pro sees less)
- [ ] Test dismissal & restore flow
- [ ] Test API error states (fallback promotions)
- [ ] Test privacy compliance (no PII in analytics)
- [ ] A/B test widget designs for CTR

---

## 11. Success Metrics

### Engagement Metrics
- **Impression Rate:** % users who see promotions (target: 80% Free, 60% Premium, 40% Pro)
- **Click-Through Rate (CTR):** % who click CTA (target: 5-10%)
- **Conversion Rate:** % who purchase (target: 2-5%)
- **Dismissal Rate:** % who dismiss (acceptable: < 20%)

### Revenue Metrics
- **Cross-Promotion Revenue:** Monthly revenue from promoted products
- **Average Order Value (AOV):** Per identity type
- **Customer Lifetime Value (CLV):** From ecosystem engagement

### Quality Metrics
- **Relevance Score:** User feedback on "Was this helpful?" (target: 70%+ yes)
- **Frequency Satisfaction:** User reports promotions are "just right" vs "too many" (target: 80%+ satisfied)
- **Restore Rate:** % dismissed promotions later restored (indicates initial dismissal may have been hasty)

---

## 12. Compliance & Ethics

### No Deceptive Practices
- Clearly label promotions with "From CodexDominion" badge
- Show actual prices (no "hidden fees")
- Indicate "Free trial" vs "Free forever"
- External links open in new tab with warning

### Respect User Intent
- Never block core functionality with promotions
- Allow dismissal without penalty
- Honor "Turn off" toggle immediately
- Don't re-show dismissed products within 7 days

### Transparent Tracking
- Explain what's tracked in Settings ("We track impressions and clicks to improve recommendations. No personal data is shared with third parties.")
- Allow export of interaction history (Pro tier)
- Delete all promotion data on account deletion

---

**🔥 SECTION 16 SPECIFICATION COMPLETE**
**Ready for implementation: Database → Backend → Frontend → Integration**

