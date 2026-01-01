"""
Create Evolution Engine database tables
"""

from models import Base
from db import engine

def create_evolution_engine_tables():
    """Create all Evolution Engine tables"""
    print("\n" + "=" * 60)
    print("🔥 CREATING EVOLUTION ENGINE TABLES")
    print("=" * 60)
    
    # Create all tables (will only create ones that don't exist)
    Base.metadata.create_all(bind=engine)
    
    print("\n✓ Database tables created successfully")
    print("\nNew tables:")
    print("  • evolution_boundaries")
    print("  • evolution_proposals")
    print("  • agent_generation_proposals")
    print("  • technique_evolutions")
    print("  • evolution_cycles")
    print("\n" + "=" * 60)
    print("🔥 Ready to initialize Evolution Engine")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    create_evolution_engine_tables()
