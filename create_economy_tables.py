"""
Create Dominion Economy Database Tables
Phase 50 - Step 1: Value System Blueprint

Creates tables for:
- AgentReputationProfile (5 value types, voting weight, tier)
- ValueTransaction (value flow tracking)
- IncentiveEvent (rewards and penalties)
- ReputationHistory (historical snapshots)
- EconomyMetrics (system-wide health)
"""

from models import Base
from db import engine

def create_economy_tables():
    """Create all economy-related database tables"""
    print("🔥 Creating Dominion Economy tables...")
    
    # Import to ensure models are registered
    from models import (
        AgentReputationProfile,
        ValueTransaction,
        IncentiveEvent,
        ReputationHistory,
        EconomyMetrics
    )
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    print("✓ Database tables created successfully:")
    print("  - agent_reputation_profiles (5 value types, voting weight, tier)")
    print("  - value_transactions (value flow tracking)")
    print("  - incentive_events (rewards and penalties)")
    print("  - reputation_history (historical snapshots)")
    print("  - economy_metrics (system-wide health)")
    print("\n🔥 The Value System Blueprint is ready for data!")

if __name__ == "__main__":
    create_economy_tables()
