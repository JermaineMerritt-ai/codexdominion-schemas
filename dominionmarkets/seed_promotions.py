"""
Seed Promotions - Populate database with identity-specific ecosystem products
Run once to initialize promotion catalog
"""

from db import SessionLocal
from models.promotions import (
    Promotion, PromotionCategory, IdentityType, 
    WidgetType, LocationType
)
from datetime import datetime
import json


def seed_promotions():
    """Seeds promotion catalog with identity-specific products"""
    session = SessionLocal()
    
    promotions = [
        # ====================================================================
        # DIASPORA PRODUCTS
        # ====================================================================
        {
            "product_id": "caribbean_tracker",
            "name": "Caribbean Investment Tracker",
            "description": "Track regional exposure across 20+ Caribbean markets with real-time currency conversion.",
            "price": 14.99,
            "category": PromotionCategory.TEMPLATE,
            "identity_fit": IdentityType.DIASPORA,
            "icon": "globe",
            "cta_text": "Learn More",
            "cta_link": "https://islandnation.app/products/caribbean-tracker",
            "widget_type": WidgetType.PRODUCT_CARD,
            "allowed_locations": ["dashboard", "portfolio", "markets"],
            "contextual_triggers": {
                "trigger_type": "portfolio",
                "conditions": {
                    "international_holdings_min": 0.2
                }
            },
            "priority": 10
        },
        {
            "product_id": "remittance_calculator",
            "name": "Global Remittance Calculator",
            "description": "Compare remittance fees across providers and find the best rates for sending money home.",
            "price": None,  # Free
            "category": PromotionCategory.TOOL,
            "identity_fit": IdentityType.DIASPORA,
            "icon": "dollar-sign",
            "cta_text": "Try Now — Free",
            "cta_link": "https://islandnation.app/tools/remittance",
            "widget_type": WidgetType.FREE_TOOL,
            "allowed_locations": ["dashboard", "news"],
            "priority": 15
        },
        {
            "product_id": "diaspora_flow_maps_pro",
            "name": "Diaspora Flow Maps Pro",
            "description": "Deep-dive analytics for diaspora markets with regional insights and flow tracking.",
            "price": 19.99,
            "category": PromotionCategory.SERVICE,
            "identity_fit": IdentityType.DIASPORA,
            "icon": "trending-up",
            "cta_text": "Explore",
            "cta_link": "https://codexdominion.app/diaspora-flow-maps",
            "widget_type": WidgetType.SERVICE_PROMOTION,
            "allowed_locations": ["dashboard", "markets"],
            "tier_restrictions": ["premium", "pro"],
            "contextual_triggers": {
                "trigger_type": "activity",
                "conditions": {
                    "news_views_this_week_min": 10
                }
            },
            "priority": 8
        },
        
        # ====================================================================
        # YOUTH PRODUCTS
        # ====================================================================
        {
            "product_id": "first_portfolio_challenge",
            "name": "First Portfolio Challenge",
            "description": "Build your first mock portfolio and learn investing basics with guided challenges.",
            "price": None,  # Free
            "category": PromotionCategory.EDUCATION,
            "identity_fit": IdentityType.YOUTH,
            "icon": "graduation-cap",
            "cta_text": "Start Challenge",
            "cta_link": "https://dominionyouth.app/challenges/first-portfolio",
            "widget_type": WidgetType.FREE_TOOL,
            "allowed_locations": ["dashboard", "portfolio"],
            "contextual_triggers": {
                "trigger_type": "portfolio",
                "conditions": {
                    "portfolio_value_max": 1000
                }
            },
            "priority": 20
        },
        {
            "product_id": "investment_basics_course",
            "name": "Investment Basics Mini-Course",
            "description": "5-part video series covering stocks, bonds, ETFs, and portfolio allocation for beginners.",
            "price": 19.99,
            "category": PromotionCategory.EDUCATION,
            "identity_fit": IdentityType.YOUTH,
            "icon": "graduation-cap",
            "cta_text": "Start Learning",
            "cta_link": "https://dominionyouth.app/courses/investment-basics",
            "widget_type": WidgetType.PRODUCT_CARD,
            "allowed_locations": ["dashboard", "news"],
            "priority": 12
        },
        {
            "product_id": "paper_trading_simulator",
            "name": "Paper Trading Simulator",
            "description": "Practice trading with virtual money. Learn without risk before investing real capital.",
            "price": 4.99,
            "category": PromotionCategory.TOOL,
            "identity_fit": IdentityType.YOUTH,
            "icon": "trending-up",
            "cta_text": "Try Free Trial",
            "cta_link": "https://dominionyouth.app/paper-trading",
            "widget_type": WidgetType.PRODUCT_CARD,
            "allowed_locations": ["dashboard", "portfolio"],
            "contextual_triggers": {
                "trigger_type": "activity",
                "conditions": {
                    "portfolio_checks_today_min": 3
                }
            },
            "priority": 10
        },
        
        # ====================================================================
        # CREATOR PRODUCTS
        # ====================================================================
        {
            "product_id": "business_financial_planner",
            "name": "Business Financial Planner",
            "description": "Excel template for tracking business revenue, expenses, and cash flow projections.",
            "price": 34.99,
            "category": PromotionCategory.TEMPLATE,
            "identity_fit": IdentityType.CREATOR,
            "icon": "file-text",
            "cta_text": "Get Template",
            "cta_link": "https://islandnation.app/products/business-planner",
            "widget_type": WidgetType.PRODUCT_CARD,
            "allowed_locations": ["dashboard", "portfolio"],
            "priority": 10
        },
        {
            "product_id": "creator_revenue_tracker",
            "name": "Creator Revenue Tracker",
            "description": "Track income from YouTube, Patreon, sponsorships, and digital products in one dashboard.",
            "price": 12.99,
            "category": PromotionCategory.TEMPLATE,
            "identity_fit": IdentityType.CREATOR,
            "icon": "dollar-sign",
            "cta_text": "Learn More",
            "cta_link": "https://islandnation.app/products/creator-tracker",
            "widget_type": WidgetType.PRODUCT_CARD,
            "allowed_locations": ["dashboard", "portfolio"],
            "contextual_triggers": {
                "trigger_type": "portfolio",
                "conditions": {
                    "stock_count_min": 3
                }
            },
            "priority": 12
        },
        {
            "product_id": "ai_prompt_packs",
            "name": "AI Prompt Packs for Creators",
            "description": "100+ tested prompts for content creation, video scripts, and business planning.",
            "price": 9.99,
            "category": PromotionCategory.TEMPLATE,
            "identity_fit": IdentityType.CREATOR,
            "icon": "sparkles",
            "cta_text": "Get Prompts",
            "cta_link": "https://islandnation.app/products/ai-prompts",
            "widget_type": WidgetType.PRODUCT_CARD,
            "allowed_locations": ["dashboard", "news"],
            "priority": 8
        },
        {
            "product_id": "creator_economy_analytics",
            "name": "Creator Economy Analytics Dashboard",
            "description": "Track trends in the creator economy with insights on platforms, tools, and monetization.",
            "price": 49.99,
            "category": PromotionCategory.SERVICE,
            "identity_fit": IdentityType.CREATOR,
            "icon": "trending-up",
            "cta_text": "Explore",
            "cta_link": "https://codexdominion.app/creator-analytics",
            "widget_type": WidgetType.SERVICE_PROMOTION,
            "allowed_locations": ["dashboard", "markets"],
            "tier_restrictions": ["premium", "pro"],
            "contextual_triggers": {
                "trigger_type": "activity",
                "conditions": {
                    "alert_count_min": 5
                }
            },
            "priority": 7
        },
        
        # ====================================================================
        # LEGACY PRODUCTS
        # ====================================================================
        {
            "product_id": "retirement_income_planner",
            "name": "Retirement Income Planner",
            "description": "Model retirement income from dividends, Social Security, and withdrawals with tax optimization.",
            "price": 39.99,
            "category": PromotionCategory.TEMPLATE,
            "identity_fit": IdentityType.LEGACY,
            "icon": "file-text",
            "cta_text": "Get Planner",
            "cta_link": "https://islandnation.app/products/retirement-planner",
            "widget_type": WidgetType.PRODUCT_CARD,
            "allowed_locations": ["dashboard", "portfolio"],
            "contextual_triggers": {
                "trigger_type": "portfolio",
                "conditions": {
                    "dividend_stock_count_min": 3
                }
            },
            "priority": 12
        },
        {
            "product_id": "dividend_tracker",
            "name": "Dividend Aristocrats Tracker",
            "description": "Excel tracker for 50+ dividend aristocrats with yield history and payment calendars.",
            "price": 14.99,
            "category": PromotionCategory.TEMPLATE,
            "identity_fit": IdentityType.LEGACY,
            "icon": "dollar-sign",
            "cta_text": "Get Tracker",
            "cta_link": "https://islandnation.app/products/dividend-tracker",
            "widget_type": WidgetType.PRODUCT_CARD,
            "allowed_locations": ["dashboard", "portfolio"],
            "priority": 10
        },
        {
            "product_id": "estate_planning_checklist",
            "name": "Estate Planning Checklist",
            "description": "Free PDF guide covering wills, trusts, beneficiaries, and legacy planning basics.",
            "price": None,  # Free
            "category": PromotionCategory.EDUCATION,
            "identity_fit": IdentityType.LEGACY,
            "icon": "file-text",
            "cta_text": "Download Free",
            "cta_link": "https://islandnation.app/free/estate-planning",
            "widget_type": WidgetType.FREE_TOOL,
            "allowed_locations": ["dashboard", "news"],
            "priority": 15
        },
        {
            "product_id": "wealth_preservation_guide",
            "name": "Wealth Preservation Guide",
            "description": "Comprehensive guide to protecting and growing wealth across generations.",
            "price": 29.99,
            "category": PromotionCategory.EDUCATION,
            "identity_fit": IdentityType.LEGACY,
            "icon": "graduation-cap",
            "cta_text": "Learn More",
            "cta_link": "https://islandnation.app/products/wealth-guide",
            "widget_type": WidgetType.PRODUCT_CARD,
            "allowed_locations": ["dashboard"],
            "tier_restrictions": ["premium", "pro"],
            "priority": 8
        },
        
        # ====================================================================
        # UNIVERSAL PRODUCTS (ALL IDENTITIES)
        # ====================================================================
        {
            "product_id": "diversification_checker",
            "name": "Portfolio Diversification Checker",
            "description": "Free tool to analyze your portfolio balance across sectors, regions, and asset types.",
            "price": None,  # Free
            "category": PromotionCategory.TOOL,
            "identity_fit": IdentityType.ALL,
            "icon": "wrench",
            "cta_text": "Check Now — Free",
            "cta_link": "https://codexdominion.app/tools/diversification",
            "widget_type": WidgetType.FREE_TOOL,
            "allowed_locations": ["dashboard", "portfolio"],
            "contextual_triggers": {
                "trigger_type": "portfolio",
                "conditions": {
                    "sector_concentration_max": 0.4
                }
            },
            "priority": 18
        },
        {
            "product_id": "workflow_automation",
            "name": "Workflow Automation Service",
            "description": "Automate financial tasks, alerts, and reporting with CodexDominion's workflow engine.",
            "price": 39.99,
            "category": PromotionCategory.SERVICE,
            "identity_fit": IdentityType.ALL,
            "icon": "wrench",
            "cta_text": "Explore",
            "cta_link": "https://codexdominion.app/workflow-automation",
            "widget_type": WidgetType.SERVICE_PROMOTION,
            "allowed_locations": ["dashboard", "alerts"],
            "tier_restrictions": ["premium", "pro"],
            "contextual_triggers": {
                "trigger_type": "activity",
                "conditions": {
                    "alert_count_min": 5
                }
            },
            "priority": 9
        },
    ]
    
    # Insert promotions
    try:
        for promo_data in promotions:
            # Check if already exists
            existing = session.query(Promotion).filter_by(
                product_id=promo_data["product_id"]
            ).first()
            
            if existing:
                print(f"⏭️  Skipping {promo_data['product_id']} (already exists)")
                continue
            
            # Convert dict to Promotion model
            promo = Promotion(
                product_id=promo_data["product_id"],
                name=promo_data["name"],
                description=promo_data["description"],
                price=promo_data.get("price"),
                category=promo_data["category"],
                identity_fit=promo_data["identity_fit"],
                icon=promo_data["icon"],
                cta_text=promo_data["cta_text"],
                cta_link=promo_data["cta_link"],
                widget_type=promo_data["widget_type"],
                allowed_locations=promo_data["allowed_locations"],
                tier_restrictions=promo_data.get("tier_restrictions"),
                contextual_triggers=promo_data.get("contextual_triggers"),
                priority=promo_data["priority"],
                is_active=True
            )
            
            session.add(promo)
            print(f"✅ Added {promo_data['product_id']}")
        
        session.commit()
        print(f"\n🎉 Seeded {len(promotions)} promotions successfully!")
    
    except Exception as e:
        session.rollback()
        print(f"❌ Error seeding promotions: {e}")
        raise
    
    finally:
        session.close()


if __name__ == "__main__":
    print("🌱 Seeding Cross-Promotion Catalog...")
    seed_promotions()
