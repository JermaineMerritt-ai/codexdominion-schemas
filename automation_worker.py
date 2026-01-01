"""
Automation Execution Worker

Background worker that listens for triggers and executes automation rules.

Components:
1. Trigger Listeners (event stream, cron scheduler, metric monitor)
2. Condition Evaluator
3. Governance Checker
4. Action Executor
5. Notification System

Usage:
    # Run as standalone process
    python automation_worker.py
    
    # Or integrate into existing worker
    from automation_worker import AutomationWorker
    worker = AutomationWorker()
    worker.start()
"""

import time
import schedule
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import threading
import logging
from db import SessionLocal
from models import (
    AutomationRule, AutomationExecution, Tenant, Workflow, WorkflowTemplate,
    TriggerType, ActionType, RiskLevel
)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


class TriggerListener:
    """Base class for trigger listeners"""
    
    def __init__(self, worker: 'AutomationWorker'):
        self.worker = worker
    
    def listen(self):
        """Override in subclasses"""
        raise NotImplementedError


class EventListener(TriggerListener):
    """
    Listens for system events and triggers automations.
    
    Events:
    - product_added
    - workflow_completed
    - store_health_changed
    - marketing_site_deployed
    - customer_signup
    """
    
    def __init__(self, worker: 'AutomationWorker'):
        super().__init__(worker)
        self.event_queue = []
    
    def emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit an event to the queue"""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.utcnow()
        }
        self.event_queue.append(event)
        logger.info(f"Event emitted: {event_type}")
    
    def listen(self):
        """Process event queue"""
        while True:
            if self.event_queue:
                event = self.event_queue.pop(0)
                self.worker.handle_event_trigger(event)
            time.sleep(1)


class ScheduleListener(TriggerListener):
    """
    Listens for scheduled times and triggers automations.
    
    Patterns:
    - Daily: Every day at specific time
    - Weekly: Specific day of week at specific time
    - Monthly: Specific day of month at specific time
    - Seasonal: Specific date (e.g., December 1st)
    """
    
    def listen(self):
        """Check schedules every minute"""
        while True:
            self.worker.check_schedules()
            time.sleep(60)  # Check every minute


class ThresholdMonitor(TriggerListener):
    """
    Monitors metrics and triggers automations when thresholds are crossed.
    
    Metrics:
    - product_count
    - workflow_completion_rate
    - store_traffic
    - campaign_performance
    - customer_churn_rate
    """
    
    def listen(self):
        """Monitor thresholds every 5 minutes"""
        while True:
            self.worker.check_thresholds()
            time.sleep(300)  # Check every 5 minutes


class BehaviorTracker(TriggerListener):
    """
    Tracks customer behavior and triggers automations.
    
    Behaviors:
    - abandoned_cart
    - product_viewed_not_bought
    - repeat_purchase
    - high_value_customer
    - dormant_customer
    """
    
    def listen(self):
        """Check behaviors every 10 minutes"""
        while True:
            self.worker.check_behaviors()
            time.sleep(600)  # Check every 10 minutes


class AutomationWorker:
    """
    Main automation execution worker.
    
    Coordinates trigger listeners, evaluates conditions, checks governance,
    executes actions, and sends notifications.
    """
    
    def __init__(self):
        self.running = False
        self.listeners = []
        
        # Initialize trigger listeners
        self.event_listener = EventListener(self)
        self.schedule_listener = ScheduleListener(self)
        self.threshold_monitor = ThresholdMonitor(self)
        self.behavior_tracker = BehaviorTracker(self)
        
        self.listeners = [
            self.event_listener,
            self.schedule_listener,
            self.threshold_monitor,
            self.behavior_tracker
        ]
    
    def start(self):
        """Start the automation worker"""
        logger.info("🔥 Starting Automation Worker...")
        self.running = True
        
        # Start each listener in its own thread
        threads = []
        for listener in self.listeners:
            thread = threading.Thread(target=listener.listen, daemon=True)
            thread.start()
            threads.append(thread)
            logger.info(f"✓ {listener.__class__.__name__} started")
        
        logger.info("✓ All listeners active. Worker is running.")
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down worker...")
            self.running = False
    
    def stop(self):
        """Stop the automation worker"""
        self.running = False
        logger.info("Automation worker stopped")
    
    # ========================================================================
    # TRIGGER HANDLERS
    # ========================================================================
    
    def handle_event_trigger(self, event: Dict[str, Any]):
        """
        Handle event-based triggers.
        
        Args:
            event: Event dictionary with type, data, timestamp
        """
        session = SessionLocal()
        try:
            # Find automations triggered by this event
            automations = session.query(AutomationRule).filter(
                AutomationRule.enabled == True,
                AutomationRule.trigger_type == TriggerType.EVENT
            ).all()
            
            for automation in automations:
                event_type = automation.trigger_config.get('event_type')
                if event_type == event['type']:
                    logger.info(f"Event trigger matched: {automation.name}")
                    self.execute_automation(automation, event['data'], 'event')
        
        finally:
            session.close()
    
    def check_schedules(self):
        """Check schedule-based triggers"""
        session = SessionLocal()
        try:
            now = datetime.utcnow()
            current_time = now.strftime("%H:%M")
            current_day = now.strftime("%A").lower()
            current_date = now.day
            
            # Find schedule-based automations
            automations = session.query(AutomationRule).filter(
                AutomationRule.enabled == True,
                AutomationRule.trigger_type == TriggerType.SCHEDULE
            ).all()
            
            for automation in automations:
                pattern = automation.trigger_config.get('pattern')
                trigger_time = automation.trigger_config.get('time', '09:00')
                
                should_trigger = False
                
                if pattern == 'daily' and trigger_time == current_time:
                    should_trigger = True
                elif pattern == 'weekly':
                    trigger_day = automation.trigger_config.get('day', 'monday')
                    if trigger_day == current_day and trigger_time == current_time:
                        should_trigger = True
                elif pattern == 'monthly':
                    trigger_date = automation.trigger_config.get('date', 1)
                    if trigger_date == current_date and trigger_time == current_time:
                        should_trigger = True
                
                if should_trigger:
                    # Check if already triggered today
                    if automation.last_triggered_at:
                        last_trigger_date = automation.last_triggered_at.date()
                        if last_trigger_date == now.date():
                            continue  # Already triggered today
                    
                    logger.info(f"Schedule trigger matched: {automation.name}")
                    context = {"current_time": current_time, "current_day": current_day}
                    self.execute_automation(automation, context, 'scheduler')
        
        finally:
            session.close()
    
    def check_thresholds(self):
        """Check threshold-based triggers"""
        session = SessionLocal()
        try:
            # Find threshold-based automations
            automations = session.query(AutomationRule).filter(
                AutomationRule.enabled == True,
                AutomationRule.trigger_type == TriggerType.THRESHOLD
            ).all()
            
            for automation in automations:
                metric = automation.trigger_config.get('metric')
                operator = automation.trigger_config.get('operator')
                threshold_value = automation.trigger_config.get('value')
                
                # Get current metric value (would integrate with actual metrics)
                current_value = self.get_metric_value(automation.tenant_id, metric)
                
                if current_value is None:
                    continue
                
                # Check if threshold is crossed
                threshold_crossed = False
                if operator == '<' and current_value < threshold_value:
                    threshold_crossed = True
                elif operator == '>' and current_value > threshold_value:
                    threshold_crossed = True
                elif operator == '<=' and current_value <= threshold_value:
                    threshold_crossed = True
                elif operator == '>=' and current_value >= threshold_value:
                    threshold_crossed = True
                elif operator == '=' and current_value == threshold_value:
                    threshold_crossed = True
                
                if threshold_crossed:
                    logger.info(f"Threshold trigger matched: {automation.name} ({metric} {operator} {threshold_value})")
                    context = {metric: current_value}
                    self.execute_automation(automation, context, 'threshold_monitor')
        
        finally:
            session.close()
    
    def check_behaviors(self):
        """Check behavior-based triggers"""
        session = SessionLocal()
        try:
            # Find behavior-based automations
            automations = session.query(AutomationRule).filter(
                AutomationRule.enabled == True,
                AutomationRule.trigger_type == TriggerType.BEHAVIOR
            ).all()
            
            for automation in automations:
                behavior_type = automation.trigger_config.get('behavior_type')
                
                # Get customers matching behavior (would integrate with actual customer data)
                matching_customers = self.get_customers_with_behavior(
                    automation.tenant_id,
                    behavior_type,
                    automation.trigger_config
                )
                
                for customer in matching_customers:
                    logger.info(f"Behavior trigger matched: {automation.name} for customer {customer['id']}")
                    context = {
                        "customer_id": customer['id'],
                        "behavior_type": behavior_type,
                        **customer
                    }
                    self.execute_automation(automation, context, 'behavior_tracker')
        
        finally:
            session.close()
    
    # ========================================================================
    # EXECUTION PIPELINE
    # ========================================================================
    
    def execute_automation(self, automation: AutomationRule, context: Dict[str, Any], trigger_source: str):
        """
        Execute an automation through the full pipeline:
        1. Create execution log
        2. Evaluate conditions
        3. Check governance
        4. Execute action
        5. Record results
        6. Send notifications
        
        Args:
            automation: AutomationRule to execute
            context: Trigger context data
            trigger_source: Source of trigger (event, scheduler, etc.)
        """
        session = SessionLocal()
        try:
            # 1. Create execution log
            execution = AutomationExecution(
                automation_rule_id=automation.id,
                tenant_id=automation.tenant_id,
                trigger_source=trigger_source,
                trigger_data=context
            )
            
            start_time = datetime.utcnow()
            automation.last_triggered_at = start_time
            
            # 2. Evaluate conditions
            logger.info(f"Evaluating conditions for {automation.name}")
            conditions_met = automation.evaluate_conditions(context)
            execution.conditions_met = conditions_met
            
            if not conditions_met:
                logger.info(f"Conditions not met for {automation.name}")
                execution.success = False
                execution.error_message = "Conditions not met"
                session.add(execution)
                session.commit()
                return
            
            logger.info(f"✓ Conditions met for {automation.name}")
            
            # 3. Check governance
            if automation.requires_approval:
                can_auto_approve = automation.should_auto_approve(context)
                if not can_auto_approve:
                    logger.info(f"⚠️ {automation.name} requires council approval")
                    execution.required_approval = True
                    execution.success = False
                    execution.error_message = "Requires council approval"
                    session.add(execution)
                    session.commit()
                    
                    # Send notification to council
                    self.notify_council_approval_needed(automation, context)
                    return
            
            # 4. Execute action
            logger.info(f"Executing action: {automation.action_type.value}")
            execution.action_started_at = datetime.utcnow()
            
            try:
                action_result = self.execute_action(automation, context)
                execution.action_result = action_result
                execution.action_completed_at = datetime.utcnow()
                execution.success = True
                logger.info(f"✓ Action executed successfully for {automation.name}")
                
            except Exception as action_error:
                logger.error(f"✗ Action execution failed: {str(action_error)}")
                execution.error_message = str(action_error)
                execution.success = False
            
            # 5. Record results
            end_time = datetime.utcnow()
            execution.execution_time_ms = (end_time - start_time).total_seconds() * 1000
            automation.record_execution(execution.success, execution.execution_time_ms)
            
            session.add(execution)
            session.commit()
            
            # 6. Send notifications
            if execution.success:
                self.notify_execution_success(automation, execution, context)
            else:
                self.notify_execution_failure(automation, execution, context)
        
        except Exception as e:
            logger.error(f"Automation execution error: {str(e)}")
            session.rollback()
        
        finally:
            session.close()
    
    def execute_action(self, automation: AutomationRule, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the automation's action.
        
        Args:
            automation: AutomationRule with action config
            context: Execution context
        
        Returns:
            Action result dictionary
        """
        action_type = automation.action_type
        action_config = automation.action_config
        
        if action_type == ActionType.START_WORKFLOW:
            return self.action_start_workflow(automation, action_config, context)
        
        elif action_type == ActionType.SEND_NOTIFICATION:
            return self.action_send_notification(automation, action_config, context)
        
        elif action_type == ActionType.UPDATE_PRODUCT:
            return self.action_update_product(automation, action_config, context)
        
        elif action_type == ActionType.GENERATE_CAMPAIGN:
            return self.action_generate_campaign(automation, action_config, context)
        
        elif action_type == ActionType.CREATE_LANDING_PAGE:
            return self.action_create_landing_page(automation, action_config, context)
        
        elif action_type == ActionType.ADD_PRODUCT:
            return self.action_add_product(automation, action_config, context)
        
        elif action_type == ActionType.UPDATE_STORE:
            return self.action_update_store(automation, action_config, context)
        
        elif action_type == ActionType.GENERATE_DRAFT:
            return self.action_generate_draft(automation, action_config, context)
        
        else:
            raise ValueError(f"Unknown action type: {action_type}")
    
    # ========================================================================
    # ACTION HANDLERS
    # ========================================================================
    
    def action_start_workflow(self, automation: AutomationRule, config: Dict, context: Dict) -> Dict:
        """Start a workflow from template"""
        # TODO: Integrate with workflow_engine
        logger.info(f"Starting workflow: {config.get('workflow_type_id')}")
        return {
            "action": "start_workflow",
            "workflow_id": "workflow_placeholder",
            "status": "simulated"
        }
    
    def action_send_notification(self, automation: AutomationRule, config: Dict, context: Dict) -> Dict:
        """Send notification to recipients"""
        recipients = config.get('recipients', [])
        message = config.get('message', '')
        logger.info(f"Sending notification to {recipients}: {message}")
        return {
            "action": "send_notification",
            "recipients": recipients,
            "status": "sent"
        }
    
    def action_update_product(self, automation: AutomationRule, config: Dict, context: Dict) -> Dict:
        """Update product data"""
        product_id = config.get('product_id') or context.get('product_id')
        updates = config.get('updates', {})
        logger.info(f"Updating product {product_id}: {updates}")
        return {
            "action": "update_product",
            "product_id": product_id,
            "status": "updated"
        }
    
    def action_generate_campaign(self, automation: AutomationRule, config: Dict, context: Dict) -> Dict:
        """Generate marketing campaign"""
        template_id = config.get('template_id')
        channels = config.get('channels', [])
        logger.info(f"Generating campaign on {channels} using template {template_id}")
        return {
            "action": "generate_campaign",
            "campaign_id": "campaign_placeholder",
            "status": "created"
        }
    
    def action_create_landing_page(self, automation: AutomationRule, config: Dict, context: Dict) -> Dict:
        """Create landing page"""
        template_id = config.get('template_id')
        logger.info(f"Creating landing page from template {template_id}")
        return {
            "action": "create_landing_page",
            "page_id": "page_placeholder",
            "status": "created"
        }
    
    def action_add_product(self, automation: AutomationRule, config: Dict, context: Dict) -> Dict:
        """Add new product"""
        template_id = config.get('template_id')
        count = config.get('count', 1)
        logger.info(f"Adding {count} product(s) from template {template_id}")
        return {
            "action": "add_product",
            "products_added": count,
            "status": "created"
        }
    
    def action_update_store(self, automation: AutomationRule, config: Dict, context: Dict) -> Dict:
        """Update store settings"""
        updates = config.get('updates', {})
        logger.info(f"Updating store: {updates}")
        return {
            "action": "update_store",
            "status": "updated"
        }
    
    def action_generate_draft(self, automation: AutomationRule, config: Dict, context: Dict) -> Dict:
        """Generate workflow draft"""
        template_id = config.get('template_id')
        logger.info(f"Generating draft from template {template_id}")
        return {
            "action": "generate_draft",
            "draft_id": "draft_placeholder",
            "status": "created"
        }
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def get_metric_value(self, tenant_id: str, metric: str) -> Optional[float]:
        """
        Get current value of a metric.
        
        Args:
            tenant_id: Tenant ID
            metric: Metric name (e.g., 'product_count')
        
        Returns:
            Current metric value or None
        """
        # TODO: Integrate with actual metrics system
        # This is a placeholder that returns mock data
        mock_metrics = {
            "product_count": 2,
            "store_traffic": 150,
            "conversion_rate": 0.03,
            "campaign_performance": 0.75
        }
        return mock_metrics.get(metric)
    
    def get_customers_with_behavior(self, tenant_id: str, behavior_type: str, config: Dict) -> List[Dict]:
        """
        Get customers matching a behavior pattern.
        
        Args:
            tenant_id: Tenant ID
            behavior_type: Behavior type (e.g., 'abandoned_cart')
            config: Behavior configuration
        
        Returns:
            List of customer dictionaries
        """
        # TODO: Integrate with actual customer data system
        # This is a placeholder that returns mock data
        return []
    
    def notify_council_approval_needed(self, automation: AutomationRule, context: Dict):
        """Notify council that approval is needed"""
        logger.info(f"📧 Notifying council for approval: {automation.name}")
        # TODO: Integrate with notification system
    
    def notify_execution_success(self, automation: AutomationRule, execution: AutomationExecution, context: Dict):
        """Notify on successful execution"""
        logger.info(f"✓ Execution succeeded: {automation.name}")
        # TODO: Integrate with notification system
    
    def notify_execution_failure(self, automation: AutomationRule, execution: AutomationExecution, context: Dict):
        """Notify on failed execution"""
        logger.error(f"✗ Execution failed: {automation.name} - {execution.error_message}")
        # TODO: Integrate with notification system


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    worker = AutomationWorker()
    worker.start()
