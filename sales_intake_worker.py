from db import SessionLocal
from models import Workflow, WorkflowMetric
from workflow_engine import workflow_engine
from email_service import send_approval_email
from datetime import datetime
import json


def score_intake(inputs: dict) -> dict:
    """
    Scores the intake based on 6 dimensions (0-3 each, max 18).
    Returns score, breakdown, and recommendation.
    """
    score_breakdown = {}
    
    # 1. Clarity of brand (0-3)
    brand_desc = inputs.get("brand_description", "")
    if len(brand_desc) > 200:
        score_breakdown["brand_clarity"] = 3
    elif len(brand_desc) > 100:
        score_breakdown["brand_clarity"] = 2
    elif len(brand_desc) > 30:
        score_breakdown["brand_clarity"] = 1
    else:
        score_breakdown["brand_clarity"] = 0
    
    # 2. Clarity of product (0-3)
    products = inputs.get("primary_products", [])
    if len(products) >= 3:
        score_breakdown["product_clarity"] = 3
    elif len(products) == 2:
        score_breakdown["product_clarity"] = 2
    elif len(products) == 1:
        score_breakdown["product_clarity"] = 1
    else:
        score_breakdown["product_clarity"] = 0
    
    # 3. Revenue ambition (0-3)
    revenue_goal = inputs.get("estimated_monthly_revenue_goal", 0)
    if revenue_goal >= 10000:
        score_breakdown["revenue_ambition"] = 3
    elif revenue_goal >= 5000:
        score_breakdown["revenue_ambition"] = 2
    elif revenue_goal >= 1000:
        score_breakdown["revenue_ambition"] = 1
    else:
        score_breakdown["revenue_ambition"] = 0
    
    # 4. Timeline readiness (0-3)
    timeline = inputs.get("timeline_readiness", "")
    if timeline == "ready_now":
        score_breakdown["timeline_readiness"] = 3
    elif timeline == "30_days":
        score_breakdown["timeline_readiness"] = 2
    elif timeline == "90_days":
        score_breakdown["timeline_readiness"] = 1
    else:
        score_breakdown["timeline_readiness"] = 0
    
    # 5. Platform fit (0-3)
    platform = inputs.get("preferred_platform", "undecided")
    if platform in ["shopify", "woocommerce"]:
        score_breakdown["platform_fit"] = 3
    elif platform == "undecided":
        score_breakdown["platform_fit"] = 2
    else:
        score_breakdown["platform_fit"] = 0
    
    # 6. Blocker severity (0-3, reversed - fewer blockers = higher score)
    blockers = inputs.get("biggest_blockers", "")
    if len(blockers) < 50:
        score_breakdown["blocker_severity"] = 3
    elif len(blockers) < 150:
        score_breakdown["blocker_severity"] = 2
    elif len(blockers) < 300:
        score_breakdown["blocker_severity"] = 1
    else:
        score_breakdown["blocker_severity"] = 0
    
    total_score = sum(score_breakdown.values())
    recommendation = "approve" if total_score >= 10 else "hold"
    
    return {
        "total_score": total_score,
        "breakdown": score_breakdown,
        "recommendation": recommendation
    }


def generate_intake_summary(inputs: dict, score_data: dict) -> str:
    """
    Generates AI-written intake summary (briefing scroll).
    In production, this would call an LLM. For now, template-based.
    """
    brand_name = inputs.get("brand_name", "Unknown Brand")
    contact_name = inputs.get("contact_name", "Unknown")
    products = ", ".join(inputs.get("primary_products", []))
    target_audience = inputs.get("target_audience", "General audience")
    revenue_goal = inputs.get("estimated_monthly_revenue_goal", 0)
    timeline = inputs.get("timeline_readiness", "unknown")
    blockers = inputs.get("biggest_blockers", "None specified")
    platform = inputs.get("preferred_platform", "undecided")
    current_stage = inputs.get("current_stage", "unknown")
    
    summary = f"""
**Who They Are:**
{contact_name} is seeking to launch {brand_name}, targeting {target_audience}.

**What They Sell:**
Primary products: {products}

**Current Stage:**
{current_stage.replace("_", " ").title()}

**Revenue Goal:**
${revenue_goal:,}/month

**Timeline:**
{timeline.replace("_", " ").title()}

**Biggest Blockers:**
{blockers}

**Platform Preference:**
{platform.title()}

**Fit Assessment:**
Total score: {score_data['total_score']}/18
- Brand clarity: {score_data['breakdown']['brand_clarity']}/3
- Product clarity: {score_data['breakdown']['product_clarity']}/3
- Revenue ambition: {score_data['breakdown']['revenue_ambition']}/3
- Timeline readiness: {score_data['breakdown']['timeline_readiness']}/3
- Platform fit: {score_data['breakdown']['platform_fit']}/3
- Blocker severity: {score_data['breakdown']['blocker_severity']}/3

**Recommended Platform:**
{"Shopify" if platform == "shopify" or platform == "undecided" else "WooCommerce"}

**Recommended Next Step:**
{score_data['recommendation'].title()} - {"This prospect shows strong fit for Empire Store Ignition." if score_data['recommendation'] == "approve" else "Additional qualification needed before proceeding."}
"""
    
    return summary.strip()


def execute_sales_intake(workflow_id: str):
    """
    Main worker execution for sales.empire_store_ignition_intake
    """
    session = SessionLocal()
    
    try:
        workflow = session.query(Workflow).filter_by(id=workflow_id).first()
        if not workflow:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        inputs = workflow.inputs or {}
        
        # A. Load and normalize inputs (already done via workflow.inputs)
        
        # B. Score the lead
        score_data = score_intake(inputs)
        
        # C. Generate intake summary
        summary = generate_intake_summary(inputs, score_data)
        
        # D. Route to Commerce Council
        workflow.status = "pending_review"
        workflow.assigned_council_id = "council_commerce"
        
        # Store summary and score in calculated_savings (or add a new JSON field)
        if not workflow.calculated_savings:
            workflow.calculated_savings = {}
        
        workflow.calculated_savings["intake_summary"] = summary
        workflow.calculated_savings["fit_score"] = score_data["total_score"]
        workflow.calculated_savings["score_breakdown"] = score_data["breakdown"]
        workflow.calculated_savings["recommendation"] = score_data["recommendation"]
        
        session.commit()
        
        print(f"✅ Intake scored and routed to Commerce Council")
        print(f"   Score: {score_data['total_score']}/18")
        print(f"   Recommendation: {score_data['recommendation']}")
        
        return {
            "status": "success",
            "score": score_data["total_score"],
            "recommendation": score_data["recommendation"]
        }
        
    except Exception as e:
        session.rollback()
        print(f"❌ Intake execution failed: {str(e)}")
        raise
    finally:
        session.close()


def approve_intake_and_create_store(workflow_id: str):
    """
    Called when Commerce Council approves intake.
    Maps intake fields → store creation workflow.
    """
    session = SessionLocal()
    
    try:
        intake_workflow = session.query(Workflow).filter_by(id=workflow_id).first()
        if not intake_workflow:
            raise ValueError(f"Intake workflow {workflow_id} not found")
        
        inputs = intake_workflow.inputs or {}
        
        # Map intake fields to store creation fields
        platform = inputs.get("preferred_platform", "shopify")
        if platform == "undecided":
            platform = "shopify"  # Default to Shopify
        
        store_workflow_type = "store.create_shopify_store" if platform == "shopify" else "store.create_woocommerce_store"
        
        store_inputs = {
            "brand_name": inputs.get("brand_name"),
            "brand_description": inputs.get("brand_description"),
            "primary_color": "#F5C542",  # Default sovereign colors
            "secondary_color": "#10B981",
            "primary_font": "Inter",
            "secondary_font": "Roboto",
            "target_countries": inputs.get("target_countries", ["US"]),
            "default_currency": "USD",  # TODO: Infer from target_countries
            "shop_owner_email": inputs.get("contact_email"),
            "product_categories": inputs.get("primary_products", []),
            "initial_products_count": max(5, len(inputs.get("primary_products", []))),
            "shopify_store_type": "new" if inputs.get("current_store_platform") == "none" else "existing",
            "existing_shopify_domain": inputs.get("current_store_url") if inputs.get("current_store_platform") != "none" else None
        }
        
        # Create store workflow
        store_workflow_id = workflow_engine.create_workflow(
            workflow_type_id=store_workflow_type,
            created_by_agent="agent_jermaine",
            inputs=store_inputs,
            assigned_council_id="council_commerce",
            auto_execute=False  # Will be manually approved
        )
        
        # Link workflows
        if not intake_workflow.calculated_savings:
            intake_workflow.calculated_savings = {}
        
        intake_workflow.calculated_savings["spawned_store_workflow_id"] = store_workflow_id
        intake_workflow.status = "approved"
        
        session.commit()
        
        # Send approval email to client
        send_approval_email(
            to_email=inputs["contact_email"],
            context={
                "contact_name": inputs["contact_name"],
                "brand_name": inputs["brand_name"],
                "platform_choice": "Shopify" if platform == "shopify" else "WooCommerce",
                "target_countries": inputs["target_countries"],
                "default_currency": "USD",
                "initial_products": store_inputs["initial_products_count"],
                "estimated_days": 7
            }
        )
        
        print(f"✅ Store workflow created: {store_workflow_id}")
        print(f"   Type: {store_workflow_type}")
        print(f"   Linked to intake: {workflow_id}")
        print(f"   Approval email sent to: {inputs['contact_email']}")
        
        return {
            "status": "success",
            "store_workflow_id": store_workflow_id,
            "store_workflow_type": store_workflow_type
        }
        
    except Exception as e:
        session.rollback()
        print(f"❌ Store workflow creation failed: {str(e)}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python sales_intake_worker.py <command> <workflow_id>")
        print("Commands: execute, approve")
        sys.exit(1)
    
    command = sys.argv[1]
    workflow_id = sys.argv[2]
    
    if command == "execute":
        result = execute_sales_intake(workflow_id)
        print(json.dumps(result, indent=2))
    elif command == "approve":
        result = approve_intake_and_create_store(workflow_id)
        print(json.dumps(result, indent=2))
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
