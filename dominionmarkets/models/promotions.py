"""
Cross-Promotion Engine - Database Models
Tracks ecosystem product promotions with identity-based targeting
"""

from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import enum
import uuid

# Import Base from root models.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from models import Base


# ============================================================================
# ENUMS
# ============================================================================

class PromotionCategory(enum.Enum):
    """Product category types"""
    TEMPLATE = "template"  # Excel, PDF, Notion templates
    TOOL = "tool"  # Web tools, calculators
    SERVICE = "service"  # SaaS subscriptions
    EDUCATION = "education"  # Courses, guides, workbooks


class IdentityType(enum.Enum):
    """User identity personas"""
    DIASPORA = "diaspora"
    YOUTH = "youth"
    CREATOR = "creator"
    LEGACY = "legacy"
    ALL = "all"  # Universal products


class WidgetType(enum.Enum):
    """Promotion display format"""
    PRODUCT_CARD = "product_card"  # Standard product display
    FREE_TOOL = "free_tool"  # Free offering highlight
    SERVICE_PROMOTION = "service_promotion"  # SaaS service promo
    INLINE_LINK = "inline_link"  # Contextual text link


class LocationType(enum.Enum):
    """Where promotions can appear"""
    DASHBOARD = "dashboard"  # Right sidebar
    PORTFOLIO = "portfolio"  # After holdings table
    MARKETS = "markets"  # After heatmap
    NEWS = "news"  # Between articles
    ALERTS = "alerts"  # Empty state or list


class InteractionAction(enum.Enum):
    """User interaction types"""
    IMPRESSION = "impression"  # Viewed promotion
    CLICK = "click"  # Clicked CTA
    DISMISS = "dismiss"  # Dismissed promotion
    RESTORE = "restore"  # Restored dismissed promotion


class DismissalReason(enum.Enum):
    """Why user dismissed promotion"""
    NOT_INTERESTED = "not_interested"
    ALREADY_HAVE = "already_have"
    TOO_EXPENSIVE = "too_expensive"
    OTHER = "other"


# ============================================================================
# MODELS
# ============================================================================

class Promotion(Base):
    """
    Ecosystem product catalog for cross-promotion.
    Defines what products can be promoted and their targeting rules.
    """
    __tablename__ = "promotions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Product Details
    product_id = Column(String(100), nullable=False, unique=True, index=True)  # e.g., "caribbean_tracker"
    name = Column(String(200), nullable=False)  # "Caribbean Investment Tracker"
    description = Column(Text, nullable=False)  # Short pitch (1-2 sentences)
    long_description = Column(Text, nullable=True)  # Full details for modal
    
    # Pricing
    price = Column(Float, nullable=True)  # null for free products
    currency = Column(String(3), nullable=False, default="USD")
    original_price = Column(Float, nullable=True)  # For showing discounts
    
    # Categorization
    category = Column(SQLEnum(PromotionCategory), nullable=False, index=True)
    identity_fit = Column(SQLEnum(IdentityType), nullable=False, index=True)  # Primary target identity
    secondary_identities = Column(JSON, nullable=True)  # List of secondary fits
    
    # Display
    icon = Column(String(50), nullable=False)  # Lucide icon name
    image_url = Column(String(500), nullable=True)  # Optional product image
    cta_text = Column(String(50), nullable=False, default="Learn More")
    cta_link = Column(String(500), nullable=False)  # External product URL
    widget_type = Column(SQLEnum(WidgetType), nullable=False, default=WidgetType.PRODUCT_CARD)
    
    # Targeting Rules
    allowed_locations = Column(JSON, nullable=False)  # List of LocationType values
    tier_restrictions = Column(JSON, nullable=True)  # null = all tiers, or ["free", "premium", "pro"]
    contextual_triggers = Column(JSON, nullable=True)  # Conditions for display (see below)
    
    # Limits
    max_impressions_per_user = Column(Integer, nullable=False, default=10)  # Cap per month
    max_global_impressions = Column(Integer, nullable=True)  # Total cap across all users
    current_global_impressions = Column(Integer, nullable=False, default=0)
    
    # Status
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    start_date = Column(DateTime, nullable=True)  # Campaign start
    end_date = Column(DateTime, nullable=True)  # Campaign end
    priority = Column(Integer, nullable=False, default=0)  # Higher = shown first
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    interactions = relationship("UserPromotionInteraction", back_populates="promotion", cascade="all, delete-orphan")


class UserPromotionInteraction(Base):
    """
    Tracks user interactions with promotions (impressions, clicks, dismissals).
    Used for frequency capping, relevance scoring, and analytics.
    """
    __tablename__ = "user_promotion_interactions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # References
    user_id = Column(String(36), nullable=False, index=True)  # FK to users table
    promotion_id = Column(String(36), ForeignKey("promotions.id"), nullable=False, index=True)
    
    # Interaction Details
    action = Column(SQLEnum(InteractionAction), nullable=False, index=True)
    location = Column(SQLEnum(LocationType), nullable=False)  # Where it was shown
    
    # Context (snapshot at time of interaction)
    user_identity = Column(SQLEnum(IdentityType), nullable=False)
    user_tier = Column(String(20), nullable=False)  # "free", "premium", "pro"
    context_data = Column(JSON, nullable=True)  # Portfolio value, stock count, etc.
    
    # Dismissal Info (if action = DISMISS)
    dismissal_reason = Column(SQLEnum(DismissalReason), nullable=True)
    hide_until = Column(DateTime, nullable=True)  # When to show again (dismissed_at + 7 days)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # Relationships
    promotion = relationship("Promotion", back_populates="interactions")


class PromotionPreference(Base):
    """
    User-level preferences for ecosystem promotions.
    Stored in separate table for easy Settings integration.
    """
    __tablename__ = "promotion_preferences"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # References
    user_id = Column(String(36), nullable=False, unique=True, index=True)  # FK to users table
    
    # Global Toggles
    enabled = Column(Boolean, nullable=False, default=True)  # Master on/off
    show_dashboard_widgets = Column(Boolean, nullable=False, default=True)
    show_inline_links = Column(Boolean, nullable=False, default=True)
    show_modal_promotions = Column(Boolean, nullable=False, default=False)  # Off by default
    
    # Frequency Control
    frequency = Column(String(20), nullable=False, default="balanced")  # "more" | "balanced" | "less"
    
    # Category Preferences
    hidden_categories = Column(JSON, nullable=True)  # List of PromotionCategory values to hide
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================================================
# CONTEXTUAL TRIGGER EXAMPLES (stored in Promotion.contextual_triggers JSON)
# ============================================================================
"""
Portfolio-Based:
{
    "trigger_type": "portfolio",
    "conditions": {
        "portfolio_value_min": 0,
        "portfolio_value_max": 1000,
        "stock_count_min": null,
        "dividend_stock_count_min": 3,
        "sector_concentration_max": 0.4,
        "international_holdings_min": 0.2
    }
}

Activity-Based:
{
    "trigger_type": "activity",
    "conditions": {
        "alert_count_min": 5,
        "news_views_this_week_min": 10,
        "portfolio_checks_today_min": 3,
        "ai_summary_usage_today_min": 5
    }
}

Time-Based:
{
    "trigger_type": "time",
    "conditions": {
        "day_of_week": ["monday"],  # 0=Monday, 6=Sunday
        "hour_start": 7,
        "hour_end": 10,
        "month": [1, 2, 3, 4]  # Tax season
    }
}

Event-Based:
{
    "trigger_type": "event",
    "conditions": {
        "earnings_season": true,
        "market_volatility_min": 0.02,
        "news_about_sectors": ["technology", "finance"]
    }
}
"""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_active_promotions(
    identity: IdentityType,
    location: LocationType,
    user_tier: str
):
    """
    Returns active promotions for a given identity, location, and tier.
    Filters by:
    - is_active = True
    - start_date <= now <= end_date (if set)
    - allowed_locations contains location
    - tier_restrictions is null OR contains user_tier
    - identity_fit = identity OR 'all'
    - max_global_impressions not reached
    """
    from sqlalchemy import and_, or_
    from db import SessionLocal
    
    session = SessionLocal()
    try:
        now = datetime.utcnow()
        
        query = session.query(Promotion).filter(
            and_(
                Promotion.is_active == True,
                or_(
                    Promotion.start_date == None,
                    Promotion.start_date <= now
                ),
                or_(
                    Promotion.end_date == None,
                    Promotion.end_date >= now
                ),
                or_(
                    Promotion.identity_fit == identity,
                    Promotion.identity_fit == IdentityType.ALL
                ),
                or_(
                    Promotion.max_global_impressions == None,
                    Promotion.current_global_impressions < Promotion.max_global_impressions
                )
            )
        )
        
        # Filter by allowed_locations and tier_restrictions in Python (JSON filtering)
        promotions = query.all()
        
        filtered = []
        for promo in promotions:
            # Check location
            if location.value not in promo.allowed_locations:
                continue
            
            # Check tier
            if promo.tier_restrictions and user_tier not in promo.tier_restrictions:
                continue
            
            filtered.append(promo)
        
        # Sort by priority (descending)
        filtered.sort(key=lambda p: p.priority, reverse=True)
        
        return filtered
    
    finally:
        session.close()


def check_user_impression_limit(user_id: str, promotion_id: str) -> bool:
    """
    Returns True if user has not exceeded max impressions for this promotion.
    Counts impressions in the last 30 days.
    """
    from sqlalchemy import and_
    from db import SessionLocal
    
    session = SessionLocal()
    try:
        # Get promotion
        promotion = session.query(Promotion).filter_by(id=promotion_id).first()
        if not promotion:
            return False
        
        # Count impressions in last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        impression_count = session.query(UserPromotionInteraction).filter(
            and_(
                UserPromotionInteraction.user_id == user_id,
                UserPromotionInteraction.promotion_id == promotion_id,
                UserPromotionInteraction.action == InteractionAction.IMPRESSION,
                UserPromotionInteraction.created_at >= thirty_days_ago
            )
        ).count()
        
        return impression_count < promotion.max_impressions_per_user
    
    finally:
        session.close()


def is_promotion_dismissed(user_id: str, promotion_id: str) -> bool:
    """
    Returns True if user has dismissed this promotion and hide_until is in the future.
    """
    from sqlalchemy import and_
    from db import SessionLocal
    
    session = SessionLocal()
    try:
        now = datetime.utcnow()
        
        dismissal = session.query(UserPromotionInteraction).filter(
            and_(
                UserPromotionInteraction.user_id == user_id,
                UserPromotionInteraction.promotion_id == promotion_id,
                UserPromotionInteraction.action == InteractionAction.DISMISS,
                UserPromotionInteraction.hide_until > now
            )
        ).first()
        
        return dismissal is not None
    
    finally:
        session.close()


def get_user_preferences(user_id: str) -> PromotionPreference:
    """
    Returns user's promotion preferences, creating defaults if not exists.
    """
    from db import SessionLocal
    
    session = SessionLocal()
    try:
        prefs = session.query(PromotionPreference).filter_by(user_id=user_id).first()
        
        if not prefs:
            # Create default preferences
            prefs = PromotionPreference(user_id=user_id)
            session.add(prefs)
            session.commit()
        
        return prefs
    
    finally:
        session.close()


def get_frequency_multiplier(frequency: str) -> float:
    """
    Returns multiplier for max widgets based on frequency preference.
    "more" = 1.5x, "balanced" = 1.0x, "less" = 0.5x
    """
    return {
        "more": 1.5,
        "balanced": 1.0,
        "less": 0.5
    }.get(frequency, 1.0)

