# E-commerce Website Creation Workflow Type Definition
# ======================================================
# Commercial variant - routes to COMMERCE COUNCIL automatically

WORKFLOW_TYPE_ECOMMERCE_WEBSITE = {
    "id": "website.create_ecommerce_site",
    "name": "Create E-commerce Website",
    "domain": "commerce",  # 🔥 Routes to COMMERCE COUNCIL instead of Media
    "description": "Creates a complete e-commerce store with product catalog, shopping cart, checkout, and payment integration",
    "category": "website_builder",
    "estimated_duration_minutes": 25,
    "required_inputs": {
        "site_name": {
            "type": "string",
            "description": "Store name/brand",
            "required": True,
            "example": "Codex Premium Templates"
        },
        "description": {
            "type": "text",
            "description": "Store description for SEO and homepage",
            "required": True,
            "example": "Premium digital products and design templates for modern businesses"
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
            "default": ["home", "shop", "product", "cart", "checkout", "account"],
            "options": ["home", "shop", "product", "cart", "checkout", "account", "about", "contact", "blog"]
        },
        "product_categories": {
            "type": "array",
            "description": "Product categories for the store",
            "required": True,
            "example": ["Templates", "Graphics", "Courses", "Ebooks"]
        },
        "payment_methods": {
            "type": "array",
            "description": "Payment methods to integrate",
            "required": False,
            "default": ["stripe", "paypal"],
            "options": ["stripe", "paypal", "square", "coinbase"]
        },
        "shipping_enabled": {
            "type": "boolean",
            "description": "Enable physical product shipping",
            "required": False,
            "default": False
        },
        "target_audience": {
            "type": "string",
            "description": "Primary customer demographic",
            "required": False,
            "example": "Small business owners and entrepreneurs"
        },
        "tone": {
            "type": "string",
            "description": "Brand voice and tone",
            "required": False,
            "default": "professional",
            "options": ["professional", "playful", "luxury", "minimal"]
        },
        "platform": {
            "type": "string",
            "description": "E-commerce platform",
            "required": False,
            "default": "nextjs",
            "options": ["nextjs", "shopify", "woocommerce"]
        },
        "contact_email": {
            "type": "email",
            "description": "Customer support email",
            "required": True,
            "example": "support@codexstore.app"
        }
    },
    "default_calculator_profile": {
        "tasks_per_week": 10,
        "time_per_task_minutes": 90,  # E-commerce takes longer
        "hourly_wage": 75,
        "automation_percent": 0.80,
        "error_rate": 0.08,
        "cost_per_error": 50,  # Higher error cost for commerce
        "value_per_accelerated_task": 100  # Faster time-to-market value
    },
    "outputs": [
        {
            "name": "site_url",
            "type": "string",
            "description": "Public store URL"
        },
        {
            "name": "pages_created",
            "type": "array",
            "description": "List of page URLs created"
        },
        {
            "name": "admin_url",
            "type": "string",
            "description": "Store admin dashboard URL"
        },
        {
            "name": "payment_integration_status",
            "type": "object",
            "description": "Status of payment gateway integrations"
        },
        {
            "name": "asset_urls",
            "type": "object",
            "description": "URLs to generated assets"
        },
        {
            "name": "deployment_id",
            "type": "string",
            "description": "Deployment identifier"
        }
    ],
    "calculated_savings": {
        "tasks_automated": "E-commerce store setup with payment integration",
        "time_saved_per_week": 900,  # 15 hours
        "hourly_rate": 75,
        "weekly_savings": 1125.0,
        "annual_savings": 58500.0
    },
    "execution_steps": [
        "Generate store structure JSON",
        "Generate product catalog schema",
        "Setup shopping cart and checkout flow",
        "Integrate payment gateway (Stripe/PayPal)",
        "Generate SEO metadata for products",
        "Apply brand theme and styling",
        "Generate Next.js/Shopify project scaffold",
        "Configure inventory management",
        "Setup customer account system",
        "Commit scaffold to GitHub repository",
        "Deploy to production (Vercel/Shopify)",
        "Run payment integration tests",
        "Return store URL and admin credentials"
    ],
    "governance": {
        "requires_review": True,
        "review_council": "council_commerce",  # 🔥 COMMERCE COUNCIL REVIEW
        "auto_execute_if_low_risk": False,
        "risk_flags": [
            "handles_payments",
            "stores_customer_data",
            "brand_sensitive",
            "high_value_transactions"
        ],
        "approval_threshold": "simple_majority",
        "review_criteria": [
            "Payment security compliance (PCI DSS)",
            "Customer data protection (GDPR/CCPA)",
            "Transaction flow accuracy",
            "Refund policy clarity",
            "Brand consistency",
            "SEO optimization for products",
            "Mobile commerce experience",
            "Cart abandonment optimization"
        ]
    },
    "success_criteria": [
        "All pages render without errors",
        "Shopping cart functionality verified",
        "Checkout process completes successfully",
        "Payment gateway integration tested",
        "Product catalog loads correctly",
        "Mobile responsive design verified",
        "Page load time < 3 seconds",
        "SSL certificate active"
    ],
    "failure_conditions": [
        "Payment integration fails",
        "Checkout process broken",
        "Security vulnerabilities detected",
        "Cart calculations incorrect",
        "Deployment fails after 3 retries"
    ],
    "tags": ["ecommerce", "store", "shop", "payments", "commerce", "retail"],
    "version": "1.0.0",
    "created_at": "2025-12-20T00:00:00Z",
    "updated_at": "2025-12-20T00:00:00Z"
}


# ==================== WORKFLOW TYPE REGISTRATION ====================

def register_ecommerce_website_workflow():
    """Register the e-commerce website creation workflow type"""
    from db import SessionLocal
    from models import WorkflowType
    
    session = SessionLocal()
    try:
        existing = session.query(WorkflowType).filter(
            WorkflowType.id == WORKFLOW_TYPE_ECOMMERCE_WEBSITE["id"]
        ).first()
        
        if existing:
            print(f"✅ E-commerce workflow '{WORKFLOW_TYPE_ECOMMERCE_WEBSITE['id']}' already registered")
            return existing
        
        workflow_type = WorkflowType(
            id=WORKFLOW_TYPE_ECOMMERCE_WEBSITE["id"],
            name=WORKFLOW_TYPE_ECOMMERCE_WEBSITE["name"],
            domain=WORKFLOW_TYPE_ECOMMERCE_WEBSITE["domain"],
            description=WORKFLOW_TYPE_ECOMMERCE_WEBSITE["description"],
            required_inputs=WORKFLOW_TYPE_ECOMMERCE_WEBSITE["required_inputs"],
            estimated_savings_weekly=WORKFLOW_TYPE_ECOMMERCE_WEBSITE["calculated_savings"]["weekly_savings"],
            is_active=True
        )
        
        session.add(workflow_type)
        session.commit()
        
        print(f"🔥 E-commerce workflow registered! Routes to COMMERCE COUNCIL")
        print(f"💰 Annual savings: ${WORKFLOW_TYPE_ECOMMERCE_WEBSITE['calculated_savings']['annual_savings']:,.2f}")
        return workflow_type
    except Exception as e:
        session.rollback()
        print(f"❌ Failed to register: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    register_ecommerce_website_workflow()
    print("\n✅ E-commerce website workflow type ready!")
    print("🎯 Auto-routes to: COMMERCE COUNCIL")
    print("💎 Higher value: $58,500/year savings")
