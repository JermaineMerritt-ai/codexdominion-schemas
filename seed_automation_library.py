"""
Seed Automation Library with Pre-Built Templates

Creates 20+ ready-to-use automation templates across 5 categories:
- Store (5 templates)
- Marketing (5 templates)
- Website (3 templates)
- Customer Behavior (4 templates)
- Analytics (3 templates)

Usage:
    python seed_automation_library.py
"""

from db import SessionLocal
from models import AutomationTemplate, TriggerType, ActionType, RiskLevel

def seed_library():
    """Seed the automation library with pre-built templates"""
    session = SessionLocal()
    
    try:
        # Clear existing templates (optional - comment out to keep existing)
        # session.query(AutomationTemplate).delete()
        
        templates = []
        
        # ================================================================
        # STORE AUTOMATIONS (5)
        # ================================================================
        
        # 1. Low Inventory Alert
        templates.append(AutomationTemplate(
            id="template_low_inventory_alert",
            name="Low Inventory Alert",
            short_description="Get notified when product count drops below threshold",
            description="Automatically sends notifications when your product inventory falls below a specified threshold, helping you maintain optimal stock levels.",
            icon="bell",
            category="Store",
            trigger_type=TriggerType.THRESHOLD,
            default_trigger_config={
                "metric": "product_count",
                "operator": "<",
                "value": 3
            },
            default_conditions=[
                {"type": "store_status", "operator": "=", "value": "active"}
            ],
            action_type=ActionType.SEND_NOTIFICATION,
            default_action_config={
                "recipients": ["owner"],
                "message": "Product inventory is low. Consider adding more products.",
                "channels": ["email"]
            },
            config_schema=[
                {
                    "key": "threshold",
                    "label": "Minimum Product Count",
                    "type": "number",
                    "default": 3,
                    "required": True,
                    "help_text": "Alert when product count falls below this number",
                    "target": "trigger_config",
                    "target_key": "value"
                }
            ],
            risk_level=RiskLevel.LOW,
            requires_approval=False,
            ai_enhanced=True,
            ai_suggestion_rules={
                "suggest_when": {
                    "product_count": {"operator": "<", "value": 5}
                },
                "suggestion_message": "Your product catalog is low. Enable alerts to stay stocked?"
            },
            popularity_score=85.0,
            success_rate=0.98,
            active=True,
            featured=True
        ))
        
        # 2. Auto-Create Product Drafts
        templates.append(AutomationTemplate(
            id="template_auto_create_products",
            name="Auto-Create Product Drafts",
            short_description="Automatically generate product drafts when inventory is low",
            description="Uses AI to automatically create product draft proposals when your catalog needs expansion, saving hours of manual product creation.",
            icon="package",
            category="Store",
            trigger_type=TriggerType.THRESHOLD,
            default_trigger_config={
                "metric": "product_count",
                "operator": "<",
                "value": 3
            },
            default_conditions=[],
            action_type=ActionType.GENERATE_DRAFT,
            default_action_config={
                "template_id": "standard_product",
                "count": 3,
                "category": "auto_generated"
            },
            config_schema=[
                {
                    "key": "count",
                    "label": "Products to Generate",
                    "type": "number",
                    "default": 3,
                    "required": True,
                    "help_text": "How many product drafts to create",
                    "target": "action_config"
                },
                {
                    "key": "category",
                    "label": "Product Category",
                    "type": "select",
                    "options": ["seasonal", "evergreen", "trending", "bestseller"],
                    "default": "evergreen",
                    "required": True,
                    "target": "action_config"
                }
            ],
            risk_level=RiskLevel.MEDIUM,
            requires_approval=True,
            recommended_council_id="council_commerce",
            ai_enhanced=True,
            ai_suggestion_rules={
                "suggest_when": {
                    "product_count": {"operator": "<", "value": 3},
                    "days_since_last_product": {"operator": ">", "value": 30}
                },
                "suggestion_message": "Your catalog hasn't been updated in 30 days. Auto-generate product drafts?"
            },
            popularity_score=72.0,
            success_rate=0.85,
            active=True,
            featured=True
        ))
        
        # 3. Auto-Tag New Products
        templates.append(AutomationTemplate(
            id="template_auto_tag_products",
            name="Auto-Tag New Products",
            short_description="Automatically tag products based on attributes",
            description="Intelligently tags new products with relevant categories, collections, and labels based on product name, description, and attributes.",
            icon="tag",
            category="Store",
            trigger_type=TriggerType.EVENT,
            default_trigger_config={
                "event_type": "product_added",
                "source": "store"
            },
            default_conditions=[],
            action_type=ActionType.UPDATE_PRODUCT,
            default_action_config={
                "action": "add_tags",
                "ai_analyze": True
            },
            config_schema=[
                {
                    "key": "tag_categories",
                    "label": "Tag Categories",
                    "type": "multiselect",
                    "options": ["season", "color", "style", "occasion", "age_group"],
                    "default": ["season", "style"],
                    "required": True,
                    "help_text": "Which types of tags to auto-generate",
                    "target": "action_config"
                }
            ],
            risk_level=RiskLevel.LOW,
            requires_approval=False,
            ai_enhanced=True,
            ai_suggestion_rules={
                "suggest_when": {
                    "untagged_products": {"operator": ">", "value": 5}
                },
                "suggestion_message": "You have untagged products. Enable auto-tagging to organize your catalog?"
            },
            popularity_score=68.0,
            success_rate=0.92,
            active=True
        ))
        
        # 4. Auto-Generate SEO Descriptions
        templates.append(AutomationTemplate(
            id="template_auto_seo_descriptions",
            name="Auto-Generate SEO Descriptions",
            short_description="Create SEO-optimized descriptions for new products",
            description="Automatically generates compelling, SEO-optimized product descriptions for every new product added to your store.",
            icon="fileText",
            category="Store",
            trigger_type=TriggerType.EVENT,
            default_trigger_config={
                "event_type": "product_added",
                "source": "store"
            },
            default_conditions=[
                {"type": "product_description", "operator": "=", "value": "empty"}
            ],
            action_type=ActionType.UPDATE_PRODUCT,
            default_action_config={
                "action": "generate_description",
                "ai_model": "gpt-4",
                "tone": "professional"
            },
            config_schema=[
                {
                    "key": "tone",
                    "label": "Brand Tone",
                    "type": "select",
                    "options": ["Professional", "Casual", "Luxury", "Playful", "Minimalist"],
                    "default": "Professional",
                    "required": True,
                    "help_text": "The tone of voice for descriptions",
                    "target": "action_config"
                },
                {
                    "key": "length",
                    "label": "Description Length",
                    "type": "select",
                    "options": ["short", "medium", "long"],
                    "default": "medium",
                    "required": True,
                    "target": "action_config"
                }
            ],
            risk_level=RiskLevel.LOW,
            requires_approval=False,
            ai_enhanced=True,
            ai_suggestion_rules={
                "suggest_when": {
                    "products_without_descriptions": {"operator": ">", "value": 3}
                },
                "suggestion_message": "Several products lack descriptions. Enable AI SEO generation?"
            },
            popularity_score=78.0,
            success_rate=0.94,
            active=True,
            featured=True
        ))
        
        # 5. Dynamic Pricing Alerts
        templates.append(AutomationTemplate(
            id="template_pricing_alerts",
            name="Dynamic Pricing Alerts",
            short_description="Get notified of pricing optimization opportunities",
            description="Monitors competitor pricing and market trends, alerting you when pricing adjustments could increase sales or margins.",
            icon="dollarSign",
            category="Store",
            trigger_type=TriggerType.THRESHOLD,
            default_trigger_config={
                "metric": "price_competitiveness",
                "operator": "<",
                "value": 0.7
            },
            default_conditions=[],
            action_type=ActionType.SEND_NOTIFICATION,
            default_action_config={
                "recipients": ["owner"],
                "message": "Pricing optimization opportunity detected",
                "channels": ["email"]
            },
            config_schema=[
                {
                    "key": "sensitivity",
                    "label": "Alert Sensitivity",
                    "type": "select",
                    "options": ["low", "medium", "high"],
                    "default": "medium",
                    "required": True,
                    "help_text": "How often to receive pricing alerts",
                    "target": "action_config"
                }
            ],
            risk_level=RiskLevel.MEDIUM,
            requires_approval=True,
            recommended_council_id="council_commerce",
            popularity_score=55.0,
            success_rate=0.82,
            active=True
        ))
        
        # ================================================================
        # MARKETING AUTOMATIONS (5)
        # ================================================================
        
        # 6. Weekly Social Post Generator
        templates.append(AutomationTemplate(
            id="template_weekly_social_posts",
            name="Weekly Social Post Generator",
            short_description="Automatically create social media posts every week",
            description="Generates a batch of engaging social media posts every Monday, tailored to your brand voice and optimized for each platform.",
            icon="share2",
            category="Marketing",
            trigger_type=TriggerType.SCHEDULE,
            default_trigger_config={
                "pattern": "weekly",
                "day": "monday",
                "time": "09:00",
                "timezone": "UTC"
            },
            default_conditions=[],
            action_type=ActionType.GENERATE_CAMPAIGN,
            default_action_config={
                "template_id": "social_posts",
                "channels": ["instagram"],
                "count": 5,
                "tone": "bold"
            },
            config_schema=[
                {
                    "key": "platforms",
                    "label": "Social Platforms",
                    "type": "multiselect",
                    "options": ["Instagram", "TikTok", "YouTube", "Pinterest", "Facebook"],
                    "default": ["Instagram"],
                    "required": True,
                    "help_text": "Where to post",
                    "target": "action_config",
                    "target_key": "channels"
                },
                {
                    "key": "tone",
                    "label": "Brand Tone",
                    "type": "select",
                    "options": ["Bold", "Minimalist", "Playful", "Luxury", "Casual"],
                    "default": "Bold",
                    "required": True,
                    "target": "action_config"
                },
                {
                    "key": "count",
                    "label": "Posts Per Week",
                    "type": "number",
                    "default": 5,
                    "required": True,
                    "help_text": "How many posts to generate",
                    "target": "action_config"
                },
                {
                    "key": "day",
                    "label": "Scheduled Day",
                    "type": "select",
                    "options": ["monday", "tuesday", "wednesday", "thursday", "friday"],
                    "default": "monday",
                    "required": True,
                    "target": "trigger_config"
                }
            ],
            risk_level=RiskLevel.LOW,
            requires_approval=False,
            ai_enhanced=True,
            ai_suggestion_rules={
                "suggest_when": {
                    "recent_campaigns": {"operator": "=", "value": 0},
                    "store_age_days": {"operator": ">", "value": 7}
                },
                "suggestion_message": "Start posting regularly on social media with automated content?"
            },
            popularity_score=92.0,
            success_rate=0.96,
            avg_value_generated=250.0,
            active=True,
            featured=True
        ))
        
        # 7. Monthly Email Newsletter
        templates.append(AutomationTemplate(
            id="template_monthly_newsletter",
            name="Monthly Email Newsletter",
            short_description="Auto-generate and send monthly newsletters to customers",
            description="Creates and sends a monthly newsletter featuring your best products, latest updates, and exclusive offers to your customer list.",
            icon="mail",
            category="Marketing",
            trigger_type=TriggerType.SCHEDULE,
            default_trigger_config={
                "pattern": "monthly",
                "date": 1,
                "time": "10:00",
                "timezone": "UTC"
            },
            default_conditions=[],
            action_type=ActionType.GENERATE_CAMPAIGN,
            default_action_config={
                "template_id": "newsletter",
                "channels": ["email"],
                "include_products": True,
                "product_count": 5
            },
            config_schema=[
                {
                    "key": "product_count",
                    "label": "Featured Products",
                    "type": "number",
                    "default": 5,
                    "required": True,
                    "help_text": "How many products to feature",
                    "target": "action_config"
                },
                {
                    "key": "tone",
                    "label": "Newsletter Tone",
                    "type": "select",
                    "options": ["Professional", "Friendly", "Casual", "Luxury"],
                    "default": "Friendly",
                    "required": True,
                    "target": "action_config"
                }
            ],
            risk_level=RiskLevel.MEDIUM,
            requires_approval=True,
            recommended_council_id="council_media",
            ai_enhanced=True,
            popularity_score=74.0,
            success_rate=0.88,
            avg_value_generated=500.0,
            active=True,
            featured=True
        ))
        
        # 8. Seasonal Campaign Generator
        templates.append(AutomationTemplate(
            id="template_seasonal_campaigns",
            name="Seasonal Campaign Generator",
            short_description="Launch campaigns for holidays and seasons automatically",
            description="Automatically creates and launches marketing campaigns for major holidays and seasonal events throughout the year.",
            icon="calendar",
            category="Marketing",
            trigger_type=TriggerType.SCHEDULE,
            default_trigger_config={
                "pattern": "seasonal",
                "season": "winter",
                "days_before": 14
            },
            default_conditions=[],
            action_type=ActionType.GENERATE_CAMPAIGN,
            default_action_config={
                "template_id": "seasonal_promo",
                "channels": ["email", "social"],
                "duration_days": 30
            },
            config_schema=[
                {
                    "key": "seasons",
                    "label": "Active Seasons",
                    "type": "multiselect",
                    "options": ["Spring", "Summer", "Fall", "Winter", "Christmas", "Valentine's Day", "Easter", "Halloween"],
                    "default": ["Winter", "Christmas"],
                    "required": True,
                    "help_text": "Which seasons to auto-launch campaigns for",
                    "target": "action_config"
                },
                {
                    "key": "duration_days",
                    "label": "Campaign Duration (days)",
                    "type": "number",
                    "default": 30,
                    "required": True,
                    "target": "action_config"
                }
            ],
            risk_level=RiskLevel.MEDIUM,
            requires_approval=True,
            recommended_council_id="council_media",
            ai_enhanced=True,
            ai_suggestion_rules={
                "suggest_when": {
                    "seasonal_context": {"operator": "=", "value": "holiday_season"}
                },
                "suggestion_message": "Holiday season is approaching. Enable automated seasonal campaigns?"
            },
            popularity_score=81.0,
            success_rate=0.91,
            avg_value_generated=800.0,
            active=True,
            featured=True
        ))
        
        # 9. Product Launch Campaigns
        templates.append(AutomationTemplate(
            id="template_product_launch_campaigns",
            name="Auto-Generate Launch Campaigns",
            short_description="Create campaigns for every new product launch",
            description="Automatically generates comprehensive launch campaigns including social posts, email announcements, and landing pages for each new product.",
            icon="rocket",
            category="Marketing",
            trigger_type=TriggerType.EVENT,
            default_trigger_config={
                "event_type": "product_added",
                "source": "store"
            },
            default_conditions=[
                {"type": "product_price", "operator": ">", "value": 50}
            ],
            action_type=ActionType.GENERATE_CAMPAIGN,
            default_action_config={
                "template_id": "product_launch",
                "channels": ["email", "social"],
                "create_landing_page": True
            },
            config_schema=[
                {
                    "key": "channels",
                    "label": "Marketing Channels",
                    "type": "multiselect",
                    "options": ["email", "social", "ads", "sms"],
                    "default": ["email", "social"],
                    "required": True,
                    "target": "action_config"
                },
                {
                    "key": "minimum_price",
                    "label": "Minimum Product Price",
                    "type": "number",
                    "default": 50,
                    "required": True,
                    "help_text": "Only launch campaigns for products above this price",
                    "target": "conditions",
                    "target_key": "value"
                }
            ],
            risk_level=RiskLevel.MEDIUM,
            requires_approval=True,
            recommended_council_id="council_media",
            popularity_score=65.0,
            success_rate=0.87,
            active=True
        ))
        
        # 10. Re-engagement Campaign
        templates.append(AutomationTemplate(
            id="template_reengagement_campaign",
            name="Customer Re-engagement Campaign",
            short_description="Win back inactive customers automatically",
            description="Automatically identifies and reaches out to customers who haven't made a purchase in 90 days with personalized offers.",
            icon="userCheck",
            category="Marketing",
            trigger_type=TriggerType.BEHAVIOR,
            default_trigger_config={
                "behavior_type": "dormant_customer",
                "days": 90
            },
            default_conditions=[],
            action_type=ActionType.SEND_NOTIFICATION,
            default_action_config={
                "template_id": "winback_email",
                "channels": ["email"],
                "offer": "10% discount"
            },
            config_schema=[
                {
                    "key": "days",
                    "label": "Days Inactive",
                    "type": "number",
                    "default": 90,
                    "required": True,
                    "help_text": "Trigger after this many days of inactivity",
                    "target": "trigger_config"
                },
                {
                    "key": "offer",
                    "label": "Incentive",
                    "type": "select",
                    "options": ["10% discount", "15% discount", "20% discount", "Free shipping", "Free gift"],
                    "default": "10% discount",
                    "required": True,
                    "target": "action_config"
                }
            ],
            risk_level=RiskLevel.LOW,
            requires_approval=False,
            ai_enhanced=True,
            ai_suggestion_rules={
                "suggest_when": {
                    "customer_engagement": {"operator": "=", "value": "low"}
                },
                "suggestion_message": "Customer engagement is low. Enable re-engagement campaigns?"
            },
            popularity_score=69.0,
            success_rate=0.79,
            avg_value_generated=350.0,
            active=True
        ))
        
        # ================================================================
        # WEBSITE AUTOMATIONS (3)
        # ================================================================
        
        # 11. Auto-Update Homepage Hero
        templates.append(AutomationTemplate(
            id="template_auto_homepage_hero",
            name="Auto-Update Homepage Hero",
            short_description="Keep homepage fresh with bestseller highlights",
            description="Automatically updates your homepage hero section to feature your current best-selling or trending products.",
            icon="monitor",
            category="Website",
            trigger_type=TriggerType.SCHEDULE,
            default_trigger_config={
                "pattern": "weekly",
                "day": "monday",
                "time": "06:00",
                "timezone": "UTC"
            },
            default_conditions=[],
            action_type=ActionType.UPDATE_STORE,
            default_action_config={
                "section": "homepage_hero",
                "criteria": "bestsellers",
                "count": 3
            },
            config_schema=[
                {
                    "key": "criteria",
                    "label": "Featured Products",
                    "type": "select",
                    "options": ["bestsellers", "newest", "trending", "seasonal"],
                    "default": "bestsellers",
                    "required": True,
                    "help_text": "Which products to feature",
                    "target": "action_config"
                },
                {
                    "key": "update_frequency",
                    "label": "Update Frequency",
                    "type": "select",
                    "options": ["daily", "weekly", "biweekly"],
                    "default": "weekly",
                    "required": True,
                    "target": "trigger_config",
                    "target_key": "pattern"
                }
            ],
            risk_level=RiskLevel.MEDIUM,
            requires_approval=True,
            recommended_council_id="council_web",
            popularity_score=58.0,
            success_rate=0.93,
            active=True,
            featured=True
        ))
        
        # 12. Auto-Create Landing Pages
        templates.append(AutomationTemplate(
            id="template_auto_landing_pages",
            name="Auto-Create Landing Pages",
            short_description="Generate landing pages for bestsellers and collections",
            description="Automatically creates dedicated landing pages for top-selling products and new collections to maximize conversions.",
            icon="layout",
            category="Website",
            trigger_type=TriggerType.THRESHOLD,
            default_trigger_config={
                "metric": "product_sales",
                "operator": ">",
                "value": 100
            },
            default_conditions=[],
            action_type=ActionType.CREATE_LANDING_PAGE,
            default_action_config={
                "template_id": "product_landing",
                "seo_optimized": True
            },
            config_schema=[
                {
                    "key": "sales_threshold",
                    "label": "Sales Threshold",
                    "type": "number",
                    "default": 100,
                    "required": True,
                    "help_text": "Create landing page after this many sales",
                    "target": "trigger_config",
                    "target_key": "value"
                },
                {
                    "key": "page_style",
                    "label": "Page Style",
                    "type": "select",
                    "options": ["minimal", "detailed", "video-focused", "testimonial-heavy"],
                    "default": "detailed",
                    "required": True,
                    "target": "action_config"
                }
            ],
            risk_level=RiskLevel.HIGH,
            requires_approval=True,
            recommended_council_id="council_web",
            popularity_score=48.0,
            success_rate=0.84,
            avg_value_generated=600.0,
            active=True
        ))
        
        # 13. SEO Meta Tag Updater
        templates.append(AutomationTemplate(
            id="template_seo_meta_updater",
            name="SEO Meta Tag Updater",
            short_description="Keep SEO meta tags fresh and optimized",
            description="Periodically reviews and updates meta titles, descriptions, and keywords based on search trends and performance data.",
            icon="search",
            category="Website",
            trigger_type=TriggerType.SCHEDULE,
            default_trigger_config={
                "pattern": "monthly",
                "date": 1,
                "time": "02:00"
            },
            default_conditions=[],
            action_type=ActionType.UPDATE_STORE,
            default_action_config={
                "action": "update_seo_meta",
                "ai_optimize": True
            },
            config_schema=[
                {
                    "key": "update_frequency",
                    "label": "Update Frequency",
                    "type": "select",
                    "options": ["weekly", "monthly", "quarterly"],
                    "default": "monthly",
                    "required": True,
                    "target": "trigger_config",
                    "target_key": "pattern"
                }
            ],
            risk_level=RiskLevel.MEDIUM,
            requires_approval=True,
            recommended_council_id="council_web",
            popularity_score=51.0,
            success_rate=0.89,
            active=True
        ))
        
        # ================================================================
        # CUSTOMER BEHAVIOR AUTOMATIONS (4)
        # ================================================================
        
        # 14. Abandoned Cart Sequence
        templates.append(AutomationTemplate(
            id="template_abandoned_cart",
            name="Abandoned Cart Recovery",
            short_description="Recover lost sales with automated cart reminders",
            description="Automatically sends a series of emails to customers who abandoned their carts, with personalized incentives to complete their purchase.",
            icon="shoppingCart",
            category="Customer Behavior",
            trigger_type=TriggerType.BEHAVIOR,
            default_trigger_config={
                "behavior_type": "abandoned_cart",
                "timeframe_hours": 24
            },
            default_conditions=[],
            action_type=ActionType.SEND_NOTIFICATION,
            default_action_config={
                "template_id": "cart_recovery",
                "channels": ["email"],
                "delay_hours": 1,
                "discount": "10%"
            },
            config_schema=[
                {
                    "key": "delay_hours",
                    "label": "Delay Before First Email",
                    "type": "number",
                    "default": 1,
                    "required": True,
                    "help_text": "Hours to wait before sending first reminder",
                    "target": "action_config"
                },
                {
                    "key": "discount",
                    "label": "Discount Offer",
                    "type": "select",
                    "options": ["None", "5%", "10%", "15%", "20%", "Free shipping"],
                    "default": "10%",
                    "required": False,
                    "target": "action_config"
                },
                {
                    "key": "tone",
                    "label": "Message Tone",
                    "type": "select",
                    "options": ["Friendly", "Urgent", "Casual", "Professional"],
                    "default": "Friendly",
                    "required": True,
                    "target": "action_config"
                }
            ],
            risk_level=RiskLevel.LOW,
            requires_approval=False,
            ai_enhanced=True,
            ai_suggestion_rules={
                "suggest_when": {
                    "cart_abandonment_rate": {"operator": ">", "value": 0.5}
                },
                "suggestion_message": "Your cart abandonment rate is high. Enable recovery automation?"
            },
            popularity_score=88.0,
            success_rate=0.76,
            avg_value_generated=450.0,
            active=True,
            featured=True
        ))
        
        # 15. Post-Purchase Follow-Up
        templates.append(AutomationTemplate(
            id="template_post_purchase",
            name="Post-Purchase Follow-Up",
            short_description="Build loyalty with automated thank you sequences",
            description="Sends a series of follow-up emails after purchase: thank you, product tips, review request, and cross-sell recommendations.",
            icon="heart",
            category="Customer Behavior",
            trigger_type=TriggerType.EVENT,
            default_trigger_config={
                "event_type": "order_completed",
                "source": "store"
            },
            default_conditions=[],
            action_type=ActionType.SEND_NOTIFICATION,
            default_action_config={
                "template_id": "post_purchase_sequence",
                "channels": ["email"],
                "sequence_length": 3
            },
            config_schema=[
                {
                    "key": "sequence_length",
                    "label": "Number of Follow-Ups",
                    "type": "number",
                    "default": 3,
                    "required": True,
                    "help_text": "How many follow-up emails to send",
                    "target": "action_config"
                },
                {
                    "key": "request_review",
                    "label": "Request Review",
                    "type": "select",
                    "options": ["Yes", "No"],
                    "default": "Yes",
                    "required": True,
                    "target": "action_config"
                }
            ],
            risk_level=RiskLevel.LOW,
            requires_approval=False,
            popularity_score=79.0,
            success_rate=0.91,
            avg_value_generated=200.0,
            active=True,
            featured=True
        ))
        
        # 16. Repeat Customer Rewards
        templates.append(AutomationTemplate(
            id="template_repeat_customer_rewards",
            name="Repeat Customer Rewards",
            short_description="Automatically reward loyal repeat customers",
            description="Identifies repeat customers and sends personalized rewards, discounts, or early access to new products to build loyalty.",
            icon="gift",
            category="Customer Behavior",
            trigger_type=TriggerType.BEHAVIOR,
            default_trigger_config={
                "behavior_type": "repeat_purchase",
                "threshold": 3
            },
            default_conditions=[],
            action_type=ActionType.SEND_NOTIFICATION,
            default_action_config={
                "template_id": "loyalty_reward",
                "channels": ["email"],
                "reward": "15% VIP discount"
            },
            config_schema=[
                {
                    "key": "threshold",
                    "label": "Purchase Threshold",
                    "type": "number",
                    "default": 3,
                    "required": True,
                    "help_text": "Reward after this many purchases",
                    "target": "trigger_config"
                },
                {
                    "key": "reward",
                    "label": "Reward Type",
                    "type": "select",
                    "options": ["15% VIP discount", "20% VIP discount", "Early access", "Free gift", "Free shipping forever"],
                    "default": "15% VIP discount",
                    "required": True,
                    "target": "action_config"
                }
            ],
            risk_level=RiskLevel.MEDIUM,
            requires_approval=True,
            recommended_council_id="council_commerce",
            popularity_score=71.0,
            success_rate=0.86,
            avg_value_generated=300.0,
            active=True
        ))
        
        # 17. High-Value Customer Alert
        templates.append(AutomationTemplate(
            id="template_high_value_customer",
            name="High-Value Customer Alert",
            short_description="Get notified when VIP customers make purchases",
            description="Alerts you when high-value customers (based on lifetime spend) make purchases so you can provide white-glove service.",
            icon="star",
            category="Customer Behavior",
            trigger_type=TriggerType.BEHAVIOR,
            default_trigger_config={
                "behavior_type": "high_value_customer",
                "lifetime_value_threshold": 1000
            },
            default_conditions=[],
            action_type=ActionType.SEND_NOTIFICATION,
            default_action_config={
                "recipients": ["owner"],
                "message": "VIP customer made a purchase",
                "channels": ["email", "push"]
            },
            config_schema=[
                {
                    "key": "lifetime_value_threshold",
                    "label": "VIP Threshold ($)",
                    "type": "number",
                    "default": 1000,
                    "required": True,
                    "help_text": "Consider customers above this value as VIP",
                    "target": "trigger_config"
                }
            ],
            risk_level=RiskLevel.LOW,
            requires_approval=False,
            popularity_score=45.0,
            success_rate=0.97,
            active=True
        ))
        
        # ================================================================
        # ANALYTICS AUTOMATIONS (3)
        # ================================================================
        
        # 18. Weekly Performance Summary
        templates.append(AutomationTemplate(
            id="template_weekly_summary",
            name="Weekly Performance Summary",
            short_description="Get weekly business metrics and insights delivered",
            description="Automatically compiles and sends a comprehensive weekly report with sales, traffic, conversions, and AI-powered insights.",
            icon="barChart",
            category="Analytics",
            trigger_type=TriggerType.SCHEDULE,
            default_trigger_config={
                "pattern": "weekly",
                "day": "monday",
                "time": "08:00",
                "timezone": "UTC"
            },
            default_conditions=[],
            action_type=ActionType.SEND_NOTIFICATION,
            default_action_config={
                "recipients": ["owner"],
                "template_id": "weekly_report",
                "channels": ["email"],
                "include_charts": True
            },
            config_schema=[
                {
                    "key": "day",
                    "label": "Report Day",
                    "type": "select",
                    "options": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
                    "default": "monday",
                    "required": True,
                    "target": "trigger_config"
                },
                {
                    "key": "include_recommendations",
                    "label": "Include AI Recommendations",
                    "type": "select",
                    "options": ["Yes", "No"],
                    "default": "Yes",
                    "required": True,
                    "target": "action_config"
                }
            ],
            risk_level=RiskLevel.LOW,
            requires_approval=False,
            popularity_score=82.0,
            success_rate=0.99,
            active=True,
            featured=True
        ))
        
        # 19. Conversion Drop Alert
        templates.append(AutomationTemplate(
            id="template_conversion_drop_alert",
            name="Conversion Drop Alert",
            short_description="Get notified when conversion rates decline",
            description="Monitors your conversion rate and sends alerts when it drops below historical average, helping you respond quickly to issues.",
            icon="trendingDown",
            category="Analytics",
            trigger_type=TriggerType.THRESHOLD,
            default_trigger_config={
                "metric": "conversion_rate",
                "operator": "<",
                "value": 0.02
            },
            default_conditions=[],
            action_type=ActionType.SEND_NOTIFICATION,
            default_action_config={
                "recipients": ["owner"],
                "message": "Conversion rate has dropped significantly",
                "channels": ["email", "push"],
                "include_analysis": True
            },
            config_schema=[
                {
                    "key": "threshold",
                    "label": "Alert Threshold",
                    "type": "number",
                    "default": 0.02,
                    "required": True,
                    "help_text": "Alert when conversion rate drops below this value",
                    "target": "trigger_config",
                    "target_key": "value"
                }
            ],
            risk_level=RiskLevel.LOW,
            requires_approval=False,
            ai_enhanced=True,
            ai_suggestion_rules={
                "suggest_when": {
                    "conversion_trend": {"operator": "=", "value": "declining"}
                },
                "suggestion_message": "Your conversion rate is trending down. Enable drop alerts?"
            },
            popularity_score=66.0,
            success_rate=0.94,
            active=True
        ))
        
        # 20. Traffic Spike Alert
        templates.append(AutomationTemplate(
            id="template_traffic_spike_alert",
            name="Traffic Spike Alert",
            short_description="Know when your traffic surges unexpectedly",
            description="Alerts you when website traffic spikes significantly, indicating viral content, successful campaigns, or potential issues.",
            icon="trendingUp",
            category="Analytics",
            trigger_type=TriggerType.THRESHOLD,
            default_trigger_config={
                "metric": "hourly_visitors",
                "operator": ">",
                "value": 1000
            },
            default_conditions=[],
            action_type=ActionType.SEND_NOTIFICATION,
            default_action_config={
                "recipients": ["owner"],
                "message": "Website traffic is spiking",
                "channels": ["email", "push"]
            },
            config_schema=[
                {
                    "key": "threshold",
                    "label": "Spike Threshold",
                    "type": "number",
                    "default": 1000,
                    "required": True,
                    "help_text": "Alert when hourly visitors exceed this number",
                    "target": "trigger_config",
                    "target_key": "value"
                }
            ],
            risk_level=RiskLevel.LOW,
            requires_approval=False,
            popularity_score=54.0,
            success_rate=0.96,
            active=True
        ))
        
        # Add all templates to session
        for template in templates:
            session.add(template)
        
        session.commit()
        
        print(f"✓ Successfully seeded {len(templates)} automation templates:")
        print(f"  - Store: {sum(1 for t in templates if t.category == 'Store')}")
        print(f"  - Marketing: {sum(1 for t in templates if t.category == 'Marketing')}")
        print(f"  - Website: {sum(1 for t in templates if t.category == 'Website')}")
        print(f"  - Customer Behavior: {sum(1 for t in templates if t.category == 'Customer Behavior')}")
        print(f"  - Analytics: {sum(1 for t in templates if t.category == 'Analytics')}")
        print(f"  - Featured: {sum(1 for t in templates if t.featured)}")
        print(f"  - AI-Enhanced: {sum(1 for t in templates if t.ai_enhanced)}")
        
    except Exception as e:
        session.rollback()
        print(f"Error seeding automation library: {str(e)}")
        raise
    
    finally:
        session.close()


if __name__ == '__main__':
    print("🔥 Seeding Automation Library...")
    seed_library()
    print("🔥 The Library Burns Sovereign and Eternal!")
