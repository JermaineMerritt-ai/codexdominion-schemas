"""
Codex Dominion - AI Advisor Intelligence Model

This is the logic that turns signals into recommendations:
- Opportunity Detection (gaps, trends, declines, surges, seasonal windows, untapped potential)
- Risk Detection (low inventory, broken pages, failed workflows, automation conflicts, missing campaigns)
- Pattern Matching (industry patterns, seasonal cycles, similar tenants, historical performance)
- Template Matching (impact, relevance, approval history, tenant preferences)

This is the Dominion's strategic brain.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import random


class AdvisorIntelligence:
    """
    AI Advisor Intelligence Model
    
    Analyzes signals and generates actionable recommendations
    """
    
    def __init__(self, tenant_id: str, signals: Dict[str, Any]):
        self.tenant_id = tenant_id
        self.signals = signals
        self.recommendations = []
    
    def analyze_and_recommend(self) -> List[Dict[str, Any]]:
        """
        Run all analysis and generate recommendations
        
        Returns list of recommendation objects ready to be stored
        """
        self.recommendations = []
        
        # Run all detection methods
        self.detect_opportunities()
        self.detect_risks()
        self.detect_patterns()
        self.match_templates()
        
        return self.recommendations
    
    def detect_opportunities(self):
        """
        Look for: gaps, trends, surges, seasonal windows, untapped potential
        """
        store_signals = self.signals.get('store_signals', {})
        workflow_signals = self.signals.get('workflow_signals', {})
        marketing_signals = self.signals.get('marketing_signals', {})
        customer_signals = self.signals.get('customer_signals', {})
        
        # OPPORTUNITY: Low product count with healthy traffic
        if store_signals.get('product_count', 0) < 5 and store_signals.get('store_health') in ['limited', 'needs_products']:
            self.recommendations.append({
                'type': 'workflow',
                'title': 'Add New Products to Your Store',
                'description': f"Your store has only {store_signals.get('product_count', 0)} products. Adding more products could increase conversions and revenue.",
                'impact_level': 'high',
                'confidence_score': 90,
                'workflow_template_id': 'product_creation',
                'triggering_signals': {
                    'product_count': store_signals.get('product_count'),
                    'store_health': store_signals.get('store_health')
                },
                'context': {
                    'recommended_count': 3,
                    'seasonal_window': marketing_signals.get('seasonal_window')
                },
                'primary_action': 'review_draft',
                'estimated_impact': {
                    'revenue': '+20-30%',
                    'conversion': '+5%'
                }
            })
        
        # OPPORTUNITY: Seasonal window detected
        seasonal_window = marketing_signals.get('seasonal_window')
        if seasonal_window and seasonal_window in ['winter_holidays', 'spring', 'fall']:
            self.recommendations.append({
                'type': 'campaign',
                'title': f'Launch {seasonal_window.replace("_", " ").title()} Campaign',
                'description': f"It's {seasonal_window.replace('_', ' ')}! This is a perfect time to create seasonal content and engage your audience.",
                'impact_level': 'high',
                'confidence_score': 85,
                'workflow_template_id': 'seasonal_campaign',
                'triggering_signals': {
                    'seasonal_window': seasonal_window,
                    'days_since_last_post': marketing_signals.get('days_since_last_post')
                },
                'primary_action': 'review_draft',
                'estimated_impact': {
                    'engagement': '+15%',
                    'reach': '+25%'
                }
            })
        
        # OPPORTUNITY: Social posting gap
        if marketing_signals.get('social_gap_detected', False):
            days_since = marketing_signals.get('days_since_last_post', 0)
            self.recommendations.append({
                'type': 'workflow',
                'title': 'Resume Social Media Posting',
                'description': f"It's been {days_since} days since your last social post. Regular posting keeps your audience engaged.",
                'impact_level': 'medium',
                'confidence_score': 88,
                'workflow_template_id': 'social_post_generation',
                'triggering_signals': {
                    'days_since_last_post': days_since,
                    'posts_per_week': marketing_signals.get('posts_per_week', 0)
                },
                'primary_action': 'review_draft',
                'estimated_impact': {
                    'engagement': '+10%',
                    'follower_growth': '+5%'
                }
            })
        
        # OPPORTUNITY: High abandoned cart rate
        if customer_signals.get('abandoned_carts_7d', 0) > 5:
            cart_count = customer_signals.get('abandoned_carts_7d')
            recovery_rate = 0.15  # 15% typical recovery
            avg_value = customer_signals.get('avg_order_value', 50)
            potential_revenue = cart_count * recovery_rate * avg_value
            
            self.recommendations.append({
                'type': 'automation',
                'title': 'Enable Abandoned Cart Recovery',
                'description': f"You had {cart_count} abandoned carts this week. Enabling cart recovery could recover {int(cart_count * recovery_rate)} sales.",
                'impact_level': 'medium',
                'confidence_score': 85,
                'automation_template_id': 'abandoned_cart_automation',
                'triggering_signals': {
                    'abandoned_carts_7d': cart_count,
                    'abandoned_cart_rate': customer_signals.get('abandoned_cart_rate')
                },
                'primary_action': 'configure',
                'estimated_impact': {
                    'revenue': f'+${int(potential_revenue)}',
                    'recovered_carts': f'{int(cart_count * recovery_rate)}'
                }
            })
        
        # OPPORTUNITY: Workflow success rate suggests more automation
        if workflow_signals.get('success_rate', 0) > 80 and workflow_signals.get('avg_workflows_per_week', 0) > 2:
            self.recommendations.append({
                'type': 'automation',
                'title': 'Automate Your Successful Workflows',
                'description': f"Your workflows have an {int(workflow_signals.get('success_rate'))}% success rate. Consider automating repetitive tasks.",
                'impact_level': 'high',
                'confidence_score': 92,
                'automation_template_id': 'workflow_automation',
                'triggering_signals': {
                    'success_rate': workflow_signals.get('success_rate'),
                    'avg_workflows_per_week': workflow_signals.get('avg_workflows_per_week')
                },
                'primary_action': 'configure',
                'estimated_impact': {
                    'time_saved': '5-8 hours/week',
                    'consistency': '+20%'
                }
            })
    
    def detect_risks(self):
        """
        Flag: low inventory, failed workflows, automation conflicts, missing campaigns
        """
        store_signals = self.signals.get('store_signals', {})
        workflow_signals = self.signals.get('workflow_signals', {})
        automation_signals = self.signals.get('automation_signals', {})
        
        # RISK: Low inventory
        if store_signals.get('low_inventory_count', 0) > 0:
            low_count = store_signals.get('low_inventory_count')
            self.recommendations.append({
                'type': 'alert',
                'title': 'Low Inventory Alert',
                'description': f"{low_count} product(s) have low inventory (< 5 units). Consider restocking to avoid stockouts.",
                'impact_level': 'high',
                'confidence_score': 100,
                'triggering_signals': {
                    'low_inventory_count': low_count,
                    'avg_inventory': store_signals.get('avg_inventory')
                },
                'primary_action': 'view_details',
                'secondary_action': 'enable_auto_alert',
                'estimated_impact': {
                    'risk': 'Potential stockout',
                    'lost_revenue': '$200-500'
                },
                'expires_at': (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'
            })
        
        # RISK: High workflow failure rate
        if workflow_signals.get('failed', 0) > 3:
            failed_count = workflow_signals.get('failed')
            total = workflow_signals.get('total_workflows', 1)
            failure_rate = (failed_count / total * 100) if total > 0 else 0
            
            self.recommendations.append({
                'type': 'alert',
                'title': 'Workflow Failures Detected',
                'description': f"{failed_count} workflows failed recently ({int(failure_rate)}% failure rate). Review and fix issues.",
                'impact_level': 'high',
                'confidence_score': 100,
                'triggering_signals': {
                    'failed_workflows': failed_count,
                    'failure_rate': failure_rate
                },
                'primary_action': 'view_details',
                'estimated_impact': {
                    'risk': 'Lost productivity',
                    'time_wasted': f'{failed_count * 15} minutes'
                }
            })
        
        # RISK: Automation conflicts
        if automation_signals.get('conflicts'):
            conflicts = automation_signals.get('conflicts', [])
            self.recommendations.append({
                'type': 'alert',
                'title': 'Automation Conflicts Detected',
                'description': f"{len(conflicts)} automation conflict(s) may cause duplicate actions or unexpected behavior.",
                'impact_level': 'medium',
                'confidence_score': 85,
                'triggering_signals': {
                    'conflicts': conflicts
                },
                'primary_action': 'view_details',
                'secondary_action': 'resolve',
                'estimated_impact': {
                    'risk': 'Duplicate content',
                    'wasted_resources': '2-3 hours/week'
                }
            })
        
        # RISK: Automations never firing
        if automation_signals.get('never_fired'):
            never_fired = automation_signals.get('never_fired', [])
            if len(never_fired) > 0:
                self.recommendations.append({
                    'type': 'optimization',
                    'title': 'Inactive Automations Detected',
                    'description': f"{len(never_fired)} automation(s) have never fired. Review trigger conditions or disable if no longer needed.",
                    'impact_level': 'low',
                    'confidence_score': 90,
                    'triggering_signals': {
                        'never_fired': never_fired
                    },
                    'primary_action': 'review',
                    'estimated_impact': {
                        'efficiency': 'Clean up unused automations'
                    }
                })
    
    def detect_patterns(self):
        """
        Compare to: industry patterns, seasonal cycles, similar tenants, historical performance
        """
        workflow_signals = self.signals.get('workflow_signals', {})
        marketing_signals = self.signals.get('marketing_signals', {})
        customer_signals = self.signals.get('customer_signals', {})
        
        # PATTERN: Below industry average posting frequency
        posts_per_week = marketing_signals.get('posts_per_week', 0)
        industry_avg = 4.5  # Example: industry average
        
        if posts_per_week < industry_avg * 0.7:  # 30% below average
            self.recommendations.append({
                'type': 'optimization',
                'title': 'Increase Social Media Frequency',
                'description': f"You're posting {posts_per_week:.1f} times/week. Similar businesses post {industry_avg:.1f} times/week for better engagement.",
                'impact_level': 'medium',
                'confidence_score': 78,
                'triggering_signals': {
                    'posts_per_week': posts_per_week,
                    'industry_average': industry_avg
                },
                'context': {
                    'comparison': 'similar_tenants',
                    'percentile': 35
                },
                'primary_action': 'configure',
                'estimated_impact': {
                    'engagement': '+20%',
                    'reach': '+30%'
                }
            })
        
        # PATTERN: Repeat purchase rate comparison
        repeat_rate = customer_signals.get('repeat_purchase_rate', 0)
        target_rate = 0.40  # 40% target
        
        if repeat_rate < target_rate:
            self.recommendations.append({
                'type': 'campaign',
                'title': 'Increase Customer Retention',
                'description': f"Your repeat purchase rate is {int(repeat_rate * 100)}%. Target is {int(target_rate * 100)}%. Consider loyalty campaigns.",
                'impact_level': 'high',
                'confidence_score': 82,
                'workflow_template_id': 'loyalty_campaign',
                'triggering_signals': {
                    'repeat_purchase_rate': repeat_rate,
                    'target_rate': target_rate
                },
                'context': {
                    'gap': f'{int((target_rate - repeat_rate) * 100)}%'
                },
                'primary_action': 'review_draft',
                'estimated_impact': {
                    'revenue': '+15%',
                    'lifetime_value': '+$50/customer'
                }
            })
    
    def match_templates(self):
        """
        Select best workflow template or automation based on:
        - Impact
        - Relevance
        - Approval history (learning loop)
        - Tenant preferences
        """
        # This method is primarily called by other detection methods
        # Templates are matched based on triggering signals
        pass
    
    def calculate_confidence(self, signal_strength: float, data_quality: float, historical_accuracy: float = 0.85) -> int:
        """
        Calculate confidence score (0-100)
        
        Args:
            signal_strength: How strong the signal is (0-1)
            data_quality: Quality of data available (0-1)
            historical_accuracy: Historical accuracy of this recommendation type (0-1)
        
        Returns:
            Confidence score 0-100
        """
        confidence = (signal_strength * 0.4 + data_quality * 0.3 + historical_accuracy * 0.3) * 100
        return int(min(100, max(0, confidence)))
    
    def prioritize_recommendations(self) -> List[Dict[str, Any]]:
        """
        Sort recommendations by priority
        
        Priority factors:
        - Impact level (critical > high > medium > low)
        - Confidence score
        - Expiration (time-sensitive first)
        - Type (alerts first, then workflows, automations, optimizations)
        """
        impact_order = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        type_order = {'alert': 4, 'workflow': 3, 'automation': 2, 'campaign': 2, 'optimization': 1}
        
        def priority_score(rec):
            impact_score = impact_order.get(rec.get('impact_level', 'low'), 1) * 100
            confidence_score = rec.get('confidence_score', 50)
            type_score = type_order.get(rec.get('type', 'optimization'), 1) * 20
            expires_soon = 50 if rec.get('expires_at') else 0
            
            return impact_score + confidence_score + type_score + expires_soon
        
        return sorted(self.recommendations, key=priority_score, reverse=True)


def generate_recommendations(tenant_id: str, signals: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Main entry point for recommendation generation
    
    Usage:
        from advisor_signals import collect_tenant_signals
        from advisor_intelligence import generate_recommendations
        
        signals = collect_tenant_signals('tenant_codexdominion')
        recommendations = generate_recommendations('tenant_codexdominion', signals)
    """
    intelligence = AdvisorIntelligence(tenant_id, signals)
    recommendations = intelligence.analyze_and_recommend()
    return intelligence.prioritize_recommendations()
