"""
🔥 RQ Worker Tasks - Background Job Processing
===============================================
Background tasks for Redis Queue (RQ) workers

Usage:
    rq worker workflows
"""

import os
import time
from datetime import datetime
from typing import Optional

# Import database and models
from db import SessionLocal
from models import Workflow, WorkflowMetric
from sqlalchemy import func

# Import workflow engine for execution logic
from workflow_engine import workflow_engine, ActionStatus


def execute_workflow(workflow_id: str) -> dict:
    """
    Execute a workflow in the background
    
    This function is called by RQ workers to process workflows asynchronously.
    It retrieves the workflow from the database, executes it, and saves metrics.
    
    Args:
        workflow_id: The ID of the workflow action to execute
        
    Returns:
        dict: Execution result with status, duration, and savings
    """
    session = SessionLocal()
    start_time = time.time()
    
    try:
        print(f"🚀 Starting workflow execution: {workflow_id}")
        
        # Get workflow from database
        workflow = session.query(Workflow).filter(Workflow.id == workflow_id).first()
        
        if not workflow:
            print(f"❌ Workflow {workflow_id} not found in database")
            return {
                "status": "error",
                "workflow_id": workflow_id,
                "error": "Workflow not found"
            }
        
        # Execute the workflow logic (currently simulated)
        # TODO: run actual automation here.
        # For now: simulate delay
        print(f"⚙️  Executing workflow type: {workflow.workflow_type_id}")
        time.sleep(5)
        
        # Update workflow status
        workflow.status = "completed"
        workflow.updated_at = func.now()
        
        # Extract weekly savings from calculated_savings
        weekly_savings = 0
        if workflow.calculated_savings:
            weekly_savings = (
                workflow.calculated_savings.get("weekly_savings")
                or workflow.calculated_savings.get("total_weekly_savings")
                or 0
            )
        
        # Create workflow metric
        metric = WorkflowMetric(
            workflow_id=workflow.id,
            duration_seconds=time.time() - start_time,
            estimated_weekly_savings=weekly_savings
        )
        session.add(metric)
        session.commit()
        
        result = {
            "status": "success",
            "workflow_id": workflow_id,
            "workflow_type": workflow.workflow_type_id,
            "duration_seconds": time.time() - start_time,
            "weekly_savings": weekly_savings,
            "completed_at": datetime.utcnow().isoformat()
        }
        
        print(f"✅ Workflow {workflow_id} completed in {time.time() - start_time:.2f}s")
        print(f"💰 Estimated savings: ${weekly_savings:.2f}/week")
        
        return result
        
    except Exception as e:
        print(f"❌ Error executing workflow {workflow_id}: {e}")
        session.rollback()
        # Optionally log this error
        raise
        
    finally:
        session.close()


def cleanup_old_workflows(days: int = 30) -> dict:
    """
    Clean up old completed workflows from the database
    
    This is a maintenance task that can be run periodically.
    
    Args:
        days: Number of days to keep workflows (default: 30)
        
    Returns:
        dict: Cleanup result with count of deleted workflows
    """
    session = SessionLocal()
    
    try:
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Delete old completed workflows
        deleted_count = session.query(Workflow).filter(
            Workflow.status == "completed",
            Workflow.completed_at < cutoff_date
        ).delete()
        
        session.commit()
        
        print(f"🧹 Cleaned up {deleted_count} workflows older than {days} days")
        
        return {
            "status": "success",
            "deleted_count": deleted_count,
            "cutoff_date": cutoff_date.isoformat()
        }
        
    except Exception as e:
        print(f"❌ Error cleaning up workflows: {e}")
        session.rollback()
        
        return {
            "status": "error",
            "error": str(e)
        }
        
    finally:
        session.close()


def generate_weekly_report() -> dict:
    """
    Generate weekly workflow performance report
    
    This task aggregates workflow metrics and can be scheduled weekly.
    
    Returns:
        dict: Report with workflow statistics
    """
    session = SessionLocal()
    
    try:
        from datetime import timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        # Count workflows by status
        total_workflows = session.query(Workflow).filter(
            Workflow.created_at >= week_ago
        ).count()
        
        completed_workflows = session.query(Workflow).filter(
            Workflow.created_at >= week_ago,
            Workflow.status == "completed"
        ).count()
        
        # Sum weekly savings
        from sqlalchemy import func
        total_savings = session.query(
            func.sum(WorkflowMetric.estimated_weekly_savings)
        ).join(Workflow).filter(
            Workflow.created_at >= week_ago
        ).scalar() or 0
        
        # Average execution time
        avg_duration = session.query(
            func.avg(WorkflowMetric.duration_seconds)
        ).join(Workflow).filter(
            Workflow.created_at >= week_ago
        ).scalar() or 0
        
        report = {
            "status": "success",
            "period": "last_7_days",
            "total_workflows": total_workflows,
            "completed_workflows": completed_workflows,
            "completion_rate": (completed_workflows / total_workflows * 100) if total_workflows > 0 else 0,
            "total_weekly_savings": float(total_savings),
            "avg_duration_seconds": float(avg_duration),
            "generated_at": datetime.utcnow().isoformat()
        }
        
        print(f"📊 Weekly report generated:")
        print(f"   Total workflows: {total_workflows}")
        print(f"   Completed: {completed_workflows} ({report['completion_rate']:.1f}%)")
        print(f"   Total savings: ${total_savings:.2f}/week")
        print(f"   Avg duration: {avg_duration:.2f}s")
        
        return report
        
    except Exception as e:
        print(f"❌ Error generating weekly report: {e}")
        
        return {
            "status": "error",
            "error": str(e)
        }
        
    finally:
        session.close()


# Additional worker tasks can be added here as needed
# Examples:
# - send_workflow_notification(workflow_id, recipient_email)
# - retry_failed_workflow(workflow_id)
# - archive_completed_workflows(older_than_days)
# - generate_council_report(council_id)
