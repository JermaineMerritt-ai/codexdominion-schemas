"""
🔥 REPUTATION ENGINE VISUALIZATION 🔥
Phase 50 - Step 2: How the Dominion tracks contribution, growth, and creative integrity

Displays:
1. Living reputation profiles for all agents
2. Strength/weakness detection
3. Voting weight distribution (influence)
4. Contribution patterns across 5 value streams
5. How reputation affects council decisions
6. Dynamic changes over time (history)
"""

import sys
import io
from datetime import datetime, timedelta
from db import SessionLocal
from models import (
    Agent, AgentReputationProfile, ValueTransaction, IncentiveEvent,
    ReputationHistory, ProposalWorkflow, Council
)
from dominion_economy import ValueSystem, ReputationEngine

# Fix emoji encoding on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_header(title: str):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"🔥 {title}")
    print("=" * 70)

def print_subheader(title: str):
    """Print subsection header"""
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}")

def show_reputation_profiles():
    """Display living reputation profiles for all agents"""
    print_header("STEP 2: THE REPUTATION ENGINE")
    print("How the Dominion tracks contribution, growth, and creative integrity.\n")
    
    with ReputationEngine() as rep_engine:
        session = rep_engine.session
        
        # Get all profiles, ordered by reputation
        profiles = rep_engine.get_rankings(limit=20)
        
        print_subheader("1. LIVING REPUTATION PROFILES")
        print("Every agent has a dynamic profile tracking their contribution patterns.\n")
        
        for i, profile in enumerate(profiles, 1):
            # Get tier emoji
            tier_emoji = {
                "emerging": "🌱",
                "established": "🌿",
                "respected": "🌳",
                "renowned": "👑",
                "legendary": "⭐"
            }.get(profile.reputation_tier, "❓")
            
            print(f"{i}. {tier_emoji} {profile.agent_id.upper()}")
            print(f"   Overall Reputation: {profile.overall_reputation:.1f}/100")
            print(f"   Tier: {profile.reputation_tier.title()}")
            print(f"   Voting Weight: {profile.voting_weight:.2f}x (influence in council debates)")
            print(f"   Proposal Authority: {profile.proposal_authority:.2f}x (how seriously proposals are taken)")
            
            # Show value streams
            print(f"\n   📊 VALUE STREAMS:")
            print(f"      CQV (Creative Quality):  {profile.creative_quality_value:6.1f} {'█' * int(profile.creative_quality_value/10)}")
            print(f"      CV  (Continuity):        {profile.continuity_value:6.1f} {'█' * int(profile.continuity_value/10)}")
            print(f"      EV  (Efficiency):        {profile.efficiency_value:6.1f} {'█' * int(profile.efficiency_value/10)}")
            print(f"      IV  (Innovation):        {profile.innovation_value:6.1f} {'█' * int(profile.innovation_value/10)}")
            print(f"      CoV (Collaboration):     {profile.collaboration_value:6.1f} {'█' * int(profile.collaboration_value/10)}")
            
            # Show strengths and weaknesses
            if profile.strengths:
                print(f"\n   💪 STRENGTHS: {', '.join(profile.strengths)}")
            if profile.weaknesses:
                print(f"   ⚠️  WEAKNESSES: {', '.join(profile.weaknesses)}")
            
            print()  # Blank line between agents

def show_influence_distribution():
    """Show how reputation affects influence in the civilization"""
    print_subheader("2. REPUTATION → INFLUENCE (NOT POWER)")
    print("Higher reputation = more influence in decisions, not hierarchical power.\n")
    
    with ReputationEngine() as rep_engine:
        profiles = rep_engine.get_rankings(limit=20)
        
        # Group by tier
        tiers = {}
        for profile in profiles:
            tier = profile.reputation_tier
            if tier not in tiers:
                tiers[tier] = []
            tiers[tier].append(profile)
        
        # Show tier-based influence
        tier_order = ["legendary", "renowned", "respected", "established", "emerging"]
        
        for tier in tier_order:
            if tier not in tiers:
                continue
            
            agents = tiers[tier]
            avg_weight = sum(p.voting_weight for p in agents) / len(agents)
            avg_authority = sum(p.proposal_authority for p in agents) / len(agents)
            
            tier_emoji = {
                "emerging": "🌱",
                "established": "🌿",
                "respected": "🌳",
                "renowned": "👑",
                "legendary": "⭐"
            }[tier]
            
            print(f"{tier_emoji} {tier.upper()} TIER ({len(agents)} agents)")
            print(f"   Average Voting Weight: {avg_weight:.2f}x")
            print(f"   Average Proposal Authority: {avg_authority:.2f}x")
            print(f"   What this means:")
            
            if tier == "legendary":
                print(f"      • Votes count for ~2x normal weight in council debates")
                print(f"      • Proposals taken very seriously by councils")
                print(f"      • Likely to lead major projects")
                print(f"      • Natural mentors for emerging agents")
            elif tier == "renowned":
                print(f"      • Votes count for ~1.6-1.8x weight in council debates")
                print(f"      • Proposals receive significant consideration")
                print(f"      • Trusted for complex creative decisions")
                print(f"      • Can lead sub-projects effectively")
            elif tier == "respected":
                print(f"      • Votes count for ~1.4-1.6x weight in council debates")
                print(f"      • Proposals reviewed with confidence")
                print(f"      • Solid contributors to collaborations")
                print(f"      • Growing influence in specialized areas")
            elif tier == "established":
                print(f"      • Votes count for ~1.0-1.3x weight in council debates")
                print(f"      • Proposals reviewed normally")
                print(f"      • Contributing regularly to projects")
                print(f"      • Building reputation through consistent work")
            elif tier == "emerging":
                print(f"      • Votes count for ~0.5-1.0x weight in council debates")
                print(f"      • Proposals reviewed cautiously")
                print(f"      • Learning through collaboration")
                print(f"      • Opportunity to grow through quality contributions")
            
            print()

def show_contribution_patterns():
    """Show how agents contribute across different value streams"""
    print_subheader("3. CONTRIBUTION PATTERNS ACROSS VALUE STREAMS")
    print("Each agent develops unique strengths and specializations.\n")
    
    with ReputationEngine() as rep_engine:
        profiles = rep_engine.get_rankings(limit=10)
        
        # Analyze top contributors in each value stream
        streams = {
            "CQV (Creative Quality)": ("creative_quality_value", []),
            "CV (Continuity)": ("continuity_value", []),
            "EV (Efficiency)": ("efficiency_value", []),
            "IV (Innovation)": ("innovation_value", []),
            "CoV (Collaboration)": ("collaboration_value", [])
        }
        
        # Populate streams
        for stream_name, (attr, agents) in streams.items():
            sorted_profiles = sorted(profiles, key=lambda p: getattr(p, attr), reverse=True)
            streams[stream_name] = (attr, sorted_profiles[:3])
        
        # Display top contributors per stream
        for stream_name, (attr, top_agents) in streams.items():
            print(f"🏆 {stream_name} — Top Contributors:")
            for i, profile in enumerate(top_agents, 1):
                value = getattr(profile, attr)
                bar = "█" * int(value/10)
                print(f"   {i}. {profile.agent_id:30s} {value:5.1f} {bar}")
            print()

def show_council_context():
    """Show how reputation provides context for council decisions"""
    print_subheader("4. REPUTATION AS COUNCIL CONTEXT")
    print("When councils review proposals, reputation adds informed context.\n")
    
    session = SessionLocal()
    try:
        # Get a sample proposal with reputation context
        proposals = session.query(ProposalWorkflow).limit(3).all()
        
        with ReputationEngine() as rep_engine:
            for proposal in proposals:
                if not proposal.originating_agent_id:
                    continue
                
                profile = rep_engine.get_profile(proposal.originating_agent_id)
                if not profile:
                    continue
                
                print(f"📋 Proposal: {proposal.title or proposal.proposal_type or 'Unknown'}")
                print(f"   Proposer: {proposal.originating_agent_id}")
                print(f"   Status: {proposal.review_status}")
                
                if proposal.assigned_council_id:
                    council = session.query(Council).filter_by(id=proposal.assigned_council_id).first()
                    if council:
                        print(f"   Reviewing Council: {council.name}")
                
                print(f"\n   PROPOSER'S REPUTATION CONTEXT:")
                print(f"      Overall Reputation: {profile.overall_reputation:.1f} ({profile.reputation_tier})")
                print(f"      Proposal Authority: {profile.proposal_authority:.2f}x")
                print(f"      Innovation Score: {profile.innovation_value:.1f}")
                print(f"      Continuity Score: {profile.continuity_value:.1f}")
                
                if profile.strengths:
                    print(f"      Known Strengths: {', '.join(profile.strengths)}")
                
                # Context interpretation
                print(f"\n   COUNCIL INTERPRETATION:")
                if profile.overall_reputation >= 75:
                    print(f"      ✅ High reputation - proposal taken very seriously")
                    print(f"      ✅ Track record suggests reliable judgment")
                elif profile.overall_reputation >= 60:
                    print(f"      ✓  Good reputation - proposal reviewed with confidence")
                    print(f"      ✓  Established contributor with proven results")
                else:
                    print(f"      ⚠️  Building reputation - proposal reviewed carefully")
                    print(f"      ⚠️  May benefit from mentor guidance")
                
                if profile.innovation_value >= 70:
                    print(f"      💡 Strong innovation history - new ideas welcome")
                
                if profile.continuity_value >= 70:
                    print(f"      🏛️ Strong identity alignment - trusted with cultural decisions")
                elif profile.continuity_value <= 30:
                    print(f"      ⚠️  Low continuity score - identity impact will be scrutinized")
                
                print()
    finally:
        session.close()

def show_reputation_dynamics():
    """Show how reputation changes over time"""
    print_subheader("5. DYNAMIC REPUTATION — GROWTH & RECOVERY")
    print("Reputation is not static - agents can grow, recover, and evolve.\n")
    
    with ReputationEngine() as rep_engine:
        session = rep_engine.session
        
        # Get recent value transactions to show dynamics
        recent_changes = session.query(ValueTransaction).order_by(
            ValueTransaction.timestamp.desc()
        ).limit(10).all()
        
        if recent_changes:
            print("📈 RECENT REPUTATION CHANGES:")
            for txn in recent_changes:
                direction = "↑" if txn.amount > 0 else "↓"
                color = "✅" if txn.amount > 0 else "⚠️"
                print(f"{color} {txn.agent_id}")
                print(f"   {direction} {txn.value_type}: {txn.amount:+.1f} points")
                print(f"   Reason: {txn.reason}")
                print(f"   When: {txn.timestamp.strftime('%Y-%m-%d %H:%M')}")
                print()
        
        print("KEY PRINCIPLES:")
        print("   • Agents can recover from mistakes through consistent quality work")
        print("   • Reputation grows through collaboration, innovation, and excellence")
        print("   • Recent activity weighs more than old history")
        print("   • No agent is permanently limited by past performance")
        print("   • The system encourages growth, not punishment")

def show_sovereign_override():
    """Show sovereign override capabilities"""
    print_subheader("6. SOVEREIGN OVERRIDE — JERMAINE'S AUTHORITY")
    print("The Reputation Engine serves your vision, not the other way around.\n")
    
    print("🔥 SOVEREIGN POWERS:")
    print("   ✓ Adjust any agent's reputation values")
    print("   ✓ Override voting weights for specific decisions")
    print("   ✓ Reset reputation profiles if needed")
    print("   ✓ Elevate agents to leadership roles regardless of reputation")
    print("   ✓ Demote agents if they drift from Dominion identity")
    print("   ✓ Create special reputation tiers or categories")
    print("   ✓ Pause reputation changes during major transitions")
    print("   ✓ Manually award bonuses for exceptional work")
    
    print("\n📋 OVERRIDE METHODS AVAILABLE:")
    print("   • reputation_engine.update_value(agent_id, value_type, change, reason)")
    print("   • Direct SQL updates to agent_reputation_profiles table")
    print("   • Manual incentive_event creation with custom values")
    print("   • Council vote weight overrides in proposal reviews")
    
    print("\n⚖️ BALANCED AUTONOMY:")
    print("   The engine operates autonomously day-to-day,")
    print("   but you always retain final authority.")
    print("   This keeps the Dominion:")
    print("      • Aligned with your vision")
    print("      • Autonomous in execution")
    print("      • Responsive to your guidance")
    print("      • Balanced between structure and flexibility")

def show_system_summary():
    """Show overall system status"""
    print_header("REPUTATION ENGINE STATUS: OPERATIONAL ✅")
    
    with ReputationEngine() as rep_engine:
        session = rep_engine.session
        
        # Count agents by tier
        profiles = rep_engine.get_rankings(limit=100)
        tier_counts = {}
        for profile in profiles:
            tier = profile.reputation_tier
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        
        print("\n📊 CIVILIZATION HEALTH:")
        print(f"   Total Agents: {len(profiles)}")
        print(f"   Average Reputation: {sum(p.overall_reputation for p in profiles) / len(profiles):.1f}")
        print(f"   Reputation Range: {min(p.overall_reputation for p in profiles):.1f} - {max(p.overall_reputation for p in profiles):.1f}")
        
        print("\n🏆 TIER DISTRIBUTION:")
        for tier in ["legendary", "renowned", "respected", "established", "emerging"]:
            count = tier_counts.get(tier, 0)
            emoji = {"legendary": "⭐", "renowned": "👑", "respected": "🌳", "established": "🌿", "emerging": "🌱"}[tier]
            bar = "█" * count
            print(f"   {emoji} {tier.title():12s}: {count:2d} {bar}")
        
        # Count recent activity
        transactions = session.query(ValueTransaction).count()
        incentives = session.query(IncentiveEvent).count()
        
        print("\n⚡ SYSTEM ACTIVITY:")
        print(f"   Total Value Transactions: {transactions}")
        print(f"   Total Incentive Events: {incentives}")
        print(f"   Engine Status: ✅ FULLY OPERATIONAL")
        
        print("\n🔥 WHAT THE REPUTATION ENGINE ENABLES:")
        print("   ✓ Living record of contribution")
        print("   ✓ Balanced influence system (not hierarchy)")
        print("   ✓ Encourages growth and recovery")
        print("   ✓ Maintains Dominion identity alignment")
        print("   ✓ Supports healthy collaboration")
        print("   ✓ Enables intelligent evolution")
        print("   ✓ Provides context for council decisions")
        print("   ✓ Remains aligned with sovereign vision")
        
        print("\n" + "=" * 70)
        print("🔥 PHASE 50 — STEP 2: COMPLETE!")
        print("The Reputation Engine is the backbone of a healthy creative civilization.")
        print("=" * 70)

if __name__ == "__main__":
    show_reputation_profiles()
    show_influence_distribution()
    show_contribution_patterns()
    show_council_context()
    show_reputation_dynamics()
    show_sovereign_override()
    show_system_summary()
