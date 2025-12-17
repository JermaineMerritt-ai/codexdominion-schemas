"""
Database models for Codex Dominion
SQLAlchemy ORM models for PostgreSQL/SQLite
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from typing import Optional

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  # user, admin, analyst
    risk_profile_default = db.Column(db.String(50), nullable=False, default='moderate')  # conservative, moderate, aggressive
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    portfolios = db.relationship('UserPortfolio', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password: str) -> None:
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify password"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'risk_profile_default': self.risk_profile_default,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<User {self.email}>'


class Portfolio(db.Model):
    """Portfolio model - stores individual portfolios"""
    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    risk_profile = db.Column(db.String(50), nullable=False, default='moderate')  # conservative, moderate, aggressive
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('user_portfolios', lazy='dynamic'))

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'risk_profile': self.risk_profile,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Portfolio {self.name} (user={self.user_id})>'


class UserPortfolio(db.Model):
    """Link table between users and portfolios (for portfolio sharing/collaboration)"""
    __tablename__ = 'user_portfolios'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False, index=True)
    is_favorite = db.Column(db.Boolean, default=False)
    permission = db.Column(db.String(20), nullable=False, default='read')  # read, write, admin
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    portfolio = db.relationship('Portfolio', backref=db.backref('shared_with', lazy='dynamic'))

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'portfolio_id': self.portfolio_id,
            'is_favorite': self.is_favorite,
            'permission': self.permission,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<UserPortfolio user={self.user_id} portfolio={self.portfolio_id}>'


class Holding(db.Model):
    """Portfolio holdings - tracks stock positions"""
    __tablename__ = 'holdings'

    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False, index=True)
    ticker = db.Column(db.String(20), nullable=False, index=True)
    shares = db.Column(db.Float, nullable=False)
    avg_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    portfolio = db.relationship('Portfolio', backref=db.backref('holdings', lazy='dynamic', cascade='all, delete-orphan'))

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'portfolio_id': self.portfolio_id,
            'ticker': self.ticker,
            'shares': self.shares,
            'avg_price': self.avg_price,
            'current_value': self.shares * self.avg_price,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Holding {self.ticker} ({self.shares} shares @ ${self.avg_price})>'


class Transaction(db.Model):
    """Portfolio transactions - buy/sell trade history"""
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False, index=True)
    ticker = db.Column(db.String(20), nullable=False, index=True)
    trade_type = db.Column(db.String(10), nullable=False)  # buy, sell
    shares = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    fees = db.Column(db.Float, nullable=False, default=0.0)
    executed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    portfolio = db.relationship('Portfolio', backref=db.backref('transactions', lazy='dynamic', cascade='all, delete-orphan'))

    @property
    def total_value(self) -> float:
        """Calculate total transaction value including fees"""
        return (self.shares * self.price) + self.fees

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'portfolio_id': self.portfolio_id,
            'ticker': self.ticker,
            'trade_type': self.trade_type,
            'shares': self.shares,
            'price': self.price,
            'fees': self.fees,
            'total_value': self.total_value,
            'executed_at': self.executed_at.isoformat() if self.executed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Transaction {self.trade_type.upper()} {self.shares} {self.ticker} @ ${self.price}>'


class StockPrice(db.Model):
    """Historical stock price data - OHLCV"""
    __tablename__ = 'stock_prices'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.BigInteger, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Composite index for efficient queries
    __table_args__ = (
        db.Index('idx_ticker_date', 'ticker', 'date'),
        db.UniqueConstraint('ticker', 'date', name='uq_ticker_date')
    )

    @property
    def daily_change(self) -> float:
        """Calculate daily price change"""
        return self.close - self.open

    @property
    def daily_change_percent(self) -> float:
        """Calculate daily percentage change"""
        if self.open == 0:
            return 0.0
        return ((self.close - self.open) / self.open) * 100

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'ticker': self.ticker,
            'date': self.date.isoformat() if self.date else None,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume,
            'daily_change': self.daily_change,
            'daily_change_percent': round(self.daily_change_percent, 2),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<StockPrice {self.ticker} {self.date} ${self.close}>'


class MarketAlert(db.Model):
    """Market alerts and significant events"""
    __tablename__ = 'market_alerts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    ticker = db.Column(db.String(20), nullable=False, index=True)
    reason_summary = db.Column(db.Text, nullable=False)
    volatility_score = db.Column(db.Float, nullable=False)
    volume_vs_avg = db.Column(db.Float, nullable=False)
    tags = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'ticker': self.ticker,
            'reason_summary': self.reason_summary,
            'volatility_score': self.volatility_score,
            'volume_vs_avg': self.volume_vs_avg,
            'tags': self.tags or [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<MarketAlert {self.ticker} {self.date} volatility={self.volatility_score}>'


class NewsletterSubscriber(db.Model):
    """Newsletter subscribers with preferences"""
    __tablename__ = 'newsletter_subscribers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    risk_profile = db.Column(db.String(50), nullable=False)
    segments = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'risk_profile': self.risk_profile,
            'segments': self.segments or [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<NewsletterSubscriber {self.email} ({self.risk_profile})>'


class Session(db.Model):
    """User session tracking"""
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    session_token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(255))
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', backref='sessions')

    def is_valid(self) -> bool:
        """Check if session is still valid"""
        return datetime.utcnow() < self.expires_at

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_token': self.session_token,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Session user={self.user_id} token={self.session_token[:8]}...>'


def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)

    with app.app_context():
        # Create all tables
        db.create_all()

        # Create default admin user if none exists
        if User.query.count() == 0:
            admin = User(
                email='admin@codexdominion.com',
                role='admin',
                risk_profile_default='moderate'
            )
            admin.set_password('codex2025')  # Change this!
            db.session.add(admin)
            db.session.commit()
            print(f"✅ Created default admin user: {admin.email}")
