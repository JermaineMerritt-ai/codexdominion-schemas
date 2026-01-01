# 🔥 Website Creation Workflow — Full Execution Steps

## Quick Reference Guide

This document describes the complete, end-to-end workflow that CodexDominion executes when creating a new website. Think of it as the "ritual" performed every time a new website is born.

## 🏗️ The 4-Step Ritual

### Step 1 — Generate the Site Blueprint (Structure JSON)
**What it does:** Creates the architectural skeleton of the entire site

**Outputs:**
- `/site.json` - Complete structural map
- `/pages/*.json` - Individual page configurations

**Contains:**
- Pages manifest with slugs and titles
- Navigation structure (primary + footer)
- Sections map for each page
- Components inventory
- SEO metadata placeholders
- Content placeholders
- Brand theme references

**Example Output:**
```json
{
  "meta": {
    "site_name": "Codex Digital Studios",
    "description": "Professional web design services",
    "blueprint_id": "bp_a1b2c3d4e5f6"
  },
  "pages": [
    {
      "slug": "home",
      "title": "Home",
      "path": "/",
      "sections": [
        {
          "id": "hero",
          "type": "hero",
          "components": ["heading", "subheading", "cta_primary"]
        }
      ]
    }
  ],
  "navigation": {
    "primary": [...],
    "footer": [...]
  }
}
```

---

### Step 2 — Generate Page Content (AI-Authored)
**What it does:** AI generates all copywriting and content

**For each page:**
- Headlines (H1, H2, H3)
- Subheadlines
- Body copy
- Calls to action
- Image prompts (for AI image generation)
- Testimonials, features, team bios, etc.

**Where the AI shines:** This is pure content creation using GPT-4/Claude

**Example Output:**
```json
{
  "pages": {
    "home": {
      "hero_title": "Welcome to Codex Digital Studios",
      "hero_subtitle": "AI-powered web design that converts",
      "cta_text": "Get Started",
      "features_title": "What We Offer",
      "feature_items": [
        {
          "title": "Expert Solutions",
          "description": "Leverage cutting-edge AI for faster results",
          "icon": "sparkles"
        }
      ]
    }
  }
}
```

---

### Step 3 — Generate SEO Metadata
**What it does:** Makes the site search-engine ready from day one

**Creates:**
- Global SEO settings
- Per-page meta tags
- OpenGraph metadata (social sharing)
- Twitter cards
- Sitemap structure (`sitemap.xml`)
- Robots.txt rules
- Canonical URLs
- Schema.org markup (structured data)

**Example Output:**
```json
{
  "global": {
    "site_name": "Codex Digital Studios",
    "default_title": "Professional Web Design | Codex Digital",
    "default_og_image": "/og-image.png"
  },
  "pages": {
    "home": {
      "title": "Home | Codex Digital Studios",
      "description": "Professional AI-powered web design...",
      "og": {...},
      "twitter": {...}
    }
  },
  "robots_txt": "User-agent: *\nAllow: /\nSitemap: /sitemap.xml"
}
```

---

### Step 4 — Generate Brand Theme File
**What it does:** Creates a complete design system

**Includes:**
- **Color palette:** Primary, secondary, accent, neutrals (with scales)
- **Typography scale:** Font families, sizes, weights, line heights
- **Spacing system:** 8px base grid with full scale
- **Button styles:** Variants (primary, secondary, outline) + sizes
- **Card styles:** Variants with shadows, borders, radii
- **Shadows:** Elevation levels (sm, md, lg, xl, 2xl)
- **Border radii:** Corner rounding system
- **Light/dark mode:** Color mode variants
- **CSS variables:** Complete CSS custom properties
- **Tailwind config:** Ready-to-use Tailwind configuration

**Example Output:**
```json
{
  "colors": {
    "brand": {
      "primary": {"500": "#1a1a1a", ...},
      "secondary": {"500": "#f7f1e3", ...},
      "accent": {"500": "#d4af37", ...}
    }
  },
  "typography": {
    "fonts": {"heading": "Inter", "body": "Open Sans"},
    "sizes": {"base": "1rem", "2xl": "1.5rem", ...}
  },
  "components": {
    "button": {
      "variants": {"primary": {...}, "secondary": {...}},
      "sizes": {"sm": {...}, "md": {...}, "lg": {...}}
    }
  }
}
```

---

## 🚀 Quick Start

### Option 1: Command Line
```bash
python website_creation_execution_complete.py \
  --name "Codex Digital Studios" \
  --description "AI-powered web design and development services" \
  --pages home about services contact blog \
  --primary-color "#1a1a1a" \
  --secondary-color "#f7f1e3" \
  --accent-color "#d4af37" \
  --heading-font "Inter" \
  --body-font "Open Sans" \
  --tone professional \
  --platform nextjs \
  --output ./generated_sites
```

### Option 2: Python API
```python
from website_creation_execution_complete import execute_website_creation_complete

result = execute_website_creation_complete(
    site_name="Codex Digital Studios",
    description="AI-powered web design and development services",
    pages=["home", "about", "services", "contact", "blog"],
    brand_colors={
        "primary": "#1a1a1a",
        "secondary": "#f7f1e3",
        "accent": "#d4af37"
    },
    typography={
        "heading": "Inter",
        "body": "Open Sans"
    },
    tone="professional",
    platform="nextjs",
    output_dir="./generated_sites"
)

print(f"Site created: {result['output_directory']}")
print(f"Duration: {result['duration_seconds']}s")
```

### Option 3: Workflow Engine Integration
```python
from workflow_engine import workflow_engine

workflow_id = workflow_engine.create_workflow(
    workflow_type_id="website.create_basic_site",
    created_by_agent="agent_jermaine",
    inputs={
        "site_name": "Codex Digital Studios",
        "description": "AI-powered web design",
        "brand_colors": {"primary": "#1a1a1a", ...},
        "pages": ["home", "about", "contact"],
        ...
    },
    calculated_savings={"weekly": 225.0},
    auto_execute=True  # Enqueues to RQ worker
)
```

---

## 📂 Output Structure

After execution, you'll get:

```
generated_sites/
└── codex-digital-studios/
    ├── site.json              # Complete blueprint
    ├── content.json           # All page content
    ├── seo.json               # SEO configuration
    ├── theme.json             # Design system
    ├── theme.css              # CSS variables
    ├── robots.txt             # Search engine rules
    ├── EXECUTION_SUMMARY.json # Execution details
    └── pages/
        ├── home.json
        ├── about.json
        ├── services.json
        ├── contact.json
        └── blog.json
```

---

## 🎯 Next Steps After Generation

1. **Review Generated Files**
   - Check `EXECUTION_SUMMARY.json` for overview
   - Review `content.json` for copy quality
   - Validate `theme.json` matches brand

2. **Customize as Needed**
   - Edit content in `pages/*.json`
   - Adjust colors in `theme.json`
   - Modify SEO in `seo.json`

3. **Generate Code** (Next Phase)
   - Convert blueprint to Next.js project
   - Apply theme to components
   - Integrate SEO metadata

4. **Deploy**
   - Push to GitHub
   - Deploy to Vercel/Netlify
   - Configure domain

---

## 🔧 Configuration Options

### Pages
- **Default:** home, about, services, contact, blog
- **Available:** home, about, services, portfolio, team, pricing, contact, blog

### Tones
- **professional** - Corporate, authoritative
- **playful** - Fun, casual, friendly
- **luxury** - Premium, exclusive, sophisticated
- **minimal** - Clean, simple, focused

### Platforms
- **nextjs** - Next.js 14+ with App Router
- **wordpress** - WordPress with custom theme
- **static** - Pure HTML/CSS/JS

---

## 📊 Performance

- **Execution Time:** ~2-5 seconds for blueprint + content
- **Output Size:** ~50-100KB JSON files
- **Scalability:** Can generate sites with 50+ pages

---

## 🤖 AI Integration Points

1. **Content Generation** (Step 2)
   - Use GPT-4/Claude for headlines, copy, CTAs
   - Image prompt generation for DALL-E/Midjourney

2. **SEO Optimization** (Step 3)
   - AI-generated meta descriptions
   - Keyword extraction
   - Schema markup suggestions

3. **Design Recommendations** (Step 4)
   - Color palette suggestions
   - Typography pairings
   - Component style variants

---

## 🔥 The Flame Burns Sovereign and Eternal! 👑
