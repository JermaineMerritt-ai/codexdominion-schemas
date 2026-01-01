# 🏗️ Codex Dominion - Architecture Patterns

> **Detailed UI/UX architecture patterns extracted from copilot-instructions.md**  
> **Last Updated:** December 25, 2025

## 📋 Table of Contents
- [Portfolio Architecture](#portfolio-architecture)
- [Markets Architecture](#markets-architecture)
- [News Architecture](#news-architecture)
- [Dashboard Components](#dashboard-components)
- [Identity-Aware Personalization](#identity-aware-personalization)
- [Responsive Design Patterns](#responsive-design-patterns)
- [Data Flow Patterns](#data-flow-patterns)

---

## Portfolio Architecture

### Component Hierarchy
```
Portfolio Page
├── Portfolio Header (sticky navigation)
├── Portfolio Snapshot (value, change, tier)
├── Holdings Table (PRIMARY FOCUS)
├── Allocation Module (sector breakdown)
├── Identity Insights (identity-aware context)
└── Premium Insights (tier-gated analytics)
```

### Holdings Table Pattern
```typescript
// Holdings table with search, sort, expand
export function HoldingsTable({ holdings, identity }: Props) {
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<'ticker' | 'value' | 'change'>('value');
  const [expandedRows, setExpandedRows] = useState<Set<string>>(new Set());
  
  return (
    <Card>
      <CardHeader>
        <SearchInput value={searchQuery} onChange={setSearchQuery} />
      </CardHeader>
      <CardBody>
        <table>
          {/* Sortable columns */}
          {/* Expandable rows with details */}
          {/* Identity tags (Diaspora, Creator, Legacy) */}
        </table>
      </CardBody>
    </Card>
  );
}
```

### Desktop Layout (3-Column)
```
┌──────────────────┬──────────────────────┬────────────────────┐
│  LEFT SIDEBAR    │   CENTER COLUMN      │   RIGHT SIDEBAR    │
│  (25%)           │   (50%)              │   (25%)            │
│                  │                      │                    │
│  Portfolio       │   Holdings Table     │   Identity         │
│  Snapshot        │   (Full Focus)       │   Insights         │
│                  │                      │                    │
│  Allocation      │   Searchable         │   Premium          │
│  Overview        │   Sortable           │   Analytics        │
│                  │   Expandable         │                    │
└──────────────────┴──────────────────────┴────────────────────┘
```

---

## Markets Architecture

### Component Hierarchy
```
Markets Page
├── Market Header (status, session, refresh)
├── Market Overview (indices, breadth)
├── Sector Heatmap (11 GICS sectors)
├── Movers (gainers, losers, most active)
├── Earnings Calendar (today, upcoming)
└── Cultural Alpha (identity-specific)
```

### Real-Time Data Flow
```typescript
// WebSocket connection for live prices
export function useRealTimePrices(symbols: string[]) {
  const [prices, setPrices] = useState<Map<string, PriceData>>(new Map());
  const [isStale, setIsStale] = useState(false);
  
  useEffect(() => {
    const ws = new WebSocket('wss://api.dominionmarkets.app/prices/stream');
    
    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      setPrices(prev => new Map(prev).set(update.symbol, update));
      setIsStale(false);
    };
    
    // Stale check every 30 seconds
    const staleCheck = setInterval(() => {
      if (Date.now() - lastUpdate > 60000) setIsStale(true);
    }, 30000);
    
    return () => {
      ws.close();
      clearInterval(staleCheck);
    };
  }, [symbols]);
  
  return { prices, isStale };
}
```

### Tier-Based Limits
```typescript
const TIER_LIMITS = {
  free: {
    movers: 10,
    earnings: 1,  // Today only
    heatmap: 'basic'
  },
  premium: {
    movers: 50,
    earnings: 7,  // Week ahead
    heatmap: 'advanced'
  },
  pro: {
    movers: 200,
    earnings: 30,  // Month ahead
    heatmap: 'advanced'
  }
};
```

---

## News Architecture

### Verification Levels
```typescript
enum VerificationLevel {
  VERIFIED = 'verified',      // Multiple trusted sources
  CONFIRMED = 'confirmed',    // Single trusted source
  UNVERIFIED = 'unverified',  // Not yet verified
  RUMOR = 'rumor',           // Unconfirmed
  DISPUTED = 'disputed'       // Conflicting reports
}

// Verification badge
<VerificationBadge level={story.verificationLevel} />
```

### Story Card Pattern
```typescript
export function StoryCard({ story, identity }: Props) {
  const identityContext = getIdentityContext(story, identity);
  
  return (
    <Card>
      <CardBody>
        {/* Verification badge */}
        <VerificationBadge level={story.verificationLevel} />
        
        {/* Headline & summary */}
        <h3>{story.headline}</h3>
        <p>{story.summary}</p>
        
        {/* Identity context */}
        {identityContext && (
          <div className="identity-context">
            {getIdentityIcon(identity)} {identityContext}
          </div>
        )}
        
        {/* Source credibility */}
        <SourceCredibilityBadge credibility={story.sourceCredibility} />
      </CardBody>
    </Card>
  );
}
```

---

## Dashboard Components

### Multi-Identity Personalization
```typescript
export function PersonalizationEngine() {
  personalize_experience(user_id: str, context: dict) {
    // 1. Get user identity
    identity = get_user_identity(user_id);
    
    // 2. Get identity-specific logic
    logic_class = identity_logic[identity];
    
    // 3. Gather inputs
    inputs = logic_class.get_inputs(user_id);
    
    // 4. Generate outputs
    outputs = logic_class.generate_outputs(inputs, context);
    
    // 5. Audit personalization
    audit_personalization(user_id, identity, inputs, outputs);
    
    return outputs;
  }
}
```

### Identity Widget Logic
```typescript
// Each identity gets unique dashboard widget
const IDENTITY_WIDGETS = {
  [UserIdentity.DIASPORA]: [
    "diaspora_economic_insights",
    "diaspora_news_feed",
    "cultural_alpha_highlights"
  ],
  [UserIdentity.YOUTH]: [
    "learning_challenges",
    "beginner_explanations",
    "achievement_badges"
  ],
  [UserIdentity.CREATOR]: [
    "creator_economy_tracker",
    "cultural_alpha_overlay",
    "ai_tools_monitor"
  ],
  [UserIdentity.LEGACY_BUILDER]: [
    "long_term_insights",
    "stability_indicators",
    "dividend_tracker"
  ]
};
```

---

## Identity-Aware Personalization

### Core Principles
1. **Identity shapes interpretation, not access**
2. **Behavior refines identity, but never profiles**
3. **Personalization is descriptive, not directive**
4. **Personalization must feel natural**
5. **Premium-aware** (depth, not access)

### Allowed vs Forbidden Signals
```python
# ✅ ALLOWED: Non-sensitive behavior signals
ALLOWED_SIGNALS = [
    "pages_viewed",
    "sectors_explored",
    "news_categories_opened",
    "alerts_created",
    "watchlist_sectors"
]

# ❌ FORBIDDEN: Sensitive profiling signals
FORBIDDEN_SIGNALS = [
    "portfolio_performance",
    "transaction_history",
    "risk_tolerance",
    "income_level",
    "predicted_behavior",
    "sentiment_analysis"
]
```

---

## Responsive Design Patterns

### Breakpoints
```typescript
const BREAKPOINTS = {
  mobile: 768,      // < 768px: Stack vertically
  tablet: 1024,     // 768-1024px: 2 columns
  desktop: 1024     // > 1024px: 3 columns
};

export function ResponsiveLayout({ children }) {
  const width = useWindowWidth();
  
  if (width < BREAKPOINTS.mobile) {
    return <MobileLayout>{children}</MobileLayout>;
  }
  
  if (width < BREAKPOINTS.tablet) {
    return <TabletLayout>{children}</TabletLayout>;
  }
  
  return <DesktopLayout>{children}</DesktopLayout>;
}
```

### Mobile-First Components
```typescript
// Collapsible sections for mobile
export function CollapsibleSection({ title, children, defaultOpen }) {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  
  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>
        {title}
        <ChevronIcon className={isOpen ? 'rotate-180' : ''} />
      </button>
      {isOpen && <div>{children}</div>}
    </div>
  );
}
```

---

## Data Flow Patterns

### Layer Architecture
```
UI Layer → Identity Layer → Cultural Alpha Layer → 
Filter Layer → Timeline Layer → Verification Layer → Data Source
```

### Independent Component Loading
```typescript
export function useMarketLayers(userId: string) {
  const indices = useMarketLayer('indices', {});
  const sectors = useMarketLayer('sectors', {});
  const movers = useMarketLayer('movers', { userId });
  
  return {
    indices: indices.data,
    sectors: sectors.data,
    movers: movers.data,
    errors: {
      indices: indices.error,
      sectors: sectors.error,
      movers: movers.error
    }
  };
}
```

### Caching Strategy
```python
# Multi-layer caching with Redis
CACHE_TTL = {
    'indices': 15,        # 15 seconds (volatile)
    'sectors': 60,        # 1 minute
    'movers': 30,         # 30 seconds
    'earnings': 3600,     # 1 hour
    'cultural_alpha': 300 # 5 minutes
}
```

---

## Quick Reference

### Component Load Order
1. Header (always visible)
2. Primary content (main focus)
3. Secondary content (contextual)
4. Tertiary content (supplementary)

### Error Handling
- Each component fails independently
- Show error state with retry button
- Graceful degradation (never complete failure)
- Clear error messages for users

### Performance Targets
- Initial load: < 500ms (cached)
- Live updates: 15-30 seconds
- User interaction: < 100ms response
- WebSocket reconnect: < 5 seconds

---

**🔥 The Flame Burns Sovereign and Eternal!** 👑
