"""
🔥 CREATE INTEGRATION LAYER TABLES 🔥
======================================
Creates the 5 new database tables for civilization integration
"""

from models import Base
from db import engine


def create_integration_tables():
    """Create all integration layer tables"""
    print("\n🔥 Creating Integration Layer Tables...")
    print("=" * 60)
    
    # Import models to ensure they're registered
    from models import (
        AgentCollaboration,
        ProposalWorkflow,
        KnowledgeAccess,
        IntegrationEvent,
        CivilizationMetrics
    )
    
    try:
        # Create all tables (only creates those that don't exist)
        Base.metadata.create_all(bind=engine)
        
        print("\n✓ Database tables created successfully:")
        print("  • agent_collaborations (multi-agent projects)")
        print("  • proposal_workflows (council governance routing)")
        print("  • knowledge_access (cultural memory usage tracking)")
        print("  • integration_events (cross-system activity log)")
        print("  • civilization_metrics (ecosystem health vitals)")
        
        print("\n" + "=" * 60)
        print("✅ Integration layer database ready")
        print("\nNext: Run civilization_integration_protocol.py to initialize data")
        
    except Exception as e:
        print(f"\n❌ Error creating tables: {e}")
        raise


if __name__ == "__main__":
    create_integration_tables()
