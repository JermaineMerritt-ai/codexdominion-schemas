# DOMINIONMARKETS — CROSS-PROMOTION ENGINE

> **Purpose:** Tactical integration between CodexDominion and DominionMarkets  
> **Goal:** Create seamless ecosystem where users flow between sub-brands  
> **Target:** 30% cross-platform usage (users active on 2+ sub-brands)

---

## 🌐 ECOSYSTEM OVERVIEW

### The Three Sub-Brands

1. **IslandNation (Creator Marketplace)**
   - Creators sell digital products (courses, templates, ebooks)
   - Revenue: 85% creator, 15% platform
   - Target: 50,000 creators by Year 3

2. **DominionYouth (Youth Engagement)**
   - Gamified challenges, educational content, skill-building
   - Revenue: Challenge fees, badge systems, sponsorships
   - Target: 100,000 youth by Year 3

3. **DominionMarkets (Financial Data Platform)**
   - Real-time stock data, verified news, portfolio tracking
   - Revenue: Premium subscriptions ($9.99/mo), Pro ($19.99/mo)
   - Target: 50,000 users by Year 3

---

## 🔗 INTEGRATION ARCHITECTURE

### Shared Infrastructure

**1. Single Sign-On (SSO)**
- One account works across all 3 sub-brands
- Auth0 handles authentication
- User profile syncs across platforms

**2. Shared Design System**
- CodexDominion Imperial Gold (#F5C542)
- Obsidian Black (#0F172A)
- Caribbean Blue (#003049) for DominionMarkets
- Consistent typography, spacing, components

**3. Unified AI Engine**
- GPT-4 backend powers all 3 platforms
- Compliance-safe prompts (descriptive only, never advice)
- Shared AI usage quota (Premium users get unlimited across all brands)

**4. Shared Data Infrastructure**
- PostgreSQL database (users, subscriptions, transactions)
- Redis caching (real-time data, session management)
- JSON ledgers (treasury, cycles, proclamations)

---

## 🎯 CROSS-PROMOTION PATHWAYS

### A. From CodexDominion → DominionMarkets

#### 1. Creator Marketplace Integration

**Scenario:** Creator on IslandNation sells finance course

**Integration Points:**

**a) Featured Courses in DominionMarkets "Learn" Tab**

```
┌─────────────────────────────────────────────────────────────────┐
│ DOMINIONMARKETS DASHBOARD — LEARN TAB                           │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ FEATURED COURSES (from IslandNation)                        ││
│ │                                                             ││
│ │ ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         ││
│ │ │ Course 1    │  │ Course 2    │  │ Course 3    │         ││
│ │ │ [Cover img] │  │ [Cover img] │  │ [Cover img] │         ││
│ │ │             │  │             │  │             │         ││
│ │ │ "Stock      │  │ "Build Your │  │ "Caribbean  │         ││
│ │ │  Analysis   │  │  First      │  │  Markets    │         ││
│ │ │  for        │  │  Portfolio" │  │  101"       │         ││
│ │ │  Beginners" │  │             │  │             │         ││
│ │ │             │  │             │  │             │         ││
│ │ │ By Sarah M. │  │ By John T.  │  │ By Maria P. │         ││
│ │ │ $29.99      │  │ $19.99      │  │ $39.99      │         ││
│ │ │             │  │             │  │             │         ││
│ │ │ [Enroll →]  │  │ [Enroll →]  │  │ [Enroll →]  │         ││
│ │ └─────────────┘  └─────────────┘  └─────────────┘         ││
│ │                                                             ││
│ │ [Browse All Courses on IslandNation →]                     ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Revenue Flow:**
- User enrolls in course from DominionMarkets
- Payment processed on IslandNation
- Revenue split: 85% creator, 15% platform
- Attribution tracked: DominionMarkets referred user

---

**b) Creator Profile Badge in DominionMarkets**

Creators who sell finance courses on IslandNation get a badge in DominionMarkets:

```
User Profile: Sarah M.
📹 Creator on IslandNation | 12 finance courses | 4.8★ (1,200 reviews)
[View Creator Profile →]
```

**User Flow:**
1. User sees Sarah's comment in DominionMarkets community forum
2. Clicks Sarah's profile → Sees "Creator on IslandNation" badge
3. Clicks "View Creator Profile" → Redirects to IslandNation
4. Browses Sarah's courses → Enrolls in "Stock Analysis for Beginners"

---

**c) Embedded Course Previews**

DominionMarkets users can preview IslandNation courses without leaving the platform:

```
┌─────────────────────────────────────────────────────────────────┐
│ AI INSIGHTS PANEL                                               │
│                                                                 │
│ 🤖 "Your portfolio is heavily concentrated in technology       │
│     (45%). Consider diversifying into other sectors."          │
│                                                                 │
│ 💡 WANT TO LEARN MORE ABOUT DIVERSIFICATION?                   │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────┐  │
│ │ 🎥 "Diversification 101" (Course Preview)                │  │
│ │                                                          │  │
│ │ [5-minute video preview plays inline]                    │  │
│ │                                                          │  │
│ │ By John T. on IslandNation | $19.99                     │  │
│ │ ⭐⭐⭐⭐⭐ 4.9 (320 reviews)                               │  │
│ │                                                          │  │
│ │ [Enroll in Full Course →]                               │  │
│ └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

#### 2. Youth Challenge Integration

**Scenario:** Youth completes financial literacy challenge on DominionYouth

**Integration Points:**

**a) DominionYouth Badge Unlocks DominionMarkets Access**

```
DominionYouth Challenge Complete!

🎓 You earned: "Financial Literacy Champion" badge

🎁 REWARD: 1 month DominionMarkets Premium FREE

[Claim Your Reward →]
```

**User Flow:**
1. Youth completes "90-Day Finance Challenge" on DominionYouth
2. Earns badge + 1 month DominionMarkets Premium
3. Clicks "Claim Your Reward" → Auto-redirects to DominionMarkets
4. Premium features unlocked for 30 days
5. End of month: Upgrade prompt (50% off first paid month)

---

**b) Youth Portfolio Challenges in DominionMarkets**

DominionYouth users see gamified portfolio challenges in DominionMarkets:

```
┌─────────────────────────────────────────────────────────────────┐
│ DOMINIONMARKETS — YOUTH CHALLENGES                              │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ 🎯 CHALLENGE: Build Your First Mock Portfolio              ││
│ │                                                             ││
│ │ Duration: 30 minutes                                        ││
│ │ Reward: 250 points + 💼 Portfolio Builder badge            ││
│ │                                                             ││
│ │ Tasks:                                                      ││
│ │ 1. Add 5 stocks to mock portfolio                          ││
│ │ 2. Allocate percentages (total = 100%)                     ││
│ │ 3. Submit for AI review                                    ││
│ │                                                             ││
│ │ [Start Challenge →]                                        ││
│ │                                                             ││
│ │ 🔥 432 users completed this challenge today                ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ [View All Challenges on DominionYouth →]                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Badge System Sync:**
- Badges earned in DominionMarkets appear in DominionYouth profile
- Youth can show off financial literacy badges to peers
- Leaderboard: Top badge earners each month

---

**c) Youth Dashboard Widget in DominionMarkets**

Youth users see a special widget promoting DominionYouth challenges:

```
┌─────────────────────────────────────────────────────────────────┐
│ YOUR DOMINIONYOUTH PROGRESS                                     │
│                                                                 │
│ Challenges Completed: 7/12                                      │
│ Badges Earned: 5                                                │
│ Next Badge: 🔥 Finance Streak (complete 3 more challenges)     │
│                                                                 │
│ [Continue Challenges →]                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

#### 3. Diaspora Economic Synergy

**Scenario:** Diaspora user tracks Caribbean stocks in DominionMarkets

**Integration Points:**

**a) IslandNation Caribbean Creator Spotlight**

DominionMarkets users interested in Caribbean markets see featured creators:

```
┌─────────────────────────────────────────────────────────────────┐
│ CARIBBEAN MARKETS — FEATURED CREATORS                           │
│                                                                 │
│ 📹 "JSE Investing 101" by Maria P.                             │
│    Course on IslandNation | $39.99                             │
│    Learn: Jamaica Stock Exchange basics, top companies, risks  │
│    [Enroll →]                                                  │
│                                                                 │
│ 📹 "Trinidad & Tobago Stocks" by Kevin R.                      │
│    Course on IslandNation | $29.99                             │
│    Learn: TTSE overview, energy sector, banking sector         │
│    [Enroll →]                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

**b) DominionYouth Caribbean Youth Challenge**

Youth from Caribbean diaspora (Toronto, London, New York) complete special challenge:

```
🎯 CHALLENGE: Caribbean Roots Portfolio

Build a mock portfolio with 50% Caribbean stocks, 50% US stocks.

Tasks:
1. Add 3 Caribbean stocks (JSE, TTSE, or BSE)
2. Add 3 US stocks
3. Allocate 50/50 split
4. Track performance for 7 days

Reward: 🇯🇲 Caribbean Roots badge + 300 points

[Start Challenge →]
```

---

### B. From DominionMarkets → CodexDominion

#### 1. Creator Recruitment Pipeline

**Scenario:** DominionMarkets user wants to teach finance

**Integration Points:**

**a) "Become a Creator" Banner in DominionMarkets**

Premium/Pro users see banner:

```
┌─────────────────────────────────────────────────────────────────┐
│ 💡 LOVE DOMINIONMARKETS? TEACH OTHERS.                         │
│                                                                 │
│ Create finance courses on IslandNation.                        │
│ Earn 85% revenue share.                                        │
│                                                                 │
│ [Become a Creator →]                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**User Flow:**
1. User clicks "Become a Creator"
2. Redirects to IslandNation signup
3. SSO auto-fills email and name
4. Guided onboarding: Upload course, set price, publish
5. Course appears in DominionMarkets "Learn" tab

---

**b) AI-Generated Course Ideas**

DominionMarkets analyzes user's activity and suggests course ideas:

```
🤖 AI SUGGESTION: You could teach this!

Based on your DominionMarkets activity:
• You've used AI summaries 200+ times
• You track 25 stocks across 5 sectors
• You've completed 8 financial literacy modules

Course Idea:
"How to Build a Diversified Portfolio (Step-by-Step)"

Estimated Revenue: $1,500-$3,000/month (based on similar courses)

[Create Course on IslandNation →]

⚠️ AI-generated suggestion. Not a guarantee.
```

---

#### 2. Youth Onboarding Funnel

**Scenario:** Youth signs up for DominionMarkets, gets introduced to DominionYouth

**Integration Points:**

**a) Onboarding Screen: "You're Part of Something Bigger"**

After completing DominionMarkets onboarding (5 screens), youth sees:

```
┌─────────────────────────────────────────────────────────────────┐
│ 🎉 YOU'RE ALL SET!                                             │
│                                                                 │
│ You're now part of the CodexDominion ecosystem.                │
│                                                                 │
│ DominionMarkets ✅ (You're here)                               │
│ • Track stocks, verified news, AI insights                     │
│                                                                 │
│ DominionYouth (New to you?)                                    │
│ • Complete challenges, earn badges, compete with friends       │
│ • 432 youth completed challenges today                         │
│                                                                 │
│ [Explore DominionYouth →] [Skip for now]                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

**b) Cross-Platform Leaderboards**

Youth can compete across both platforms:

```
🏆 YOUTH LEADERBOARD (All Platforms)

1. @jordan_invests | 12,450 points
   • DominionMarkets: 5 badges
   • DominionYouth: 7 challenges

2. @sarah_finance | 11,320 points
   • DominionMarkets: 4 badges
   • DominionYouth: 9 challenges

3. @marcus_trader | 10,890 points
   • DominionMarkets: 6 badges
   • DominionYouth: 5 challenges

Your Rank: #87 (Keep climbing!)

[View Full Leaderboard →]
```

---

#### 3. Premium Subscription Bundles

**Scenario:** User subscribes to DominionMarkets Premium, gets perks across all platforms

**Integration Points:**

**a) Ecosystem Premium Bundle**

```
┌─────────────────────────────────────────────────────────────────┐
│ 🌟 ECOSYSTEM PREMIUM ($14.99/month)                            │
│                                                                 │
│ One subscription. Three platforms.                              │
│                                                                 │
│ ✓ DominionMarkets Premium                                      │
│   • Unlimited stocks, AI, alerts                               │
│                                                                 │
│ ✓ IslandNation Creator Tools                                   │
│   • Advanced analytics, priority support                       │
│                                                                 │
│ ✓ DominionYouth Pro Features                                   │
│   • Exclusive challenges, badges, rewards                      │
│                                                                 │
│ Save $10/month vs. individual subscriptions                     │
│                                                                 │
│ [Upgrade to Ecosystem Premium →]                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Pricing:**
- DominionMarkets Premium alone: $9.99/mo
- IslandNation Creator Tools: $9.99/mo
- DominionYouth Pro: $4.99/mo
- **Total if separate:** $24.97/mo
- **Ecosystem Bundle:** $14.99/mo (40% savings)

---

**b) Premium Badge Across All Platforms**

Users with Ecosystem Premium get a special badge:

```
User Profile: Jermaine Merritt
🌟 Ecosystem Premium Member
```

Badge appears in:
- DominionMarkets dashboard (header)
- IslandNation creator profile
- DominionYouth leaderboard

---

## 🔄 EVENT APIs & DATA SHARING

### Shared Event System

**Architecture:** Event-driven communication between sub-brands

**Example Events:**

1. **user.badge_earned** (DominionMarkets → DominionYouth)
   ```json
   {
     "event": "user.badge_earned",
     "user_id": "user_12345",
     "platform": "DominionMarkets",
     "badge_id": "portfolio_builder",
     "badge_name": "Portfolio Builder",
     "earned_at": "2025-12-24T12:00:00Z"
   }
   ```

2. **user.challenge_completed** (DominionYouth → DominionMarkets)
   ```json
   {
     "event": "user.challenge_completed",
     "user_id": "user_12345",
     "platform": "DominionYouth",
     "challenge_id": "7_day_finance_streak",
     "challenge_name": "7-Day Finance Streak",
     "reward": "1_month_premium_free",
     "completed_at": "2025-12-24T15:30:00Z"
   }
   ```

3. **user.course_enrolled** (IslandNation → DominionMarkets)
   ```json
   {
     "event": "user.course_enrolled",
     "user_id": "user_12345",
     "platform": "IslandNation",
     "course_id": "stock_analysis_101",
     "course_name": "Stock Analysis for Beginners",
     "creator_id": "creator_456",
     "price": 29.99,
     "referral_source": "DominionMarkets_learn_tab",
     "enrolled_at": "2025-12-24T16:45:00Z"
   }
   ```

---

### Consolidated Dashboard

**Unified View Across All Platforms:**

```
┌─────────────────────────────────────────────────────────────────┐
│ CODEXDOMINION — ECOSYSTEM DASHBOARD                             │
│                                                                 │
│ ┌─────────────────────────┐  ┌────────────────────────────────┐│
│ │ DOMINIONMARKETS         │  │ ISLANDNATION                   ││
│ │                         │  │                                ││
│ │ Portfolio Value:        │  │ Courses Created: 3             ││
│ │ $125,450                │  │ Total Revenue: $4,230          ││
│ │                         │  │ Students: 142                  ││
│ │ Watchlist: 12 stocks    │  │                                ││
│ │ Alerts: 5 active        │  │ [View Creator Dashboard →]     ││
│ │                         │  │                                ││
│ │ [View Dashboard →]      │  │                                ││
│ └─────────────────────────┘  └────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ DOMINIONYOUTH                                               ││
│ │                                                             ││
│ │ Challenges Completed: 7/12                                  ││
│ │ Badges Earned: 5 (🎓📈💼🔥🇯🇲)                              ││
│ │ Leaderboard Rank: #87                                       ││
│ │                                                             ││
│ │ [View Youth Dashboard →]                                   ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ RECENT ACTIVITY (All Platforms)                             ││
│ │                                                             ││
│ │ • 2 hours ago: Completed "Build Mock Portfolio" (Youth)    ││
│ │ • 5 hours ago: Added AAPL to watchlist (Markets)           ││
│ │ • Yesterday: Enrolled in "Diversification 101" (Island)    ││
│ │ • 2 days ago: Earned "Finance Streak" badge (Youth)        ││
│ │                                                             ││
│ │ [View All Activity →]                                      ││
│ └─────────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Access:** dominionecosystem.app (unified dashboard)

---

## 📊 CROSS-PROMOTION METRICS & TARGETS

### Key Performance Indicators (KPIs)

1. **Cross-Platform Usage Rate**
   - **Target:** 30% of users active on 2+ sub-brands
   - **Measure:** (Users on 2+ platforms / Total users) × 100
   - **Benchmark:** Industry average is 10-15%, we target 30%

2. **Course Enrollment from DominionMarkets**
   - **Target:** 500 course enrollments from DominionMarkets referrals (Year 1)
   - **Measure:** Track `referral_source: DominionMarkets_learn_tab`
   - **Revenue Impact:** 500 enrollments × $29 avg = $14,500 revenue

3. **Youth → Markets Conversion**
   - **Target:** 20% of DominionYouth users try DominionMarkets
   - **Measure:** (Youth users who signed up for Markets / Total Youth users) × 100
   - **Funnel:** Challenge reward → 1 month Premium free → Paid conversion

4. **Ecosystem Premium Adoption**
   - **Target:** 15% of Premium users upgrade to Ecosystem Bundle
   - **Measure:** (Ecosystem Premium subscriptions / DominionMarkets Premium) × 100
   - **Revenue Impact:** $14.99/mo vs. $9.99/mo = +$5/mo per user

5. **Creator Recruitment from Markets**
   - **Target:** 50 DominionMarkets users become IslandNation creators (Year 1)
   - **Measure:** Track signup source: `DominionMarkets_creator_banner`
   - **Impact:** 50 creators × 3 courses avg × $29 avg × 20 students = $87,000 revenue

6. **Badge Cross-Platform Syncing**
   - **Target:** 80% of badges earned sync across platforms within 5 minutes
   - **Measure:** Event API latency + success rate
   - **Technical KPI:** < 5 min sync time, > 95% success rate

---

## 💰 REVENUE SYNERGY PROJECTIONS

### Year 1 Cross-Promotion Revenue Impact

**Direct Revenue (Tracked):**
- Course enrollments from Markets: $14,500
- Ecosystem Premium upgrades: $22,500 (150 users × $5/mo × 30 months)
- Creator recruitment: $87,000 (50 creators × $1,740 avg revenue)

**Total Direct Impact:** $124,000

**Indirect Revenue (Estimated):**
- Youth → Markets conversions: $45,000 (500 youth × $9.99/mo × 9 months)
- Longer LTV from cross-platform users: $60,000 (lower churn = 3+ months extra)
- Brand loyalty premium: $30,000 (cross-platform users upgrade at 2x rate)

**Total Indirect Impact:** $135,000

**Total Year 1 Cross-Promotion Revenue:** $259,000

---

### Year 3 Cross-Promotion Revenue Impact

**Projections (Conservative):**
- 10,000 cross-platform users (30% of 33,000 total)
- Ecosystem Premium: 1,500 users × $14.99/mo = $269,820/year
- Course enrollments: 5,000/year × $29 avg = $145,000/year
- Creator ecosystem: 200 creators × $8,700 avg = $1,740,000/year

**Total Year 3 Cross-Promotion Revenue:** $2.15M (35% of total revenue)

---

## ✅ CROSS-PROMOTION ENGINE CHECKLIST

- [x] Ecosystem architecture defined (SSO, shared design, AI engine, data infrastructure)
- [x] CodexDominion → DominionMarkets pathways (creator courses, youth challenges, diaspora synergy)
- [x] DominionMarkets → CodexDominion pathways (creator recruitment, youth onboarding, premium bundles)
- [x] Event APIs documented (badge_earned, challenge_completed, course_enrolled)
- [x] Consolidated dashboard designed (unified view across 3 platforms)
- [x] Cross-promotion metrics defined (6 KPIs)
- [x] Revenue synergy projections calculated (Year 1: $259K, Year 3: $2.15M)
- [x] Ecosystem Premium bundle designed ($14.99/mo for all 3 platforms)
- [x] Integration touchpoints mapped (10+ cross-promotion features)

---

**Status:** CROSS-PROMOTION ENGINE COMPLETE ✅  
**Target:** 30% cross-platform usage, $259K Year 1 revenue impact  
**Launch Target:** Q2 2025 (Phase 3 — Ecosystem Integration)
