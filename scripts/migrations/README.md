# JSON → Postgres Migration Guide

## 📋 Overview

This directory contains one-time migration scripts to move data from JSON files to the Postgres database.

## 🎯 Migration Order

1. **councils.json** → `councils` table
2. **agents.json** → `agents` + `agent_reputation` + `agent_training` tables
3. **workflows.json** → `workflows` + `workflow_metrics` + `workflow_votes` tables

## 🚀 Quick Start

### Prerequisites

1. **Postgres installed and running**
2. **Database created**: `createdb codexdominion`
3. **Schema initialized**: Run `001_init.sql` migration
4. **Python environment**: SQLAlchemy installed

### Step 1: Setup Database

```bash
# Create database
createdb codexdominion

# Run schema migration
psql -U postgres -d codexdominion -f 001_init.sql

# Verify tables created
psql -U postgres -d codexdominion -c "\dt"
# Should show: agents, agent_reputation, agent_training, councils, council_members, workflow_types, workflows, workflow_votes, workflow_metrics
```

### Step 2: Configure Database URL

Update `DATABASE_URL` in each migration script:

```python
DATABASE_URL = "postgresql://postgres:password@localhost:5432/codexdominion"
```

**Or** set environment variable:

```bash
export DATABASE_URL="postgresql://postgres:password@localhost:5432/codexdominion"
```

### Step 3: Run Migrations

**Option 1: Run all migrations (recommended)**

```bash
# From project root
python scripts/migrations/run_all_migrations.py
```

**Option 2: Run individually**

```bash
# Councils first (no dependencies)
python scripts/migrations/migrate_councils_from_json.py

# Agents second (no dependencies)
python scripts/migrations/migrate_agents_from_json.py

# Workflows last (depends on agents and councils)
python scripts/migrations/migrate_workflows_from_json.py
```

### Step 4: Verify Migration

```bash
# Connect to database
psql -U postgres -d codexdominion

# Check record counts
SELECT COUNT(*) FROM councils;      -- Should match councils.json
SELECT COUNT(*) FROM agents;        -- Should match agents.json
SELECT COUNT(*) FROM workflows;     -- Should match workflow state

# Verify relationships
SELECT a.name, ar.score, at.strengths
FROM agents a
LEFT JOIN agent_reputation ar ON a.id = ar.agent_id
LEFT JOIN agent_training at ON a.id = at.agent_id
LIMIT 5;
```

## 📁 Migration Scripts

### migrate_councils_from_json.py

**Input**: `councils.json` (36 councils)
**Output**: Records in `councils` table

**Features**:
- ✅ Handles both array and object JSON structures
- ✅ Upsert logic (insert new, update existing)
- ✅ JSONB fields: `primary_engines`, `oversight`
- ✅ Nullable fields: `purpose`, `domain`, `status`

**Example output**:
```
🔄 Starting council migration from JSON to Postgres...
📋 Found 36 councils in JSON
📊 Database currently has 0 councils
➕ Inserted: Finance Council (finance-council)
➕ Inserted: Operations Council (ops-council)
...
✅ Migration complete!
   Inserted: 36
   Updated:  0
   Skipped:  0
   Total in DB: 36
```

### migrate_agents_from_json.py

**Input**: `agents.json` or `agents_simple.json`
**Output**: Records in `agents`, `agent_reputation`, `agent_training` tables

**Features**:
- ✅ Multi-table transaction (agents + reputation + training in single commit)
- ✅ Handles 1-to-1 relationships
- ✅ JSONB fields: `strengths`, `weaknesses`, `restricted_workflow_types`
- ✅ Fallback to agents_simple.json if agents.json not found

**Example output**:
```
🔄 Starting agent migration from JSON to Postgres...
📋 Found 12 agents in JSON
📊 Database currently has 0 agents
➕ Inserted agent: Finance Analyst (agent-001)
  ➕ Inserted reputation: score=85
  ➕ Inserted training: 5 strengths
...
✅ Migration complete!
   Agents inserted: 12
   Agents updated:  0
   Reputations inserted: 12
   Training records inserted: 12
   Total agents in DB: 12
```

### migrate_workflows_from_json.py

**Input**: `workflows.json` (if persisted)
**Output**: Records in `workflows`, `workflow_metrics`, `workflow_votes` tables

**Features**:
- ✅ Handles workflows with metrics and votes
- ✅ Foreign key relationships: `created_by_agent`, `assigned_council_id`
- ✅ JSONB fields: `inputs`, `calculated_savings`
- ✅ Graceful handling if workflows.json doesn't exist

**Example output**:
```
🔄 Starting workflow migration from JSON to Postgres...
📋 Found 8 workflows in JSON
📊 Database currently has 0 workflows
➕ Inserted workflow: wf-001 (optimize_payroll)
  ➕ Inserted metrics: duration=45s
  ➕ Inserted vote: agent-002 voted approve
...
✅ Migration complete!
   Workflows inserted: 8
   Metrics inserted: 8
   Votes inserted: 12
   Total workflows in DB: 8
```

## 🔧 Troubleshooting

### Error: "JSON file not found"

**Solution**: Ensure JSON files are in project root:
- `councils.json`
- `agents.json` or `agents_simple.json`
- `workflows.json` (optional)

### Error: "relation does not exist"

**Solution**: Run database schema migration first:
```bash
psql -U postgres -d codexdominion -f 001_init.sql
```

### Error: "could not connect to server"

**Solution**: Start Postgres service:
```bash
# Windows
net start postgresql-x64-14

# Linux/Mac
sudo service postgresql start
```

### Error: "foreign key constraint violation"

**Solution**: Ensure migration order is correct:
1. Councils first (no dependencies)
2. Agents second (no dependencies)
3. Workflows last (depends on agents and councils)

## 🎯 Next Steps After Migration

### Step 1: Update Flask Endpoints

**Before (JSON)**:
```python
def get_councils():
    with open('councils.json', 'r') as f:
        councils = json.load(f)
    return jsonify(councils)
```

**After (Postgres)**:
```python
from models import Council

def get_councils():
    councils = session.query(Council).all()
    return jsonify([c.to_dict() for c in councils])
```

### Step 2: Test API Endpoints

```bash
# Test councils endpoint
curl http://localhost:5000/api/councils

# Test agent profile endpoint
curl http://localhost:5000/api/agents/agent-001

# Test workflows endpoint
curl http://localhost:5000/api/workflows
```

### Step 3: Deprecate JSON Files

```bash
# Create backups directory
mkdir backups

# Move JSON files
mv councils.json backups/councils.json.bak
mv agents.json backups/agents.json.bak
mv workflows.json backups/workflows.json.bak

# Add deprecation warning in code
import warnings
warnings.warn("JSON files deprecated. Use Postgres DB.", DeprecationWarning)
```

## 📊 Migration Summary

| JSON File | Tables | Records (Example) |
|-----------|--------|-------------------|
| councils.json | councils | 36 |
| agents.json | agents, agent_reputation, agent_training | 12 + 12 + 12 |
| workflows.json | workflows, workflow_metrics, workflow_votes | 8 + 8 + 12 |

**Total Tables**: 9
**Total Records**: ~100 (varies by environment)

## 🔥 Success Criteria

- ✅ All migrations run without errors
- ✅ Record counts match JSON files
- ✅ Foreign key relationships intact
- ✅ JSONB fields properly structured
- ✅ Flask endpoints read from Postgres
- ✅ Frontend displays Postgres data
- ✅ JSON files moved to backups/

---

**🔥 The Data Burns Sovereign and Eternal! 👑**

