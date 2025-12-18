"""
Application Configuration
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""

    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

    # Database
    DATABASE_URL = os.environ.get(
        'DATABASE_URL',
        'sqlite:///investment_app.db'  # Use SQLite for development (no server needed)
    )
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG

    # Session
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # AI Configuration
    AI_PROMPTS_DIR = os.path.join(os.path.dirname(__file__), '..', '')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'openai')  # 'openai' or 'anthropic'
    AI_MODEL = os.environ.get('AI_MODEL', 'gpt-4o-mini')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

    # Stock Data API Configuration
    STOCK_API_KEY = os.environ.get('STOCK_API_KEY')
    STOCK_API_PROVIDER = os.environ.get('STOCK_API_PROVIDER', 'database')  # 'database', 'polygon', 'alphavantage'

    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Newsletter Schedule
    DAILY_EMAIL_TIME = '08:00'  # 8 AM
    WEEKLY_EMAIL_DAY = 'monday'
    WEEKLY_EMAIL_TIME = '09:00'
    MONTHLY_EMAIL_DAY = 1  # First of month
    MONTHLY_EMAIL_TIME = '10:00'

    # Risk Profiles
    RISK_PROFILES = ['conservative', 'moderate', 'aggressive']

    # Compliance
    COMPLIANCE_MODE = True
    SHOW_DISCLAIMERS = True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Config dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
