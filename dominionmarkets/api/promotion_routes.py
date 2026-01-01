"""
Cross-Promotion Engine - API Routes
Flask endpoints for promotion selection, tracking, and user preferences
"""

from flask import Blueprint, jsonify, request
from typing import Dict, Any
from datetime import datetime

from services.promotion_service import PromotionService, get_promotion_ctr, get_top_promotions_by_identity
from services.behavior_tracker import get_recent_behavior, track_activity
from models.promotions import (
    LocationType, IdentityType, DismissalReason,
    get_user_preferences, Promotion
)
from db import SessionLocal

# Create Blueprint
promotion_bp = Blueprint('promotions', __name__, url_prefix='/api/promotions')


# ============================================================================
# PROMOTION SELECTION
# ============================================================================

@promotion_bp.route('/', methods=['GET'])
def get_promotions():
    """
    GET /api/promotions?location=dashboard&context={...}
    
    Returns list of promotions for the current user based on location and context.
    
    Query Params:
        location (required): dashboard | portfolio | markets | news | alerts
        context (optional): JSON string with portfolio stats, activity metrics
    
    Response:
        {
            "promotions": [...],
            "max_impressions_reached": false
        }
    """
    try:
        # Get user from session/auth (mock for now)
        user_id = request.args.get('user_id') or 'user_123'  # TODO: Get from auth
        user_identity_str = request.args.get('identity', 'youth')
        user_tier = request.args.get('tier', 'free')
        
        # Parse location
        location_str = request.args.get('location')
        if not location_str:
            return jsonify({"error": "location is required"}), 400
        
        try:
            location = LocationType[location_str.upper()]
        except KeyError:
            return jsonify({"error": f"Invalid location: {location_str}"}), 400
        
        try:
            user_identity = IdentityType[user_identity_str.upper()]
        except KeyError:
            user_identity = IdentityType.YOUTH  # Default
        
        # Parse context
        context_str = request.args.get('context', '{}')
        try:
            context = eval(context_str) if context_str else {}
        except:
            context = {}
        
        # Add user_id to context for ranking
        context['user_id'] = user_id
        
        # Select promotions
        service = PromotionService()
        promotions = service.select_promotions(
            user_id=user_id,
            user_identity=user_identity,
            user_tier=user_tier,
            location=location,
            context=context,
            max_results=2
        )
        
        return jsonify({
            "promotions": promotions,
            "max_impressions_reached": False  # TODO: Check global cap
        }), 200
    
    except Exception as e:
        print(f"Error fetching promotions: {e}")
        return jsonify({"error": "Failed to fetch promotions"}), 500


# ============================================================================
# TRACKING
# ============================================================================

@promotion_bp.route('/impression', methods=['POST'])
def track_impression():
    """
    POST /api/promotions/impression
    Body: {
        "promotion_id": "promo_001",
        "location": "dashboard",
        "context": {...}  // optional
    }
    
    Records that a promotion was shown to the user.
    """
    try:
        data = request.get_json()
        
        # Get user from session/auth
        user_id = data.get('user_id') or 'user_123'  # TODO: Get from auth
        user_identity_str = data.get('identity', 'youth')
        user_tier = data.get('tier', 'free')
        
        promotion_id = data.get('promotion_id')
        location_str = data.get('location')
        context = data.get('context')
        
        if not promotion_id or not location_str:
            return jsonify({"error": "promotion_id and location are required"}), 400
        
        try:
            location = LocationType[location_str.upper()]
            user_identity = IdentityType[user_identity_str.upper()]
        except KeyError as e:
            return jsonify({"error": f"Invalid enum value: {e}"}), 400
        
        # Track impression
        service = PromotionService()
        success = service.track_impression(
            user_id=user_id,
            promotion_id=promotion_id,
            location=location,
            user_identity=user_identity,
            user_tier=user_tier,
            context=context
        )
        
        if success:
            return jsonify({"message": "Impression tracked"}), 200
        else:
            return jsonify({"error": "Failed to track impression"}), 500
    
    except Exception as e:
        print(f"Error tracking impression: {e}")
        return jsonify({"error": "Failed to track impression"}), 500


@promotion_bp.route('/click', methods=['POST'])
def track_click():
    """
    POST /api/promotions/click
    Body: {
        "promotion_id": "promo_001",
        "location": "dashboard",
        "action": "learn_more" | "try_now" | "dismiss"
    }
    
    Records that user clicked on a promotion CTA.
    """
    try:
        data = request.get_json()
        
        user_id = data.get('user_id') or 'user_123'  # TODO: Get from auth
        user_identity_str = data.get('identity', 'youth')
        user_tier = data.get('tier', 'free')
        
        promotion_id = data.get('promotion_id')
        location_str = data.get('location')
        action = data.get('action', 'click')
        
        if not promotion_id or not location_str:
            return jsonify({"error": "promotion_id and location are required"}), 400
        
        try:
            location = LocationType[location_str.upper()]
            user_identity = IdentityType[user_identity_str.upper()]
        except KeyError as e:
            return jsonify({"error": f"Invalid enum value: {e}"}), 400
        
        # Track click
        service = PromotionService()
        success = service.track_click(
            user_id=user_id,
            promotion_id=promotion_id,
            location=location,
            user_identity=user_identity,
            user_tier=user_tier,
            context={"action": action}
        )
        
        if success:
            return jsonify({"message": "Click tracked"}), 200
        else:
            return jsonify({"error": "Failed to track click"}), 500
    
    except Exception as e:
        print(f"Error tracking click: {e}")
        return jsonify({"error": "Failed to track click"}), 500


@promotion_bp.route('/dismiss', methods=['POST'])
def dismiss_promotion():
    """
    POST /api/promotions/dismiss
    Body: {
        "promotion_id": "promo_001",
        "location": "dashboard",
        "reason": "not_interested" | "already_have" | "too_expensive" | "other",
        "hide_duration_days": 7  // optional, default 7
    }
    
    Dismisses a promotion for X days.
    """
    try:
        data = request.get_json()
        
        user_id = data.get('user_id') or 'user_123'  # TODO: Get from auth
        user_identity_str = data.get('identity', 'youth')
        user_tier = data.get('tier', 'free')
        
        promotion_id = data.get('promotion_id')
        location_str = data.get('location')
        reason_str = data.get('reason', 'other')
        hide_days = data.get('hide_duration_days', 7)
        
        if not promotion_id or not location_str:
            return jsonify({"error": "promotion_id and location are required"}), 400
        
        try:
            location = LocationType[location_str.upper()]
            user_identity = IdentityType[user_identity_str.upper()]
        except KeyError as e:
            return jsonify({"error": f"Invalid enum value: {e}"}), 400
        
        # Dismiss
        service = PromotionService()
        success = service.dismiss_promotion(
            user_id=user_id,
            promotion_id=promotion_id,
            location=location,
            user_identity=user_identity,
            user_tier=user_tier,
            reason=reason_str,
            hide_days=hide_days
        )
        
        if success:
            return jsonify({"message": "Promotion dismissed"}), 200
        else:
            return jsonify({"error": "Failed to dismiss promotion"}), 500
    
    except Exception as e:
        print(f"Error dismissing promotion: {e}")
        return jsonify({"error": "Failed to dismiss promotion"}), 500


# ============================================================================
# DISMISSED PROMOTIONS
# ============================================================================

@promotion_bp.route('/dismissed', methods=['GET'])
def get_dismissed():
    """
    GET /api/promotions/dismissed
    
    Returns list of currently dismissed promotions for the user.
    """
    try:
        user_id = request.args.get('user_id') or 'user_123'  # TODO: Get from auth
        
        service = PromotionService()
        dismissed = service.get_dismissed_promotions(user_id)
        
        return jsonify({"dismissed": dismissed}), 200
    
    except Exception as e:
        print(f"Error fetching dismissed promotions: {e}")
        return jsonify({"error": "Failed to fetch dismissed promotions"}), 500


@promotion_bp.route('/restore', methods=['POST'])
def restore_promotion():
    """
    POST /api/promotions/restore
    Body: {
        "promotion_id": "promo_001"
    }
    
    Restores a dismissed promotion.
    """
    try:
        data = request.get_json()
        
        user_id = data.get('user_id') or 'user_123'  # TODO: Get from auth
        promotion_id = data.get('promotion_id')
        
        if not promotion_id:
            return jsonify({"error": "promotion_id is required"}), 400
        
        service = PromotionService()
        success = service.restore_promotion(user_id, promotion_id)
        
        if success:
            return jsonify({"message": "Promotion restored"}), 200
        else:
            return jsonify({"error": "Failed to restore promotion"}), 404
    
    except Exception as e:
        print(f"Error restoring promotion: {e}")
        return jsonify({"error": "Failed to restore promotion"}), 500


# ============================================================================
# USER PREFERENCES
# ============================================================================

@promotion_bp.route('/preferences', methods=['GET'])
def get_preferences():
    """
    GET /api/promotions/preferences
    
    Returns user's promotion preferences.
    """
    try:
        user_id = request.args.get('user_id') or 'user_123'  # TODO: Get from auth
        
        prefs = get_user_preferences(user_id)
        
        return jsonify({
            "enabled": prefs.enabled,
            "show_dashboard_widgets": prefs.show_dashboard_widgets,
            "show_inline_links": prefs.show_inline_links,
            "show_modal_promotions": prefs.show_modal_promotions,
            "frequency": prefs.frequency,
            "hidden_categories": prefs.hidden_categories or []
        }), 200
    
    except Exception as e:
        print(f"Error fetching preferences: {e}")
        return jsonify({"error": "Failed to fetch preferences"}), 500


@promotion_bp.route('/preferences', methods=['PUT'])
def update_preferences():
    """
    PUT /api/promotions/preferences
    Body: {
        "enabled": true,
        "show_dashboard_widgets": true,
        "show_inline_links": true,
        "show_modal_promotions": false,
        "frequency": "balanced",  // "more" | "balanced" | "less"
        "hidden_categories": ["service"]
    }
    
    Updates user's promotion preferences.
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id') or 'user_123'  # TODO: Get from auth
        
        service = PromotionService()
        success = service.update_preferences(
            user_id=user_id,
            enabled=data.get('enabled'),
            show_dashboard_widgets=data.get('show_dashboard_widgets'),
            show_inline_links=data.get('show_inline_links'),
            show_modal_promotions=data.get('show_modal_promotions'),
            frequency=data.get('frequency'),
            hidden_categories=data.get('hidden_categories')
        )
        
        if success:
            return jsonify({"message": "Preferences updated"}), 200
        else:
            return jsonify({"error": "Failed to update preferences"}), 500
    
    except Exception as e:
        print(f"Error updating preferences: {e}")
        return jsonify({"error": "Failed to update preferences"}), 500


# ============================================================================
# ANALYTICS (ADMIN ONLY)
# ============================================================================

@promotion_bp.route('/analytics/ctr/<promotion_id>', methods=['GET'])
def get_ctr(promotion_id: str):
    """
    GET /api/promotions/analytics/ctr/<promotion_id>?days=30
    
    Returns click-through rate for a promotion.
    """
    try:
        days = int(request.args.get('days', 30))
        
        ctr = get_promotion_ctr(promotion_id, days)
        
        return jsonify({
            "promotion_id": promotion_id,
            "ctr": round(ctr, 2),
            "period_days": days
        }), 200
    
    except Exception as e:
        print(f"Error fetching CTR: {e}")
        return jsonify({"error": "Failed to fetch CTR"}), 500


@promotion_bp.route('/analytics/top/<identity>', methods=['GET'])
def get_top_by_identity(identity: str):
    """
    GET /api/promotions/analytics/top/<identity>?days=30
    
    Returns top performing promotions for an identity type.
    """
    try:
        days = int(request.args.get('days', 30))
        
        try:
            identity_enum = IdentityType[identity.upper()]
        except KeyError:
            return jsonify({"error": f"Invalid identity: {identity}"}), 400
        
        top = get_top_promotions_by_identity(identity_enum, days)
        
        return jsonify({
            "identity": identity,
            "top_promotions": top,
            "period_days": days
        }), 200
    
    except Exception as e:
        print(f"Error fetching top promotions: {e}")
        return jsonify({"error": "Failed to fetch top promotions"}), 500


# ============================================================================
# CATALOG (FOR ADMIN)
# ============================================================================

@promotion_bp.route('/catalog', methods=['GET'])
def get_catalog():
    """
    GET /api/promotions/catalog?category=template&identity=diaspora
    
    Returns full product catalog with optional filters.
    """
    try:
        category_str = request.args.get('category')
        identity_str = request.args.get('identity')
        is_active = request.args.get('active', 'true').lower() == 'true'
        
        session = SessionLocal()
        try:
            query = session.query(Promotion)
            
            if is_active:
                query = query.filter(Promotion.is_active == True)
            
            if category_str:
                query = query.filter(Promotion.category == category_str.upper())
            
            if identity_str:
                query = query.filter(Promotion.identity_fit == identity_str.upper())
            
            promotions = query.all()
            
            return jsonify({
                "catalog": [
                    {
                        "id": p.id,
                        "product_id": p.product_id,
                        "name": p.name,
                        "price": p.price,
                        "category": p.category.value,
                        "identity_fit": p.identity_fit.value,
                        "is_active": p.is_active
                    }
                    for p in promotions
                ]
            }), 200
        
        finally:
            session.close()
    
    except Exception as e:
        print(f"Error fetching catalog: {e}")
        return jsonify({"error": "Failed to fetch catalog"}), 500


# ============================================================================
# BEHAVIOR TRACKING ENDPOINTS
# ============================================================================

@promotion_bp.route('/behavior/recent', methods=['GET'])
def get_user_behavior():
    """
    GET /api/promotions/behavior/recent
    
    Returns recent behavior summary for cross-promotion refinement.
    Used by frontend to enrich promotion selection context.
    """
    try:
        user_id = request.args.get('user_id') or 'user_123'  # TODO: Get from auth
        
        behavior = get_recent_behavior(user_id)
        
        return jsonify(behavior), 200
    
    except Exception as e:
        print(f"Error fetching behavior: {e}")
        return jsonify({"error": "Failed to fetch behavior"}), 500


@promotion_bp.route('/behavior/track', methods=['POST'])
def track_user_activity():
    """
    POST /api/promotions/behavior/track
    Body: {
        "activity_type": "stock_view" | "news_read" | "portfolio_check" | "sector_view" | "ai_summary" | "alert_creation",
        "metadata": {
            "symbol": "AAPL",  // for stock_view
            "sector": "technology",  // for sector_view
            "category": "earnings",  // for news_read
            "is_diaspora": true,  // for news_read
            "is_creator": false  // for news_read
        }
    }
    
    Tracks user activity for behavioral cross-promotion.
    """
    try:
        data = request.get_json()
        
        user_id = data.get('user_id') or 'user_123'  # TODO: Get from auth
        activity_type = data.get('activity_type')
        metadata = data.get('metadata', {})
        
        if not activity_type:
            return jsonify({"error": "activity_type is required"}), 400
        
        track_activity(user_id, activity_type, metadata)
        
        return jsonify({"message": "Activity tracked"}), 200
    
    except Exception as e:
        print(f"Error tracking activity: {e}")
        return jsonify({"error": "Failed to track activity"}), 500


# ============================================================================
# HEALTH CHECK
# ============================================================================

@promotion_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "cross-promotion-engine",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

