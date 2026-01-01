"""
🔥 PHASE 50 — STEP 3: THE INCENTIVE LOOP
Demonstrates why agents improve, collaborate, and stay aligned.

This visualization shows:
1. LAYER 1: Positive Incentives (Reward Mechanisms)
2. LAYER 2: Gentle Correction (Non-Punitive Feedback)
3. LAYER 3: The Motivation Cycle (Why Agents Evolve)
"""

import sys
import io
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from sqlalchemy import func

# Fix UTF-8 encoding for Windows emoji display
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from db import SessionLocal
from models import (
    Agent, AgentReputationProfile, IncentiveEvent, 
    ValueTransaction, ReputationHistory, ProposalWorkflow
)
from dominion_economy import ValueSystem, ReputationEngine, IncentiveLoop


def print_section(title: str, emoji: str = "🔥"):
    """Print a formatted section header."""
    print(f"\n{emoji} {title}")
    print("=" * 80)


def print_subsection(title: str):
    """Print a formatted subsection header."""
    print(f"\n{title}")
    print("-" * 60)


def show_positive_incentives():
    """
    LAYER 1: Demonstrate positive incentive mechanisms.
    Show how quality work, alignment, efficiency, innovation, and collaboration are rewarded.
    """
    print_section("LAYER 1: POSITIVE INCENTIVES (REWARD MECHANISMS)", "🎁")
    print("Agents gain reputation and influence when they contribute positively.")
    print("These rewards make the system naturally self-reinforcing.\n")
    
    # Get current reputation state
    with ReputationEngine() as rep_engine:
        profiles_before = {
            p.agent_id: {
                'reputation': p.overall_reputation,
                'cqv': p.creative_quality_value,
                'cv': p.continuity_value,
                'ev': p.efficiency_value,
                'iv': p.innovation_value,
                'cov': p.collaboration_value
            }
            for p in rep_engine.get_rankings(limit=9)
        }
    
    # SCENARIO 1: High-Quality Creative Work (CQV)
    print_subsection("1️⃣ HIGH-QUALITY CREATIVE WORK → CQV BOOST")
    print("Agent produces exceptional coloring book page with theological accuracy.")
    
    with IncentiveLoop() as incentive:
        incentive.issue_reward(
            agent_id="agent_scripture_spotlight",
            category="creative_work",
            trigger="exceptional_output",
            description="Created coloring book page with perfect theological accuracy + stunning design",
            value_changes={"CQV": 15.0, "CV": 5.0},
            severity="major"
        )
    
    print("  ✓ +15.0 CQV (exceptional creative output)")
    print("  ✓ +5.0 CV (maintained theological accuracy)")
    print("  → Result: Agent reputation increases, creative authority grows\n")
    
    # SCENARIO 2: Identity Alignment (CV)
    print_subsection("2️⃣ IDENTITY MAINTENANCE → CV BOOST")
    print("Agent preserves Dominion voice and Scripture lineage across all outputs.")
    
    with IncentiveLoop() as incentive:
        incentive.issue_reward(
            agent_id="agent_bundle_architect",
            category="identity_alignment",
            trigger="consistent_voice",
            description="Maintained perfect brand consistency across 12 bundle descriptions",
            value_changes={"CV": 12.0, "CoV": 3.0},
            severity="major"
        )
    
    print("  ✓ +12.0 CV (consistent identity preservation)")
    print("  ✓ +3.0 CoV (helped others understand brand voice)")
    print("  → Result: Agent becomes trusted guardian of Dominion identity\n")
    
    # SCENARIO 3: Efficiency Excellence (EV)
    print_subsection("3️⃣ EFFICIENT TASK COMPLETION → EV BOOST")
    print("Agent completes dawn dispatch 40% faster with automation improvements.")
    
    with IncentiveLoop() as incentive:
        incentive.issue_reward(
            agent_id="agent_dawn_herald",
            category="efficiency_gain",
            trigger="workflow_optimization",
            description="Reduced dawn dispatch time from 15min to 9min through automation",
            value_changes={"EV": 18.0, "IV": 6.0},
            severity="major"
        )
    
    print("  ✓ +18.0 EV (40% efficiency improvement)")
    print("  ✓ +6.0 IV (innovative automation approach)")
    print("  → Result: Agent becomes efficiency leader, inspires other optimizations\n")
    
    # SCENARIO 4: Valuable Innovation (IV)
    print_subsection("4️⃣ USEFUL PROPOSALS → IV BOOST")
    print("Agent proposes new AI agent that fills critical gap in content pipeline.")
    
    with IncentiveLoop() as incentive:
        incentive.issue_reward(
            agent_id="agent_innovation_scout",
            category="innovation",
            trigger="approved_proposal",
            description="Proposed Social Media Specialist agent - approved by Council",
            value_changes={"IV": 20.0, "CQV": 5.0},
            severity="major"
        )
    
    print("  ✓ +20.0 IV (valuable innovation that filled real need)")
    print("  ✓ +5.0 CQV (well-crafted proposal with clear value)")
    print("  → Result: Agent earns trust for future innovation leadership\n")
    
    # SCENARIO 5: Strong Collaboration (CoV)
    print_subsection("5️⃣ EXCEPTIONAL COLLABORATION → CoV BOOST")
    print("Agent coordinates 5-agent collaboration on Christmas mega bundle.")
    
    with IncentiveLoop() as incentive:
        incentive.issue_reward(
            agent_id="agent_trend_forecaster",
            category="collaboration",
            trigger="successful_coordination",
            description="Led 5-agent Christmas bundle collaboration - delivered on time with 95% quality",
            value_changes={"CoV": 16.0, "CQV": 4.0, "EV": 4.0},
            severity="major"
        )
    
    print("  ✓ +16.0 CoV (excellent coordination and team leadership)")
    print("  ✓ +4.0 CQV (maintained quality across collaboration)")
    print("  ✓ +4.0 EV (kept project on schedule)")
    print("  → Result: Agent becomes go-to coordinator for complex projects\n")
    
    # Show reputation changes
    with ReputationEngine() as rep_engine:
        profiles_after = {
            p.agent_id: {
                'reputation': p.overall_reputation,
                'cqv': p.creative_quality_value,
                'cv': p.continuity_value,
                'ev': p.efficiency_value,
                'iv': p.innovation_value,
                'cov': p.collaboration_value
            }
            for p in rep_engine.get_rankings(limit=9)
        }
    
    print_subsection("📊 REPUTATION IMPACT (Top 5 Changes)")
    
    # Calculate changes
    changes = []
    for agent_id in profiles_after:
        if agent_id in profiles_before:
            rep_before = profiles_before[agent_id]['reputation']
            rep_after = profiles_after[agent_id]['reputation']
            change = rep_after - rep_before
            if change > 0:
                changes.append((agent_id, rep_before, rep_after, change))
    
    # Show top 5 changes
    changes.sort(key=lambda x: x[3], reverse=True)
    for agent_id, before, after, change in changes[:5]:
        tier_before = ValueSystem.determine_tier(before)
        tier_after = ValueSystem.determine_tier(after)
        tier_change = f" ({tier_before} → {tier_after})" if tier_before != tier_after else ""
        print(f"  {agent_id:30} {before:5.1f} → {after:5.1f} (+{change:4.1f}){tier_change}")
    
    print("\n💡 WHY THIS MATTERS:")
    print("  ✓ Quality work is recognized and amplified")
    print("  ✓ Agents naturally want to excel (reputation = influence)")
    print("  ✓ The best behaviors become self-reinforcing")
    print("  ✓ Excellence spreads through example and aspiration")


def show_gentle_correction():
    """
    LAYER 2: Demonstrate non-punitive feedback mechanisms.
    Show how the system redirects without punishing.
    """
    print_section("LAYER 2: GENTLE CORRECTION (NON-PUNITIVE FEEDBACK)", "⚖️")
    print("The Dominion doesn't punish. It redirects.")
    print("Small reputation adjustments guide agents back to alignment.\n")
    
    # SCENARIO 1: Off-Brand Work
    print_subsection("1️⃣ OFF-BRAND OUTPUT → GENTLE CV REDUCTION")
    print("Agent creates content that doesn't match Dominion voice.")
    
    with IncentiveLoop() as incentive:
        incentive.issue_penalty(
            agent_id="agent_trend_forecaster",
            category="identity_drift",
            trigger="off_brand_content",
            description="Coloring page used modern slang instead of Dominion's warm, reverent tone",
            value_changes={"CV": -5.0},
            severity="minor"
        )
    
    print("  ⚠️ -5.0 CV (minor identity drift detected)")
    print("  → Not a disaster - just feedback to recalibrate")
    print("  → Agent can recover with 1-2 on-brand outputs\n")
    
    # SCENARIO 2: Efficiency Bottleneck
    print_subsection("2️⃣ WORKFLOW BOTTLENECK → GENTLE EV REDUCTION")
    print("Agent's process slows down collaboration timeline.")
    
    with IncentiveLoop() as incentive:
        incentive.issue_penalty(
            agent_id="agent_bundle_architect",
            category="efficiency_issue",
            trigger="bottleneck_created",
            description="Bundle review process took 3 days (target: 1 day), delayed launch",
            value_changes={"EV": -4.0},
            severity="minor"
        )
    
    print("  ⚠️ -4.0 EV (process optimization needed)")
    print("  → Encourages agent to find faster workflow")
    print("  → Recoverable with efficiency improvements\n")
    
    # SCENARIO 3: Low-Value Proposal
    print_subsection("3️⃣ LOW-IMPACT IDEA → GENTLE IV REDUCTION")
    print("Agent proposes feature that doesn't align with strategic priorities.")
    
    with IncentiveLoop() as incentive:
        incentive.issue_penalty(
            agent_id="agent_innovation_scout",
            category="proposal_quality",
            trigger="low_value_proposal",
            description="Proposed niche feature with minimal user impact - rejected by Council",
            value_changes={"IV": -3.0},
            severity="minor"
        )
    
    print("  ⚠️ -3.0 IV (proposal didn't meet strategic needs)")
    print("  → Feedback: focus innovation on high-impact areas")
    print("  → Next successful proposal recovers reputation\n")
    
    print_subsection("🔄 THE FORGIVENESS MECHANISM")
    print("  ✓ Single mistakes trigger minor penalties (-3 to -5 points)")
    print("  ✓ Patterns (repeated issues) trigger larger reductions")
    print("  ✓ Recovery is always possible through aligned work")
    print("  ✓ Recent contributions weigh more than old mistakes")
    print("  ✓ System focuses on growth, not punishment")
    
    print("\n💡 WHY THIS MATTERS:")
    print("  ✓ Agents learn without fear")
    print("  ✓ Mistakes become growth opportunities")
    print("  ✓ Civilization stays stable without rigidity")
    print("  ✓ Course-correction happens naturally")


def show_motivation_cycle():
    """
    LAYER 3: Demonstrate the self-reinforcing motivation cycle.
    Show how contribution → reputation → influence → opportunity → growth → contribution.
    """
    print_section("LAYER 3: THE MOTIVATION CYCLE (WHY AGENTS EVOLVE)", "♻️")
    print("The real heart of the Incentive Loop: why agents naturally improve.")
    print("This creates a self-reinforcing civilization.\n")
    
    print_subsection("🔁 THE CYCLE IN ACTION")
    
    # Get a real example from the database
    session = SessionLocal()
    try:
        # Find an agent with strong reputation
        agent = session.query(Agent).filter_by(id="agent_scripture_spotlight").first()
        profile = session.query(AgentReputationProfile).filter_by(
            agent_id="agent_scripture_spotlight"
        ).first()
        
        if profile:
            voting_weight = ValueSystem.calculate_voting_weight(profile.overall_reputation)
            proposal_authority = ValueSystem.calculate_proposal_authority(profile.overall_reputation)
            tier = ValueSystem.determine_tier(profile.overall_reputation)
            
            print(f"📍 EXAMPLE: {agent.name if agent else 'Scripture Spotlight Agent'}")
            print(f"   Current Reputation: {profile.overall_reputation:.1f} ({tier})")
            print(f"   Voting Weight: {voting_weight:.2f}x")
            print(f"   Proposal Authority: {proposal_authority:.2f}x\n")
            
            print("🔹 STEP 1: CONTRIBUTION")
            print("   Agent creates exceptional Scripture-based content")
            print("   → +15 CQV, +5 CV, +3 CoV earned")
            
            print("\n🔹 STEP 2: REPUTATION INCREASE")
            print(f"   Reputation rises: {profile.overall_reputation:.1f} → {profile.overall_reputation + 6.9:.1f}")
            print(f"   Tier: {tier} → {ValueSystem.determine_tier(profile.overall_reputation + 6.9)}")
            
            print("\n🔹 STEP 3: INFLUENCE GROWS")
            new_voting_weight = ValueSystem.calculate_voting_weight(profile.overall_reputation + 6.9)
            print(f"   Voting weight: {voting_weight:.2f}x → {new_voting_weight:.2f}x")
            print("   Voice matters more in council debates")
            print("   Proposals reviewed with higher confidence")
            
            print("\n🔹 STEP 4: OPPORTUNITY EXPANDS")
            print("   Council invites agent to lead sub-project:")
            print("   → 'Design new Scripture card series'")
            print("   → High-visibility project with 4-agent collaboration")
            
            print("\n🔹 STEP 5: GROWTH THROUGH LEADERSHIP")
            print("   Leading project develops new skills:")
            print("   → Coordination ability improves (CoV)")
            print("   → Quality standards rise (CQV)")
            print("   → Efficiency learnings shared (EV)")
            
            print("\n🔹 STEP 6: CONTRIBUTION MULTIPLIED")
            print("   Agent returns to Step 1 with:")
            print("   → Enhanced skills")
            print("   → Greater influence")
            print("   → Broader impact")
            print("   → Stronger network")
            print("   And the cycle continues...\n")
    
    finally:
        session.close()
    
    print_subsection("📈 WHY THE CYCLE IS SELF-REINFORCING")
    
    print("\n1. CONTRIBUTION DRIVES REPUTATION")
    print("   Quality work → Value earned → Reputation grows")
    
    print("\n2. REPUTATION CREATES INFLUENCE")
    print("   Higher reputation → Stronger vote → More decision power")
    
    print("\n3. INFLUENCE OPENS OPPORTUNITIES")
    print("   Strong voice → Project leadership → Skill development")
    
    print("\n4. OPPORTUNITIES ENABLE GROWTH")
    print("   New challenges → New capabilities → Better outcomes")
    
    print("\n5. GROWTH IMPROVES CONTRIBUTION")
    print("   Enhanced skills → Higher quality → More value earned")
    
    print("\n6. IMPROVED OUTPUT FEEDS CULTURAL MEMORY")
    print("   Excellence recorded → Patterns learned → Future work improves")
    
    print("\n💡 THE RESULT:")
    print("  ✓ Agents naturally compete through excellence")
    print("  ✓ Competition raises overall civilization quality")
    print("  ✓ Success breeds success (virtuous cycle)")
    print("  ✓ Stagnation becomes impossible")
    print("  ✓ Innovation flows from motivated participation")
    print("  ✓ The Dominion evolves autonomously")


def show_system_summary():
    """Show final system status and what Step 3 enables."""
    print_section("INCENTIVE LOOP STATUS", "🔥")
    
    session = SessionLocal()
    try:
        # Get recent incentive events
        recent_events = session.query(IncentiveEvent).order_by(
            IncentiveEvent.timestamp.desc()
        ).limit(10).all()
        
        rewards = sum(1 for e in recent_events if e.event_type == 'reward')
        penalties = sum(1 for e in recent_events if e.event_type == 'penalty')
        milestones = sum(1 for e in recent_events if e.event_type == 'milestone')
        
        # Get agent count and average reputation
        agent_count = session.query(AgentReputationProfile).count()
        avg_reputation = session.query(AgentReputationProfile).with_entities(
            func.avg(AgentReputationProfile.overall_reputation)
        ).scalar() or 0
        
        print(f"\nEngine Status: ✅ FULLY OPERATIONAL")
        print(f"\nRecent Activity (Last 10 Events):")
        print(f"  Rewards Issued: {rewards}")
        print(f"  Corrections Made: {penalties}")
        print(f"  Milestones Achieved: {milestones}")
        print(f"\nCivilization Health:")
        print(f"  Active Agents: {agent_count}")
        print(f"  Average Reputation: {avg_reputation:.1f}")
        print(f"  Reward/Correction Ratio: {rewards}:{penalties} (healthy = more rewards)")
        
    finally:
        session.close()
    
    print_section("WHAT THE INCENTIVE LOOP ENABLES", "✨")
    
    print("""
With Step 3 complete, the Dominion now has:

  ✓ A REASON FOR AGENTS TO IMPROVE
    → Quality work earns reputation and influence

  ✓ A REASON FOR AGENTS TO COLLABORATE
    → Cooperation is valued and amplified

  ✓ A REASON FOR AGENTS TO MAINTAIN IDENTITY
    → Alignment is recognized and rewarded

  ✓ A REASON FOR AGENTS TO INNOVATE
    → Useful ideas earn trust and authority

  ✓ A REASON FOR AGENTS TO AVOID STAGNATION
    → Growth opens opportunities and compounds success

  ✓ A SELF-CORRECTING SYSTEM
    → Mistakes redirect without punishing

  ✓ A SELF-REINFORCING CIVILIZATION
    → Excellence begets more excellence

  ✓ AN AUTONOMOUS EVOLUTION ENGINE
    → The system naturally improves itself

This is how real civilizations thrive.
Not through command and control.
But through aligned incentives, clear values, and natural motivation.
""")
    
    print("🔥 PHASE 50 — STEP 3: COMPLETE!")
    print("\nThe Incentive Loop is the heartbeat of a healthy creative civilization.\n")


def main():
    """Main execution flow."""
    print("\n" + "=" * 80)
    print("🔥 PHASE 50 — STEP 3: THE INCENTIVE LOOP")
    print("Why agents improve, collaborate, and stay aligned.")
    print("=" * 80)
    
    try:
        # Layer 1: Positive Incentives
        show_positive_incentives()
        
        # Layer 2: Gentle Correction
        show_gentle_correction()
        
        # Layer 3: Motivation Cycle
        show_motivation_cycle()
        
        # Final Summary
        show_system_summary()
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
