"""
Codex Dominion - AI Advisor Signal Collection

The Advisor continuously monitors signals across the tenant's ecosystem:
- Store signals (products, inventory, pricing, health, traffic, conversion)
- Workflow signals (completed, failed, idle, overdue reviews, drafts)
- Marketing signals (campaign frequency, engagement, seasonal opportunities, social gaps)
- Customer behavior signals (abandoned carts, repeat purchases, high-value customers)
- Automation signals (firing too often, never firing, conflicts, deprecated templates)

The Advisor sees the whole empire at once.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from db import SessionLocal
from models import (
    Store, Workflow, WorkflowStatus, AutomationExecution,
    AutomationEvent, EventResult, AutomationRule, AutomationDebugLog
)


class SignalCollector:
    """Collects signals from all systems across the tenant's ecosystem"""
    
    def __init__(self, tenant_id: str, session=None):
        self.tenant_id = tenant_id
        self.session = session or SessionLocal()
        self.should_close_session = session is None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.should_close_session:
            self.session.close()
    
    def collect_all_signals(self, days: int = 30) -> Dict[str, Any]:
        """
        Collect all signals for the tenant
        
        Returns comprehensive signal data across all categories
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        return {
            'store_signals': self.collect_store_signals(),
            'workflow_signals': self.collect_workflow_signals(cutoff_date),
            'marketing_signals': self.collect_marketing_signals(cutoff_date),
            'customer_signals': self.collect_customer_signals(cutoff_date),
            'automation_signals': self.collect_automation_signals(cutoff_date),
            'metadata': {
                'tenant_id': self.tenant_id,
                'collected_at': datetime.utcnow().isoformat() + 'Z',
                'lookback_days': days
            }
        }
    
    def collect_store_signals(self) -> Dict[str, Any]:
        """
        Store signals: product count, inventory, pricing, health, traffic, conversion
        """
        # Get store data (simulated for now - in production, query actual tables)
        stores = self.session.query(Store).filter(
            Store.tenant_id == self.tenant_id
        ).all()
        
        if not stores:
            return {
                'store_count': 0,
                'product_count': 0,
                'avg_inventory': 0,
                'low_inventory_count': 0,
                'pricing_pattern': 'unknown',
                'store_health': 'unknown',
                'traffic_trend': 'unknown',
                'conversion_rate': 0
            }
        
        # Simulated product data (in production, query from Product table or external API)
        # For now, use store count as proxy
        product_count = len(stores) * 4  # Assume 4 products per store on average
        avg_inventory = 15.5  # Simulated
        low_inventory_count = 2  # Simulated
        pricing_pattern = 'mid-range'  # Simulated
        
        return {
            'store_count': len(stores),
            'product_count': product_count,
            'avg_inventory': round(avg_inventory, 1),
            'low_inventory_count': low_inventory_count,
            'pricing_pattern': pricing_pattern,
            'store_health': 'healthy' if product_count >= 5 else 'limited' if product_count >= 3 else 'needs_products',
            'traffic_trend': 'growing',  # In production, calculate from analytics
            'conversion_rate': 3.5  # In production, calculate from orders/visitors
        }
    
    def collect_workflow_signals(self, cutoff_date: datetime) -> Dict[str, Any]:
        """
        Workflow signals: completed, failed, idle, overdue reviews, drafts not submitted
        """
        workflows = self.session.query(Workflow).filter(
            Workflow.tenant_id == self.tenant_id,
            Workflow.created_at >= cutoff_date
        ).all()
        
        completed = sum(1 for w in workflows if w.status == WorkflowStatus.COMPLETED)
        failed = sum(1 for w in workflows if w.status == WorkflowStatus.FAILED)
        draft = sum(1 for w in workflows if w.status == WorkflowStatus.DRAFT)
        pending = sum(1 for w in workflows if w.status == WorkflowStatus.PENDING_APPROVAL)
        
        # Check for idle workflows (no activity in 7+ days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        idle_workflows = [
            w for w in workflows 
            if w.updated_at and w.updated_at < seven_days_ago 
            and w.status not in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED]
        ]
        
        # Check for overdue reviews (pending > 3 days)
        three_days_ago = datetime.utcnow() - timedelta(days=3)
        overdue_reviews = [
            w for w in workflows
            if w.status == WorkflowStatus.PENDING_APPROVAL
            and w.created_at and w.created_at < three_days_ago
        ]
        
        return {
            'total_workflows': len(workflows),
            'completed': completed,
            'failed': failed,
            'draft_count': draft,
            'pending_approval': pending,
            'idle_count': len(idle_workflows),
            'overdue_reviews': len(overdue_reviews),
            'success_rate': (completed / len(workflows) * 100) if workflows else 0,
            'avg_workflows_per_week': len(workflows) / 4.3  # Approximate weeks in 30 days
        }
    
    def collect_marketing_signals(self, cutoff_date: datetime) -> Dict[str, Any]:
        """
        Marketing signals: campaign frequency, engagement, seasonal opportunities, social gaps
        """
        # Get social post workflows
        social_workflows = self.session.query(Workflow).filter(
            Workflow.tenant_id == self.tenant_id,
            Workflow.workflow_type_id.like('%social%'),
            Workflow.created_at >= cutoff_date
        ).all()
        
        # Calculate posting frequency
        if social_workflows:
            days_since_first = (datetime.utcnow() - min(w.created_at for w in social_workflows if w.created_at)).days
            posts_per_week = len(social_workflows) / (days_since_first / 7) if days_since_first > 0 else 0
        else:
            posts_per_week = 0
        
        # Get last social post date
        if social_workflows:
            last_post = max(w.created_at for w in social_workflows if w.created_at)
            days_since_last_post = (datetime.utcnow() - last_post).days
        else:
            days_since_last_post = 999
        
        # Detect seasonal opportunities
        current_month = datetime.utcnow().month
        seasonal_window = None
        if current_month == 12:
            seasonal_window = 'winter_holidays'
        elif current_month in [1, 2]:
            seasonal_window = 'winter'
        elif current_month in [3, 4, 5]:
            seasonal_window = 'spring'
        elif current_month in [6, 7, 8]:
            seasonal_window = 'summer'
        elif current_month in [9, 10, 11]:
            seasonal_window = 'fall'
        
        return {
            'total_campaigns': len(social_workflows),
            'posts_per_week': round(posts_per_week, 1),
            'days_since_last_post': days_since_last_post,
            'social_gap_detected': days_since_last_post > 7,
            'seasonal_window': seasonal_window,
            'engagement_rate': 4.2,  # In production, calculate from analytics
            'best_posting_time': '10:00'  # In production, calculate from engagement data
        }
    
    def collect_customer_signals(self, cutoff_date: datetime) -> Dict[str, Any]:
        """
        Customer behavior signals: abandoned carts, repeat purchases, high-value customers, browsing patterns
        """
        # In production, query Order and Customer tables
        # For now, return simulated data
        
        return {
            'total_customers': 150,
            'new_customers_30d': 23,
            'repeat_customers': 45,
            'high_value_customers': 12,  # > $500 lifetime value
            'abandoned_carts_7d': 14,
            'abandoned_cart_rate': 0.35,  # 35%
            'avg_order_value': 67.50,
            'repeat_purchase_rate': 0.30,  # 30%
            'browsing_patterns': {
                'top_categories': ['digital_downloads', 'homeschool', 'wedding'],
                'avg_session_duration': 280,  # seconds
                'bounce_rate': 0.42
            }
        }
    
    def collect_automation_signals(self, cutoff_date: datetime) -> Dict[str, Any]:
        """
        Automation signals: firing too often, never firing, conflicts, deprecated templates
        """
        # Get all automations
        automations = self.session.query(AutomationRule).filter(
            AutomationRule.tenant_id == self.tenant_id
        ).all()
        
        # Get execution events
        events = self.session.query(AutomationEvent).filter(
            AutomationEvent.tenant_id == self.tenant_id,
            AutomationEvent.timestamp >= cutoff_date
        ).all()
        
        # Get debug logs
        debug_logs = self.session.query(AutomationDebugLog).filter(
            AutomationDebugLog.tenant_id == self.tenant_id,
            AutomationDebugLog.timestamp >= cutoff_date
        ).all()
        
        # Detect automations firing too often (> 10x per day)
        firing_counts = {}
        for event in events:
            firing_counts[event.automation_id] = firing_counts.get(event.automation_id, 0) + 1
        
        days_span = (datetime.utcnow() - cutoff_date).days or 1
        firing_too_often = [
            aid for aid, count in firing_counts.items()
            if count / days_span > 10
        ]
        
        # Detect automations never firing
        automation_ids = {a.id for a in automations}
        firing_ids = {e.automation_id for e in events}
        never_fired = list(automation_ids - firing_ids)
        
        # Detect deprecated templates
        deprecated = [
            a.id for a in automations
            if hasattr(a, 'template_version') and a.template_version in ['v1', 'v2']
        ]
        
        # Detect conflicts (simulated)
        conflicts = []
        social_automations = [a for a in automations if 'social' in a.id.lower()]
        if len(social_automations) > 1:
            conflicts.append({
                'type': 'overlapping_schedules',
                'automation_ids': [a.id for a in social_automations]
            })
        
        return {
            'total_automations': len(automations),
            'active_automations': sum(1 for a in automations if a.enabled),
            'total_executions': len(events),
            'successful_executions': sum(1 for e in events if e.result == EventResult.SUCCESS),
            'failed_executions': sum(1 for e in events if e.result == EventResult.FAILED),
            'firing_too_often': firing_too_often,
            'never_fired': never_fired,
            'deprecated_templates': deprecated,
            'conflicts': conflicts,
            'avg_executions_per_day': len(events) / days_span
        }
    
    def close(self):
        """Close session if we own it"""
        if self.should_close_session:
            self.session.close()


def collect_tenant_signals(tenant_id: str, days: int = 30) -> Dict[str, Any]:
    """
    Convenience function to collect all signals for a tenant
    
    Usage:
        signals = collect_tenant_signals('tenant_codexdominion', days=30)
    """
    with SignalCollector(tenant_id) as collector:
        return collector.collect_all_signals(days=days)
