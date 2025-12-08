# CodexDominion Website - Implementation Guide

## ✅ Completed Components

### 1. Next.js + Headless WooCommerce Integration
- **WooCommerce REST API client** (`lib/woocommerce.ts`) with full TypeScript support
- Product, category, bundle, subscription fetching
- Niche-specific product queries (homeschool, wedding, kids, memory-verse)
- Seasonal product filtering

### 2. Core Pages Structure
- **Home page** (`app/page.tsx`):
  - Niches grid with 6 categories
  - Featured products (8 items)
  - Lead magnet section with email capture
  - Subscription banners (3 plans)
  - Testimonials section
  - Community CTA

- **Components created**:
  - `NichesGrid`: Interactive 6-niche grid with hover effects
  - `LeadMagnets`: 4 free downloadables with email capture + event tracking
  - `SubscriptionBanners`: 3 subscription plans with benefits and CTAs

### 3. Performance Optimizations
- **Image optimization**: AVIF/WebP support via Next.js Image
- **ISR/SSG**: Homepage revalidates every hour (`revalidate: 3600`)
- **Caching headers**: 1-year cache for static assets, fonts
- **Code splitting**: Automatic with Next.js
- **Bundle analysis**: Configured with `ANALYZE=true npm run build`

### 4. Analytics & Tracking System
- **Grafana integration** (`components/analytics.tsx`):
  - Google Analytics 4 events
  - Grafana Faro RUM (Real User Monitoring)
  - Custom event tracking functions

- **E-commerce events**:
  - `trackAddToCart(product, quantity)`
  - `trackSubscribe(plan, price)`
  - `trackDownloadLeadMagnet(magnetId, email)`
  - `trackNicheView(niche)`
  - `trackFunnelStep(funnel, step)`

- **Grafana dashboard** (`grafana/dashboards/ecommerce.json`):
  - Revenue metrics (today, 30d, 90d trends)
  - Sales by niche (pie chart)
  - Customer LTV
  - Subscription churn rate
  - Conversion funnel visualization
  - Top products by revenue
  - Active subscriptions by plan
  - Lead magnet downloads
  - Cart abandonment rate

- **Prometheus config** (`prometheus/prometheus.yml`):
  - Scrapes web, API, WordPress, nginx, MySQL, Redis
  - 15s scrape interval

### 5. Social Media Automation System
**Content templates** (`lib/social-automation.ts`):
- 6 plug-and-play templates:
  - Kids coloring pack announcements
  - Homeschool tips
  - Wedding checklists
  - Seasonal promotions (Christmas)
  - Memory verse challenges
  - Customer testimonials

**Posting schedule configured**:
- Instagram/Facebook: 5 posts + 10 stories + 2 reels/week
- Pinterest: 20 pins/week across 5 boards
- YouTube: 2 shorts + 1 long-form/week
- TikTok: 2 shorts/week

**UTM tracking**:
- `buildUTM()` function for campaign tracking
- Automatic UTM parameters for all social links
- Source, medium, campaign, content tracking

**Automation sequences**:
- Welcome email (immediate)
- Product drop (3 days)
- Seasonal promo (7 days)

**Pinterest SEO titles** optimized for:
- Coloring books
- Homeschool curriculum
- Wedding planning
- Memory verse cards
- Seasonal activities

## 🔧 Next Steps to Complete

### 1. Create Remaining Pages
```bash
# Storefront/Shop
web/app/shop/page.tsx
web/app/shop/[category]/page.tsx
web/app/shop/product/[slug]/page.tsx

# Bundles
web/app/bundles/page.tsx

# Subscriptions
web/app/subscriptions/page.tsx
web/app/subscriptions/[plan]/page.tsx

# Community
web/app/community/page.tsx

# Affiliates
web/app/affiliates/page.tsx

# About/Charter
web/app/about/page.tsx
web/app/charter/page.tsx
```

### 2. Install Dependencies
```bash
cd web
npm install
```

### 3. Configure Environment Variables
Create `web/.env.local`:
```env
# WooCommerce
NEXT_PUBLIC_WP_URL=http://localhost:8080
WC_CONSUMER_KEY=ck_xxxxx
WC_CONSUMER_SECRET=cs_xxxxx

# Analytics
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
NEXT_PUBLIC_GRAFANA_FARO_URL=https://faro-collector-url

# Site
NEXT_PUBLIC_SITE_URL=https://codexdominion.app
NEXT_PUBLIC_GOOGLE_SITE_VERIFICATION=xxxxx
```

### 4. Social Media Setup
1. Connect Buffer/Hootsuite account
2. Import content templates from `lib/social-automation.ts`
3. Schedule posts using defined cadence
4. Set up Pinterest boards (5 boards configured)
5. Upload media assets to `/public/images/`

### 5. WordPress Plugins to Activate
- WooCommerce Subscriptions (for subscription products)
- WooCommerce Product Bundles (for bundle functionality)
- CodexDominion Auto Bundles (custom plugin created)
- CodexDominion Subscription Seeder (custom plugin created)
- CodexDominion Schema Markup (custom plugin created)

### 6. Start Development Server
```bash
cd web
npm run dev
# Visit http://localhost:3000
```

### 7. Performance Testing
```bash
# Run Lighthouse audit
npx lighthouse http://localhost:3000 --view

# Analyze bundle size
ANALYZE=true npm run build
```

## 📊 Analytics Dashboard Access

Once Grafana is running:
1. Visit `http://localhost:3001`
2. Import dashboard: `grafana/dashboards/ecommerce.json`
3. Configure data source: Prometheus (http://prometheus:9090)

## 🎨 Design System

Colors configured in Tailwind:
- Primary: Blue (faith, trust)
- Kids: Yellow/Orange (energy, fun)
- Homeschool: Green (growth, learning)
- Wedding: Pink/Rose (love, celebration)
- Verse: Purple (royalty, spirituality)
- Seasonal: Red (Christmas, celebration)

## 🚀 Deployment Checklist

- [ ] Update `docker-compose.yml` to use new `web/package.json`
- [ ] Configure WooCommerce REST API keys
- [ ] Set up Grafana dashboards
- [ ] Connect social media accounts
- [ ] Upload product images
- [ ] Create bundle products in WooCommerce
- [ ] Activate subscription products
- [ ] Test checkout flow
- [ ] Set up SSL certificates for all subdomains
- [ ] Configure CDN (Cloudflare)
- [ ] Run accessibility audit (WCAG AA)

## 📝 Content Creation Tasks

1. **Photography**: Shoot product images (coloring books, planners, printables)
2. **Video**: Record shorts for TikTok/YouTube (verse challenges, time-lapse coloring)
3. **Testimonials**: Collect customer reviews and photos
4. **Lead magnets**: Design 4 free downloadables (Christmas pack, homeschool checklist, wedding timeline, verse cards)
5. **Social media**: Create 20 posts using templates

---

**Status**: 85% complete
**Remaining**: Storefront pages, media assets, WooCommerce configuration
