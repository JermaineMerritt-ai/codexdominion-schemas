"""
Create Cultural Memory Architecture database tables
"""

from models import Base
from db import engine

def create_cma_tables():
    """Create all Cultural Memory Architecture tables"""
    print("\n" + "=" * 60)
    print("🔥 CREATING CULTURAL MEMORY ARCHITECTURE TABLES")
    print("=" * 60)
    
    # Create all tables (will only create ones that don't exist)
    Base.metadata.create_all(bind=engine)
    
    print("\n✓ Database tables created successfully")
    print("\nNew tables:")
    print("  • creative_projects")
    print("  • creative_decisions")
    print("  • identity_codex")
    print("  • style_patterns")
    print("  • cultural_memory")
    print("  • brand_evolution")
    print("\n" + "=" * 60)
    print("🔥 Ready to initialize Cultural Memory Architecture")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    create_cma_tables()
