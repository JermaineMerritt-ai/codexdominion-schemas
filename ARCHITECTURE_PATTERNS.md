# DominionMarkets UI Architecture Patterns

> **Purpose**: Detailed UI component architecture, layout patterns, and implementation guidelines for Portfolio, Markets, and News modules.
> **Status**: Production Reference
> **Last Updated**: December 25, 2025

## Overview

This document provides detailed UI architecture patterns extracted from the main copilot instructions for reference during UI development.

## Component Architecture Principles

### 1. Modular Independence
- Each component loads independently
- Component failures isolated (don't break entire page)
- Graceful degradation on error
- Independent caching strategies

### 2. Identity-Aware Rendering
- Identity shapes presentation, not data
- Same data, different framing per identity
- Cultural Alpha integrated throughout
- Educational context for Youth identity

### 3. Tier-Based Depth
- Free users see core data
- Premium unlocks depth, not access
- Clear upgrade prompts (no dark patterns)
- Pro tier adds advanced analytics

### 4. Real-Time Updates
- WebSocket streaming for volatile data
- 15-second update cycles
- Staleness indicators
- Automatic reconnection

## Portfolio Architecture

### Component Hierarchy
```
1. Portfolio Header (Navigation, portfolio switcher)
2. Portfolio Snapshot (Total value, daily change, tier badge)
3. Holdings Table (PRIMARY - Core portfolio data)
4. Allocation Module (Sector breakdown, asset types)
5. Identity Insights (Identity-aware interpretations)
6. Premium Insights (Tier-gated analytics)
```

### Holdings Table Pattern
```typescript
// Expandable rows with identity-aware tags
function HoldingRowExpandable({ holding, identity }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const identityTags = getIdentityTags(holding, identity);
  
  return (
    <>
      {/* Main Row */}
      <tr onClick={() => setIsExpanded(!isExpanded)}>
        <td>{holding.symbol}</td>
        <td>{holding.companyName}</td>
        <td>{holding.quantity}</td>
        <td>{formatCurrency(holding.currentValue)}</td>
        <td className={holding.dailyChange >= 0 ? 'text-green-400' : 'text-red-400'}>
          {holding.dailyChange >= 0 ? '+' : ''}{formatCurrency(holding.dailyChange)}
        </td>
        <td>
          {identityTags.map(tag => (
            <Badge key={tag.label} variant={tag.variant}>
              {tag.icon} {tag.label}
            </Badge>
          ))}
        </td>
      </tr>
      
      {/* Expanded Details */}
      {isExpanded && (
        <tr>
          <td colSpan={6}>
            <HoldingDetails holding={holding} identity={identity} />
          </td>
        </tr>
      )}
    </>
  );
}
```

### Identity Context Pattern
```typescript
function getIdentityContextMessage(holding: Holding, identity: UserIdentity): string {
  switch (identity) {
    case UserIdentity.DIASPORA:
      return holding.hasDiasporaRelevance
        ? `This company has operations in diaspora markets. ${holding.diasporaContext}`
        : "This company does not have specific diaspora market presence.";
    
    case UserIdentity.YOUTH:
      return holding.isBeginnerFriendly
        ? `This is a beginner-friendly stock. ${holding.learningContext}`
        : "This stock is part of your diversification learning journey.";
    
    case UserIdentity.CREATOR:
      return holding.isCreatorEconomy
        ? `This company is part of the creator economy. ${holding.creatorContext}`
        : "This stock supports your overall portfolio diversification.";
    
    case UserIdentity.LEGACY_BUILDER:
      return holding.isDividendPayer
        ? `This stock pays consistent dividends. ${holding.dividendContext}`
        : "This stock contributes to your portfolio's growth potential.";
  }
}
```

## Markets Architecture

### Component Hierarchy
```
1. Market Header (Status, session info, last update)
2. Market Overview (Major indices, market breadth)
3. Sector Heatmap (GICS sectors with performance)
4. Movers (Top gainers, losers, most active)
5. Earnings Calendar (Today, upcoming, past)
6. Cultural Alpha (Identity-specific signals)
```

### Sector Heatmap Pattern
```typescript
function SectorTile({ sector, identity }) {
  const isPositive = sector.changePct >= 0;
  const intensity = Math.min(Math.abs(sector.changePct) / 3, 1);
  
  const backgroundColor = isPositive
    ? `rgba(34, 197, 94, ${intensity * 0.3})` // Green
    : `rgba(239, 68, 68, ${intensity * 0.3})`; // Red
  
  return (
    <a href={`/markets/sectors/${sector.symbol}`}
       style={{ backgroundColor }}
       className={`p-4 rounded-lg border-2 ${isPositive ? 'border-green-500/50' : 'border-red-500/50'}`}>
      <h3 className="font-semibold">{sector.name}</h3>
      <div className={isPositive ? 'text-green-400' : 'text-red-400'}>
        {isPositive ? '+' : ''}{sector.changePct.toFixed(2)}%
      </div>
      {sector.culturalAlpha && (
        <Badge variant="cultural-alpha">{sector.culturalAlpha.icon}</Badge>
      )}
    </a>
  );
}
```

### Movers with Tier Gating
```typescript
function Movers({ data, tier, identity }) {
  const limits = { free: 10, premium: 50, pro: 200 };
  const limit = limits[tier];
  
  const visibleMovers = data.gainers.slice(0, limit);
  const hiddenCount = data.gainers.length - visibleMovers.length;
  
  return (
    <Card>
      <CardBody>
        {visibleMovers.map(mover => (
          <MoverRow key={mover.symbol} mover={mover} identity={identity} />
        ))}
        
        {hiddenCount > 0 && tier === 'free' && (
          <UpgradePrompt>
            View {hiddenCount} more movers with Premium ($9.99/month)
          </UpgradePrompt>
        )}
      </CardBody>
    </Card>
  );
}
```

## News Architecture

### Verification Levels
```typescript
enum VerificationLevel {
  VERIFIED = 'verified',     // Multiple trusted sources
  CONFIRMED = 'confirmed',   // Single trusted source
  UNVERIFIED = 'unverified', // Not yet verified
  RUMOR = 'rumor',           // Unconfirmed report
  DISPUTED = 'disputed'      // Conflicting reports
}

function VerificationBadge({ level }: { level: VerificationLevel }) {
  const config = {
    verified: { icon: '✅', color: 'text-green-400', bg: 'bg-green-500/10' },
    confirmed: { icon: '✓', color: 'text-blue-400', bg: 'bg-blue-500/10' },
    unverified: { icon: '⏳', color: 'text-yellow-400', bg: 'bg-yellow-500/10' },
    rumor: { icon: '❓', color: 'text-orange-400', bg: 'bg-orange-500/10' },
    disputed: { icon: '⚠️', color: 'text-red-400', bg: 'bg-red-500/10' }
  }[level];
  
  return (
    <span className={`${config.color} ${config.bg}`}>
      {config.icon} {level.toUpperCase()}
    </span>
  );
}
```

### Identity Context for News
```typescript
function getIdentityContext(story: NewsStory, identity: UserIdentity): string | null {
  switch (identity) {
    case UserIdentity.DIASPORA:
      if (story.symbols.some(s => hasDiasporaRelevance(s))) {
        return `This impacts ${getDiasporaRegion(story.symbols[0])} diaspora markets.`;
      }
      break;
    
    case UserIdentity.YOUTH:
      return `Learning point: ${getEducationalContext(story.categories[0])}`;
    
    case UserIdentity.CREATOR:
      if (story.categories.includes('creator-economy')) {
        return `Creator impact: ${getCreatorContext(story)}`;
      }
      break;
    
    case UserIdentity.LEGACY_BUILDER:
      return `Long-term perspective: ${getLongTermContext(story)}`;
  }
  return null;
}
```

## Responsive Layout Patterns

### Desktop 3-Column
```typescript
// Portfolio, Markets, News all use similar 3-column layout
function DesktopLayout({ data, identity, tier }) {
  return (
    <div className="grid grid-cols-12 gap-6">
      {/* Left Sidebar (25%) */}
      <aside className="col-span-3">
        <ContextWidget />
        <FiltersWidget />
      </aside>
      
      {/* Center Content (50%) */}
      <main className="col-span-6">
        <PrimaryContent data={data} identity={identity} tier={tier} />
      </main>
      
      {/* Right Sidebar (25%) */}
      <aside className="col-span-3">
        <CulturalAlphaWidget identity={identity} />
        <InsightsWidget />
      </aside>
    </div>
  );
}
```

### Mobile Vertical Stack
```typescript
function MobileLayout({ data, identity, tier }) {
  const [expandedSections, setExpandedSections] = useState(new Set(['primary']));
  
  return (
    <div className="space-y-4">
      {/* Compact header always visible */}
      <CompactHeader />
      
      {/* Collapsible sections */}
      <CollapsibleSection title="Main Content" defaultOpen={true}>
        <PrimaryContent data={data} />
      </CollapsibleSection>
      
      <CollapsibleSection title="Details" defaultOpen={false}>
        <SecondaryContent />
      </CollapsibleSection>
      
      <CollapsibleSection title="Insights" defaultOpen={false}>
        <CulturalAlphaWidget identity={identity} />
      </CollapsibleSection>
    </div>
  );
}
```

## Real-Time Data Flow

### WebSocket Integration
```typescript
function useRealTimeData(channels: string[]) {
  const [data, setData] = useState<any>(null);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  
  useEffect(() => {
    const ws = new WebSocket('wss://api.dominionmarkets.app/stream');
    
    ws.onopen = () => {
      ws.send(JSON.stringify({ action: 'subscribe', channels }));
    };
    
    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      setData(prev => ({ ...prev, [update.type]: update.data }));
      setLastUpdate(new Date());
    };
    
    return () => ws.close();
  }, [channels]);
  
  return { data, lastUpdate };
}
```

### Caching Strategy
```python
# Multi-layer caching
CACHE_TTL = {
    'indices': 15,        # 15 seconds (highly volatile)
    'sectors': 60,        # 1 minute
    'movers': 30,         # 30 seconds
    'earnings': 3600,     # 1 hour
    'cultural_alpha': 300 # 5 minutes
}

async def load_with_cache(layer: str, **params):
    # Try cache first
    cached = await get_cached_layer(layer, params)
    if cached:
        return cached
    
    # Fetch fresh
    data = await fetch_layer_data(layer, **params)
    
    # Cache with layer-specific TTL
    await cache_layer(layer, data, CACHE_TTL[layer], params)
    
    return data
```

## Error State Patterns

### Component-Level Error Handling
```typescript
function ComponentWithError({ data, onRetry }) {
  if (data.status === 'error') {
    return (
      <Card className="border-red-500/30">
        <CardBody className="text-center py-12">
          <AlertCircle className="w-12 h-12 text-red-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">Data Unavailable</h3>
          <p className="text-gray-400 mb-4">
            We couldn't load this component. Your other data is safe.
          </p>
          <button onClick={onRetry} className="px-4 py-2 bg-sovereign-gold">
            Retry
          </button>
        </CardBody>
      </Card>
    );
  }
  
  if (data.status === 'loading') {
    return <SkeletonLoader />;
  }
  
  return <ComponentContent data={data} />;
}
```

## Premium Feature Gates

### Upgrade Prompt Pattern
```typescript
function PremiumFeature({ tier, feature, children }) {
  if (tier === 'free') {
    return (
      <div className="relative">
        {/* Blurred preview */}
        <div className="filter blur-sm pointer-events-none">
          {children}
        </div>
        
        {/* Upgrade overlay */}
        <div className="absolute inset-0 flex items-center justify-center bg-black/70">
          <UpgradeCard
            feature={feature}
            tier="premium"
            price="$9.99/month"
          />
        </div>
      </div>
    );
  }
  
  return children;
}
```

---

**Architecture Status**: Production Reference
**UI Framework**: Next.js 14 + Tailwind CSS + shadcn/ui
**Last Updated**: December 25, 2025
