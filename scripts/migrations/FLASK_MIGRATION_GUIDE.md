# Flask Endpoint Migration Guide: JSON → Postgres

## 📋 Overview

This guide shows how to migrate Flask endpoints from reading JSON files to querying Postgres database using SQLAlchemy ORM.

## 🎯 Migration Pattern

### Before (JSON)
```python
import json
from flask import jsonify

def load_councils():
    with open('councils.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/api/councils')
def get_councils():
    councils = load_councils()
    return jsonify(councils)
```

### After (Postgres)
```python
from flask import jsonify
from models import Council
from database import get_session

@app.route('/api/councils')
def get_councils():
    session = get_session()
    councils = session.query(Council).all()
    return jsonify([c.to_dict() for c in councils])
```

## 📦 Required Setup

### 1. Database Session Manager (database.py)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

DATABASE_URL = "postgresql://postgres:password@localhost:5432/codexdominion"

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(bind=engine)
session_factory = scoped_session(SessionLocal)

def get_session():
    """Get thread-safe database session"""
    return session_factory()
```

### 2. Model Serialization (models.py)

Add `to_dict()` methods to all models:

```python
class Council(Base):
    __tablename__ = 'councils'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    purpose = Column(Text)
    domain = Column(String)
    primary_engines = Column(JSONB)
    oversight = Column(JSONB)
    status = Column(String, default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Serialize to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'purpose': self.purpose,
            'domain': self.domain,
            'primary_engines': self.primary_engines,
            'oversight': self.oversight,
            'status': self.status,
            'created_at': self.created_at.isoformat() + 'Z'
        }
```

## 🔄 Endpoint Migration Examples

### Example 1: List All Councils

**Before (JSON)**:
```python
@app.route('/api/councils')
def get_councils():
    councils = json.load(open('councils.json'))
    return jsonify(councils)
```

**After (Postgres)**:
```python
from models import Council
from database import get_session

@app.route('/api/councils')
def get_councils():
    session = get_session()
    councils = session.query(Council).all()
    return jsonify([c.to_dict() for c in councils])
```

### Example 2: Get Single Council by ID

**Before (JSON)**:
```python
@app.route('/api/councils/<council_id>')
def get_council(council_id):
    councils = json.load(open('councils.json'))
    council = next((c for c in councils if c['id'] == council_id), None)
    if not council:
        return jsonify({'error': 'Council not found'}), 404
    return jsonify(council)
```

**After (Postgres)**:
```python
from models import Council
from database import get_session

@app.route('/api/councils/<council_id>')
def get_council(council_id):
    session = get_session()
    council = session.query(Council).filter(Council.id == council_id).first()
    if not council:
        return jsonify({'error': 'Council not found'}), 404
    return jsonify(council.to_dict())
```

### Example 3: Agent Profile with Relationships

**Before (JSON)**:
```python
@app.route('/api/agents/<agent_id>')
def get_agent_profile(agent_id):
    agents = json.load(open('agents.json'))
    agent = next((a for a in agents if a['id'] == agent_id), None)
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    # Manually add reputation and training
    reputation = agent.get('reputation', {})
    training = agent.get('training', {})
    
    return jsonify({
        **agent,
        'reputation': reputation,
        'training': training
    })
```

**After (Postgres with JOINs)**:
```python
from models import Agent
from database import get_session
from sqlalchemy.orm import joinedload

@app.route('/api/agents/<agent_id>')
def get_agent_profile(agent_id):
    session = get_session()
    
    # Eager load relationships
    agent = session.query(Agent).options(
        joinedload(Agent.reputation),
        joinedload(Agent.training)
    ).filter(Agent.id == agent_id).first()
    
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    # Serialize with nested objects
    return jsonify({
        **agent.to_dict(),
        'reputation': agent.reputation.to_dict() if agent.reputation else None,
        'training': agent.training.to_dict() if agent.training else None
    })
```

### Example 4: Council with Members

**Before (JSON)**:
```python
@app.route('/api/councils/<council_id>')
def get_council_detail(council_id):
    councils = json.load(open('councils.json'))
    council = next((c for c in councils if c['id'] == council_id), None)
    if not council:
        return jsonify({'error': 'Council not found'}), 404
    
    # Manually fetch member IDs (if stored separately)
    member_ids = council.get('members', [])
    agents = json.load(open('agents.json'))
    members = [a for a in agents if a['id'] in member_ids]
    
    return jsonify({
        **council,
        'members': members
    })
```

**After (Postgres with JOIN)**:
```python
from models import Council, Agent, CouncilMember
from database import get_session
from sqlalchemy.orm import joinedload

@app.route('/api/councils/<council_id>')
def get_council_detail(council_id):
    session = get_session()
    
    # Fetch council with members via junction table
    council = session.query(Council).filter(Council.id == council_id).first()
    if not council:
        return jsonify({'error': 'Council not found'}), 404
    
    # Get members via council_members junction table
    members = session.query(Agent).join(
        CouncilMember, Agent.id == CouncilMember.agent_id
    ).filter(CouncilMember.council_id == council_id).all()
    
    return jsonify({
        **council.to_dict(),
        'members': [m.to_dict() for m in members]
    })
```

### Example 5: Workflows with Metrics

**Before (JSON)**:
```python
@app.route('/api/workflows')
def get_workflows():
    workflows = json.load(open('workflows.json'))
    return jsonify(workflows)
```

**After (Postgres with JOIN)**:
```python
from models import Workflow, WorkflowMetric
from database import get_session
from sqlalchemy.orm import joinedload

@app.route('/api/workflows')
def get_workflows():
    session = get_session()
    
    # Eager load metrics
    workflows = session.query(Workflow).options(
        joinedload(Workflow.metrics)
    ).all()
    
    result = []
    for wf in workflows:
        wf_dict = wf.to_dict()
        # Include first metric (or aggregate)
        if wf.metrics:
            wf_dict['metrics'] = wf.metrics[0].to_dict()
        result.append(wf_dict)
    
    return jsonify(result)
```

## 🔍 Query Optimization Patterns

### Pattern 1: Eager Loading (N+1 Prevention)

**Bad (N+1 queries)**:
```python
agents = session.query(Agent).all()
for agent in agents:
    print(agent.reputation.score)  # Triggers separate query per agent
```

**Good (Single query)**:
```python
agents = session.query(Agent).options(
    joinedload(Agent.reputation),
    joinedload(Agent.training)
).all()
for agent in agents:
    print(agent.reputation.score)  # No additional queries
```

### Pattern 2: Filtering

**Before (JSON)**:
```python
councils = json.load(open('councils.json'))
active_councils = [c for c in councils if c.get('status') == 'active']
```

**After (Postgres)**:
```python
active_councils = session.query(Council).filter(Council.status == 'active').all()
```

### Pattern 3: Counting

**Before (JSON)**:
```python
councils = json.load(open('councils.json'))
count = len([c for c in councils if c.get('status') == 'active'])
```

**After (Postgres)**:
```python
count = session.query(Council).filter(Council.status == 'active').count()
```

### Pattern 4: Pagination

**Before (JSON)**:
```python
page = int(request.args.get('page', 1))
per_page = int(request.args.get('per_page', 10))
councils = json.load(open('councils.json'))
start = (page - 1) * per_page
end = start + per_page
return jsonify(councils[start:end])
```

**After (Postgres)**:
```python
page = int(request.args.get('page', 1))
per_page = int(request.args.get('per_page', 10))
councils = session.query(Council).offset((page - 1) * per_page).limit(per_page).all()
return jsonify([c.to_dict() for c in councils])
```

## 🎯 Complete Example: AgentExtended Endpoint

This is the full implementation for `/api/agents/<agent_id>` matching the TypeScript `AgentExtended` interface:

```python
from models import Agent, AgentReputation, AgentTraining, Council, CouncilMember
from database import get_session
from sqlalchemy.orm import joinedload

@app.route('/api/agents/<agent_id>')
def get_agent_extended(agent_id):
    """Return AgentExtended format matching TypeScript interface"""
    session = get_session()
    
    # Eager load reputation and training
    agent = session.query(Agent).options(
        joinedload(Agent.reputation),
        joinedload(Agent.training)
    ).filter(Agent.id == agent_id).first()
    
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    # Get councils this agent is a member of
    councils = session.query(Council).join(
        CouncilMember, Council.id == CouncilMember.council_id
    ).filter(CouncilMember.agent_id == agent_id).all()
    
    # Serialize councils as full objects
    councils_data = [{
        'id': c.id,
        'name': c.name,
        'domain': c.domain,
        'status': c.status
    } for c in councils]
    
    # Build AgentExtended response
    response = {
        # Core agent fields
        'id': agent.id,
        'name': agent.name,
        'role': agent.role,
        'personality': agent.personality,
        'mode': agent.mode,
        'avatar_icon': agent.avatar_icon,
        'avatar_color': agent.avatar_color,
        'created_at': agent.created_at.isoformat() + 'Z',
        
        # Extended computed fields
        'domain': councils_data[0]['domain'] if councils_data else None,
        'engines': agent.primary_engines if hasattr(agent, 'primary_engines') else [],
        'status': 'active' if agent.reputation and agent.reputation.score > 0 else 'inactive',
        'last_active': agent.created_at.isoformat() + 'Z',  # Or from workflow history
        
        # Nested relationships
        'reputation': {
            'score': agent.reputation.score,
            'total_savings': agent.reputation.total_savings,
            'workflows_executed': agent.reputation.workflows_executed,
            'approval_rate': agent.reputation.approval_rate,
            'updated_at': agent.reputation.updated_at.isoformat() + 'Z'
        } if agent.reputation else None,
        
        'training': {
            'strengths': agent.training.strengths,
            'weaknesses': agent.training.weaknesses,
            'restricted_workflow_types': agent.training.restricted_workflow_types,
            'last_feedback': agent.training.last_feedback,
            'updated_at': agent.training.updated_at.isoformat() + 'Z'
        } if agent.training else None,
        
        # Full council objects
        'councils': councils_data
    }
    
    return jsonify(response)
```

## 🔥 Migration Checklist

- [ ] Install SQLAlchemy: `pip install sqlalchemy psycopg2-binary`
- [ ] Create `database.py` with session manager
- [ ] Add `to_dict()` methods to all models
- [ ] Update `/api/councils` endpoint
- [ ] Update `/api/councils/<id>` endpoint
- [ ] Update `/api/agents` endpoint
- [ ] Update `/api/agents/<id>` endpoint
- [ ] Update `/api/workflows` endpoint
- [ ] Add eager loading with `joinedload()` for relationships
- [ ] Replace all `json.load()` calls with `session.query()`
- [ ] Test all endpoints with Postgres data
- [ ] Remove JSON file loading code
- [ ] Move JSON files to `backups/` directory

---

**🔥 The Queries Burn Sovereign and Eternal! 👑**

