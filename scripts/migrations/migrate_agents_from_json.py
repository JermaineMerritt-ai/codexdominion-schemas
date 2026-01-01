"""
CODEX DOMINION - AGENTS MIGRATION
========================================
Migrate agents from agents_simple.json to PostgreSQL/SQLite database

Usage:
    python scripts/migrations/migrate_agents_from_json.py
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
import uuid
from contextlib import contextmanager

# Set SQLite database before any imports
os.environ['DATABASE_URL'] = 'sqlite:///codexdominion.db'

# Add parent directory to path to import models
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models import Base, Agent, AgentReputation, AgentTraining
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Create SQLite engine directly
engine = create_engine(
    'sqlite:///codexdominion.db',
    echo=False,
    poolclass=StaticPool,
    connect_args={'check_same_thread': False}
)

# Create session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

@contextmanager
def get_db_session():
    """Context manager for database sessions"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def load_agents_json(json_path: str = "agents.json"):
    """Load agents from JSON file"""
    json_file = Path(__file__).parent.parent.parent / json_path
    if not json_file.exists():
        print(f"❌ JSON file not found: {json_file}")
        # Try agents_simple.json as fallback
        json_file = Path(__file__).parent.parent.parent / "agents_simple.json"
        if not json_file.exists():
            print("❌ No agents JSON file found (tried agents.json and agents_simple.json)")
            sys.exit(1)
    
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Handle both array and object with "agents" key
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and "agents" in data:
        return data["agents"]
    else:
        print("❌ Unexpected JSON structure. Expected array or object with 'agents' key")
        sys.exit(1)


def migrate_agents():
    """Migrate agents from JSON to Postgres"""
    print("🔄 Starting agent migration from JSON to Postgres...")
    
    # Connect to database using centralized session
    Base.metadata.create_all(engine)  # Ensure tables exist
    
    with get_db_session() as session:
        try:
            # Load JSON data
            agents_data = load_agents_json()
            print(f"📋 Found {len(agents_data)} agents in JSON")
            
            # Check existing agents
            existing_count = session.query(Agent).count()
            print(f"📊 Database currently has {existing_count} agents")
            
            # Process each agent
            agents_inserted = 0
            agents_updated = 0
            reputation_inserted = 0
            training_inserted = 0
            skipped = 0
            
            for agent_data in agents_data:
                agent_id = agent_data.get("id")
                if not agent_id:
                    print(f"⚠️  Skipping agent without ID: {agent_data.get('name', 'Unknown')}")
                    skipped += 1
                    continue
                
                # Check if agent already exists
                existing_agent = session.query(Agent).filter(Agent.id == agent_id).first()
                
                if existing_agent:
                    # Update existing agent (match new models.py structure)
                    existing_agent.name = agent_data.get("name") or existing_agent.name
                    existing_agent.display_name = agent_data.get("display_name") or existing_agent.display_name
                    existing_agent.description = agent_data.get("description") or existing_agent.description
                    existing_agent.avatar_url = agent_data.get("avatar_url") or existing_agent.avatar_url
                    existing_agent.is_active = agent_data.get("is_active", existing_agent.is_active)
                    if agent_data.get("capabilities"):
                        existing_agent.capabilities = agent_data.get("capabilities")
                    agents_updated += 1
                    print(f"✏️  Updated agent: {existing_agent.name} ({agent_id})")
                else:
                    # Create new agent (matching new models.py structure)
                    agent = Agent(
                        id=agent_id,
                        name=agent_data.get("name", "Unnamed Agent"),
                        display_name=agent_data.get("display_name"),
                        description=agent_data.get("description"),
                        avatar_url=agent_data.get("avatar_url"),
                        is_active=agent_data.get("is_active", True),
                        capabilities=agent_data.get("capabilities", {}),
                        created_at=datetime.utcnow()
                    )
                    session.add(agent)
                    agents_inserted += 1
                print(f"➕ Inserted agent: {agent.name} ({agent_id})")
                
                # Create initial reputation record
                rep = AgentReputation(
                    id=f"rep_{uuid.uuid4().hex[:12]}",
                    agent_id=agent_id,
                    trust_score=0.0,
                    total_actions=0,
                    successful_actions=0,
                    failed_actions=0,
                    total_savings_generated=0.0
                )
                session.add(rep)
                reputation_inserted += 1
                
                # Create initial training record
                training = AgentTraining(
                    id=f"train_{uuid.uuid4().hex[:12]}",
                    agent_id=agent_id,
                    training_type="initial",
                    topic="Agent initialization",
                    outcome="success",
                    notes="Created via migration"
                )
                session.add(training)
                training_inserted += 1
            
            # Handle reputation (1-to-1 relationship)
            reputation_data = agent_data.get("reputation")
            if reputation_data:
                existing_rep = session.query(AgentReputation).filter(
                    AgentReputation.agent_id == agent_id
                ).first()
                
                if existing_rep:
                    # Update existing reputation (match new models.py structure)
                    existing_rep.trust_score = reputation_data.get("trust_score", existing_rep.trust_score)
                    existing_rep.total_actions = reputation_data.get("total_actions", existing_rep.total_actions)
                    existing_rep.successful_actions = reputation_data.get("successful_actions", existing_rep.successful_actions)
                    existing_rep.failed_actions = reputation_data.get("failed_actions", existing_rep.failed_actions)
                    existing_rep.total_savings_generated = reputation_data.get("total_savings_generated", existing_rep.total_savings_generated)
                    print(f"  ✏️  Updated reputation: trust_score={existing_rep.trust_score}")
                else:
                    # Create new reputation (match new models.py structure)
                    reputation = AgentReputation(
                        id=f"rep_{uuid.uuid4().hex[:12]}",
                        agent_id=agent_id,
                        trust_score=reputation_data.get("trust_score", 0.0),
                        total_actions=reputation_data.get("total_actions", 0),
                        successful_actions=reputation_data.get("successful_actions", 0),
                        failed_actions=reputation_data.get("failed_actions", 0),
                        total_savings_generated=reputation_data.get("total_savings_generated", 0.0)
                    )
                    session.add(reputation)
                    reputation_inserted += 1
                    print(f"  ➕ Inserted reputation: trust_score={reputation.trust_score}")
            
            # Handle training (1-to-1 relationship)
            training_data = agent_data.get("training")
            if training_data:
                existing_training = session.query(AgentTraining).filter(
                    AgentTraining.agent_id == agent_id
                ).first()
                
                if existing_training:
                    # Update existing training (match new models.py structure)
                    existing_training.training_type = training_data.get("training_type", existing_training.training_type)
                    existing_training.topic = training_data.get("topic", existing_training.topic)
                    existing_training.outcome = training_data.get("outcome", existing_training.outcome)
                    existing_training.feedback_score = training_data.get("feedback_score", existing_training.feedback_score)
                    existing_training.notes = training_data.get("notes", existing_training.notes)
                    print(f"  ✏️  Updated training: type={existing_training.training_type}")
                else:
                    # Create new training (match new models.py structure)
                    training = AgentTraining(
                        id=f"train_{uuid.uuid4().hex[:12]}",
                        agent_id=agent_id,
                        training_type=training_data.get("training_type", "initial"),
                        topic=training_data.get("topic", "Agent initialization"),
                        outcome=training_data.get("outcome", "success"),
                        feedback_score=training_data.get("feedback_score"),
                        notes=training_data.get("notes", "Created via migration")
                    )
                    session.add(training)
                    training_inserted += 1
                    print(f"  ➕ Inserted training: {training.training_type}")
            
            # Commit transaction
            session.commit()
            
            print("\n" + "=" * 60)
            print("✅ Migration complete!")
            print(f"   Agents inserted: {agents_inserted}")
            print(f"   Agents updated:  {agents_updated}")
            print(f"   Reputations inserted: {reputation_inserted}")
            print(f"   Training records inserted: {training_inserted}")
            print(f"   Skipped:  {skipped}")
            print(f"   Total agents in DB: {session.query(Agent).count()}")
            print(f"   Total reputations in DB: {session.query(AgentReputation).count()}")
            print(f"   Total training records in DB: {session.query(AgentTraining).count()}")
            print("=" * 60)
        
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    migrate_agents()
