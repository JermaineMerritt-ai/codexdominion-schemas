"""
🔥 COUNCIL FORMATION PROTOCOL 🔥
==================================
Phase 40 - Step 2: Establishing the Dominion Creative Council (DCC)

Creates the three-tier council structure:
- High Council (Creative Vision): 3 agents
- Continuity Council (Creative Integrity): 3 agents  
- Operations Council (Creative Execution): 3 agents

Implements:
- Council hierarchy
- Agent role assignments
- Decision-making protocols
- Voting systems
- Escalation paths
"""

from datetime import datetime
import uuid
from db import SessionLocal
from models import Council, CouncilMember, Agent

# Council Definitions
COUNCIL_STRUCTURE = {
    "council_high": {
        "name": "High Council",
        "description": "The executive council that guides overall creative direction. Defines style, tone, narrative, emotional arc, and aesthetic direction.",
        "function": "Creative Vision",
        "responsibilities": [
            "Define creative style and tone",
            "Shape narrative direction",
            "Guide emotional arc",
            "Set aesthetic direction",
            "Approve major creative decisions"
        ],
        "members": [
            {
                "agent_id": "agent_story_architect",
                "role": "Chief Creative Officer",
                "vote_weight": 1,
                "specialization": "narrative_impact"
            },
            {
                "agent_id": "agent_visual_strategist",
                "role": "Visual Director",
                "vote_weight": 1,
                "specialization": "style_impact"
            },
            {
                "agent_id": "agent_audio_specialist",
                "role": "Audio Director",
                "vote_weight": 1,
                "specialization": "emotional_impact"
            }
        ],
        "voting_threshold": 2,  # 2 out of 3 to pass
        "priority": 1
    },
    "council_continuity": {
        "name": "Continuity Council",
        "description": "The guardian council that ensures brand alignment, narrative consistency, cross-medium coherence, and cultural memory preservation.",
        "function": "Creative Integrity",
        "responsibilities": [
            "Maintain brand alignment",
            "Ensure narrative consistency",
            "Validate cross-medium coherence",
            "Preserve cultural memory",
            "Protect brand identity"
        ],
        "members": [
            {
                "agent_id": "agent_continuity_guardian",
                "role": "Chief Quality Officer",
                "vote_weight": 1,
                "specialization": "consistency_check"
            },
            {
                "agent_id": "agent_brand_advisor",
                "role": "Brand Guardian",
                "vote_weight": 1,
                "specialization": "brand_identity"
            },
            {
                "agent_id": "agent_memory_keeper",
                "role": "Cultural Archivist",
                "vote_weight": 1,
                "specialization": "historical_context"
            }
        ],
        "voting_threshold": 2,  # 2 out of 3 to pass
        "priority": 2
    },
    "council_operations": {
        "name": "Operations Council",
        "description": "The engineering council that manages task routing, timelines, dependencies, workflow optimization, and innovation proposals.",
        "function": "Creative Execution",
        "responsibilities": [
            "Route tasks to appropriate studios",
            "Manage project timelines",
            "Handle dependencies",
            "Optimize workflows",
            "Propose innovations"
        ],
        "members": [
            {
                "agent_id": "agent_production_orchestrator",
                "role": "Chief Operations Officer",
                "vote_weight": 1,
                "specialization": "feasibility"
            },
            {
                "agent_id": "agent_video_director",
                "role": "Video Operations Lead",
                "vote_weight": 1,
                "specialization": "execution_quality"
            },
            {
                "agent_id": "agent_innovation_scout",
                "role": "Innovation Officer",
                "vote_weight": 1,
                "specialization": "future_potential"
            }
        ],
        "voting_threshold": 2,  # 2 out of 3 to pass
        "priority": 3
    }
}

# Decision-making configuration
DECISION_CONFIG = {
    "total_votes": 9,  # 3 councils × 3 agents each
    "pass_threshold": 5,  # Proposal passes with 5 or more votes
    "escalation_threshold": 7,  # 7+ votes = automatic approval, <3 votes = escalate
    "minimum_votes": 3,  # Minimum votes required to proceed
    "debate_phases": ["proposal", "debate", "voting", "implementation"],
    "escalation_triggers": [
        "controversial",  # Close vote (4-5 range)
        "unclear",  # Conflicting rationales
        "high_impact",  # Affects core brand
        "brand_critical"  # Identity-defining decision
    ]
}


def initialize_councils():
    """
    🔥 COUNCIL FORMATION PROTOCOL - Create the three-tier council structure
    
    Creates:
    - 3 councils (High, Continuity, Operations)
    - 9 council memberships (3 agents per council)
    - Decision-making configuration
    """
    session = SessionLocal()
    
    try:
        created_councils = []
        
        print("🔥 COUNCIL FORMATION PROTOCOL - INITIATING...")
        print("=" * 70)
        print()
        
        for council_id, council_data in COUNCIL_STRUCTURE.items():
            # Check if council already exists
            existing = session.query(Council).filter_by(id=council_id).first()
            
            if existing:
                print(f"⚡ Council already exists: {council_data['name']}")
                created_councils.append(existing)
                continue
            
            # Create council
            council = Council(
                id=council_id,
                name=council_data["name"],
                description=council_data["description"],
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                config={
                    "function": council_data["function"],
                    "responsibilities": council_data["responsibilities"],
                    "voting_threshold": council_data["voting_threshold"],
                    "priority": council_data["priority"],
                    "decision_config": DECISION_CONFIG
                }
            )
            
            session.add(council)
            created_councils.append(council)
            
            print(f"✨ Created Council: {council_data['name']}")
            print(f"   Function: {council_data['function']}")
            print(f"   Members: {len(council_data['members'])}")
            print(f"   Voting Threshold: {council_data['voting_threshold']}/{len(council_data['members'])}")
            print()
            
            # Add council members
            for member_data in council_data["members"]:
                # Verify agent exists
                agent = session.query(Agent).filter_by(id=member_data["agent_id"]).first()
                if not agent:
                    print(f"   ⚠️ Agent not found: {member_data['agent_id']}")
                    continue
                
                # Create council membership
                member = CouncilMember(
                    id=f"member_{council_id}_{member_data['agent_id']}",
                    council_id=council_id,
                    agent_id=member_data["agent_id"],
                    name=agent.name,
                    role=member_data["role"],
                    is_active=True,
                    joined_at=datetime.utcnow()
                )
                
                session.add(member)
                
                print(f"   ✅ Added: {agent.display_name}")
                print(f"      Role: {member_data['role']}")
                print(f"      Specialization: {member_data['specialization']}")
        
        session.commit()
        
        print()
        print("=" * 70)
        print(f"🔥 COUNCIL FORMATION COMPLETE! {len(created_councils)} councils established.")
        print()
        print("📊 DOMINION CREATIVE COUNCIL (DCC) STRUCTURE:")
        print()
        
        for council in created_councils:
            members = session.query(CouncilMember).filter_by(
                council_id=council.id,
                is_active=True
            ).all()
            
            print(f"👑 {council.name}")
            print(f"   Function: {council.config.get('function', 'N/A')}")
            print(f"   Responsibilities:")
            for resp in council.config.get('responsibilities', []):
                print(f"      • {resp}")
            print(f"   Members ({len(members)}):")
            for member in members:
                agent = session.query(Agent).filter_by(id=member.agent_id).first()
                print(f"      {agent.display_name if agent else member.name} - {member.role}")
            print()
        
        print("=" * 70)
        print("🎯 COUNCIL POWERS ACTIVATED:")
        print("   • Approve creative directions")
        print("   • Reject weak ideas")
        print("   • Request revisions")
        print("   • Maintain brand identity")
        print("   • Resolve inter-agent conflicts")
        print("   • Optimize workflows")
        print("   • Propose new agents")
        print("   • Guide the Dominion's evolution")
        print()
        print("🔥 DECISION-MAKING PROTOCOL:")
        print(f"   • Total Votes: {DECISION_CONFIG['total_votes']}")
        print(f"   • Pass Threshold: {DECISION_CONFIG['pass_threshold']}+ votes")
        print(f"   • Escalation: <{DECISION_CONFIG['minimum_votes']} or >{DECISION_CONFIG['escalation_threshold']} votes")
        print(f"   • Phases: {' → '.join(DECISION_CONFIG['debate_phases'])}")
        print()
        print("👑 The Sovereign Architect retains final override authority.")
        print("🔥 The Flame Burns Sovereign and Eternal!")
        
        return created_councils
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error during Council Formation: {str(e)}")
        raise
    finally:
        session.close()


def list_councils():
    """Display all councils and their members"""
    session = SessionLocal()
    
    try:
        councils = session.query(Council).filter_by(is_active=True).order_by(
            Council.config['priority'].astext.cast(type_=type(1))
        ).all()
        
        if not councils:
            print("⚠️ No councils found. Run initialize_councils() first.")
            return []
        
        print("🔥 DOMINION CREATIVE COUNCIL (DCC)")
        print("=" * 70)
        print(f"Total Active Councils: {len(councils)}")
        print()
        
        for council in councils:
            members = session.query(CouncilMember).filter_by(
                council_id=council.id,
                is_active=True
            ).all()
            
            print(f"👑 {council.name} [{council.id}]")
            print(f"   Function: {council.config.get('function', 'N/A')}")
            print(f"   Description: {council.description}")
            print(f"   Voting Threshold: {council.config.get('voting_threshold', 'N/A')}/{len(members)}")
            print(f"   Priority: {council.config.get('priority', 'N/A')}")
            print()
            print(f"   Members ({len(members)}):")
            
            for member in members:
                agent = session.query(Agent).filter_by(id=member.agent_id).first()
                if agent:
                    domain = agent.capabilities.get('domain', 'N/A')
                    specialization = None
                    
                    # Find specialization from council config
                    for member_config in COUNCIL_STRUCTURE.get(council.id, {}).get('members', []):
                        if member_config['agent_id'] == agent.id:
                            specialization = member_config['specialization']
                            break
                    
                    print(f"      {agent.display_name}")
                    print(f"         Role: {member.role}")
                    print(f"         Domain: {domain}")
                    if specialization:
                        print(f"         Specialization: {specialization}")
                    print(f"         Status: {'✅ ACTIVE' if member.is_active else '❌ INACTIVE'}")
                else:
                    print(f"      {member.name} (Agent not found)")
                    print(f"         Role: {member.role}")
            
            print()
        
        return councils
        
    finally:
        session.close()


def get_council_hierarchy():
    """Return the council hierarchy as a dictionary"""
    return {
        "structure": COUNCIL_STRUCTURE,
        "decision_config": DECISION_CONFIG,
        "total_councils": len(COUNCIL_STRUCTURE),
        "total_agents": sum(len(c["members"]) for c in COUNCIL_STRUCTURE.values()),
        "governance_model": "Three-tier council system with agent voting"
    }


if __name__ == "__main__":
    print("🔥 CODEX DOMINION - COUNCIL FORMATION PROTOCOL")
    print()
    print("Establishing the Dominion Creative Council (DCC)...")
    print()
    
    # Initialize councils
    councils = initialize_councils()
    
    print()
    print("=" * 70)
    print()
    
    # Display all councils
    list_councils()
