# Website Creation Workflow Type Definition
# ==========================================
# First official CodexDominion workflow for building digital empires

WORKFLOW_TYPE_WEBSITE_CREATION = {
    "id": "website.create_basic_site",
    "name": "Create Basic Website",
    "domain": "media",  # Routes to Media Council
    "description": "Creates a new website scaffold with home, about, contact, blog pages, SEO metadata, and brand styling",
    "category": "website_builder",
    "estimated_duration_minutes": 15,
    "required_inputs": {
        "site_name": {
            "type": "string",
            "description": "Website name/title",
            "required": True,
            "example": "Codex Digital Studios"
        },
        "description": {
            "type": "text",
            "description": "Brief description for SEO and homepage",
            "required": True,
            "example": "Professional web design and development services"
        },
        "brand_colors": {
            "type": "array",
            "description": "Array of hex color codes for brand palette",
            "required": False,
            "default": ["#1a1a1a", "#f7f1e3", "#d4af37"],
            "example": ["#2563eb", "#10b981", "#f59e0b"]
        },
        "primary_font": {
            "type": "string",
            "description": "Font family for headings",
            "required": False,
            "default": "Inter",
            "example": "Montserrat"
        },
        "secondary_font": {
            "type": "string",
            "description": "Font family for body text",
            "required": False,
            "default": "Open Sans",
            "example": "Roboto"
        },
        "pages": {
            "type": "array",
            "description": "List of pages to create",
            "required": False,
            "default": ["home", "about", "contact", "blog"],
            "options": ["home", "about", "contact", "blog", "services", "portfolio", "team", "pricing"]
        },
        "target_audience": {
            "type": "string",
            "description": "Primary target audience for content optimization",
            "required": False,
            "example": "Small businesses seeking web presence"
        },
        "tone": {
            "type": "string",
            "description": "Content tone and voice",
            "required": False,
            "default": "professional",
            "options": ["professional", "playful", "luxury", "minimal"]
        },
        "platform": {
            "type": "string",
            "description": "Target deployment platform",
            "required": False,
            "default": "nextjs",
            "options": ["nextjs", "wordpress", "shopify", "static"]
        },
        "contact_email": {
            "type": "email",
            "description": "Contact form recipient email",
            "required": True,
            "example": "contact@codexdominion.app"
        }
    },
    "default_calculator_profile": {
        "tasks_per_week": 20,
        "time_per_task_minutes": 30,
        "hourly_wage": 40,
        "automation_percent": 0.85,
        "error_rate": 0.05,
        "cost_per_error": 20,
        "value_per_accelerated_task": 0
    },
    "outputs": [
        {
            "name": "site_url",
            "type": "string",
            "description": "Public URL of created site"
        },
        {
            "name": "pages_created",
            "type": "array",
            "description": "List of page URLs created"
        },
        {
            "name": "asset_urls",
            "type": "object",
            "description": "URLs to generated assets (CSS, JS, images)"
        },
        {
            "name": "deployment_id",
            "type": "string",
            "description": "Deployment identifier for tracking"
        }
    ],
    "calculated_savings": {
        "tasks_automated": "Creating 5+ pages manually",
        "time_saved_per_week": 180,  # minutes
        "hourly_rate": 75,  # USD
        "weekly_savings": 225.0,  # USD
        "annual_savings": 11700.0  # USD
    },
    "execution_steps": [
        "Generate site structure JSON",
        "Generate content for each page",
        "Generate SEO metadata",
        "Generate brand theme file",
        "Generate Next.js project scaffold",
        "Commit scaffold to GitHub repository",
        "Trigger deployment pipeline (Vercel/Netlify)",
        "Return deployed URL and repository link"
    ],
    "governance": {
        "requires_review": True,
        "review_council": "council_media",
        "auto_execute_if_low_risk": False,
        "risk_flags": [
            "public_facing",
            "brand_sensitive",
            "youth_sensitive"
        ],
        "approval_threshold": "simple_majority",
        "review_criteria": [
            "Brand consistency",
            "SEO best practices",
            "Accessibility compliance",
            "Content structure",
            "Navigation clarity"
        ]
    },
    "success_criteria": [
        "All pages render without errors",
        "SEO meta tags present on all pages",
        "Contact form sends test email successfully",
        "Site loads in under 3 seconds",
        "Mobile responsive design verified",
        "Accessibility score > 90 (Lighthouse)"
    ],
    "failure_conditions": [
        "Deployment fails after 3 retries",
        "Critical accessibility violations",
        "Broken navigation links",
        "Contact form non-functional",
        "Site not accessible via URL"
    ],
    "tags": ["website", "starter", "scaffold", "seo", "basic"],
    "version": "1.0.0",
    "created_at": "2025-12-20T00:00:00Z",
    "updated_at": "2025-12-20T00:00:00Z"
}


# ==================== WORKFLOW TYPE REGISTRATION ====================

def register_website_creation_workflow():
    """
    Register the website creation workflow type in the database
    
    Usage:
        from workflow_types.website_creation import register_website_creation_workflow
        register_website_creation_workflow()
    """
    from db import SessionLocal
    from models import WorkflowType
    
    session = SessionLocal()
    try:
        # Check if already exists
        existing = session.query(WorkflowType).filter(
            WorkflowType.id == WORKFLOW_TYPE_WEBSITE_CREATION["id"]
        ).first()
        
        if existing:
            print(f"✅ Workflow type '{WORKFLOW_TYPE_WEBSITE_CREATION['id']}' already registered")
            return existing
        
        # Create new workflow type
        workflow_type = WorkflowType(
            id=WORKFLOW_TYPE_WEBSITE_CREATION["id"],
            name=WORKFLOW_TYPE_WEBSITE_CREATION["name"],
            domain=WORKFLOW_TYPE_WEBSITE_CREATION["domain"],
            description=WORKFLOW_TYPE_WEBSITE_CREATION["description"],
            required_inputs=WORKFLOW_TYPE_WEBSITE_CREATION["required_inputs"],
            estimated_savings_weekly=WORKFLOW_TYPE_WEBSITE_CREATION["calculated_savings"]["weekly_savings"],
            is_active=True
        )
        
        session.add(workflow_type)
        session.commit()
        
        print(f"🔥 Workflow type '{WORKFLOW_TYPE_WEBSITE_CREATION['id']}' registered successfully!")
        return workflow_type
    except Exception as e:
        session.rollback()
        print(f"❌ Failed to register workflow type: {e}")
        raise
    finally:
        session.close()


# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    # Register workflow type
    register_website_creation_workflow()
    
    # Example workflow creation
    print("\n" + "="*60)
    print("EXAMPLE: Creating a website workflow")
    print("="*60)
    
    from workflow_engine import workflow_engine
    
    example_inputs = {
        "site_name": "Codex Digital Studios",
        "site_description": "Professional web design and AI-powered development services",
        "brand_colors": {
            "primary": "#1a1a1a",
            "secondary": "#f7f1e3",
            "accent": "#d4af37"
        },
        "typography": {
            "heading": "Inter",
            "body": "Open Sans"
        },
        "pages": ["home", "about", "services", "contact", "blog"],
        "include_blog": True,
        "contact_email": "hello@codexdigital.app"
    }
    
    example_savings = {
        "tasks_automated": "Manual website creation (5 pages)",
        "time_saved_per_week": 180,
        "hourly_rate": 75,
        "weekly_savings": 225.0,
        "total_weekly_savings": 225.0,
        "annual_savings": 11700.0
    }
    
    workflow_id = workflow_engine.create_workflow(
        workflow_type_id="website.create_basic_site",
        created_by_agent="agent_jermaine_super_action",
        inputs=example_inputs,
        calculated_savings=example_savings,
        assigned_council_id="council_media"
    )
    
    print(f"\n✅ Workflow created: {workflow_id}")
    print(f"📊 Weekly savings: ${example_savings['weekly_savings']}")
    print(f"⏱️  Estimated duration: 15 minutes")
    print(f"🏛️  Assigned to: Media Council")
    print(f"\n🔥 The Flame Burns Sovereign and Eternal! 👑")
