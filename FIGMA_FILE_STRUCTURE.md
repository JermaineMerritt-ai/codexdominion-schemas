# FIGMA FILE STRUCTURE & NAMING SYSTEM
**CodexDominion Design System**  
**Version 1.0.0** | December 23, 2025

---

## 🏗️ OVERVIEW

This document defines the **exact file structure, naming conventions, and quality standards** for the CodexDominion Figma design system. This is the **single source of truth** for all design work.

---

## 📛 COMPONENT NAMING SYSTEM

### Pattern (BEM-like)
```
Category / ComponentName / Variant / State
```

**Example:**
```
Button / Primary / Default
Button / Primary / Hover
Button / Primary / Disabled
Card / Creator / Default
Input / Text / Error
```

---

## 🗂️ COMPONENT CATEGORIES

### 1. Layout/

**Purpose:** Grid systems, containers, section templates

```
Layout / Grid / Desktop
Layout / Grid / Tablet
Layout / Grid / Mobile
Layout / Section / Standard
Layout / Section / Wide
Layout / Container / Content
Layout / Container / Full
```

**Usage:**
- Desktop: 12-column grid, 24px gutter
- Tablet: 8-column grid, 24px gutter
- Mobile: 4-column grid, 16px gutter

---

### 2. Navigation/

**Purpose:** Headers, footers, tabs, breadcrumbs

```
Navigation / Header / Default
Navigation / Header / Logged In
Navigation / Footer / Default
Navigation / Tab / Primary
Navigation / Tab / Secondary
Navigation / Breadcrumb / Default
```

**States:**
- Default
- Hover
- Active

---

### 3. Buttons/

**Purpose:** All button types and states

```
Button / Primary / Default
Button / Primary / Hover
Button / Primary / Pressed
Button / Primary / Disabled

Button / Secondary / Default
Button / Secondary / Hover
Button / Secondary / Pressed
Button / Secondary / Disabled

Button / Tertiary / Text
Button / Tertiary / Hover
Button / Tertiary / Pressed
```

**Required States:**
- Default (initial state)
- Hover (mouse over)
- Pressed (active click)
- Disabled (non-interactive)

---

### 4. Inputs/

**Purpose:** Form fields, checkboxes, toggles, selects

```
Input / Text / Default
Input / Text / Focus
Input / Text / Error
Input / Text / Success
Input / Text / Disabled

Input / Select / Default
Input / Select / Open
Input / Select / Error

Input / Checkbox / Unchecked
Input / Checkbox / Checked
Input / Checkbox / Disabled

Input / Toggle / Off
Input / Toggle / On
Input / Toggle / Disabled
```

**Required States:**
- Default
- Focus (active input)
- Error (validation failed)
- Success (validation passed)
- Disabled

---

### 5. Cards/

**Purpose:** Content containers for creators, products, challenges

```
Card / Creator / Default
Card / Creator / Hover

Card / Product / Default
Card / Product / Featured
Card / Product / Hover

Card / Challenge / Default
Card / Challenge / Active
Card / Challenge / Completed

Card / Testimonial / Default
```

**Required States:**
- Default
- Hover (elevation change)
- Featured (special styling for promoted items)

---

### 6. Feedback/

**Purpose:** Toasts, badges, alerts, notifications

```
Feedback / Toast / Success
Feedback / Toast / Error
Feedback / Toast / Warning
Feedback / Toast / Info

Feedback / Badge / Rank
Feedback / Badge / Challenge
Feedback / Badge / New

Feedback / Alert / Success
Feedback / Alert / Error
Feedback / Alert / Warning
```

**Toast Auto-Dismiss:**
- Success: 3s
- Error: Persistent (manual dismiss)
- Warning: 5s
- Info: 3s

---

### 7. Data Display/

**Purpose:** Leaderboards, stats, progress bars

```
Data / LeaderboardRow / Default
Data / LeaderboardRow / Highlighted
Data / LeaderboardRow / Top3

Data / Stat / KPI
Data / Stat / Revenue
Data / Stat / Engagement

Data / Progress / Challenge
Data / Progress / Upload
Data / Progress / Loading
```

---

### 8. Overlays/

**Purpose:** Modals, drawers, tooltips, popovers

```
Overlay / Modal / Center
Overlay / Modal / Confirmation
Overlay / Modal / Form

Overlay / Drawer / Right
Overlay / Drawer / Left

Overlay / Tooltip / Top
Overlay / Tooltip / Bottom
Overlay / Tooltip / Right
Overlay / Tooltip / Left

Overlay / Popover / Menu
```

---

### 9. Icons/

**Purpose:** All iconography (24x24px default size)

```
Icon / ArrowRight
Icon / ArrowLeft
Icon / Crown
Icon / Lightning
Icon / Trophy
Icon / Check
Icon / Close
Icon / Menu
Icon / Search
Icon / Upload
Icon / Share
Icon / Heart
Icon / Star
```

**Icon Sizes:**
- Small: 16x16px (inline icons)
- Default: 24x24px (UI icons)
- Large: 32x32px (feature icons)
- XL: 48x48px (hero icons)

---

### 10. Sections/

**Purpose:** Full-width page sections

```
Section / Hero / Homepage
Section / Hero / Marketplace
Section / Hero / DominionYouth
Section / Hero / Diaspora
Section / Hero / ActionAI

Section / Grid / Creators
Section / Grid / Products
Section / Grid / Challenges

Section / FAQ / Default
Section / FAQ / Expanded

Section / CTA / Newsletter
Section / CTA / GetStarted
```

---

## 📄 FIGMA PAGE STRUCTURE

### File Name
```
CodexDominion Design System v1.0
```

---

### Page 00 – Foundations

**Purpose:** Design tokens, variables, core styles

**Frames:**
```
00 – Foundations
├── Color Tokens
│   ├── Primary Colors (Blue, Gold, Coral, Teal)
│   ├── Neutral Colors (White, Gray scale)
│   └── Semantic Colors (Success, Warning, Error, Info)
│
├── Typography Styles
│   ├── Display (48px, Bold)
│   ├── H1 (32px, Semibold)
│   ├── H2 (24px, Semibold)
│   ├── H3 (20px, Semibold)
│   ├── Body (16px, Regular)
│   ├── Caption (14px, Regular)
│   └── Overline (12px, Medium)
│
├── Spacing Scale (8-pt grid)
│   ├── space.1 (4px)
│   ├── space.2 (8px)
│   ├── space.3 (12px)
│   ├── space.4 (16px)
│   ├── space.5 (24px)
│   ├── space.6 (32px)
│   ├── space.7 (40px)
│   ├── space.8 (48px)
│   └── space.9 (64px)
│
├── Border Radius
│   ├── radius.sm (4px)
│   ├── radius.md (8px)
│   ├── radius.lg (12px)
│   └── radius.xl (20px)
│
├── Shadows
│   ├── shadow.sm (subtle lift)
│   ├── shadow.md (card elevation)
│   └── shadow.lg (modal/overlay)
│
└── Grid + Layout Examples
    ├── Desktop (12-column, 24px gutter)
    ├── Tablet (8-column, 24px gutter)
    └── Mobile (4-column, 16px gutter)
```

---

### Page 01 – Components

**Purpose:** Atomic components (buttons, inputs, cards, etc.)

**Frames:**
```
01 – Components
├── Buttons
│   ├── Primary (Default, Hover, Pressed, Disabled)
│   ├── Secondary (Default, Hover, Pressed, Disabled)
│   └── Tertiary (Default, Hover, Pressed)
│
├── Inputs
│   ├── Text (Default, Focus, Error, Success, Disabled)
│   ├── Select (Default, Open, Error)
│   ├── Checkbox (Unchecked, Checked, Disabled)
│   └── Toggle (Off, On, Disabled)
│
├── Cards
│   ├── Creator (Default, Hover)
│   ├── Product (Default, Featured, Hover)
│   ├── Challenge (Default, Active, Completed)
│   └── Testimonial (Default)
│
├── Navigation
│   ├── Header (Default, Logged In)
│   ├── Footer (Default)
│   └── Tabs (Primary, Secondary)
│
├── Overlays
│   ├── Modal (Center, Confirmation, Form)
│   ├── Drawer (Right, Left)
│   └── Tooltip (Top, Bottom, Right, Left)
│
├── Data Display
│   ├── LeaderboardRow (Default, Highlighted, Top3)
│   ├── Stat / KPI
│   └── Progress (Challenge, Upload, Loading)
│
├── Badges & Toasts
│   ├── Badge (Rank, Challenge, New)
│   └── Toast (Success, Error, Warning, Info)
│
└── Icons (24x24px)
    ├── Navigation (Arrow, Menu, Close)
    ├── Actions (Upload, Share, Download)
    └── Social (WhatsApp, Instagram, TikTok, Facebook)
```

---

### Page 02 – Patterns

**Purpose:** Component compositions and reusable patterns

**Frames:**
```
02 – Patterns
├── Forms
│   ├── Sign Up Form
│   ├── Login Form
│   ├── Upload Product Form
│   └── Payout Request Form
│
├── Tables
│   ├── Leaderboard Table
│   ├── Transaction History Table
│   └── Product List Table
│
├── Leaderboard Layouts
│   ├── Weekly Leaderboard
│   ├── Monthly Leaderboard
│   └── All-Time Leaderboard
│
├── Challenge Panels
│   ├── Active Challenge
│   ├── Completed Challenge
│   └── Locked Challenge
│
├── Product Grids
│   ├── 3-Column Grid (Desktop)
│   ├── 2-Column Grid (Tablet)
│   └── 1-Column Grid (Mobile)
│
└── Onboarding Sequences
    ├── Welcome Screen
    ├── Role Selection
    ├── Profile Setup
    └── First Action
```

---

### Page 03 – Marketing Pages

**Purpose:** Full marketing website pages (Homepage, Marketplace, etc.)

**Frames:**
```
03 – Marketing Pages
├── Homepage
│   ├── Desktop / Homepage / v1
│   ├── Tablet / Homepage / v1
│   └── Mobile / Homepage / v1
│
├── Marketplace
│   ├── Desktop / Marketplace / v1
│   ├── Tablet / Marketplace / v1
│   └── Mobile / Marketplace / v1
│
├── DominionYouth
│   ├── Desktop / DominionYouth / v1
│   ├── Tablet / DominionYouth / v1
│   └── Mobile / DominionYouth / v1
│
├── Diaspora
│   ├── Desktop / Diaspora / v1
│   ├── Tablet / Diaspora / v1
│   └── Mobile / Diaspora / v1
│
├── Action AI
│   ├── Desktop / ActionAI / v1
│   ├── Tablet / ActionAI / v1
│   └── Mobile / ActionAI / v1
│
├── About
│   ├── Desktop / About / v1
│   └── Mobile / About / v1
│
├── Manifesto
│   ├── Desktop / Manifesto / v1
│   └── Mobile / Manifesto / v1
│
└── FAQ
    ├── Desktop / FAQ / v1
    └── Mobile / FAQ / v1
```

**Frame Naming Pattern:**
```
[Breakpoint] / [Page Name] / v[Version]

Examples:
- Desktop / Homepage / v1
- Mobile / Upload Product / v2
- Tablet / Marketplace / v1
```

---

### Page 04 – App Flows

**Purpose:** User flows and screens for core application features

**Frames:**
```
04 – App Flows
├── Sign Up Flow
│   ├── 1. Welcome Screen
│   ├── 2. Create Account
│   ├── 3. Verify Email
│   └── 4. Success
│
├── Upload Product Flow
│   ├── 1. Product Details
│   ├── 2. Upload Files
│   ├── 3. Preview
│   └── 4. Published
│
├── Share Link Flow
│   ├── 1. Link Generated
│   ├── 2. Share Options
│   └── 3. Shared Success
│
├── Purchase Flow
│   ├── 1. Product Page
│   ├── 2. Checkout
│   ├── 3. Payment Processing
│   └── 4. Purchase Complete
│
├── Payout Flow
│   ├── 1. Earnings Dashboard
│   ├── 2. Request Payout
│   ├── 3. Processing
│   └── 4. Payout Complete
│
└── Leaderboard Flow
    ├── 1. Leaderboard View
    ├── 2. Rank-Up Notification
    └── 3. Badge Unlocked
```

**Flow Naming Pattern:**
```
[Step Number]. [Screen Name]

Example:
- 1. Welcome Screen
- 2. Create Account
- 3. Success
```

---

### Page 05 – Prototypes

**Purpose:** Interactive prototypes for testing and demos

**Frames:**
```
05 – Prototypes
├── Launch Site Prototype
│   ├── Homepage → Marketplace
│   ├── Homepage → DominionYouth
│   └── Homepage → Action AI
│
├── Youth Onboarding Prototype
│   ├── Welcome → Role Selection
│   ├── Role Selection → Profile Setup
│   └── Profile Setup → First Challenge
│
└── Creator Onboarding Prototype
    ├── Welcome → Create Account
    ├── Create Account → Upload Product
    └── Upload Product → Share Link
```

**Prototype Settings:**
- Device: Desktop (1440px width) or Mobile (375px width)
- Background: #F5F5F5 (light gray)
- Starting Frame: Clearly labeled "START HERE"

---

### Page 06 – Archive

**Purpose:** Deprecated designs, old explorations (keep for reference)

**Frames:**
```
06 – Archive
├── Old Explorations
│   ├── Homepage Iteration 1
│   ├── Homepage Iteration 2
│   └── Card Explorations
│
└── Deprecated Versions
    ├── Old Button System (v0.9)
    ├── Old Color Palette (v0.8)
    └── Old Typography (v0.7)
```

---

## ✅ DESIGN QA CHECKLIST

**Before ANY design ships, it MUST pass this checklist.**

---

### 📐 Visual & Layout

#### Spacing
- [ ] Uses **8-pt spacing scale** (4px, 8px, 12px, 16px, 24px, 32px, 40px, 48px, 64px)
- [ ] **No random spacing** (5px, 11px, 23px, etc.)
- [ ] Consistent spacing between similar elements
- [ ] Padding and margins use design tokens

#### Grid
- [ ] Components **align to grid**
- [ ] No off-grid drift (snap to 8px grid)
- [ ] Desktop: 12-column grid used correctly
- [ ] Tablet: 8-column grid used correctly
- [ ] Mobile: 4-column grid used correctly

#### Typography
- [ ] Correct **text styles** used (Display, H1, H2, H3, Body, Caption, Overline)
- [ ] Font sizes match design system (48px, 32px, 24px, 20px, 16px, 14px, 12px)
- [ ] Font weights correct (Bold 700, Semibold 600, Medium 500, Regular 400)
- [ ] Line heights set correctly (1.5 for body, 1.2 for headings)

#### Color
- [ ] **Only brand tokens used** (`color.primary.blue`, `color.primary.gold`, etc.)
- [ ] No arbitrary hex codes (#123456, etc.)
- [ ] Semantic colors used correctly (success, warning, error, info)
- [ ] Color palette consistent across all screens

---

### 🎯 States & Interactions

#### Buttons
- [ ] **Default** state defined
- [ ] **Hover** state defined (brightness +10%, shadow increase, translateY -1px)
- [ ] **Pressed** state defined (scale 0.97, shadow reduces)
- [ ] **Disabled** state defined (50% opacity, cursor not-allowed)
- [ ] All states use design system components

#### Inputs
- [ ] **Default** state defined
- [ ] **Focus** state defined (gold border + glow)
- [ ] **Error** state defined (red border + error message)
- [ ] **Success** state defined (green border)
- [ ] **Disabled** state defined (50% opacity)

#### Links
- [ ] **Hover** state defined (underline, color change)
- [ ] **Visited** state defined where needed
- [ ] Focus state visible (for accessibility)

#### Micro-Interactions
- [ ] **Button hover** behavior specified (150ms duration, ease-out)
- [ ] **Card lift** behavior specified (translateY -4px, shadow increase)
- [ ] **Rank-up animation** specified (slide up 20px, pulse glow, toast)
- [ ] **Badge unlock** specified (scale 0.8 → 1.05 → 1.0, glow effect)
- [ ] **Sale notification** specified (slide from top-right, confetti, 3s auto-dismiss)

---

### ♿ Accessibility

#### Contrast
- [ ] Text meets **WCAG AA** contrast ratio minimum:
  - Normal text: 4.5:1
  - Large text (18px+): 3:1
- [ ] Primary color combos checked (blue on white, gold on blue, etc.)
- [ ] Links distinguishable from body text

#### Text Size
- [ ] Body text **≥ 16px** (mobile and desktop)
- [ ] Caption text ≥ 14px
- [ ] All text readable on smallest supported screen (320px)

#### Focus States
- [ ] **Visible focus indicator** on all interactive elements
- [ ] Focus ring uses `color.primary.gold` with 3px glow
- [ ] Focus order logical (top to bottom, left to right)

#### Interactive Targets
- [ ] Buttons ≥ 44x44px (mobile touch targets)
- [ ] Links ≥ 44px height with adequate spacing

---

### 📝 Content

#### Voice & Tone
- [ ] **Direct and warm** (no corporate jargon)
- [ ] Empowering language ("Your", "You", "Create", "Earn")
- [ ] Caribbean pride evident (culture, community references)
- [ ] Emoji used strategically (🔥, 🎉, 👑, 💰, 💙)

#### Consistency
- [ ] **Same action = same label**
  - Example: Always "Start Earning", never "Begin Earning"
- [ ] Button labels consistent across flows
- [ ] Terminology consistent (creator vs. seller, product vs. item)

#### Error Messages
- [ ] **Human and specific** ("This email is already in use. Try signing in?")
- [ ] Not blaming the user ("Please enter a valid email" vs. "You entered an invalid email")
- [ ] Helpful next steps provided

#### Empty States
- [ ] Friendly copy ("No products yet" vs. "0 products found")
- [ ] Clear call-to-action ("Upload Product" button)

---

### 🔄 Handoff

#### Component Usage
- [ ] Uses **design system components** (not detached copies)
- [ ] Component overrides documented
- [ ] No "frankenstein" components (avoid mixing detached + system components)

#### Naming Conventions
- [ ] Frames use agreed naming system:
  - `Desktop / Homepage / v1`
  - `Mobile / Upload Product / v2`
- [ ] Components use BEM-like pattern:
  - `Button / Primary / Default`
  - `Card / Creator / Hover`
- [ ] Layers named clearly (not "Frame 1234", "Rectangle 5678")

#### Annotations
- [ ] **Edge cases annotated**:
  - Empty states (no products, no sales)
  - Max length scenarios (long product names, long usernames)
  - Loading states (spinner, skeleton screens)
  - Error states (network error, validation error)
- [ ] Interaction notes added ("On click, show modal")
- [ ] Responsive behavior documented ("Hide on mobile")

#### Assets
- [ ] Images optimized (WebP format, compressed)
- [ ] Icons exported as SVG (not PNG)
- [ ] Fonts included in Figma file
- [ ] All assets properly named and organized

---

## 🚀 FIGMA BEST PRACTICES

### Auto Layout
- Always use **Auto Layout** for components (not absolute positioning)
- Set resizing: **Hug contents** or **Fill container**
- Use consistent spacing (from design tokens)

### Constraints
- Set constraints for responsive behavior
- Use **Scale** for icons, **Left/Right** for text

### Variants
- Use **Component Properties** for variants (not separate components)
- Example: Button with `Type` (Primary, Secondary, Tertiary) and `State` (Default, Hover, Pressed, Disabled)

### Variables
- Import design tokens as **local variables**
- Apply variables to fills, strokes, text, spacing
- Keep variables organized in collections (Color, Typography, Spacing, etc.)

### Styles
- Create **text styles** for all typography tokens
- Create **color styles** for fills and strokes
- Create **effect styles** for shadows

---

## 📦 FIGMA FILE ORGANIZATION TIPS

### Frame Naming
```
✅ GOOD: Desktop / Homepage / v1
❌ BAD: Frame 1234

✅ GOOD: Mobile / Upload Product / v2
❌ BAD: Upload Product - Mobile

✅ GOOD: Button / Primary / Default
❌ BAD: Primary Button
```

### Layer Naming
```
✅ GOOD: Hero Headline
❌ BAD: Text Layer

✅ GOOD: CTA Button
❌ BAD: Rectangle 5678

✅ GOOD: Product Image
❌ BAD: Image 1
```

### Component Organization
- Group related components in frames
- Use dividers (lines) to separate sections
- Add descriptions using text layers

---

## 🎨 VERSION CONTROL

### Versioning Pattern
```
v[Major].[Minor]

Examples:
- v1.0 (initial launch)
- v1.1 (minor updates)
- v2.0 (major redesign)
```

### When to Bump Version
- **Major (v2.0)**: Complete redesign, breaking changes
- **Minor (v1.1)**: New components, non-breaking updates

### Version Notes
Add version notes frame at top of each page:
```
Version 1.0
Released: December 23, 2025
Changes:
- Initial design system launch
- 52 components
- 6 app flows
- 8 marketing pages
```

---

## 📋 PRE-LAUNCH CHECKLIST

Before sharing Figma file with developers:

- [ ] All pages organized per structure above
- [ ] All components named using BEM-like pattern
- [ ] All design tokens imported as variables
- [ ] All text styles created
- [ ] All color styles created
- [ ] All effect styles (shadows) created
- [ ] Design QA checklist passed for all screens
- [ ] Annotations added for edge cases
- [ ] Prototypes tested and working
- [ ] File published to team library
- [ ] Dev handoff notes added
- [ ] Component status checklist updated

---

**Status:** 🟢 Ready for Implementation  
**Version:** 1.0.0  
**Last Updated:** December 23, 2025  
**Companion Files:**
- `design-tokens.json` (W3C format tokens)
- `FIGMA_COMPONENT_SPECS.md` (Component measurements)
- `UX_COPY_MICROSTATE_SPECS.md` (All copy and states)

🔥 **Organized. Consistent. Sovereign.** 👑
