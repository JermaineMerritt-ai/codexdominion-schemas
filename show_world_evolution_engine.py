"""
DEMONSTRATION: WORLD EVOLUTION ENGINE

This script demonstrates all 4 layers of world evolution:
1. Local Evolution Loops - Internal improvement cycles
2. World-Specific Agent Generation - Specialized agents per world
3. World-Level Style Evolution - Creative style adaptation
4. Cosmic Evolution Synchronization - Prevent drift/destabilization

Shows how worlds evolve independently while maintaining cosmic coherence.
"""

from world_evolution_engine import (
    WorldEvolutionEngine,
    CosmicEvolutionSynchronizer
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


def demo_layer_1_evolution_loops(engine: WorldEvolutionEngine):
    """
    LAYER 1: Local Evolution Loops
    
    Shows the 6-phase improvement cycle:
    1. Observation
    2. Analysis
    3. Proposal
    4. Review
    5. Implementation
    6. Memory Update
    """
    print_section("LAYER 1 - LOCAL EVOLUTION LOOPS")
    
    print("\nThe 6-Phase Improvement Cycle:")
    print("  1. OBSERVATION - Monitor patterns")
    print("  2. ANALYSIS - Identify opportunities")
    print("  3. PROPOSAL - Draft improvement")
    print("  4. REVIEW - Council debate and vote")
    print("  5. IMPLEMENTATION - Update workflows")
    print("  6. MEMORY UPDATE - Log the change")
    
    # Phase 1: Observation
    print_subsection("Phase 1: OBSERVATION")
    
    observations = []
    
    obs1 = engine.evolution_loop.phase_1_observe(
        observation_type="performance_metric",
        observation_data={
            "metric": "engagement_rate",
            "current_value": 0.72,
            "trend": "increasing",
            "sample_size": 1000
        },
        observed_by_agent="agent_wonder_scout"
    )
    observations.append(obs1)
    print(f"  [*] Observation 1: {obs1['observation_type']}")
    print(f"      Metric: {obs1['data']['metric']} = {obs1['data']['current_value']}")
    print(f"      Trend: {obs1['data']['trend']}")
    
    obs2 = engine.evolution_loop.phase_1_observe(
        observation_type="quality_feedback",
        observation_data={
            "source": "audience_reviews",
            "average_rating": 4.6,
            "common_praise": "Simple and clear moral lessons",
            "improvement_area": "Could use more visual variety"
        },
        observed_by_agent="agent_continuity_guardian"
    )
    observations.append(obs2)
    print(f"  [*] Observation 2: {obs2['observation_type']}")
    print(f"      Rating: {obs2['data']['average_rating']}/5.0")
    print(f"      Improvement: {obs2['data']['improvement_area']}")
    
    # Phase 2: Analysis
    print_subsection("Phase 2: ANALYSIS")
    
    analysis = engine.evolution_loop.phase_2_analyze(
        observations=observations,
        analyzed_by_agent="agent_wonder_scout"
    )
    
    # Add insights
    analysis["patterns_identified"].extend([
        "High engagement with simple narratives",
        "Audience desires more visual diversity"
    ])
    analysis["opportunities"].append("Expand illustration style variations while maintaining clarity")
    analysis["recommendations"].append("Introduce 3 new illustration styles for different story types")
    
    print(f"  [*] Patterns Identified: {len(analysis['patterns_identified'])}")
    for pattern in analysis['patterns_identified']:
        print(f"      - {pattern}")
    
    print(f"  [*] Opportunities: {len(analysis['opportunities'])}")
    for opp in analysis['opportunities']:
        print(f"      + {opp}")
    
    # Phase 3: Proposal
    print_subsection("Phase 3: PROPOSAL")
    
    proposal = engine.evolution_loop.phase_3_propose(
        title="Expand Illustration Style Library",
        description="Add 3 new illustration styles: Watercolor Dreams, Bold Shapes, Gentle Pencil. Maintain simple clarity while adding visual variety.",
        category="technique",
        observations=observations,
        analysis=analysis,
        proposed_by_agent="agent_wonder_scout",
        impact_scope="local",
        priority="medium"
    )
    
    print(f"  [*] Proposal Created: {proposal.title}")
    print(f"      Category: {proposal.category}")
    print(f"      Impact: {proposal.impact_scope}")
    print(f"      Priority: {proposal.priority}")
    print(f"      Status: {proposal.status}")
    
    # Phase 4: World Council Review
    print_subsection("Phase 4: WORLD COUNCIL REVIEW")
    
    council_votes = {
        "agent_creative_rep": "approve",
        "agent_continuity_rep": "approve",
        "agent_operations_rep": "approve"
    }
    
    approved, review_result = engine.evolution_loop.phase_4_review(
        proposal_id=proposal.proposal_id,
        council_votes=council_votes
    )
    
    print("  [*] Council Votes:")
    for agent, vote in council_votes.items():
        print(f"      - {agent.replace('agent_', '').replace('_', ' ').title()}: {vote.upper()}")
    
    print(f"\n  [*] Review Result:")
    print(f"      Approved: {approved}")
    print(f"      Votes - Approve: {review_result['approve']}, Reject: {review_result['reject']}")
    print(f"      Status: {review_result['status'].upper()}")
    
    # Phase 5: Implementation
    if approved:
        print_subsection("Phase 5: IMPLEMENTATION")
        
        impl_result = engine.evolution_loop.phase_5_implement(
            proposal_id=proposal.proposal_id,
            implementation_notes="Integrated 3 new illustration styles into workflow. Created style guides for each. Trained illustration agents on new techniques. Updated production templates."
        )
        
        print(f"  [OK] Proposal Implemented")
        print(f"      Category: {impl_result['category']}")
        print(f"      Implemented: {impl_result['implemented_at']}")
        print(f"      Notes: {impl_result['notes'][:100]}...")
        
        # Phase 6: Memory Update
        print_subsection("Phase 6: MEMORY UPDATE")
        
        engine.evolution_loop.phase_6_memory_update(
            proposal_id=proposal.proposal_id,
            memory_entry="Expanded illustration library with 3 new styles (Watercolor Dreams, Bold Shapes, Gentle Pencil) to increase visual variety while maintaining clarity and simplicity that defines Children's Story World aesthetic."
        )
        
        print("  [OK] Cultural Memory Updated")
        print("      Change logged in world's evolution history")
        print("      Lineage maintained: Simple clarity + Visual variety")


def demo_layer_2_agent_generation(engine: WorldEvolutionEngine):
    """
    LAYER 2: World-Specific Agent Generation
    
    Shows how worlds create specialized agents.
    """
    print_section("LAYER 2 - WORLD-SPECIFIC AGENT GENERATION")
    
    print("\nWorld-specific roles enable deeper specialization:")
    
    # Template 1: Emotion-Clarity Specialist
    print_subsection("Agent Role 1: Emotion-Clarity Specialist")
    
    template1 = engine.agent_generator.create_agent_template(
        role_name="Emotion-Clarity Specialist",
        role_description="Ensures emotional arcs are simple, clear, and age-appropriate for children",
        specialization="emotional_storytelling",
        base_reputation=55.0,
        initial_capabilities=[
            "emotion_identification",
            "age_appropriate_emotional_pacing",
            "clarity_validation"
        ]
    )
    
    print(f"  [*] Template Created: {template1.role_name}")
    print(f"      Specialization: {template1.specialization}")
    print(f"      Base Reputation: {template1.base_reputation}")
    print(f"      Capabilities: {len(template1.initial_capabilities)}")
    for cap in template1.initial_capabilities:
        print(f"        - {cap}")
    
    # Generate agent from template
    agent1, world_agent1 = engine.agent_generator.generate_agent_from_template(
        template_id=template1.template_id,
        agent_name="Emotional Journey Guide Emma"
    )
    
    print(f"\n  [OK] Agent Generated: {agent1.name}")
    print(f"      Agent ID: {agent1.id}")
    print(f"      Role: {agent1.capabilities.get('role', 'N/A')}")
    print(f"      Status: {'active' if agent1.is_active else 'inactive'}")
    print(f"      Citizenship: {world_agent1.citizenship_status}")
    
    # Template 2: Moral-Arc Advisor
    print_subsection("Agent Role 2: Moral-Arc Advisor")
    
    template2 = engine.agent_generator.create_agent_template(
        role_name="Moral-Arc Advisor",
        role_description="Crafts gentle moral lessons that feel natural within the story",
        specialization="moral_storytelling",
        base_reputation=58.0,
        initial_capabilities=[
            "moral_lesson_integration",
            "subtlety_balance",
            "values_alignment"
        ]
    )
    
    print(f"  [*] Template Created: {template2.role_name}")
    print(f"      Specialization: {template2.specialization}")
    
    agent2, world_agent2 = engine.agent_generator.generate_agent_from_template(
        template_id=template2.template_id,
        agent_name="Gentle Wisdom Weaver Walter"
    )
    
    print(f"\n  [OK] Agent Generated: {agent2.name}")
    print(f"      Agent ID: {agent2.id}")
    
    # Population growth statistics
    print_subsection("Population Growth Statistics")
    
    growth_stats = engine.agent_generator.get_world_population_growth()
    
    print(f"  [*] World: {growth_stats['world_name']}")
    print(f"      Total Population: {growth_stats['total_population']}")
    print(f"      Founding Citizens: {growth_stats['founding_citizens']}")
    print(f"      Generated Agents: {growth_stats['generated_agents']}")
    print(f"      Growth Rate: {growth_stats['growth_rate']:.1f}%")
    print(f"      Templates Created: {growth_stats['templates_created']}")


def demo_layer_3_style_evolution(engine: WorldEvolutionEngine):
    """
    LAYER 3: World-Level Style Evolution
    
    Shows how worlds evolve their creative style.
    """
    print_section("LAYER 3 - WORLD-LEVEL STYLE EVOLUTION")
    
    print("\nWorlds can evolve style aspects organically:")
    
    # Style Evolution 1: Color Palette
    print_subsection("Style Evolution 1: Color Palette Refinement")
    
    style_proposal1 = engine.style_evolution.propose_style_evolution(
        style_aspect="color_palette",
        current_value=["bright_primary", "high_saturation"],
        proposed_value=["soft_pastels", "gentle_saturation", "warm_undertones"],
        rationale="Audience feedback shows preference for calmer, warmer tones that still feel playful but less overwhelming",
        proposed_by_agent="agent_imagination_illustrator"
    )
    
    print(f"  [*] Proposal: {style_proposal1.style_aspect}")
    print(f"      Current: {style_proposal1.current_value}")
    print(f"      Proposed: {style_proposal1.proposed_value}")
    print(f"      Rationale: {style_proposal1.rationale}")
    
    # Simulate voting
    engine.style_evolution.vote_on_style_proposal(style_proposal1.style_proposal_id, "approve")
    engine.style_evolution.vote_on_style_proposal(style_proposal1.style_proposal_id, "approve")
    engine.style_evolution.vote_on_style_proposal(style_proposal1.style_proposal_id, "approve")
    
    print(f"\n  [*] Votes: {style_proposal1.approval_votes} approve, {style_proposal1.rejection_votes} reject")
    
    # Apply style evolution
    result1 = engine.style_evolution.apply_style_evolution(style_proposal1.style_proposal_id)
    
    if result1["status"] == "applied":
        print(f"  [OK] Style Evolution Applied")
        print(f"      Approval Rate: {result1['approval_rate']*100:.0f}%")
        print(f"      Status: {style_proposal1.status.upper()}")
    
    # Style Evolution 2: Narrative Pacing
    print_subsection("Style Evolution 2: Narrative Pacing")
    
    style_proposal2 = engine.style_evolution.propose_style_evolution(
        style_aspect="narrative_pacing",
        current_value={"tempo": "moderate", "scene_length": "medium"},
        proposed_value={"tempo": "gentle", "scene_length": "slightly_shorter", "transition_softness": "increased"},
        rationale="Shorter scenes with softer transitions better match children's attention spans while maintaining story flow",
        proposed_by_agent="agent_narrative_weaver"
    )
    
    print(f"  [*] Proposal: {style_proposal2.style_aspect}")
    print(f"      Current: {style_proposal2.current_value}")
    print(f"      Proposed: {style_proposal2.proposed_value}")
    
    # Simulate voting
    engine.style_evolution.vote_on_style_proposal(style_proposal2.style_proposal_id, "approve")
    engine.style_evolution.vote_on_style_proposal(style_proposal2.style_proposal_id, "approve")
    
    result2 = engine.style_evolution.apply_style_evolution(style_proposal2.style_proposal_id)
    
    if result2["status"] == "applied":
        print(f"\n  [OK] Style Evolution Applied")
        print(f"      Status: {style_proposal2.status.upper()}")
    
    # Show evolution history
    print_subsection("Style Evolution History")
    
    history = engine.style_evolution.get_style_evolution_history()
    print(f"  [*] Total Style Changes: {len(history)}")
    for i, record in enumerate(history[-3:], 1):  # Show last 3
        print(f"      {i}. {record['aspect']}: {record['from']} -> {record['to']}")


def demo_layer_4_cosmic_sync(engine: WorldEvolutionEngine):
    """
    LAYER 4: Cosmic Evolution Synchronization
    
    Shows safeguards and network synchronization.
    """
    print_section("LAYER 4 - COSMIC EVOLUTION SYNCHRONIZATION")
    
    print("\nSafeguards maintain cosmic coherence:")
    
    # Drift Detection
    print_subsection("Drift Detection")
    
    drift_report = engine.synchronizer.detect_world_drift(engine.world_id)
    
    print(f"  [*] World: {drift_report['world_name']}")
    print(f"      Drift Detected: {drift_report['drift_detected']}")
    print(f"      Severity: {drift_report['severity'].upper()}")
    
    if drift_report['drift_factors']:
        print(f"\n  [!] Drift Factors:")
        for factor in drift_report['drift_factors']:
            print(f"      - {factor}")
        
        print(f"\n  [!] Recommendations:")
        for rec in drift_report['recommendations']:
            print(f"      + {rec}")
    else:
        print(f"      Status: [OK] No drift detected - world aligned")
    
    print(f"\n      Requires Intervention: {drift_report['requires_intervention']}")
    
    # Cosmic-Wide Evolution Status
    print_subsection("Cosmic Evolution Status")
    
    cosmic_status = engine.synchronizer.get_cosmic_evolution_status()
    
    print(f"  [*] Total Worlds: {cosmic_status['total_worlds']}")
    print(f"      Actively Evolving: {cosmic_status['worlds_evolving']}")
    print(f"      Total Evolutions: {cosmic_status['total_evolutions']}")
    print(f"      Average per World: {cosmic_status['avg_evolutions_per_world']:.1f}")
    print(f"\n  [*] Drift Analysis:")
    print(f"      Worlds Drifting: {cosmic_status['worlds_drifting']}")
    print(f"      Drift Percentage: {cosmic_status['drift_percentage']:.1f}%")
    print(f"      Cosmic Health: {cosmic_status['cosmic_health'].upper()}")
    
    # Evolution Synchronization
    print_subsection("Network Synchronization")
    
    print("  [*] Broadcasting evolution to Inter-World Network...")
    
    evolution_data = {
        "title": "Expanded Illustration Style Library",
        "category": "technique",
        "effectiveness": 85.0,
        "description": "3 new illustration styles successfully integrated"
    }
    
    engine.synchronizer.synchronize_evolution_to_network(
        world_id=engine.world_id,
        evolution_type="innovation",
        evolution_data=evolution_data
    )
    
    print(f"      [OK] Evolution broadcast complete")
    print(f"      Type: {evolution_data['category']}")
    print(f"      Effectiveness: {evolution_data['effectiveness']}%")
    print(f"      Available to all connected worlds")


def main():
    """Run complete World Evolution Engine demonstration."""
    
    print("\n" + "=" * 80)
    print("WORLD EVOLUTION ENGINE DEMONSTRATION")
    print("Phase 60 - Step 4")
    print("=" * 80)
    
    print("\nThis system enables:")
    print("  * Worlds to evolve independently")
    print("  * Internal improvement cycles")
    print("  * Specialized agent generation")
    print("  * Creative style adaptation")
    print("  * Cosmic coherence safeguards")
    
    session = SessionLocal()
    
    try:
        # Get Children's Story World
        world = session.query(World).filter_by(name="The Children's Story World").first()
        
        if not world:
            print("\n[ERROR] Children's Story World not found")
            print("Run world_genesis_protocol.py first to create worlds")
            return
        
        print(f"\n[*] Selected World: {world.name}")
        print(f"    World ID: {world.id}")
        print(f"    Type: {world.world_type}")
        print(f"    Population: {world.population}")
        
        # Initialize Evolution Engine
        engine = WorldEvolutionEngine(world.id)
        
        # Demo Layer 1: Evolution Loops
        demo_layer_1_evolution_loops(engine)
        
        # Demo Layer 2: Agent Generation
        demo_layer_2_agent_generation(engine)
        
        # Demo Layer 3: Style Evolution
        demo_layer_3_style_evolution(engine)
        
        # Demo Layer 4: Cosmic Sync
        demo_layer_4_cosmic_sync(engine)
        
        # Final Status
        print_section("WORLD EVOLUTION ENGINE STATUS")
        
        status = engine.get_evolution_status()
        
        print(f"\n[OK] World: {status['world_id']}")
        print(f"Status: {status['evolution_engine_status'].upper()}")
        
        print("\n[*] Layer Status:")
        layers = status['layers']
        
        print(f"  1. Local Evolution Loops:")
        print(f"     - Active Proposals: {layers['local_evolution_loops']['active_proposals']}")
        print(f"     - Implemented: {layers['local_evolution_loops']['implemented_proposals']}")
        print(f"     - Total Cycles: {layers['local_evolution_loops']['total_cycles']}")
        
        print(f"\n  2. Agent Generation:")
        print(f"     - Total Population: {layers['agent_generation']['total_population']}")
        print(f"     - Generated Agents: {layers['agent_generation']['generated_agents']}")
        print(f"     - Templates: {layers['agent_generation']['templates_created']}")
        
        print(f"\n  3. Style Evolution:")
        print(f"     - Style Changes: {layers['style_evolution']['style_changes']}")
        print(f"     - Active Proposals: {layers['style_evolution']['active_proposals']}")
        
        print(f"\n  4. Cosmic Synchronization:")
        print(f"     - Drift Detected: {layers['cosmic_sync']['drift_detected']}")
        print(f"     - Severity: {layers['cosmic_sync']['drift_severity']}")
        print(f"     - Intervention Required: {layers['cosmic_sync']['requires_intervention']}")
        
        print("\n[*] Capabilities:")
        for capability in status['capabilities']:
            print(f"  + {capability}")
        
        print("\n" + "=" * 80)
        print("THE WORLD EVOLUTION ENGINE IS OPERATIONAL")
        print("=" * 80)
        
        print("\nThis world can now:")
        print("  * Evolve through internal improvement cycles")
        print("  * Generate specialized agents tailored to its purpose")
        print("  * Adapt its creative style based on experience")
        print("  * Stay synchronized with cosmic standards")
        print("  * Grow without losing its identity")
        print("  * Innovate while maintaining coherence")
        
        print("\n" + "=" * 80)
        print("Your cosmos is now SELF-EVOLVING.")
        print("Worlds have their own life cycles.")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        session.close()
        if 'engine' in locals():
            engine.close()


if __name__ == "__main__":
    main()
