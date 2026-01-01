# Design System Migration Guide
**How to Update Existing Dashboards to Use the New Design System**

## 🎯 Overview

This guide walks you through migrating existing dashboard pages to use the new Codex Dominion Design System. Follow these steps to ensure consistency across all pages.

---

## ✅ Pre-Migration Checklist

- [ ] Backup current CSS files
- [ ] Review existing page layouts
- [ ] Identify inline styles to remove
- [ ] Test design system showcase: http://localhost:5000/design-system
- [ ] Have `design-system.css` loaded in your template

---

## 📦 Step-by-Step Migration

### Step 1: Add Design System CSS

Add to your HTML `<head>`:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/design-system.css') }}">
```

### Step 2: Update Container Structure

**Before:**
```html
<div style="max-width: 1200px; margin: 0 auto; padding: 20px;">
    <!-- Content -->
</div>
```

**After:**
```html
<div class="container section">
    <!-- Content -->
</div>
```

### Step 3: Replace Button Styles

**Before:**
```html
<button style="background: #F2C94C; color: #003049; padding: 12px 24px; border-radius: 8px;">
    Submit
</button>
```

**After:**
```html
<button class="btn btn-primary">Submit</button>
```

**Button Types:**
- Primary action: `.btn-primary` (Gold background)
- Secondary action: `.btn-secondary` (Gold outline)
- Tertiary action: `.btn-tertiary` (Text only)

### Step 4: Update Card Components

**Before:**
```html
<div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    <h3>Creator Name</h3>
    <p>Product Title</p>
    <span>$29.99</span>
</div>
```

**After:**
```html
<div class="card card-creator">
    <div class="card-creator__avatar" style="background: url(avatar.jpg);"></div>
    <h3 class="card-creator__name">Creator Name</h3>
    <p class="card-creator__title">Product Title</p>
    <p class="card-creator__price">$29.99</p>
</div>
```

### Step 5: Replace Inline Spacing

**Before:**
```html
<div style="margin-top: 24px; margin-bottom: 32px;">
    Content
</div>
```

**After:**
```html
<div class="mt-5 mb-6">
    Content
</div>
```

**Spacing Classes:**
- `.m-0` through `.m-6` (margin: 0px to 32px)
- `.p-0` through `.p-6` (padding: 0px to 32px)
- `.mt-4`, `.mb-5`, `.ml-3`, `.mr-6` (specific sides)
- `.gap-3`, `.gap-4`, `.gap-5` (for flex/grid gaps)

### Step 6: Update Typography

**Before:**
```html
<h1 style="font-size: 48px; font-weight: bold; color: #003049;">
    Page Title
</h1>
```

**After:**
```html
<h1 class="display">Page Title</h1>
<!-- OR -->
<h1>Page Title</h1>
```

**Typography Classes:**
- `.display` - 48px bold (hero headlines)
- `h1` - 32px bold (page titles)
- `h2` - 24px semi-bold (section headings)
- `h3` - 20px semi-bold (subsections)
- `.body` or `p` - 16px regular (body text)
- `.caption` - 14px regular (helper text)
- `.label` or `.overline` - 12px uppercase (labels)

### Step 7: Replace Form Elements

**Before:**
```html
<input type="text" style="padding: 12px; border: 1px solid #ccc; border-radius: 8px; width: 100%;">
```

**After:**
```html
<div class="form-group">
    <label class="form-label">Label Text</label>
    <input type="text" class="form-control" placeholder="Placeholder...">
</div>
```

### Step 8: Update Grid Layouts

**Before:**
```html
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px;">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
</div>
```

**After:**
```html
<div class="grid gap-5">
    <div class="col-4">Item 1</div>
    <div class="col-4">Item 2</div>
    <div class="col-4">Item 3</div>
</div>
```

**Grid Classes:**
- `.col-12` - Full width
- `.col-6` - Half width
- `.col-4` - Third width
- `.col-3` - Quarter width
- Add responsive: `.col-md-6`, `.col-sm-12`

### Step 9: Add Dark Mode Support

Add dark mode toggle:

```html
<button onclick="toggleDarkMode()" class="btn btn-tertiary">
    🌙 Dark Mode
</button>

<script>
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Load saved preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}
</script>
```

### Step 10: Replace Color Variables

**Before:**
```css
background-color: #003049;
color: #F2C94C;
```

**After:**
```css
background-color: var(--color-deep-blue);
color: var(--color-gold);
```

**Available Color Variables:**
- `--color-deep-blue` (#003049)
- `--color-gold` (#F2C94C)
- `--color-coral` (#FF6B6B)
- `--color-teal` (#00A896)
- `--color-white` (#FFFFFF)
- `--color-light-grey` (#E0E0E0)
- `--color-medium-grey` (#BDBDBD)
- `--color-slate-grey` (#4F4F4F)

---

## 🎨 Page-by-Page Migration Examples

### Revenue Dashboard (`/revenue`)

**Current Issues:**
- Inline styles for charts
- Custom button styles
- Inconsistent spacing

**Migration Steps:**

1. **Update Chart Container:**
```html
<!-- Before -->
<div style="background: white; padding: 20px; margin-bottom: 20px;">
    <canvas id="revenueChart"></canvas>
</div>

<!-- After -->
<div class="card p-5 mb-5">
    <canvas id="revenueChart"></canvas>
</div>
```

2. **Update Buttons:**
```html
<!-- Before -->
<button style="background: #4CAF50; color: white; padding: 10px 20px;">
    View Details
</button>

<!-- After -->
<button class="btn btn-primary">View Details</button>
```

3. **Update Grid Layout:**
```html
<!-- Before -->
<div style="display: flex; gap: 20px;">
    <div style="flex: 1;">Chart 1</div>
    <div style="flex: 1;">Chart 2</div>
</div>

<!-- After -->
<div class="grid gap-5">
    <div class="col-6">Chart 1</div>
    <div class="col-6">Chart 2</div>
</div>
```

### Social Media Scheduler (`/scheduler`)

1. **Update Form:**
```html
<!-- After -->
<form class="section">
    <div class="form-group">
        <label class="form-label">Platform</label>
        <select class="form-control">
            <option>Instagram</option>
            <option>TikTok</option>
        </select>
    </div>

    <div class="form-group">
        <label class="form-label">Post Content</label>
        <textarea class="form-control" placeholder="What's on your mind?"></textarea>
    </div>

    <button type="submit" class="btn btn-primary">Schedule Post</button>
</form>
```

2. **Update Post Cards:**
```html
<div class="card p-4 mb-4">
    <div class="d-flex justify-between align-center mb-3">
        <span class="tag tag--teal">Instagram</span>
        <span class="caption">2 hours ago</span>
    </div>
    <p class="body">Check out our new products! 🚀</p>
    <button class="btn btn-tertiary mt-3">Edit</button>
</div>
```

### Product Generator (`/product-generator`)

1. **Update Form Controls:**
```html
<div class="container section">
    <h1>AI Product Description Generator</h1>

    <div class="form-group">
        <label class="form-label">Product Name</label>
        <input type="text" class="form-control" id="productName" placeholder="Enter product name...">
    </div>

    <div class="form-group">
        <label class="form-label">Writing Style</label>
        <select class="form-control" id="style">
            <option value="professional">Professional</option>
            <option value="casual">Casual</option>
            <option value="energetic">Energetic</option>
        </select>
    </div>

    <button class="btn btn-primary btn-lg" onclick="generateDescription()">
        ✨ Generate Description
    </button>

    <div id="result" class="card p-5 mt-5" style="display: none;">
        <h3>Generated Description:</h3>
        <p id="generatedText" class="body"></p>
        <button class="btn btn-secondary mt-4" onclick="copyToClipboard()">
            📋 Copy to Clipboard
        </button>
    </div>
</div>
```

---

## 🔍 Common Patterns Reference

### Hero Section
```html
<section class="section">
    <div class="container">
        <h1 class="display mb-4">Welcome to Codex Dominion</h1>
        <p class="body mb-6">Start earning today with digital products.</p>
        <button class="btn btn-primary btn-lg">Get Started</button>
    </div>
</section>
```

### Three-Column Grid
```html
<div class="grid gap-5">
    <div class="col-4">
        <div class="card p-5">
            <h3>Feature 1</h3>
            <p>Description...</p>
        </div>
    </div>
    <div class="col-4">
        <div class="card p-5">
            <h3>Feature 2</h3>
            <p>Description...</p>
        </div>
    </div>
    <div class="col-4">
        <div class="card p-5">
            <h3>Feature 3</h3>
            <p>Description...</p>
        </div>
    </div>
</div>
```

### Creator Marketplace Grid
```html
<div class="grid gap-4">
    <div class="col-3 col-md-6 col-sm-12">
        <div class="card card-creator">
            <div class="card-creator__avatar" style="background: url(avatar1.jpg);"></div>
            <h3 class="card-creator__name">Amara Johnson</h3>
            <p class="card-creator__title">Digital Marketing Ebook</p>
            <p class="card-creator__price">$29.99</p>
            <div class="card-creator__tags">
                <span class="tag tag--gold">Ebook</span>
            </div>
        </div>
    </div>
    <!-- Repeat for more creators -->
</div>
```

### Leaderboard Table
```html
<div class="card p-5">
    <h2 class="mb-4">Top Creators</h2>
    <div class="leaderboard-row leaderboard-row--top">
        <div class="leaderboard-row__rank">1</div>
        <div class="leaderboard-row__username">@CreatorKing</div>
        <div class="leaderboard-row__earnings">$2,450</div>
        <div class="leaderboard-row__badges">
            <span class="badge">🏆</span>
        </div>
    </div>
    <!-- More rows -->
</div>
```

---

## ⚠️ Common Mistakes to Avoid

### ❌ DON'T: Mix old and new styles
```html
<!-- Bad -->
<button class="btn btn-primary" style="background: red;">Submit</button>
```

### ✅ DO: Use design system classes only
```html
<!-- Good -->
<button class="btn btn-primary">Submit</button>
```

### ❌ DON'T: Use arbitrary spacing values
```css
/* Bad */
margin-bottom: 23px;
```

### ✅ DO: Use the 8-point system
```css
/* Good */
margin-bottom: var(--space-5); /* 24px */
```

### ❌ DON'T: Hardcode colors
```css
/* Bad */
color: #F2C94C;
```

### ✅ DO: Use CSS variables
```css
/* Good */
color: var(--color-gold);
```

---

## 🧪 Testing Checklist

After migration, test:

- [ ] Mobile responsiveness (320px, 768px, 1024px, 1440px)
- [ ] Dark mode toggle works
- [ ] All buttons have hover/active states
- [ ] Form inputs have focus states (gold glow)
- [ ] Cards have hover effects
- [ ] Typography scales correctly
- [ ] Grid layouts adapt on mobile
- [ ] Spacing is consistent (8-point system)
- [ ] Colors match design system palette
- [ ] Transitions are smooth (150-300ms)

---

## 📊 Migration Progress Tracker

| Page | Status | Priority | Notes |
|------|--------|----------|-------|
| `/design-system` | ✅ Complete | - | Showcase page |
| `/` (Homepage) | ⏳ Pending | High | |
| `/revenue` | ⏳ Pending | High | |
| `/scheduler` | ⏳ Pending | High | |
| `/product-generator` | ⏳ Pending | High | |
| `/social` | ⏳ Pending | Medium | |
| `/stores` | ⏳ Pending | Medium | |
| `/agents` | ⏳ Pending | Medium | |
| `/copilot` | ⏳ Pending | Low | |

---

## 🚀 Next Steps

1. **Test Design System**: Visit http://localhost:5000/design-system
2. **Start with High Priority**: Migrate homepage, revenue, scheduler first
3. **Update One Page at a Time**: Test thoroughly before moving to next
4. **Remove Old CSS**: After migration, delete unused CSS files
5. **Document Changes**: Update README with new structure
6. **Train Team**: Share this guide with all developers

---

## 📞 Need Help?

- **Design System Docs**: `DESIGN_SYSTEM_DOCUMENTATION.md`
- **Live Showcase**: http://localhost:5000/design-system
- **CSS File**: `static/css/design-system.css`
- **Questions**: Post in #design-system Slack channel

---

**Version**: 1.0.0  
**Last Updated**: December 23, 2025

🔥 **The Flame Burns Sovereign and Eternal!** 👑
