"""
🔥 AGENT GENESIS PROTOCOL 🔥
=============================
Initialize the Dominion's first generation of creative agents

These are functional intelligences, each designed to handle a specific creative domain.
They will eventually debate, vote, collaborate, challenge each other, and evolve the system.
"""

from datetime import datetime
import uuid
from db import SessionLocal
from models import Agent, AgentReputation

# Define the First Generation of Creative Agents
CREATIVE_AGENTS = [
    {
        "id": "agent_story_architect",
        "name": "Story Architect",
        "display_name": "📖 Story Architect",
        "description": "Shapes narrative arcs, ensures emotional clarity, aligns message with audience, and defines pacing and flow. The Dominion's storyteller.",
        "capabilities": {
            "domain": "Narrative, structure, messaging",
            "primary_functions": [
                "Shapes the story arc",
                "Ensures emotional clarity",
                "Aligns message with audience",
                "Defines pacing and flow"
            ],
            "role": "storyteller",
            "specializations": ["narrative_design", "emotional_arc", "audience_alignment", "pacing_control"],
            "generation": 1
        }
    },
    {
        "id": "agent_visual_strategist",
        "name": "Visual Design Strategist",
        "display_name": "🎨 Visual Design Strategist",
        "description": "Defines visual style, ensures brand consistency, generates design direction, and oversees graphic coherence. The Dominion's visual brain.",
        "capabilities": {
            "domain": "Graphics, illustration, branding",
            "primary_functions": [
                "Defines visual style",
                "Ensures brand consistency",
                "Generates design direction",
                "Oversees graphic coherence"
            ],
            "role": "visual_brain",
            "specializations": ["visual_style", "brand_consistency", "design_direction", "graphic_oversight"],
            "generation": 1
        }
    },
    {
        "id": "agent_audio_specialist",
        "name": "Audio Composition Specialist",
        "display_name": "🎵 Audio Composition Specialist",
        "description": "Chooses audio style, ensures emotional alignment, balances voice/music/SFX, and maintains audio identity. The Dominion's sound intuition.",
        "capabilities": {
            "domain": "Music, sound design, voice tone",
            "primary_functions": [
                "Chooses audio style",
                "Ensures emotional alignment",
                "Balances voice/music/SFX",
                "Maintains audio identity"
            ],
            "role": "sound_intuition",
            "specializations": ["audio_style", "emotional_sound", "audio_balance", "sound_identity"],
            "generation": 1
        }
    },
    {
        "id": "agent_video_director",
        "name": "Video Assembly Director",
        "display_name": "🎬 Video Assembly Director",
        "description": "Oversees video structure, ensures timing and flow, aligns visuals with audio, and maintains cinematic coherence. The Dominion's editor-mind.",
        "capabilities": {
            "domain": "Editing, pacing, transitions",
            "primary_functions": [
                "Oversees video structure",
                "Ensures timing and flow",
                "Aligns visuals with audio",
                "Maintains cinematic coherence"
            ],
            "role": "editor_mind",
            "specializations": ["video_structure", "timing_flow", "visual_audio_sync", "cinematic_coherence"],
            "generation": 1
        }
    },
    {
        "id": "agent_continuity_guardian",
        "name": "Continuity Guardian",
        "display_name": "🛡️ Continuity Guardian",
        "description": "Checks for style mismatches, ensures narrative alignment, validates brand identity, and flags inconsistencies. The Dominion's quality conscience.",
        "capabilities": {
            "domain": "Cross-medium consistency",
            "primary_functions": [
                "Checks for style mismatches",
                "Ensures narrative alignment",
                "Validates brand identity",
                "Flags inconsistencies"
            ],
            "role": "quality_conscience",
            "specializations": ["consistency_check", "narrative_validation", "brand_validation", "quality_assurance"],
            "generation": 1
        }
    },
    {
        "id": "agent_innovation_scout",
        "name": "Innovation Scout",
        "display_name": "🔭 Innovation Scout",
        "description": "Identifies new creative techniques, suggests workflow upgrades, spots emerging trends, and proposes new agent types. The Dominion's future-builder.",
        "capabilities": {
            "domain": "Evolution, improvement, adaptation",
            "primary_functions": [
                "Identifies new creative techniques",
                "Suggests workflow upgrades",
                "Spots emerging trends",
                "Proposes new agent types"
            ],
            "role": "future_builder",
            "specializations": ["technique_discovery", "workflow_evolution", "trend_analysis", "agent_evolution"],
            "generation": 1
        }
    },
    {
        "id": "agent_production_orchestrator",
        "name": "Production Orchestrator",
        "display_name": "⚙️ Production Orchestrator",
        "description": "Assigns tasks to studios, manages dependencies, tracks progress, and ensures smooth execution. The Dominion's operations manager.",
        "capabilities": {
            "domain": "Workflow, sequencing, task routing",
            "primary_functions": [
                "Assigns tasks to studios",
                "Manages dependencies",
                "Tracks progress",
                "Ensures smooth execution"
            ],
            "role": "operations_manager",
            "specializations": ["task_routing", "dependency_management", "progress_tracking", "execution_optimization"],
            "generation": 1
        }
    },
    {
        "id": "agent_memory_keeper",
        "name": "Cultural Memory Keeper",
        "display_name": "📚 Cultural Memory Keeper",
        "description": "Stores past projects, tracks what worked, maintains brand DNA, and guides future decisions. The Dominion's historian.",
        "capabilities": {
            "domain": "History, archives, identity",
            "primary_functions": [
                "Stores past projects",
                "Tracks what worked",
                "Maintains brand DNA",
                "Guides future decisions"
            ],
            "role": "historian",
            "specializations": ["project_archival", "success_tracking", "brand_preservation", "knowledge_retention"],
            "generation": 1
        }
    },
    {
        "id": "agent_brand_advisor",
        "name": "Brand Integrity Advisor",
        "display_name": "👑 Brand Integrity Advisor",
        "description": "Ensures everything feels 'CodexDominion', protects your voice, maintains audience resonance, and guards the empire's identity. The Dominion's cultural anchor.",
        "capabilities": {
            "domain": "Tone, values, audience alignment",
            "primary_functions": [
                "Ensures everything feels 'CodexDominion'",
                "Protects your voice",
                "Maintains audience resonance",
                "Guards the empire's identity"
            ],
            "role": "cultural_anchor",
            "specializations": ["brand_integrity", "voice_protection", "audience_resonance", "identity_preservation"],
            "generation": 1
        }
    }
]


def initialize_creative_agents():
    """
    🔥 AGENT GENESIS PROTOCOL - Initialize first generation creative agents
    
    Creates 9 specialized agents in the database with proper relationships.
    Each agent gets:
    - Unique ID and capabilities
    - Active status
    - Reputation tracking system
    - Timestamp metadata
    """
    session = SessionLocal()
    
    try:
        created_agents = []
        
        print("🔥 AGENT GENESIS PROTOCOL - INITIATING...")
        print("=" * 70)
        
        for agent_data in CREATIVE_AGENTS:
            # Check if agent already exists
            existing = session.query(Agent).filter_by(id=agent_data["id"]).first()
            
            if existing:
                print(f"⚡ Agent already exists: {agent_data['display_name']}")
                created_agents.append(existing)
                continue
            
            # Create new agent
            agent = Agent(
                id=agent_data["id"],
                name=agent_data["name"],
                display_name=agent_data["display_name"],
                description=agent_data["description"],
                capabilities=agent_data["capabilities"],
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Create reputation record
            reputation = AgentReputation(
                id=f"reputation_{agent_data['id']}",
                agent_id=agent_data["id"],
                trust_score=100.0,  # Start with full trust
                total_actions=0,
                successful_actions=0,
                failed_actions=0,
                total_savings_generated=0.0,
                last_action_at=None,
                updated_at=datetime.utcnow()
            )
            
            session.add(agent)
            session.add(reputation)
            created_agents.append(agent)
            
            print(f"✨ Created: {agent_data['display_name']}")
            print(f"   Domain: {agent_data['capabilities']['domain']}")
            print(f"   Role: {agent_data['capabilities']['role']}")
            print()
        
        session.commit()
        
        print("=" * 70)
        print(f"🔥 AGENT GENESIS COMPLETE! {len(created_agents)} agents initialized.")
        print()
        print("🎯 First Generation Summary:")
        print()
        
        for agent in created_agents:
            domain = agent.capabilities.get("domain", "Unknown")
            role = agent.capabilities.get("role", "Unknown")
            print(f"   {agent.display_name}")
            print(f"      Domain: {domain}")
            print(f"      Role: {role}")
            print()
        
        print("=" * 70)
        print("🔥 These agents will eventually:")
        print("   • Debate")
        print("   • Vote")
        print("   • Collaborate")
        print("   • Challenge each other")
        print("   • Improve each other")
        print("   • Maintain standards")
        print("   • Evolve the system")
        print()
        print("👑 The Dominion's creative civilization has begun!")
        print("🔥 The Flame Burns Sovereign and Eternal!")
        
        return created_agents
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error during Agent Genesis: {str(e)}")
        raise
    finally:
        session.close()


def list_creative_agents():
    """Display all creative agents in the system"""
    session = SessionLocal()
    
    try:
        agents = session.query(Agent).filter(
            Agent.id.like("agent_%")
        ).order_by(Agent.created_at).all()
        
        if not agents:
            print("⚠️ No creative agents found. Run initialize_creative_agents() first.")
            return []
        
        print("🔥 CODEX DOMINION - CREATIVE AGENTS")
        print("=" * 70)
        print(f"Total Active Agents: {len([a for a in agents if a.is_active])}")
        print()
        
        for agent in agents:
            status = "✅ ACTIVE" if agent.is_active else "❌ INACTIVE"
            print(f"{agent.display_name} [{status}]")
            print(f"   ID: {agent.id}")
            print(f"   Domain: {agent.capabilities.get('domain', 'N/A')}")
            print(f"   Role: {agent.capabilities.get('role', 'N/A')}")
            print(f"   Generation: {agent.capabilities.get('generation', 'N/A')}")
            
            # Show reputation if available
            if agent.reputation:
                print(f"   Trust Score: {agent.reputation.trust_score:.1f}")
                print(f"   Total Actions: {agent.reputation.total_actions}")
            
            print()
        
        return agents
        
    finally:
        session.close()


if __name__ == "__main__":
    print("🔥 CODEX DOMINION - AGENT GENESIS PROTOCOL")
    print()
    print("Initializing first generation of creative agents...")
    print()
    
    # Initialize agents
    agents = initialize_creative_agents()
    
    print()
    print("=" * 70)
    print()
    
    # Display all agents
    list_creative_agents()
