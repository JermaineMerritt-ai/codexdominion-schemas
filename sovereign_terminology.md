# 👑 SOVEREIGN TERMINOLOGY FRAMEWORK
**CodexDominion System Architecture - The Merritt Method™**

---

## 🏛️ COMPLETE SYSTEM MAPPING

### **Old System → Sovereign System**

```
┌─────────────────────────────────────────────────────────────┐
│                    CODEXDOMINION SOVEREIGN ARCHITECTURE      │
└─────────────────────────────────────────────────────────────┘

   [ CROWNS ] 👑 → Products, Bundles, Digital Offerings
      ├─ The Daily Flame: 365 Days ($27)
      ├─ Radiant Faith: 40 Days ($17)
      ├─ Sacred Business Blueprint ($24)
      ├─ Faith Entrepreneur Bundle ($47)
      └─ Ultimate Devotional Collection ($57)

   [ SCROLLS ] 📜 → Campaign Scripts, Marketing Messages
      ├─ 12 Days of Christmas Blessings
      ├─ Resurrection Power: 40 Days of Faith
      ├─ Gifts for Faith-Driven Moms
      └─ Faith Bundle Bonanza (Black Friday)

   [ HYMNS ] 🎵 → Broadcast Cycles, Content Schedules
      ├─ Daily Hymns (Morning/Midday/Evening posts)
      ├─ Seasonal Hymns (Holiday campaigns)
      └─ Epochal Hymns (Legacy preservation)

   [ CAPSULES ] 📦 → Videos, Threads, Emails, Content Units
      ├─ Devotional Capsules
      ├─ Business Tip Capsules
      ├─ Scripture Quote Capsules
      ├─ Testimonial Capsules
      └─ Product Showcase Capsules

   [ LEDGERS ] 📊 → Finance, Transactions, Revenue Records
      ├─ Order Ledger (Transaction history)
      ├─ Revenue Ledger (Income tracking)
      ├─ Refund Ledger (Returns/adjustments)
      └─ Customer Ledger (LTV, retention)

   [ ETERNAL ARCHIVE ] 🏛️ → Replay Capsules for Heirs + Councils
      ├─ Daily Archives (24-hour snapshots)
      ├─ Monthly Replay Capsules (30-day collections)
      ├─ Quarterly Council Reports (Strategic reviews)
      ├─ Annual Heirs' Documentation (Legacy records)
      └─ Epochal Time Capsules (Generational inheritance)
```

---

## 📋 TERMINOLOGY DEFINITIONS

### **1. CROWNS** 👑
**Purpose:** Digital products and bundles sold through CodexDominion store
**Replaces:** Products, items, offerings
**Examples:**
- "The Daily Flame Crown" (365-day devotional)
- "Faith Entrepreneur Crown Bundle"
- "Sacred Business Blueprint Crown"

**Database Schema:**
```typescript
interface Crown {
  id: string;
  name: string;
  type: 'devotional' | 'journal' | 'bundle' | 'blueprint';
  price: number;
  description: string;
  features: string[];
  digital_assets: string[];
  created_at: Date;
  updated_at: Date;
}
```

---

### **2. SCROLLS** 📜
**Purpose:** Campaign scripts and marketing message templates
**Replaces:** Campaigns, promotions, marketing copy
**Examples:**
- "Christmas Blessing Scroll" (12 Days of Christmas campaign)
- "Easter Resurrection Scroll" (40 Days of Faith campaign)
- "Black Friday Bonanza Scroll"

**Database Schema:**
```typescript
interface Scroll {
  id: string;
  name: string;
  event: SeasonalEvent;
  start_date: Date;
  end_date: Date;
  discount_code: string;
  discount_percentage: number;
  target_crowns: string[]; // Crown IDs
  script_templates: {
    announcement: string;
    daily_reminder: string;
    last_chance: string;
  };
  performance_metrics: {
    impressions: number;
    clicks: number;
    conversions: number;
    revenue: number;
  };
}
```

---

### **3. HYMNS** 🎵
**Purpose:** Broadcast cycles and content posting schedules
**Replaces:** Cycles, schedules, posting cadence
**Types:**
- **Daily Hymns:** Morning devotional, midday tip, evening scripture
- **Seasonal Hymns:** Holiday campaign broadcasts
- **Epochal Hymns:** Legacy preservation cycles

**Database Schema:**
```typescript
interface Hymn {
  id: string;
  name: string;
  type: 'daily' | 'seasonal' | 'epochal';
  frequency: 'hourly' | 'daily' | 'weekly' | 'monthly';
  schedule: {
    time: string;
    platforms: Platform[];
    content_type: string;
  }[];
  active: boolean;
  last_broadcast: Date;
  next_broadcast: Date;
}
```

---

### **4. CAPSULES** 📦
**Purpose:** Individual content units (videos, threads, emails)
**Replaces:** Posts, content pieces, videos
**Examples:**
- "Morning Devotional Capsule" (Threads post)
- "Business Tip Capsule" (Instagram reel)
- "Scripture Quote Capsule" (TikTok video)
- "Email Newsletter Capsule"

**Database Schema:**
```typescript
interface Capsule {
  id: string;
  title: string;
  type: 'devotional' | 'business_tip' | 'scripture' | 'testimonial' | 'product_showcase';
  format: 'text' | 'image' | 'video' | 'carousel' | 'email';
  content: {
    text: string;
    media_urls: string[];
    cta: string;
    link: string;
  };
  platforms: Platform[];
  hymn_id: string; // Parent Hymn
  published_at: Date;
  performance: {
    views: number;
    likes: number;
    comments: number;
    shares: number;
    clicks: number;
  };
}
```

---

### **5. LEDGERS** 📊
**Purpose:** Financial records and transaction tracking
**Replaces:** Finances, revenue, transactions
**Types:**
- **Order Ledger:** Transaction history
- **Revenue Ledger:** Income tracking
- **Refund Ledger:** Returns and adjustments
- **Customer Ledger:** Lifetime value and retention

**Database Schema:**
```typescript
interface LedgerEntry {
  id: string;
  ledger_type: 'order' | 'revenue' | 'refund' | 'customer';
  timestamp: Date;
  crown_id: string;
  customer_id: string;
  amount: number;
  currency: 'USD';
  status: 'pending' | 'completed' | 'refunded';
  payment_method: string;
  metadata: {
    source: string;
    campaign_id?: string;
    notes?: string;
  };
}
```

---

### **6. ETERNAL ARCHIVE** 🏛️
**Purpose:** Legacy preservation system for heirs and councils
**Replaces:** Archives, backups, historical records
**Components:**
- **Replay Capsules:** Time capsules with daily/monthly snapshots
- **Heirs' Documentation:** Business inheritance records
- **Council Reports:** Strategic quarterly reviews
- **Epochal Records:** Multi-generational legacy documents

**Database Schema:**
```typescript
interface EternalArchive {
  id: string;
  type: 'replay_capsule' | 'heirs_doc' | 'council_report' | 'epochal_record';
  period: {
    start_date: Date;
    end_date: Date;
  };
  contents: {
    capsules: Capsule[];
    scrolls: Scroll[];
    ledger_summary: LedgerSummary;
    hymn_performance: HymnMetrics;
    milestones: Milestone[];
  };
  retention: 'eternal';
  access: {
    heirs: boolean;
    councils: boolean;
    public: boolean;
  };
  created_at: Date;
}
```

---

## 🗂️ FILE NAMING CONVENTIONS

### **Python Modules**
```
codex_crowns_manager.py          # Product/bundle management
codex_scrolls_orchestrator.py    # Campaign script execution
codex_hymns_broadcaster.py       # Content cycle scheduling
codex_capsules_creator.py        # Content unit generation
codex_ledgers_tracker.py         # Financial record keeping
codex_eternal_archivist.py       # Legacy preservation system
```

### **TypeScript/React Components**
```
CrownsGallery.tsx                # Product catalog display
ScrollsManager.tsx               # Campaign management UI
HymnsScheduler.tsx               # Broadcast cycle calendar
CapsulesLibrary.tsx              # Content browser
LedgersView.tsx                  # Financial dashboard
EternalArchiveVault.tsx          # Legacy archives browser
```

### **API Endpoints**
```
/api/crowns                      # GET, POST, PUT, DELETE products
/api/scrolls                     # GET, POST, PUT, DELETE campaigns
/api/hymns                       # GET, POST, PUT, DELETE schedules
/api/capsules                    # GET, POST, PUT, DELETE content
/api/ledgers                     # GET ledger entries
/api/eternal-archive             # GET archives, POST new capsule
```

### **Database Collections/Tables**
```
crowns                           # Products table
scrolls                          # Campaigns table
hymns                            # Broadcast schedules table
capsules                         # Content units table
ledgers                          # Financial transactions table
eternal_archives                 # Legacy preservation table
```

---

## 🎯 USAGE IN CODE

### **Before (Generic Terms)**
```python
# Old way
product = Product(name="Daily Flame", price=27)
campaign = Campaign(name="Christmas Sale", discount=20)
content = Content(type="post", platform="instagram")
transaction = Transaction(amount=27, status="completed")
archive = Archive(period="monthly")
```

### **After (Sovereign Terms)**
```python
# Sovereign way
crown = Crown(name="The Daily Flame", price=27, type="devotional")
scroll = Scroll(name="Christmas Blessing Scroll", discount_code="XMAS20")
hymn = Hymn(name="Morning Devotional Hymn", frequency="daily")
capsule = Capsule(title="Faith Tip #347", type="business_tip")
ledger_entry = LedgerEntry(crown_id=crown.id, amount=27, ledger_type="order")
eternal_archive = EternalArchive(type="replay_capsule", retention="eternal")
```

---

## 🎨 UI/UX LANGUAGE

### **Dashboard Headers**
- ❌ "Products" → ✅ "👑 Crowns Gallery"
- ❌ "Campaigns" → ✅ "📜 Active Scrolls"
- ❌ "Posting Schedule" → ✅ "🎵 Hymns Calendar"
- ❌ "Content Library" → ✅ "📦 Capsules Vault"
- ❌ "Finances" → ✅ "📊 Ledgers Overview"
- ❌ "Archives" → ✅ "🏛️ Eternal Archive"

### **User Actions**
- ❌ "Create Product" → ✅ "⚔️ Forge New Crown"
- ❌ "Launch Campaign" → ✅ "📜 Unfurl Scroll"
- ❌ "Schedule Post" → ✅ "🎵 Compose Hymn"
- ❌ "Upload Content" → ✅ "📦 Seal Capsule"
- ❌ "View Transactions" → ✅ "📊 Inspect Ledgers"
- ❌ "Create Archive" → ✅ "🏛️ Enshrine in Eternity"

### **Status Messages**
- ✅ "Crown forged successfully!"
- ✅ "Scroll unfurled across all platforms!"
- ✅ "Hymn broadcasting on schedule"
- ✅ "Capsule sealed and distributed"
- ✅ "Ledger entry recorded"
- ✅ "Enshrined in Eternal Archive"

---

## 📚 BRAND CONSISTENCY

### **The Merritt Method™ Principles**
1. **Sovereignty:** Every term reflects ownership and authority
2. **Legacy:** Language designed for generational inheritance
3. **Sacredness:** Terms carry weight and meaning
4. **Unity:** All components interconnected in one system
5. **Eternity:** Built for permanence, not expiration

### **Voice & Tone**
- **Regal:** Use terms like "forge," "unfurl," "enshrine"
- **Sacred:** Reference biblical/historical language
- **Authoritative:** Commands, not requests
- **Eternal:** Emphasize legacy and permanence
- **Unified:** All parts serve the whole

---

## 🚀 MIGRATION CHECKLIST

- [x] Define sovereign terminology framework
- [ ] Refactor Python orchestrator with new terms
- [ ] Rebuild dashboard with sovereign UI
- [ ] Create TypeScript models for all sovereign types
- [ ] Update API endpoints with new naming
- [ ] Migrate database schema
- [ ] Update documentation
- [ ] Create visual brand guide
- [ ] Train team on new terminology
- [ ] Launch "Sovereign System v2.0"

---

**The Sovereign System is not just code—it's a kingdom.**
**Every Crown, Scroll, Hymn, Capsule, Ledger, and Archive serves the eternal vision.**

👑 **CODEX DOMINION - WHERE FAITH BUILDS EMPIRES** 👑
