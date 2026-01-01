"""
Cross-Promotion Engine - Promotion Selection Service
Intelligently selects and ranks promotions based on identity, context, and user behavior
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy import and_, or_
from db import SessionLocal
from models.promotions import (
    Promotion, UserPromotionInteraction, PromotionPreference,
    PromotionCategory, IdentityType, LocationType, InteractionAction,
    get_active_promotions, check_user_impression_limit,
    is_promotion_dismissed, get_user_preferences, get_frequency_multiplier
)
import json


class PromotionService:
    """
    Service for selecting and ranking promotions based on contextual triggers.
    """
    
    def __init__(self):
        self.session = SessionLocal()
    
    def __del__(self):
        self.session.close()
    
    def select_promotions(
        self,
        user_id: str,
        user_identity: IdentityType,
        user_tier: str,
        location: LocationType,
        context: Dict[str, Any],
        max_results: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Selects promotions for a user based on identity, location, and context.
        
        Args:
            user_id: User UUID
            user_identity: User's identity type (diaspora, youth, creator, legacy)
            user_tier: User's subscription tier (free, premium, pro)
            location: Where promotion will be shown (dashboard, portfolio, markets, news, alerts)
            context: Dict with portfolio stats, activity metrics, etc.
            max_results: Maximum promotions to return (default 2)
        
        Returns:
            List of promotion dicts ready for frontend display
        """
        # Check user preferences
        prefs = get_user_preferences(user_id)
        if not prefs.enabled:
            return []
        
        # Check location-specific preference
        if location == LocationType.DASHBOARD and not prefs.show_dashboard_widgets:
            return []
        if location in [LocationType.PORTFOLIO, LocationType.MARKETS, LocationType.NEWS, LocationType.ALERTS] and not prefs.show_inline_links:
            return []
        
        # Apply frequency multiplier to max_results
        frequency_multiplier = get_frequency_multiplier(prefs.frequency)
        max_results = int(max_results * frequency_multiplier)
        if max_results < 1:
            max_results = 1
        
        # Get active promotions for this identity, location, tier
        promotions = get_active_promotions(user_identity, location, user_tier)
        
        # Filter by user-specific rules
        filtered = []
        for promo in promotions:
            # Check if user dismissed this promotion
            if is_promotion_dismissed(user_id, promo.id):
                continue
            
            # Check impression limit
            if not check_user_impression_limit(user_id, promo.id):
                continue
            
            # Check if category is hidden by user
            if prefs.hidden_categories and promo.category.value in prefs.hidden_categories:
                continue
            
            # Check contextual triggers
            if promo.contextual_triggers:
                if not self._check_contextual_triggers(promo.contextual_triggers, context):
                    continue
            
            filtered.append(promo)
        
        # Rank by contextual relevance
        ranked = self._rank_promotions(filtered, context, user_identity)
        
        # Limit results
        final = ranked[:max_results]
        
        # Convert to frontend format
        return [self._format_promotion(p) for p in final]
    
    def _check_contextual_triggers(
        self,
        triggers: Dict[str, Any],
        context: Dict[str, Any]
    ) -> bool:
        """
        Checks if promotion's contextual triggers are met.
        
        Returns True if all conditions in trigger are satisfied.
        """
        trigger_type = triggers.get("trigger_type")
        conditions = triggers.get("conditions", {})
        
        if trigger_type == "portfolio":
            return self._check_portfolio_triggers(conditions, context)
        
        elif trigger_type == "activity":
            return self._check_activity_triggers(conditions, context)
        
        elif trigger_type == "time":
            return self._check_time_triggers(conditions)
        
        elif trigger_type == "event":
            return self._check_event_triggers(conditions, context)
        
        return True  # No trigger = always show
    
    def _check_portfolio_triggers(
        self,
        conditions: Dict[str, Any],
        context: Dict[str, Any]
    ) -> bool:
        """Portfolio-based trigger conditions"""
        portfolio_value = context.get("portfolio_value", 0)
        stock_count = context.get("stock_count", 0)
        dividend_stock_count = context.get("dividend_stock_count", 0)
        sector_concentration = context.get("sector_concentration", 0)
        international_holdings = context.get("international_holdings_percent", 0)
        
        # Check min/max portfolio value
        if "portfolio_value_min" in conditions:
            if portfolio_value < conditions["portfolio_value_min"]:
                return False
        if "portfolio_value_max" in conditions:
            if portfolio_value > conditions["portfolio_value_max"]:
                return False
        
        # Check stock counts
        if "stock_count_min" in conditions:
            if stock_count < conditions["stock_count_min"]:
                return False
        if "dividend_stock_count_min" in conditions:
            if dividend_stock_count < conditions["dividend_stock_count_min"]:
                return False
        
        # Check sector concentration
        if "sector_concentration_max" in conditions:
            if sector_concentration > conditions["sector_concentration_max"]:
                return False
        
        # Check international holdings
        if "international_holdings_min" in conditions:
            if international_holdings < conditions["international_holdings_min"]:
                return False
        
        return True
    
    def _check_activity_triggers(
        self,
        conditions: Dict[str, Any],
        context: Dict[str, Any]
    ) -> bool:
        """Activity-based trigger conditions"""
        alert_count = context.get("alert_count", 0)
        news_views_this_week = context.get("news_views_this_week", 0)
        portfolio_checks_today = context.get("portfolio_checks_today", 0)
        ai_summary_usage_today = context.get("ai_summary_usage_today", 0)
        
        if "alert_count_min" in conditions:
            if alert_count < conditions["alert_count_min"]:
                return False
        
        if "news_views_this_week_min" in conditions:
            if news_views_this_week < conditions["news_views_this_week_min"]:
                return False
        
        if "portfolio_checks_today_min" in conditions:
            if portfolio_checks_today < conditions["portfolio_checks_today_min"]:
                return False
        
        if "ai_summary_usage_today_min" in conditions:
            if ai_summary_usage_today < conditions["ai_summary_usage_today_min"]:
                return False
        
        return True
    
    def _check_time_triggers(self, conditions: Dict[str, Any]) -> bool:
        """Time-based trigger conditions"""
        now = datetime.utcnow()
        
        # Check day of week (0=Monday, 6=Sunday)
        if "day_of_week" in conditions:
            if now.weekday() not in conditions["day_of_week"]:
                return False
        
        # Check hour range
        if "hour_start" in conditions and "hour_end" in conditions:
            if not (conditions["hour_start"] <= now.hour < conditions["hour_end"]):
                return False
        
        # Check month
        if "month" in conditions:
            if now.month not in conditions["month"]:
                return False
        
        return True
    
    def _check_event_triggers(
        self,
        conditions: Dict[str, Any],
        context: Dict[str, Any]
    ) -> bool:
        """Event-based trigger conditions"""
        # Earnings season (Jan, Apr, Jul, Oct)
        if conditions.get("earnings_season"):
            now = datetime.utcnow()
            if now.month not in [1, 4, 7, 10]:
                return False
        
        # Market volatility
        if "market_volatility_min" in conditions:
            market_volatility = context.get("market_volatility", 0)
            if market_volatility < conditions["market_volatility_min"]:
                return False
        
        # News about specific sectors
        if "news_about_sectors" in conditions:
            recent_news_sectors = context.get("recent_news_sectors", [])
            if not any(sector in recent_news_sectors for sector in conditions["news_about_sectors"]):
                return False
        
        return True
    
    def _rank_promotions(
        self,
        promotions: List[Promotion],
        context: Dict[str, Any],
        user_identity: IdentityType
    ) -> List[Promotion]:
        """
        Ranks promotions by relevance score.
        
        Scoring factors:
        - Priority (set in database)
        - Identity exact match (boost if perfect fit)
        - Behavioral relevance (stocks viewed, news read)
        - Contextual trigger specificity (more conditions = higher relevance)
        - Category diversity (prefer varied categories)
        - Recency of last impression (avoid showing too recently)
        """
        from services.behavior_tracker import BehaviorTracker
        
        scored = []
        behavior_tracker = BehaviorTracker()
        
        for promo in promotions:
            score = promo.priority  # Start with base priority
            
            # Boost for exact identity match
            if promo.identity_fit == user_identity:
                score += 10
            elif promo.identity_fit == IdentityType.ALL:
                score += 5
            
            # Boost for behavioral relevance (NEW)
            behavioral_score = behavior_tracker.calculate_behavioral_relevance(
                context.get("user_id", ""),
                promo.identity_fit.value
            )
            score += behavioral_score
            
            # Boost for contextual triggers (more specific = higher score)
            if promo.contextual_triggers:
                condition_count = len(promo.contextual_triggers.get("conditions", {}))
                score += condition_count * 2
            
            # Penalize if shown recently (check last impression)
            last_impression = self._get_last_impression_date(context.get("user_id"), promo.id)
            if last_impression:
                days_since = (datetime.utcnow() - last_impression).days
                if days_since < 7:
                    score -= (7 - days_since) * 2  # Penalty decreases over time
            
            scored.append((promo, score))
        
        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return [promo for promo, score in scored]
    
    def _get_last_impression_date(self, user_id: str, promotion_id: str) -> Optional[datetime]:
        """Returns date of last impression for this user/promotion, or None"""
        if not user_id:
            return None
        
        last_interaction = self.session.query(UserPromotionInteraction).filter(
            and_(
                UserPromotionInteraction.user_id == user_id,
                UserPromotionInteraction.promotion_id == promotion_id,
                UserPromotionInteraction.action == InteractionAction.IMPRESSION
            )
        ).order_by(UserPromotionInteraction.created_at.desc()).first()
        
        return last_interaction.created_at if last_interaction else None
    
    def _format_promotion(self, promo: Promotion) -> Dict[str, Any]:
        """Converts Promotion model to frontend-ready dict"""
        return {
            "id": promo.id,
            "product_id": promo.product_id,
            "name": promo.name,
            "description": promo.description,
            "long_description": promo.long_description,
            "price": promo.price,
            "currency": promo.currency,
            "original_price": promo.original_price,
            "category": promo.category.value,
            "identity_fit": promo.identity_fit.value,
            "icon": promo.icon,
            "image_url": promo.image_url,
            "cta_text": promo.cta_text,
            "cta_link": promo.cta_link,
            "widget_type": promo.widget_type.value
        }
    
    def track_impression(
        self,
        user_id: str,
        promotion_id: str,
        location: LocationType,
        user_identity: IdentityType,
        user_tier: str,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Records an impression (promotion was shown to user).
        Updates global impression count for the promotion.
        
        Returns True if successfully tracked.
        """
        try:
            # Create interaction record
            interaction = UserPromotionInteraction(
                user_id=user_id,
                promotion_id=promotion_id,
                action=InteractionAction.IMPRESSION,
                location=location,
                user_identity=user_identity,
                user_tier=user_tier,
                context_data=context
            )
            self.session.add(interaction)
            
            # Increment global impression count
            promotion = self.session.query(Promotion).filter_by(id=promotion_id).first()
            if promotion:
                promotion.current_global_impressions += 1
            
            self.session.commit()
            return True
        
        except Exception as e:
            self.session.rollback()
            print(f"Error tracking impression: {e}")
            return False
    
    def track_click(
        self,
        user_id: str,
        promotion_id: str,
        location: LocationType,
        user_identity: IdentityType,
        user_tier: str,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Records a click (user clicked CTA button).
        
        Returns True if successfully tracked.
        """
        try:
            interaction = UserPromotionInteraction(
                user_id=user_id,
                promotion_id=promotion_id,
                action=InteractionAction.CLICK,
                location=location,
                user_identity=user_identity,
                user_tier=user_tier,
                context_data=context
            )
            self.session.add(interaction)
            self.session.commit()
            return True
        
        except Exception as e:
            self.session.rollback()
            print(f"Error tracking click: {e}")
            return False
    
    def dismiss_promotion(
        self,
        user_id: str,
        promotion_id: str,
        location: LocationType,
        user_identity: IdentityType,
        user_tier: str,
        reason: str,
        hide_days: int = 7
    ) -> bool:
        """
        Records a dismissal and sets hide_until date.
        
        Args:
            reason: "not_interested", "already_have", "too_expensive", "other"
            hide_days: How many days to hide (default 7)
        
        Returns True if successfully dismissed.
        """
        try:
            hide_until = datetime.utcnow() + timedelta(days=hide_days)
            
            interaction = UserPromotionInteraction(
                user_id=user_id,
                promotion_id=promotion_id,
                action=InteractionAction.DISMISS,
                location=location,
                user_identity=user_identity,
                user_tier=user_tier,
                dismissal_reason=reason,
                hide_until=hide_until
            )
            self.session.add(interaction)
            self.session.commit()
            return True
        
        except Exception as e:
            self.session.rollback()
            print(f"Error dismissing promotion: {e}")
            return False
    
    def restore_promotion(self, user_id: str, promotion_id: str) -> bool:
        """
        Restores a dismissed promotion by setting hide_until to past.
        
        Returns True if successfully restored.
        """
        try:
            # Find most recent dismissal
            dismissal = self.session.query(UserPromotionInteraction).filter(
                and_(
                    UserPromotionInteraction.user_id == user_id,
                    UserPromotionInteraction.promotion_id == promotion_id,
                    UserPromotionInteraction.action == InteractionAction.DISMISS
                )
            ).order_by(UserPromotionInteraction.created_at.desc()).first()
            
            if dismissal:
                dismissal.hide_until = datetime.utcnow() - timedelta(days=1)  # Set to past
                
                # Add restore interaction
                restore = UserPromotionInteraction(
                    user_id=user_id,
                    promotion_id=promotion_id,
                    action=InteractionAction.RESTORE,
                    location=dismissal.location,
                    user_identity=dismissal.user_identity,
                    user_tier=dismissal.user_tier
                )
                self.session.add(restore)
                
                self.session.commit()
                return True
            
            return False
        
        except Exception as e:
            self.session.rollback()
            print(f"Error restoring promotion: {e}")
            return False
    
    def get_dismissed_promotions(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Returns list of currently dismissed promotions for this user.
        """
        now = datetime.utcnow()
        
        dismissed = self.session.query(UserPromotionInteraction).join(
            Promotion
        ).filter(
            and_(
                UserPromotionInteraction.user_id == user_id,
                UserPromotionInteraction.action == InteractionAction.DISMISS,
                UserPromotionInteraction.hide_until > now
            )
        ).all()
        
        return [
            {
                "promotion_id": d.promotion_id,
                "promotion_name": d.promotion.name,
                "dismissed_at": d.created_at.isoformat(),
                "hide_until": d.hide_until.isoformat(),
                "reason": d.dismissal_reason.value if d.dismissal_reason else None
            }
            for d in dismissed
        ]
    
    def update_preferences(
        self,
        user_id: str,
        enabled: Optional[bool] = None,
        show_dashboard_widgets: Optional[bool] = None,
        show_inline_links: Optional[bool] = None,
        show_modal_promotions: Optional[bool] = None,
        frequency: Optional[str] = None,
        hidden_categories: Optional[List[str]] = None
    ) -> bool:
        """
        Updates user's promotion preferences.
        
        Returns True if successfully updated.
        """
        try:
            prefs = get_user_preferences(user_id)
            
            if enabled is not None:
                prefs.enabled = enabled
            if show_dashboard_widgets is not None:
                prefs.show_dashboard_widgets = show_dashboard_widgets
            if show_inline_links is not None:
                prefs.show_inline_links = show_inline_links
            if show_modal_promotions is not None:
                prefs.show_modal_promotions = show_modal_promotions
            if frequency is not None:
                prefs.frequency = frequency
            if hidden_categories is not None:
                prefs.hidden_categories = hidden_categories
            
            prefs.updated_at = datetime.utcnow()
            self.session.commit()
            return True
        
        except Exception as e:
            self.session.rollback()
            print(f"Error updating preferences: {e}")
            return False


# ============================================================================
# ANALYTICS HELPERS
# ============================================================================

def get_promotion_ctr(promotion_id: str, days: int = 30) -> float:
    """
    Calculates click-through rate for a promotion over the last N days.
    CTR = (clicks / impressions) * 100
    """
    session = SessionLocal()
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        impressions = session.query(UserPromotionInteraction).filter(
            and_(
                UserPromotionInteraction.promotion_id == promotion_id,
                UserPromotionInteraction.action == InteractionAction.IMPRESSION,
                UserPromotionInteraction.created_at >= start_date
            )
        ).count()
        
        clicks = session.query(UserPromotionInteraction).filter(
            and_(
                UserPromotionInteraction.promotion_id == promotion_id,
                UserPromotionInteraction.action == InteractionAction.CLICK,
                UserPromotionInteraction.created_at >= start_date
            )
        ).count()
        
        if impressions == 0:
            return 0.0
        
        return (clicks / impressions) * 100
    
    finally:
        session.close()


def get_top_promotions_by_identity(identity: IdentityType, days: int = 30) -> List[Dict[str, Any]]:
    """
    Returns top performing promotions for a given identity, ranked by CTR.
    """
    session = SessionLocal()
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get all active promotions for this identity
        promotions = session.query(Promotion).filter(
            or_(
                Promotion.identity_fit == identity,
                Promotion.identity_fit == IdentityType.ALL
            ),
            Promotion.is_active == True
        ).all()
        
        results = []
        for promo in promotions:
            ctr = get_promotion_ctr(promo.id, days)
            
            impressions = session.query(UserPromotionInteraction).filter(
                and_(
                    UserPromotionInteraction.promotion_id == promo.id,
                    UserPromotionInteraction.action == InteractionAction.IMPRESSION,
                    UserPromotionInteraction.created_at >= start_date
                )
            ).count()
            
            results.append({
                "promotion_id": promo.id,
                "name": promo.name,
                "ctr": round(ctr, 2),
                "impressions": impressions,
                "category": promo.category.value
            })
        
        # Sort by CTR descending
        results.sort(key=lambda x: x["ctr"], reverse=True)
        
        return results
    
    finally:
        session.close()

