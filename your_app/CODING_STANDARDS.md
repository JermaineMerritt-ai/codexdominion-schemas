# 📋 Codex Dominion Coding Standards

## 1. Code Style (PEP8)

### Follow PEP8 Guidelines
```python
# Good ✅
def calculate_portfolio_value(holdings: list[Holding]) -> float:
    """Calculate total portfolio value from holdings."""
    total = 0.0
    for holding in holdings:
        total += holding.shares * holding.avg_price
    return total

# Bad ❌
def calcPortVal(h):
    t=0
    for x in h:
        t+=x.shares*x.avg_price
    return t
```

### Naming Conventions
- **Classes:** `PascalCase` (e.g., `Portfolio`, `StockPrice`)
- **Functions/Methods:** `snake_case` (e.g., `get_user_portfolios`, `calculate_returns`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`, `DEFAULT_RISK_PROFILE`)
- **Private methods:** `_leading_underscore` (e.g., `_validate_ticker`)

### Line Length
- Maximum 88 characters (Black formatter default)
- Use parentheses for line continuation

```python
# Good ✅
result = service.get_stock_analysis(
    ticker="AAPL",
    start_date=start,
    end_date=end,
    include_technical=True
)

# Bad ❌
result = service.get_stock_analysis(ticker="AAPL", start_date=start, end_date=end, include_technical=True)
```

---

## 2. SQLAlchemy ORM

### Always Use ORM, Never Raw SQL
```python
# Good ✅
portfolio = Portfolio.query.filter_by(user_id=user_id).first()
holdings = Holding.query.filter_by(portfolio_id=portfolio.id).all()

# Bad ❌
cursor.execute("SELECT * FROM portfolios WHERE user_id = ?", (user_id,))
```

### Define Relationships Properly
```python
class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationships
    user = db.relationship('User', backref='portfolios')
    holdings = db.relationship('Holding', backref='portfolio', cascade='all, delete-orphan')
```

### Use Query Methods
```python
# Filtering
portfolios = Portfolio.query.filter_by(user_id=user_id).all()

# Joins
results = db.session.query(Portfolio, Holding).join(Holding).filter(
    Portfolio.user_id == user_id
).all()

# Ordering
holdings = Holding.query.order_by(Holding.ticker.asc()).all()

# Aggregations
total_value = db.session.query(
    func.sum(Holding.shares * Holding.avg_price)
).filter_by(portfolio_id=portfolio_id).scalar()
```

### Always Commit Transactions
```python
# Good ✅
try:
    portfolio = Portfolio(user_id=user_id, name=name)
    db.session.add(portfolio)
    db.session.commit()
except Exception as e:
    db.session.rollback()
    raise

# Bad ❌
portfolio = Portfolio(user_id=user_id, name=name)
db.session.add(portfolio)
# Missing commit!
```

---

## 3. Flask Blueprints (Modularity)

### Blueprint Structure
```
your_app/
├── auth/
│   ├── __init__.py
│   ├── routes.py
│   └── forms.py
├── portfolio/
│   ├── __init__.py
│   ├── routes.py
│   └── services.py
├── stocks/
│   ├── __init__.py
│   ├── routes.py
│   └── services.py
└── newsletter/
    ├── __init__.py
    └── routes.py
```

### Blueprint Registration
```python
# auth/__init__.py
from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

from . import routes

# app.py
from auth import auth_bp
from portfolio import portfolio_bp
from stocks import stocks_bp

app.register_blueprint(auth_bp)
app.register_blueprint(portfolio_bp)
app.register_blueprint(stocks_bp)
```

### Blueprint Routes
```python
# portfolio/routes.py
from . import portfolio_bp
from .services import PortfolioService

@portfolio_bp.route('/dashboard')
def dashboard():
    portfolios = PortfolioService.get_user_portfolios(current_user.id)
    return render_template('portfolio/dashboard.html', portfolios=portfolios)

@portfolio_bp.route('/create', methods=['POST'])
def create_portfolio():
    data = request.get_json()
    portfolio = PortfolioService.create_portfolio(current_user.id, data)
    return jsonify(portfolio.to_dict()), 201
```

---

## 4. Environment Variables for Secrets

### Never Hardcode Secrets
```python
# Good ✅
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

# Bad ❌
OPENAI_API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgresql://user:pass@localhost/db"
```

### .env File Structure
```bash
# .env
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
DATABASE_URL=sqlite:///codex_dominion.db

# API Keys
OPENAI_API_KEY=sk-...
ALPHA_VANTAGE_KEY=...

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
```

### .env.example Template
```bash
# Create this for documentation
# .env.example (committed to git)
FLASK_ENV=development
SECRET_KEY=change-this-in-production
DATABASE_URL=sqlite:///codex_dominion.db
OPENAI_API_KEY=your-openai-key
```

---

## 5. Cache AI Responses

### Use Redis or In-Memory Cache
```python
from functools import lru_cache
import redis
import json

# In-memory cache (simple)
@lru_cache(maxsize=100)
def get_stock_analysis_cached(ticker: str, date: str):
    return StockService.get_analysis(ticker, date)

# Redis cache (production)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_ai_response(prompt: str):
    # Check cache first
    cache_key = f"ai_response:{hash(prompt)}"
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    # Generate new response
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    # Cache for 1 hour
    redis_client.setex(cache_key, 3600, json.dumps(response))
    return response
```

### Cache Strategy
- **Stock Prices:** Cache for 1 minute during market hours, 1 hour after close
- **AI Analysis:** Cache for 24 hours
- **User Portfolios:** Cache for 5 minutes
- **Market Data:** Cache for 15 minutes

---

## 6. Keep Prompts in `prompts/`

### Directory Structure
```
your_app/
├── prompts/
│   ├── stock_analysis.txt
│   ├── risk_assessment.txt
│   ├── portfolio_summary.txt
│   └── market_alert.txt
```

### Load Prompts Dynamically
```python
# prompts/loader.py
import os

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), 'prompts')

def load_prompt(name: str) -> str:
    """Load prompt template from file."""
    path = os.path.join(PROMPTS_DIR, f"{name}.txt")
    with open(path, 'r') as f:
        return f.read()

# Usage
stock_analysis_prompt = load_prompt('stock_analysis')
prompt = stock_analysis_prompt.format(
    ticker=ticker,
    current_price=price,
    volume=volume
)
```

### Prompt Template Example
```
# prompts/stock_analysis.txt
You are a professional stock analyst. Analyze {ticker}.

Current Price: ${current_price}
Volume: {volume}
Risk Profile: {risk_profile}

Provide:
1. Buy/Sell/Hold recommendation
2. Target price (12-month)
3. Key risks (3-5 points)
4. Growth catalysts (3-5 points)

Format as JSON.
```

---

## 7. Keep Business Logic in `services/`

### Service Layer Pattern
```
your_app/
├── services/
│   ├── __init__.py
│   ├── portfolio_service.py
│   ├── stock_service.py
│   ├── ai_service.py
│   └── newsletter_service.py
```

### Service Implementation
```python
# services/portfolio_service.py
from database import db, Portfolio, Holding, Transaction
from typing import List, Optional

class PortfolioService:
    """Business logic for portfolio operations."""

    @staticmethod
    def get_user_portfolios(user_id: int) -> List[Portfolio]:
        """Get all portfolios for a user."""
        return Portfolio.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create_portfolio(user_id: int, data: dict) -> Portfolio:
        """Create new portfolio with validation."""
        portfolio = Portfolio(
            user_id=user_id,
            name=data['name'],
            risk_profile=data['risk_profile']
        )
        db.session.add(portfolio)
        db.session.commit()
        return portfolio

    @staticmethod
    def calculate_portfolio_value(portfolio_id: int) -> float:
        """Calculate total portfolio value."""
        holdings = Holding.query.filter_by(portfolio_id=portfolio_id).all()
        return sum(h.shares * h.avg_price for h in holdings)

    @staticmethod
    def execute_trade(portfolio_id: int, ticker: str, trade_type: str,
                     shares: float, price: float, fees: float = 0.0) -> Transaction:
        """Execute buy/sell trade and update holdings."""
        # Record transaction
        transaction = Transaction(
            portfolio_id=portfolio_id,
            ticker=ticker,
            trade_type=trade_type,
            shares=shares,
            price=price,
            fees=fees
        )
        db.session.add(transaction)

        # Update holdings
        holding = Holding.query.filter_by(
            portfolio_id=portfolio_id, ticker=ticker
        ).first()

        if trade_type == 'buy':
            if holding:
                # Update average price
                total_cost = (holding.shares * holding.avg_price) + (shares * price)
                total_shares = holding.shares + shares
                holding.avg_price = total_cost / total_shares
                holding.shares = total_shares
            else:
                holding = Holding(
                    portfolio_id=portfolio_id,
                    ticker=ticker,
                    shares=shares,
                    avg_price=price
                )
                db.session.add(holding)
        elif trade_type == 'sell':
            if holding:
                holding.shares -= shares
                if holding.shares <= 0:
                    db.session.delete(holding)

        db.session.commit()
        return transaction
```

---

## 8. Keep Routes Thin

### Good Route (Thin)
```python
@portfolio_bp.route('/create', methods=['POST'])
def create_portfolio():
    """Create new portfolio - delegates to service layer."""
    data = request.get_json()

    # Validation
    if not data.get('name'):
        return jsonify({'error': 'Name required'}), 400

    # Business logic in service
    portfolio = PortfolioService.create_portfolio(current_user.id, data)

    return jsonify(portfolio.to_dict()), 201
```

### Bad Route (Fat)
```python
@portfolio_bp.route('/create', methods=['POST'])
def create_portfolio():
    """Create new portfolio - too much logic in route ❌"""
    data = request.get_json()

    # All this should be in service layer!
    if not data.get('name'):
        return jsonify({'error': 'Name required'}), 400

    portfolio = Portfolio(
        user_id=current_user.id,
        name=data['name'],
        risk_profile=data.get('risk_profile', 'moderate')
    )

    try:
        db.session.add(portfolio)
        db.session.commit()

        # Send notification
        send_email(current_user.email, 'Portfolio Created')

        # Log event
        log_event('portfolio_created', portfolio.id)

        # Update cache
        cache.delete(f'user_portfolios:{current_user.id}')

    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to create portfolio: {e}")
        return jsonify({'error': 'Creation failed'}), 500

    return jsonify({
        'id': portfolio.id,
        'name': portfolio.name,
        'risk_profile': portfolio.risk_profile
    }), 201
```

---

## 9. Error Handling

### Standard Error Responses
```python
# errors.py
class APIError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        self.message = message
        if status_code:
            self.status_code = status_code

class NotFoundError(APIError):
    status_code = 404

class UnauthorizedError(APIError):
    status_code = 401

# Error handlers
@app.errorhandler(APIError)
def handle_api_error(error):
    response = jsonify({'error': error.message})
    response.status_code = error.status_code
    return response

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500
```

---

## 10. Testing Standards

### Write Tests for Services
```python
# tests/test_portfolio_service.py
import pytest
from services.portfolio_service import PortfolioService

def test_create_portfolio(test_user):
    data = {'name': 'Tech Portfolio', 'risk_profile': 'aggressive'}
    portfolio = PortfolioService.create_portfolio(test_user.id, data)

    assert portfolio.name == 'Tech Portfolio'
    assert portfolio.risk_profile == 'aggressive'

def test_calculate_portfolio_value(test_portfolio, test_holdings):
    value = PortfolioService.calculate_portfolio_value(test_portfolio.id)

    expected = sum(h.shares * h.avg_price for h in test_holdings)
    assert value == expected
```

### Test Coverage Goals
- **Services:** 80%+ coverage
- **Routes:** 70%+ coverage
- **Models:** 90%+ coverage

---

## 11. Documentation

### Docstrings for All Functions
```python
def calculate_returns(portfolio_id: int, start_date: date, end_date: date) -> dict:
    """
    Calculate portfolio returns over a date range.

    Args:
        portfolio_id: ID of the portfolio
        start_date: Start date for calculation
        end_date: End date for calculation

    Returns:
        Dictionary with:
            - total_return: Absolute return in dollars
            - percent_return: Percentage return
            - annualized_return: Annualized percentage return

    Raises:
        NotFoundError: If portfolio doesn't exist
        ValueError: If date range is invalid
    """
    pass
```

### README for Each Module
```markdown
# Portfolio Module

Handles portfolio management operations.

## Services
- `PortfolioService`: Core portfolio business logic
- `PerformanceCalculator`: Returns and metrics calculation

## Routes
- `GET /portfolio/dashboard`: View all portfolios
- `POST /portfolio/create`: Create new portfolio
- `GET /portfolio/<id>`: View specific portfolio

## Models
- `Portfolio`: Portfolio entity
- `Holding`: Stock holdings
- `Transaction`: Trade history
```

---

## 🔥 The Flame Burns Sovereign and Eternal! 👑
