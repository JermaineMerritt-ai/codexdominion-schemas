# DominionMarkets Pro Theme Specification

## 🎯 Overview

**Purpose:** Professional investment platform for long-term, income-focused investors

**Design Philosophy:**
- **Conservative:** Trustworthy, stable, professional aesthetic
- **Data-Rich:** Dense information displays with long-term historical context
- **Income-Focused:** Dividend tracking, yield analysis, passive income optimization
- **Patient:** Design for buy-and-hold investors, not day traders

**Target Audience:**
- Long-term investors (5-20 year horizons)
- Dividend income seekers
- Retirement portfolio managers
- Institutional investors
- Conservative wealth builders

---

## 🎨 COLOR SYSTEM

### Primary Colors

**Navy Blue (#001F3F)**
- **Use:** Headers, navigation, primary backgrounds, professional sections
- **RGB:** 0, 31, 63
- **HSL:** 210°, 100%, 12%
- **Accessible on:** White text (AAA), Emerald text (AAA)
- **Gradient variant:** `linear-gradient(135deg, #001F3F 0%, #003366 100%)`

**Navy Gradient (Professional Headers)**
- **Use:** Dashboard headers, institutional sections, data-heavy displays
- **Gradient:** Linear, top to bottom
- **Start:** `#001F3F` (Navy Blue)
- **End:** `#004080` (Deep Blue)
- **CSS:** `background: linear-gradient(180deg, #001F3F 0%, #004080 100%);`

**Emerald Green (#10B981)**
- **Use:** Dividend income, yield growth, passive income indicators, success states
- **RGB:** 16, 185, 129
- **HSL:** 158°, 84%, 39%
- **Accessible on:** White text (AAA), Dark backgrounds (AAA)
- **Gradient variant:** `linear-gradient(135deg, #10B981 0%, #059669 100%)`

**Dividend Gold (#D4AF37)** (Secondary)
- **Use:** Premium dividend stocks, aristocrat badges, high-yield highlights
- **RGB:** 212, 175, 55
- **HSL:** 46°, 65%, 52%
- **Accessible on:** Dark text (AAA), Navy backgrounds (AAA)

**Wealth Blue (#4A90E2)** (Tertiary)
- **Use:** Growth stocks, portfolio value, informational elements
- **RGB:** 74, 144, 226
- **HSL:** 212°, 73%, 59%
- **Accessible on:** White text (AAA)

### Semantic Colors

**Success (Dividend Paid):** `#10B981` (Emerald Green)
**Warning (Dividend Cut):** `#F59E0B` (Amber)
**Error (Dividend Suspended):** `#EF4444` (Red)
**Info:** `#4A90E2` (Wealth Blue)
**Yield:** `#10B981` (Emerald with percentage display)

### Backgrounds

**Primary Background:** `#F9FAFB` (Very Light Gray)
**Secondary Background:** `#FFFFFF` (White)
**Card Background:** `#FFFFFF` with subtle shadow
**Dark Mode Background:** `#0F1419` (Charcoal)
**Data Grid Background:** `#F3F4F6` (Light Gray, zebra striping)

### Neutrals

**Dark Text:** `#111827` (Near Black)
**Medium Text:** `#6B7280` (Gray)
**Light Text:** `#9CA3AF` (Light Gray)
**Divider:** `#E5E7EB` (Very Light Gray)
**Border:** `#D1D5DB` (Light Gray Border)

---

## ✍️ TYPOGRAPHY

**Primary Font:** Inter (same as DominionMarkets)
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

**Display Font:** Lora (for institutional headings, report titles)
```css
font-family: 'Lora', Georgia, serif;
```

**Monospace Font:** Roboto Mono (dividend amounts, yield percentages, precise numbers)
```css
font-family: 'Roboto Mono', 'Courier New', monospace;
```

### Type Scale (Pro Investor Variant)

| Token | Size | Weight | Line Height | Use Case |
|-------|------|--------|-------------|----------|
| `text-xs` | 11px | 400 | 1.4 | Dense table data, footnotes |
| `text-sm` | 13px | 400 | 1.5 | Body text in tables |
| `text-base` | 15px | 400 | 1.6 | Standard body text |
| `text-lg` | 17px | 500 | 1.5 | Section headings |
| `text-xl` | 19px | 600 | 1.4 | Card titles |
| `text-2xl` | 22px | 700 | 1.3 | Page titles |
| `text-3xl` | 28px | 700 | 1.2 | Dashboard headings |
| `text-4xl` | 36px | 700 | 1.1 | Portfolio value, total yield |
| `text-display` | 42px | 700 | 1.0 | Landing page hero (Lora) |

**Note:** Smaller base font (15px) allows more data density for institutional investors

---

## 🧩 COMPONENT LIBRARY

### 1. Dividend Tracker Widget

**Purpose:** Comprehensive dividend income tracking with historical analysis

**Visual Design:**
```
┌─────────────────────────────────────────────────────────────────┐
│ 💰 DIVIDEND INCOME TRACKER                        Annual View   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ANNUAL INCOME:                                                 │
│  2025: $12,485.75  (+18.5% YoY)  [Projected: $14,200.00]       │
│  2024: $10,542.30  (+12.3% YoY)                                 │
│  2023: $9,392.10   (+8.7% YoY)                                  │
│                                                                 │
│  [12-MONTH CHART: Monthly dividend income with trend line]      │
│                                                                 │
│  PAYMENT CALENDAR:                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Dec 28 | JNJ   | $65.50  | Quarterly | ✅ Confirmed     │  │
│  │ Jan 5  | KO    | $48.25  | Quarterly | 🔔 Upcoming      │  │
│  │ Jan 12 | PG    | $72.80  | Quarterly | 🔔 Upcoming      │  │
│  │ Jan 15 | VZ    | $51.30  | Quarterly | 🔔 Upcoming      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  TOP DIVIDEND PAYERS:                                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. JNJ  | $262.00/year | 21.0% of total | 2.85% yield   │  │
│  │ 2. PG   | $291.20/year | 23.3% of total | 2.61% yield   │  │
│  │ 3. VZ   | $205.20/year | 16.4% of total | 6.12% yield   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  METRICS:                                                       │
│  • Portfolio Yield: 3.45% (vs S&P 500: 1.52%)                  │
│  • Dividend Growth Rate (5Y): 8.2% CAGR                        │
│  • Payout Ratio: 58% (Healthy)                                 │
│  • Dividend Aristocrats: 5 holdings 👑                         │
│  • Consecutive Years Paid: Avg 18 years                        │
│                                                                 │
│  [Export Report] [Set Alerts] [View All Holdings]              │
└─────────────────────────────────────────────────────────────────┘
```

**Specs:**
- **Width:** 100% (responsive)
- **Height:** Auto (min 600px)
- **Background:** White (#FFFFFF)
- **Border:** 1px solid #E5E7EB
- **Border radius:** 8px (less rounded, more professional)
- **Padding:** 24px
- **Header background:** Navy gradient
- **Dividend amounts:** Roboto Mono, Emerald Green (#10B981)
- **Confirmed payments:** Green checkmark ✅
- **Upcoming payments:** Bell icon 🔔
- **Chart:** 12-month bar chart with trend line overlay

**Figma Component:**
```typescript
interface DividendTracker {
  annualIncome: {
    year: number;                      // 2025
    total: number;                     // 12485.75
    yoyGrowth: number;                 // +18.5
    projected: number;                 // 14200.00 (based on current holdings)
  }[];
  
  paymentCalendar: DividendPayment[];
  
  topPayers: {
    symbol: string;                    // 'JNJ'
    annualAmount: number;              // 262.00
    percentOfTotal: number;            // 21.0
    yieldPercent: number;              // 2.85
  }[];
  
  metrics: {
    portfolioYield: number;            // 3.45
    spYield: number;                   // 1.52 (benchmark)
    dividendGrowthRate5Y: number;      // 8.2
    avgPayoutRatio: number;            // 58
    aristocratCount: number;           // 5 (stocks with 25+ years consecutive increases)
    avgConsecutiveYears: number;       // 18
  };
  
  chartData: {
    month: string;                     // 'Jan 2025'
    income: number;                    // 1042.50
  }[];
}

interface DividendPayment {
  date: string;                        // '2025-12-28'
  symbol: string;                      // 'JNJ'
  amount: number;                      // 65.50
  frequency: 'Monthly' | 'Quarterly' | 'Semi-Annual' | 'Annual';
  status: 'confirmed' | 'upcoming' | 'estimated';
  exDividendDate?: string;             // '2025-12-05'
  paymentDate?: string;                // '2025-12-28'
}
```

**Interactions:**
- **Hover on payment:** Show ex-dividend date, record date, payment date
- **Click payment:** Open dividend detail modal (history, payout ratio, sustainability score)
- **"Export Report" button:** Generate PDF with full dividend history (5-10 years)
- **"Set Alerts" button:** Configure notifications (ex-dividend dates, payment confirmations, dividend cuts)
- **"View All Holdings" button:** Navigate to full dividend portfolio view
- **Chart hover:** Show exact monthly income + cumulative YTD

**Educational Elements:**
- **Dividend Aristocrat badge (👑):** Tooltip explains "25+ years of consecutive dividend increases"
- **Payout Ratio:** Color-coded (Green: <70%, Yellow: 70-80%, Red: >80%)
- **Yield comparison:** Always shows portfolio yield vs S&P 500 benchmark
- **Sustainability score:** Algorithm-based (1-100) assessing dividend safety

---

### 2. Long-Term Charts Widget

**Purpose:** Multi-decade historical charts for patient investors

**Visual Design:**
```
┌─────────────────────────────────────────────────────────────────┐
│ 📊 LONG-TERM PERFORMANCE                           JNJ          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TIME PERIOD: [1Y] [5Y] [10Y] [20Y] [ALL TIME] [CUSTOM]        │
│                                                                 │
│  [CHART: 20-year price history with dividend reinvestment]      │
│  • Price: Blue line                                             │
│  • Total Return (w/ dividends): Emerald line                    │
│  • S&P 500 Benchmark: Dotted gray line                          │
│                                                                 │
│  PERFORMANCE SUMMARY:                                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Period        │ Price Return │ Total Return │ S&P 500   │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ 1 Year        │ +8.2%        │ +10.8%       │ +12.5%    │  │
│  │ 5 Year        │ +42.5%       │ +58.3%       │ +68.2%    │  │
│  │ 10 Year       │ +158.7%      │ +225.4%      │ +198.6%   │  │
│  │ 20 Year       │ +385.2%      │ +652.8%      │ +420.3%   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ANNUALIZED RETURNS (CAGR):                                     │
│  • 10-Year: 12.5% (w/ dividends) vs 11.4% (price only)         │
│  • 20-Year: 10.8% (w/ dividends) vs 8.2% (price only)          │
│                                                                 │
│  DIVIDEND CONTRIBUTION:                                         │
│  • $10,000 invested in 2005 → $65,280 today                    │
│  • Dividends contributed: $22,100 (33.9% of total return)      │
│  • Reinvested dividends bought: 142 additional shares           │
│                                                                 │
│  KEY EVENTS (Overlay on chart):                                 │
│  📍 2008: Financial Crisis (-45% drawdown, recovered by 2010)  │
│  📍 2011: Dividend increased 7.5% (20th consecutive year)      │
│  📍 2020: COVID-19 (-15% drawdown, recovered in 6 months)      │
│                                                                 │
│  [Toggle Dividends] [Compare Stocks] [Download Data]           │
└─────────────────────────────────────────────────────────────────┘
```

**Specs:**
- **Width:** 100% (responsive)
- **Height:** 600px (chart area 500px)
- **Background:** White (#FFFFFF)
- **Border:** 1px solid #E5E7EB
- **Border radius:** 8px
- **Chart type:** Line chart with area fill
- **Price line:** Navy Blue (#001F3F)
- **Total return line:** Emerald Green (#10B981), 2px thickness
- **Benchmark line:** Dotted gray (#9CA3AF)
- **Time period buttons:** Navy background when active
- **Event markers:** Gold pins 📍 on chart

**Figma Component:**
```typescript
interface LongTermChart {
  symbol: string;                      // 'JNJ'
  timePeriod: '1Y' | '5Y' | '10Y' | '20Y' | 'ALL' | 'CUSTOM';
  
  chartData: {
    date: string;                      // '2005-01-01'
    price: number;                     // 64.50
    totalReturn: number;               // 64.50 (initial), grows with dividends
    spReturn: number;                  // S&P 500 benchmark
  }[];
  
  performanceSummary: {
    period: string;                    // '10 Year'
    priceReturn: number;               // +158.7
    totalReturn: number;               // +225.4
    spReturn: number;                  // +198.6
  }[];
  
  annualizedReturns: {
    period: string;                    // '10-Year'
    cagrWithDividends: number;         // 12.5
    cagrPriceOnly: number;             // 11.4
  }[];
  
  dividendContribution: {
    initialInvestment: number;         // 10000
    currentValue: number;              // 65280
    dividendsContributed: number;      // 22100
    percentOfReturn: number;           // 33.9
    additionalShares: number;          // 142
  };
  
  keyEvents: {
    date: string;                      // '2008-09-15'
    title: string;                     // 'Financial Crisis'
    description: string;               // '-45% drawdown, recovered by 2010'
    impact: 'positive' | 'negative' | 'neutral';
  }[];
}
```

**Interactions:**
- **Time period buttons:** Switch chart timeframe (1Y, 5Y, 10Y, 20Y, All Time, Custom date range)
- **"Toggle Dividends" button:** Show/hide total return line (with dividend reinvestment)
- **"Compare Stocks" button:** Overlay up to 3 additional stocks for comparison
- **"Download Data" button:** Export CSV with daily/monthly price + dividend data
- **Chart hover:** Crosshair shows exact values for all lines at that date
- **Event marker click:** Show detailed explanation of event + impact analysis
- **Zoom controls:** Mouse wheel zoom, drag to pan (for detailed analysis)

**Chart Features:**
- **Logarithmic scale option:** Better visualize long-term growth
- **Inflation adjustment:** Toggle real vs nominal returns
- **Dividend reinvestment simulation:** Assumes automatic reinvestment at ex-dividend price
- **Drawdown overlay:** Shade negative periods (bear markets, corrections)
- **Recovery time annotations:** "Recovered to previous high in 8 months"

**Educational Context:**
- **CAGR explanation:** Tooltip explains "Compound Annual Growth Rate"
- **Total return vs price return:** Side-by-side comparison highlights dividend power
- **Time in market:** "Holding for 20+ years smooths volatility, increases odds of positive returns"
- **Dollar-cost averaging simulator:** Show impact of regular monthly investments

---

### 3. Dividend Aristocrat Badge

**Purpose:** Highlight elite dividend-paying stocks

**Visual Design:**
```
┌────────────────────────┐
│  👑 DIVIDEND ARISTOCRAT│
│                        │
│  25+ Years             │
│  Consecutive Increases │
└────────────────────────┘
```

**Specs:**
- **Width:** 200px
- **Height:** 80px
- **Background:** Dividend Gold (#D4AF37) gradient
- **Border:** 2px solid darker gold
- **Border radius:** 6px
- **Icon:** 👑 (48px)
- **Text color:** Navy Blue (#001F3F)

**Variants:**
- **Dividend Aristocrat:** 25+ years (Gold)
- **Dividend King:** 50+ years (Platinum/Silver)
- **Dividend Contender:** 10-24 years (Bronze)

---

### 4. Yield Comparison Table

**Purpose:** Compare dividend yields across holdings

**Visual Design:**
```
┌─────────────────────────────────────────────────────────────────┐
│ DIVIDEND YIELD ANALYSIS                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Symbol │ Yield │ 5Y Avg │ Payout Ratio │ Growth (5Y) │ Safety│
│  ───────┼───────┼────────┼──────────────┼─────────────┼───────│
│  VZ     │ 6.12% │ 5.85%  │ 52%          │ +3.2%       │ 85/100│
│  T      │ 5.87% │ 6.12%  │ 58%          │ +1.1%       │ 72/100│
│  PG     │ 2.61% │ 2.48%  │ 65%          │ +5.5%       │ 92/100│
│  JNJ    │ 2.85% │ 2.72%  │ 48%          │ +6.2%       │ 95/100│
│  KO     │ 3.15% │ 3.05%  │ 72%          │ +4.1%       │ 88/100│
│                                                                 │
│  Portfolio Avg: 4.12%  |  S&P 500: 1.52%  |  Spread: +2.60%   │
└─────────────────────────────────────────────────────────────────┘
```

**Specs:**
- **Row height:** 48px
- **Header background:** Navy (#001F3F)
- **Zebra striping:** Alternating white and light gray
- **Yield color:** Emerald Green if >3%, standard if 1-3%, amber if <1%
- **Safety score:** Color-coded (Green: 80-100, Yellow: 60-79, Red: <60)

---

### 5. Portfolio Income Projection

**Purpose:** Forecast future dividend income based on holdings

**Visual Design:**
```
┌─────────────────────────────────────────────────────────────────┐
│ 💰 INCOME PROJECTION                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Current Annual Income: $12,485.75                              │
│                                                                 │
│  PROJECTIONS (Conservative 5% growth):                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Year  │ Projected Income │ Monthly Avg │ % of Goal      │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ 2026  │ $13,110.04       │ $1,092.50   │ 26.2% of $50K │  │
│  │ 2027  │ $13,765.54       │ $1,147.13   │ 27.5% of $50K │  │
│  │ 2028  │ $14,453.82       │ $1,204.49   │ 28.9% of $50K │  │
│  │ 2029  │ $15,176.51       │ $1,264.71   │ 30.4% of $50K │  │
│  │ 2030  │ $15,935.34       │ $1,327.94   │ 31.9% of $50K │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  [CHART: Projected income growth line with shaded confidence]   │
│                                                                 │
│  TO REACH $50,000/YEAR GOAL:                                    │
│  • Need: $37,514.25 more annual income                          │
│  • At current yield (3.45%): Invest $1,087,341 more             │
│  • With $2,000/month contributions: 28.5 years                  │
│  • Accelerate with $5,000/month: 10.2 years                     │
│                                                                 │
│  ASSUMPTIONS:                                                   │
│  • Average dividend growth: 5% annually (historical: 8.2%)     │
│  • New investments: $2,000/month at 3.45% yield                │
│  • Dividends reinvested automatically                           │
│  • No principal withdrawals                                     │
│                                                                 │
│  [Adjust Assumptions] [Set Income Goal] [Plan Contributions]   │
└─────────────────────────────────────────────────────────────────┘
```

**Specs:**
- **Width:** 100%
- **Padding:** 24px
- **Background:** White with Emerald accent border
- **Projection chart:** 5-10 year line chart with confidence bands
- **Goal progress:** Progress bar showing % of income goal achieved

---

### 6. Ex-Dividend Calendar

**Purpose:** Track upcoming ex-dividend dates to optimize purchases

**Visual Design:**
```
┌─────────────────────────────────────────────────────────────────┐
│ 📅 EX-DIVIDEND CALENDAR                            This Month   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  WHY IT MATTERS: Buy before ex-dividend date to receive payment │
│                                                                 │
│  DECEMBER 2025:                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Dec 26 │ KO    │ Ex-Div Date    │ $0.485/share | 3.15%  │  │
│  │        │       │ Record: Dec 27 │ Pay: Jan 5   | 🔔     │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ Dec 27 │ JNJ   │ Ex-Div Date    │ $1.19/share  | 2.85%  │  │
│  │        │       │ Record: Dec 28 │ Pay: Jan 8   | 🔔     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  JANUARY 2026:                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Jan 2  │ PG    │ Ex-Div Date    │ $0.912/share | 2.61%  │  │
│  │ Jan 8  │ VZ    │ Ex-Div Date    │ $0.665/share | 6.12%  │  │
│  │ Jan 15 │ T     │ Ex-Div Date    │ $0.555/share | 5.87%  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  [Add to Google Calendar] [Set Reminders] [Export iCal]        │
└─────────────────────────────────────────────────────────────────┘
```

**Specs:**
- **Row height:** 72px (2 rows per stock: ex-div info + record/pay dates)
- **Upcoming dates:** Bell icon 🔔 for dates within 7 days
- **Past dates:** Grayed out
- **Calendar integration:** One-click export to Google Calendar, iCal

---

## 🎭 MICRO-INTERACTIONS

### Dividend Payment Animation
```
Animation: Cash register "cha-ching" + number count-up
Duration: 800ms
Trigger: Dividend confirmed
Effect: Amount animates from 0 → final value
Sound: Optional "cha-ching" sound effect
```

### Yield Tooltip Hover
```
Animation: Fade in with slight scale
Duration: 200ms
Content: Current yield + 5Y average + payout ratio
```

### Long-Term Chart Zoom
```
Animation: Smooth scale transition
Duration: 300ms
Easing: ease-in-out
Controls: Mouse wheel or pinch gesture
```

### Aristocrat Badge Shine
```
Animation: Subtle gold shimmer across badge
Duration: 2s
Loop: Every 10 seconds
Effect: Light sweep from left to right
```

### Income Projection Update
```
Animation: Progress bar fill
Duration: 1s
Trigger: User adjusts assumptions
Effect: Bars animate from old → new projected values
```

---

## ♿ ACCESSIBILITY

**WCAG 2.1 AAA Compliance:**
- Navy Blue (#001F3F) with white text: 16:1 (AAA)
- Emerald Green (#10B981) on white: 4.5:1 (AA for large text)
- All data tables have proper headers and aria-labels

**Investor-Specific Considerations:**
- Logarithmic scale option for vision-impaired users
- Screen reader announces dividend payment confirmations
- Keyboard shortcuts for chart navigation (arrow keys, +/- zoom)
- High contrast mode for all charts

---

## 📱 RESPONSIVE DESIGN

**Mobile (≤767px):**
- Dividend tracker: Simplified to current month + top 3 payers
- Long-term charts: Touch-friendly zoom, 1-column layout
- Yield table: Horizontal scroll with sticky first column

**Tablet (768-1023px):**
- 2-column dashboard layout
- Full dividend calendar visible
- Charts maintain full functionality

**Desktop (≥1024px):**
- 3-column dashboard layout
- Side-by-side chart comparisons
- Dense data tables with sorting

---

## 🎨 DASHBOARD LAYOUTS

### Pro Dashboard Home (Dividend-Focused)

**Sections:**
1. **Hero Header** - Navy gradient, "Passive Income: $12,485.75/year"
2. **Dividend Tracker** - Full width, primary widget
3. **Payment Calendar** - Left column (40%)
4. **Income Projection** - Right column (60%)
5. **Long-Term Charts** - Full width, featured stock performance
6. **Yield Comparison Table** - Full width, sortable data
7. **Aristocrat Holdings** - Badge showcase section

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ Navy Header (Gradient) - Passive Income Display         │
├─────────────────────────────────────────────────────────┤
│ Dividend Tracker (Full Width)                           │
├──────────────────────────┬──────────────────────────────┤
│ Payment Calendar         │ Income Projection            │
│ (Left 40%)               │ (Right 60%)                  │
├──────────────────────────┴──────────────────────────────┤
│ Long-Term Charts (Full Width)                           │
├─────────────────────────────────────────────────────────┤
│ Yield Comparison Table (Full Width)                     │
├─────────────────────────────────────────────────────────┤
│ Aristocrat Holdings (Badge Grid)                        │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 IMPLEMENTATION NOTES

**Tailwind Config Overrides (Pro theme):**
```javascript
// tailwind.config.pro.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'navy': '#001F3F',
        'navy-medium': '#003366',
        'navy-light': '#004080',
        'emerald-dividend': '#10B981',
        'gold-dividend': '#D4AF37',
        'wealth-blue': '#4A90E2',
      },
      fontFamily: {
        'display': ['Lora', 'Georgia', 'serif'],
      },
      fontSize: {
        'xs': '11px',  // Denser for tables
        'base': '15px', // Slightly smaller for data-heavy views
      },
    },
  },
};
```

**Component Naming Convention:**
- Prefix all Pro components with `Pro-`
- Example: `<ProDividendTracker />`, `<ProLongTermChart />`, `<ProYieldTable />`

**Data Sources:**
- **Alpha Vantage API:** Real-time stock prices, historical data (20+ years)
- **Dividend.com API:** Ex-dividend dates, payment schedules
- **SEC EDGAR:** Payout ratios, financial statements
- **Internal calculations:** Dividend growth rates, sustainability scores

**Historical Data Storage:**
- Store 50+ years of price data (if available)
- Store dividend history back to IPO
- Compress older data (monthly instead of daily for 10+ years ago)
- S3 or similar for long-term cold storage

**Performance Optimization:**
- Chart data: Load on-demand, cache 5-10 years
- Tables: Virtual scrolling for large datasets
- Lazy load aristocrat badges (only render visible)

---

**Last Updated:** December 24, 2025
**Status:** Specification complete, ready for design + development
**Owner:** DominionMarkets Pro Product Team
