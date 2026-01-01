# Design System Naming Conventions - COMPLETE
**CodexDominion Design System v1.0.0**  
**Updated:** December 23, 2025

---

## ✅ Updated Naming Conventions

The design system has been updated with standardized naming conventions across all layers:

### 1. **Component Naming** (PascalCase)

#### Available Components:
```
HeroSection          - Full-screen hero banners
FeatureColumns       - Multi-column feature layouts
CreatorGrid          - Product/creator grid displays
LeaderboardPanel     - Rankings and leaderboards
TestimonialStrip     - Customer testimonial carousels (TODO)
FaqAccordion         - FAQ collapsible sections (TODO)
```

#### Usage in HTML:
```html
<!-- Component classes use lowercase with hyphens -->
<section class="hero-section">...</section>
<div class="feature-columns">...</div>
<div class="creator-grid">...</div>
<div class="leaderboard-panel">...</div>
```

---

### 2. **Utility Classes** (Utility-First CSS)

#### Typography Utilities:
```css
text-display      /* 48px bold - Hero headlines */
text-h1           /* 32px bold - Page titles */
text-h2           /* 24px semi-bold - Section headings */
text-h3           /* 20px semi-bold - Subsections */
text-body         /* 16px regular - Body text */
text-caption      /* 14px regular - Helper text */
text-label        /* 12px uppercase - Labels */
```

**Usage:**
```html
<h1 class="text-display">Hero Headline</h1>
<p class="text-body">Regular paragraph text</p>
<span class="text-label">CATEGORY</span>
```

#### Color Utilities - Text:
```css
text-primary      /* Deep Caribbean Blue (#003049) */
text-accent       /* Gold (#F2C94C) */
text-coral        /* Coral (#FF6B6B) */
text-teal         /* Teal (#00A896) */
text-white        /* White */
text-grey         /* Slate Grey */
```

**Usage:**
```html
<h2 class="text-primary">Blue Heading</h2>
<span class="text-accent">Gold Text</span>
<p class="text-coral">Coral emphasis</p>
```

#### Color Utilities - Background:
```css
bg-primary        /* Deep Caribbean Blue background */
bg-accent         /* Gold background */
bg-coral          /* Coral background */
bg-teal           /* Teal background */
bg-white          /* White background */
bg-light          /* Light grey background */
```

**Usage:**
```html
<div class="bg-primary text-white">Dark section</div>
<button class="bg-accent text-primary">Gold Button</button>
```

#### Color Utilities - Border:
```css
border-primary    /* Blue border */
border-accent     /* Gold border */
border-coral      /* Coral border */
border-teal       /* Teal border */
border-light      /* Light grey border */
```

**Usage:**
```html
<div class="border-accent" style="border-width: 2px;">Gold bordered box</div>
```

#### Spacing Utilities:

**Padding (all sides):**
```css
p-0, p-1, p-2, p-3, p-4, p-5, p-6, p-7, p-8
/* p-4 = 16px padding on all sides */
```

**Padding Horizontal (left + right):**
```css
px-0, px-1, px-2, px-3, px-4, px-5, px-6, px-8
/* px-6 = 32px padding left and right */
```

**Padding Vertical (top + bottom):**
```css
py-0, py-1, py-2, py-3, py-4, py-5, py-6, py-8
/* py-4 = 16px padding top and bottom */
```

**Margin (all sides):**
```css
m-0, m-1, m-2, m-3, m-4, m-5, m-6, m-7, m-8
/* m-5 = 24px margin on all sides */
```

**Margin Top:**
```css
mt-0, mt-1, mt-2, mt-3, mt-4, mt-5, mt-6, mt-8, mt-10
/* mt-8 = 48px margin top */
```

**Margin Bottom:**
```css
mb-0, mb-1, mb-2, mb-3, mb-4, mb-5, mb-6, mb-8, mb-10
/* mb-6 = 32px margin bottom */
```

**Margin Horizontal (left + right):**
```css
mx-0, mx-1, mx-2, mx-3, mx-4, mx-5, mx-6, mx-auto
/* mx-auto = centered horizontally */
```

**Margin Vertical (top + bottom):**
```css
my-0, my-1, my-2, my-3, my-4, my-5, my-6, my-8
/* my-4 = 16px margin top and bottom */
```

**Usage Examples:**
```html
<div class="p-4 mb-6">16px padding, 32px margin bottom</div>
<div class="px-6 py-4">32px horizontal, 16px vertical padding</div>
<div class="mt-8 mx-auto">48px top margin, centered</div>
<section class="py-8 px-4">48px vertical, 16px horizontal padding</section>
```

---

### 3. **Design Tokens** (CSS Variables)

#### Color Tokens:
```css
/* Token Format: --color-{category}-{name} */
--color-primary-blue: #003049;
--color-accent-gold: #F2C94C;
--color-accent-coral: #FF6B6B;
--color-accent-teal: #00A896;

/* Legacy aliases (backward compatibility): */
--color-deep-blue: #003049;   /* Same as color-primary-blue */
--color-gold: #F2C94C;        /* Same as color-accent-gold */
--color-coral: #FF6B6B;       /* Same as color-accent-coral */
--color-teal: #00A896;        /* Same as color-accent-teal */
```

**Usage in Custom CSS:**
```css
.custom-header {
  background: var(--color-primary-blue);
  color: var(--color-accent-gold);
}
```

#### Spacing Tokens:
```css
/* Token Format: --space-{number} */
--space-1: 4px;      /* space.1 - Tight spacing */
--space-2: 8px;      /* space.2 - Small gaps */
--space-3: 12px;     /* space.3 - Default gap */
--space-4: 16px;     /* space.4 - Base unit */
--space-5: 24px;     /* space.5 - Section spacing */
--space-6: 32px;     /* space.6 - Large gaps */
--space-7: 40px;     /* space.7 - XL gaps */
--space-8: 48px;     /* space.8 - XXL gaps */
--space-10: 64px;    /* space.10 - Section breaks */
--space-12: 80px;    /* space.12 - Major sections */
--space-14: 96px;    /* space.14 - Hero sections */
```

**Usage:**
```css
.custom-section {
  padding: var(--space-8);    /* 48px padding */
  margin-bottom: var(--space-6);  /* 32px margin */
}
```

#### Border Radius Tokens:
```css
/* Token Format: --radius-{size} */
--radius-sm: 4px;        /* radius.sm - Small corners */
--radius-md: 8px;        /* radius.md - Medium (buttons, inputs) */
--radius-lg: 12px;       /* radius.lg - Large (cards) */
--radius-xl: 16px;       /* radius.xl - Extra large */
--radius-full: 9999px;   /* radius.full - Fully rounded (badges) */
```

**Usage:**
```css
.custom-button {
  border-radius: var(--radius-md);   /* 8px rounded corners */
}

.custom-card {
  border-radius: var(--radius-lg);   /* 12px rounded corners */
}
```

---

## 📋 Complete Utility Class Reference

### Display Utilities:
```css
d-none            /* display: none */
d-block           /* display: block */
d-inline          /* display: inline */
d-inline-block    /* display: inline-block */
d-flex            /* display: flex */
d-grid            /* display: grid */
```

### Flexbox Utilities:
```css
justify-start     /* justify-content: flex-start */
justify-center    /* justify-content: center */
justify-end       /* justify-content: flex-end */
justify-between   /* justify-content: space-between */
justify-around    /* justify-content: space-around */

align-start       /* align-items: flex-start */
align-center      /* align-items: center */
align-end         /* align-items: flex-end */
align-stretch     /* align-items: stretch */
```

### Gap Utilities (Flex/Grid):
```css
gap-1, gap-2, gap-3, gap-4, gap-5, gap-6
/* gap-4 = 16px gap between flex/grid items */
```

---

## 🎯 Real-World Examples

### Example 1: Hero Section with Utility Classes
```html
<section class="bg-primary text-white py-8 px-4">
  <div class="mx-auto" style="max-width: 960px;">
    <h1 class="text-display mb-4">Your Culture. Your Creators.</h1>
    <p class="text-body mb-6">The Caribbean's first digital economy.</p>
    <button class="bg-accent text-primary px-6 py-3">Get Started</button>
  </div>
</section>
```

### Example 2: Feature Grid
```html
<div class="feature-columns py-8">
  <div class="grid gap-6">
    <div class="col-4 p-5 bg-white">
      <h3 class="text-h3 text-primary mb-3">Marketplace</h3>
      <p class="text-body text-grey">Sell digital products globally.</p>
    </div>
    <div class="col-4 p-5 bg-white">
      <h3 class="text-h3 text-primary mb-3">Youth Program</h3>
      <p class="text-body text-grey">Earn commissions promoting products.</p>
    </div>
    <div class="col-4 p-5 bg-white">
      <h3 class="text-h3 text-primary mb-3">AI Tools</h3>
      <p class="text-body text-grey">Build and promote with AI.</p>
    </div>
  </div>
</div>
```

### Example 3: Custom Component with Tokens
```css
/* Custom CSS using design tokens */
.custom-hero-section {
  background: var(--color-primary-blue);
  padding: var(--space-10) var(--space-4);
  border-radius: var(--radius-lg);
}

.custom-card {
  background: var(--color-accent-gold);
  color: var(--color-primary-blue);
  padding: var(--space-5);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  transition: transform var(--transition-base);
}

.custom-card:hover {
  transform: translateY(-4px);
}
```

---

## ✅ Migration Checklist

When updating existing code to use new conventions:

- [ ] **Typography**: Replace font-size with `.text-*` classes
- [ ] **Colors**: Use `.text-*`, `.bg-*`, `.border-*` utilities
- [ ] **Spacing**: Replace inline padding/margin with `.p-*`, `.m-*` classes
- [ ] **Tokens**: Use CSS variables (`var(--space-4)`) instead of hardcoded values
- [ ] **Components**: Use semantic class names (`.hero-section`, `.feature-columns`)

---

## 🔗 Quick Reference Links

- **Full Documentation**: `DESIGN_SYSTEM_DOCUMENTATION.md`
- **Migration Guide**: `DESIGN_SYSTEM_MIGRATION_GUIDE.md`
- **Live Showcase**: http://localhost:5000/design-system
- **CSS File**: `static/css/design-system.css`

---

## 📊 Naming Convention Summary

| Category | Convention | Examples |
|----------|-----------|----------|
| Components | PascalCase → kebab-case | `HeroSection` → `.hero-section` |
| Utility Classes | Prefix-value | `.text-display`, `.p-4`, `.bg-primary` |
| Design Tokens | --category-name | `--color-primary-blue`, `--space-4`, `--radius-md` |
| CSS Classes | kebab-case | `.btn-primary`, `.card-creator` |
| JavaScript Functions | camelCase | `toggleDarkMode()`, `showToast()` |

---

**Status**: ✅ Complete  
**Version**: 1.0.0  
**Last Updated**: December 23, 2025  

🔥 **The Flame Burns Sovereign and Eternal!** 👑
