"""
Codex Dominion - AI Advisor API

REST API for AI Advisor recommendations:
- GET /recommendations - Get all active recommendations
- GET /recommendations/:id - Get specific recommendation
- POST /recommendations/:id/accept - Accept recommendation
- POST /recommendations/:id/dismiss - Dismiss recommendation
- POST /recommendations/refresh - Generate new recommendations
- GET /recommendations/stats - Get advisor performance stats

The Advisor feels like a partner, not a nag.
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from db import SessionLocal
from models import AdvisorRecommendation, RecommendationType, RecommendationStatus
from advisor_signals import collect_tenant_signals
from advisor_intelligence import generate_recommendations
import random


advisor_bp = Blueprint('advisor', __name__)


def register_advisor_routes(app):
    """Register advisor API routes with Flask app"""
    app.register_blueprint(advisor_bp, url_prefix='/api/advisor')
    print("✓ AI Advisor API registered")


@advisor_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    """
    Get all active recommendations for a tenant
    
    Query params:
    - tenant_id (required)
    - status: pending|accepted|dismissed (default: pending)
    - limit: max results (default: 20)
    """
    session = SessionLocal()
    
    try:
        tenant_id = request.args.get('tenant_id')
        if not tenant_id:
            return jsonify({'error': 'tenant_id is required'}), 400
        
        status = request.args.get('status', 'pending')
        limit = int(request.args.get('limit', 20))
        
        # Query recommendations
        query = session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.tenant_id == tenant_id
        )
        
        if status:
            query = query.filter(
                AdvisorRecommendation.status == RecommendationStatus(status)
            )
        
        # Exclude expired recommendations
        query = query.filter(
            (AdvisorRecommendation.expires_at.is_(None)) |
            (AdvisorRecommendation.expires_at > datetime.utcnow())
        )
        
        recommendations = query.order_by(
            AdvisorRecommendation.created_at.desc()
        ).limit(limit).all()
        
        return jsonify({
            'tenant_id': tenant_id,
            'total': len(recommendations),
            'recommendations': [rec.to_dict() for rec in recommendations]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


@advisor_bp.route('/recommendations/<rec_id>', methods=['GET'])
def get_recommendation(rec_id: str):
    """Get specific recommendation details"""
    session = SessionLocal()
    
    try:
        recommendation = session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.id == rec_id
        ).first()
        
        if not recommendation:
            return jsonify({'error': 'Recommendation not found'}), 404
        
        return jsonify(recommendation.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


@advisor_bp.route('/recommendations/<rec_id>/accept', methods=['POST'])
def accept_recommendation(rec_id: str):
    """
    Accept a recommendation
    
    Body:
    {
        "feedback": "optional feedback string"
    }
    
    Returns the updated recommendation and any pre-filled draft data
    """
    session = SessionLocal()
    
    try:
        recommendation = session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.id == rec_id
        ).first()
        
        if not recommendation:
            return jsonify({'error': 'Recommendation not found'}), 404
        
        # Update status
        recommendation.status = RecommendationStatus.ACCEPTED
        recommendation.accepted_at = datetime.utcnow()
        
        # Store feedback if provided
        data = request.json or {}
        if data.get('feedback'):
            recommendation.tenant_feedback = {
                'feedback': data['feedback'],
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        
        session.commit()
        
        # Return recommendation with draft data
        response = recommendation.to_dict()
        response['draft_data'] = recommendation.pre_filled_data
        
        return jsonify({
            'success': True,
            'message': 'Recommendation accepted',
            'recommendation': response
        }), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


@advisor_bp.route('/recommendations/<rec_id>/dismiss', methods=['POST'])
def dismiss_recommendation(rec_id: str):
    """
    Dismiss a recommendation
    
    Body:
    {
        "reason": "optional reason string"
    }
    """
    session = SessionLocal()
    
    try:
        recommendation = session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.id == rec_id
        ).first()
        
        if not recommendation:
            return jsonify({'error': 'Recommendation not found'}), 404
        
        # Update status
        recommendation.status = RecommendationStatus.DISMISSED
        recommendation.dismissed_at = datetime.utcnow()
        
        # Store reason if provided
        data = request.json or {}
        if data.get('reason'):
            recommendation.tenant_feedback = {
                'dismiss_reason': data['reason'],
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        
        session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Recommendation dismissed'
        }), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


@advisor_bp.route('/recommendations/refresh', methods=['POST'])
def refresh_recommendations():
    """
    Generate new recommendations based on current signals
    
    Body:
    {
        "tenant_id": "tenant_codexdominion",
        "days": 30  // optional, default 30
    }
    
    This collects fresh signals, analyzes them, and creates new recommendations
    """
    session = SessionLocal()
    
    try:
        data = request.json
        tenant_id = data.get('tenant_id')
        days = data.get('days', 30)
        
        if not tenant_id:
            return jsonify({'error': 'tenant_id is required'}), 400
        
        # Collect signals
        signals = collect_tenant_signals(tenant_id, days=days)
        
        # Generate recommendations
        new_recs = generate_recommendations(tenant_id, signals)
        
        # Store recommendations in database
        stored_recs = []
        for rec_data in new_recs:
            rec_id = f"rec_{int(datetime.utcnow().timestamp())}_{random.randint(1000, 9999)}"
            
            recommendation = AdvisorRecommendation(
                id=rec_id,
                tenant_id=tenant_id,
                recommendation_type=RecommendationType(rec_data.get('type', 'optimization')),
                status=RecommendationStatus.PENDING,
                title=rec_data['title'],
                description=rec_data['description'],
                impact_level=rec_data['impact_level'],
                confidence_score=rec_data['confidence_score'],
                workflow_template_id=rec_data.get('workflow_template_id'),
                automation_template_id=rec_data.get('automation_template_id'),
                pre_filled_data=rec_data.get('pre_filled_data'),
                triggering_signals=rec_data['triggering_signals'],
                context=rec_data.get('context'),
                primary_action=rec_data['primary_action'],
                secondary_action=rec_data.get('secondary_action'),
                expires_at=datetime.fromisoformat(rec_data['expires_at'].replace('Z', '')) if rec_data.get('expires_at') else None,
                estimated_impact=rec_data.get('estimated_impact')
            )
            
            session.add(recommendation)
            stored_recs.append(recommendation)
        
        session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Generated {len(stored_recs)} new recommendations',
            'recommendations': [r.to_dict() for r in stored_recs],
            'signals_analyzed': {
                'store': signals['store_signals'],
                'workflow': signals['workflow_signals'],
                'marketing': signals['marketing_signals'],
                'customer': signals['customer_signals'],
                'automation': signals['automation_signals']
            }
        }), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


@advisor_bp.route('/recommendations/stats', methods=['GET'])
def get_advisor_stats():
    """
    Get AI Advisor performance statistics
    
    Query params:
    - tenant_id (required)
    - days: lookback period (default: 30)
    
    Returns:
    - Total recommendations generated
    - Acceptance rate
    - Dismissal rate
    - Estimated vs actual impact (learning loop)
    - Top recommendation types
    """
    session = SessionLocal()
    
    try:
        tenant_id = request.args.get('tenant_id')
        if not tenant_id:
            return jsonify({'error': 'tenant_id is required'}), 400
        
        days = int(request.args.get('days', 30))
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        # Get all recommendations in period
        recommendations = session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.tenant_id == tenant_id,
            AdvisorRecommendation.created_at >= cutoff
        ).all()
        
        total = len(recommendations)
        
        if total == 0:
            return jsonify({
                'tenant_id': tenant_id,
                'period_days': days,
                'total_recommendations': 0,
                'message': 'No recommendations generated yet'
            }), 200
        
        # Calculate stats
        accepted = sum(1 for r in recommendations if r.status == RecommendationStatus.ACCEPTED)
        dismissed = sum(1 for r in recommendations if r.status == RecommendationStatus.DISMISSED)
        pending = sum(1 for r in recommendations if r.status == RecommendationStatus.PENDING)
        completed = sum(1 for r in recommendations if r.status == RecommendationStatus.COMPLETED)
        
        # Count by type
        type_counts = {}
        for r in recommendations:
            rec_type = r.recommendation_type.value if r.recommendation_type else 'unknown'
            type_counts[rec_type] = type_counts.get(rec_type, 0) + 1
        
        # Average confidence
        avg_confidence = sum(r.confidence_score for r in recommendations) / total
        
        # Impact tracking (for learning loop)
        with_impact = [r for r in recommendations if r.actual_impact]
        impact_accuracy = len(with_impact) / total if total > 0 else 0
        
        return jsonify({
            'tenant_id': tenant_id,
            'period_days': days,
            'total_recommendations': total,
            'acceptance_rate': (accepted / total * 100) if total > 0 else 0,
            'dismissal_rate': (dismissed / total * 100) if total > 0 else 0,
            'pending_count': pending,
            'completed_count': completed,
            'avg_confidence_score': round(avg_confidence, 1),
            'recommendation_types': type_counts,
            'impact_tracking': {
                'recommendations_with_impact': len(with_impact),
                'impact_accuracy': round(impact_accuracy * 100, 1)
            },
            'learning_status': 'active' if accepted > 5 else 'warming_up'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


@advisor_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'operational',
        'service': 'AI Advisor API',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 200
