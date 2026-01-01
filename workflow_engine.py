"""
🔥 CODEX DOMINION - WORKFLOW ENGINE 🔥
=======================================
Database-backed workflow orchestration with RQ (Redis Queue)

This engine NO LONGER uses in-memory storage.
All workflows are persisted to PostgreSQL and executed via RQ workers.

Key Changes:
- No _actions dict
- create_workflow() writes to DB and enqueues RQ job
- get_workflow() reads from DB
- list_workflows() queries DB
- Worker execution via worker_tasks.py

Usage:
    from workflow_engine import workflow_engine
    
    workflow_id = workflow_engine.create_workflow(
        workflow_type_id="website_creation",
        created_by_agent="agent_jermaine",
        inputs={"domain": "example.com"},
        calculated_savings={"weekly_savings": 100},
        assigned_council_id="council_ops",
        auto_execute=True
    )
"""

from typing import Dict, Any, Optional, List
import uuid
import os
import time

from db import SessionLocal
from models import Workflow, WorkflowMetric, WorkflowType, WorkflowStatus
from rq import Queue
import redis

# Initialize Redis connection and RQ queue
redis_conn = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
queue = Queue("workflows", connection=redis_conn)


# Notification support
ENABLE_NOTIFICATIONS = os.getenv("ENABLE_WORKFLOW_NOTIFICATIONS", "true").lower() == "true"

# Council routing rules - map workflow types to council IDs
COUNCIL_RULES = {
    # Social & Media workflows
    "social.generate_launch_campaign_for_store": "council_media",
    "launch_campaign": "council_media",
    "social_media_post": "council_media",
    "content_creation": "council_media",
    "blog_post": "council_media",
    
    # Store & Commerce workflows
    "store.update_pricing": "council_commerce",
    "store_creation": "council_commerce",
    "product_launch": "council_commerce",
    "pricing_change": "council_commerce",
    "ecommerce_setup": "council_commerce",
    
    # Web workflows
    "website.create_landing_page": "council_web",
    "website_creation": "council_web",
    "landing_page": "council_web",
    "page_update": "council_web",
    
    # Automation workflows
    "automation.create_flow": "council_automation",
    "workflow_automation": "council_automation",
    "integration_setup": "council_automation",
    "api_connection": "council_automation",
    
    # Finance workflows
    "budget_allocation": "council_finance",
    "expense_approval": "council_finance",
    "payment_processing": "council_finance",
}


def get_council_for_workflow_type(workflow_type: str) -> Optional[str]:
    """
    Get the council ID for a given workflow type.
    
    Args:
        workflow_type: Workflow type ID (e.g., "store_creation")
    
    Returns:
        council_id or None if no rule exists
    
    Examples:
        >>> get_council_for_workflow_type("store_creation")
        "council_commerce"
        
        >>> get_council_for_workflow_type("unknown_type")
        None
    """
    return COUNCIL_RULES.get(workflow_type)


def add_council_rule(workflow_type: str, council_id: str):
    """
    Add or update a council routing rule.
    
    Args:
        workflow_type: Workflow type ID
        council_id: Council ID to assign (e.g., "council_commerce")
    
    Usage:
        add_council_rule("new_workflow_type", "council_media")
    """
    COUNCIL_RULES[workflow_type] = council_id
    print(f"✅ Added council rule: {workflow_type} → {council_id}")


def remove_council_rule(workflow_type: str):
    """
    Remove a council routing rule.
    
    Args:
        workflow_type: Workflow type ID to remove
    """
    if workflow_type in COUNCIL_RULES:
        del COUNCIL_RULES[workflow_type]
        print(f"✅ Removed council rule: {workflow_type}")
    else:
        print(f"⚠️  No rule exists for: {workflow_type}")


def list_council_rules() -> Dict[str, str]:
    """
    Get all council routing rules.
    
    Returns:
        Dictionary of workflow_type → council_id mappings
    """
    return COUNCIL_RULES.copy()


def _emit_notification_event(event: Dict[str, Any]):
    """
    Emit notification event to RQ queue
    
    Args:
        event: Event dict with workflow_id, event_type, etc.
    """
    if not ENABLE_NOTIFICATIONS:
        return
    
    try:
        from notification_worker import dispatch_workflow_notification
        queue.enqueue(dispatch_workflow_notification, event, job_timeout=300)
        print(f"✅ Notification event queued: {event.get('event_type')} for workflow {event.get('workflow_id')}")
    except Exception as e:
        print(f"⚠️ Failed to queue notification: {e}")


class WorkflowEngine:
    """
    Database-backed workflow orchestration engine
    
    All workflows are stored in PostgreSQL.
    Execution is handled by RQ workers (see worker_tasks.py).
    """
    
    def create_workflow(
        self,
        workflow_type_id: str,
        created_by_agent: str,
        inputs: Dict[str, Any],
        calculated_savings: Dict[str, Any],
        assigned_council_id: Optional[str] = None,
        auto_execute: bool = True,
        auto_route_councils: bool = True
    ) -> str:
        """
        Create a workflow record in database and optionally enqueue for execution.
        
        Args:
            workflow_type_id: Type of workflow (e.g., "website_creation")
            created_by_agent: Agent ID that created this workflow
            inputs: Workflow input parameters
            calculated_savings: Estimated savings/metrics
            assigned_council_id: Council to review this workflow (manual override)
            auto_execute: If True, enqueue for immediate RQ execution
            auto_route_councils: If True, automatically determine council via routing engine
            
        Returns:
            workflow_id: UUID of created workflow
        """
        session = SessionLocal()
        try:
            workflow_id = self._generate_id()
            
            # Determine initial status and council assignment
            initial_status = WorkflowStatus.PENDING
            
            # Auto-route to council using simplified rules-based approach
            if auto_route_councils and not assigned_council_id:
                # Check if workflow type has a council rule
                if workflow_type_id in COUNCIL_RULES:
                    assigned_council_id = COUNCIL_RULES[workflow_type_id]
                    initial_status = WorkflowStatus.PENDING_REVIEW
                    print(f"🎯 Routed to {assigned_council_id} (rules-based)")
                else:
                    # Fallback to content-based routing
                    try:
                        from council_routing_engine import create_council_review_request
                        
                        review_request = create_council_review_request(
                            workflow_id=workflow_id,
                            workflow_type_id=workflow_type_id,
                            inputs=inputs,
                            calculated_savings=calculated_savings,
                            created_by_agent=created_by_agent
                        )
                        
                        # Get primary council
                        primary_council = review_request["councils"]["primary"]
                        assigned_council_id = f"council_{primary_council}"
                        initial_status = WorkflowStatus.PENDING_REVIEW
                        
                        print(f"🎯 Auto-routed to {primary_council} council (content-based)")
                        print(f"   Required councils: {', '.join(review_request['councils']['required'])}")
                        print(f"   Triggers: {', '.join(review_request['content_analysis']['triggers'])}")
                        
                        # Store review request in workflow outputs for later reference
                        inputs["_council_review_request"] = review_request
                    except Exception as e:
                        print(f"⚠️ Council routing failed: {e}")
                        # No council assigned - workflow runs immediately
                        assigned_council_id = None
                        initial_status = WorkflowStatus.PENDING
            
            # If council is manually assigned, require review
            if assigned_council_id and initial_status == WorkflowStatus.PENDING:
                initial_status = WorkflowStatus.PENDING_REVIEW
            
            workflow = Workflow(
                id=workflow_id,
                workflow_type_id=workflow_type_id,
                created_by_agent=created_by_agent,
                inputs=inputs,
                calculated_savings=calculated_savings,
                status=initial_status,
                assigned_council_id=assigned_council_id
            )
            session.add(workflow)
            session.commit()
            
            status_msg = "pending review" if initial_status == WorkflowStatus.PENDING_REVIEW else "running"
            print(f"✅ Created workflow: {workflow_id} (type: {workflow_type_id}, status: {status_msg})")
            
            # Emit workflow started notification
            _emit_notification_event({
                "workflow_id": workflow_id,
                "event_type": "status_change",
                "step": "workflow_started",
                "is_start": True
            })
            
            # Enqueue for execution only if not pending review
            if auto_execute and initial_status != WorkflowStatus.PENDING_REVIEW:
                self.enqueue_execution(workflow_id)
            elif initial_status == WorkflowStatus.PENDING_REVIEW:
                print(f"⏸️  Workflow {workflow_id} awaiting council review - not auto-executing")
            
            return workflow_id
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error creating workflow: {e}")
            raise
        finally:
            session.close()
    
    def enqueue_execution(self, workflow_id: str):
        """
        Enqueue workflow for execution via RQ worker.
        
        Args:
            workflow_id: ID of workflow to execute
        """
        session = SessionLocal()
        try:
            # Get workflow to determine type
            workflow = session.query(Workflow).filter(Workflow.id == workflow_id).first()
            if not workflow:
                raise ValueError(f"Workflow {workflow_id} not found")
            
            # Route to appropriate worker based on workflow type
            if workflow.workflow_type_id.startswith("website."):
                from website_creation_worker import website_creation_task
                job = queue.enqueue(
                    website_creation_task,
                    workflow_id,
                    workflow.inputs,
                    job_timeout="15m"
                )
            elif workflow.workflow_type_id.startswith("customer_service."):
                # Future: customer service worker
                job = queue.enqueue(
                    "worker_tasks.execute_workflow",
                    workflow_id,
                    job_timeout="10m"
                )
            else:
                # Default generic worker
                job = queue.enqueue(
                    "worker_tasks.execute_workflow",
                    workflow_id,
                    job_timeout="10m"
                )
            
            print(f"📋 Enqueued workflow {workflow_id} as job {job.id}")
            
        except Exception as e:
            print(f"❌ Error enqueuing workflow {workflow_id}: {e}")
            # Update workflow status to failed
            self.update_status(workflow_id, WorkflowStatus.FAILED, error_message=str(e))
        finally:
            session.close()
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """
        Retrieve a workflow by ID from database.
        
        Args:
            workflow_id: ID of workflow to retrieve
            
        Returns:
            Workflow object or None if not found
        """
        session = SessionLocal()
        try:
            return session.query(Workflow).filter(Workflow.id == workflow_id).first()
        finally:
            session.close()
    
    def list_workflows(
        self, 
        limit: int = 50, 
        status: Optional[WorkflowStatus] = None,
        agent_id: Optional[str] = None
    ) -> List[Workflow]:
        """
        List workflows from database with optional filters.
        
        Args:
            limit: Maximum number of workflows to return
            status: Filter by workflow status
            agent_id: Filter by creator agent ID
            
        Returns:
            List of Workflow objects
        """
        session = SessionLocal()
        try:
            query = session.query(Workflow)
            
            if status:
                query = query.filter(Workflow.status == status)
            
            if agent_id:
                query = query.filter(Workflow.created_by_agent == agent_id)
            
            return query.order_by(Workflow.created_at.desc()).limit(limit).all()
        finally:
            session.close()
    
    def update_status(
        self, 
        workflow_id: str, 
        status: WorkflowStatus,
        error_message: Optional[str] = None
    ):
        """
        Update workflow status in database.
        
        Args:
            workflow_id: ID of workflow to update
            status: New status
            error_message: Optional error message if status is FAILED
        """
        session = SessionLocal()
        try:
            workflow = session.query(Workflow).filter(Workflow.id == workflow_id).first()
            if not workflow:
                print(f"⚠️  Workflow {workflow_id} not found")
                return
            
            workflow.status = status
            if error_message:
                workflow.error_message = error_message
            
            session.commit()
            
            print(f"✅ Updated workflow {workflow_id} status to {status.value}")
            
            # Emit notification events based on status
            if status == WorkflowStatus.COMPLETED:
                _emit_notification_event({
                    "workflow_id": workflow_id,
                    "event_type": "status_change",
                    "step": "workflow_complete",
                    "summary": workflow.outputs.get("summary", "Workflow completed successfully.")
                })
            elif status == WorkflowStatus.PENDING_REVIEW:
                _emit_notification_event({
                    "workflow_id": workflow_id,
                    "event_type": "status_change",
                    "status": "pending_review"
                })
            elif status == WorkflowStatus.FAILED:
                _emit_notification_event({
                    "workflow_id": workflow_id,
                    "event_type": "status_change",
                    "status": "failed"
                })
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error updating workflow status: {e}")
            raise
        finally:
            session.close()
    
    def record_step_completion(
        self, 
        workflow_id: str, 
        step_name: str,
        next_step_name: Optional[str] = None
    ):
        """
        Record completion of a workflow step and emit notification.
        
        Args:
            workflow_id: ID of workflow
            step_name: Name of completed step
            next_step_name: Optional name of next step
        """
        print(f"✅ Step completed: {step_name} for workflow {workflow_id}")
        
        # Emit step completed notification
        _emit_notification_event({
            "workflow_id": workflow_id,
            "event_type": "step_complete",
            "step_name": step_name,
            "next_step_name": next_step_name or "Final step",
            "status": "completed"
        })
        
        session.close()
    
    def record_metric(
        self,
        workflow_id: str,
        duration_seconds: float,
        estimated_weekly_savings: float,
        cpu_usage_percent: Optional[float] = None,
        memory_usage_mb: Optional[float] = None
    ):
        """
        Record performance metrics for a workflow execution.
        
        Args:
            workflow_id: ID of workflow
            duration_seconds: Execution duration
            estimated_weekly_savings: Estimated weekly savings
            cpu_usage_percent: Optional CPU usage
            memory_usage_mb: Optional memory usage
        """
        session = SessionLocal()
        try:
            metric = WorkflowMetric(
                id=self._generate_id(),
                workflow_id=workflow_id,
                duration_seconds=duration_seconds,
                estimated_weekly_savings=estimated_weekly_savings,
                cpu_usage_percent=cpu_usage_percent,
                memory_usage_mb=memory_usage_mb
            )
            session.add(metric)
            session.commit()
            print(f"📊 Recorded metrics for workflow {workflow_id}")
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error recording metrics: {e}")
            raise
        finally:
            session.close()
    
    def _generate_id(self) -> str:
        """Generate unique workflow ID"""
        return f"wf_{uuid.uuid4().hex[:16]}"


# Global singleton instance
workflow_engine = WorkflowEngine()


# Export for backward compatibility with old code
__all__ = ['WorkflowEngine', 'workflow_engine']
