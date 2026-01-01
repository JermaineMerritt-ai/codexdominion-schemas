"""
Quick Reference: Database Usage Patterns
Copy-paste these patterns into your Flask/FastAPI code
"""

# ============================================================================
# PATTERN 1: Context Manager (Recommended for most cases)
# ============================================================================

from database import get_db_session
from models import Agent

def get_agents_list():
    with get_db_session() as session:
        agents = session.query(Agent).all()
        return [a.to_dict() for a in agents]


# ============================================================================
# PATTERN 2: Manual Session (When you need more control)
# ============================================================================

from database import get_session
from models import Council

def get_council_by_id(council_id: str):
    session = get_session()
    try:
        council = session.query(Council).filter(Council.id == council_id).first()
        return council.to_dict() if council else None
    finally:
        session.close()


# ============================================================================
# PATTERN 3: Flask Route with Context Manager
# ============================================================================

from flask import Flask, jsonify
from database import get_db_session
from models import Agent
from sqlalchemy.orm import joinedload

app = Flask(__name__)

@app.route('/api/agents')
def api_get_agents():
    with get_db_session() as session:
        agents = session.query(Agent).options(
            joinedload(Agent.reputation),
            joinedload(Agent.training)
        ).all()
        return jsonify([a.to_dict() for a in agents])


# ============================================================================
# PATTERN 4: Flask Route with Manual Session
# ============================================================================

from flask import Flask, jsonify
from database import get_session
from models import Council

app = Flask(__name__)

@app.route('/api/councils/<council_id>')
def api_get_council(council_id):
    session = get_session()
    try:
        council = session.query(Council).filter(Council.id == council_id).first()
        if not council:
            return jsonify({'error': 'Council not found'}), 404
        return jsonify(council.to_dict())
    finally:
        session.close()


# ============================================================================
# PATTERN 5: Flask App Teardown (Cleanup on shutdown)
# ============================================================================

from flask import Flask
from database import close_db

app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    close_db()


# ============================================================================
# PATTERN 6: FastAPI Dependency Injection
# ============================================================================

from fastapi import FastAPI, Depends
from database import get_db_session
from models import Agent
from typing import Generator
from sqlalchemy.orm import Session

app = FastAPI()

def get_db() -> Generator[Session, None, None]:
    with get_db_session() as session:
        yield session

@app.get('/api/agents')
def read_agents(session: Session = Depends(get_db)):
    agents = session.query(Agent).all()
    return [a.to_dict() for a in agents]


# ============================================================================
# PATTERN 7: Query with JOINs (Eager Loading)
# ============================================================================

from database import get_db_session
from models import Agent, Council, CouncilMember
from sqlalchemy.orm import joinedload

def get_agent_with_councils(agent_id: str):
    with get_db_session() as session:
        # Eager load relationships
        agent = session.query(Agent).options(
            joinedload(Agent.reputation),
            joinedload(Agent.training)
        ).filter(Agent.id == agent_id).first()
        
        # Get councils via junction table
        councils = session.query(Council).join(
            CouncilMember, Council.id == CouncilMember.council_id
        ).filter(CouncilMember.agent_id == agent_id).all()
        
        return {
            **agent.to_dict(),
            'reputation': agent.reputation.to_dict() if agent.reputation else None,
            'training': agent.training.to_dict() if agent.training else None,
            'councils': [c.to_dict() for c in councils]
        }


# ============================================================================
# PATTERN 8: Filtering and Pagination
# ============================================================================

from database import get_db_session
from models import Workflow

def get_workflows_paginated(page: int = 1, per_page: int = 10, status: str = None):
    with get_db_session() as session:
        query = session.query(Workflow)
        
        # Add filters
        if status:
            query = query.filter(Workflow.status == status)
        
        # Pagination
        offset = (page - 1) * per_page
        workflows = query.offset(offset).limit(per_page).all()
        total = query.count()
        
        return {
            'workflows': [w.to_dict() for w in workflows],
            'page': page,
            'per_page': per_page,
            'total': total
        }


# ============================================================================
# PATTERN 9: Creating New Records
# ============================================================================

from database import get_db_session
from models import Agent, AgentReputation, AgentTraining
from datetime import datetime

def create_agent(agent_data: dict):
    with get_db_session() as session:
        # Create agent
        agent = Agent(
            id=agent_data['id'],
            name=agent_data['name'],
            role=agent_data.get('role'),
            created_at=datetime.utcnow()
        )
        session.add(agent)
        
        # Create reputation
        reputation = AgentReputation(
            agent_id=agent.id,
            score=0,
            total_savings=0.0,
            workflows_executed=0,
            approval_rate=0.0,
            updated_at=datetime.utcnow()
        )
        session.add(reputation)
        
        # Session automatically commits on context exit
        return agent.to_dict()


# ============================================================================
# PATTERN 10: Updating Records
# ============================================================================

from database import get_db_session
from models import Agent
from datetime import datetime

def update_agent(agent_id: str, updates: dict):
    with get_db_session() as session:
        agent = session.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            return None
        
        # Update fields
        for key, value in updates.items():
            if hasattr(agent, key):
                setattr(agent, key, value)
        
        # Session automatically commits
        return agent.to_dict()


# ============================================================================
# PATTERN 11: Database Info and Health Check
# ============================================================================

from database import get_session, get_db_info

def health_check():
    """Check database health"""
    try:
        session = get_session()
        session.execute("SELECT 1")
        session.close()
        
        info = get_db_info()
        return {
            'status': 'healthy',
            'database': info['url'],
            'environment': info['environment']
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }


# ============================================================================
# PATTERN 12: Initialize Database Tables
# ============================================================================

from database import init_db

def setup_database():
    """Create all tables defined in models.py"""
    init_db()
    print("Database tables created successfully!")


# ============================================================================
# Common Imports Quick Reference
# ============================================================================

"""
# Essential imports for any database operation:

from database import get_db_session, get_session, close_db
from models import Agent, AgentReputation, AgentTraining, Council, CouncilMember, Workflow, WorkflowMetric, WorkflowVote
from sqlalchemy.orm import joinedload
from datetime import datetime

# Flask:
from flask import Flask, jsonify, request

# FastAPI:
from fastapi import FastAPI, Depends
from typing import Generator
from sqlalchemy.orm import Session
"""

# ============================================================================
# Testing Your Setup
# ============================================================================

"""
# Test database connection:
python test_db_connection.py

# Test and create schema:
python test_db_connection.py --init

# Test in Python REPL:
python
>>> from database import get_db_session
>>> from models import Council
>>> with get_db_session() as session:
...     councils = session.query(Council).all()
...     print(f"Found {len(councils)} councils")
"""
