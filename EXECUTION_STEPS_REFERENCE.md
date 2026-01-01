# 🎬 Website Creation Execution Steps - Quick Reference

## Overview
When a `website.create_basic_site` workflow is created, it goes through these stages:

```
CREATE → ROUTE → ENQUEUE → EXECUTE → DEPLOY → REVIEW → COMPLETE
```

---

## Step-by-Step Execution

### Step 0: Workflow Creation (User/Agent)
```python
workflow_id = workflow_engine.create_workflow(
    workflow_type_id="website.create_basic_site",
    created_by_agent="agent_jermaine",
    inputs={
        "site_name": "My Site",
        "site_description": "Description",
        "pages": ["home", "about", "contact"],
        "brand_colors": {...},
        "contact_email": "hello@example.com"
    },
    calculated_savings={"weekly_savings": 225},
    auto_route_councils=True  # Automatic council routing
)
```

**Output:**
```
🎯 Auto-routed to media council
   Required councils: media
   Triggers: media_keywords_detected
✅ Created workflow: wf_abc123 (type: website.create_basic_site)
📋 Enqueued workflow wf_abc123 as job rq:job:xyz789
```

---

### Step 1-2: Generate Site Structure & Content (30-120s)

**Function:** `generate_site_content()`

**Inputs:**
- site_name: "Codex Digital Studios"
- description: "AI-powered web development"
- pages: ["home", "about", "services", "contact", "blog"]

**Outputs:**
```json
{
  "pages": [
    {
      "slug": "home",
      "title": "Home",
      "sections": [
        {
          "type": "hero",
          "heading": "Welcome to Codex Digital Studios",
          "subheading": "AI-powered web development",
          "cta": {"text": "Get Started", "link": "/contact"}
        },
        {
          "type": "features",
          "items": [
            {"title": "Quality Service", "description": "..."},
            {"title": "Expert Team", "description": "..."}
          ]
        }
      ]
    },
    {...}
  ],
  "navigation": [
    {"label": "Home", "href": "/"},
    {"label": "About", "href": "/about"}
  ]
}
```

**What Happens:**
- AI analyzes site purpose and generates appropriate sections
- Hero sections for home page
- Text sections for about/services
- Contact forms
- Blog indexes
- Navigation structure built automatically

---

### Step 3: Generate SEO Metadata (45s)

**Function:** `generate_seo_metadata()`

**Outputs:**
```json
{
  "base": {
    "title": "Codex Digital Studios",
    "description": "AI-powered web development...",
    "keywords": ["codex digital studios", "website"],
    "ogImage": "/og-image.png"
  },
  "pages": {
    "home": {
      "title": "Home | Codex Digital Studios",
      "description": "...",
      "path": "/"
    },
    "about": {...}
  },
  "sitemap": {
    "pages": [
      {"path": "/", "priority": 1.0},
      {"path": "/about", "priority": 0.8}
    ]
  },
  "robots": "User-agent: *\nAllow: /\nSitemap: /sitemap.xml"
}
```

**What Happens:**
- Meta tags for each page
- OpenGraph tags for social sharing
- Twitter card configuration
- Sitemap.xml structure
- robots.txt rules

---

### Step 4: Generate Brand Theme (60s)

**Function:** `generate_brand_theme()`

**Inputs:**
```json
{
  "brand_colors": {
    "primary": "#1a1a1a",
    "secondary": "#f7f1e3",
    "accent": "#d4af37"
  },
  "typography": {
    "heading": "Inter",
    "body": "Open Sans"
  }
}
```

**Outputs:**
```css
:root {
  --color-primary: #1a1a1a;
  --color-secondary: #f7f1e3;
  --color-accent: #d4af37;
  
  --font-heading: 'Inter', sans-serif;
  --font-body: 'Open Sans', sans-serif;
  
  --container-width: 1280px;
  --section-padding: 80px;
}
```

**What Happens:**
- CSS variables created
- Tailwind config generated
- Component styling applied
- Responsive breakpoints set

---

### Step 5: Generate Next.js Project (120s)

**Function:** `generate_nextjs_project()`

**Creates:**
```
codex-digital-studios/
├── package.json
├── next.config.js
├── tsconfig.json
├── tailwind.config.js
├── app/
│   ├── layout.tsx
│   ├── page.tsx (home)
│   ├── globals.css
│   ├── about/
│   │   └── page.tsx
│   ├── services/
│   │   └── page.tsx
│   ├── contact/
│   │   └── page.tsx
│   └── blog/
│       └── page.tsx
└── public/
    ├── robots.txt
    └── sitemap.xml
```

**package.json:**
```json
{
  "name": "codex-digital-studios",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "export": "next build && next export"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0"
  }
}
```

**What Happens:**
- Complete Next.js 14 project structure
- TypeScript configuration
- App router pages for each section
- Styled components with brand theme
- Static export configuration
- Ready to deploy

---

### Step 6: Deploy to GitHub (60s)

**Function:** `deploy_to_github_and_vercel()` (Part 1)

**Commands (simulated in MVP, real in production):**
```bash
cd codex-digital-studios
git init
git add .
git commit -m "Initial commit: AI-generated website"
gh repo create codexdominion/codex-digital-studios --public
git push -u origin main
```

**Output:**
```json
{
  "repo_url": "https://github.com/codexdominion/codex-digital-studios"
}
```

**What Happens:**
- Git repository initialized
- Code committed
- GitHub repo created via API
- Code pushed to main branch
- Repo becomes source of truth

---

### Step 7: Deploy to Vercel (120s)

**Function:** `deploy_to_github_and_vercel()` (Part 2)

**Commands (simulated in MVP, real in production):**
```bash
vercel --prod
```

**Output:**
```json
{
  "site_url": "https://codex-digital-studios.vercel.app",
  "deployment_id": "deploy_1703098765"
}
```

**What Happens:**
- Vercel CLI or API called
- Next.js project built
- Static files generated
- Deployed to CDN
- SSL certificate auto-provisioned
- Live URL returned

---

### Step 8: Record Metrics & Complete (30s)

**Function:** `execute_website_creation()` (Finalization)

**Workflow Updated:**
```json
{
  "status": "COMPLETED",
  "completed_at": "2025-12-20T15:45:30Z",
  "outputs": {
    "site_url": "https://codex-digital-studios.vercel.app",
    "pages_created": [
      "https://codex-digital-studios.vercel.app/",
      "https://codex-digital-studios.vercel.app/about",
      "https://codex-digital-studios.vercel.app/services",
      "https://codex-digital-studios.vercel.app/contact",
      "https://codex-digital-studios.vercel.app/blog"
    ],
    "asset_urls": {
      "project_directory": "/generated_sites/codex-digital-studios",
      "github_repo": "https://github.com/codexdominion/codex-digital-studios"
    },
    "deployment_id": "deploy_1703098765",
    "decision": "approved",
    "execution_summary": {
      "pages_generated": 5,
      "duration_seconds": 525,
      "status": "success"
    }
  }
}
```

**Metrics Recorded:**
```json
{
  "workflow_id": "wf_abc123",
  "duration_seconds": 525,
  "estimated_weekly_savings": 225,
  "success_rate": 1.0,
  "error_count": 0
}
```

**What Happens:**
- Workflow status → COMPLETED
- Outputs stored in database
- Metrics recorded
- Agent notified
- User notified
- Council review requested (if configured)

---

## Total Execution Time

| Step | Duration | Status |
|------|----------|--------|
| 1. Site Structure | 30s | ✅ |
| 2. Content Generation | 120s | ✅ |
| 3. SEO Metadata | 45s | ✅ |
| 4. Brand Theme | 60s | ✅ |
| 5. Next.js Project | 120s | ✅ |
| 6. GitHub Deploy | 60s | ✅ |
| 7. Vercel Deploy | 120s | ✅ |
| 8. Finalization | 30s | ✅ |
| **TOTAL** | **~9 minutes** | **✅** |

**Manual equivalent:** 3+ hours  
**Savings:** 85% time reduction  
**Cost savings:** $225/week ($11,700/year)

---

## Error Handling

### Execution Failures

**If Step 3 fails (SEO generation):**
```python
workflow.status = WorkflowStatus.FAILED
workflow.outputs = {
    "error": "SEO metadata generation failed",
    "failed_at_step": 3,
    "completed_steps": ["structure", "content"]
}
metric.success_rate = 0.0
metric.error_count = 1
```

**User sees:**
```
❌ Workflow failed at Step 3: SEO Metadata Generation
✅ Completed: Site structure, Content generation
📋 You can retry or modify inputs
```

### Partial Success

**If deployment fails but site is generated:**
```python
workflow.status = WorkflowStatus.PARTIALLY_COMPLETED
workflow.outputs = {
    "project_directory": "/generated_sites/...",
    "github_repo": "https://github.com/...",
    "site_url": null,  # Deploy failed
    "deployment_error": "Vercel API timeout"
}
```

**User sees:**
```
⚠️  Website generated but deployment failed
✅ Project ready at: /generated_sites/codex-digital-studios
✅ Code pushed to: https://github.com/codexdominion/codex-digital-studios
❌ Vercel deployment timed out
📋 You can manually deploy or retry
```

---

## Monitoring Execution

### Real-time Status

```bash
# Get workflow status
curl http://localhost:5000/api/workflows/wf_abc123

# Response shows current step
{
  "status": "IN_PROGRESS",
  "current_step": "Generating SEO metadata...",
  "progress": "3/7 steps completed"
}
```

### RQ Worker Logs

```bash
rq worker workflows --verbose
```

**Output:**
```
[2025-12-20 15:42:10] Processing workflow wf_abc123
[2025-12-20 15:42:12] Step 1/7: Generate site structure
[2025-12-20 15:42:15] ✅ Structure generated (5 pages)
[2025-12-20 15:42:15] Step 2/7: Generate content
[2025-12-20 15:43:20] ✅ Content generated
[2025-12-20 15:43:20] Step 3/7: Generate SEO metadata
[2025-12-20 15:44:05] ✅ SEO metadata complete
...
[2025-12-20 15:50:30] ✅ Workflow completed successfully
```

---

## Council Review (Post-Execution)

After execution completes, council members review:

```
WORKFLOW REVIEW: wf_abc123
==========================

EXECUTION RESULTS:
✅ Site deployed: https://codex-digital-studios.vercel.app
✅ 5 pages generated
✅ SEO metadata complete
✅ Brand theme applied
✅ Accessibility score: 95/100

REVIEW CHECKLIST:
☐ Brand consistency
☐ Content quality
☐ SEO implementation
☐ Accessibility compliance
☐ Mobile responsiveness

APPROVE / DENY / REQUEST CHANGES
```

---

## 🔥 Quick Commands

**Create website:**
```bash
python -c "from workflow_engine import workflow_engine; workflow_engine.create_workflow('website.create_basic_site', 'agent_jermaine', {'site_name': 'Test Site', 'pages': ['home']}, {'weekly_savings': 225})"
```

**Check status:**
```bash
curl http://localhost:5000/api/workflows/wf_abc123
```

**Start worker:**
```bash
rq worker workflows
```

**Test locally:**
```bash
python website_creation_worker.py
```

🔥 **The site factory is operational!**
