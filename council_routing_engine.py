"""
CODEX DOMINION - COUNCIL ROUTING ENGINE
========================================
Determines which council(s) should review a workflow based on content and context

Council Review Rules:
- Media Council: Public-facing sites, content-heavy sites
- Commerce Council: Commercial sites, e-commerce, paid services
- Youth Council: Content targeting minors (<18)
- Identity & Safety Council: Authentication, personal data, sensitive content
- Governance Council: System-wide policy changes

Integration with Workflow Review System:
- Automatically assigns workflows to councils based on content analysis
- Triggers pending_review status when thresholds are exceeded
- Routes to primary council for approval/rejection
- Sends notifications when workflows require human review
"""

from typing import Dict, Any, List, Optional
from enum import Enum

# Import database models for council routing
try:
    from db import SessionLocal
    from models import Council, Workflow, WorkflowStatus, WorkflowDecision
    from notification_worker import notify_needs_review
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("⚠️ Database models not available - council routing will run in analysis-only mode")


class CouncilDomain(str, Enum):
    MEDIA = "media"
    COMMERCE = "commerce"
    FINANCE = "finance"
    YOUTH = "youth"
    IDENTITY_SAFETY = "identity_safety"
    TECHNOLOGY = "technology"
    GOVERNANCE = "governance"


class ReviewTrigger:
    """Rules that trigger council review"""
    
    # Keywords that trigger specific council reviews
    COMMERCE_KEYWORDS = [
        "shop", "store", "buy", "purchase", "payment", "checkout",
        "pricing", "product", "cart", "order", "sell", "ecommerce"
    ]
    
    YOUTH_KEYWORDS = [
        "kid", "child", "youth", "teen", "student", "school",
        "education", "learning", "homework", "classroom"
    ]
    
    IDENTITY_KEYWORDS = [
        "login", "signup", "auth", "password", "profile", "account",
        "personal", "private", "sensitive", "identity", "verification"
    ]
    
    MEDIA_KEYWORDS = [
        "blog", "content", "media", "publish", "article", "post",
        "video", "image", "gallery", "news", "social"
    ]
    
    # High-value thresholds that require additional review
    HIGH_VALUE_THRESHOLD_WEEKLY = 1000  # USD
    HIGH_VALUE_THRESHOLD_ANNUAL = 50000  # USD


def analyze_workflow_content(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze workflow inputs to determine content characteristics
    
    Args:
        inputs: Workflow input dictionary
    
    Returns:
        content_analysis: Dictionary with flags for different content types
    """
    analysis = {
        "is_commercial": False,
        "targets_youth": False,
        "handles_identity": False,
        "is_public_facing": True,  # Default assumption for websites
        "has_media_content": False,
        "triggers": []
    }
    
    # Convert all inputs to lowercase string for keyword matching
    input_text = " ".join([
        str(v).lower() for v in inputs.values() if v is not None
    ])
    
    # Check for commerce triggers
    if any(keyword in input_text for keyword in ReviewTrigger.COMMERCE_KEYWORDS):
        analysis["is_commercial"] = True
        analysis["triggers"].append("commerce_keywords_detected")
    
    # Check for youth triggers
    if any(keyword in input_text for keyword in ReviewTrigger.YOUTH_KEYWORDS):
        analysis["targets_youth"] = True
        analysis["triggers"].append("youth_keywords_detected")
    
    # Check for identity/safety triggers
    if any(keyword in input_text for keyword in ReviewTrigger.IDENTITY_KEYWORDS):
        analysis["handles_identity"] = True
        analysis["triggers"].append("identity_keywords_detected")
    
    # Check for media triggers
    if any(keyword in input_text for keyword in ReviewTrigger.MEDIA_KEYWORDS):
        analysis["has_media_content"] = True
        analysis["triggers"].append("media_keywords_detected")
    
    # Check explicit flags in inputs
    if inputs.get("is_commercial", False):
        analysis["is_commercial"] = True
        analysis["triggers"].append("explicit_commercial_flag")
    
    if inputs.get("target_audience") == "youth":
        analysis["targets_youth"] = True
        analysis["triggers"].append("explicit_youth_targeting")
    
    if inputs.get("requires_authentication", False):
        analysis["handles_identity"] = True
        analysis["triggers"].append("authentication_required")
    
    return analysis


def determine_required_councils(
    workflow_type_id: str,
    inputs: Dict[str, Any],
    calculated_savings: Optional[Dict[str, float]] = None
) -> List[CouncilDomain]:
    """
    Determine which council(s) must review this workflow
    
    Args:
        workflow_type_id: Type of workflow (e.g., "website.create_basic_site")
        inputs: Workflow input dictionary
        calculated_savings: Financial impact (weekly/annual savings)
    
    Returns:
        List of CouncilDomain values that must review
    
    Examples:
        >>> determine_required_councils(
        ...     "website.create_basic_site",
        ...     {"site_name": "My Store", "description": "Buy products online"}
        ... )
        [CouncilDomain.MEDIA, CouncilDomain.COMMERCE]
    """
    councils = []
    
    # Analyze content
    analysis = analyze_workflow_content(inputs)
    
    # Rule 1: All public-facing websites go to Media Council
    if analysis["is_public_facing"] and "website" in workflow_type_id:
        councils.append(CouncilDomain.MEDIA)
    
    # Rule 2: Commercial content goes to Commerce Council
    if analysis["is_commercial"]:
        councils.append(CouncilDomain.COMMERCE)
    
    # Rule 3: Youth-targeted content goes to Youth Council
    if analysis["targets_youth"]:
        councils.append(CouncilDomain.YOUTH)
    
    # Rule 4: Identity/authentication goes to Identity & Safety Council
    if analysis["handles_identity"]:
        councils.append(CouncilDomain.IDENTITY_SAFETY)
    
    # Rule 5: High-value workflows get Governance Council oversight
    if calculated_savings:
        weekly = calculated_savings.get("weekly_savings", 0)
        annual = calculated_savings.get("annual_savings", weekly * 52)
        
        if (weekly >= ReviewTrigger.HIGH_VALUE_THRESHOLD_WEEKLY or
            annual >= ReviewTrigger.HIGH_VALUE_THRESHOLD_ANNUAL):
            councils.append(CouncilDomain.GOVERNANCE)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_councils = []
    for council in councils:
        if council not in seen:
            seen.add(council)
            unique_councils.append(council)
    
    return unique_councils


def get_primary_council(councils: List[CouncilDomain]) -> CouncilDomain:
    """
    Get the primary (lead) council from a list of required councils
    
    Priority order:
    1. Governance (highest authority)
    2. Commerce (business impact)
    3. Media (public-facing)
    4. Identity & Safety (security)
    5. Youth (protection)
    6. Technology (infrastructure)
    7. Finance (cost management)
    """
    priority_order = [
        CouncilDomain.GOVERNANCE,
        CouncilDomain.COMMERCE,
        CouncilDomain.MEDIA,
        CouncilDomain.IDENTITY_SAFETY,
        CouncilDomain.YOUTH,
        CouncilDomain.TECHNOLOGY,
        CouncilDomain.FINANCE
    ]
    
    for council in priority_order:
        if council in councils:
            return council
    
    # Default to Media if no match
    return CouncilDomain.MEDIA


def create_council_review_request(
    workflow_id: str,
    workflow_type_id: str,
    inputs: Dict[str, Any],
    calculated_savings: Optional[Dict[str, float]] = None,
    created_by_agent: str = None
) -> Dict[str, Any]:
    """
    Create a complete council review request with routing and context
    
    Args:
        workflow_id: Workflow database ID
        workflow_type_id: Type of workflow
        inputs: Workflow inputs
        calculated_savings: Financial impact
        created_by_agent: Agent who created the workflow
    
    Returns:
        Review request dictionary with councils, context, and metadata
    """
    # Determine required councils
    required_councils = determine_required_councils(
        workflow_type_id,
        inputs,
        calculated_savings
    )
    
    # Get primary council
    primary_council = get_primary_council(required_councils)
    
    # Analyze content for context
    content_analysis = analyze_workflow_content(inputs)
    
    # Build review request
    review_request = {
        "workflow_id": workflow_id,
        "workflow_type_id": workflow_type_id,
        "created_by_agent": created_by_agent,
        "councils": {
            "primary": primary_council.value,
            "required": [c.value for c in required_councils],
            "count": len(required_councils)
        },
        "content_analysis": content_analysis,
        "calculated_savings": calculated_savings,
        "review_criteria": get_review_criteria(required_councils),
        "approval_threshold": "simple_majority",  # 50% + 1
        "status": "pending_review"
    }
    
    return review_request


def get_review_criteria(councils: List[CouncilDomain]) -> List[str]:
    """Get the review criteria based on which councils are involved"""
    criteria = []
    
    if CouncilDomain.MEDIA in councils:
        criteria.extend([
            "Brand consistency and voice",
            "Content quality and accuracy",
            "SEO and discoverability",
            "Accessibility compliance (WCAG 2.1)"
        ])
    
    if CouncilDomain.COMMERCE in councils:
        criteria.extend([
            "Pricing transparency",
            "Payment security",
            "Terms of service clarity",
            "Return/refund policy"
        ])
    
    if CouncilDomain.YOUTH in councils:
        criteria.extend([
            "Age-appropriate content",
            "COPPA compliance",
            "Parental consent mechanisms",
            "Safety features and moderation"
        ])
    
    if CouncilDomain.IDENTITY_SAFETY in councils:
        criteria.extend([
            "Data privacy and encryption",
            "Authentication security",
            "GDPR/CCPA compliance",
            "User data handling procedures"
        ])
    
    if CouncilDomain.GOVERNANCE in councils:
        criteria.extend([
            "Strategic alignment",
            "Risk assessment",
            "Budget impact",
            "Long-term sustainability"
        ])
    
    return list(set(criteria))  # Remove duplicates


def route_workflow_to_council(
    workflow_id: str,
    auto_assign: bool = True,
    auto_notify: bool = True
) -> Dict[str, Any]:
    """
    Route a workflow to the appropriate council for review
    
    This is the main integration point with the workflow review system.
    
    Args:
        workflow_id: Workflow database ID
        auto_assign: If True, automatically assign to council and update status
        auto_notify: If True, send notification to council members
    
    Returns:
        routing_result: Dictionary with council assignment and actions taken
    
    Usage:
        # In workflow_engine.py after workflow creation:
        from council_routing_engine import route_workflow_to_council
        
        workflow_id = workflow_engine.create_workflow(...)
        routing = route_workflow_to_council(workflow_id, auto_assign=True, auto_notify=True)
    """
    if not DATABASE_AVAILABLE:
        return {
            "success": False,
            "error": "Database not available",
            "workflow_id": workflow_id
        }
    
    session = SessionLocal()
    try:
        # Get workflow
        workflow = session.query(Workflow).filter_by(id=workflow_id).first()
        if not workflow:
            return {"success": False, "error": "Workflow not found", "workflow_id": workflow_id}
        
        # Determine required councils
        required_councils = determine_required_councils(
            workflow.workflow_type_id,
            workflow.inputs or {},
            workflow.calculated_savings
        )
        
        if not required_councils:
            return {
                "success": True,
                "requires_review": False,
                "workflow_id": workflow_id,
                "message": "No council review required"
            }
        
        # Get primary council
        primary_council_domain = get_primary_council(required_councils)
        
        # Find council in database
        council = session.query(Council).filter_by(
            id=f"council_{primary_council_domain.value}"
        ).first()
        
        if not council:
            # Try alternate ID format
            council = session.query(Council).filter(
                Council.name.ilike(f"%{primary_council_domain.value}%")
            ).first()
        
        if not council:
            return {
                "success": False,
                "error": f"Council not found: {primary_council_domain.value}",
                "workflow_id": workflow_id,
                "required_councils": [c.value for c in required_councils]
            }
        
        # Check if workflow savings exceed council's review threshold
        requires_review = should_require_review(workflow, council)
        
        result = {
            "success": True,
            "requires_review": requires_review,
            "workflow_id": workflow_id,
            "assigned_council_id": council.id,
            "assigned_council_name": council.name,
            "required_councils": [c.value for c in required_councils],
            "actions_taken": []
        }
        
        if auto_assign and requires_review:
            # Assign workflow to council
            workflow.assigned_council_id = council.id
            workflow.status = WorkflowStatus.PENDING_REVIEW
            workflow.decision_status = WorkflowDecision.PENDING
            session.commit()
            result["actions_taken"].append("assigned_to_council")
            result["actions_taken"].append("status_updated_to_pending_review")
            
            # Send notification
            if auto_notify:
                try:
                    notify_needs_review(
                        workflow_id=workflow_id,
                        summary={
                            "council": council.name,
                            "reason": "savings_threshold_exceeded" if requires_review else "manual_review",
                            "required_councils": [c.value for c in required_councils]
                        }
                    )
                    result["actions_taken"].append("notification_sent")
                except Exception as e:
                    result["notification_error"] = str(e)
        
        return result
        
    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "error": str(e),
            "workflow_id": workflow_id
        }
    finally:
        session.close()


def should_require_review(workflow: "Workflow", council: "Council") -> bool:
    """
    Determine if a workflow requires council review based on oversight configuration
    
    Args:
        workflow: Workflow SQLAlchemy object
        council: Council SQLAlchemy object
    
    Returns:
        True if review is required, False otherwise
    
    Review Triggers:
    1. Workflow savings exceed council's review_threshold_weekly_savings
    2. Workflow action_type is in council's blocked_action_types
    3. Council requires review for all workflows (review_actions=True with no threshold)
    """
    if not council.config or not council.config.get("oversight"):
        return False
    
    oversight = council.config["oversight"]
    
    # Check if council reviews actions at all
    if not oversight.get("review_actions", False):
        return False
    
    # Check savings threshold
    threshold = oversight.get("review_threshold_weekly_savings", float('inf'))
    weekly_savings = 0
    if workflow.calculated_savings:
        weekly_savings = (
            workflow.calculated_savings.get("weekly") or
            workflow.calculated_savings.get("weekly_savings") or
            0
        )
    
    if weekly_savings >= threshold:
        return True
    
    # Check blocked action types
    blocked_actions = oversight.get("blocked_action_types", [])
    if workflow.type and workflow.type in blocked_actions:
        return True
    
    return False


def get_council_members_for_notification(council_id: str) -> List[str]:
    """
    Get list of user IDs who should be notified for a council review
    
    Args:
        council_id: Council database ID
    
    Returns:
        List of user_ids (council operators + members)
    """
    if not DATABASE_AVAILABLE:
        return []
    
    session = SessionLocal()
    try:
        from models import User, CouncilMember
        
        council = session.query(Council).filter_by(id=council_id).first()
        if not council:
            return []
        
        user_ids = []
        
        # Get council operators (users with voting rights)
        if council.operators:
            user_ids.extend([u.id for u in council.operators])
        
        # Get council members (agents with associated users)
        members = session.query(CouncilMember).filter_by(
            council_id=council_id,
            is_active=True
        ).all()
        
        # TODO: Map agents to users when agent->user relationship exists
        
        return list(set(user_ids))  # Remove duplicates
        
    except Exception as e:
        print(f"❌ Error getting council members: {str(e)}")
        return []
    finally:
        session.close()


if __name__ == "__main__":
    # Example 1: Basic website
    print("=" * 60)
    print("EXAMPLE 1: Basic Public Website")
    print("=" * 60)
    
    request1 = create_council_review_request(
        workflow_id="wf_abc123",
        workflow_type_id="website.create_basic_site",
        inputs={
            "site_name": "Codex Digital Studios",
            "site_description": "Professional web design services",
            "pages": ["home", "about", "services", "contact", "blog"]
        },
        calculated_savings={"weekly_savings": 225.0},
        created_by_agent="agent_jermaine_super_action"
    )
    
    import json
    print(json.dumps(request1, indent=2))
    
    # Example 2: E-commerce site
    print("\n" + "=" * 60)
    print("EXAMPLE 2: E-commerce Store")
    print("=" * 60)
    
    request2 = create_council_review_request(
        workflow_id="wf_def456",
        workflow_type_id="website.create_ecommerce_store",
        inputs={
            "site_name": "Codex Shop",
            "site_description": "Buy digital products and templates online",
            "features": ["product_catalog", "shopping_cart", "payment_processing"],
            "payment_methods": ["credit_card", "paypal"]
        },
        calculated_savings={"weekly_savings": 450.0},
        created_by_agent="agent_commerce_strategist"
    )
    
    print(json.dumps(request2, indent=2))
    
    # Example 3: Educational site for youth
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Youth Educational Platform")
    print("=" * 60)
    
    request3 = create_council_review_request(
        workflow_id="wf_ghi789",
        workflow_type_id="website.create_learning_platform",
        inputs={
            "site_name": "Kids Bible Stories",
            "site_description": "Interactive Bible learning for children ages 5-12",
            "target_audience": "youth",
            "features": ["video_lessons", "quizzes", "parent_dashboard"]
        },
        calculated_savings={"weekly_savings": 180.0},
        created_by_agent="agent_content_creator"
    )
    
    print(json.dumps(request3, indent=2))
