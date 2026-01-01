# Codex Dominion Design System Documentation
**Version 1.0.0** | December 23, 2025

## 📚 Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Design Principles](#design-principles)
4. [Color System](#color-system)
5. [Typography](#typography)
6. [Layout & Spacing](#layout--spacing)
7. [Components](#components)
8. [Motion System](#motion-system)
9. [Developer Handoff](#developer-handoff)
10. [Best Practices](#best-practices)

---

## 🎨 Overview

The Codex Dominion Design System is a comprehensive UI kit built on an **8-point spacing system** with a **12-column grid**, Caribbean Blue & Gold color palette, and smooth motion system. Designed for creators, youth, and diaspora communities.

### Key Features:
- ✅ 8-point spacing system for consistent layouts
- ✅ 12-column responsive grid (desktop), 8-column (tablet), 4-column (mobile)
- ✅ Caribbean Blue (#003049) & Gold (#F2C94C) brand palette
- ✅ 50+ pre-built components
- ✅ Dark mode support
- ✅ Smooth 150-300ms transitions
- ✅ Mobile-first responsive design

---

## 🚀 Getting Started

### Installation

Include the design system CSS in your HTML:

```html
<link rel="stylesheet" href="/static/css/design-system.css">
```

### Quick Start Example

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="/static/css/design-system.css">
</head>
<body>
    <div class="container section">
        <h1>Welcome to Codex Dominion</h1>
        <p>Start building with our design system.</p>
        <button class="btn btn-primary">Get Started</button>
    </div>
</body>
</html>
```

### View Live Showcase

Access the complete component library:
```
http://localhost:5000/design-system
```

---

## 🎯 Design Principles

### 1. Direct & Warm
- Use short sentences, minimal jargon
- Speak to creators, youth, diaspora like real people, not "users"

### 2. Confident & Energetic
- Bold colors, clear CTAs
- Smooth animations that feel purposeful, not gimmicky

### 3. Accessible
- WCAG 2.1 AA contrast ratios
- Keyboard navigation support
- Screen reader friendly

---

## 🌈 Color System

### Primary Colors

| Color | Hex | CSS Variable | Usage |
|-------|-----|--------------|-------|
| **Deep Caribbean Blue** | `#003049` | `var(--color-deep-blue)` | Backgrounds, headings |
| **Gold Accent** | `#F2C94C` | `var(--color-gold)` | CTAs, highlights |

### Secondary Colors

| Color | Hex | CSS Variable | Usage |
|-------|-----|--------------|-------|
| **Coral** | `#FF6B6B` | `var(--color-coral)` | Alerts, emphasis, youth energy |
| **Teal/Aqua** | `#00A896` | `var(--color-teal)` | Supporting accents, AI/tech |

### Neutrals

| Color | Hex | CSS Variable |
|-------|-----|--------------|
| White | `#FFFFFF` | `var(--color-white)` |
| Light Grey | `#E0E0E0` | `var(--color-light-grey)` |
| Medium Grey | `#BDBDBD` | `var(--color-medium-grey)` |
| Slate Grey | `#4F4F4F` | `var(--color-slate-grey)` |

### Usage Ratios (Recommended)

- **Backgrounds**: 30% Deep Blue, 40% White, 30% Neutrals
- **CTAs**: 70% Gold, 30% Coral
- **Text**: Slate Grey on light, White on dark

### Dark Mode Colors

```css
--color-dm-bg: #0a1929
--color-dm-surface: #1e293b
--color-dm-border: #334155
--color-dm-text: #e2e8f0
```

---

## 📝 Typography

### Font Family

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
```

### Type Scale

| Element | Size | Weight | Line Height | CSS Class |
|---------|------|--------|-------------|-----------|
| Display | 48px | Bold (700) | 1.2 | `.display` |
| H1 | 32px | Bold (700) | 1.2 | `h1` or `.h1` |
| H2 | 24px | Semi-bold (600) | 1.5 | `h2` or `.h2` |
| H3 | 20px | Semi-bold (600) | 1.5 | `h3` or `.h3` |
| Body | 16px | Regular (400) | 1.6 | `p` or `.body` |
| Caption | 14px | Regular (400) | 1.5 | `.caption` |
| Label | 12px | Semi-bold (600) | 1.2 | `.label` or `.overline` |

### Usage Examples

```html
<h1 class="display">Hero Headline</h1>
<h1>Page Title</h1>
<h2>Section Heading</h2>
<h3>Subsection Heading</h3>
<p>Body text goes here...</p>
<p class="caption">Small helper text</p>
<p class="label">CATEGORY LABEL</p>
```

---

## 📐 Layout & Spacing

### 8-Point Spacing System

All spacing uses multiples of 4px (base unit):

```css
--space-1: 4px    /* Tight spacing */
--space-2: 8px    /* Small gaps */
--space-3: 12px   /* Default gap */
--space-4: 16px   /* Base unit */
--space-5: 24px   /* Section spacing */
--space-6: 32px   /* Large gaps */
--space-7: 40px   /* XL gaps */
--space-8: 48px   /* XXL gaps */
--space-10: 64px  /* Section breaks */
--space-12: 80px  /* Major sections */
--space-14: 96px  /* Hero sections */
```

### Section Padding

```css
/* Desktop */
--section-padding-desktop: 80px;

/* Mobile */
--section-padding-mobile: 48px;
```

Usage:
```html
<section class="section">
    <!-- Content with automatic padding -->
</section>
```

### Content Width

```css
--content-max-width: 1200px;  /* Maximum container width */
--content-safe-width: 960px;  /* Safe content width */
```

Usage:
```html
<div class="container">...</div>
<div class="container container-safe">...</div>
```

### 12-Column Grid System

**Desktop Grid:**
- 12 columns, 72-80px max width per column
- Gutter: 24px
- Margin: 24-32px

**Tablet Grid:**
- 8 columns
- Gutter: 16-24px

**Mobile Grid:**
- 4 columns
- Gutter: 16px

#### Grid Usage

```html
<div class="grid">
    <div class="col-6">Half width</div>
    <div class="col-6">Half width</div>
</div>

<div class="grid">
    <div class="col-4">Third</div>
    <div class="col-4">Third</div>
    <div class="col-4">Third</div>
</div>

<!-- Responsive columns -->
<div class="grid">
    <div class="col-8 col-md-4 col-sm-4">
        Responsive: 8 cols on desktop, 4 on tablet, 4 on mobile
    </div>
</div>
```

### Spacing Utilities

```html
<!-- Margin -->
<div class="mt-4">Margin top: 16px</div>
<div class="mb-5">Margin bottom: 24px</div>
<div class="m-6">Margin all sides: 32px</div>

<!-- Padding -->
<div class="p-4">Padding: 16px</div>
<div class="p-5">Padding: 24px</div>

<!-- Gap (for flex/grid) -->
<div class="d-flex gap-4">...</div>
```

---

## 🧩 Components

### Buttons

#### Primary Button
**Use for**: Main CTAs (e.g., "Start Earning", "Explore Marketplace")

```html
<button class="btn btn-primary">Start Earning</button>
<button class="btn btn-primary btn-lg">Large Button</button>
<button class="btn btn-primary btn-sm">Small Button</button>
<button class="btn btn-primary" disabled>Disabled</button>
```

**Specs:**
- Background: Gold Accent (#F2C94C)
- Text: Deep Blue (#003049)
- Radius: 8px
- Padding: 12-16px vertical, 20-24px horizontal
- Font: 16px, semi-bold

**States:**
- Default: Solid gold
- Hover: Darker gold + shadow + translateY(-1px)
- Active: scale(0.97)
- Disabled: 50% opacity, no hover

#### Secondary Button
**Use for**: Secondary actions (e.g., "Learn More", "View Leaderboard")

```html
<button class="btn btn-secondary">Learn More</button>
```

**Specs:**
- Background: Transparent
- Border: 2px Gold Accent
- Text: Gold Accent
- Same radius & padding as primary

#### Tertiary Button
**Use for**: Low-priority actions ("See all", "View details")

```html
<button class="btn btn-tertiary">See all</button>
```

**Specs:**
- Text only, Coral (#FF6B6B) or Gold
- Underline on hover

---

### Cards

#### Creator Card
**Use for**: Marketplace, featured creators

```html
<div class="card card-creator">
    <div class="card-creator__avatar" style="background: url(avatar.jpg);"></div>
    <h3 class="card-creator__name">Amara Johnson</h3>
    <p class="card-creator__title">Digital Marketing Ebook</p>
    <p class="card-creator__price">$29.99</p>
    <div class="card-creator__tags">
        <span class="tag tag--gold">Ebook</span>
        <span class="tag tag--teal">Marketing</span>
    </div>
</div>
```

**Content:**
- Creator avatar/image
- Creator name
- Product title
- Price
- Tag(s)

**Style:**
- Background: White
- Radius: 12px
- Shadow: Soft (0 8px 24px rgba(0,0,0,0.08))
- Padding: 16-20px

#### Product Card
**Use for**: Grid listings

```html
<div class="card card-product">
    <div class="card-product__badge">Promoted</div>
    <div class="card-product__thumbnail"></div>
    <span class="card-product__category">Ebook</span>
    <h3 class="card-product__title">Side Hustle Success Guide</h3>
    <p class="card-product__price">$24.99</p>
</div>
```

#### Leaderboard Row
**Use for**: Rankings, leaderboards

```html
<div class="leaderboard-row leaderboard-row--top">
    <div class="leaderboard-row__rank">1</div>
    <div class="leaderboard-row__username">@CreatorKing</div>
    <div class="leaderboard-row__earnings">$2,450</div>
    <div class="leaderboard-row__badges">
        <span class="badge">🏆</span>
    </div>
</div>
```

**Style:**
- Alternate row shading
- Top 3 get `.leaderboard-row--top` class with gold gradient

---

### Form Inputs

#### Text Input

```html
<div class="form-group">
    <label class="form-label">Email Address</label>
    <input type="email" class="form-control" placeholder="your@email.com">
</div>
```

**Specs:**
- Border: 1px Slate Gray (30-40% opacity)
- Radius: 8px
- Padding: 10-12px
- Focus: Gold border + subtle glow

#### Textarea

```html
<textarea class="form-control" placeholder="Your message..."></textarea>
```

**Specs:**
- Min-height: 120px
- Vertical resize only

#### Select Dropdown

```html
<div class="select">
    <select class="form-control">
        <option>Choose category...</option>
        <option>Ebook</option>
        <option>Template</option>
    </select>
</div>
```

**Specs:**
- Same style as inputs
- Chevron icon on right (auto-added via CSS)

#### Checkboxes

```html
<label class="checkbox">
    <input type="checkbox">
    <span>I agree to the terms</span>
</label>
```

**Specs:**
- Checked state: Gold fill
- Unchecked: Grey border

---

### Tags & Badges

#### Tags

```html
<span class="tag">Default</span>
<span class="tag tag--gold">Gold</span>
<span class="tag tag--coral">Coral</span>
<span class="tag tag--teal">Teal</span>
```

#### Badges (Notification Counts)

```html
<span class="badge">5</span>
```

---

### Utilities

#### Avatar

```html
<img src="avatar.jpg" class="avatar" alt="User">
<img src="avatar.jpg" class="avatar avatar-lg" alt="User">
```

#### Divider

```html
<div class="divider"></div>
```

---

## 🎬 Motion System

### Principles

- **Feel**: Confident, smooth, not gimmicky
- **Duration**: 150-300ms for most UI motions
- **Easing**:
  - Enter: `ease-out` (cubic-bezier(0.16, 1, 0.3, 1))
  - Exit: `ease-in` (cubic-bezier(0.7, 0, 0.84, 0))

### Transitions

```css
--transition-fast: 150ms cubic-bezier(0.16, 1, 0.3, 1);
--transition-base: 200ms cubic-bezier(0.16, 1, 0.3, 1);
--transition-slow: 300ms cubic-bezier(0.16, 1, 0.3, 1);
--transition-exit: 200ms cubic-bezier(0.7, 0, 0.84, 0);
```

### Page Transitions

```html
<div class="page-transition">
    <!-- Page content -->
</div>
```

**Behavior:**
- Fade + slight upward motion
- Duration: 200-250ms

### Hover States

**Buttons:**
- Slight brightness increase
- Shadow intensifies
- translateY(-1px)

**Cards:**
- Lift: translateY(-2px to -4px)
- Shadow intensifies

### Micro-Interactions

#### Leaderboard Rank-Up

```html
<div class="leaderboard-row rank-up">...</div>
```

**Behavior:**
- Row pulses once, gently slides up
- Small "You moved up!" toast (3 seconds)

#### Badge Unlock

```html
<span class="badge badge-unlock">🏆</span>
```

**Behavior:**
- Scale: 0.8 → 1.05 → 1.0
- Duration: 400-500ms
- Sparkle/glow effect

#### Button Press

**Behavior:**
- 0.95 scale on mousedown
- Back to 1.0 on mouseup

### Loading States

#### Skeleton Loading

```html
<div class="skeleton" style="height: 200px;"></div>
<div class="skeleton" style="height: 20px; width: 60%;"></div>
```

**Behavior:**
- Animating shimmer
- 1000-1500ms loop

#### Loading Copy

- "Loading your opportunities..." (for youth)
- "Loading your marketplace..." (for creators)

---

## 💻 Developer Handoff

### Content Model

```json
{
  "page": {
    "id": "home",
    "slug": "/",
    "title": "Codex Dominion",
    "seo": {
      "title": "Codex Dominion - Digital Marketplace",
      "description": "..."
    },
    "sections": [
      {
        "id": "hero",
        "type": "hero",
        "props": {
          "headline": "Start Earning Today",
          "subheadline": "Join thousands of creators...",
          "cta": {
            "label": "Get Started",
            "href": "/signup",
            "variant": "primary"
          }
        }
      }
    ]
  }
}
```

### CTA Object Structure

```json
{
  "label": "Start Earning",
  "href": "/signup",
  "variant": "primary"
}
```

**Variants**: `primary`, `secondary`, `link`

### Section Types

- `hero` - Hero banner with CTA
- `threeColumn` - 3-column layout
- `grid` - Product/creator grid
- `faq` - FAQ accordion
- `testimonials` - Customer testimonials
- `leaderboard` - Rankings table

### Naming Conventions

**CSS Classes:**
- BEM methodology: `.block__element--modifier`
- Example: `.card-creator__name--highlighted`

**Components:**
- PascalCase: `CreatorCard`, `ProductGrid`

**Functions:**
- camelCase: `showToast()`, `toggleDarkMode()`

**Files:**
- kebab-case: `design-system.css`, `creator-card.html`

---

## ✅ Best Practices

### 1. Always Use Design Tokens

```css
/* ✅ Good */
color: var(--color-gold);
padding: var(--space-4);

/* ❌ Bad */
color: #F2C94C;
padding: 16px;
```

### 2. Maintain Spacing Consistency

Use the 8-point system for all spacing:

```css
/* ✅ Good */
margin-bottom: var(--space-5);  /* 24px */

/* ❌ Bad */
margin-bottom: 23px;
```

### 3. Responsive Design

Mobile-first approach:

```css
/* ✅ Good */
.card {
  width: 100%;
}

@media (min-width: 768px) {
  .card {
    width: 50%;
  }
}
```

### 4. Accessibility

- Use semantic HTML (`<button>`, `<nav>`, `<main>`)
- Include alt text for images
- Ensure 4.5:1 contrast ratio for text
- Support keyboard navigation

### 5. Dark Mode Support

Always define dark mode styles:

```css
.card {
  background: var(--color-white);
}

.dark-mode .card {
  background: var(--color-dm-surface);
}
```

### 6. Performance

- Use CSS transitions instead of JavaScript animations
- Minimize repaints/reflows
- Lazy load images
- Use `will-change` sparingly

---

## 🔗 Resources

- **Live Showcase**: http://localhost:5000/design-system
- **CSS File**: `/static/css/design-system.css`
- **Template**: `/templates/design-system-showcase.html`
- **Figma**: [Link to Figma file] (TODO)
- **GitHub**: [Repository link] (TODO)

---

## 📞 Support

For questions or contributions:
- Email: design@codexdominion.app
- Slack: #design-system
- GitHub Issues: [Link]

---

**Version**: 1.0.0  
**Last Updated**: December 23, 2025  
**Maintained by**: Codex Dominion Design Team

🔥 **The Flame Burns Sovereign and Eternal!** 👑
