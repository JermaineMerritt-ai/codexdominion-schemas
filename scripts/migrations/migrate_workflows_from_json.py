"""
CODEX DOMINION - WORKFLOWS MIGRATION
===========================================
Migrate workflows from JSON/in-memory state to PostgreSQL database

Usage:
    python scripts/migrations/migrate_workflows_from_json.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import uuid

# Add parent directory to path to import models
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models import Base, Workflow, WorkflowMetric, WorkflowVote, WorkflowType
from database import get_db_session, engine


def load_workflows_json(json_path: str = "workflows.json"):
    """Load workflows from JSON file (if persisted)"""
    json_file = Path(__file__).parent.parent.parent / json_path
    if not json_file.exists():
        print(f"⚠️  Workflow JSON file not found: {json_file}")
        print("⚠️  If workflows are in-memory only, you'll need to export them first")
        return []
    
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Handle both array and object with "workflows" key
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and "workflows" in data:
        return data["workflows"]
    else:
        print("❌ Unexpected JSON structure. Expected array or object with 'workflows' key")
        return []


def migrate_workflows():
    """Migrate workflows from JSON to Postgres"""
    print("🔄 Starting workflow migration from JSON to Postgres...")
    
    # Connect to database using centralized session
    Base.metadata.create_all(engine)  # Ensure tables exist
    
    with get_db_session() as session:
        try:
            # Load JSON data
            workflows_data = load_workflows_json()
        if not workflows_data:
            print("⚠️  No workflows found. Migration skipped.")
            return
        
        print(f"📋 Found {len(workflows_data)} workflows in JSON")
        
        # Check existing workflows
        existing_count = session.query(Workflow).count()
        print(f"📊 Database currently has {existing_count} workflows")
        
        # Process each workflow
        workflows_inserted = 0
        workflows_updated = 0
        metrics_inserted = 0
        votes_inserted = 0
        skipped = 0
        
        for workflow_data in workflows_data:
            workflow_id = workflow_data.get("id")
            if not workflow_id:
                print(f"⚠️  Skipping workflow without ID")
                skipped += 1
                continue
            
            # Check if workflow already exists
            existing_workflow = session.query(Workflow).filter(Workflow.id == workflow_id).first()
            
            if existing_workflow:
                # Update existing workflow (match new models.py structure)
                # Note: workflow_type_id and created_by_agent are immutable
                existing_workflow.assigned_council_id = workflow_data.get("assigned_council_id") or existing_workflow.assigned_council_id
                existing_workflow.status = workflow_data.get("status", existing_workflow.status)
                existing_workflow.inputs = workflow_data.get("inputs") or existing_workflow.inputs
                existing_workflow.outputs = workflow_data.get("outputs") or existing_workflow.outputs
                existing_workflow.calculated_savings = workflow_data.get("calculated_savings") or existing_workflow.calculated_savings
                existing_workflow.error_message = workflow_data.get("error_message")
                existing_workflow.retry_count = workflow_data.get("retry_count", existing_workflow.retry_count)
                existing_workflow.updated_at = datetime.utcnow()
                workflows_updated += 1
                print(f"✏️  Updated workflow: {workflow_id} (type: {existing_workflow.workflow_type_id})")
            else:
                # Create new workflow (matching new models.py structure)
                workflow = Workflow(
                    id=workflow_id,
                    workflow_type_id=workflow_data.get("workflow_type_id", "unknown"),
                    created_by_agent=workflow_data.get("created_by_agent", "system"),
                    assigned_council_id=workflow_data.get("assigned_council_id"),
                    status=workflow_data.get("status", "pending"),
                    inputs=workflow_data.get("inputs", {}),
                    outputs=workflow_data.get("outputs", {}),
                    calculated_savings=workflow_data.get("calculated_savings", {}),
                    error_message=workflow_data.get("error_message"),
                    retry_count=workflow_data.get("retry_count", 0),
                    created_at=datetime.utcnow()
                )
                session.add(workflow)
                workflows_inserted += 1
                print(f"➕ Inserted workflow: {workflow_id} (type: {workflow.workflow_type_id})")
            
            # Handle metrics (1-to-many relationship)
            metrics_data = workflow_data.get("metrics")
            if metrics_data:
                # Check if metrics already exist
                existing_metrics = session.query(WorkflowMetric).filter(
                    WorkflowMetric.workflow_id == workflow_id
                ).first()
                
                if not existing_metrics:
                    # Create new metrics
                    metrics = WorkflowMetric(
                        workflow_id=workflow_id,
                        duration_seconds=metrics_data.get("duration_seconds", 0),
                        estimated_weekly_savings=metrics_data.get("estimated_weekly_savings", 0.0),
                        actual_savings=metrics_data.get("actual_savings"),
                        efficiency_score=metrics_data.get("efficiency_score"),
                        completed_at=metrics_data.get("completed_at") or datetime.utcnow()
                    )
                    session.add(metrics)
                    metrics_inserted += 1
                    print(f"  ➕ Inserted metrics: duration={metrics.duration_seconds}s")
            
            # Handle votes (1-to-many relationship)
            votes_data = workflow_data.get("votes", [])
            for vote_data in votes_data:
                # Check if vote already exists
                existing_vote = session.query(WorkflowVote).filter(
                    WorkflowVote.workflow_id == workflow_id,
                    WorkflowVote.member_id == vote_data.get("member_id")
                ).first()
                
                if not existing_vote:
                    # Create new vote
                    vote = WorkflowVote(
                        workflow_id=workflow_id,
                        member_id=vote_data.get("member_id"),
                        vote=vote_data.get("vote", "abstain"),
                        reason=vote_data.get("reason"),
                        timestamp=vote_data.get("timestamp") or datetime.utcnow()
                    )
                    session.add(vote)
                    votes_inserted += 1
                    print(f"  ➕ Inserted vote: {vote.member_id} voted {vote.vote}")
        
        # Commit transaction
        session.commit()
        
        print("\n" + "=" * 60)
        print("✅ Migration complete!")
        print(f"   Workflows inserted: {workflows_inserted}")
        print(f"   Workflows updated:  {workflows_updated}")
        print(f"   Metrics inserted: {metrics_inserted}")
        print(f"   Votes inserted: {votes_inserted}")
        print(f"   Skipped:  {skipped}")
        print(f"   Total workflows in DB: {session.query(Workflow).count()}")
        print(f"   Total metrics in DB: {session.query(WorkflowMetric).count()}")
        print(f"   Total votes in DB: {session.query(WorkflowVote).count()}")
        print("=" * 60)
        
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    migrate_workflows()
