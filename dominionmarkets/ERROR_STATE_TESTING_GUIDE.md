# Error State Testing Guide

## Overview
This guide shows how to test all error scenarios in DominionMarkets using DevTools and mock APIs.

---

## Testing Methods

### 1. Network Errors (Offline)

**Chrome DevTools:**
1. Open DevTools (F12)
2. Go to Network tab
3. Select "Offline" from throttling dropdown
4. Reload page or trigger fetch

**Expected Result:**
- `<NetworkError />` component shows
- Message: "Unable to connect — check your connection."
- Retry button visible
- Offline overlay appears in root layout

**Test Pages:**
- Dashboard: `/dashboard/integrated`
- Portfolio: `/portfolio/integrated`
- Markets: `/markets/integrated`

---

### 2. Server Errors (500, 502, 503)

**Option A: DevTools Request Blocking**
1. Open DevTools → Network tab
2. Right-click on request
3. Select "Block request URL"
4. Add pattern to block (e.g., `*/api/dashboard*`)

**Option B: Mock API with 500 Response**
```typescript
// In your API route or mock server
export async function GET(request: Request) {
  // Simulate 500 error
  return new Response(
    JSON.stringify({ error: 'Internal server error' }),
    { status: 500 }
  );
}
```

**Expected Result:**
- `<ServerError />` component shows
- Message: "Something went wrong — try again later."
- Retry button visible

---

### 3. Timeout Errors

**Mock Slow Response:**
```typescript
// In API route or mock server
export async function GET(request: Request) {
  // Simulate 35-second delay (exceeds 30s timeout)
  await new Promise(resolve => setTimeout(resolve, 35000));
  
  return Response.json({ data: [] });
}
```

**DevTools Network Throttling:**
1. Open DevTools → Network tab
2. Select "Slow 3G" throttling
3. Trigger fetch request
4. Wait for timeout (30 seconds)

**Expected Result:**
- `<TimeoutError />` component shows
- Message: "This is taking longer than expected — retry."
- Retry button visible

---

### 4. Authentication Errors (401)

**Mock 401 Response:**
```typescript
// In API route
export async function GET(request: Request) {
  // Simulate expired token
  return new Response(
    JSON.stringify({ error: 'Unauthorized' }),
    { status: 401 }
  );
}
```

**Expected Result:**
- `<AuthenticationError />` component shows
- Message: "Your session expired — please log in again."
- Log In button redirects to `/login`

---

### 5. Generic Data Load Errors

**Mock 404 or Generic Error:**
```typescript
// In API route
export async function GET(request: Request) {
  return new Response(
    JSON.stringify({ error: 'Not found' }),
    { status: 404 }
  );
}
```

**Expected Result:**
- `<DataLoadError />` component shows
- Message: "Unable to load data — retry."
- Retry button visible

---

## Testing Empty States

### No Portfolio Holdings

**Mock Empty Response:**
```typescript
// /api/portfolio
export async function GET() {
  return Response.json({
    holdings: [],
    totalValue: 0,
    totalGainLoss: 0,
    totalGainLossPercent: 0,
    allocation: {}
  });
}
```

**Expected Result:**
- `<NoPortfolioEmpty />` shows with identity-aware message
- Diaspora: "No holdings yet — add your first Caribbean or international stock."
- Youth: "No holdings yet — add your first stock and start learning."
- Creator: "No holdings yet — add your first creator-economy stock."
- Legacy: "No holdings yet — add your first dividend stock."

### No Market Movers

**Mock Empty Movers:**
```typescript
// /api/markets/movers
export async function GET() {
  return Response.json({
    gainers: [],
    losers: []
  });
}
```

**Expected Result:**
- `<NoMoversEmpty />` shows
- Message: "No significant movement at the moment."

### No Earnings Today

**Mock Empty Earnings:**
```typescript
// /api/markets/earnings
export async function GET() {
  return Response.json({
    events: []
  });
}
```

**Expected Result:**
- `<NoEarningsEmpty />` shows
- Message: "No companies reporting earnings today."

---

## Testing Premium Gates

### Free Tier User

**Set User Tier to Free:**
```typescript
// In page component
const [userTier, setUserTier] = useState<UserTier>('free');
```

**Actions to Test:**
1. Click "Export CSV" button
2. Click "Analytics" button
3. Try to access multi-portfolio feature

**Expected Results:**
- `<PremiumGateCSVExport />` modal shows
- Message: "Upgrade to Premium to export portfolios as CSV."
- Features list displayed
- "Upgrade" button redirects to `/pricing`
- "Close" button dismisses modal

### Premium Features List

Test these premium gates:
- CSV Export: `<PremiumGateCSVExport />`
- Advanced Charts: `<PremiumGateAdvancedCharts />`
- Multi-Portfolio: `<PremiumGateMultiPortfolio />`
- AI Insights: `<PremiumGateAIInsights />`
- Analytics: `<PremiumGateAnalytics />`

---

## Testing Loading States

### Identity-Aware Loading

**Test Identity Variations:**
```typescript
// Change identity prop
<DashboardLoading identity="diaspora" />  // "Loading regional insights…"
<DashboardLoading identity="youth" />     // "Loading your learning dashboard…"
<DashboardLoading identity="creator" />   // "Loading creator-economy data…"
<DashboardLoading identity="legacy" />    // "Loading long-term indicators…"
```

**Verify Messages:**
- Diaspora loading shows: "Loading regional insights…"
- Youth loading shows: "Loading your learning dashboard…"
- Creator loading shows: "Loading creator-economy data…"
- Legacy loading shows: "Loading long-term indicators…"

### Skeleton Loaders

**Test Skeleton Components:**
```typescript
<TableSkeleton rows={5} columns={5} />   // Portfolio table
<CardSkeleton />                          // Dashboard widget
<ChartSkeleton />                         // Chart visualization
```

**Verify:**
- Animated pulse effect
- Correct number of rows/columns
- Appropriate sizing

---

## Testing Offline Mode

### Simulate Offline

**Chrome DevTools:**
1. Open DevTools (F12)
2. Go to Application tab
3. Check "Offline" in Service Workers section

OR

1. Network tab → Select "Offline"

**Expected Results:**
- `<OfflineOverlay />` shows full-screen
- Message: "You're offline — reconnect to continue."
- "Check Connection" button visible
- "View Cached Data" button visible (if cached data exists)
- `<CompactOfflineIndicator />` shows in nav bar

### Cached Data

**Test Cached Portfolio:**
```typescript
// Save to localStorage
localStorage.setItem('cached_portfolio', JSON.stringify({
  data: { holdings: [...] },
  timestamp: Date.now()
}));
```

**Go Offline and Test:**
1. Load portfolio page
2. Go offline
3. Click "View Cached Data"
4. Verify cached data loads
5. See "Last synced" timestamp

---

## Mock API Server (Optional)

Create a mock API server for comprehensive testing:

```typescript
// lib/mockApi.ts
export const mockApiHandlers = {
  // Simulate network error
  networkError: () => {
    throw new Error('Network request failed');
  },

  // Simulate 500 error
  serverError: () => {
    return new Response(
      JSON.stringify({ error: 'Internal server error' }),
      { status: 500 }
    );
  },

  // Simulate timeout
  timeout: async () => {
    await new Promise(resolve => setTimeout(resolve, 35000));
    return Response.json({ data: [] });
  },

  // Simulate 401
  authError: () => {
    return new Response(
      JSON.stringify({ error: 'Unauthorized' }),
      { status: 401 }
    );
  },

  // Simulate empty data
  emptyData: () => {
    return Response.json({
      holdings: [],
      alerts: [],
      news: []
    });
  }
};
```

---

## Testing Checklist

### Error States
- [ ] Network error (offline) shows NetworkError
- [ ] Server error (500) shows ServerError
- [ ] Timeout (30s+) shows TimeoutError
- [ ] Auth error (401) shows AuthenticationError
- [ ] Generic error shows DataLoadError
- [ ] SmartErrorBoundary auto-detects error type
- [ ] Retry buttons work correctly
- [ ] Error messages are calm and neutral

### Empty States
- [ ] No portfolio shows NoPortfolioEmpty
- [ ] No watchlist shows NoWatchlistEmpty
- [ ] No alerts shows NoAlertsEmpty (identity-aware)
- [ ] No market movers shows NoMoversEmpty
- [ ] No earnings shows NoEarningsEmpty
- [ ] Identity variations work (Diaspora/Youth/Creator/Legacy)
- [ ] Action buttons work correctly

### Loading States
- [ ] Dashboard loading shows identity message
- [ ] Portfolio loading shows identity message
- [ ] Markets loading shows identity message
- [ ] Skeleton loaders animate correctly
- [ ] TableSkeleton shows correct rows/columns
- [ ] CardSkeleton renders properly
- [ ] ChartSkeleton displays correctly

### Premium Gates
- [ ] Free tier triggers premium gates
- [ ] Premium/Pro tier bypasses gates
- [ ] CSV Export gate shows features list
- [ ] Analytics gate shows features list
- [ ] Upgrade button redirects to /pricing
- [ ] Close button dismisses modal
- [ ] PremiumBadge shows on locked features

### Offline Mode
- [ ] Offline overlay appears when offline
- [ ] CompactOfflineIndicator shows in nav
- [ ] "Check Connection" button works
- [ ] "View Cached Data" works when available
- [ ] Cached data timestamp displays correctly
- [ ] Overlay auto-dismisses when online

---

## Browser DevTools Shortcuts

### Chrome
- **Open DevTools:** F12 or Ctrl+Shift+I
- **Network Tab:** Ctrl+Shift+N (while DevTools open)
- **Offline Mode:** Network tab → Offline dropdown
- **Block Requests:** Network tab → Right-click → Block URL
- **Throttling:** Network tab → Throttling dropdown

### Firefox
- **Open DevTools:** F12 or Ctrl+Shift+I
- **Network Tab:** Ctrl+Shift+E
- **Offline Mode:** File → Work Offline

### Safari
- **Open DevTools:** Cmd+Option+I
- **Network Tab:** Cmd+Option+R
- **Throttling:** Develop → Network Conditions

---

## Common Issues & Solutions

### Error state not showing
- Check if error is caught properly in try/catch
- Verify error object has correct shape
- Check SmartErrorBoundary is wrapping component

### Loading state flickers
- Add minimum loading time (300ms)
- Use debounce for rapid state changes

### Premium gate not appearing
- Verify userTier state is 'free'
- Check gate component is imported correctly
- Ensure modal is not hidden by z-index

### Offline overlay not showing
- Check navigator.onLine is false
- Verify component is in root layout
- Test on actual device (not just DevTools)

---

## Summary

**Test Coverage:**
- ✅ 5 error types (Network, Server, Timeout, Auth, Data)
- ✅ 8+ empty states (identity-aware)
- ✅ 4 identity loading variations
- ✅ 6+ premium gates
- ✅ Offline mode with caching
- ✅ Skeleton loaders (Table, Card, Chart)

**Testing Time:** ~30 minutes for full coverage

🔥 **Every error scenario builds trust. Test them all!**
