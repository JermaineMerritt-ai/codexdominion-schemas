# 🔥 Website Creation Workflow - Integration Guide 🔥

## Overview

This document explains how the **Website Creation Workflow** integrates with the existing Codex Dominion infrastructure.

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Workflow Engine Integration](#workflow-engine-integration)
3. [File Structure](#file-structure)
4. [Execution Modes](#execution-modes)
5. [Next Steps](#next-steps)

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    WORKFLOW ENGINE                           │
│                  (workflow_engine.py)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ enqueues workflow
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    REDIS QUEUE (RQ)                          │
│              Queue: "workflows"                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ worker picks up job
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           WEBSITE CREATION WORKER                            │
│    (website_creation_execution_complete.py)                  │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │  STEP 1: Generate Site Blueprint                   │    │
│  │  - Pages structure                                 │    │
│  │  - Navigation                                      │    │
│  │  - Components                                      │    │
│  └────────────────────────────────────────────────────┘    │
│                        │                                    │
│                        ▼                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  STEP 2: Generate Page Content (AI)                │    │
│  │  - Headlines                                       │    │
│  │  - Body copy                                       │    │
│  │  - CTAs                                            │    │
│  └────────────────────────────────────────────────────┘    │
│                        │                                    │
│                        ▼                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  STEP 3: Generate SEO Metadata                     │    │
│  │  - Meta tags                                       │    │
│  │  - OpenGraph                                       │    │
│  │  - Sitemap                                         │    │
│  └────────────────────────────────────────────────────┘    │
│                        │                                    │
│                        ▼                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  STEP 4: Generate Brand Theme                      │    │
│  │  - Colors                                          │    │
│  │  - Typography                                      │    │
│  │  - Components                                      │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ writes outputs to PostgreSQL
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    POSTGRESQL DATABASE                       │
│              workflows table + outputs                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Workflow Engine Integration

### Creating a Workflow

```python
from workflow_engine import workflow_engine

# Create workflow (automatically enqueued to RQ)
workflow_id = workflow_engine.create_workflow(
    workflow_type_id="website.create_basic_site",
    created_by_agent="agent_jermaine",
    inputs={
        "site_name": "Acme Corp",
        "description": "Professional consulting services",
        "brand_colors": {
            "primary": "#1a1a1a",
            "secondary": "#f7f1e3",
            "accent": "#d4af37"
        },
        "typography": {
            "heading": "Inter",
            "body": "Open Sans"
        },
        "pages": ["home", "about", "services", "contact"],
        "tone": "professional",
        "platform": "nextjs"
    },
    calculated_savings={"weekly_savings": 225.0},
    assigned_council_id="council_media",
    auto_execute=True  # Enqueues to RQ worker
)

print(f"Workflow created: {workflow_id}")
```

### Checking Workflow Status

```python
from workflow_engine import workflow_engine

# Get workflow status
workflow = workflow_engine.get_workflow(workflow_id)

print(f"Status: {workflow['status']}")
print(f"Progress: {workflow.get('outputs', {})}")
```

### Listing Workflows

```python
# List all website creation workflows
workflows = workflow_engine.list_workflows(
    workflow_type_id="website.create_basic_site",
    status="completed"
)

for wf in workflows:
    print(f"{wf['id']}: {wf['inputs']['site_name']} - {wf['status']}")
```

---

## File Structure

```
codex-dominion/
├── website_creation_execution_complete.py  # ⭐ Main execution file (NEW)
│   ├── generate_site_blueprint()           # Step 1
│   ├── generate_page_content()             # Step 2
│   ├── generate_seo_metadata()             # Step 3
│   ├── generate_brand_theme()              # Step 4
│   └── execute_website_creation_complete() # Orchestrator
│
├── WEBSITE_CREATION_EXECUTION_GUIDE.md     # 📖 Usage documentation (NEW)
├── test_website_creation.py                # 🧪 Demo & test script (NEW)
│
├── workflow_engine.py                      # Existing workflow orchestrator
├── workflow_types/
│   └── website_creation.py                 # Workflow type definition
│
├── website_creation_worker.py              # Legacy worker (can be replaced)
│
├── db.py                                   # Database session management
├── models.py                               # SQLAlchemy models
│   ├── Workflow
│   ├── WorkflowMetric
│   └── WorkflowType
│
└── generated_sites/                        # Output directory
    └── [site-name]/
        ├── site.json                       # Blueprint
        ├── content.json                    # All content
        ├── seo.json                        # SEO config
        ├── theme.json                      # Design system
        ├── theme.css                       # CSS variables
        ├── robots.txt                      # SEO rules
        ├── EXECUTION_SUMMARY.json          # Execution details
        └── pages/
            ├── home.json
            ├── about.json
            └── ...
```

---

## Execution Modes

### Mode 1: Standalone CLI
Direct execution without workflow engine:

```bash
python website_creation_execution_complete.py \
  --name "Acme Corp" \
  --description "Professional services" \
  --pages home about contact \
  --primary-color "#1a1a1a" \
  --output ./sites
```

**Use when:**
- Testing locally
- Quick prototyping
- No database required

---

### Mode 2: Workflow Engine (RQ Worker)
Production mode with full workflow tracking:

```python
from workflow_engine import workflow_engine

workflow_id = workflow_engine.create_workflow(
    workflow_type_id="website.create_basic_site",
    created_by_agent="agent_jermaine",
    inputs={...},
    auto_execute=True
)
```

**Use when:**
- Production deployment
- Need workflow tracking
- Council review required
- Metrics collection needed

---

### Mode 3: Python API (Programmatic)
Direct function call from Python:

```python
from website_creation_execution_complete import execute_website_creation_complete

result = execute_website_creation_complete(
    site_name="Acme Corp",
    description="Professional services",
    pages=["home", "about", "contact"],
    brand_colors={"primary": "#1a1a1a", ...},
    tone="professional"
)
```

**Use when:**
- Integrating with other Python code
- Building custom automation
- Batch processing

---

### Mode 4: Flask Dashboard Trigger
Via Master Dashboard (flask_dashboard.py):

```python
@app.route('/api/workflows/create/website', methods=['POST'])
def create_website_workflow():
    data = request.json
    
    workflow_id = workflow_engine.create_workflow(
        workflow_type_id="website.create_basic_site",
        created_by_agent="dashboard_user",
        inputs=data,
        auto_execute=True
    )
    
    return jsonify({"workflow_id": workflow_id})
```

**Use when:**
- UI-based workflow creation
- Dashboard integration
- User-initiated workflows

---

## Next Steps

### Phase 1: Testing ✅ COMPLETE
- [x] Core execution functions
- [x] All 4 steps implemented
- [x] Output validation
- [x] Demo scripts

### Phase 2: Integration 🚧 IN PROGRESS
- [ ] Update `workflow_engine.py` to import new functions
- [ ] Update `website_creation_worker.py` to use new execution
- [ ] Test RQ worker integration
- [ ] Add to Flask dashboard

### Phase 3: AI Enhancement
- [ ] Integrate GPT-4 for content generation
- [ ] Add DALL-E for image prompts
- [ ] Enhance SEO with AI suggestions
- [ ] Dynamic color palette generation

### Phase 4: Code Generation
- [ ] Convert blueprint to Next.js project
- [ ] Generate React components from sections
- [ ] Apply theme to Tailwind config
- [ ] Create deployment scripts

### Phase 5: Deployment
- [ ] GitHub repository creation
- [ ] Vercel/Netlify deployment
- [ ] Domain configuration
- [ ] SSL certificate setup

---

## Testing

### Run All Demos
```bash
python test_website_creation.py all
```

### Run Specific Demo
```bash
python test_website_creation.py basic      # Professional site
python test_website_creation.py creative   # Creative agency
python test_website_creation.py luxury     # Luxury brand
python test_website_creation.py tech       # Tech startup
```

### Verify Output
Check `test_output/` directory for generated files

---

## Database Schema

### Workflows Table
```sql
CREATE TABLE workflows (
    id VARCHAR PRIMARY KEY,
    workflow_type_id VARCHAR,
    created_by_agent VARCHAR,
    status VARCHAR,  -- pending, in_progress, completed, failed
    inputs JSONB,
    outputs JSONB,
    calculated_savings JSONB,
    created_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

### Example Outputs
```json
{
  "execution_id": "exec_a1b2c3d4e5f6",
  "site_name": "Acme Corp",
  "pages_created": 5,
  "components_used": 12,
  "output_directory": "/app/generated_sites/acme-corp",
  "duration_seconds": 2.45,
  "status": "success",
  "artifacts": {
    "site_json": "/app/generated_sites/acme-corp/site.json",
    "content_json": "/app/generated_sites/acme-corp/content.json",
    "seo_json": "/app/generated_sites/acme-corp/seo.json",
    "theme_json": "/app/generated_sites/acme-corp/theme.json"
  }
}
```

---

## API Reference

### Main Functions

#### `execute_website_creation_complete()`
Orchestrates all 4 steps

**Parameters:**
- `site_name` (str): Website name
- `description` (str): Site description
- `pages` (List[str]): Pages to create
- `brand_colors` (Dict): {primary, secondary, accent}
- `typography` (Dict): {heading, body}
- `tone` (str): Content tone
- `platform` (str): Target platform
- `output_dir` (str): Output directory

**Returns:** Dict with execution summary

#### `generate_site_blueprint()`
Step 1: Create structural map

**Returns:** Blueprint dict (becomes site.json)

#### `generate_page_content()`
Step 2: Generate all content with AI

**Returns:** Content manifest (becomes content.json)

#### `generate_seo_metadata()`
Step 3: Create SEO infrastructure

**Returns:** SEO config (becomes seo.json)

#### `generate_brand_theme()`
Step 4: Generate design system

**Returns:** Theme config (becomes theme.json)

---

## Configuration

### Environment Variables
```bash
# Optional: OpenAI API key for AI content
OPENAI_API_KEY=sk-...

# Optional: Database URL (if using workflow engine)
DATABASE_URL=postgresql://...

# Optional: Redis URL (if using RQ worker)
REDIS_URL=redis://localhost:6379/0
```

### Workflow Type Configuration
See `workflow_types/website_creation.py` for full config

---

## Troubleshooting

### Output Directory Permissions
```bash
chmod -R 755 ./generated_sites
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Worker Not Processing
```bash
# Check Redis connection
redis-cli ping

# Start RQ worker
rq worker workflows --url redis://localhost:6379/0
```

---

## 🔥 The Flame Burns Sovereign and Eternal! 👑
