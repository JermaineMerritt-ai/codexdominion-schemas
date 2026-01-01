"""
Display the Evolution Engine status
The self-improving Dominion
"""

from db import SessionLocal
from models import (
    EvolutionBoundary, EvolutionProposal, AgentGenerationProposal,
    TechniqueEvolution, EvolutionCycle
)


def show_evolution_engine():
    """Display complete Evolution Engine status"""
    session = SessionLocal()
    
    try:
        print("\n" + "=" * 70)
        print("🔥 EVOLUTION ENGINE - COMPLETE STATUS")
        print("=" * 70)
        
        # LAYER 4: Evolution Boundaries
        print("\n🛡️ LAYER 4: EVOLUTION BOUNDARIES")
        print("-" * 70)
        
        boundaries = session.query(EvolutionBoundary).filter_by(is_active="active").all()
        
        # Group by type
        boundary_types = {}
        for boundary in boundaries:
            if boundary.boundary_type not in boundary_types:
                boundary_types[boundary.boundary_type] = []
            boundary_types[boundary.boundary_type].append(boundary)
        
        for btype in ["sacred", "guarded", "flexible"]:
            if btype in boundary_types:
                items = boundary_types[btype]
                icon = "🔒" if btype == "sacred" else "⚠️" if btype == "guarded" else "🔓"
                print(f"\n{icon} {btype.upper()} BOUNDARIES ({len(items)})")
                for item in items:
                    print(f"   • {item.principle}")
                    print(f"     Category: {item.category} | Approval: {item.approval_required}")
                    print(f"     Protected: {item.what_is_protected}")
        
        print(f"\n✓ Total Boundaries: {len(boundaries)}")
        
        # LAYER 1: Evolution Proposals
        print("\n\n📝 LAYER 1: EVOLUTION PROPOSALS")
        print("-" * 70)
        
        proposals = session.query(EvolutionProposal).all()
        
        # Group by status
        status_groups = {}
        for proposal in proposals:
            if proposal.status not in status_groups:
                status_groups[proposal.status] = []
            status_groups[proposal.status].append(proposal)
        
        for status, items in sorted(status_groups.items()):
            status_icon = "⏳" if "pending" in status else "✅" if status == "approved" else "🚀" if status == "implemented" else "❌"
            print(f"\n{status_icon} {status.upper().replace('_', ' ')} ({len(items)})")
            for item in items:
                print(f"   • {item.title}")
                print(f"     Type: {item.proposal_type} | By: {item.proposed_by_agent}")
                if item.expected_benefits:
                    benefits = ", ".join([f"{k}: {v}" for k, v in list(item.expected_benefits.items())[:2]])
                    print(f"     Benefits: {benefits}")
        
        print(f"\n✓ Total Proposals: {len(proposals)}")
        
        # LAYER 2: Agent Generation Proposals
        print("\n\n👥 LAYER 2: NEW AGENT PROPOSALS")
        print("-" * 70)
        
        agent_proposals = session.query(AgentGenerationProposal).all()
        
        for proposal in agent_proposals:
            status_icon = "⏳" if "pending" in proposal.status else "✅" if proposal.status == "approved" else "❌"
            print(f"\n{status_icon} {proposal.proposed_agent_name}")
            print(f"   Role: {proposal.proposed_agent_role}")
            print(f"   Domain: {proposal.proposed_domain}")
            print(f"   Gap: {proposal.gap_identified[:60]}...")
            print(f"   Proposed by: {proposal.proposed_by_agent}")
            print(f"   Council: {proposal.council_assignment}")
            print(f"   Status: {proposal.status.replace('_', ' ')}")
            if proposal.agent_id_created:
                print(f"   ✅ Agent Created: {proposal.agent_id_created}")
        
        print(f"\n✓ Total Agent Proposals: {len(agent_proposals)}")
        
        # LAYER 3: Technique Evolutions
        print("\n\n🎨 LAYER 3: TECHNIQUE EVOLUTIONS")
        print("-" * 70)
        
        techniques = session.query(TechniqueEvolution).all()
        
        for technique in techniques:
            status_icon = "🧪" if technique.status == "testing" else "✅" if technique.status == "approved" else "❌"
            print(f"\n{status_icon} {technique.technique_name}")
            print(f"   Category: {technique.technique_category}")
            print(f"   Status: {technique.status}")
            print(f"   Evolution: {technique.old_approach[:40]}... → {technique.new_approach[:40]}...")
            if technique.test_results:
                results = ", ".join([f"{k}: {v}" for k, v in list(technique.test_results.items())[:2]])
                print(f"   Results: {results}")
            if technique.approved_by_council:
                print(f"   ✅ Approved by: {technique.approved_by_council}")
        
        print(f"\n✓ Total Technique Evolutions: {len(techniques)}")
        
        # LAYER 1: Evolution Cycles
        print("\n\n🔄 LAYER 1: SELF-IMPROVEMENT CYCLES")
        print("-" * 70)
        
        cycles = session.query(EvolutionCycle).all()
        
        for cycle in cycles:
            status = "🟢" if cycle.completed_at else "🔵"
            print(f"\n{status} Cycle #{cycle.cycle_number}")
            print(f"   Observation: {cycle.observation[:60]}...")
            print(f"   Analysis: {cycle.analysis[:60]}...")
            print(f"   Council Review: {cycle.council_review_status}")
            print(f"   Implementation: {cycle.implementation_status}")
            print(f"   Memory Updated: {'✅' if cycle.memory_updated else '⏳'}")
            if cycle.completed_at:
                print(f"   Completed: {cycle.completed_at.strftime('%Y-%m-%d')}")
        
        print(f"\n✓ Total Cycles: {len(cycles)}")
        active_cycles = sum(1 for c in cycles if not c.completed_at)
        print(f"✓ Active Cycles: {active_cycles}")
        
        # Summary Statistics
        print("\n\n" + "=" * 70)
        print("📊 EVOLUTION ENGINE SUMMARY")
        print("=" * 70)
        
        print(f"\n🛡️ BOUNDARIES:")
        print(f"   • Total: {len(boundaries)}")
        sacred_count = len(boundary_types.get("sacred", []))
        guarded_count = len(boundary_types.get("guarded", []))
        flexible_count = len(boundary_types.get("flexible", []))
        print(f"   • Sacred: {sacred_count} | Guarded: {guarded_count} | Flexible: {flexible_count}")
        
        print(f"\n📝 EVOLUTION:")
        print(f"   • {len(proposals)} improvement proposals")
        pending = sum(1 for p in proposals if "pending" in p.status)
        approved = sum(1 for p in proposals if p.status == "approved")
        implemented = sum(1 for p in proposals if p.status == "implemented")
        print(f"   • Pending: {pending} | Approved: {approved} | Implemented: {implemented}")
        
        print(f"\n👥 EXPANSION:")
        print(f"   • {len(agent_proposals)} new agent proposals")
        approved_agents = sum(1 for p in agent_proposals if p.status == "approved")
        print(f"   • Approved: {approved_agents}")
        
        print(f"\n🎨 ADAPTATION:")
        print(f"   • {len(techniques)} technique evolutions")
        approved_techniques = sum(1 for t in techniques if t.status == "approved")
        print(f"   • Approved: {approved_techniques}")
        
        print(f"\n🔄 CYCLES:")
        print(f"   • {len(cycles)} total cycles")
        print(f"   • {active_cycles} active")
        completed_cycles = len(cycles) - active_cycles
        print(f"   • {completed_cycles} completed")
        
        print("\n" + "=" * 70)
        print("🔥 The Dominion evolves with structure and governance.")
        print("👑 Adaptive intelligence within sovereign boundaries.")
        print("=" * 70 + "\n")
        
    finally:
        session.close()


if __name__ == "__main__":
    show_evolution_engine()
