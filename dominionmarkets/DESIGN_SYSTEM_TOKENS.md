# DominionMarkets - Design System Tokens

**Last Updated:** December 24, 2025  
**Status:** Production Ready - Buildable Specification  
**Version:** 2.0 (Complete System)

---

## 🎯 Overview

This document defines the complete visual language of DominionMarkets. All tokens are aligned with CodexDominion's Council Seal architecture but tuned specifically for financial data environments.

**Token Architecture:**
- Base tokens (universal across all identities)
- Identity-specific theme overrides (Diaspora, Youth, Creator, Legacy-Builder)
- Component-specific tokens (charts, badges, cards)
- Responsive breakpoints and adaptive tokens

---

## 🎨 COLOR TOKENS

### Primary Palette

**Caribbean Blue** (`caribbean-blue`)
- **Value:** `#003049`
- **RGB:** 0, 48, 73
- **HSL:** 198°, 100%, 14%
- **Use Cases:** Headers, navigation, chart baselines, brand identity
- **Accessibility:** AAA with white text (15:1 contrast)
- **CSS Variable:** `--color-caribbean-blue`

**Market Green** (`market-green`)
- **Value:** `#00A896`
- **RGB:** 0, 168, 150
- **HSL:** 174°, 100%, 33%
- **Use Cases:** Positive price movement, gains, confirmations, success states
- **Accessibility:** AA with white text (4.5:1), AAA with dark backgrounds
- **CSS Variable:** `--color-market-green`

**Coral Red** (`coral-red`)
- **Value:** `#FF6B6B`
- **RGB:** 255, 107, 107
- **HSL:** 0°, 100%, 71%
- **Use Cases:** Negative price movement, losses, warnings, alerts
- **Accessibility:** AA with white text (4.5:1), AA with dark text
- **CSS Variable:** `--color-coral-red`

**Sovereign Gold** (`sovereign-gold`)
- **Value:** `#F2C94C`
- **RGB:** 242, 201, 76
- **HSL:** 45°, 86%, 62%
- **Use Cases:** Premium highlights, accents, featured content, badges
- **Accessibility:** AAA with dark text (8:1)
- **CSS Variable:** `--color-sovereign-gold`

### Neutral Palette

**White** (`neutral-white`)
- **Value:** `#FFFFFF`
- **Use:** Card backgrounds, clean surfaces
- **CSS Variable:** `--color-neutral-white`

**Light Gray** (`neutral-light`)
- **Value:** `#E0E0E0`
- **Use:** Borders, dividers, subtle backgrounds
- **CSS Variable:** `--color-neutral-light`

**Medium Gray** (`neutral-medium`)
- **Value:** `#BDBDBD`
- **Use:** Secondary borders, disabled states
- **CSS Variable:** `--color-neutral-medium`

**Dark Gray** (`neutral-dark`)
- **Value:** `#4F4F4F`
- **Use:** Body text, secondary information
- **CSS Variable:** `--color-neutral-dark`

**Black** (`neutral-black`)
- **Value:** `#000000`
- **Use:** High contrast text, overlays
- **CSS Variable:** `--color-neutral-black`

### Semantic Colors

**Success** (`semantic-success`)
- **Value:** `#00A896` (Market Green)
- **Use:** Successful operations, confirmations
- **CSS Variable:** `--color-semantic-success`

**Warning** (`semantic-warning`)
- **Value:** `#F2C94C` (Sovereign Gold)
- **Use:** Cautions, developing stories
- **CSS Variable:** `--color-semantic-warning`

**Error** (`semantic-error`)
- **Value:** `#FF6B6B` (Coral Red)
- **Use:** Errors, critical alerts, dividend cuts
- **CSS Variable:** `--color-semantic-error`

**Info** (`semantic-info`)
- **Value:** `#003049` (Caribbean Blue)
- **Use:** Informational messages, neutral data
- **CSS Variable:** `--color-semantic-info`

---

## ✍️ TYPOGRAPHY TOKENS

### Font Family

**Primary Font** (`font-primary`)
- **Value:** `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- **Use:** Body text, UI elements, data displays
- **Weights Available:** 400, 500, 600, 700
- **CSS Variable:** `--font-family-primary`

**Monospace Font** (`font-mono`)
- **Value:** `'Roboto Mono', 'Courier New', monospace`
- **Use:** Numbers, prices, percentages, code
- **CSS Variable:** `--font-family-mono`

### Font Sizes

| Token | Value | Use Case | Line Height | CSS Variable |
|-------|-------|----------|-------------|--------------|
| `text-hero` | 48px | Landing page heroes | 1.1 | `--font-size-hero` |
| `text-display` | 32px | Dashboard headers | 1.2 | `--font-size-display` |
| `text-h1` | 24px | Page titles | 1.3 | `--font-size-h1` |
| `text-h2` | 20px | Section headings | 1.4 | `--font-size-h2` |
| `text-base` | 16px | Body text | 1.5 | `--font-size-base` |
| `text-sm` | 14px | Labels, captions | 1.5 | `--font-size-sm` |
| `text-xs` | 12px | Metadata, timestamps | 1.4 | `--font-size-xs` |

### Font Weights

| Token | Value | Use Case | CSS Variable |
|-------|-------|----------|--------------|
| `weight-bold` | 700 | Headers, emphasis | `--font-weight-bold` |
| `weight-semibold` | 600 | Subheadings, buttons | `--font-weight-semibold` |
| `weight-medium` | 500 | Highlights, labels | `--font-weight-medium` |
| `weight-regular` | 400 | Body text | `--font-weight-regular` |

---

## 📏 SPACING TOKENS (8pt Grid System)

All spacing follows an 8-point grid system for visual consistency.

| Token | Value | Use Case | CSS Variable |
|-------|-------|----------|--------------|
| `space-xs` | 4px | Tight padding, icon gaps | `--space-xs` |
| `space-sm` | 8px | Small padding, element spacing | `--space-sm` |
| `space-md` | 12px | Medium padding | `--space-md` |
| `space-base` | 16px | Standard padding, card spacing | `--space-base` |
| `space-lg` | 24px | Large padding, section spacing | `--space-lg` |
| `space-xl` | 32px | Extra large spacing | `--space-xl` |
| `space-2xl` | 40px | Dashboard sections | `--space-2xl` |
| `space-3xl` | 48px | Major sections | `--space-3xl` |
| `space-4xl` | 64px | Hero sections | `--space-4xl` |

**Usage Examples:**
```css
/* Card padding */
padding: var(--space-base); /* 16px */

/* Section spacing */
margin-bottom: var(--space-lg); /* 24px */

/* Dashboard sections */
gap: var(--space-2xl); /* 32px */
```

---

## 🔲 RADIUS TOKENS

| Token | Value | Use Case | CSS Variable |
|-------|-------|----------|--------------|
| `radius-sm` | 4px | Badges, small buttons | `--radius-sm` |
| `radius-base` | 8px | Cards, inputs, buttons | `--radius-base` |
| `radius-lg` | 12px | Large cards, modals | `--radius-lg` |
| `radius-xl` | 20px | Feature cards, hero sections | `--radius-xl` |

---

## 🌑 SHADOW TOKENS

| Token | Value | Use Case | CSS Variable |
|-------|-------|----------|--------------|
| `shadow-sm` | `0 2px 8px rgba(0,0,0,0.08)` | Buttons, small cards | `--shadow-sm` |
| `shadow-base` | `0 4px 16px rgba(0,0,0,0.10)` | Cards, dropdowns | `--shadow-base` |
| `shadow-lg` | `0 8px 24px rgba(0,0,0,0.12)` | Modals, overlays | `--shadow-lg` |

**Hover States:**
- Add shadow on hover for lift effect
- Increase shadow size by 1 level (sm → base, base → lg)

---

## 🔳 BORDER TOKENS

### Border Widths

| Token | Value | Use Case | CSS Variable |
|-------|-------|----------|--------------|
| `border-thin` | 1px | Default borders, dividers | `--border-thin` |
| `border-medium` | 2px | Emphasized borders, active states | `--border-medium` |
| `border-thick` | 3px | Premium indicators, focus states | `--border-thick` |

### Border Colors

| Token | Value | Use Case | CSS Variable |
|-------|-------|----------|--------------|
| `border-light` | `#E0E0E0` | Default borders | `--border-light` |
| `border-medium` | `#BDBDBD` | Emphasized borders | `--border-medium` |
| `border-accent` | `#F2C94C` | Premium borders | `--border-accent` |

---

## 📊 CHART TOKENS

### Line Charts

| Token | Value | Use Case | CSS Variable |
|-------|-------|----------|--------------|
| `chart-line-positive` | `#00A896` | Price increases, gains | `--chart-line-positive` |
| `chart-line-negative` | `#FF6B6B` | Price decreases, losses | `--chart-line-negative` |
| `chart-line-neutral` | `#4F4F4F` | Benchmarks, baselines | `--chart-line-neutral` |

**Line Styling:**
- Positive lines: 2px solid
- Negative lines: 2px solid
- Neutral lines: 1px dashed

### Candlestick Charts

| Token | Value | Use Case | CSS Variable |
|-------|-------|----------|--------------|
| `chart-candle-up` | `#00A896` | Bullish candles | `--chart-candle-up` |
| `chart-candle-down` | `#FF6B6B` | Bearish candles | `--chart-candle-down` |

### Heatmaps

| Token | Value | Use Case | CSS Variable |
|-------|-------|----------|--------------|
| `chart-heatmap-cold` | `#003049` | Negative/low values | `--chart-heatmap-cold` |
| `chart-heatmap-neutral` | `#00A896` | Neutral values | `--chart-heatmap-neutral` |
| `chart-heatmap-hot` | `#F2C94C` | Positive/high values | `--chart-heatmap-hot` |

**Gradient Scale:**
```css
background: linear-gradient(90deg, 
  var(--chart-heatmap-cold) 0%, 
  var(--chart-heatmap-neutral) 50%, 
  var(--chart-heatmap-hot) 100%
);
```

---

## 🏷️ BADGE TOKENS

### Verification Badges

**Multi-Source Verified** (`badge-verified`)
- **Background:** `#00A896` (Market Green)
- **Text:** `#FFFFFF`
- **Icon:** ✅
- **Border Radius:** 4px
- **Padding:** 4px 8px
- **Font:** 12px bold
- **CSS Variable:** `--badge-verified-bg`, `--badge-verified-text`

**Developing Story** (`badge-developing`)
- **Background:** `#F2C94C` (Sovereign Gold)
- **Text:** `#003049` (Caribbean Blue)
- **Icon:** ⚠️
- **Border Radius:** 4px
- **Padding:** 4px 8px
- **Font:** 12px bold
- **CSS Variable:** `--badge-developing-bg`, `--badge-developing-text`

**Conflicting Reports** (`badge-conflicting`)
- **Background:** `#FF6B6B` (Coral Red)
- **Text:** `#FFFFFF`
- **Icon:** ❌
- **Border Radius:** 4px
- **Padding:** 4px 8px
- **Font:** 12px bold
- **CSS Variable:** `--badge-conflicting-bg`, `--badge-conflicting-text`

### Premium Badges

**Premium Tier** (`badge-premium`)
- **Background:** Sovereign Gold gradient
- **Text:** `#003049`
- **Icon:** ⭐
- **Border:** 2px solid gold

**Pro Tier** (`badge-pro`)
- **Background:** Caribbean Blue gradient
- **Text:** `#FFFFFF`
- **Icon:** 👑
- **Border:** 2px solid blue

---

## 🎨 IDENTITY-BASED THEME TOKENS

### Diaspora Theme

**Colors:**
```css
--theme-diaspora-header: linear-gradient(180deg, #003049 0%, #005A7D 100%);
--theme-diaspora-accent: #F2C94C;
--theme-diaspora-background: #F5F0E8; /* Warm sand */
```

**Widgets:**
- Diaspora Economic Flow Maps™
- Caribbean-linked companies
- Remittance-influenced sectors
- Cultural Alpha highlights

### Youth Theme

**Colors:**
```css
--theme-youth-header: #00D9C0; /* Neon teal */
--theme-youth-accent: #FF9580; /* Coral */
--theme-youth-background: #F5F5F5; /* Slate gray */
```

**Widgets:**
- Learning badges
- Mock portfolio
- Financial literacy challenges
- Simplified charts

### Creator Theme

**Colors:**
```css
--theme-creator-header: linear-gradient(90deg, #1E293B 0%, #334155 100%);
--theme-creator-accent: #F2C94C; /* Gold */
--theme-creator-background: #FFFFFF;
```

**Widgets:**
- Creator-economy index
- Digital-product stocks
- AI-tool companies
- Market trends

### Legacy-Builder Theme (Pro)

**Colors:**
```css
--theme-legacy-header: linear-gradient(180deg, #001F3F 0%, #004080 100%);
--theme-legacy-accent: #10B981; /* Emerald */
--theme-legacy-background: #F9FAFB; /* Off-white */
```

**Widgets:**
- Dividend trackers
- Long-term charts (20+ years)
- Wealth-preservation insights
- Low-volatility sectors

---

## 📱 RESPONSIVE BREAKPOINTS

| Token | Value | Use Case | CSS Variable |
|-------|-------|----------|--------------|
| `breakpoint-xs` | 0-479px | Mobile portrait | `--breakpoint-xs` |
| `breakpoint-sm` | 480-767px | Mobile landscape | `--breakpoint-sm` |
| `breakpoint-md` | 768-1023px | Tablets | `--breakpoint-md` |
| `breakpoint-lg` | 1024-1439px | Desktop | `--breakpoint-lg` |
| `breakpoint-xl` | 1440px+ | Large desktop | `--breakpoint-xl` |

**Grid System:**
- Mobile: 4-column grid
- Tablet: 8-column grid
- Desktop: 12-column grid

---

## 🎬 ANIMATION TOKENS

### Durations

| Token | Value | Use Case | CSS Variable |
|-------|-------|----------|--------------|
| `duration-instant` | 100ms | Button press, micro-interactions | `--duration-instant` |
| `duration-fast` | 200ms | Hover states, tooltips | `--duration-fast` |
| `duration-base` | 300ms | Standard transitions | `--duration-base` |
| `duration-slow` | 500ms | Modal open, page transitions | `--duration-slow` |

### Easing Functions

| Token | Value | Use Case | CSS Variable |
|-------|-------|----------|--------------|
| `ease-default` | `ease-in-out` | Standard transitions | `--ease-default` |
| `ease-in` | `ease-in` | Elements appearing | `--ease-in` |
| `ease-out` | `ease-out` | Elements disappearing | `--ease-out` |
| `ease-bounce` | `cubic-bezier(0.68, -0.55, 0.265, 1.55)` | Playful interactions | `--ease-bounce` |

---

## 🏗️ IMPLEMENTATION GUIDE

### Tailwind CSS Config

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'caribbean-blue': '#003049',
        'market-green': '#00A896',
        'coral-red': '#FF6B6B',
        'sovereign-gold': '#F2C94C',
        'neutral': {
          white: '#FFFFFF',
          light: '#E0E0E0',
          medium: '#BDBDBD',
          dark: '#4F4F4F',
          black: '#000000',
        },
      },
      fontFamily: {
        primary: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['Roboto Mono', 'Courier New', 'monospace'],
      },
      fontSize: {
        'hero': '48px',
        'display': '32px',
        'h1': '24px',
        'h2': '20px',
        'base': '16px',
        'sm': '14px',
        'xs': '12px',
      },
      spacing: {
        'xs': '4px',
        'sm': '8px',
        'md': '12px',
        'base': '16px',
        'lg': '24px',
        'xl': '32px',
        '2xl': '40px',
        '3xl': '48px',
        '4xl': '64px',
      },
      borderRadius: {
        'sm': '4px',
        'base': '8px',
        'lg': '12px',
        'xl': '20px',
      },
      boxShadow: {
        'sm': '0 2px 8px rgba(0,0,0,0.08)',
        'base': '0 4px 16px rgba(0,0,0,0.10)',
        'lg': '0 8px 24px rgba(0,0,0,0.12)',
      },
    },
  },
};
```

### CSS Custom Properties

```css
:root {
  /* Colors */
  --color-caribbean-blue: #003049;
  --color-market-green: #00A896;
  --color-coral-red: #FF6B6B;
  --color-sovereign-gold: #F2C94C;
  
  /* Typography */
  --font-family-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-family-mono: 'Roboto Mono', 'Courier New', monospace;
  --font-size-base: 16px;
  --font-weight-regular: 400;
  --font-weight-bold: 700;
  
  /* Spacing */
  --space-base: 16px;
  --space-lg: 24px;
  
  /* Radius */
  --radius-base: 8px;
  
  /* Shadow */
  --shadow-base: 0 4px 16px rgba(0,0,0,0.10);
}

/* Diaspora Theme Override */
[data-theme="diaspora"] {
  --theme-header: linear-gradient(180deg, #003049 0%, #005A7D 100%);
  --theme-accent: #F2C94C;
  --theme-background: #F5F0E8;
}

/* Youth Theme Override */
[data-theme="youth"] {
  --theme-header: #00D9C0;
  --theme-accent: #FF9580;
  --theme-background: #F5F5F5;
}

/* Creator Theme Override */
[data-theme="creator"] {
  --theme-header: linear-gradient(90deg, #1E293B 0%, #334155 100%);
  --theme-accent: #F2C94C;
  --theme-background: #FFFFFF;
}

/* Legacy-Builder Theme Override */
[data-theme="legacy"] {
  --theme-header: linear-gradient(180deg, #001F3F 0%, #004080 100%);
  --theme-accent: #10B981;
  --theme-background: #F9FAFB;
}
```

### React/TypeScript Implementation

```typescript
// design-tokens.ts
export const colors = {
  caribbeanBlue: '#003049',
  marketGreen: '#00A896',
  coralRed: '#FF6B6B',
  sovereignGold: '#F2C94C',
  neutral: {
    white: '#FFFFFF',
    light: '#E0E0E0',
    medium: '#BDBDBD',
    dark: '#4F4F4F',
    black: '#000000',
  },
};

export const typography = {
  fontFamily: {
    primary: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    mono: "'Roboto Mono', 'Courier New', monospace",
  },
  fontSize: {
    hero: '48px',
    display: '32px',
    h1: '24px',
    h2: '20px',
    base: '16px',
    sm: '14px',
    xs: '12px',
  },
  fontWeight: {
    bold: 700,
    semibold: 600,
    medium: 500,
    regular: 400,
  },
};

export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '12px',
  base: '16px',
  lg: '24px',
  xl: '32px',
  '2xl': '40px',
  '3xl': '48px',
  '4xl': '64px',
};

export const radius = {
  sm: '4px',
  base: '8px',
  lg: '12px',
  xl: '20px',
};

export const shadows = {
  sm: '0 2px 8px rgba(0,0,0,0.08)',
  base: '0 4px 16px rgba(0,0,0,0.10)',
  lg: '0 8px 24px rgba(0,0,0,0.12)',
};

// Theme tokens by identity
export const themes = {
  diaspora: {
    header: 'linear-gradient(180deg, #003049 0%, #005A7D 100%)',
    accent: '#F2C94C',
    background: '#F5F0E8',
  },
  youth: {
    header: '#00D9C0',
    accent: '#FF9580',
    background: '#F5F5F5',
  },
  creator: {
    header: 'linear-gradient(90deg, #1E293B 0%, #334155 100%)',
    accent: '#F2C94C',
    background: '#FFFFFF',
  },
  legacy: {
    header: 'linear-gradient(180deg, #001F3F 0%, #004080 100%)',
    accent: '#10B981',
    background: '#F9FAFB',
  },
};
```

---

## ✅ TOKEN CHECKLIST

**Before Implementation:**
- [ ] All color tokens defined with accessibility ratios
- [ ] Typography scale covers all use cases
- [ ] Spacing follows 8pt grid system
- [ ] Responsive breakpoints match design
- [ ] Identity themes fully specified
- [ ] Chart tokens defined for data visualization
- [ ] Badge tokens cover all verification states
- [ ] Animation durations and easing defined

**Implementation Files:**
- [ ] `tailwind.config.js` updated
- [ ] CSS custom properties file created
- [ ] TypeScript design tokens exported
- [ ] Figma design tokens JSON exported
- [ ] Documentation published to team

---

**Status:** ✅ Complete and production-ready  
**Next Steps:** Export to Figma, implement in codebase, validate with design team
