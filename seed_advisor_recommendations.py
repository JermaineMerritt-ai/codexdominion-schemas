"""
Seed AI Advisor Recommendations

Creates sample recommendations to demonstrate the AI Advisor system.
"""

from datetime import datetime, timedelta
from db import SessionLocal
from models import AdvisorRecommendation, RecommendationType, RecommendationStatus
import random


def seed_advisor_recommendations():
    """Create sample advisor recommendations"""
    session = SessionLocal()
    
    try:
        tenant_id = "tenant_codexdominion"
        
        # Clear existing recommendations for clean demo
        session.query(AdvisorRecommendation).filter(
            AdvisorRecommendation.tenant_id == tenant_id
        ).delete()
        
        recommendations = [
            # 1. Add New Products (High impact, workflow)
            {
                'id': f"rec_{int(datetime.utcnow().timestamp())}_{random.randint(1000, 9999)}",
                'tenant_id': tenant_id,
                'recommendation_type': RecommendationType.WORKFLOW,
                'status': RecommendationStatus.PENDING,
                'title': 'Add a New Product: Winter Collection',
                'description': 'Your store has high traffic but only 3 active products. Adding a seasonal product could increase conversions.',
                'impact_level': 'high',
                'confidence_score': 92,
                'workflow_template_id': 'product_creation',
                'pre_filled_data': {
                    'product_type': 'seasonal',
                    'category': 'winter_collection',
                    'suggested_price_range': '15-25'
                },
                'triggering_signals': {
                    'product_count': 3,
                    'store_health': 'limited',
                    'seasonal_window': 'winter'
                },
                'context': {
                    'seasonal_window': 'winter',
                    'recommended_count': 3
                },
                'primary_action': 'review_draft',
                'secondary_action': 'dismiss',
                'estimated_impact': {
                    'revenue': '+20-30%',
                    'conversion': '+5%'
                }
            },
            
            # 2. Enable Abandoned Cart Automation (Medium impact, automation)
            {
                'id': f"rec_{int(datetime.utcnow().timestamp()) + 1}_{random.randint(1000, 9999)}",
                'tenant_id': tenant_id,
                'recommendation_type': RecommendationType.AUTOMATION,
                'status': RecommendationStatus.PENDING,
                'title': 'Enable Abandoned Cart Automation',
                'description': 'You had 14 abandoned carts this week. Enabling this automation could recover 2-3 sales.',
                'impact_level': 'medium',
                'confidence_score': 88,
                'automation_template_id': 'abandoned_cart_recovery',
                'pre_filled_data': {
                    'trigger_delay': '2_hours',
                    'email_template': 'cart_reminder',
                    'discount_offer': '10%'
                },
                'triggering_signals': {
                    'abandoned_carts_7d': 14,
                    'abandoned_cart_rate': 0.35
                },
                'primary_action': 'configure',
                'secondary_action': 'dismiss',
                'estimated_impact': {
                    'revenue': '+$250',
                    'recovered_carts': '2-3'
                }
            },
            
            # 3. Resume Social Media Posting (Medium impact, workflow)
            {
                'id': f"rec_{int(datetime.utcnow().timestamp()) + 2}_{random.randint(1000, 9999)}",
                'tenant_id': tenant_id,
                'recommendation_type': RecommendationType.CAMPAIGN,
                'status': RecommendationStatus.PENDING,
                'title': 'Resume Social Media Posting',
                'description': "It's been 10 days since your last social post. Regular posting keeps your audience engaged.",
                'impact_level': 'medium',
                'confidence_score': 85,
                'workflow_template_id': 'social_post_generation',
                'pre_filled_data': {
                    'platforms': ['Instagram', 'TikTok'],
                    'post_type': 'product_showcase',
                    'frequency': 'weekly'
                },
                'triggering_signals': {
                    'days_since_last_post': 10,
                    'posts_per_week': 0.3
                },
                'primary_action': 'review_draft',
                'secondary_action': 'dismiss',
                'estimated_impact': {
                    'engagement': '+10%',
                    'follower_growth': '+5%'
                }
            },
            
            # 4. Low Inventory Alert (High impact, alert)
            {
                'id': f"rec_{int(datetime.utcnow().timestamp()) + 3}_{random.randint(1000, 9999)}",
                'tenant_id': tenant_id,
                'recommendation_type': RecommendationType.ALERT,
                'status': RecommendationStatus.PENDING,
                'title': 'Low Inventory Alert',
                'description': '2 product(s) have low inventory (< 5 units). Consider restocking to avoid stockouts.',
                'impact_level': 'high',
                'confidence_score': 100,
                'triggering_signals': {
                    'low_inventory_count': 2,
                    'avg_inventory': 8.5
                },
                'primary_action': 'view_details',
                'secondary_action': 'enable_auto_alert',
                'expires_at': datetime.utcnow() + timedelta(days=7),
                'estimated_impact': {
                    'risk': 'Potential stockout',
                    'lost_revenue': '$200-500'
                }
            },
            
            # 5. Automate Successful Workflows (High impact, automation)
            {
                'id': f"rec_{int(datetime.utcnow().timestamp()) + 4}_{random.randint(1000, 9999)}",
                'tenant_id': tenant_id,
                'recommendation_type': RecommendationType.AUTOMATION,
                'status': RecommendationStatus.PENDING,
                'title': 'Suggested Automation: Weekly Social Posts',
                'description': "Your workflows have an 85% success rate. Consider automating repetitive tasks to save time.",
                'impact_level': 'high',
                'confidence_score': 92,
                'automation_template_id': 'weekly_social_automation',
                'pre_filled_data': {
                    'schedule': 'every_monday_9am',
                    'platforms': ['Instagram', 'TikTok'],
                    'auto_generate_content': True
                },
                'triggering_signals': {
                    'success_rate': 85,
                    'avg_workflows_per_week': 3.5
                },
                'primary_action': 'configure',
                'secondary_action': 'dismiss',
                'estimated_impact': {
                    'time_saved': '5-8 hours/week',
                    'consistency': '+20%'
                }
            },
            
            # 6. Increase Social Frequency (Medium impact, optimization)
            {
                'id': f"rec_{int(datetime.utcnow().timestamp()) + 5}_{random.randint(1000, 9999)}",
                'tenant_id': tenant_id,
                'recommendation_type': RecommendationType.OPTIMIZATION,
                'status': RecommendationStatus.PENDING,
                'title': 'Increase Social Media Frequency',
                'description': "You're posting 2.5 times/week. Similar businesses post 4.5 times/week for better engagement.",
                'impact_level': 'medium',
                'confidence_score': 78,
                'triggering_signals': {
                    'posts_per_week': 2.5,
                    'industry_average': 4.5
                },
                'context': {
                    'comparison': 'similar_tenants',
                    'percentile': 35
                },
                'primary_action': 'configure',
                'secondary_action': 'dismiss',
                'estimated_impact': {
                    'engagement': '+20%',
                    'reach': '+30%'
                }
            }
        ]
        
        # Create recommendation objects
        for rec_data in recommendations:
            recommendation = AdvisorRecommendation(**rec_data)
            session.add(recommendation)
        
        session.commit()
        
        print(f"✓ Successfully seeded {len(recommendations)} advisor recommendations")
        print(f"  High Impact: {sum(1 for r in recommendations if r['impact_level'] == 'high')}")
        print(f"  Medium Impact: {sum(1 for r in recommendations if r['impact_level'] == 'medium')}")
        print(f"  Low Impact: {sum(1 for r in recommendations if r['impact_level'] == 'low')}")
        print(f"  Avg Confidence: {sum(r['confidence_score'] for r in recommendations) / len(recommendations):.1f}%")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error seeding recommendations: {e}")
        raise
    
    finally:
        session.close()


if __name__ == '__main__':
    seed_advisor_recommendations()
