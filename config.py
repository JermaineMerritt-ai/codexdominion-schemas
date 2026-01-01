"""
Codex Dominion - Central Configuration
Loads environment variables and provides application configuration
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Application configuration class"""
    
    # Database Configuration
    # Using SQLite for development (no installation required)
    # Switch to PostgreSQL in production via DATABASE_URL env var
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        'sqlite:///codexdominion.db'
    )
    
    # SQLAlchemy Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'false').lower() == 'true'
    SQLALCHEMY_POOL_SIZE = int(os.getenv('SQLALCHEMY_POOL_SIZE', '10'))
    SQLALCHEMY_MAX_OVERFLOW = int(os.getenv('SQLALCHEMY_MAX_OVERFLOW', '20'))
    SQLALCHEMY_POOL_TIMEOUT = int(os.getenv('SQLALCHEMY_POOL_TIMEOUT', '30'))
    SQLALCHEMY_POOL_RECYCLE = int(os.getenv('SQLALCHEMY_POOL_RECYCLE', '3600'))
    
    # Application Configuration
    APP_ENV = os.getenv('PYTHON_ENV', 'development')
    DEBUG = APP_ENV == 'development'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # API Configuration
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', '8001'))
    API_URL = os.getenv('NEXT_PUBLIC_API_URL', 'http://localhost:8001')
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',')
    
    # Redis Configuration
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
    
    # Azure Configuration
    AZURE_SUBSCRIPTION_ID = os.getenv('AZURE_SUBSCRIPTION_ID')
    AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get the database URL with proper format for SQLAlchemy"""
        url = cls.DATABASE_URL
        
        # Only process PostgreSQL URLs, leave SQLite as-is
        if url.startswith('sqlite'):
            return url
        
        # Ensure postgresql+psycopg2:// format for SQLAlchemy
        if url.startswith('postgresql://'):
            url = url.replace('postgresql://', 'postgresql+psycopg2://', 1)
        elif not url.startswith('postgresql+psycopg2://') and not url.startswith('sqlite'):
            url = f'postgresql+psycopg2://{url}'
        
        return url
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment"""
        return cls.APP_ENV == 'production'
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment"""
        return cls.APP_ENV == 'development'


# Create config instance
config = Config()
