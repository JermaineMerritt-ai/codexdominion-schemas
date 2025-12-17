"""
Codex Dominion - Flask Application Configuration
"""

import os
from datetime import timedelta
from pathlib import Path

# Load .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass  # python-dotenv not installed, use system environment variables

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'codex-sovereign-flame-eternal-2025'

    # JSON Ledger Paths (configurable via environment or default to parent directory)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    PORTFOLIOS_FILE = os.environ.get('PORTFOLIOS_FILE') or os.path.join(BASE_DIR, 'portfolios.json')
    STOCK_ANALYSIS_FILE = os.environ.get('STOCK_ANALYSIS_FILE') or os.path.join(BASE_DIR, 'stock_analysis.json')
    PORTFOLIO_INSIGHTS_FILE = os.environ.get('PORTFOLIO_INSIGHTS_FILE') or os.path.join(BASE_DIR, 'portfolio_insights.json')
    TRADING_PICKS_FILE = os.environ.get('TRADING_PICKS_FILE') or os.path.join(BASE_DIR, 'trading_picks.json')
    NEWSLETTER_FILE = os.environ.get('NEWSLETTER_FILE') or os.path.join(BASE_DIR, 'newsletter_subscribers.json')

    # API Keys (Optional - for enhanced features)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
    POLYGON_API_KEY = os.environ.get('POLYGON_API_KEY')
    FINNHUB_API_KEY = os.environ.get('FINNHUB_API_KEY')
    ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')

    # Email Configuration (Optional - for newsletter delivery)
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USER = os.environ.get('SMTP_USER')
    SMTP_PASS = os.environ.get('SMTP_PASS')

    # Database URL (Optional - currently using JSON ledgers)
    DATABASE_URL = os.environ.get('DATABASE_URL')

    # SQLAlchemy Configuration
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Default to SQLite for development
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'codex_dominion.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set True for SQL query logging

    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # Set True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Application settings
    JSONIFY_PRETTYPRINT_REGULAR = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max request size

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False

# Config dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
