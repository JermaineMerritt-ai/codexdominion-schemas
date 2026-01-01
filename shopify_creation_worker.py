import os
import sys
from datetime import datetime
from db import SessionLocal
from models import Workflow, Store
from store_service import create_product
from email_service import send_completion_email

def execute_store_creation(workflow_id: str):
    session = SessionLocal()
    try:
        workflow = session.query(Workflow).filter(Workflow.id == workflow_id).first()
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        if workflow.status != "pending_review":
            print(f"⚠️  Workflow {workflow_id} is not pending review (status: {workflow.status})")
            return
        
        inputs = workflow.inputs
        
        print(f"🏗️  Starting store creation for: {inputs['brand_name']}")
        workflow.status = "running"
        session.commit()
        
        # Step 1: Connect or create Shopify store
        print(f"📦 Step 1/4: Connecting to Shopify store...")
        store = _connect_or_create_store(session, workflow_id, inputs)
        
        # Step 2: Create products
        print(f"🎨 Step 2/4: Creating {inputs['initial_products_count']} products...")
        created_products = _create_products(session, store, inputs)
        
        # Step 3: Generate marketing site
        print(f"🌐 Step 3/4: Generating marketing site...")
        site_url = _generate_marketing_site(session, workflow_id, inputs, store)
        
        # Step 4: Send completion email
        print(f"📧 Step 4/4: Notifying client...")
        _send_completion_notification(inputs, store, site_url, len(created_products))
        
        # Store artifacts
        workflow.calculated_savings = workflow.calculated_savings or {}
        workflow.calculated_savings.update({
            "store_id": store.id,
            "storefront_url": f"https://{store.domain}",
            "admin_url": f"https://{store.domain}/admin",
            "marketing_site_url": site_url,
            "products_created": len(created_products),
            "completed_at": datetime.utcnow().isoformat() + "Z"
        })
        workflow.status = "completed"
        session.commit()
        
        # Auto-trigger social campaign workflow
        print(f"🚀 Spawning social campaign workflow...")
        _spawn_social_campaign(session, workflow_id, store, inputs)
        
        print(f"✅ Store creation complete: {inputs['brand_name']}")
        print(f"   Storefront: https://{store.domain}")
        print(f"   Admin: https://{store.domain}/admin")
        print(f"   Marketing Site: {site_url}")
        print(f"   Products: {len(created_products)}")
        
    except Exception as e:
        print(f"❌ Error in store creation: {str(e)}")
        workflow.status = "failed"
        workflow.calculated_savings = workflow.calculated_savings or {}
        workflow.calculated_savings["error"] = str(e)
        workflow.calculated_savings["failed_at"] = datetime.utcnow().isoformat() + "Z"
        session.commit()
        raise
    finally:
        session.close()

def _connect_or_create_store(session, workflow_id: str, inputs: dict) -> Store:
    """Connect to existing store or create new record"""
    
    # Check if store already exists
    existing_store = session.query(Store).filter(Store.domain == inputs.get("shopify_domain")).first()
    if existing_store:
        print(f"   Found existing store: {existing_store.id}")
        return existing_store
    
    # Create new store record
    store = Store(
        id=f"store_{workflow_id[:8]}",
        name=inputs["brand_name"],
        platform="shopify",
        domain=inputs.get("shopify_domain") or f"{inputs['brand_name'].lower().replace(' ', '-')}.myshopify.com",
        credentials={
            "access_token": inputs.get("shopify_access_token"),
            "store_domain": inputs.get("shopify_domain")
        },
        settings={
            "primary_color": inputs.get("primary_color", "#F5C542"),
            "secondary_color": inputs.get("secondary_color", "#10B981"),
            "font_family": inputs.get("font_family", "Inter"),
            "product_categories": inputs.get("product_categories", []),
            "target_countries": inputs.get("target_countries", ["US"]),
            "default_currency": inputs.get("default_currency", "USD")
        },
        created_by_workflow_id=workflow_id
    )
    
    session.add(store)
    session.commit()
    
    print(f"   Created store record: {store.id}")
    return store

def _create_products(session, store: Store, inputs: dict) -> list:
    """Generate and create products in Shopify"""
    
    created_products = []
    product_count = inputs.get("initial_products_count", 5)
    categories = inputs.get("product_categories", ["general"])
    
    for i in range(product_count):
        category = categories[i % len(categories)] if categories else "general"
        
        product_payload = {
            "title": f"{inputs['brand_name']} {category.title()} Product {i+1}",
            "body_html": f"<p>Premium {category} product from {inputs['brand_name']}. Crafted with care for your {inputs.get('target_audience', 'customers')}.</p>",
            "vendor": inputs['brand_name'],
            "product_type": category,
            "tags": [category, inputs['brand_name'], "new"],
            "variants": [
                {
                    "price": "29.99",
                    "sku": f"{inputs['brand_name'][:3].upper()}-{category[:3].upper()}-{i+1:03d}",
                    "inventory_quantity": 100
                }
            ],
            "status": "draft"
        }
        
        try:
            result = create_product(store, product_payload)
            created_products.append({
                "id": result.get("product", {}).get("id"),
                "title": result.get("product", {}).get("title"),
                "handle": result.get("product", {}).get("handle")
            })
            print(f"   ✓ Created: {product_payload['title']}")
        except Exception as e:
            print(f"   ⚠️  Failed to create product {i+1}: {str(e)}")
    
    return created_products

def _generate_marketing_site(session, workflow_id: str, inputs: dict, store: Store) -> str:
    """Generate marketing site via website.create_basic_site workflow"""
    
    # Import here to avoid circular dependencies
    from website_creation_worker_complete import execute_website_creation
    
    # Create website workflow
    site_inputs = {
        "site_name": f"{inputs['brand_name']} Store",
        "site_description": inputs.get("brand_description", f"Official store for {inputs['brand_name']}"),
        "pages": ["home", "products", "about", "contact"],
        "color_scheme": {
            "primary": inputs.get("primary_color", "#F5C542"),
            "secondary": inputs.get("secondary_color", "#10B981")
        },
        "font_family": inputs.get("font_family", "Inter"),
        "deploy_to": "vercel",
        "repo_name": f"{inputs['brand_name'].lower().replace(' ', '-')}-site"
    }
    
    site_workflow = Workflow(
        id=f"workflow_{datetime.utcnow().timestamp()}",
        workflow_type_id="website.create_basic_site",
        action_type="website.create_basic_site",
        status="running",
        inputs=site_inputs,
        parent_workflow_id=workflow_id,
        created_by_agent="agent_shopify_creator"
    )
    
    session.add(site_workflow)
    session.commit()
    
    # Execute website creation (synchronous for now)
    try:
        execute_website_creation(site_workflow.id)
        session.refresh(site_workflow)
        deployed_url = site_workflow.calculated_savings.get("deployed_url")
        print(f"   ✓ Marketing site deployed: {deployed_url}")
        return deployed_url
    except Exception as e:
        print(f"   ⚠️  Failed to generate marketing site: {str(e)}")
        return f"https://{store.domain}"

def _send_completion_notification(inputs: dict, store: Store, site_url: str, products_created: int):
    """Send completion email to client"""
    
    try:
        send_completion_email(
            to_email=inputs.get("contact_email"),
            context={
                "contact_name": inputs.get("contact_name"),
                "brand_name": inputs["brand_name"],
                "storefront_url": f"https://{store.domain}",
                "admin_url": f"https://{store.domain}/admin",
                "marketing_site_url": site_url,
                "products_created": products_created
            }
        )
        print(f"   ✓ Completion email sent to: {inputs.get('contact_email')}")
    except Exception as e:
        print(f"   ⚠️  Failed to send completion email: {str(e)}")

def _spawn_social_campaign(session, workflow_id: str, store: Store, inputs: dict):
    """Auto-trigger social campaign workflow"""
    
    # Try to get parent intake workflow for target_audience
    parent_workflow = session.query(Workflow).filter(Workflow.id == inputs.get("parent_workflow_id")).first()
    intake_target_audience = None
    if parent_workflow and parent_workflow.inputs:
        intake_target_audience = parent_workflow.inputs.get("target_audience")
    
    social_inputs = {
        "store_id": store.id,
        "store_url": f"https://{store.domain}",
        "brand_name": inputs["brand_name"],
        "target_audience": intake_target_audience or inputs.get("target_audience", "general audience"),
        "primary_platforms": ["instagram", "youtube", "email"],
        "launch_duration_days": 7
    }
    
    social_workflow = Workflow(
        id=f"workflow_{datetime.utcnow().timestamp()}_social",
        workflow_type_id="social.generate_launch_campaign_for_store",
        action_type="social.generate_launch_campaign_for_store",
        status="pending_review",
        inputs=social_inputs,
        assigned_council_id="council_media",
        parent_workflow_id=workflow_id,
        created_by_agent="agent_shopify_creator"
    )
    
    session.add(social_workflow)
    session.commit()
    
    # Store reference in parent workflow
    parent = session.query(Workflow).filter(Workflow.id == workflow_id).first()
    if parent:
        parent.calculated_savings = parent.calculated_savings or {}
        parent.calculated_savings["spawned_social_workflow_id"] = social_workflow.id
        session.commit()
    
    print(f"   ✓ Social campaign workflow created: {social_workflow.id}")
    print(f"   Assigned to: council_media")
    print(f"   Platforms: {', '.join(social_inputs['primary_platforms'])}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python shopify_creation_worker.py <workflow_id>")
        sys.exit(1)
    
    workflow_id = sys.argv[1]
    execute_store_creation(workflow_id)
