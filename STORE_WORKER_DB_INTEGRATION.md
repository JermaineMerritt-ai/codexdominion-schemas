# Store Creation Worker - Database Integration Guide

> **Purpose**: Exact field mapping for `shopify_creation_worker.py` to populate database models  
> **Last Updated**: December 20, 2025

## Overview

This guide specifies exactly how the store creation worker should populate the `Store` and `WorkflowArtifact` models when execution completes.

## 1. Store Model Population

When creating the Store record in `_connect_or_create_store()`:

```python
from models import Store

store = Store(
    # Identity
    id=f"store_{workflow_id[:8]}",  # Short UUID from workflow
    tenant_id=workflow.tenant_id,  # From parent workflow
    
    # Core fields
    name=inputs["brand_name"],
    platform="shopify",  # Hardcoded for v1
    domain=inputs.get("shopify_domain") or f"{inputs['brand_name'].lower().replace(' ', '-')}.myshopify.com",
    
    # URLs (populated after verification)
    storefront_url=f"https://{domain}",  # After store connection verified
    admin_url=f"https://{domain}/admin",
    
    # Credentials (encrypted in production)
    access_token=inputs.get("shopify_access_token"),
    owner_email=inputs.get("contact_email"),
    
    # Settings
    settings={
        "primary_color": inputs.get("primary_color", "#F5C542"),
        "secondary_color": inputs.get("secondary_color", "#10B981"),
        "font_family": inputs.get("font_family", "Inter"),
        "product_categories": inputs.get("product_categories", []),
        "target_countries": inputs.get("target_countries", ["US"]),
        "default_currency": inputs.get("default_currency", "USD")
    },
    
    # Status
    status="pending_setup",  # Initial status
    created_via_workflow_id=workflow_id,
    
    # Timestamps (auto-managed by SQLAlchemy)
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)

session.add(store)
session.commit()
```

### Status Transitions

Update `store.status` as workflow progresses:

```python
# After store connection verified
store.status = "active"
session.commit()

# If any step fails
store.status = "error"
session.commit()
```

## 2. WorkflowArtifact Creation

Create artifacts after each major step completes. This keeps URLs and metadata separate from the workflow row.

### Import

```python
from models import WorkflowArtifact
from datetime import datetime
```

### Artifact Creation Pattern

```python
def create_artifact(session, workflow_id, tenant_id, kind, label, value):
    """Helper to create workflow artifacts"""
    artifact = WorkflowArtifact(
        id=f"artifact_{datetime.utcnow().timestamp()}",
        workflow_id=workflow_id,
        tenant_id=tenant_id,
        kind=kind,
        label=label,
        value=value,
        created_at=datetime.utcnow()
    )
    session.add(artifact)
    return artifact
```

### Artifacts to Create

After **Step 1: Store Connection**:

```python
create_artifact(
    session=session,
    workflow_id=workflow_id,
    tenant_id=workflow.tenant_id,
    kind="storefront_url",
    label="Storefront URL",
    value=f"https://{store.domain}"
)

create_artifact(
    session=session,
    workflow_id=workflow_id,
    tenant_id=workflow.tenant_id,
    kind="admin_url",
    label="Admin Dashboard",
    value=f"https://{store.domain}/admin"
)

session.commit()
```

After **Step 2: Product Creation**:

```python
# After all products created
create_artifact(
    session=session,
    workflow_id=workflow_id,
    tenant_id=workflow.tenant_id,
    kind="product_count",
    label="Products Created",
    value=str(len(created_products))
)

# Optional: Store product list as JSON
create_artifact(
    session=session,
    workflow_id=workflow_id,
    tenant_id=workflow.tenant_id,
    kind="product_list",
    label="Product Catalog",
    value=json.dumps([{
        "id": p["id"],
        "title": p["title"],
        "handle": p["handle"]
    } for p in created_products])
)

session.commit()
```

After **Step 3: Marketing Site**:

```python
# After website workflow completes
create_artifact(
    session=session,
    workflow_id=workflow_id,
    tenant_id=workflow.tenant_id,
    kind="marketing_site_url",
    label="Marketing Site",
    value=deployed_url
)

session.commit()
```

## 3. Workflow Model Updates

Update the main workflow record with linking fields:

```python
# Link workflow to store
workflow.related_store_id = store.id

# Update status as workflow progresses
workflow.status = "running"  # When execution starts
workflow.started_at = datetime.utcnow()
session.commit()

# ... work happens ...

# When complete
workflow.status = "completed"
workflow.completed_at = datetime.utcnow()
workflow.decision = "approved"  # Auto-approved (no council review for store creation)
session.commit()
```

### Calculated Savings (Legacy Compatibility)

Keep `calculated_savings` for backward compatibility but prefer artifacts:

```python
workflow.calculated_savings = workflow.calculated_savings or {}
workflow.calculated_savings.update({
    "store_id": store.id,
    "storefront_url": f"https://{store.domain}",
    "admin_url": f"https://{store.domain}/admin",
    "marketing_site_url": deployed_url,
    "products_created": len(created_products),
    "completed_at": datetime.utcnow().isoformat() + "Z",
    "spawned_social_workflow_id": social_workflow.id  # After social workflow created
})
session.commit()
```

## 4. Social Campaign Workflow

When spawning the social campaign workflow:

```python
social_workflow = Workflow(
    id=f"workflow_{datetime.utcnow().timestamp()}_social",
    tenant_id=workflow.tenant_id,  # CRITICAL: Inherit from parent
    workflow_type_id="social.generate_launch_campaign_for_store",
    type="social.generate_launch_campaign_for_store",
    category="social",
    created_by_agent="agent_shopify_creator",
    
    # Linking
    parent_workflow_id=workflow_id,  # Link to store creation workflow
    related_store_id=store.id,  # Link to store
    
    # Status
    status="pending_review",
    decision="pending",  # Awaits council_media approval
    assigned_council_id="council_media",
    
    # Inputs
    inputs=social_inputs,
    
    # Summary (optional, for council review)
    summary=f"7-day launch campaign for {inputs['brand_name']} across Instagram, YouTube, and email.",
    
    # Timestamps
    created_at=datetime.utcnow()
)

session.add(social_workflow)
session.commit()

# Link back to parent workflow
workflow.calculated_savings["spawned_social_workflow_id"] = social_workflow.id
session.commit()
```

## 5. Complete Integration Example

Here's the complete `execute_store_creation()` with database integration:

```python
def execute_store_creation(workflow_id: str):
    session = SessionLocal()
    try:
        workflow = session.query(Workflow).filter(Workflow.id == workflow_id).first()
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        inputs = workflow.inputs
        
        # Update workflow status
        workflow.status = "running"
        workflow.started_at = datetime.utcnow()
        session.commit()
        
        # Step 1: Connect/create store
        store = _connect_or_create_store(session, workflow_id, workflow.tenant_id, inputs)
        workflow.related_store_id = store.id
        session.commit()
        
        # Create storefront/admin artifacts
        create_artifact(session, workflow_id, workflow.tenant_id, "storefront_url", "Storefront URL", f"https://{store.domain}")
        create_artifact(session, workflow_id, workflow.tenant_id, "admin_url", "Admin Dashboard", f"https://{store.domain}/admin")
        session.commit()
        
        # Step 2: Create products
        created_products = _create_products(session, store, inputs)
        create_artifact(session, workflow_id, workflow.tenant_id, "product_count", "Products Created", str(len(created_products)))
        session.commit()
        
        # Update store status
        store.status = "active"
        session.commit()
        
        # Step 3: Generate marketing site
        site_url = _generate_marketing_site(session, workflow_id, inputs, store)
        create_artifact(session, workflow_id, workflow.tenant_id, "marketing_site_url", "Marketing Site", site_url)
        session.commit()
        
        # Step 4: Send completion email
        _send_completion_notification(inputs, store, site_url, len(created_products))
        
        # Step 5: Spawn social campaign
        social_workflow = _spawn_social_campaign(session, workflow_id, workflow.tenant_id, store, inputs)
        
        # Update workflow status
        workflow.status = "completed"
        workflow.completed_at = datetime.utcnow()
        workflow.decision = "approved"
        workflow.calculated_savings = workflow.calculated_savings or {}
        workflow.calculated_savings["spawned_social_workflow_id"] = social_workflow.id
        session.commit()
        
    except Exception as e:
        workflow.status = "failed"
        workflow.completed_at = datetime.utcnow()
        workflow.decision = "error"
        store.status = "error"
        session.commit()
        raise
    finally:
        session.close()
```

## 6. API Query Patterns for Portal

The portal UI will fetch data like this:

```python
# Fetch store with workflows
store = session.query(Store).filter(Store.id == store_id).first()
workflows = session.query(Workflow).filter(Workflow.related_store_id == store_id).all()

# Fetch workflow with artifacts
workflow = session.query(Workflow).filter(Workflow.id == workflow_id).first()
artifacts = session.query(WorkflowArtifact).filter(WorkflowArtifact.workflow_id == workflow_id).all()

# Fetch recent workflows for tenant
workflows = session.query(Workflow).filter(
    Workflow.tenant_id == tenant_id
).order_by(Workflow.created_at.desc()).limit(5).all()
```

## 7. Migration Checklist

To implement this integration:

- [ ] Update `shopify_creation_worker.py`:
  - [ ] Import `Store` and `WorkflowArtifact` models
  - [ ] Update `_connect_or_create_store()` to use new Store fields
  - [ ] Add artifact creation after each step
  - [ ] Update workflow linking fields (related_store_id, decision)
  - [ ] Pass tenant_id to social workflow

- [ ] Create database migration:
  - [ ] Add new Store fields (storefront_url, admin_url, access_token, owner_email)
  - [ ] Add Workflow fields (category, decision, related_store_id, summary)
  - [ ] Create WorkflowArtifact table

- [ ] Implement portal API endpoints:
  - [ ] `GET /api/portal/dashboard` - Dashboard data
  - [ ] `GET /api/portal/stores/:id` - Store detail
  - [ ] `GET /api/portal/workflows/:id` - Workflow detail
  - [ ] `GET /api/portal/workflows/:id/artifacts` - Workflow artifacts

- [ ] Update sales_intake_worker.py:
  - [ ] Set tenant_id when creating store workflow
  - [ ] Set workflow.type and workflow.category

## 8. Key Fields Reference

### Store
- `id` - UUID string
- `tenant_id` - Foreign key (REQUIRED)
- `name` - Brand/store name
- `platform` - "shopify" or "woocommerce"
- `domain` - Store domain (e.g., "mybrand.myshopify.com")
- `storefront_url` - Public URL
- `admin_url` - Admin dashboard URL
- `access_token` - Platform credentials
- `owner_email` - Store owner email
- `settings` - JSON (colors, fonts, categories)
- `status` - "pending_setup", "active", "error"
- `created_via_workflow_id` - Foreign key to Workflow

### Workflow
- `id` - UUID string
- `tenant_id` - Foreign key (nullable for internal)
- `type` - String like "store.create_shopify_store"
- `category` - "sales", "store", "social", "website"
- `status` - "pending_review", "queued", "running", "completed", "failed"
- `decision` - "pending", "approved", "declined", "error"
- `parent_workflow_id` - Foreign key to parent Workflow
- `related_store_id` - Foreign key to Store
- `summary` - Text for council review
- `started_at` - Datetime when execution started
- `completed_at` - Datetime when finished

### WorkflowArtifact
- `id` - UUID string
- `workflow_id` - Foreign key (REQUIRED)
- `tenant_id` - Foreign key (REQUIRED)
- `kind` - "storefront_url", "admin_url", "marketing_site_url", "product_count", etc.
- `label` - Human-readable description
- `value` - Text/JSON content

---

**Status**: Ready for implementation  
**Next Step**: Update `shopify_creation_worker.py` with these patterns
