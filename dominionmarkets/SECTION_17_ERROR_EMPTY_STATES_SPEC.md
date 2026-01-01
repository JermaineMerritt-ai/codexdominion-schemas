# SECTION 17 — ERROR & EMPTY STATES SPECIFICATION

## Overview
Error and empty states are critical trust-building moments. They must feel calm, neutral, and helpful—never dramatic, technical, or blaming.

**Core Principles:**
1. ✅ **Never blame the user** - "Unable to load" not "You didn't configure this"
2. ✅ **Never expose internal systems** - "Data unavailable" not "PostgreSQL connection failed"
3. ✅ **Never imply advice** - "No holdings yet" not "You should add stocks"
4. ✅ **Always offer a retry** - Every error has a clear action
5. ✅ **Always stay calm and neutral** - No exclamation marks, no drama
6. ✅ **Always maintain identity tone** - Loading states adapt to Diaspora/Youth/Creator/Legacy

---

## Design Philosophy

### What Makes Good Error States
- **Calm**: No red, no bold warnings, subtle messaging
- **Neutral**: No blame, no assumptions about cause
- **Trustworthy**: Honest about what happened
- **Non-technical**: "Unable to load data" not "API 500 error"
- **Identity-aware**: Diaspora sees "regional insights", Youth sees "learning dashboard"
- **Consistent**: Same patterns across all modules

### What to Avoid
- ❌ Blame language: "You forgot to...", "Your connection failed"
- ❌ Technical jargon: "Error 500", "null pointer exception"
- ❌ Advice implications: "You should upgrade", "Try adding stocks"
- ❌ Dramatic tone: "Critical failure!", "System down!"
- ❌ Internal details: "Database timeout", "Redis cache miss"

---

## 17.1 Global Error States

### Network Error
**Message:** "Unable to connect — check your connection."
**Icon:** WifiOff (Lucide)
**Action:** Retry button
**When:** Fetch requests fail with network error

```tsx
<NetworkError onRetry={() => refetch()} />
```

### Server Error
**Message:** "Something went wrong — try again later."
**Icon:** ServerCrash (Lucide)
**Action:** Retry button
**When:** 500, 502, 503 status codes

```tsx
<ServerError onRetry={() => refetch()} />
```

### Timeout Error
**Message:** "This is taking longer than expected — retry."
**Icon:** Clock (Lucide)
**Action:** Retry button
**When:** Request exceeds timeout threshold (30s)

```tsx
<TimeoutError onRetry={() => refetch()} />
```

### Data Load Failure
**Message:** "Unable to load data — retry."
**Icon:** AlertCircle (Lucide)
**Action:** Retry button
**When:** Generic data fetch failures

```tsx
<DataLoadError onRetry={() => refetch()} />
```

### Authentication Error
**Message:** "Your session expired — please log in again."
**Icon:** ShieldAlert (Lucide)
**Action:** Log in button
**When:** 401 status code, expired JWT

```tsx
<AuthenticationError onLogin={() => router.push('/login')} />
```

---

## 17.2 Dashboard Error States

### Market Ticker Failure
**Message:** "Market data unavailable — retry."
**Icon:** TrendingUp (Lucide)
**Action:** Retry button
**Module:** Dashboard (Market Ticker Widget)

### Portfolio Snapshot Failure
**Message:** "Unable to load your portfolio."
**Icon:** Briefcase (Lucide)
**Action:** Retry button
**Module:** Dashboard (Portfolio Widget)

### News Failure
**Message:** "News temporarily unavailable."
**Icon:** Newspaper (Lucide)
**Action:** Retry button
**Module:** Dashboard (News Widget)

### Identity Widget Failure
**Message:** "Unable to load identity insights."
**Icon:** User (Lucide)
**Action:** Retry button
**Module:** Dashboard (Identity Widget)

---

## 17.3 Dashboard Empty States

### No Portfolio
**Message:** "No holdings yet — add your first stock to unlock insights."
**Icon:** PlusCircle (Lucide)
**Action:** Add Stock button → `/portfolio`
**Module:** Dashboard (Portfolio Widget)

```tsx
<NoPortfolioEmpty 
  onAddStock={() => router.push('/portfolio')} 
  identity="diaspora" 
/>
```

### No Watchlist
**Message:** "Your watchlist is empty — search for a company to add."
**Icon:** Eye (Lucide)
**Action:** Search button → `/markets`
**Module:** Dashboard (Watchlist Widget)

### No Alerts
**Message:** "You have no alerts yet — create your first alert."
**Icon:** Bell (Lucide)
**Action:** Create Alert button → `/alerts`
**Module:** Dashboard (Alerts Widget)

### No News
**Message:** "No news available — check back later."
**Icon:** Newspaper (Lucide)
**Action:** None (passive state)
**Module:** Dashboard (News Widget)

---

## 17.4 Markets Module Error States

### Heatmap Failure
**Message:** "Unable to load heatmap."
**Icon:** Grid (Lucide)
**Action:** Retry button
**Module:** Markets (Heatmap Tab)

### Gainers/Losers Failure
**Message:** "Unable to load market movers."
**Icon:** TrendingUp (Lucide)
**Action:** Retry button
**Module:** Markets (Movers Tab)

### Volume Spikes Failure
**Message:** "Unable to load volume data."
**Icon:** BarChart3 (Lucide)
**Action:** Retry button
**Module:** Markets (Volume Tab)

### Earnings Calendar Failure
**Message:** "Earnings data temporarily unavailable."
**Icon:** Calendar (Lucide)
**Action:** Retry button
**Module:** Markets (Earnings Tab)

---

## 17.5 Markets Empty States

### No Movers
**Message:** "No significant movement at the moment."
**Icon:** Minus (Lucide)
**Action:** None (passive state)
**Module:** Markets (Movers Tab)

### No Earnings Today
**Message:** "No companies reporting earnings today."
**Icon:** Calendar (Lucide)
**Action:** None (passive state)
**Module:** Markets (Earnings Tab)

---

## 17.6 Stock Detail Error States

### Overview Failure
**Message:** "Unable to load company data."
**Icon:** Building2 (Lucide)
**Action:** Retry button
**Module:** Stock Detail (Overview Tab)

### Chart Failure
**Message:** "Chart data unavailable."
**Icon:** LineChart (Lucide)
**Action:** Retry button
**Module:** Stock Detail (Chart)

### News Failure
**Message:** "No verified news available."
**Icon:** Newspaper (Lucide)
**Action:** Retry button
**Module:** Stock Detail (News Tab)

### Insights Failure
**Message:** "Unable to load insights."
**Icon:** Lightbulb (Lucide)
**Action:** Retry button
**Module:** Stock Detail (Insights Tab)

---

## 17.7 Stock Detail Empty States

### No News
**Message:** "No recent news for this company."
**Icon:** Newspaper (Lucide)
**Action:** None (passive state)
**Module:** Stock Detail (News Tab)

### No Insights (Free Tier)
**Message:** "Upgrade to Premium to unlock insights."
**Icon:** Lock (Lucide)
**Action:** Upgrade button → `/pricing`
**Module:** Stock Detail (Insights Tab)

---

## 17.8 Portfolio Module Error States

### Portfolio Load Failure
**Message:** "Unable to load your portfolio."
**Icon:** Briefcase (Lucide)
**Action:** Retry button
**Module:** Portfolio (Main View)

### Holding Update Failure
**Message:** "Unable to update holding."
**Icon:** AlertCircle (Lucide)
**Action:** Retry button
**Module:** Portfolio (Edit Holding Modal)

### Analytics Failure
**Message:** "Analytics temporarily unavailable."
**Icon:** PieChart (Lucide)
**Action:** Retry button
**Module:** Portfolio (Analytics Tab)

---

## 17.9 Portfolio Empty States

### No Holdings
**Message:** "No holdings yet — add your first stock."
**Icon:** PlusCircle (Lucide)
**Action:** Add Stock button
**Module:** Portfolio (Main View)

**Identity Variations:**
- **Diaspora:** "No holdings yet — add your first Caribbean or international stock."
- **Youth:** "No holdings yet — add your first stock and start learning."
- **Creator:** "No holdings yet — add your first creator-economy stock."
- **Legacy:** "No holdings yet — add your first dividend stock."

### No Allocation Data
**Message:** "Add holdings to see your allocation."
**Icon:** PieChart (Lucide)
**Action:** Add Stock button
**Module:** Portfolio (Allocation View)

### No Analytics (Free Tier)
**Message:** "Upgrade to Premium to unlock analytics."
**Icon:** Lock (Lucide)
**Action:** Upgrade button → `/pricing`
**Module:** Portfolio (Analytics Tab)

---

## 17.10 News Verification Center Error States

### Verification Failure
**Message:** "Unable to verify this story."
**Icon:** ShieldAlert (Lucide)
**Action:** Retry button
**Module:** News Verification (Detail View)

### Source Load Failure
**Message:** "Unable to load sources."
**Icon:** Link (Lucide)
**Action:** Retry button
**Module:** News Verification (Sources Tab)

### Timeline Failure
**Message:** "Timeline unavailable."
**Icon:** Clock (Lucide)
**Action:** Retry button
**Module:** News Verification (Timeline Tab)

---

## 17.11 News Empty States

### No Sources
**Message:** "No sources available for this story."
**Icon:** Link (Lucide)
**Action:** None (passive state)
**Module:** News Verification (Sources Tab)

### No Related Companies
**Message:** "No related companies found."
**Icon:** Building2 (Lucide)
**Action:** None (passive state)
**Module:** News Verification (Related Companies)

---

## 17.12 Alerts Center Error States

### Alert Creation Failure
**Message:** "Unable to create alert."
**Icon:** Bell (Lucide)
**Action:** Retry button
**Module:** Alerts (Create Modal)

### Alert Update Failure
**Message:** "Unable to update alert."
**Icon:** AlertCircle (Lucide)
**Action:** Retry button
**Module:** Alerts (Edit Modal)

### Alert Load Failure
**Message:** "Unable to load alerts."
**Icon:** Bell (Lucide)
**Action:** Retry button
**Module:** Alerts (Main View)

---

## 17.13 Alerts Empty States

### No Alerts
**Message:** "You have no alerts yet — create your first alert."
**Icon:** Bell (Lucide)
**Action:** Create Alert button
**Module:** Alerts (Main View)

**Identity Variations:**
- **Diaspora:** "No alerts yet — track Caribbean market movements."
- **Youth:** "No alerts yet — get notified when your stocks move."
- **Creator:** "No alerts yet — track creator-economy earnings."
- **Legacy:** "No alerts yet — monitor dividend announcements."

### Premium-Only Alerts
**Message:** "Upgrade to Premium to unlock earnings alerts."
**Icon:** Lock (Lucide)
**Action:** Upgrade button → `/pricing`
**Module:** Alerts (Earnings Alert Type)

---

## 17.14 Settings Module Error States

### Save Failure
**Message:** "Unable to save changes."
**Icon:** Save (Lucide)
**Action:** Retry button
**Module:** Settings (Any Tab)

### Billing Failure
**Message:** "Payment method could not be updated."
**Icon:** CreditCard (Lucide)
**Action:** Retry button
**Module:** Settings (Billing Tab)

### Identity Switch Failure
**Message:** "Unable to update identity."
**Icon:** User (Lucide)
**Action:** Retry button
**Module:** Settings (Profile Tab)

### Data Export Failure
**Message:** "Export unavailable — try again later."
**Icon:** Download (Lucide)
**Action:** Retry button
**Module:** Settings (Privacy Tab)

---

## 17.15 Settings Empty States

### No Billing History
**Message:** "No billing history available."
**Icon:** Receipt (Lucide)
**Action:** None (passive state)
**Module:** Settings (Billing Tab)

### No Connected Devices
**Message:** "No devices connected."
**Icon:** Smartphone (Lucide)
**Action:** None (passive state)
**Module:** Settings (Security Tab)

---

## 17.16 Premium Gate States

### Design Principles
- **Respectful:** No pushy sales language
- **Calm:** Neutral tone, no urgency tactics
- **Value-focused:** Explain what they get
- **Non-pushy:** "Upgrade" not "Subscribe now!"

### Premium Gate
**Message:** "Upgrade to Premium to unlock this feature."
**Icon:** Lock (Lucide)
**Actions:**
- Primary: Upgrade → `/pricing`
- Secondary: Close

**Feature Variations:**
- CSV Export: "Upgrade to Premium to export portfolios as CSV."
- Advanced Charts: "Upgrade to Premium for technical indicators."
- Multi-Portfolio: "Upgrade to Premium for unlimited portfolios."
- AI Insights: "Upgrade to Premium to unlock AI-powered insights."

### Pro Gate
**Message:** "Upgrade to Pro for advanced tools."
**Icon:** Crown (Lucide)
**Actions:**
- Primary: Upgrade → `/pricing`
- Secondary: Close

**Feature Variations:**
- API Access: "Upgrade to Pro for API access."
- Institutional Tools: "Upgrade to Pro for institutional analytics."
- White-label: "Upgrade to Pro for white-label branding."

---

## 17.17 Loading States

### Design Principles
- **Minimal:** Simple spinner or skeleton
- **Clean:** No distracting animations
- **Identity-aware:** Loading messages reflect identity

### Global Loading
**Message:** "Loading…"
**Icon:** Loader2 (Lucide, spinning)

### Identity Loading Variations

**Diaspora:**
- "Loading regional insights…"
- "Loading Caribbean markets…"
- "Loading diaspora indicators…"

**Youth:**
- "Loading your learning dashboard…"
- "Loading beginner resources…"
- "Loading portfolio basics…"

**Creator:**
- "Loading creator-economy data…"
- "Loading platform metrics…"
- "Loading creator insights…"

**Legacy:**
- "Loading long-term indicators…"
- "Loading dividend data…"
- "Loading retirement metrics…"

### Module-Specific Loading

**Dashboard:** "Loading dashboard…"
**Markets:** "Loading market data…"
**Portfolio:** "Loading your portfolio…"
**News:** "Loading verified news…"
**Alerts:** "Loading alerts…"

---

## 17.18 Offline States

### Offline Message
**Message:** "You're offline — reconnect to continue."
**Icon:** WifiOff (Lucide)
**Actions:**
- Primary: Retry
- Secondary: View cached data (if available)

**Design:**
- Full-screen overlay with translucent background
- Persistent until connection restored
- Auto-dismiss when online

**Cached Data Availability:**
- Portfolio: Available (last sync timestamp shown)
- Markets: Not available (real-time required)
- News: Partially available (last 10 articles)

---

## 17.19 Component Architecture

### File Structure
```
components/
├── errors/
│   ├── GlobalErrorStates.tsx        # Network, Server, Timeout, Auth, Data
│   ├── DashboardErrors.tsx          # Market ticker, portfolio, news, identity
│   ├── MarketsErrors.tsx            # Heatmap, movers, volume, earnings
│   ├── StockDetailErrors.tsx        # Overview, chart, news, insights
│   ├── PortfolioErrors.tsx          # Load, update, analytics
│   ├── NewsErrors.tsx               # Verification, sources, timeline
│   ├── AlertsErrors.tsx             # Creation, update, load
│   └── SettingsErrors.tsx           # Save, billing, identity, export
├── empty/
│   ├── GlobalEmptyStates.tsx        # No portfolio, watchlist, alerts, news
│   ├── DashboardEmpty.tsx           # Dashboard-specific empty states
│   ├── MarketsEmpty.tsx             # No movers, no earnings
│   ├── StockDetailEmpty.tsx         # No news, no insights
│   ├── PortfolioEmpty.tsx           # No holdings, no allocation, no analytics
│   ├── NewsEmpty.tsx                # No sources, no related companies
│   ├── AlertsEmpty.tsx              # No alerts, premium-only
│   └── SettingsEmpty.tsx            # No billing, no devices
├── loading/
│   └── IdentityLoadingStates.tsx    # Identity-aware loading indicators
├── gates/
│   └── PremiumGateStates.tsx        # Premium/Pro upgrade gates
└── offline/
    └── OfflineState.tsx             # Offline message with retry
```

### Base Component Pattern
```tsx
interface ErrorStateProps {
  message?: string;
  onRetry?: () => void;
  icon?: React.ReactNode;
  className?: string;
}

export function ErrorState({ message, onRetry, icon, className }: ErrorStateProps) {
  return (
    <div className={cn("flex flex-col items-center justify-center p-8 text-center", className)}>
      <div className="mb-4 text-sovereign-slate-400">
        {icon}
      </div>
      <p className="text-sovereign-slate-300 mb-4">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-sovereign-gold text-sovereign-obsidian rounded-lg hover:bg-sovereign-gold-hover"
        >
          Retry
        </button>
      )}
    </div>
  );
}
```

### Identity-Aware Pattern
```tsx
interface IdentityEmptyStateProps {
  identity: "diaspora" | "youth" | "creator" | "legacy";
  onAction?: () => void;
}

export function NoPortfolioEmpty({ identity, onAction }: IdentityEmptyStateProps) {
  const messages = {
    diaspora: "No holdings yet — add your first Caribbean or international stock.",
    youth: "No holdings yet — add your first stock and start learning.",
    creator: "No holdings yet — add your first creator-economy stock.",
    legacy: "No holdings yet — add your first dividend stock."
  };

  return (
    <EmptyState
      message={messages[identity]}
      icon={<PlusCircle className="w-12 h-12" />}
      actionLabel="Add Stock"
      onAction={onAction}
    />
  );
}
```

---

## 17.20 Implementation Checklist

### Phase 1: Core Components
- [ ] Create GlobalErrorStates.tsx (Network, Server, Timeout, Auth, Data)
- [ ] Create GlobalEmptyStates.tsx (No portfolio, watchlist, alerts, news)
- [ ] Create IdentityLoadingStates.tsx (Identity-aware loading)
- [ ] Create PremiumGateStates.tsx (Premium/Pro gates)
- [ ] Create OfflineState.tsx (Offline overlay)

### Phase 2: Module Components
- [ ] Create DashboardErrors.tsx + DashboardEmpty.tsx
- [ ] Create MarketsErrors.tsx + MarketsEmpty.tsx
- [ ] Create StockDetailErrors.tsx + StockDetailEmpty.tsx
- [ ] Create PortfolioErrors.tsx + PortfolioEmpty.tsx
- [ ] Create NewsErrors.tsx + NewsEmpty.tsx
- [ ] Create AlertsErrors.tsx + AlertsEmpty.tsx
- [ ] Create SettingsErrors.tsx + SettingsEmpty.tsx

### Phase 3: Integration
- [ ] Replace inline error messages with error components
- [ ] Add identity-aware empty states to Dashboard
- [ ] Add premium gates to locked features
- [ ] Add offline state overlay to root layout
- [ ] Add loading states to all async operations

### Phase 4: Testing
- [ ] Test network error scenarios
- [ ] Test empty state variations by identity
- [ ] Test premium gate CTAs
- [ ] Test offline/online transitions
- [ ] Test loading state animations

---

## 17.21 Design System Integration

### Colors
```typescript
const errorColors = {
  background: "bg-sovereign-obsidian",        // #0F172A
  text: "text-sovereign-slate-300",           // Neutral gray
  icon: "text-sovereign-slate-400",           // Muted icon
  button: "bg-sovereign-gold text-sovereign-obsidian", // Gold CTA
  border: "border-sovereign-slate-700"        // Subtle border
};
```

### Typography
```typescript
const errorTypography = {
  message: "text-base text-sovereign-slate-300",   // 16px, neutral
  heading: "text-lg font-medium text-white",       // 18px, emphasis
  caption: "text-sm text-sovereign-slate-400"      // 14px, muted
};
```

### Icons (Lucide)
```typescript
const errorIcons = {
  network: WifiOff,
  server: ServerCrash,
  timeout: Clock,
  auth: ShieldAlert,
  data: AlertCircle,
  empty: Inbox,
  premium: Lock,
  offline: WifiOff,
  loading: Loader2
};
```

---

## Summary

**Error & Empty State System:**
- ✅ 5 global error states (Network, Server, Timeout, Auth, Data)
- ✅ 7 module-specific error categories (Dashboard, Markets, Stock, Portfolio, News, Alerts, Settings)
- ✅ 15+ empty states with identity variations
- ✅ Premium/Pro gates for locked features
- ✅ Identity-aware loading states (Diaspora/Youth/Creator/Legacy)
- ✅ Offline state overlay with retry

**Principles Enforced:**
1. Never blame the user
2. Never expose internal systems
3. Never imply advice
4. Always offer a retry
5. Always stay calm and neutral
6. Always maintain identity tone

🔥 **Every error is an opportunity to build trust!**
