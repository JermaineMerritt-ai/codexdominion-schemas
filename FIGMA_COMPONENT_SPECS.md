# FIGMA-READY COMPONENT SPECIFICATIONS
**CodexDominion Design System**  
**Version 1.0.0** | December 23, 2025

---

## 🎨 DESIGN TOKENS REFERENCE

### Color Tokens

#### Core Colors
```
color.primary.blue    → #003049   (Deep Caribbean Blue)
color.primary.gold    → #F2C94C   (Gold Accent)
color.primary.coral   → #FF6B6B   (Coral)
color.primary.teal    → #00A896   (Teal/Aqua)
```

#### Neutrals
```
color.neutral.white          → #FFFFFF
color.neutral.gray.light     → #E0E0E0
color.neutral.gray.medium    → #BDBDBD
color.neutral.gray.dark      → #4F4F4F
```

#### Semantic
```
color.semantic.success   → #00A896   (Teal)
color.semantic.warning   → #F2C94C   (Gold)
color.semantic.error     → #FF6B6B   (Coral)
color.semantic.info      → #003049   (Blue)
```

### Typography Tokens

#### Font Families
```
font.family.primary → Inter / SF-style sans-serif
```

#### Font Sizes
```
font.size.display   → 48px   (Hero headlines)
font.size.h1        → 32px   (Page titles)
font.size.h2        → 24px   (Section headings)
font.size.h3        → 20px   (Subsections)
font.size.body      → 16px   (Body text)
font.size.caption   → 14px   (Helper text)
font.size.overline  → 12px   (Labels, categories)
```

#### Font Weights
```
font.weight.bold      → 700
font.weight.semibold  → 600
font.weight.medium    → 500
font.weight.regular   → 400
```

### Spacing Tokens (8-pt grid)
```
space.1  → 4px    (Tight spacing)
space.2  → 8px    (Small gaps)
space.3  → 12px   (Default gap)
space.4  → 16px   (Base unit)
space.5  → 24px   (Section spacing)
space.6  → 32px   (Large gaps)
space.7  → 40px   (XL gaps)
space.8  → 48px   (XXL gaps)
space.9  → 64px   (Section breaks)
```

### Radius Tokens
```
radius.sm  → 4px    (Small corners)
radius.md  → 8px    (Buttons, inputs)
radius.lg  → 12px   (Cards)
radius.xl  → 20px   (Extra large)
```

### Shadow Tokens
```
shadow.sm  → 0 2px 8px rgba(0,0,0,0.08)    (Subtle lift)
shadow.md  → 0 4px 16px rgba(0,0,0,0.10)   (Card elevation)
shadow.lg  → 0 8px 24px rgba(0,0,0,0.12)   (Modal/overlay)
```

---

## 🔘 BUTTON COMPONENTS

### Primary Button

**Visual Specs:**
- **Fill**: `color.primary.gold` (#F2C94C)
- **Text**: `color.primary.blue` (#003049)
- **Font Size**: `font.size.body` (16px)
- **Font Weight**: `font.weight.semibold` (600)
- **Border Radius**: `radius.md` (8px)
- **Padding**: `space.3` vertical (12px), `space.4` horizontal (16px)
- **Shadow**: `shadow.sm` on default state

**States:**
| State | Behavior |
|-------|----------|
| **Default** | Solid gold fill, deep blue text |
| **Hover** | Brightness +10%, shadow increases to `shadow.md`, translateY(-1px) |
| **Pressed** | scale(0.97), shadow reduces |
| **Disabled** | 50% opacity, no hover effect, cursor not-allowed |

**Figma Auto Layout:**
- Direction: Horizontal
- Spacing: 8px (for icon + text)
- Padding: 12px vertical, 16px horizontal
- Resizing: Hug contents

**Usage:**
```
Primary CTAs: "Start Earning", "Create Account", "Publish Product"
```

---

### Secondary Button

**Visual Specs:**
- **Fill**: Transparent
- **Border**: 2px solid `color.primary.gold` (#F2C94C)
- **Text**: `color.primary.gold` (#F2C94C)
- **Font Size**: `font.size.body` (16px)
- **Font Weight**: `font.weight.semibold` (600)
- **Border Radius**: `radius.md` (8px)
- **Padding**: `space.3` vertical (12px), `space.4` horizontal (16px)

**States:**
| State | Behavior |
|-------|----------|
| **Default** | Transparent with gold border |
| **Hover** | Background: rgba(242, 201, 76, 0.1), border color intensifies |
| **Pressed** | scale(0.97) |
| **Disabled** | 50% opacity, no hover |

**Usage:**
```
Secondary actions: "Learn More", "View Details", "Cancel"
```

---

### Tertiary Button

**Visual Specs:**
- **Fill**: Transparent
- **Border**: None
- **Text**: `color.primary.coral` (#FF6B6B)
- **Font Size**: `font.size.body` (16px)
- **Font Weight**: `font.weight.medium` (500)
- **Border Radius**: None
- **Padding**: `space.2` vertical (8px), `space.3` horizontal (12px)

**States:**
| State | Behavior |
|-------|----------|
| **Default** | Text-only coral color |
| **Hover** | Underline appears, color darkens 10% |
| **Pressed** | scale(0.97) |

**Usage:**
```
Low-priority actions: "See all", "View profile", "Skip"
```

---

## 🃏 CARD COMPONENTS

### Creator Card

**Visual Specs:**
- **Width**: Auto (flexible, min 280px)
- **Background**: `color.neutral.white` (#FFFFFF)
- **Border Radius**: `radius.lg` (12px)
- **Shadow**: `shadow.md` (0 4px 16px rgba(0,0,0,0.10))
- **Padding**: `space.4` (16px)

**Structure (Top to Bottom):**
1. **Thumbnail** (Square ratio, 280x280px)
   - Border radius: `radius.md` (8px)
   
2. **Creator Name** (text.h3)
   - Font: `font.size.h3` (20px), `font.weight.semibold` (600)
   - Color: `color.primary.blue`
   - Margin top: `space.3` (12px)

3. **Product Title** (text.body)
   - Font: `font.size.body` (16px), `font.weight.regular` (400)
   - Color: `color.neutral.gray.dark`
   - Margin top: `space.2` (8px)

4. **Price** (text.h3)
   - Font: `font.size.h3` (20px), `font.weight.bold` (700)
   - Color: `color.primary.blue`
   - Margin top: `space.3` (12px)

5. **Category Pills** (horizontal flex)
   - Pill: `radius.md` (8px), padding: `space.1` vertical, `space.2` horizontal
   - Background: `color.primary.gold` with 20% opacity
   - Text: `font.size.caption` (14px), `color.primary.blue`
   - Margin top: `space.3` (12px)
   - Gap: `space.2` (8px)

**States:**
| State | Behavior |
|-------|----------|
| **Default** | Standard elevation |
| **Hover** | translateY(-4px), shadow increases to `shadow.lg`, border: 1px `color.primary.gold` |
| **Pressed** | scale(0.98) |

**Figma Auto Layout:**
- Direction: Vertical
- Spacing: Varies per element (see structure)
- Padding: 16px all sides
- Resizing: Hug contents vertically, Fixed/Fill horizontally

---

### Product Card

**Visual Specs:**
Same as Creator Card, plus:

**Additional Elements:**
- **"Promoted by youth" Micro-label**
  - Position: Top-right corner, absolute
  - Background: `color.primary.teal`
  - Text: `font.size.overline` (12px), `color.neutral.white`
  - Padding: `space.1` vertical, `space.2` horizontal
  - Border radius: `radius.sm` (4px)

---

### Leaderboard Row

**Visual Specs:**
- **Height**: 64px (fixed)
- **Background**: `color.neutral.white` (alternating rows use `color.neutral.gray.light` with 30% opacity)
- **Border Radius**: `radius.md` (8px)
- **Padding**: `space.3` (12px) horizontal
- **Shadow**: None (default), `shadow.sm` on hover

**Structure (Left to Right):**
1. **Rank Number** (48px circle)
   - Background: `color.neutral.gray.light`
   - Text: `font.size.h3` (20px), `font.weight.bold` (700)
   - Color: `color.primary.blue`
   
2. **Username** (flex-grow)
   - Font: `font.size.body` (16px), `font.weight.semibold` (600)
   - Color: `color.primary.blue`
   
3. **Earnings** (fixed width, 120px)
   - Font: `font.size.h3` (20px), `font.weight.bold` (700)
   - Color: `color.primary.gold`
   
4. **Badges** (horizontal flex, max 3 visible)
   - Size: 24x24px each
   - Gap: `space.1` (4px)

**Top 3 Special Styling:**
- **Rank 1-3**: Background gradient (gold to transparent)
- **Rank 1**: Gold glow effect, larger rank badge (64px)
- **Crown icon** appears next to rank 1

**States:**
| State | Behavior |
|-------|----------|
| **Default** | Standard row |
| **Hover** | Background lightens 5%, shadow.sm appears |
| **Rank-Up** | Animate upward 20px, pulse glow, toast notification |

---

## 📝 INPUT COMPONENTS

### Text Input

**Visual Specs:**
- **Height**: 44px (fixed)
- **Background**: `color.neutral.white`
- **Border**: 1px solid `color.neutral.gray.medium` (#BDBDBD)
- **Border Radius**: `radius.md` (8px)
- **Padding**: `space.3` (12px) horizontal
- **Font**: `font.size.body` (16px), `font.weight.regular` (400)
- **Placeholder Color**: `color.neutral.gray.medium` with 60% opacity

**States:**
| State | Behavior |
|-------|----------|
| **Default** | Gray border |
| **Focus** | Border: 2px `color.primary.gold`, soft glow (0 0 0 3px rgba(242,201,76,0.2)) |
| **Error** | Border: 2px `color.semantic.error`, text color: `color.semantic.error` |
| **Success** | Border: 2px `color.semantic.success` |
| **Disabled** | 50% opacity, cursor not-allowed |

**Label (above input):**
- Font: `font.size.caption` (14px), `font.weight.medium` (500)
- Color: `color.neutral.gray.dark`
- Margin bottom: `space.2` (8px)

**Helper Text (below input):**
- Font: `font.size.caption` (14px), `font.weight.regular` (400)
- Color: `color.neutral.gray.dark`
- Margin top: `space.1` (4px)

**Error Text (below input):**
- Font: `font.size.caption` (14px), `font.weight.regular` (400)
- Color: `color.semantic.error`
- Icon: ⚠️ prepended
- Margin top: `space.1` (4px)

---

## ✨ MOTION SYSTEM

### Duration Tokens
```
motion.duration.fast    → 150ms   (Button hovers, small UI changes)
motion.duration.medium  → 200ms   (Card animations, form states)
motion.duration.slow    → 300ms   (Page transitions, complex animations)
```

### Easing Tokens
```
motion.easing.enter  → cubic-bezier(0.16, 1, 0.3, 1)    (ease-out)
motion.easing.exit   → cubic-bezier(0.7, 0, 0.84, 0)    (ease-in)
```

---

## 🎬 MICRO-INTERACTIONS SPEC

### Button Interactions

**Primary Button Hover:**
```
Duration: 150ms
Easing: motion.easing.enter
Changes:
  - Brightness: +10%
  - Transform: translateY(-1px)
  - Shadow: shadow.sm → shadow.md
```

**Button Press:**
```
Duration: 100ms
Easing: motion.easing.exit
Changes:
  - Transform: scale(0.97)
  - Shadow: Reduces slightly
```

---

### Card Interactions

**Card Hover:**
```
Duration: 200ms
Easing: motion.easing.enter
Changes:
  - Transform: translateY(-4px)
  - Shadow: shadow.md → shadow.lg
  - Border: 1px solid color.primary.gold appears
```

---

### Leaderboard Rank-Up Animation

**Trigger:** When user's rank increases

**Animation Sequence:**
1. **Slide Up** (300ms)
   - Transform: translateY(20px) → translateY(0)
   - Easing: motion.easing.enter
   
2. **Pulse Glow** (400ms)
   - Background: Pulse gold gradient (fade in/out)
   - Loop: 2 times
   
3. **Toast Notification** (appears simultaneously)
   - Position: Bottom center
   - Text: "You just moved up! 🎉"
   - Duration: 3 seconds, auto-dismiss
   - Animation: Slide up from bottom (150ms)

**Figma Prototype:**
- After Delay: 0ms
- Navigate to: Same frame (with animation)
- Animation: Smart Animate
- Easing: Ease Out
- Duration: 300ms

---

### Badge Unlock Animation

**Trigger:** New badge earned

**Animation Sequence:**
1. **Scale In** (400ms)
   - Transform: scale(0.8) → scale(1.05) → scale(1.0)
   - Easing: motion.easing.enter (with overshoot)
   
2. **Glow Effect** (600ms)
   - Shadow: Soft gold glow behind badge
   - Opacity: 0 → 1 → 0
   - Loop: 1 time

**Figma Prototype:**
- After Delay: 0ms
- Animation: Smart Animate
- Easing: Spring (Bouncy, 10%)
- Duration: 400ms

---

### Sale Notification (Toast)

**Trigger:** Product sold

**Animation Sequence:**
1. **Slide In** (250ms)
   - Position: Slide from top-right
   - Transform: translateX(100%) → translateX(0)
   - Easing: motion.easing.enter
   
2. **Confetti Burst** (simultaneous)
   - Particle animation (optional in Figma)
   - Duration: 800ms
   
3. **Auto-Dismiss** (after 3 seconds)
   - Slide Out: translateX(0) → translateX(100%)
   - Duration: 200ms
   - Easing: motion.easing.exit

**Toast Specs:**
- Background: `color.primary.gold`
- Text: `color.primary.blue`
- Font: `font.size.body` (16px), `font.weight.semibold` (600)
- Padding: `space.3` vertical, `space.4` horizontal
- Border Radius: `radius.md` (8px)
- Shadow: `shadow.lg`
- Max Width: 400px

---

## 📱 RESPONSIVE BREAKPOINTS

```
Mobile:   320px - 767px
Tablet:   768px - 1023px
Desktop:  1024px+
```

**Grid Adjustments:**
- Mobile: 4 columns
- Tablet: 8 columns
- Desktop: 12 columns

**Gutter:**
- Mobile: 16px
- Tablet: 24px
- Desktop: 24px

---

## 🎨 FIGMA IMPORT INSTRUCTIONS

### Step 1: Create Variable Collections

1. In Figma, go to **Local Variables** panel
2. Create new collection: **"CodexDominion - Colors"**
3. Import color tokens from `design-tokens.json`
4. Repeat for Typography, Spacing, Radius, Shadow collections

### Step 2: Set Up Components

1. Create **Button** component set with variants:
   - Type: Primary, Secondary, Tertiary
   - State: Default, Hover, Pressed, Disabled
   - Size: Default, Large, Small

2. Create **Card** component set:
   - Type: Creator, Product
   - State: Default, Hover, Pressed

3. Create **Input** component set:
   - State: Default, Focus, Error, Success, Disabled

### Step 3: Apply Variables

- Use color variables for fills, borders, text
- Use spacing variables for padding, gaps
- Use radius variables for corner radius
- Use shadow variables for effects

### Step 4: Prototype Interactions

1. Add **Hover** interactions:
   - While hovering → Change to "Hover" variant
   - After delay: 0ms
   - Animation: Smart Animate, 150ms ease-out

2. Add **Press** interactions:
   - While pressing → Change to "Pressed" variant
   - Animation: Smart Animate, 100ms ease-in

3. Add **Rank-Up** animation:
   - After delay: 0ms
   - Animate: Smart Animate
   - Duration: 300ms, ease-out
   - Move: 20px upward

---

## 📋 COMPONENT STATUS CHECKLIST

| Component | Design | Tokens | Prototype | Status |
|-----------|--------|--------|-----------|--------|
| Primary Button | ✅ | ✅ | ✅ | Complete |
| Secondary Button | ✅ | ✅ | ✅ | Complete |
| Tertiary Button | ✅ | ✅ | ✅ | Complete |
| Creator Card | ✅ | ✅ | ✅ | Complete |
| Product Card | ✅ | ✅ | ✅ | Complete |
| Leaderboard Row | ✅ | ✅ | ✅ | Complete |
| Text Input | ✅ | ✅ | ✅ | Complete |
| Textarea | ✅ | ✅ | ⏳ | Pending |
| Select Dropdown | ✅ | ✅ | ⏳ | Pending |
| Checkbox | ✅ | ✅ | ⏳ | Pending |
| Radio Button | ⏳ | ⏳ | ⏳ | TODO |
| Toggle Switch | ⏳ | ⏳ | ⏳ | TODO |
| Badge | ✅ | ✅ | ✅ | Complete |
| Tag | ✅ | ✅ | ⏳ | Pending |
| Avatar | ✅ | ✅ | ⏳ | Pending |
| Modal | ⏳ | ⏳ | ⏳ | TODO |
| Tooltip | ⏳ | ⏳ | ⏳ | TODO |
| Toast Notification | ✅ | ✅ | ✅ | Complete |

---

**Status:** 🟢 Ready for Figma Import  
**Version:** 1.0.0  
**Last Updated:** December 23, 2025  
**Import File:** `design-tokens.json`

🔥 **The Flame Burns Sovereign and Eternal!** 👑
