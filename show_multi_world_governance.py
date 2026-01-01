"""
🔥 DEMONSTRATION: MULTI-WORLD GOVERNANCE SYSTEM

This script demonstrates all 4 components of cosmic governance:
1. Cosmic Council of Worlds (CCW)
2. Inter-World Voting System (IWVS)
3. Inter-World Resolution Protocol (IWRP)
4. Cosmic Alignment Framework (CAF)

Shows how worlds collaborate, vote, resolve disputes, and maintain alignment.
"""

from multi_world_governance import (
    MultiWorldGovernanceSystem,
    ProposalType,
    DisputeType,
    RepresentativeRole
)
from db import SessionLocal
from multiworld_schema import World


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(f">> {title}")
    print("=" * 80)


def print_subsection(title: str):
    """Print a subsection header."""
    print(f"\n--- {title} ---")


def demo_component_1_cosmic_council():
    """
    COMPONENT 1: Cosmic Council of Worlds
    
    Shows:
    - Appointing representatives for each world
    - Council composition
    - Voting power distribution
    """
    print_section("COMPONENT 1 — COSMIC COUNCIL OF WORLDS (CCW)")
    
    governance = MultiWorldGovernanceSystem()
    session = SessionLocal()
    
    try:
        # Get all worlds
        worlds = session.query(World).all()
        
        print(f"\n[*] Found {len(worlds)} worlds in the cosmos")
        
        # Appoint representatives for each world
        print("\n[*] APPOINTING REPRESENTATIVES:")
        
        for world in worlds[:3]:  # Demo with first 3 worlds
            print(f"\n  World: {world.name}")
            
            # For demo purposes, appoint mock agents
            # In production, these would be actual top-performing agents from each world
            representatives = governance.ccw.appoint_representatives(
                world_id=world.id,
                creative_agent_id=f"agent_{world.id}_creative",
                continuity_agent_id=f"agent_{world.id}_continuity",
                operations_agent_id=f"agent_{world.id}_operations"
            )
            
            for rep in representatives:
                print(f"    • {rep.role.value.upper()}: Voting Weight = {rep.voting_weight:.2f}")
            
            total_power = governance.ccw.get_total_voting_power(world.id)
            print(f"    Total Voting Power: {total_power:.2f}")
        
        # Show council composition
        print("\n[*] COUNCIL COMPOSITION:")
        composition = governance.ccw.get_council_composition()
        print(f"  Total Representatives: {composition['total_representatives']}")
        print(f"  Worlds Represented: {composition['total_worlds_represented']}")
        print(f"  Average Voting Power per World: {composition['avg_voting_power_per_world']:.2f}")
        
        return governance
        
    finally:
        session.close()


def demo_component_2_voting_system(governance: MultiWorldGovernanceSystem):
    """
    COMPONENT 2: Inter-World Voting System
    
    Shows:
    - Creating proposals with different thresholds
    - Casting votes from multiple representatives
    - Tallying results
    - Determining outcomes
    """
    print_section("COMPONENT 2 — INTER-WORLD VOTING SYSTEM (IWVS)")
    
    # Scenario 1: Simple Majority Proposal (51%)
    print_subsection("Scenario 1: Routine Decision (Simple Majority)")
    
    proposal1 = governance.iwvs.create_proposal(
        title="Allocate Senior Agents to Easter Video Project",
        description="Send 3 senior video editors to support Easter Story Video Series",
        proposal_type=ProposalType.RESOURCE_ALLOCATION,
        proposed_by_world="dominion_prime",
        proposed_by_rep="rep_dominion_prime_operations"
    )
    
    print(f"  Proposal Created: {proposal1.title}")
    print(f"  Type: {proposal1.proposal_type.value}")
    print(f"  Threshold Required: {proposal1.threshold.value * 100}%")
    
    # Cast votes
    representatives = list(governance.ccw.representatives.values())[:6]
    
    votes_cast = [
        (representatives[0], "approve", "Good project alignment"),
        (representatives[1], "approve", "Resources available"),
        (representatives[2], "approve", "Will improve quality"),
        (representatives[3], "reject", "Need agents for our own projects"),
        (representatives[4], "abstain", "Neutral on this"),
        (representatives[5], "approve", "Strong support")
    ]
    
    print("\n  Votes Cast:")
    for rep, vote_value, reasoning in votes_cast:
        governance.iwvs.cast_vote(
            proposal_id=proposal1.proposal_id,
            representative_id=rep.representative_id,
            vote_value=vote_value,
            reasoning=reasoning
        )
        print(f"    • {rep.role.value}: {vote_value.upper()} - {reasoning}")
    
    # Tally results
    results1 = governance.iwvs.tally_votes(proposal1.proposal_id)
    print(f"\n  [*] RESULTS:")
    print(f"    Approval Rate: {results1['approval_rate'] * 100:.1f}%")
    print(f"    Threshold Required: {results1['threshold_required'] * 100:.1f}%")
    print(f"    Status: {results1['status'].upper()} [PASS]" if results1['threshold_met'] else f"    Status: {results1['status'].upper()} [FAIL]")
    
    # Scenario 2: Supermajority Proposal (66%)
    print_subsection("Scenario 2: Structural Change (Supermajority)")
    
    proposal2 = governance.iwvs.create_proposal(
        title="Create New World: Faith & Inspiration",
        description="Establish a new world focused on devotionals, sermons, and spiritual content",
        proposal_type=ProposalType.NEW_WORLD_CREATION,
        proposed_by_world="dominion_prime",
        proposed_by_rep="rep_dominion_prime_creative"
    )
    
    print(f"  Proposal Created: {proposal2.title}")
    print(f"  Type: {proposal2.proposal_type.value}")
    print(f"  Threshold Required: {proposal2.threshold.value * 100}%")
    
    # Cast votes (higher approval for expansion)
    votes_cast2 = [
        (representatives[0], "approve", "Excellent strategic expansion"),
        (representatives[1], "approve", "Fills market gap"),
        (representatives[2], "approve", "Strong demand signal"),
        (representatives[3], "approve", "Aligns with mission"),
        (representatives[4], "reject", "Too soon to expand"),
        (representatives[5], "approve", "Strongly support")
    ]
    
    print("\n  Votes Cast:")
    for rep, vote_value, reasoning in votes_cast2:
        governance.iwvs.cast_vote(
            proposal_id=proposal2.proposal_id,
            representative_id=rep.representative_id,
            vote_value=vote_value,
            reasoning=reasoning
        )
        print(f"    • {rep.role.value}: {vote_value.upper()} - {reasoning}")
    
    # Tally results
    results2 = governance.iwvs.tally_votes(proposal2.proposal_id)
    print(f"\n  [*] RESULTS:")
    print(f"    Approval Rate: {results2['approval_rate'] * 100:.1f}%")
    print(f"    Threshold Required: {results2['threshold_required'] * 100:.1f}%")
    print(f"    Status: {results2['status'].upper()} [PASS]" if results2['threshold_met'] else f"    Status: {results2['status'].upper()} [FAIL]")


def demo_component_3_resolution_protocol(governance: MultiWorldGovernanceSystem):
    """
    COMPONENT 3: Inter-World Resolution Protocol
    
    Shows:
    - Filing a dispute
    - Submitting arguments
    - Creating resolution proposal
    - Resolving via vote
    - Escalating to sovereign
    """
    print_section("COMPONENT 3 — INTER-WORLD RESOLUTION PROTOCOL (IWRP)")
    
    # Scenario 1: Resource Conflict (Resolved by Council)
    print_subsection("Scenario 1: Resource Conflict")
    
    dispute1 = governance.iwrp.file_dispute(
        dispute_type=DisputeType.RESOURCE_CONFLICT,
        world_a="world_childrens_stories",
        world_b="world_video_factory",
        description="Both worlds competing for the same senior motion graphics specialist for the Easter project",
        severity="medium"
    )
    
    print(f"  Dispute Filed: {dispute1.dispute_id}")
    print(f"  Type: {dispute1.dispute_type.value}")
    print(f"  Between: {dispute1.world_a} vs {dispute1.world_b}")
    print(f"  Severity: {dispute1.severity}")
    
    # Submit arguments
    print("\n  Arguments Submitted:")
    governance.iwrp.submit_argument(
        dispute_id=dispute1.dispute_id,
        world_id="world_childrens_stories",
        argument="We initiated the Easter project and requested this specialist first. Our timeline is critical for holiday delivery."
    )
    print(f"    • Children's Stories: Timeline priority, first request")
    
    governance.iwrp.submit_argument(
        dispute_id=dispute1.dispute_id,
        world_id="world_video_factory",
        argument="Our world specializes in video production at scale. The specialist will be more effective in our ecosystem with better tools."
    )
    print(f"    • Video Factory: Specialization advantage, better infrastructure")
    
    print(f"\n  Status: {dispute1.status.upper()} (Both arguments received)")
    
    # Council creates resolution proposal
    representatives = list(governance.ccw.representatives.values())
    
    resolution_proposal = governance.iwrp.create_resolution_proposal(
        dispute_id=dispute1.dispute_id,
        resolution_description="Assign specialist to Children's Stories for Easter project (30 days), then transfer to Video Factory for ongoing work",
        proposed_by_rep=representatives[0].representative_id
    )
    
    print(f"\n  Resolution Proposed: {resolution_proposal.description}")
    
    # Vote on resolution
    for rep in representatives[:4]:
        governance.iwvs.cast_vote(
            proposal_id=resolution_proposal.proposal_id,
            representative_id=rep.representative_id,
            vote_value="approve",
            reasoning="Fair compromise for both worlds"
        )
    
    results = governance.iwvs.tally_votes(resolution_proposal.proposal_id)
    
    if results['threshold_met']:
        governance.iwrp.resolve_dispute(
            dispute_id=dispute1.dispute_id,
            resolution=resolution_proposal.description,
            resolved_by="council_vote"
        )
        print(f"  [OK] Dispute Resolved by Council Vote ({results['approval_rate']*100:.0f}% approval)")
    
    # Scenario 2: Identity-Level Dispute (Escalate to Sovereign)
    print_subsection("Scenario 2: Identity Drift (Sovereign Escalation)")
    
    dispute2 = governance.iwrp.file_dispute(
        dispute_type=DisputeType.IDENTITY_DRIFT,
        world_a="dominion_prime",
        world_b="world_techniques_lab",
        description="Techniques Lab experimenting with edgy humor that conflicts with brand's family-friendly identity",
        severity="high"
    )
    
    print(f"  Dispute Filed: {dispute2.dispute_id}")
    print(f"  Type: {dispute2.dispute_type.value}")
    print(f"  Severity: {dispute2.severity.upper()}")
    
    # Escalate to sovereign because it affects core identity
    escalation = governance.iwrp.escalate_to_sovereign(
        dispute_id=dispute2.dispute_id,
        escalation_reason="Affects core brand identity and child-safety standards - requires sovereign decision"
    )
    
    print(f"\n  [!] ESCALATED TO SOVEREIGN AUTHORITY")
    print(f"    Reason: {escalation['reason']}")
    print(f"    Requires Decision: {escalation['requires_decision']}")
    print(f"    Status: {dispute2.status.upper()}")


def demo_component_4_alignment_framework(governance: MultiWorldGovernanceSystem):
    """
    COMPONENT 4: Cosmic Alignment Framework
    
    Shows:
    - Assessing world alignment across 3 pillars
    - Identifying drift
    - Generating recommendations
    - Maintaining cosmic coherence
    """
    print_section("COMPONENT 4 — COSMIC ALIGNMENT FRAMEWORK (CAF)")
    
    session = SessionLocal()
    
    try:
        worlds = session.query(World).limit(3).all()
        
        print("\n[*] ASSESSING COSMIC ALIGNMENT:")
        print("\nThree Pillars:")
        print("  1. Shared Identity - Core values and tone alignment")
        print("  2. Local Autonomy - Unique cultural identity")
        print("  3. Cosmic Harmony - Collaboration and contribution")
        
        for world in worlds:
            print(f"\n{'='*60}")
            print(f"World: {world.name}")
            print(f"{'='*60}")
            
            assessment = governance.caf.assess_world_alignment(world.id)
            
            scores = assessment['alignment_scores']
            print(f"\n  [*] ALIGNMENT SCORES:")
            print(f"    Shared Identity: {scores['shared_identity']:.1f}/100")
            print(f"    Local Autonomy: {scores['local_autonomy']:.1f}/100")
            print(f"    Cosmic Harmony: {scores['cosmic_harmony']:.1f}/100")
            print(f"    Overall: {scores['overall']:.1f}/100")
            
            # Status badge
            status = assessment['status']
            status_badge = {
                "excellent": "[**]",
                "good": "[OK]",
                "needs_improvement": "[!!]",
                "critical_drift": "[!!]"
            }
            print(f"\n  Status: {status_badge.get(status, '[-]')} {status.upper().replace('_', ' ')}")
            
            # Recommendations
            if assessment['recommendations']:
                print(f"\n  [!] RECOMMENDATIONS:")
                for rec in assessment['recommendations']:
                    print(f"    • {rec}")
        
        # Show cosmic coherence
        print(f"\n{'='*80}")
        print("[*] COSMIC COHERENCE STATUS")
        print(f"{'='*80}")
        
        # Calculate average alignment across all worlds
        all_worlds = session.query(World).all()
        total_alignment = 0
        
        for world in all_worlds:
            assessment = governance.caf.assess_world_alignment(world.id)
            total_alignment += assessment['alignment_scores']['overall']
        
        avg_alignment = total_alignment / len(all_worlds) if all_worlds else 0
        
        print(f"\n  Average Cosmic Alignment: {avg_alignment:.1f}/100")
        
        if avg_alignment >= 80:
            print("  Status: [**] EXCELLENT - Cosmos is unified and coherent")
        elif avg_alignment >= 60:
            print("  Status: [OK] GOOD - Cosmos is stable with healthy diversity")
        elif avg_alignment >= 40:
            print("  Status: [!!] NEEDS ATTENTION - Some worlds drifting")
        else:
            print("  Status: [!!] CRITICAL - Cosmos fragmentation risk")
        
    finally:
        session.close()


def main():
    """Run complete governance system demonstration."""
    
    print("\n" + "=" * 80)
    print("MULTI-WORLD GOVERNANCE SYSTEM DEMONSTRATION")
    print("Phase 60 - Step 3")
    print("=" * 80)
    
    print("\nThis system enables:")
    print("  * Democratic decision-making across worlds")
    print("  * Weighted voting with multiple thresholds")
    print("  * Structured dispute resolution")
    print("  * Cosmic alignment monitoring")
    print("  * Sovereign escalation for critical issues")
    
    try:
        # Component 1: Cosmic Council
        governance = demo_component_1_cosmic_council()
        
        # Component 2: Voting System
        demo_component_2_voting_system(governance)
        
        # Component 3: Resolution Protocol
        demo_component_3_resolution_protocol(governance)
        
        # Component 4: Alignment Framework
        demo_component_4_alignment_framework(governance)
        
        # Final Status
        print_section("GOVERNANCE SYSTEM STATUS")
        
        status = governance.get_governance_status()
        
        print(f"\n[OK] {status['governance_name']}")
        print(f"Status: {status['status'].upper()}")
        
        print(f"\n[*] Components:")
        for component, desc in status['components'].items():
            print(f"  • {component.upper()}: {desc}")
        
        print(f"\n[*] Statistics:")
        print(f"  Active Proposals: {status['active_proposals']}")
        print(f"  Active Disputes: {status['active_disputes']}")
        print(f"  Worlds Represented: {status['council_composition']['total_worlds_represented']}")
        print(f"  Total Representatives: {status['council_composition']['total_representatives']}")
        
        print("\n[*] Capabilities:")
        for capability in status['capabilities']:
            print(f"  + {capability}")
        
        print("\n" + "=" * 80)
        print("THE MULTI-WORLD GOVERNANCE SYSTEM IS OPERATIONAL")
        print("=" * 80)
        
        print("\nYour creative cosmos can now:")
        print("  * Make democratic decisions across worlds")
        print("  * Resolve disputes fairly and transparently")
        print("  * Maintain identity while honoring diversity")
        print("  * Scale without fragmentation")
        print("  * Balance power between worlds")
        print("  * Evolve while staying unified")
        print("  * Escalate critical decisions to you")
        
        print("\n" + "=" * 80)
        print("You are the Sovereign of a Governed Galaxy.")
        print("Your cosmos has democracy, law, and order.")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if 'governance' in locals():
            governance.close()


if __name__ == "__main__":
    main()
