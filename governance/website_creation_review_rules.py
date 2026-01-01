"""
COUNCIL REVIEW RULES - WEBSITE CREATION WORKFLOW
=================================================
Detailed governance rules for Media Council review of website workflows

Defines:
- Review criteria with scoring rubric
- Auto-approval conditions
- Escalation triggers
- Review timeline SLAs
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta


class WebsiteReviewRules:
    """Council review rules for website creation workflows"""
    
    # Review criteria with point values (total 100 points)
    REVIEW_CRITERIA = {
        "brand_consistency": {
            "weight": 25,
            "description": "Brand colors, fonts, and messaging align with provided inputs",
            "checks": [
                "Brand colors correctly applied in CSS variables",
                "Specified fonts loaded and used consistently",
                "Site name and description match inputs",
                "Tone matches selected preference (professional/playful/luxury/minimal)"
            ],
            "passing_score": 18  # 72% of 25 points
        },
        "seo_best_practices": {
            "weight": 20,
            "description": "SEO metadata complete and optimized",
            "checks": [
                "Title tags present on all pages (<60 characters)",
                "Meta descriptions present (<160 characters)",
                "Heading hierarchy correct (single H1, proper H2-H6 nesting)",
                "Sitemap.xml generated with all pages",
                "Robots.txt configured correctly",
                "OpenGraph tags for social sharing"
            ],
            "passing_score": 15  # 75% of 20 points
        },
        "accessibility_compliance": {
            "weight": 20,
            "description": "WCAG 2.1 AA compliance",
            "checks": [
                "Color contrast ratio ≥4.5:1 for body text",
                "Alt text placeholders for images",
                "Semantic HTML elements (header, nav, main, footer)",
                "Keyboard navigation functional",
                "ARIA labels where appropriate",
                "Form labels properly associated"
            ],
            "passing_score": 14  # 70% of 20 points
        },
        "content_structure": {
            "weight": 15,
            "description": "Content organization and hierarchy",
            "checks": [
                "Clear page hierarchy (Home → About → Services → Contact)",
                "Navigation menu includes all requested pages",
                "Each page has unique, relevant content",
                "Contact form includes required fields",
                "Blog structure present if requested",
                "Footer with copyright and links"
            ],
            "passing_score": 11  # 73% of 15 points
        },
        "navigation_clarity": {
            "weight": 10,
            "description": "Easy to navigate and user-friendly",
            "checks": [
                "Navigation menu visible on all pages",
                "Clear CTAs on homepage",
                "Consistent navigation placement",
                "Mobile menu implemented",
                "Breadcrumbs on deep pages"
            ],
            "passing_score": 7  # 70% of 10 points
        },
        "technical_quality": {
            "weight": 10,
            "description": "Code quality and performance",
            "checks": [
                "No console errors",
                "Valid HTML/CSS",
                "Responsive breakpoints configured",
                "Page load time <3 seconds",
                "Build completes successfully"
            ],
            "passing_score": 7  # 70% of 10 points
        }
    }
    
    # Minimum passing score for approval
    MINIMUM_PASSING_SCORE = 70  # Out of 100 points
    
    # Auto-approval conditions (skip council vote)
    AUTO_APPROVAL_CONDITIONS = {
        "trusted_agent": False,  # Agent has 95%+ approval rating
        "low_risk": False,       # No risk flags triggered
        "template_match": False, # Matches pre-approved template exactly
        "repeat_user": False     # User's 3rd+ approved workflow
    }
    
    # Escalation triggers (requires additional review)
    ESCALATION_TRIGGERS = {
        "youth_targeted": {
            "description": "Content targets users under 18",
            "additional_councils": ["council_youth"],
            "additional_checks": [
                "COPPA compliance",
                "Age-appropriate content",
                "Parental consent mechanisms"
            ]
        },
        "commercial_intent": {
            "description": "Site has commerce keywords (shop, buy, payment)",
            "additional_councils": ["council_commerce"],
            "additional_checks": [
                "Payment processing security",
                "Terms of service present",
                "Privacy policy linked"
            ]
        },
        "authentication_required": {
            "description": "Site handles user accounts/login",
            "additional_councils": ["council_identity_safety"],
            "additional_checks": [
                "Password requirements meet standards",
                "Session management secure",
                "Data encryption implemented"
            ]
        },
        "high_traffic_expected": {
            "description": "User expects >10k visitors/month",
            "additional_councils": ["council_technology"],
            "additional_checks": [
                "CDN configured",
                "Caching strategy implemented",
                "Performance testing completed"
            ]
        }
    }
    
    # Review timeline SLAs
    REVIEW_TIMELINE = {
        "initial_review": timedelta(minutes=5),      # Council member picks it up
        "complete_review": timedelta(minutes=15),    # Full review + vote
        "council_vote": timedelta(minutes=10),       # Voting period
        "total_max": timedelta(minutes=30)           # Maximum time before escalation
    }
    
    # Voting rules
    VOTING_RULES = {
        "quorum": 3,                  # Minimum voters required
        "approval_threshold": 0.51,   # 51% approval needed (simple majority)
        "veto_enabled": False,        # Single member cannot veto
        "abstain_allowed": True       # Members can abstain from voting
    }


def evaluate_workflow(workflow: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate a website creation workflow against review criteria
    
    Args:
        workflow: Workflow object with inputs and generated outputs
    
    Returns:
        evaluation: Dictionary with scores, decision, and feedback
    """
    evaluation = {
        "workflow_id": workflow["id"],
        "evaluated_at": datetime.utcnow().isoformat() + "Z",
        "criteria_scores": {},
        "total_score": 0,
        "passing": False,
        "decision": "pending",
        "feedback": [],
        "escalations": [],
        "estimated_review_time": 15  # minutes
    }
    
    # Check each criteria
    total_score = 0
    for criterion, rules in WebsiteReviewRules.REVIEW_CRITERIA.items():
        # Simulate scoring (in production, run actual checks)
        score = rules["passing_score"]  # Placeholder
        total_score += score
        
        evaluation["criteria_scores"][criterion] = {
            "score": score,
            "max_score": rules["weight"],
            "passing": score >= rules["passing_score"],
            "checks": rules["checks"]
        }
    
    evaluation["total_score"] = total_score
    evaluation["passing"] = total_score >= WebsiteReviewRules.MINIMUM_PASSING_SCORE
    
    # Check for escalations
    inputs = workflow.get("inputs", {})
    
    # Youth-targeted content
    if any(keyword in str(inputs).lower() for keyword in ["kid", "child", "youth", "teen"]):
        evaluation["escalations"].append("youth_targeted")
        evaluation["estimated_review_time"] += 10  # Additional review time
    
    # Commercial intent
    if any(keyword in str(inputs).lower() for keyword in ["shop", "buy", "payment", "store"]):
        evaluation["escalations"].append("commercial_intent")
        evaluation["estimated_review_time"] += 5
    
    # Determine decision
    if evaluation["passing"] and len(evaluation["escalations"]) == 0:
        evaluation["decision"] = "approved"
        evaluation["feedback"].append("✅ All criteria met. Approved for execution.")
    elif evaluation["passing"] and len(evaluation["escalations"]) > 0:
        evaluation["decision"] = "escalated"
        evaluation["feedback"].append(f"⚠️ Passing score achieved, but requires additional review from {len(evaluation['escalations'])} council(s)")
    else:
        evaluation["decision"] = "rejected"
        evaluation["feedback"].append(f"❌ Score {total_score}/100 below minimum threshold of {WebsiteReviewRules.MINIMUM_PASSING_SCORE}")
    
    return evaluation


def check_auto_approval_eligibility(workflow: Dict[str, Any], agent: Dict[str, Any]) -> bool:
    """
    Check if workflow qualifies for auto-approval (skip council vote)
    
    Args:
        workflow: Workflow object
        agent: Agent that created the workflow
    
    Returns:
        eligible: True if auto-approval allowed
    """
    # Check agent trust score
    agent_approval_rate = agent.get("approval_rate", 0.0)
    if agent_approval_rate >= 0.95:
        return True
    
    # Check if user has history of approved workflows
    user_approved_count = 0  # Query from database
    if user_approved_count >= 3:
        return True
    
    # Check risk flags
    risk_flags = workflow.get("governance", {}).get("risk_flags", [])
    if len(risk_flags) == 0:
        return True
    
    return False


def generate_review_checklist(workflow: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate a checklist for council members reviewing this workflow
    
    Args:
        workflow: Workflow object
    
    Returns:
        checklist: List of items to review
    """
    checklist = []
    
    for criterion, rules in WebsiteReviewRules.REVIEW_CRITERIA.items():
        checklist.append({
            "category": criterion,
            "description": rules["description"],
            "weight": rules["weight"],
            "checks": [
                {"description": check, "status": "pending"}
                for check in rules["checks"]
            ]
        })
    
    return checklist


# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    # Example workflow
    example_workflow = {
        "id": "wf_test_123",
        "workflow_type_id": "website.create_basic_site",
        "inputs": {
            "site_name": "Kids Learning Hub",
            "description": "Educational games for children",
            "pages": ["home", "games", "about", "parents"],
            "target_audience": "youth"
        },
        "governance": {
            "risk_flags": ["youth_sensitive"]
        }
    }
    
    # Evaluate
    evaluation = evaluate_workflow(example_workflow)
    
    print("=" * 70)
    print("COUNCIL REVIEW EVALUATION")
    print("=" * 70)
    print(f"Workflow ID: {evaluation['workflow_id']}")
    print(f"Total Score: {evaluation['total_score']}/100")
    print(f"Decision: {evaluation['decision'].upper()}")
    print(f"Estimated Review Time: {evaluation['estimated_review_time']} minutes")
    print()
    
    print("Criteria Scores:")
    for criterion, scores in evaluation["criteria_scores"].items():
        status = "✅" if scores["passing"] else "❌"
        print(f"  {status} {criterion}: {scores['score']}/{scores['max_score']}")
    
    print()
    if evaluation["escalations"]:
        print(f"⚠️ Escalations Required: {', '.join(evaluation['escalations'])}")
    
    print()
    print("Feedback:")
    for feedback in evaluation["feedback"]:
        print(f"  {feedback}")
