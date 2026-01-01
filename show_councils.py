"""Display the complete council structure"""
from db import SessionLocal
from models import Council, CouncilMember, Agent

session = SessionLocal()

try:
    print("🔥 DOMINION CREATIVE COUNCIL - STRUCTURE")
    print("=" * 70)
    
    councils = session.query(Council).filter(
        Council.id.like("council_%")
    ).order_by(Council.created_at).all()
    
    print(f"Total Councils: {len(councils)}")
    print()
    
    for council in councils:
        print(f"\n{'=' * 70}")
        print(f"{council.name.upper()}")
        print(f"{'=' * 70}")
        print(f"ID: {council.id}")
        print(f"Description: {council.description}")
        
        # Display config if present
        if council.config:
            if 'function' in council.config:
                print(f"Function: {council.config['function']}")
            if 'responsibilities' in council.config:
                print(f"\nResponsibilities:")
                for resp in council.config['responsibilities']:
                    print(f"  • {resp}")
        
        print(f"\nMEMBERS:")
        
        members = session.query(CouncilMember).filter_by(
            council_id=council.id
        ).all()
        
        for member in members:
            agent = session.query(Agent).filter_by(id=member.agent_id).first()
            if agent:
                print(f"\n  {agent.display_name}")
                print(f"    Role: {member.role}")
                print(f"    Domain: {agent.capabilities.get('domain', 'N/A')}")
                print(f"    Status: {'✅ ACTIVE' if member.is_active else '❌ INACTIVE'}")
    
    print(f"\n{'=' * 70}")
    print("\n🎯 VOTING SYSTEM:")
    print("  • Total Votes: 9 (3 per council)")
    print("  • Pass Threshold: 5+ votes")
    print("  • Escalation: Controversial → Sovereign Architect")
    print("\n🔥 The Flame Burns Sovereign and Eternal! 👑")
    
finally:
    session.close()
