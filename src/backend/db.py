"""Database session utilities for Codex Dominion."""

from typing import Generator

from src.backend.main import SessionLocal


def get_db() -> Generator:
    """Yield a database session and ensure closure."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
