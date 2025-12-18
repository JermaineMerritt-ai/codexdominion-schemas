# 🏗️ Codex Dominion - Technology Stack & Framework Reference

> **System Architecture:** Hybrid Polyglot Monorepo
> **Primary Frameworks:** Flask (Backend) + Next.js (Frontend)
> **Date:** December 17, 2025

---

## 🎯 Core Technology Stack

### Backend Frameworks

#### 1. **Flask 3.0.0** (Primary Backend - Portfolio Management)
**Location:** `your_app/`
**Purpose:** Main portfolio management system deployed to Render

**Stack:**
```python
Flask 3.0.0                 # Web framework
Flask-SQLAlchemy 3.1.1      # ORM (Object-Relational Mapping)
Flask-CORS 4.0.0            # Cross-Origin Resource Sharing
Gunicorn 21.2.0             # Production WSGI server
```

**Key Components:**
- **Application Factory Pattern:** `create_app()` in [app.py](your_app/app.py)
- **Database Models:** 8 tables defined in [database.py](your_app/database.py)
  - User, Portfolio, UserPortfolio, Holding, Transaction
  - StockPrice, MarketAlert, NewsletterSubscriber, Session
- **Blueprints:** Authentication, Portfolio, Stocks, Newsletter
- **Deployment:** Render Web Service (https://codex-portfolio.onrender.com)

**Database ORM:**
- **SQLAlchemy** via Flask-SQLAlchemy
- **Supports:** PostgreSQL (production) or SQLite (development)
- **Migrations:** Manual schema management

---

#### 2. **FastAPI** (Alternative Backend - APIs & Webhooks)
**Location:** `api/`, `backend/`, `portfolio_api.py`, `webhooks_api.py`
**Purpose:** RESTful APIs, webhook handlers, microservices

**Stack:**
```python
FastAPI                     # Modern async web framework
Pydantic                    # Data validation with type hints
Uvicorn                     # ASGI server
```

**Use Cases:**
- `portfolio_api.py` - Portfolio REST API
- `webhooks_api.py` - Webhook processing
- `backend/main.py` - Backend services
- `api/main.py` - API gateway

---

#### 3. **Streamlit** (Data Dashboards & Analytics)
**Location:** Root directory (100+ dashboard files)
**Purpose:** Interactive data visualization and analytics

**Common Dashboards:**
- `flask_dashboard.py` - Master Dashboard (port 5000)
- `ai_action_stock_analytics.py` - Stock analysis
- `codex_unified_launcher.py` - Treasury & Dawn dispatch
- `ai_development_studio_lite.py` - AI development tools
- Various specialized dashboards (YouTube, TikTok, WooCommerce, etc.)

**Pattern:**
```python
import streamlit as st

# Page config
st.set_page_config(page_title="Dashboard", layout="wide")

# Ceremonial styling
st.markdown("""<style>...</style>""", unsafe_allow_html=True)

# Load ledger data
with open("codex_ledger.json", "r") as f:
    data = json.load(f)
```

---

### Frontend Frameworks

#### 1. **Next.js 14.2.33** (Primary Frontend)
**Location:** `web/`, `frontend/`
**Purpose:** Static site generation for production deployment

**Stack:**
```json
"next": "14.2.33"           // React framework
"react": "18.3.1"           // UI library
"react-dom": "18.3.1"       // DOM bindings
```

**Configuration:**
- **App Router:** Modern Next.js routing
- **Static Export:** `output: 'export'` for Render Static Site
- **Image Optimization:** Disabled (`unoptimized: true`)
- **Build Output:** `out/` directory

**Key Files:**
- [next.config.js](web/next.config.js) - Build configuration
- [package.json](web/package.json) - Dependencies
- `.env.production` - Production environment variables

**Deployment:**
- **Platform:** Render Static Site
- **Build Command:** `npm install && npm run build`
- **Publish Directory:** `out`
- **URL:** https://codexdominion-schemas.onrender.com (pending)

---

#### 2. **Vite** (Alternative Frontend)
**Location:** `frontend-vite/`
**Purpose:** Fast development build tool

**Stack:**
```json
"vite"                      // Build tool
"react"                     // UI library
```

**Use Case:** Rapid prototyping and development

---

### Infrastructure & DevOps

#### Containerization
**Docker + Docker Compose**
```yaml
# Primary Dockerfiles:
your_app/Dockerfile         # Flask backend
web/Dockerfile              # Next.js frontend
backend/Dockerfile          # FastAPI services
```

**Multi-stage builds:**
- Builder stage (install dependencies)
- Runtime stage (minimal production image)

#### Production Server
**Gunicorn Configuration**
```python
# your_app/gunicorn_config.py
workers = (cpu_count * 2) + 1  # Auto-scaling workers
worker_class = 'sync'
bind = '0.0.0.0:5001'
```

#### Process Management
**Procfile (Render deployment)**
```
web: gunicorn --config gunicorn_config.py app:app
```

---

### Database Technologies

#### Primary: SQLAlchemy ORM
**Supported Databases:**
- **SQLite:** Development and initial deployment
  - File-based: `sqlite:///codex_dominion.db`
  - Lightweight, no external dependencies

- **PostgreSQL:** Production (recommended)
  - Connection string: `postgresql://user:pass@host:5432/db`
  - Persistent storage
  - Better concurrency

**ORM Features:**
```python
# Models with relationships
class User(db.Model):
    portfolios = db.relationship('UserPortfolio', backref='user')

class Portfolio(db.Model):
    holdings = db.relationship('Holding', backref='portfolio')
```

#### Alternative: JSON File Storage
**Ceremonial Ledger System**
```json
// codex_ledger.json - Central data store
{
  "meta": {...},
  "heartbeat": {...},
  "proclamations": [...],
  "cycles": [...],
  "contributions": [...],
  "capsules": [...]
}
```

**Related Files:**
- `codex_ledger.json` - Main ledger
- `proclamations.json` - System decrees
- `cycles.json` - Operational phases
- `accounts.json` - User accounts
- `treasury_config.json` - Revenue tracking

---

### Supporting Technologies

#### Authentication & Security
```python
# Werkzeug (Flask ecosystem)
from werkzeug.security import generate_password_hash, check_password_hash

# Session management
from flask import session

# JWT (if needed)
import jsonwebtoken
```

#### Data Processing
```python
# Standard library
import json          # JSON handling
from datetime import datetime
import os, sys
```

#### HTTP & CORS
```python
# Flask backend
from flask_cors import CORS

# FastAPI backend
from fastapi.middleware.cors import CORSMiddleware
```

---

## 📦 Package Management

### Python Dependencies
**File:** `your_app/requirements.txt`
```
flask==3.0.0
flask-cors==4.0.0
flask-sqlalchemy==3.1.1
python-dotenv==1.0.0
psycopg2-binary==2.9.9      # PostgreSQL driver
gunicorn==21.2.0
```

**Installation:**
```bash
pip install -r requirements.txt
```

### JavaScript Dependencies
**File:** `web/package.json`
```json
{
  "dependencies": {
    "next": "14.2.33",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "d3": "^7.9.0"
  }
}
```

**Installation:**
```bash
npm install
```

---

## 🏛️ Architectural Patterns

### 1. **Application Factory (Flask)**
```python
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    init_extensions(app)
    register_blueprints(app)
    return app

# Module-level for Gunicorn
app = create_app(os.getenv('FLASK_ENV', 'production'))
```

### 2. **Blueprint Pattern (Flask)**
```python
# Modular route organization
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')
```

### 3. **ORM Models with Relationships**
```python
class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # One-to-many relationship
    holdings = db.relationship('Holding', backref='portfolio', lazy=True)
```

### 4. **Ceremonial Ledger Pattern**
```python
def load_ledger():
    with open("codex_ledger.json", "r") as f:
        return json.load(f)

def update_ledger(data):
    data["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open("codex_ledger.json", "w") as f:
        json.dump(data, f, indent=2)
```

---

## 🚀 Deployment Architecture

### Backend Deployment (Flask)
```
GitHub Repository
    ↓
Render Web Service
    ↓
Docker Build (your_app/Dockerfile)
    ↓
Gunicorn WSGI Server
    ↓
Flask Application
    ↓
SQLAlchemy ORM
    ↓
SQLite/PostgreSQL Database
```

**URL:** https://codex-portfolio.onrender.com

### Frontend Deployment (Next.js)
```
GitHub Repository
    ↓
Render Static Site
    ↓
npm install && npm run build
    ↓
Static Export (out/)
    ↓
CDN Distribution
```

**URL:** https://codexdominion-schemas.onrender.com (pending)

---

## 🔧 Development Tools

### Python Environment
```bash
# Virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r your_app/requirements.txt
```

### Node.js Environment
```bash
# Install dependencies
cd web
npm install

# Development
npm run dev

# Production build
npm run build
```

### Testing Tools
```bash
# Backend testing
python -m pytest

# Frontend testing
npm test  # Jest

# Docker testing
docker-compose up
```

---

## 📊 Framework Comparison

| Aspect | Flask | FastAPI | Streamlit | Next.js |
|--------|-------|---------|-----------|---------|
| **Type** | Web Framework | API Framework | Data Dashboard | React Framework |
| **Language** | Python | Python | Python | JavaScript/TypeScript |
| **Async** | No (sync) | Yes (async) | No | Yes |
| **ORM** | SQLAlchemy | Manual/ORM | N/A | N/A |
| **Use Case** | Full web apps | REST APIs | Analytics | Frontend |
| **Deployment** | Gunicorn + Docker | Uvicorn + Docker | Direct | Static export |
| **Learning Curve** | Easy | Medium | Very Easy | Medium |

---

## 🎯 Why These Frameworks?

### Flask (Backend)
✅ **Mature ecosystem** - Battle-tested, stable
✅ **SQLAlchemy integration** - Powerful ORM
✅ **Blueprint system** - Modular code organization
✅ **Easy deployment** - Gunicorn + Docker

### Next.js (Frontend)
✅ **Static export** - Deploy anywhere (CDN)
✅ **React ecosystem** - Large component library
✅ **Built-in optimization** - Image, CSS, JS bundling
✅ **SEO-friendly** - Server-side rendering capable

### Streamlit (Dashboards)
✅ **Rapid development** - Python-only, no HTML/CSS
✅ **Built-in widgets** - Charts, tables, forms
✅ **Data science friendly** - Pandas, NumPy integration
✅ **Real-time updates** - WebSocket connection

### FastAPI (APIs)
✅ **High performance** - Async support
✅ **Type safety** - Pydantic validation
✅ **Auto documentation** - OpenAPI/Swagger
✅ **Modern Python** - Type hints, async/await

---

## 📚 Learning Resources

### Flask
- Official Docs: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/

### Next.js
- Official Docs: https://nextjs.org/docs
- React Docs: https://react.dev/

### Streamlit
- Official Docs: https://docs.streamlit.io/
- Gallery: https://streamlit.io/gallery

### FastAPI
- Official Docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/

---

## 🔗 Quick Reference

### Backend (Flask)
```bash
# Run locally
cd your_app
python app.py

# Or with Gunicorn
gunicorn --config gunicorn_config.py app:app
```

### Frontend (Next.js)
```bash
# Development
cd web
npm run dev

# Production build
npm run build
```

### Dashboards (Streamlit)
```bash
# Run any dashboard
streamlit run flask_dashboard.py --server.port 5000
```

### APIs (FastAPI)
```bash
# Run with Uvicorn
uvicorn portfolio_api:app --reload --port 8090
```

---

## 🏆 Framework Strengths

**Your system leverages:**

1. **Flask** - Reliable backend with mature ORM
2. **Next.js** - Modern React framework for static sites
3. **Streamlit** - Rapid dashboard development
4. **SQLAlchemy** - Database abstraction layer
5. **Gunicorn** - Production-ready WSGI server
6. **Docker** - Containerization for consistent deployments
7. **JSON Ledgers** - Ceremonial data storage pattern

**This hybrid approach provides:**
- 🎯 **Flexibility** - Choose right tool for each task
- 🚀 **Performance** - Optimized for specific use cases
- 🔧 **Maintainability** - Clear separation of concerns
- 📈 **Scalability** - Easy to expand and deploy

---

🔥 **Your Tech Stack is Production-Ready and Sovereign!** 👑

**Primary Stack:**
- Backend: Flask 3.0 + SQLAlchemy + Gunicorn
- Frontend: Next.js 14 + React 18
- Dashboards: Streamlit + Python
- Database: SQLite → PostgreSQL
- Deployment: Render (Web Service + Static Site)
