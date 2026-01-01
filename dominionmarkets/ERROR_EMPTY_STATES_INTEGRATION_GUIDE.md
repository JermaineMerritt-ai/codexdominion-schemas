# Error & Empty States - Integration Guide

## Overview
This guide shows how to integrate error and empty state components throughout DominionMarkets.

**Files Created:**
1. `SECTION_17_ERROR_EMPTY_STATES_SPEC.md` - Complete specification
2. `components/errors/GlobalErrorStates.tsx` - Network, Server, Timeout, Auth, Data errors
3. `components/empty/GlobalEmptyStates.tsx` - No portfolio, watchlist, alerts, news
4. `components/loading/IdentityLoadingStates.tsx` - Identity-aware loading
5. `components/gates/PremiumGateStates.tsx` - Premium/Pro upgrade gates
6. `components/offline/OfflineState.tsx` - Offline handling with caching
7. `components/errors/ModuleErrorStates.tsx` - Module-specific errors

---

## Quick Reference

### When to Use Each Component

| Scenario | Component |
|----------|-----------|
| Network failure | `<NetworkError onRetry={...} />` |
| 500 server error | `<ServerError onRetry={...} />` |
| Request timeout | `<TimeoutError onRetry={...} />` |
| 401 auth error | `<AuthenticationError onLogin={...} />` |
| Generic data error | `<DataLoadError onRetry={...} />` |
| No portfolio holdings | `<NoPortfolioEmpty identity={identity} onAction={...} />` |
| No watchlist stocks | `<NoWatchlistEmpty onAction={...} />` |
| No alerts created | `<NoAlertsEmpty identity={identity} onAction={...} />` |
| Loading dashboard | `<DashboardLoading identity={identity} />` |
| Premium feature locked | `<PremiumGateCSVExport onUpgrade={...} />` |
| User is offline | `<OfflineOverlay hasCachedData={true} />` |

---

## Integration Examples

### 1. Dashboard Module

```tsx
// app/dashboard/page.tsx
import { 
  SmartErrorBoundary, 
  DashboardLoading, 
  NoPortfolioEmpty 
} from '@/components';

export default function DashboardPage({ 
  identity 
}: { 
  identity: "diaspora" | "youth" | "creator" | "legacy" 
}) {
  const { data, loading, error, refetch } = useQuery('/api/dashboard');

  // Show loading state
  if (loading) {
    return <DashboardLoading identity={identity} />;
  }

  // Show error state
  if (error) {
    return (
      <SmartErrorBoundary 
        error={error} 
        onRetry={refetch}
        onLogin={() => router.push('/login')} 
      />
    );
  }

  // Show empty state if no portfolio
  if (!data?.portfolio?.holdings?.length) {
    return (
      <NoPortfolioEmpty 
        identity={identity}
        onAction={() => router.push('/portfolio')} 
      />
    );
  }

  return <DashboardContent data={data} />;
}
```

### 2. Markets Module

```tsx
// app/markets/heatmap/page.tsx
import { HeatmapError, MarketsLoading } from '@/components';

export default function HeatmapPage() {
  const { data, loading, error, refetch } = useQuery('/api/markets/heatmap');

  if (loading) {
    return <MarketsLoading />;
  }

  if (error) {
    return <HeatmapError onRetry={refetch} />;
  }

  if (!data?.sectors?.length) {
    return <NoMoversEmpty />;
  }

  return <HeatmapChart data={data} />;
}
```

### 3. Portfolio Module with Premium Gate

```tsx
// app/portfolio/analytics/page.tsx
import { 
  PortfolioLoadError, 
  PremiumGateAnalytics,
  NoHoldingsEmpty 
} from '@/components';

export default function PortfolioAnalytics({ 
  userTier,
  identity 
}: { 
  userTier: "free" | "premium" | "pro";
  identity: "diaspora" | "youth" | "creator" | "legacy";
}) {
  const { data, loading, error, refetch } = useQuery('/api/portfolio');

  if (loading) {
    return <PortfolioLoading identity={identity} />;
  }

  if (error) {
    return <PortfolioLoadError onRetry={refetch} />;
  }

  // Show premium gate for free users
  if (userTier === 'free') {
    return (
      <PremiumGateAnalytics 
        onUpgrade={() => router.push('/pricing')}
        onClose={() => router.back()}
      />
    );
  }

  // Show empty state if no holdings
  if (!data?.holdings?.length) {
    return (
      <NoHoldingsEmpty 
        identity={identity}
        onAction={() => router.push('/portfolio')}
      />
    );
  }

  return <AnalyticsDashboard data={data} />;
}
```

### 4. Alerts Module with Identity Awareness

```tsx
// app/alerts/page.tsx
import { 
  AlertLoadError, 
  NoAlertsEmpty,
  AlertsLoading 
} from '@/components';

export default function AlertsModule({ 
  identity 
}: { 
  identity: "diaspora" | "youth" | "creator" | "legacy" 
}) {
  const { data, loading, error, refetch } = useQuery('/api/alerts');

  if (loading) {
    return <AlertsLoading />;
  }

  if (error) {
    return <AlertLoadError onRetry={refetch} />;
  }

  // Show identity-aware empty state
  if (!data?.alerts?.length) {
    return (
      <NoAlertsEmpty 
        identity={identity}
        onAction={() => openCreateModal()}
      />
    );
  }

  return <AlertsList alerts={data.alerts} />;
}
```

### 5. CSV Export with Premium Badge

```tsx
// components/portfolio/ExportButton.tsx
import { PremiumBadge, PremiumGateCSVExport } from '@/components';

export function ExportButton({ userTier }: { userTier: string }) {
  const [showGate, setShowGate] = useState(false);

  const handleExport = () => {
    if (userTier === 'free') {
      setShowGate(true);
    } else {
      exportToCSV();
    }
  };

  return (
    <>
      <button 
        onClick={handleExport}
        className="flex items-center gap-2"
      >
        Export CSV
        {userTier === 'free' && <PremiumBadge tier="premium" size="sm" />}
      </button>

      {showGate && (
        <OverlayPremiumGate
          tier="premium"
          message="Upgrade to Premium to export portfolios as CSV."
          features={[
            'Export to Excel/CSV',
            'Schedule automatic exports',
            'Historical snapshots'
          ]}
          onUpgrade={() => router.push('/pricing')}
          onClose={() => setShowGate(false)}
        />
      )}
    </>
  );
}
```

### 6. Offline State in Root Layout

```tsx
// app/layout.tsx
import { OfflineOverlay, CompactOfflineIndicator } from '@/components';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <nav>
          <Logo />
          <CompactOfflineIndicator />
        </nav>

        <OfflineOverlay
          hasCachedData={true}
          onViewCached={() => router.push('/portfolio?cached=true')}
          lastSyncTime={new Date()}
        />

        {children}
      </body>
    </html>
  );
}
```

### 7. Form Validation with Inline Errors

```tsx
// components/forms/LoginForm.tsx
import { InlineError } from '@/components';

export function LoginForm() {
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');

  const validateEmail = (email: string) => {
    if (!email) {
      setEmailError('Email is required');
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      setEmailError('Email is invalid');
    } else {
      setEmailError('');
    }
  };

  return (
    <form>
      <div>
        <input 
          type="email" 
          onChange={(e) => validateEmail(e.target.value)}
        />
        {emailError && <InlineError message={emailError} />}
      </div>

      <div>
        <input type="password" />
        {passwordError && <InlineError message={passwordError} />}
      </div>

      <button type="submit">Log In</button>
    </form>
  );
}
```

### 8. Data Fetching with Offline Support

```tsx
// lib/api.ts
import { offlineFetch } from '@/components/offline/OfflineState';

export async function fetchPortfolio() {
  const { data, fromCache, error } = await offlineFetch('/api/portfolio', {
    cacheKey: 'cached_portfolio',
    maxCacheAge: 3600000 // 1 hour
  });

  if (fromCache) {
    console.log('📦 Showing cached portfolio data');
  }

  if (error) {
    throw new Error(error);
  }

  return data;
}
```

### 9. Skeleton Loading States

```tsx
// app/portfolio/page.tsx
import { TableSkeleton, CardSkeleton } from '@/components';

export default function PortfolioPage() {
  const { data, loading } = useQuery('/api/portfolio');

  if (loading) {
    return (
      <div className="space-y-6">
        <CardSkeleton />
        <TableSkeleton rows={10} columns={5} />
      </div>
    );
  }

  return <PortfolioTable data={data} />;
}
```

### 10. Button Loading States

```tsx
// components/buttons/SaveButton.tsx
import { InlineLoading } from '@/components';

export function SaveButton({ onSave }: { onSave: () => Promise<void> }) {
  const [loading, setLoading] = useState(false);

  const handleSave = async () => {
    setLoading(true);
    try {
      await onSave();
    } finally {
      setLoading(false);
    }
  };

  return (
    <button 
      onClick={handleSave}
      disabled={loading}
      className="px-4 py-2 bg-sovereign-gold rounded"
    >
      {loading ? <InlineLoading message="Saving…" /> : 'Save Changes'}
    </button>
  );
}
```

---

## Component Hierarchy

```
Error & Empty States System
│
├── Global States (app-wide)
│   ├── GlobalErrorStates
│   │   ├── NetworkError
│   │   ├── ServerError
│   │   ├── TimeoutError
│   │   ├── AuthenticationError
│   │   └── DataLoadError
│   │
│   ├── GlobalEmptyStates
│   │   ├── NoPortfolioEmpty (identity-aware)
│   │   ├── NoWatchlistEmpty
│   │   ├── NoAlertsEmpty (identity-aware)
│   │   └── NoNewsEmpty
│   │
│   └── OfflineState
│       ├── OfflineOverlay
│       ├── CompactOfflineIndicator
│       └── ReconnectingIndicator
│
├── Module States (module-specific)
│   ├── Dashboard
│   │   ├── MarketTickerError
│   │   ├── PortfolioSnapshotError
│   │   ├── DashboardNewsError
│   │   └── IdentityWidgetError
│   │
│   ├── Markets
│   │   ├── HeatmapError
│   │   ├── MoversError
│   │   ├── VolumeSpikesError
│   │   └── EarningsCalendarError
│   │
│   ├── Portfolio
│   │   ├── PortfolioLoadError
│   │   ├── HoldingUpdateError
│   │   └── AnalyticsError
│   │
│   ├── News Verification
│   │   ├── VerificationError
│   │   ├── SourceLoadError
│   │   └── TimelineError
│   │
│   ├── Alerts
│   │   ├── AlertCreationError
│   │   ├── AlertUpdateError
│   │   └── AlertLoadError
│   │
│   └── Settings
│       ├── SettingsSaveError
│       ├── BillingError
│       ├── IdentitySwitchError
│       └── DataExportError
│
├── Loading States (identity-aware)
│   ├── DashboardLoading
│   ├── MarketsLoading
│   ├── PortfolioLoading
│   ├── NewsLoading
│   ├── AlertsLoading
│   ├── StockDetailLoading
│   └── Skeletons
│       ├── SkeletonLoader
│       ├── CardSkeleton
│       ├── TableSkeleton
│       └── ChartSkeleton
│
└── Premium Gates
    ├── Premium Tier
    │   ├── PremiumGateCSVExport
    │   ├── PremiumGateAdvancedCharts
    │   ├── PremiumGateMultiPortfolio
    │   ├── PremiumGateAIInsights
    │   ├── PremiumGateEarningsAlerts
    │   └── PremiumGateAnalytics
    │
    └── Pro Tier
        ├── ProGateAPIAccess
        ├── ProGateInstitutional
        └── ProGateWhiteLabel
```

---

## Checklist for Developers

### When Adding New Features

- [ ] Add appropriate loading state (identity-aware if module-level)
- [ ] Handle network/server/timeout errors with SmartErrorBoundary
- [ ] Show empty state if data collection is empty
- [ ] Add premium gate if feature requires upgrade
- [ ] Support offline mode with cached data (if applicable)
- [ ] Add inline errors for form validation
- [ ] Use skeleton loaders for tables/cards
- [ ] Test all error scenarios (401, 500, network, timeout)

### Testing Checklist

- [ ] Test network failure (disable network in DevTools)
- [ ] Test server error (mock 500 response)
- [ ] Test timeout (mock slow API)
- [ ] Test authentication error (expire token)
- [ ] Test empty states for each module
- [ ] Test premium gates for free users
- [ ] Test offline mode with cached data
- [ ] Test loading states for identity variations
- [ ] Test retry actions work correctly
- [ ] Test form validation errors display correctly

---

## Design Principles Recap

**6 Principles:**
1. ✅ **Never blame the user** - "Unable to load" not "You didn't configure this"
2. ✅ **Never expose internal systems** - "Data unavailable" not "PostgreSQL error"
3. ✅ **Never imply advice** - "No holdings yet" not "You should add stocks"
4. ✅ **Always offer a retry** - Every error has a clear action
5. ✅ **Always stay calm and neutral** - No exclamation marks, no drama
6. ✅ **Always maintain identity tone** - Loading states adapt to Diaspora/Youth/Creator/Legacy

---

## Summary

**Section 17 Complete:**
- ✅ 5 global error states (Network, Server, Timeout, Auth, Data)
- ✅ 20+ module-specific error states (Dashboard, Markets, Stock, Portfolio, News, Alerts, Settings)
- ✅ 15+ empty states with identity variations (Diaspora/Youth/Creator/Legacy)
- ✅ 10+ premium gates (Premium/Pro tier locks)
- ✅ Identity-aware loading states (4 identity messages per module)
- ✅ Offline state system with caching support
- ✅ Skeleton loaders (Card, Table, Chart)
- ✅ Inline error states (form validation)
- ✅ Compact variants (for small widgets)
- ✅ Smart error boundary (auto-detects error type)

**Next Steps:**
1. Integrate error states into existing modules
2. Replace inline error messages with components
3. Add identity-aware loading to all pages
4. Test offline mode with cached data
5. Add premium gates to locked features
6. Implement form validation with InlineError
7. Test all error scenarios (network, server, auth, timeout)

🔥 **Every error state builds trust. Every empty state guides users. Every loading state respects identity.**
