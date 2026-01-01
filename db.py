"""
Codex Dominion - Database Session Management
Provides SQLAlchemy engine, session factory, and connection utilities

NOTE: This file is a copy of database.py for import consistency.
      Some files import from 'database', others from 'db'.
      Both modules are identical and can be used interchangeably.
"""

from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.pool import QueuePool

from config import config

# Create SQLAlchemy engine with connection pooling
# Note: SQLite uses different pooling strategy than PostgreSQL
is_sqlite = config.get_database_url().startswith('sqlite')

if is_sqlite:
    # SQLite: Use StaticPool for single-threaded access
    from sqlalchemy.pool import StaticPool
    engine = create_engine(
        config.get_database_url(),
        echo=config.SQLALCHEMY_ECHO,
        poolclass=StaticPool,
        connect_args={'check_same_thread': False}  # Allow multi-threaded access
    )
else:
    # PostgreSQL/MySQL: Use QueuePool
    engine = create_engine(
        config.get_database_url(),
        echo=config.SQLALCHEMY_ECHO,
        pool_size=config.SQLALCHEMY_POOL_SIZE,
        max_overflow=config.SQLALCHEMY_MAX_OVERFLOW,
        pool_timeout=config.SQLALCHEMY_POOL_TIMEOUT,
        pool_recycle=config.SQLALCHEMY_POOL_RECYCLE,
        poolclass=QueuePool,
        pool_pre_ping=True,  # Verify connections before using them
    )

# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# Create thread-safe scoped session
SessionFactory = scoped_session(SessionLocal)


def get_session() -> Session:
    """
    Get a database session.
    
    Usage in Flask/FastAPI:
        session = get_session()
        try:
            # Use session
            agents = session.query(Agent).all()
        finally:
            session.close()
    
    Returns:
        Session: SQLAlchemy session instance
    """
    return SessionFactory()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions with automatic cleanup.
    
    Usage:
        with get_db_session() as session:
            agents = session.query(Agent).all()
            # Session automatically closed and rolled back on error
    
    Yields:
        Session: SQLAlchemy session instance
    """
    session = SessionFactory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    """
    Initialize database - create all tables defined in models.
    
    Usage:
        from db import init_db
        init_db()  # Creates all tables
    """
    from models import Base  # Import here to avoid circular imports
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")


def drop_db():
    """
    Drop all database tables - USE WITH CAUTION!
    Only for development/testing environments.
    """
    from models import Base
    if not config.is_production():
        Base.metadata.drop_all(bind=engine)
        print("⚠️  All database tables dropped")
    else:
        raise RuntimeError("Cannot drop database in production environment")


def get_db_info() -> dict:
    """
    Get database connection information.
    
    Returns:
        dict: Database info including URL, pool size, etc.
    """
    return {
        'url': config.DATABASE_URL.split('@')[-1],  # Hide credentials
        'pool_size': config.SQLALCHEMY_POOL_SIZE,
        'max_overflow': config.SQLALCHEMY_MAX_OVERFLOW,
        'pool_timeout': config.SQLALCHEMY_POOL_TIMEOUT,
        'pool_recycle': config.SQLALCHEMY_POOL_RECYCLE,
        'echo': config.SQLALCHEMY_ECHO,
        'environment': config.APP_ENV
    }


# Event listener to log connection pool stats (development only)
if config.DEBUG:
    @event.listens_for(engine, "connect")
    def receive_connect(dbapi_conn, connection_record):
        print(f"🔌 Database connection established")
    
    @event.listens_for(engine, "close")
    def receive_close(dbapi_conn, connection_record):
        print(f"🔌 Database connection closed")


# Cleanup function for application shutdown
def close_db():
    """
    Close all database connections and dispose of the engine.
    Call this during application shutdown.
    """
    SessionFactory.remove()
    engine.dispose()
    print("✅ Database connections closed")


# Export commonly used items
__all__ = [
    'engine',
    'SessionLocal',
    'SessionFactory',
    'get_session',
    'get_db_session',
    'init_db',
    'drop_db',
    'get_db_info',
    'close_db'
]
