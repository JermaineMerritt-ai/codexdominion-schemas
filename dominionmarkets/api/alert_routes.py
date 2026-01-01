"""
Alert API Routes
================
Flask API endpoints for Alert Center functionality
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from decimal import Decimal
import uuid

from db import SessionLocal
from models.alerts import (
    Alert, AlertTrigger, UserAlertPreference,
    AlertType, AlertStatus, ConditionType, IdentityType,
    get_user_alert_count_by_type, check_tier_limit, 
    get_recent_triggers, get_user_alert_summary
)
from services.alert_service import alert_service

# Create blueprint
alerts_bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')


def get_current_user_id():
    """Get current user ID from session - placeholder"""
    # TODO: Implement actual session management
    return request.headers.get('X-User-ID', '00000000-0000-0000-0000-000000000000')


def get_user_tier():
    """Get current user's subscription tier - placeholder"""
    # TODO: Get from user model/session
    return request.headers.get('X-User-Tier', 'free')


# ==================== Alert CRUD ====================

@alerts_bp.route('/', methods=['GET'])
def list_alerts():
    """
    List all alerts for current user
    
    Query params:
    - status: Filter by status (active, triggered, paused)
    - alert_type: Filter by type (price, news, earnings, etc.)
    - page: Page number (default 1)
    - limit: Results per page (default 20)
    """
    user_id = get_current_user_id()
    session = SessionLocal()
    
    try:
        # Parse query params
        status = request.args.get('status')
        alert_type = request.args.get('alert_type')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        
        # Build query
        query = session.query(Alert).filter(
            Alert.user_id == user_id,
            Alert.status != AlertStatus.DELETED
        )
        
        if status:
            query = query.filter(Alert.status == AlertStatus[status.upper()])
        
        if alert_type:
            query = query.filter(Alert.alert_type == AlertType[alert_type.upper()])
        
        # Get total count
        total = query.count()
        
        # Paginate
        alerts = query.order_by(Alert.created_at.desc())\
                     .offset((page - 1) * limit)\
                     .limit(limit)\
                     .all()
        
        return jsonify({
            'alerts': [alert.to_dict() for alert in alerts],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@alerts_bp.route('/', methods=['POST'])
def create_alert():
    """
    Create new alert
    
    Body:
    {
        "alert_type": "price",
        "symbol": "AAPL",
        "condition_type": "above",
        "target_value": 185.00,
        "alert_name": "AAPL Above $185",
        "notification_push": true,
        "notification_email": false
    }
    """
    user_id = get_current_user_id()
    user_tier = get_user_tier()
    session = SessionLocal()
    
    try:
        data = request.json
        
        # Validate alert type
        alert_type_str = data.get('alert_type', '').upper()
        if alert_type_str not in AlertType.__members__:
            return jsonify({'error': 'Invalid alert_type'}), 400
        
        alert_type = AlertType[alert_type_str]
        
        # Check tier limits
        can_create, current_count, limit = check_tier_limit(session, user_id, alert_type, user_tier)
        if not can_create:
            return jsonify({
                'error': 'Alert limit reached',
                'current_count': current_count,
                'limit': limit,
                'tier': user_tier,
                'upgrade_required': True
            }), 403
        
        # Validate condition type
        condition_type_str = data.get('condition_type', '').upper()
        if condition_type_str not in ConditionType.__members__:
            return jsonify({'error': 'Invalid condition_type'}), 400
        
        condition_type = ConditionType[condition_type_str]
        
        # Create alert
        alert = Alert(
            user_id=user_id,
            alert_type=alert_type,
            symbol=data.get('symbol', '').upper() if data.get('symbol') else None,
            condition_type=condition_type,
            target_value=Decimal(str(data.get('target_value'))) if data.get('target_value') else None,
            min_verification_score=data.get('min_verification_score', 75),
            article_threshold=data.get('article_threshold', 1),
            portfolio_id=data.get('portfolio_id'),
            alert_name=data.get('alert_name'),
            status=AlertStatus.ACTIVE,
            notification_push=data.get('notification_push', True),
            notification_email=data.get('notification_email', False),
            notification_sms=data.get('notification_sms', False)
        )
        
        session.add(alert)
        session.commit()
        
        return jsonify({
            'message': 'Alert created successfully',
            'alert': alert.to_dict()
        }), 201
        
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@alerts_bp.route('/<alert_id>', methods=['GET'])
def get_alert(alert_id):
    """Get alert details"""
    user_id = get_current_user_id()
    session = SessionLocal()
    
    try:
        alert = session.query(Alert).filter(
            Alert.id == alert_id,
            Alert.user_id == user_id
        ).first()
        
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        # Get trigger history
        triggers = session.query(AlertTrigger).filter(
            AlertTrigger.alert_id == alert_id
        ).order_by(AlertTrigger.triggered_at.desc()).limit(10).all()
        
        alert_dict = alert.to_dict()
        alert_dict['triggers'] = [t.to_dict() for t in triggers]
        
        return jsonify(alert_dict)
        
    finally:
        session.close()


@alerts_bp.route('/<alert_id>', methods=['PATCH'])
def update_alert(alert_id):
    """Update alert"""
    user_id = get_current_user_id()
    session = SessionLocal()
    
    try:
        alert = session.query(Alert).filter(
            Alert.id == alert_id,
            Alert.user_id == user_id
        ).first()
        
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        data = request.json
        
        # Update allowed fields
        if 'target_value' in data:
            alert.target_value = Decimal(str(data['target_value']))
        if 'alert_name' in data:
            alert.alert_name = data['alert_name']
        if 'min_verification_score' in data:
            alert.min_verification_score = data['min_verification_score']
        if 'notification_push' in data:
            alert.notification_push = data['notification_push']
        if 'notification_email' in data:
            alert.notification_email = data['notification_email']
        if 'notification_sms' in data:
            alert.notification_sms = data['notification_sms']
        
        alert.updated_at = datetime.utcnow()
        session.commit()
        
        return jsonify({
            'message': 'Alert updated successfully',
            'alert': alert.to_dict()
        })
        
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@alerts_bp.route('/<alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    """Delete alert (soft delete)"""
    user_id = get_current_user_id()
    session = SessionLocal()
    
    try:
        alert = session.query(Alert).filter(
            Alert.id == alert_id,
            Alert.user_id == user_id
        ).first()
        
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        alert.status = AlertStatus.DELETED
        session.commit()
        
        return jsonify({'message': 'Alert deleted successfully'})
        
    finally:
        session.close()


# ==================== Alert Management ====================

@alerts_bp.route('/<alert_id>/pause', methods=['POST'])
def pause_alert(alert_id):
    """Pause an alert"""
    user_id = get_current_user_id()
    session = SessionLocal()
    
    try:
        alert = session.query(Alert).filter(
            Alert.id == alert_id,
            Alert.user_id == user_id
        ).first()
        
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        alert.status = AlertStatus.PAUSED
        session.commit()
        
        return jsonify({
            'message': 'Alert paused',
            'alert': alert.to_dict()
        })
        
    finally:
        session.close()


@alerts_bp.route('/<alert_id>/resume', methods=['POST'])
def resume_alert(alert_id):
    """Resume a paused alert"""
    user_id = get_current_user_id()
    session = SessionLocal()
    
    try:
        alert = session.query(Alert).filter(
            Alert.id == alert_id,
            Alert.user_id == user_id,
            Alert.status == AlertStatus.PAUSED
        ).first()
        
        if not alert:
            return jsonify({'error': 'Alert not found or not paused'}), 404
        
        alert.status = AlertStatus.ACTIVE
        session.commit()
        
        return jsonify({
            'message': 'Alert resumed',
            'alert': alert.to_dict()
        })
        
    finally:
        session.close()


# ==================== Alert Triggers ====================

@alerts_bp.route('/<alert_id>/triggers', methods=['GET'])
def get_alert_triggers(alert_id):
    """Get trigger history for an alert"""
    user_id = get_current_user_id()
    session = SessionLocal()
    
    try:
        # Verify ownership
        alert = session.query(Alert).filter(
            Alert.id == alert_id,
            Alert.user_id == user_id
        ).first()
        
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        # Get triggers
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        
        query = session.query(AlertTrigger).filter(
            AlertTrigger.alert_id == alert_id
        )
        
        total = query.count()
        
        triggers = query.order_by(AlertTrigger.triggered_at.desc())\
                       .offset((page - 1) * limit)\
                       .limit(limit)\
                       .all()
        
        return jsonify({
            'triggers': [t.to_dict() for t in triggers],
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit
            }
        })
        
    finally:
        session.close()


@alerts_bp.route('/triggers/recent', methods=['GET'])
def get_recent_triggers():
    """Get recent triggers across all alerts"""
    user_id = get_current_user_id()
    session = SessionLocal()
    
    try:
        hours = int(request.args.get('hours', 24))
        triggers = get_recent_triggers(session, user_id, hours)
        
        # Add alert details to each trigger
        result = []
        for trigger in triggers:
            trigger_dict = trigger.to_dict()
            if trigger.alert:
                trigger_dict['alert'] = {
                    'id': str(trigger.alert.id),
                    'alert_type': trigger.alert.alert_type.value,
                    'symbol': trigger.alert.symbol,
                    'alert_name': trigger.alert.alert_name
                }
            result.append(trigger_dict)
        
        return jsonify({'triggers': result})
        
    finally:
        session.close()


# ==================== Summary & Limits ====================

@alerts_bp.route('/summary', methods=['GET'])
def get_summary():
    """Get alert summary for dashboard"""
    user_id = get_current_user_id()
    user_tier = get_user_tier()
    session = SessionLocal()
    
    try:
        summary = get_user_alert_summary(session, user_id, user_tier)
        return jsonify(summary)
        
    finally:
        session.close()


@alerts_bp.route('/limits', methods=['GET'])
def get_limits():
    """Get tier limits for current user"""
    user_tier = get_user_tier()
    
    alert_obj = Alert()
    limits = alert_obj.get_tier_limits(user_tier)
    
    return jsonify({
        'tier': user_tier,
        'limits': limits
    })


# ==================== User Preferences ====================

@alerts_bp.route('/preferences', methods=['GET'])
def get_preferences():
    """Get user alert preferences"""
    user_id = get_current_user_id()
    session = SessionLocal()
    
    try:
        prefs = session.query(UserAlertPreference).filter(
            UserAlertPreference.user_id == user_id
        ).first()
        
        if not prefs:
            # Create default preferences
            prefs = UserAlertPreference(user_id=user_id)
            session.add(prefs)
            session.commit()
        
        return jsonify(prefs.to_dict())
        
    finally:
        session.close()


@alerts_bp.route('/preferences', methods=['PATCH'])
def update_preferences():
    """Update user alert preferences"""
    user_id = get_current_user_id()
    session = SessionLocal()
    
    try:
        prefs = session.query(UserAlertPreference).filter(
            UserAlertPreference.user_id == user_id
        ).first()
        
        if not prefs:
            prefs = UserAlertPreference(user_id=user_id)
            session.add(prefs)
        
        data = request.json
        
        # Update fields
        if 'identity_type' in data:
            prefs.identity_type = IdentityType[data['identity_type'].upper()]
        if 'default_notification_push' in data:
            prefs.default_notification_push = data['default_notification_push']
        if 'default_notification_email' in data:
            prefs.default_notification_email = data['default_notification_email']
        if 'default_notification_sms' in data:
            prefs.default_notification_sms = data['default_notification_sms']
        if 'quiet_hours_start' in data:
            prefs.quiet_hours_start = data['quiet_hours_start']
        if 'quiet_hours_end' in data:
            prefs.quiet_hours_end = data['quiet_hours_end']
        if 'timezone' in data:
            prefs.timezone = data['timezone']
        
        prefs.updated_at = datetime.utcnow()
        session.commit()
        
        return jsonify({
            'message': 'Preferences updated',
            'preferences': prefs.to_dict()
        })
        
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


# ==================== Alert Templates (Identity-Aware) ====================

@alerts_bp.route('/templates', methods=['GET'])
def get_templates():
    """Get pre-configured alert templates based on user identity"""
    identity = request.args.get('identity', 'all').lower()
    
    templates = {
        'diaspora': [
            {
                'name': 'Emerging Markets ETF Price Alert',
                'alert_type': 'price',
                'symbol': 'EEM',
                'condition_type': 'percent_up',
                'target_value': 5.0,
                'description': 'Get notified when emerging markets gain 5%'
            },
            {
                'name': 'Global Payments News',
                'alert_type': 'news',
                'symbol': 'V',
                'condition_type': 'any_news',
                'min_verification_score': 80,
                'description': 'Visa news alerts for Caribbean expansion'
            }
        ],
        'youth': [
            {
                'name': 'S&P 500 ETF Price Alert',
                'alert_type': 'price',
                'symbol': 'SPY',
                'condition_type': 'below',
                'target_value': 450.00,
                'description': 'Buy opportunity when S&P dips'
            },
            {
                'name': 'Index Fund Dividend Alert',
                'alert_type': 'dividend',
                'symbol': 'VYM',
                'condition_type': 'ex_date_approaching',
                'description': 'Don\'t miss dividend dates'
            }
        ],
        'creator': [
            {
                'name': 'Shopify Earnings Alert',
                'alert_type': 'earnings',
                'symbol': 'SHOP',
                'condition_type': 'earnings_upcoming_7d',
                'description': 'Creator platform earnings updates'
            },
            {
                'name': 'Payment Processor News',
                'alert_type': 'news',
                'symbol': 'SQ',
                'condition_type': 'any_news',
                'description': 'Square/Block news for creators'
            }
        ],
        'legacy': [
            {
                'name': 'Dividend Aristocrat Alert',
                'alert_type': 'dividend',
                'symbol': 'JNJ',
                'condition_type': 'dividend_changed',
                'description': 'Track Johnson & Johnson dividends'
            },
            {
                'name': 'Blue Chip Earnings',
                'alert_type': 'earnings',
                'symbol': 'BRK.B',
                'condition_type': 'earnings_released',
                'description': 'Berkshire Hathaway earnings'
            }
        ]
    }
    
    return jsonify({
        'identity': identity,
        'templates': templates.get(identity, [])
    })
