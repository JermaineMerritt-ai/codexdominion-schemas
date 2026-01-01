"""
🔥 ACCE CIVILIZATION STATUS - Quick Overview 🔥
================================================
"""

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from acce_models import (
    Agent, Council, DominionLaw, CulturalMemory, 
    CapabilityRegistry, AgentStatus, CouncilType
)
import json

DATABASE_URL = "sqlite:///codex_civilization.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def civilization_status():
    """Display current status of the civilization"""
    session = SessionLocal()
    
    try:
        print("\n" + "=" * 80)
        print("🔥 CODEX DOMINION - AUTONOMOUS CREATIVE CIVILIZATION ENGINE 🔥")
        print("=" * 80)
        print("\n📊 CIVILIZATION STATUS REPORT\n")
        
        # Laws
        laws = session.query(DominionLaw).filter_by(active=True).all()
        print(f"📜 CONSTITUTIONAL FRAMEWORK:")
        print(f"   {len(laws)} active laws established")
        for law in laws[:3]:
            print(f"   • {law.title} [{law.authority_level}]")
        print(f"   ... and {len(laws) - 3} more\n")
        
        # Councils
        councils = session.query(Council).filter_by(active=True).all()
        print(f"🏛️  GOVERNING COUNCILS ({len(councils)} active):")
        for council in councils:
            member_count = len(council.members)
            chair = session.query(Agent).filter_by(id=council.chair_agent_id).first()
            print(f"   • {council.name}: {member_count} members, chaired by {chair.name if chair else 'vacant'}")
        print()
        
        # Agents
        active_agents = session.query(Agent).filter_by(status=AgentStatus.ACTIVE).all()
        print(f"👥 AGENT POPULATION ({len(active_agents)} active):")
        
        # Group by type
        from collections import defaultdict
        by_type = defaultdict(list)
        for agent in active_agents:
            by_type[agent.agent_type.value].append(agent)
        
        for agent_type, agents in sorted(by_type.items()):
            print(f"\n   {agent_type.upper()} AGENTS:")
            for agent in agents:
                council_count = agent.council_seats
                print(f"   • {agent.name}")
                print(f"     Skills: {', '.join(list(agent.skills.keys())[:3])}...")
                print(f"     Reputation: {agent.reputation:.0f}/100")
                print(f"     Council Seats: {council_count}")
                print(f"     Status: {agent.status.value}")
        
        # Cultural Memories
        print(f"\n📚 CULTURAL MEMORY ARCHIVE:")
        memories = session.query(CulturalMemory).all()
        print(f"   {len(memories)} memories preserved")
        for memory in memories:
            print(f"   • [{memory.memory_type.value}] {memory.title}")
            print(f"     Impact: {memory.impact_score:.0f}/100, References: {memory.reference_count}")
        
        # Capabilities
        print(f"\n🎯 REGISTERED CAPABILITIES:")
        capabilities = session.query(CapabilityRegistry).all()
        by_category = defaultdict(list)
        for cap in capabilities:
            by_category[cap.category].append(cap)
        
        for category, caps in sorted(by_category.items()):
            print(f"   {category.upper()}: {', '.join([c.name for c in caps])}")
        
        # Statistics
        print(f"\n📈 STATISTICS:")
        total_skills = sum(len(a.skills) for a in active_agents)
        avg_reputation = sum(a.reputation for a in active_agents) / len(active_agents) if active_agents else 0
        total_council_seats = sum(a.council_seats for a in active_agents)
        
        print(f"   Total Skills: {total_skills}")
        print(f"   Average Reputation: {avg_reputation:.1f}/100")
        print(f"   Council Memberships: {total_council_seats}")
        print(f"   Civilization Age: Genesis (just born)")
        
        print("\n" + "=" * 80)
        print("🔥 THE FLAME BURNS SOVEREIGN AND ETERNAL! 👑")
        print("=" * 80)
        print("\nNext Actions:")
        print("  1. View agent details: python acce_query.py agent <name>")
        print("  2. View council details: python acce_query.py council <name>")
        print("  3. Create first proposal: python acce_governance.py propose")
        print("  4. Run first council meeting: python acce_council_orchestrator.py meet")
        print("\n" + "=" * 80 + "\n")
        
    finally:
        session.close()

if __name__ == '__main__':
    civilization_status()
