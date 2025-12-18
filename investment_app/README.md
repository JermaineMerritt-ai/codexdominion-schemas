# Investment Platform Flask Application

Flask application structure for Codex Dominion investment platform.

## Structure

```
investment_app/
├── app.py              # Main application factory
├── config.py           # Configuration classes
├── extensions.py       # Flask extensions (SQLAlchemy, Login)
├── models.py           # Database models
├── ai_prompts.py       # AI prompt manager
├── portfolio/          # Portfolio management blueprint
│   ├── __init__.py
│   └── routes.py
├── stocks/             # Stock data blueprint
│   ├── __init__.py
│   └── routes.py
├── newsletter/         # Newsletter/email blueprint
│   ├── __init__.py
│   └── routes.py
├── auth/               # Authentication blueprint
│   ├── __init__.py
│   └── routes.py
├── templates/          # HTML templates (TODO)
├── static/             # CSS, JS, images (TODO)
└── tasks/              # Background tasks
    └── __init__.py
```

## Setup

1. Install dependencies:
```bash
cd investment_app
pip install -r requirements.txt

# For AI features (choose one):
pip install openai  # For OpenAI GPT models
pip install anthropic  # For Anthropic Claude models
```

2. Set environment variables:

**Windows PowerShell:**
```powershell
.\setup-env.ps1  # Edit this file first with your API keys
```

**Linux/Mac:**
```bash
source setup-env.sh  # Edit this file first with your API keys
```

**Or create .env file:**
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

**Minimum required:**
```bash
# Windows PowerShell
$env:OPENAI_API_KEY = "sk-proj-YOUR-KEY-HERE"
$env:AI_PROVIDER = "openai"
$env:AI_MODEL = "gpt-4o-mini"
$env:DATABASE_URL = "postgresql://pgadmin:Jer47@localhost:5432/codex"

# Linux/Mac
export OPENAI_API_KEY="sk-proj-YOUR-KEY-HERE"
export AI_PROVIDER="openai"
export AI_MODEL="gpt-4o-mini"
export DATABASE_URL="postgresql://pgadmin:Jer47@localhost:5432/codex"
```

3. Get API Keys:
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic** (optional): https://console.anthropic.com/
- **Polygon.io** (optional): https://polygon.io/
- **Alpha Vantage** (optional): https://www.alphavantage.co/

4. Initialize database:
```bash
# From parent directory
python apply_users_schema.py

# Or using Flask-Migrate
flask db init
flask db migrate -m "Initial schema"
flask db upgrade
```

5. Run application:
```bash
python app.py
```

6. Check health endpoint:
```
http://localhost:5000/health
```

Should return:
```json
{
  "status": "operational",
  "database": "connected",
  "ai_prompts": 8,
  "ai_service": {
    "configured": true,
    "provider": "openai",
    "model": "gpt-4o-mini"
  }
}
```

## Features

### Implemented
- ✅ Application factory pattern
- ✅ Blueprint structure (portfolio, stocks, newsletter, auth)
- ✅ Database models (10 tables)
- ✅ AI prompt manager (8 prompts)
- ✅ Configuration classes (dev/prod/test)
- ✅ Authentication routes
- ✅ Portfolio routes with AI analysis
- ✅ Stock routes with AI analysis
- ✅ Newsletter subscription
- ✅ Background task structure

### TODO
- ⏳ HTML templates
- ⏳ Static assets (CSS, JS)
- ⏳ AI model integration (OpenAI API)
- ⏳ Email sending (SMTP/SendGrid)
- ⏳ Task scheduling (APScheduler/Celery)
- ⏳ Admin dashboard
- ⏳ Testing suite

## Routes

### Authentication
- `GET/POST /auth/login` - User login
- `GET/POST /auth/register` - User registration
- `GET /auth/logout` - User logout

### Portfolio
- `GET /portfolio/` - Portfolio dashboard
- `GET /portfolio/<id>` - View portfolio
- `GET /portfolio/<id>/analyze` - AI portfolio analysis
- `GET /portfolio/<id>/trades` - Trade history

### Stocks
- `GET /stocks/` - Stock screener
- `GET /stocks/<ticker>` - Stock detail
- `GET /stocks/<ticker>/analyze` - AI stock analysis
- `GET /stocks/alerts` - Recent market alerts

### Newsletter
- `GET/POST /newsletter/subscribe` - Newsletter subscription
- `GET /newsletter/unsubscribe/<email>` - Unsubscribe
- `GET /newsletter/preview/<type>` - Preview templates
- `GET /newsletter/generate/<type>` - Generate newsletter (admin)

## AI Integration

AI prompts are loaded from parent directory:
- `ai_stock_analyst_prompt.txt`
- `ai_portfolio_analyst_prompt.txt`
- `ai_day_trade_ideas_prompt.txt`
- `ai_daily_email_prompt.txt`
- `ai_weekly_portfolio_email_prompt.txt`
- `ai_monthly_deep_dive_prompt.txt`
- `ai_risk_profile_translator_prompt.txt`
- `ai_concept_explainer_prompt.txt`

Usage:
```python
import ai_prompts

# Load a prompt
prompt = ai_prompts.load_prompt('stock_analyst')

# Get all prompts
all_prompts = ai_prompts.get_all_prompts()
```

## Database

PostgreSQL with 10 tables:
- users (authentication + risk profiles)
- portfolios (user portfolios)
- holdings (portfolio positions)
- trades (transaction history)
- stocks (market data)
- fundamentals (financial data)
- alerts (market signals)
- subscribers (email list)
- advisor_clients (advisor relationships)

Run schema: `python apply_users_schema.py` (from parent directory)

## Compliance

All AI-generated content follows compliance guidelines in `AI_COMPLIANCE_GUIDELINES.md`:
- No financial advice
- No price targets
- No buy/sell directives
- Educational focus only
- Risk awareness
- Multiple perspectives

---

**Status:** Core structure complete, templates and AI integration pending
**Last Updated:** December 16, 2025
