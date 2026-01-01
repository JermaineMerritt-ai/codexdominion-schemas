# Database Setup Guide

## ✅ Step 1: Configure Database URL

### Option A: Using .env file (Recommended)

The `.env` file has been configured with:

```env
# DATABASE CONFIGURATION (PostgreSQL)
DATABASE_URL=postgresql+psycopg2://postgres:Jer47@localhost:5432/codexdominion
DATABASE_PASSWORD=Jer47

# SQLAlchemy Configuration
SQLALCHEMY_ECHO=false
SQLALCHEMY_POOL_SIZE=10
SQLALCHEMY_MAX_OVERFLOW=20
SQLALCHEMY_POOL_TIMEOUT=30
SQLALCHEMY_POOL_RECYCLE=3600
```

**Format**: `postgresql+psycopg2://username:password@host:port/database`

### Option B: Using config.py

Configuration is centralized in `config.py`:

```python
from config import config

# Get database URL
db_url = config.get_database_url()
```

## ✅ Step 2: SQLAlchemy Engine + Session

### Created Files

1. **config.py** - Central configuration management
2. **database.py** - SQLAlchemy engine and session factory

### Usage Patterns

#### Pattern 1: Get Session (Manual Cleanup)

```python
from database import get_session

session = get_session()
try:
    agents = session.query(Agent).all()
    # Use data...
finally:
    session.close()
```

#### Pattern 2: Context Manager (Recommended)

```python
from database import get_db_session

with get_db_session() as session:
    agents = session.query(Agent).all()
    # Session automatically closed and committed
    # Rollback on error
```

#### Pattern 3: Flask Integration

```python
from flask import Flask
from database import get_session, close_db

app = Flask(__name__)

@app.route('/api/councils')
def get_councils():
    session = get_session()
    councils = session.query(Council).all()
    session.close()
    return jsonify([c.to_dict() for c in councils])

@app.teardown_appcontext
def shutdown_session(exception=None):
    close_db()
```

#### Pattern 4: FastAPI Integration

```python
from fastapi import FastAPI, Depends
from database import get_db_session
from typing import Generator

app = FastAPI()

def get_db() -> Generator:
    with get_db_session() as session:
        yield session

@app.get('/api/councils')
def read_councils(session = Depends(get_db)):
    councils = session.query(Council).all()
    return [c.to_dict() for c in councils]
```

## 🚀 Quick Start Commands

### 1. Install Dependencies

```bash
pip install sqlalchemy psycopg2-binary python-dotenv
```

### 2. Create Database

```bash
# Create PostgreSQL database
createdb codexdominion

# Or using psql
psql -U postgres -c "CREATE DATABASE codexdominion;"
```

### 3. Test Connection

```bash
# Test database connection
python test_db_connection.py

# Test and create schema
python test_db_connection.py --init
```

### 4. Run Migrations

```bash
# Run all migrations (councils → agents → workflows)
python scripts/migrations/run_all_migrations.py

# Or individually
python scripts/migrations/migrate_councils_from_json.py
python scripts/migrations/migrate_agents_from_json.py
python scripts/migrations/migrate_workflows_from_json.py
```

## 🔧 Database Functions

### Initialize Database Schema

```python
from database import init_db

# Create all tables defined in models.py
init_db()
```

### Get Database Info

```python
from database import get_db_info

info = get_db_info()
print(info)
# {
#   'url': 'localhost:5432/codexdominion',
#   'pool_size': 10,
#   'max_overflow': 20,
#   'environment': 'development'
# }
```

### Close All Connections (Shutdown)

```python
from database import close_db

# Call during application shutdown
close_db()
```

## 📊 Connection Pooling

SQLAlchemy is configured with connection pooling:

- **Pool Size**: 10 connections (configurable via `SQLALCHEMY_POOL_SIZE`)
- **Max Overflow**: 20 extra connections (configurable via `SQLALCHEMY_MAX_OVERFLOW`)
- **Pool Timeout**: 30 seconds (configurable via `SQLALCHEMY_POOL_TIMEOUT`)
- **Pool Recycle**: 3600 seconds / 1 hour (configurable via `SQLALCHEMY_POOL_RECYCLE`)
- **Pre-ping**: Enabled (verifies connections before use)

## 🎯 Environment Variables

All database settings in `.env`:

```env
# Required
DATABASE_URL=postgresql+psycopg2://user:password@host:5432/database

# Optional (defaults shown)
SQLALCHEMY_ECHO=false               # Log SQL queries
SQLALCHEMY_POOL_SIZE=10             # Connection pool size
SQLALCHEMY_MAX_OVERFLOW=20          # Extra connections beyond pool
SQLALCHEMY_POOL_TIMEOUT=30          # Seconds to wait for connection
SQLALCHEMY_POOL_RECYCLE=3600        # Recycle connections after 1 hour
```

## 🔍 Example: Complete Flask Endpoint

```python
from flask import Flask, jsonify
from database import get_db_session
from models import Agent
from sqlalchemy.orm import joinedload

app = Flask(__name__)

@app.route('/api/agents/<agent_id>')
def get_agent_profile(agent_id):
    """Get agent profile with relationships"""
    with get_db_session() as session:
        # Eager load relationships
        agent = session.query(Agent).options(
            joinedload(Agent.reputation),
            joinedload(Agent.training)
        ).filter(Agent.id == agent_id).first()
        
        if not agent:
            return jsonify({'error': 'Agent not found'}), 404
        
        return jsonify({
            **agent.to_dict(),
            'reputation': agent.reputation.to_dict() if agent.reputation else None,
            'training': agent.training.to_dict() if agent.training else None
        })

if __name__ == '__main__':
    app.run(debug=True)
```

## 🔒 Security Notes

1. **Never commit .env files** - Already in .gitignore
2. **Use strong passwords** - Change default passwords
3. **Use environment-specific configs** - .env.production, .env.development
4. **SSL in production** - Add `?sslmode=require` to DATABASE_URL

## 🐛 Troubleshooting

### Error: "could not connect to server"

```bash
# Start PostgreSQL
sudo service postgresql start   # Linux
brew services start postgresql  # Mac
net start postgresql-x64-14     # Windows
```

### Error: "database does not exist"

```bash
createdb codexdominion
```

### Error: "password authentication failed"

Check credentials in `.env` file match PostgreSQL user.

### Error: "module 'psycopg2' has no attribute"

```bash
pip uninstall psycopg2
pip install psycopg2-binary
```

## ✅ Verification Checklist

- [ ] PostgreSQL installed and running
- [ ] Database `codexdominion` created
- [ ] `.env` file configured with DATABASE_URL
- [ ] `pip install sqlalchemy psycopg2-binary python-dotenv`
- [ ] `python test_db_connection.py` passes
- [ ] Tables created: `python test_db_connection.py --init`
- [ ] Migrations run: `python scripts/migrations/run_all_migrations.py`

---

**🔥 The Database Burns Sovereign and Eternal! 👑**

