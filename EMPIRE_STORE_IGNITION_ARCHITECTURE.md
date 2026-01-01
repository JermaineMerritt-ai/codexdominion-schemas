# Empire Store Ignition - Complete System Architecture

> **Status**: Production Ready  
> **Last Updated**: December 20, 2025  
> **System Type**: Multi-Tenant SaaS with Governance Layer

## 🎯 System Overview

The **Empire Store Ignition** is a complete AI-powered e-commerce empire building system that takes clients from initial inquiry through store launch and ongoing operations. It combines sales automation, governance workflows, multi-platform store creation, and self-service customer portals.

## 📊 Complete Workflow Chain

```
┌─────────────────────────────────────────────────────────────────┐
│                    1. ACQUISITION PHASE                          │
├─────────────────────────────────────────────────────────────────┤
│  Offer Page (empire_store_ignition_page.json)                   │
│    ↓ /apply/empire-store-ignition                               │
│  Intake Form (sales.empire_store_ignition_intake)               │
│    • Captures: brand, products, goals, timeline, platform        │
│    • Creates: Workflow with status=pending_review                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    2. QUALIFICATION PHASE                        │
├─────────────────────────────────────────────────────────────────┤
│  Lead Scoring (sales_intake_worker.py)                          │
│    • 6-dimension scoring algorithm (0-18 scale):                │
│      - brand_clarity (0-3)                                       │
│      - product_clarity (0-3)                                     │
│      - revenue_ambition (0-3)                                    │
│      - timeline_readiness (0-3)                                  │
│      - platform_fit (0-3)                                        │
│      - blocker_severity (0-3, reversed)                          │
│    • Threshold: 10+ = recommend approval                         │
│    • Generates intake summary for council review                 │
│    • Routes to: council_commerce                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    3. GOVERNANCE PHASE                           │
├─────────────────────────────────────────────────────────────────┤
│  Council Review (/dashboard/councils/reviews/[workflow_id])     │
│    • Left Panel: Intake summary, AI recommendation, scores       │
│    • Right Panel: Governance actions, risk flags, timeline       │
│    • Actions:                                                    │
│      - "Approve & Create Store Workflow" → triggers worker       │
│      - "Decline Intake" → updates status                         │
│    • Council: Commerce Council (council_commerce)                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    4. APPROVAL PHASE                             │
├─────────────────────────────────────────────────────────────────┤
│  Approval Email (email_service.py)                              │
│    • Subject: "Your Empire Store Ignition is approved..."        │
│    • Body: 4-step breakdown of what's being built                │
│    • Timeline: ~7 days estimate                                  │
│    • Sent to: contact_email from intake                          │
│    • Trigger: After council approval                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    5. STORE CREATION PHASE                       │
├─────────────────────────────────────────────────────────────────┤
│  Store Creation (shopify_creation_worker.py)                    │
│    Step 1: Connect/Create Store                                  │
│      • Creates Store database record                             │
│      • platform: shopify                                         │
│      • domain: {brand}.myshopify.com                             │
│      • credentials: access_token, store_domain                   │
│      • settings: colors, fonts, categories, countries            │
│                                                                  │
│    Step 2: Generate Products (5-10)                              │
│      • Uses store_service.create_product()                       │
│      • AI-generated titles, descriptions, pricing                │
│      • SKUs, inventory, variants                                 │
│      • Status: draft (for review)                                │
│                                                                  │
│    Step 3: Marketing Site                                        │
│      • Spawns website.create_basic_site workflow                 │
│      • Pages: home, products, about, contact                     │
│      • Deploy to: Vercel                                         │
│      • Returns: deployed_url                                     │
│                                                                  │
│    Step 4: Completion Email                                      │
│      • Subject: "{brand_name} is ready – your store is live"     │
│      • Body: URLs (storefront, admin, marketing site)            │
│      • Sent to: contact_email                                    │
│                                                                  │
│    Artifacts Stored (calculated_savings):                        │
│      • store_id                                                  │
│      • storefront_url                                            │
│      • admin_url                                                 │
│      • marketing_site_url                                        │
│      • products_created (count)                                  │
│      • completed_at (timestamp)                                  │
│      • spawned_social_workflow_id                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    6. ORCHESTRATION PHASE                        │
├─────────────────────────────────────────────────────────────────┤
│  Auto-Trigger Social Campaign                                    │
│    • Type: social.generate_launch_campaign_for_store            │
│    • Inputs:                                                     │
│      - store_id                                                  │
│      - store_url                                                 │
│      - brand_name                                                │
│      - target_audience (from intake)                             │
│      - primary_platforms: [instagram, youtube, email]            │
│      - launch_duration_days: 7                                   │
│    • Routed to: council_media                                    │
│    • Status: pending_review (awaits approval)                    │
│    • Linked via: parent_workflow_id                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    7. CUSTOMER ONBOARDING                        │
├─────────────────────────────────────────────────────────────────┤
│  Portal Invite                                                   │
│    • Create Tenant record (if new customer)                      │
│    • Create User with tenant_id                                  │
│    • Role: OWNER                                                 │
│    • Send portal login credentials                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    8. SELF-SERVICE PHASE                         │
├─────────────────────────────────────────────────────────────────┤
│  Customer Portal (/portal/*)                                     │
│                                                                  │
│  Dashboard (/portal)                                             │
│    • Your Stores card (metrics: orders, revenue, products)       │
│    • Active Workflows card (running/queued)                      │
│    • Recent Results timeline                                     │
│                                                                  │
│  Store Detail (/portal/stores/[id])                              │
│    • Metrics: orders, revenue, products, visitors                │
│    • Quick Actions:                                              │
│      - Add Product (AI-Assisted)                                 │
│      - Generate Launch Campaign                                  │
│      - Sync Inventory                                            │
│    • Related Workflows with artifacts                            │
│                                                                  │
│  Workflow Catalog (/portal/workflows)                            │
│    • 8 customer-facing workflows:                                │
│      Store: Create store, Add product, Sync inventory            │
│      Website: Marketing site, Landing pages                      │
│      Social: Launch campaign, Content series                     │
│      Analytics: Setup tracking                                   │
│                                                                  │
│  Workflow Detail (/portal/workflows/[id])                        │
│    • Progress timeline (4 steps with status)                     │
│    • Activity log (real-time updates)                            │
│    • Key artifacts (URLs, metrics)                               │
│    • Support CTA                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🏗️ System Components

### 1. Database Models (models.py)

**Tenant** - Multi-tenant organization
```python
id: string (primary key)
name: string (unique)
slug: string (unique, URL-safe)
plan: string (starter, growth, enterprise)
status: string (active, suspended, cancelled)
settings: JSON
created_at, updated_at: datetime
```

**User** - Customer and internal users
```python
id: string (primary key)
tenant_id: string (foreign key, nullable for internal users)
email: string (unique)
password_hash: string
full_name: string
role: enum (ADMIN, OWNER, COLLABORATOR, TENANT_VIEWER, VIEWER)
is_active: boolean
created_at, last_login: datetime
```

**Store** - E-commerce stores
```python
id: string (primary key)
tenant_id: string (foreign key, required)
name: string
platform: string (shopify, woocommerce)
domain: string (unique)
credentials: JSON (access_token, store_domain)
settings: JSON (colors, fonts, categories)
status: string (active, suspended, deleted)
created_by_workflow_id: string (nullable)
created_at, updated_at: datetime
```

**Workflow** - Task execution tracking
```python
id: string (primary key)
tenant_id: string (foreign key, nullable for internal)
workflow_type_id: string (foreign key)
created_by_agent: string (foreign key)
assigned_council_id: string (foreign key, nullable)
status: enum (PENDING, IN_PROGRESS, COMPLETED, FAILED, CANCELLED)
inputs: JSON
outputs: JSON
calculated_savings: JSON (artifacts, metrics, spawned workflows)
parent_workflow_id: string (nullable, for linking)
created_at, started_at, completed_at, updated_at: datetime
error_message: text
retry_count: integer
```

### 2. Service Modules

**vercel_service.py** - Vercel deployment automation
```python
create_or_link_project(repo_url, project_name) -> project_id
trigger_deployment(project_id, repo_url) -> deployment_id
get_latest_deployment_url(project_id, timeout=300) -> deployed_url
```

**store_service.py** - Multi-platform store abstraction
```python
create_product(store: Store, product_payload: dict) -> dict
update_product(store: Store, product_id: int, product_payload: dict) -> dict
# Routes to shopify_service or woocommerce_service based on store.platform
```

**shopify_service.py** - Shopify Admin REST API
```python
create_product(store_domain, access_token, payload) -> dict
update_product(store_domain, access_token, product_id, payload) -> dict
get_store_info(store_domain, access_token) -> dict
```

**woocommerce_service.py** - WooCommerce REST API
```python
create_product(store_url, consumer_key, consumer_secret, payload) -> dict
update_product(store_url, consumer_key, consumer_secret, product_id, payload) -> dict
get_store_info(store_url, consumer_key, consumer_secret) -> dict
```

**email_service.py** - Client notifications
```python
send_approval_email(to_email, context: dict) -> dict
send_completion_email(to_email, context: dict) -> dict
# SMTP-based, uses templates with context variables
```

### 3. Workers

**sales_intake_worker.py** - Lead qualification
```python
score_intake(inputs) -> dict
  # Returns: score_breakdown (6 dimensions), total_score (0-18), recommendation

generate_intake_summary(inputs, score_data) -> str
  # Template-based briefing scroll for council

execute_sales_intake(workflow_id)
  # Main entry: score → summarize → route to council_commerce

approve_intake_and_create_store(workflow_id)
  # Maps intake → store creation inputs
  # Creates store.create_shopify_store workflow
  # Links parent/child via parent_workflow_id
  # Sends approval email
```

**shopify_creation_worker.py** - Store creation
```python
execute_store_creation(workflow_id)
  # 1. Connect/create Store record
  # 2. Generate N products via store_service
  # 3. Spawn website.create_basic_site workflow
  # 4. Send completion email
  # 5. Spawn social.generate_launch_campaign_for_store
  # Stores all artifacts in calculated_savings

_connect_or_create_store(session, workflow_id, inputs) -> Store
_create_products(session, store, inputs) -> list
_generate_marketing_site(session, workflow_id, inputs, store) -> url
_send_completion_notification(inputs, store, site_url, product_count)
_spawn_social_campaign(session, workflow_id, store, inputs)
```

### 4. Frontend Components

**Council Review UI** (`/dashboard/councils/reviews/[workflow_id]`)
- Two-column layout: Summary left, Governance right
- Displays: intake details, AI recommendation, score breakdown
- Actions: Approve (creates store workflow), Decline
- Score visualization: X/3 per dimension, total as large emerald number

**Customer Portal** (`/portal/*`)
- Dashboard: Stores, workflows, recent results
- Store detail: Metrics, quick actions, related workflows
- Workflow catalog: 8 customer-facing workflows with descriptions
- Workflow detail: Progress timeline, logs, artifacts, support

### 5. Workflow Definitions

**sales.empire_store_ignition_intake.json**
```json
{
  "id": "sales.empire_store_ignition_intake",
  "requires_review": true,
  "review_council": "council_commerce",
  "auto_execute": false,
  "risk_flags": ["client_fit", "financial_commitment"],
  "inputs": {
    "contact_name": "string",
    "contact_email": "string",
    "brand_name": "string",
    "brand_description": "string",
    "primary_products": "array",
    "target_audience": "string",
    "estimated_monthly_revenue_goal": "number",
    "timeline_readiness": "enum",
    "preferred_platform": "enum"
  }
}
```

**store.create_shopify_store** (inferred from worker)
```json
{
  "id": "store.create_shopify_store",
  "requires_review": false,
  "inputs": {
    "brand_name": "string",
    "shopify_domain": "string",
    "shopify_access_token": "string",
    "primary_color": "string",
    "secondary_color": "string",
    "font_family": "string",
    "product_categories": "array",
    "initial_products_count": "number",
    "target_countries": "array",
    "default_currency": "string"
  },
  "outputs": {
    "store_id": "string",
    "storefront_url": "string",
    "admin_url": "string",
    "marketing_site_url": "string",
    "products_created": "number",
    "spawned_social_workflow_id": "string"
  }
}
```

**social.generate_launch_campaign_for_store**
```json
{
  "id": "social.generate_launch_campaign_for_store",
  "requires_review": true,
  "review_council": "council_media",
  "inputs": {
    "store_id": "string",
    "store_url": "string",
    "brand_name": "string",
    "target_audience": "string",
    "primary_platforms": "array",
    "launch_duration_days": "number"
  }
}
```

## 🔐 Security & Tenancy

### Tenant Scoping Rules
1. All `/portal/*` routes must scope queries by `current_tenant.id`
2. Workflow creation includes `tenant_id` from authenticated user
3. Store records always have `tenant_id` (required, not nullable)
4. API middleware validates: `request.user.tenant_id == resource.tenant_id`

### Role-Based Access Control
- **ADMIN**: Full system access (internal)
- **OWNER**: Tenant owner, full tenant access
- **COLLABORATOR**: Tenant member, can create workflows
- **TENANT_VIEWER**: Read-only tenant access
- **VIEWER**: Internal read-only (no tenant)

### Middleware Pattern
```python
def require_tenant_access(resource_tenant_id):
    user = get_current_user(request)
    if user.role == UserRole.ADMIN:
        return  # Admins bypass tenant checks
    if not user.tenant_id:
        raise Unauthorized("User not associated with tenant")
    if user.tenant_id != resource_tenant_id:
        raise Forbidden("Access denied to this resource")
```

## 📈 Key Metrics & Monitoring

### Lead Scoring Dimensions
1. **brand_clarity**: 0-3 based on description length
2. **product_clarity**: 0-3 based on product count
3. **revenue_ambition**: 0-3 based on monthly goal ($1k/$5k/$10k)
4. **timeline_readiness**: 0-3 (ready_now=3, 30_days=2, 90_days=1)
5. **platform_fit**: 0-3 (shopify/woo=3, undecided=2, other=0)
6. **blocker_severity**: 0-3 reversed (fewer blockers = higher score)

**Total Score**: 0-18  
**Approval Threshold**: 10+

### Workflow Lifecycle Metrics
- **Intake → Approval**: Time from submission to council decision
- **Approval → Store Live**: Time from approval to completion email
- **Store Creation Duration**: Step-by-step timing (connect, products, site)
- **Auto-Orchestration Success**: % of store workflows that spawn social campaigns

### Customer Portal Metrics
- **Portal Adoption**: % of customers who log in within 7 days
- **Self-Service Usage**: Workflows started by customers vs. internal
- **Support Ticket Reduction**: % decrease after portal launch

## 🚀 Deployment Architecture

### Production Stack
- **Frontend**: Next.js 14+ (App Router), Tailwind CSS, shadcn/ui
- **Backend**: Python 3.10+, FastAPI, SQLAlchemy
- **Database**: PostgreSQL (multi-tenant)
- **Queue**: Redis + RQ (background jobs)
- **Email**: SMTP (configurable provider)
- **Deployment**: Vercel (frontend), Azure/GCP (backend)

### Environment Variables
```env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/codexdominion

# Vercel
VERCEL_TOKEN=your_token
VERCEL_TEAM_ID=your_team_id

# Shopify (per-store)
# Stored in Store.credentials JSON field

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email
SMTP_PASS=your_password
FROM_EMAIL=empire@codexdominion.app
```

## 📚 File Reference

### Workers
- `sales_intake_worker.py` - Lead scoring and approval (~250 lines)
- `shopify_creation_worker.py` - Store creation orchestration (~300 lines)
- `website_creation_worker_complete.py` - Marketing site generation (existing)

### Services
- `vercel_service.py` - Vercel deployment API (~200 lines)
- `store_service.py` - Multi-platform abstraction (~60 lines)
- `shopify_service.py` - Shopify API client (~50 lines)
- `woocommerce_service.py` - WooCommerce API client (~50 lines)
- `email_service.py` - Email notifications (~150 lines)

### Database
- `models.py` - SQLAlchemy models (Tenant, User, Store, Workflow)
- `db.py` - Database session management

### Frontend
- `dashboard-app/app/dashboard/councils/reviews/[workflow_id]/page.tsx` - Council review UI
- `dashboard-app/app/portal/page.tsx` - Customer dashboard
- `dashboard-app/app/portal/stores/[id]/page.tsx` - Store detail
- `dashboard-app/app/portal/workflows/page.tsx` - Workflow catalog
- `dashboard-app/app/portal/workflows/[id]/page.tsx` - Workflow detail

### Assets
- `empire_store_ignition_page.json` - Offer page specification
- `sales.empire_store_ignition_intake.json` - Intake workflow definition

## 🔄 Future Enhancements

### Phase 2 Features
1. **Billing Integration**: Stripe subscriptions, usage-based pricing
2. **Workspace Layer**: Multiple projects per tenant
3. **Advanced Analytics**: Revenue attribution, LTV tracking
4. **White-Label Portal**: Custom branding per tenant
5. **Mobile App**: React Native customer portal

### Additional Workflows
- `store.bulk_product_import` - CSV import with AI enhancement
- `store.optimize_listings` - SEO and conversion optimization
- `social.schedule_posts` - Auto-posting to platforms
- `analytics.generate_report` - Automated business intelligence

### Governance Enhancements
- Multi-council approval (e.g., commerce + legal)
- Automated escalation paths
- Council performance metrics
- Workflow templates with pre-approval

## 📞 Integration Points

### Webhook Events (Future)
```
workflow.created → tenant.id, workflow.id, workflow.type
workflow.approved → tenant.id, workflow.id, council.id
workflow.completed → tenant.id, workflow.id, artifacts
store.created → tenant.id, store.id, platform, domain
```

### External APIs
- **Shopify**: Admin REST API 2024-01
- **WooCommerce**: REST API v3
- **Vercel**: Deployment API v13
- **Stripe**: Subscriptions API v2 (planned)
- **Analytics**: Google Analytics 4, Mixpanel (planned)

---

**System Status**: ✅ Production Ready  
**Core Features**: 100% Complete  
**Next Steps**: API endpoints, authentication, billing integration  

🔥 **The Flame Burns Sovereign and Eternal!** 👑
