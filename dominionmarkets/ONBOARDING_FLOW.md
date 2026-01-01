# DOMINIONMARKETS — ONBOARDING FLOW

> **Purpose:** Short, clean, confidence-building first experience  
> **Goal:** Get users to dashboard with minimal friction  
> **Length:** 5 screens (2-3 minutes max)

---

## 🎯 ONBOARDING PHILOSOPHY

### Design Principles

**1. Clarity Over Completeness**
- Don't overwhelm with features
- Show value immediately
- Allow skipping non-essential steps

**2. Trust Through Transparency**
- Explain why we need information
- Show data privacy commitments
- Never surprise users

**3. Progressive Disclosure**
- Start simple
- Add complexity gradually
- Let users explore at their pace

**4. Quick Wins**
- Show working dashboard fast
- Let users customize later
- Celebrate small completions

---

## 📱 SCREEN 1: WELCOME

### Visual Layout
```
┌─────────────────────────────────────┐
│                                     │
│         [DominionMarkets Logo]      │
│                                     │
│      Welcome to DominionMarkets     │
│                                     │
│     Your window into global         │
│           markets.                  │
│                                     │
│                                     │
│       [Get Started Button]          │
│                                     │
│   Already have an account? [Login]  │
│                                     │
└─────────────────────────────────────┘
```

### Copy

**Headline:**
```
Welcome to DominionMarkets
```

**Subheadline:**
```
Your window into global markets.
```

**Primary CTA:**
```
[Get Started]
```
*Action:* Navigate to Screen 2

**Secondary CTA:**
```
Already have an account? [Login]
```
*Action:* Navigate to login page

### Design Specs

**Background:**
- Gradient: Caribbean Blue (#003049) to darker shade
- Subtle animated background (floating data points, slow)

**Logo:**
- Size: 80px × 80px
- Position: Top center
- Animation: Fade in (500ms)

**Text:**
- Headline: 32px bold, white
- Subheadline: 18px regular, white (80% opacity)

**Button:**
- Primary: Gold (#F2C94C) background, dark text
- Width: 280px (desktop), 90% (mobile)
- Height: 56px
- Border radius: 8px
- Hover: Lighten 10%

**Animation:**
- Logo fades in (500ms)
- Headline fades in (700ms, delay 200ms)
- Subheadline fades in (700ms, delay 400ms)
- Button fades in (700ms, delay 600ms)

### Tracking Event
```javascript
analytics.track('onboarding_started', {
  timestamp: new Date(),
  source: 'homepage'
});
```

---

## 📋 SCREEN 2: WHAT YOU GET

### Visual Layout
```
┌─────────────────────────────────────┐
│   [Progress: 1/5]           [Skip]  │
│                                     │
│   What you get with DominionMarkets │
│                                     │
│   📈 Real-time data                 │
│   Track live prices on stocks,      │
│   indices, and sectors.             │
│                                     │
│   💼 Portfolio tracking             │
│   See your allocation, performance, │
│   and risk — privately.             │
│                                     │
│   📰 Verified news                  │
│   Multi-source fact-checking        │
│   for trusted headlines.            │
│                                     │
│   🤖 AI summaries                   │
│   Descriptive insights (never       │
│   advice) on your portfolio.        │
│                                     │
│   🔔 Custom alerts                  │
│   Get notified on price changes,    │
│   volume spikes, and news.          │
│                                     │
│          [Continue]                 │
│                                     │
└─────────────────────────────────────┘
```

### Copy

**Headline:**
```
What you get with DominionMarkets
```

**Features (5 Items):**

**1. Real-time data**
```
📈 Real-time data
Track live prices on stocks, indices, and sectors.
```

**2. Portfolio tracking**
```
💼 Portfolio tracking
See your allocation, performance, and risk — privately.
```

**3. Verified news**
```
📰 Verified news
Multi-source fact-checking for trusted headlines.
```

**4. AI summaries**
```
🤖 AI summaries
Descriptive insights (never advice) on your portfolio.
```

**5. Custom alerts**
```
🔔 Custom alerts
Get notified on price changes, volume spikes, and news.
```

**Primary CTA:**
```
[Continue]
```
*Action:* Navigate to Screen 3

**Secondary CTA (Top Right):**
```
[Skip]
```
*Action:* Navigate directly to dashboard

### Design Specs

**Progress Indicator:**
- Position: Top left
- Format: "1/5"
- Color: White with 60% opacity
- Font: 14px regular

**Skip Button:**
- Position: Top right
- Color: White text (60% opacity)
- Hover: 100% opacity
- Font: 14px regular

**Feature List:**
- Icon size: 32px
- Icon-to-text spacing: 16px
- Feature title: 18px bold, white
- Feature description: 14px regular, white (80% opacity)
- Vertical spacing between items: 24px

**Background:**
- Same gradient as Screen 1
- Maintain consistency

**Button:**
- Same specs as Screen 1

### Animation
- Features fade in sequentially (100ms delay between each)
- Total animation time: 500ms

### Tracking Event
```javascript
analytics.track('onboarding_features_viewed', {
  timestamp: new Date(),
  screen: 2
});
```

---

## 💼 SCREEN 3: PORTFOLIO SETUP

### Visual Layout
```
┌─────────────────────────────────────┐
│   [Progress: 2/5]           [Skip]  │
│                                     │
│   Add your holdings to unlock       │
│         insights.                   │
│                                     │
│   We don't connect to brokers.      │
│   Your data stays private.          │
│                                     │
│   ┌─────────────────────────────┐  │
│   │  [Manual Entry Icon]        │  │
│   │  Add Manually               │  │
│   │  Enter symbols and shares   │  │
│   └─────────────────────────────┘  │
│                                     │
│   ┌─────────────────────────────┐  │
│   │  [CSV Upload Icon]          │  │
│   │  Import CSV                 │  │
│   │  Upload holdings spreadsheet│  │
│   └─────────────────────────────┘  │
│                                     │
│   ┌─────────────────────────────┐  │
│   │  [Skip Icon]                │  │
│   │  Skip for now               │  │
│   │  Explore first, add later   │  │
│   └─────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

### Copy

**Headline:**
```
Add your holdings to unlock insights.
```

**Subheadline:**
```
We don't connect to brokers.
Your data stays private.
```

**Option 1: Manual Entry**
```
[Icon: ✍️ Manual Entry]
Add Manually
Enter symbols and shares one by one.
```
*Action:* Open manual entry form (inline)

**Option 2: CSV Import**
```
[Icon: 📄 CSV Upload]
Import CSV
Upload a spreadsheet with your holdings.
```
*Action:* Open file picker

**Option 3: Skip**
```
[Icon: ⏭️ Skip]
Skip for now
Explore first, add your portfolio later.
```
*Action:* Navigate to Screen 4

### Design Specs

**Headline:**
- Font: 28px bold, white
- Position: Top center

**Subheadline:**
- Font: 14px regular, white (80% opacity)
- Position: Below headline
- Privacy icon: 🔒 before text

**Option Cards:**
- Width: 100% (max 400px)
- Height: 120px
- Background: White with 10% opacity
- Border: 1px solid white with 20% opacity
- Border radius: 12px
- Padding: 20px
- Hover: Background white with 15% opacity, cursor pointer
- Vertical spacing: 16px between cards

**Card Content:**
- Icon: 40px, top-left
- Title: 18px bold, white
- Description: 14px regular, white (80% opacity)

**Manual Entry Form (If Selected):**
```
┌─────────────────────────────────────┐
│   Stock Symbol                      │
│   [Input: e.g., AAPL]               │
│                                     │
│   Number of Shares                  │
│   [Input: e.g., 10]                 │
│                                     │
│   Purchase Price (Optional)         │
│   [Input: e.g., $150.00]            │
│                                     │
│   [Add Holding]  [Add More]         │
│                                     │
└─────────────────────────────────────┘
```

**CSV Template Link:**
```
Need a template? [Download CSV Template]
```

### Animation
- Options fade in sequentially (150ms delay)
- Manual form slides in from right (300ms)

### Tracking Event
```javascript
analytics.track('onboarding_portfolio_setup', {
  timestamp: new Date(),
  option_selected: 'manual' | 'csv' | 'skip'
});
```

---

## 📊 SCREEN 4: WATCHLIST SETUP

### Visual Layout
```
┌─────────────────────────────────────┐
│   [Progress: 3/5]           [Skip]  │
│                                     │
│   Choose the stocks you want        │
│         to follow.                  │
│                                     │
│   [Search: Type symbol or company]  │
│                                     │
│   Popular:                          │
│   [+ AAPL] [+ MSFT] [+ GOOGL]      │
│   [+ TSLA] [+ NVDA] [+ AMZN]       │
│                                     │
│   Caribbean:                        │
│   [+ NCB.JA] [+ JMMB.JA]           │
│   [+ RBL.TT] [+ ANSA.TT]           │
│                                     │
│   Your Watchlist (4):               │
│   • AAPL                 [Remove]   │
│   • MSFT                 [Remove]   │
│   • GOOGL                [Remove]   │
│   • NCB.JA               [Remove]   │
│                                     │
│          [Build My Dashboard]       │
│                                     │
└─────────────────────────────────────┘
```

### Copy

**Headline:**
```
Choose the stocks you want to follow.
```

**Search Placeholder:**
```
Type symbol or company name (e.g., Apple or AAPL)
```

**Popular Stocks Section:**
```
Popular:
```
Chips: AAPL, MSFT, GOOGL, TSLA, NVDA, AMZN

**Caribbean Stocks Section:**
```
Caribbean:
```
Chips: NCB.JA, JMMB.JA, RBL.TT, ANSA.TT

**Your Watchlist:**
```
Your Watchlist (4):
```
List with remove buttons

**Primary CTA:**
```
[Build My Dashboard]
```
*Action:* Navigate to Screen 5

**Secondary CTA (Top Right):**
```
[Skip]
```
*Action:* Navigate to Screen 5 with empty watchlist

### Design Specs

**Search Bar:**
- Width: 100% (max 500px)
- Height: 48px
- Background: White with 10% opacity
- Border: 1px solid white with 20% opacity
- Border radius: 8px
- Placeholder: White with 60% opacity
- Icon: 🔍 (left side, 16px from edge)

**Stock Chips (Add Buttons):**
- Background: White with 10% opacity
- Border: 1px solid white with 20% opacity
- Border radius: 20px (pill shape)
- Padding: 8px 16px
- Font: 14px medium, white
- Hover: Background white with 15% opacity
- Active state: Gold (#F2C94C) background, dark text
- Icon: + before symbol

**Section Headers:**
- Font: 16px bold, white
- Margin-top: 24px

**Watchlist Items:**
- Background: White with 10% opacity
- Border radius: 8px
- Padding: 12px 16px
- Font: 16px medium, white
- Remove button: Red icon on hover

**Button (Build My Dashboard):**
- Same primary button specs
- Disabled if watchlist empty (lower opacity, no hover)

### Interaction Flow

**1. User clicks chip (+AAPL):**
- Chip changes to active state (gold background)
- Symbol appears in "Your Watchlist"
- Count updates: (1), (2), etc.

**2. User searches symbol:**
- Dropdown shows results below search
- Click result to add to watchlist

**3. User removes symbol:**
- Confirm dialog: "Remove AAPL from watchlist?"
- Yes: Symbol removed, chip returns to inactive state

### Animation
- Chips fade in (staggered, 50ms delay each)
- Watchlist items slide in from left (200ms)

### Tracking Event
```javascript
analytics.track('onboarding_watchlist_created', {
  timestamp: new Date(),
  symbols_added: ['AAPL', 'MSFT', 'GOOGL', 'NCB.JA'],
  watchlist_count: 4
});
```

---

## 🎉 SCREEN 5: DASHBOARD READY

### Visual Layout
```
┌─────────────────────────────────────┐
│                                     │
│         [Success Icon: ✅]          │
│                                     │
│   Your market intelligence hub      │
│          is live.                   │
│                                     │
│   You're all set! Here's what       │
│   you can do now:                   │
│                                     │
│   • Track 4 stocks in real-time     │
│   • View market movers and trends   │
│   • Read verified financial news    │
│   • Get AI insights on your data    │
│                                     │
│                                     │
│      [Enter DominionMarkets]        │
│                                     │
│   Want more? [Upgrade to Premium]   │
│                                     │
└─────────────────────────────────────┘
```

### Copy

**Success Icon:**
```
✅ (80px size, animated checkmark)
```

**Headline:**
```
Your market intelligence hub is live.
```

**Subheadline:**
```
You're all set! Here's what you can do now:
```

**Capability List:**
```
• Track 4 stocks in real-time
• View market movers and trends
• Read verified financial news
• Get AI insights on your data
```
*(List items dynamically based on user's setup)*

**Primary CTA:**
```
[Enter DominionMarkets]
```
*Action:* Navigate to dashboard

**Secondary CTA:**
```
Want more? [Upgrade to Premium]
```
*Action:* Navigate to pricing page (opens in new tab)

### Design Specs

**Success Icon:**
- Size: 80px × 80px
- Color: Market Green (#00A896)
- Animation: Scale up from 0 to 1 (400ms), then pulse once (200ms)

**Headline:**
- Font: 32px bold, white
- Position: Center

**Subheadline:**
- Font: 16px regular, white (80% opacity)
- Margin-top: 16px

**Capability List:**
- Bullet style: • (white with 80% opacity)
- Font: 16px regular, white
- Line height: 1.6
- Margin-top: 24px

**Primary Button:**
- Same specs as previous screens
- Full width on mobile

**Secondary CTA:**
- Font: 14px medium, white with 60% opacity
- Underline on hover
- Position: Below primary button (16px margin)

### Animation

**Entry sequence:**
1. Success icon animates in (400ms)
2. Headline fades in (300ms, delay 400ms)
3. Subheadline fades in (300ms, delay 600ms)
4. Capability list fades in (300ms, delay 800ms)
5. Buttons fade in (300ms, delay 1000ms)

**Confetti (Optional):**
- Brief confetti animation (2 seconds)
- Triggered on page load
- Colors: Caribbean Blue, Market Green, Gold

### Tracking Event
```javascript
analytics.track('onboarding_completed', {
  timestamp: new Date(),
  portfolio_added: true,
  watchlist_count: 4,
  time_spent_seconds: 120
});
```

---

## 🔄 OPTIONAL SCREEN: EMAIL VERIFICATION

*(Insert between Screen 5 and Dashboard if email not verified)*

### Visual Layout
```
┌─────────────────────────────────────┐
│                                     │
│        [Email Icon: 📧]             │
│                                     │
│   Verify your email to unlock       │
│       all features.                 │
│                                     │
│   We sent a verification link to:   │
│   user@example.com                  │
│                                     │
│   Check your inbox (and spam).      │
│                                     │
│      [Resend Email]                 │
│                                     │
│   [I'll do this later]              │
│                                     │
└─────────────────────────────────────┘
```

### Copy

**Headline:**
```
Verify your email to unlock all features.
```

**Body:**
```
We sent a verification link to:
user@example.com

Check your inbox (and spam folder).
```

**Primary CTA:**
```
[Resend Email]
```
*Action:* Trigger email resend

**Secondary CTA:**
```
[I'll do this later]
```
*Action:* Skip to dashboard

### Tracking Event
```javascript
analytics.track('email_verification_prompted', {
  timestamp: new Date(),
  email: 'user@example.com'
});
```

---

## 📊 ONBOARDING METRICS

### Success Metrics

**Completion Rate:**
- **Target:** 70%+ of users complete all 5 screens
- **Baseline:** 50-60% (industry average)

**Time to Dashboard:**
- **Target:** 2-3 minutes average
- **Baseline:** 5+ minutes (too slow)

**Portfolio Setup Rate:**
- **Target:** 50%+ add at least 1 holding
- **Baseline:** 30-40%

**Watchlist Setup Rate:**
- **Target:** 80%+ add at least 3 stocks
- **Baseline:** 60-70%

### Drop-off Analysis

**Expected Drop-off Points:**
1. **Screen 2 (Features):** 10-15% skip immediately
2. **Screen 3 (Portfolio):** 30-40% skip (privacy concern or lazy)
3. **Screen 4 (Watchlist):** 15-20% skip
4. **Screen 5 (Completion):** 5% abandon before entering dashboard

**Mitigation Strategies:**
- Allow skipping all non-essential steps
- Show value before asking for input
- Minimize form fields
- Use smart defaults (pre-populate popular stocks)

---

## 🎨 DESIGN VARIATIONS

### Desktop vs. Mobile

**Desktop (≥1200px):**
- Center modal (max width 600px)
- Background: Blurred dashboard preview
- Box shadow for elevation

**Mobile (<768px):**
- Full screen
- No modal
- Solid background gradient

### Light Mode Variant

*(If adding light mode)*

**Background:**
- White with subtle gradient
- Caribbean Blue accents

**Text:**
- Slate Gray (#4F4F4F) for body
- Black (#0F172A) for headlines

**Buttons:**
- Primary: Caribbean Blue background, white text
- Secondary: White background, Caribbean Blue border

---

## 🧪 A/B TEST IDEAS

### Experiment 1: Portfolio Setup Position
- **Variant A (Current):** Portfolio setup on Screen 3
- **Variant B:** Portfolio setup after dashboard (post-onboarding)
- **Hypothesis:** Delaying portfolio setup increases completion rate

### Experiment 2: Watchlist Defaults
- **Variant A (Current):** Empty watchlist, user adds manually
- **Variant B:** Pre-populated with 5 popular stocks (user can remove)
- **Hypothesis:** Pre-populated watchlist increases engagement

### Experiment 3: Screen Count
- **Variant A (Current):** 5 screens
- **Variant B:** 3 screens (combine Features + Portfolio + Watchlist)
- **Hypothesis:** Fewer screens increases completion rate

### Experiment 4: CTA Copy
- **Variant A (Current):** "Build My Dashboard"
- **Variant B:** "Show Me the Data"
- **Hypothesis:** Action-oriented copy increases clicks

---

## ♿ ACCESSIBILITY

### Keyboard Navigation

**Tab Order:**
1. Skip button (top right)
2. Primary CTA (bottom)
3. Secondary options (if present)

**Keyboard Shortcuts:**
- `Enter`: Proceed to next screen
- `Esc`: Skip current screen
- `Tab`: Navigate focusable elements

### Screen Reader Announcements

**Screen 1:**
```
"Welcome to DominionMarkets. Your window into global markets. Button: Get Started."
```

**Screen 4 (Watchlist):**
```
"Added Apple to watchlist. Your watchlist now has 1 stock."
```

**Screen 5:**
```
"Success! Your market intelligence hub is live. Button: Enter DominionMarkets."
```

### Focus States

**All interactive elements:**
- 2px solid outline (Gold #F2C94C)
- Offset: 2px
- Visible on keyboard focus, not mouse click

---

## ✅ ONBOARDING CHECKLIST

- [x] 5 screens designed (Welcome, Features, Portfolio, Watchlist, Success)
- [x] Copy written for all screens
- [x] CTAs defined (primary + secondary)
- [x] Skip options provided
- [x] Design specs documented
- [x] Animation details included
- [x] Tracking events specified
- [x] Mobile responsive layouts defined
- [x] Accessibility guidelines included
- [x] A/B test ideas proposed

---

**Status:** ONBOARDING FLOW COMPLETE ✅  
**Next Steps:** Build React components, integrate with auth system, test user flows  
**Launch Target:** Q2 2025
