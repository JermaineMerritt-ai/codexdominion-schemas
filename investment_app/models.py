"""
Database Models
"""
from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user')
    risk_profile = db.Column(db.String(50), default='moderate')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    portfolios = db.relationship('Portfolio', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Portfolio(db.Model):
    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    risk_profile = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    holdings = db.relationship('Holding', backref='portfolio', lazy='dynamic', cascade='all, delete-orphan')
    trades = db.relationship('Trade', backref='portfolio', lazy='dynamic', cascade='all, delete-orphan')

class Holding(db.Model):
    __tablename__ = 'holdings'

    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    ticker = db.Column(db.String(10), nullable=False, index=True)
    shares = db.Column(db.Numeric(10, 2), nullable=False)
    avg_cost = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Trade(db.Model):
    __tablename__ = 'trades'

    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    ticker = db.Column(db.String(10), nullable=False, index=True)
    trade_type = db.Column(db.String(10), nullable=False)  # 'buy' or 'sell'
    shares = db.Column(db.Numeric(10, 2), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    fees = db.Column(db.Numeric(10, 2), default=0.00)
    trade_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255))
    sector = db.Column(db.String(100), index=True)
    price = db.Column(db.Numeric(10, 2))
    market_cap = db.Column(db.Numeric(15, 2))
    pe_ratio = db.Column(db.Numeric(10, 2))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Fundamental(db.Model):
    __tablename__ = 'fundamentals'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), db.ForeignKey('stocks.ticker'), nullable=False, index=True)
    revenue_trend = db.Column(db.String(10))  # 'up', 'down', 'flat'
    net_income_trend = db.Column(db.String(10))
    debt_level = db.Column(db.String(20))  # 'low', 'moderate', 'elevated'
    profit_margin_strength = db.Column(db.String(20))  # 'weak', 'moderate', 'strong'
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Alert(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    ticker = db.Column(db.String(10), db.ForeignKey('stocks.ticker'), nullable=False, index=True)
    reason_summary = db.Column(db.Text, nullable=False)
    volatility_score = db.Column(db.Numeric(5, 2))
    volume_vs_avg = db.Column(db.Numeric(10, 2))
    tags = db.Column(db.JSON)

class Subscriber(db.Model):
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    risk_preference = db.Column(db.String(50), default='moderate')
    daily_email = db.Column(db.Boolean, default=True)
    weekly_email = db.Column(db.Boolean, default=True)
    monthly_email = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AdvisorClient(db.Model):
    __tablename__ = 'advisor_clients'

    id = db.Column(db.Integer, primary_key=True)
    advisor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
