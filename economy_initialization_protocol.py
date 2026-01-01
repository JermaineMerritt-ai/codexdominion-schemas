"""
Dominion Economy Initialization Protocol
Phase 50 - Step 1: Value System Blueprint

Populates the economy with realistic sample data demonstrating:
- 5 value types in action (CQV, CV, EV, IV, CoV)
- Reputation profiles for all 9 agents
- Value transactions from real work
- Incentive events (rewards and penalties)
- Reputation history snapshots
- Economy health metrics

Real Scenarios:
1. Advent Devotional collaboration → CQV + CoV distribution
2. Scripture Agent proposal → IV + EV rewards
3. Minimalist technique → IV recognition
4. TikTok Strategy debate → CoV earned through collaboration
5. Identity alignment checks → CV rewards/penalties
"""

import sys
import io
from datetime import datetime, timedelta
from db import SessionLocal
from dominion_economy import (
    ValueSystem,
    ReputationEngine,
    IncentiveLoop,
    DistributionSystem
)

# Fix emoji encoding on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def initialize_economy():
    """Initialize the Dominion Economy with realistic sample data"""
    
    print("🔥 PHASE 50 — STEP 1: VALUE SYSTEM BLUEPRINT")
    print("=" * 60)
    
    # Use context managers for economy systems
    with ReputationEngine() as reputation_engine:
        with IncentiveLoop() as incentive_loop:
            with DistributionSystem() as distribution:
                session = reputation_engine.session
                
                # 1. Initialize reputation profiles for all 9 agents
                print("\n📊 1. INITIALIZING AGENT REPUTATION PROFILES...")
                
                agents = [
                    "agent_jermaine",
                    "agent_scripture_spotlight",
                    "agent_joyful_wonder",
                    "agent_bundle_architect",
                    "agent_innovation_scout",
                    "agent_trend_forecaster",
                    "agent_customer_voice",
                    "agent_analytics_sage",
                    "agent_dawn_herald"
                ]
                
                for agent_id in agents:
                    profile = reputation_engine.get_or_create_profile(agent_id)
                    print(f"   ✓ {agent_id} — Tier: {profile.reputation_tier} (0 CQV, 0 CV, 0 EV, 0 IV, 0 CoV)")
                
                # 2. Distribute value from Advent Devotional collaboration (completed)
                print("\n🎄 2. ADVENT DEVOTIONAL SERIES (Completed Collaboration)")
                print("   Agents: Jermaine, Scripture Spotlight, Joyful Wonder, Bundle Architect")
                
                # High creative quality (95%) and strong collaboration (4 agents)
                # CQV: 28.5 points (95% * 30), CoV: 14.25 points (95% * 15)
                for agent_id in ["agent_jermaine", "agent_scripture_spotlight", "agent_joyful_wonder", "agent_bundle_architect"]:
                    incentive_loop.issue_reward(
                        agent_id=agent_id,
                        category="collaboration",
                        trigger="Advent Devotional Series completed",
                        description="25 Bible stories with reflection questions - excellent quality",
                        value_changes={"CQV": 28.5, "CoV": 14.25},
                        severity="major"
                    )
                print("   ✓ Distributed CQV (28.5 pts) + CoV (14.25 pts) to 4 agents")
                
                # 3. Scripture Agent proposal approval - innovation reward
                print("\n📜 3. SCRIPTURE SELECTOR AGENT PROPOSAL (Approved)")
                print("   Proposer: Innovation Scout")
                
                # Award innovation value for new agent proposal
                # IV: 22.5 points (high innovation impact)
                incentive_loop.issue_reward(
                    agent_id="agent_innovation_scout",
                    category="innovation",
                    trigger="New agent proposal approved",
                    description="Scripture Selector Agent - approved by Council of Continuity",
                    value_changes={"IV": 22.5},
                    severity="major"
                )
                print("   ✓ Rewarded +22.5 IV (new agent proposal)")
                
                # Also reward efficiency for clear proposal
                # EV: 11.25 points (clear documentation)
                incentive_loop.issue_reward(
                    agent_id="agent_innovation_scout",
                    category="efficiency",
                    trigger="Well-structured proposal",
                    description="Clear implementation plan and requirements documentation",
                    value_changes={"EV": 11.25},
                    severity="moderate"
                )
                print("   ✓ Rewarded +11.25 EV (clear proposal structure)")
                
                # 4. Minimalist technique implementation - innovation recognition
                print("\n🎨 4. MINIMALIST COLORING TECHNIQUE (Implemented)")
                print("   Proposer: Trend Forecaster")
                
                # Major milestone: successful evolution implementation
                # IV: 22.5 points (major innovation), CQV: 15 points (improved quality)
                incentive_loop.issue_milestone(
                    agent_id="agent_trend_forecaster",
                    category="evolution",
                    trigger="Evolution technique adopted system-wide",
                    description="Minimalist coloring technique improved visual clarity across all products",
                    value_changes={"IV": 22.5, "CQV": 15.0}
                )
                print("   ✓ Milestone reward: +22.5 IV + 15 CQV (successful innovation)")
                
                # 5. TikTok Strategy collaboration - active debate (collaboration value)
                print("\n📱 5. TIKTOK STRATEGY RESEARCH (Active)")
                print("   Agents: Trend Forecaster, Customer Voice, Analytics Sage")
                
                # Good progress (75%), 3-agent collaboration
                # CQV: 22.5 points (75% * 30), CoV: 11.25 points (75% * 15)
                for agent_id in ["agent_trend_forecaster", "agent_customer_voice", "agent_analytics_sage"]:
                    incentive_loop.issue_reward(
                        agent_id=agent_id,
                        category="collaboration",
                        trigger="TikTok Strategy Research (in progress)",
                        description="Researching short-form vs depth - debate ongoing",
                        value_changes={"CQV": 22.5, "CoV": 11.25},
                        severity="moderate"
                    )
                print("   ✓ Distributed CQV (22.5 pts) + CoV (11.25 pts) to 3 agents")
                
                # 6. Identity alignment checks - continuity rewards/penalties
                print("\n🏛️ 6. IDENTITY ALIGNMENT CHECKS")
                
                # Reward for strong identity alignment (95%)
                # CV: 23.75 points (95% * 25)
                incentive_loop.issue_reward(
                    agent_id="agent_scripture_spotlight",
                    category="identity_alignment",
                    trigger="Perfect identity alignment",
                    description="Scripture selections perfectly align with Dominion values",
                    value_changes={"CV": 23.75},
                    severity="moderate"
                )
                print("   ✓ Scripture Spotlight: +23.75 CV (95% identity alignment)")
                
                # Minor penalty for weak alignment (70%)
                # CV: -7.5 points (30% gap * 25)
                incentive_loop.issue_penalty(
                    agent_id="agent_trend_forecaster",
                    category="identity_misalignment",
                    trigger="Potential identity compromise",
                    description="TikTok strategy may sacrifice depth for virality",
                    value_changes={"CV": -7.5},
                    severity="minor"
                )
                print("   ⚠️  Trend Forecaster: -7.5 CV (caution on depth vs virality)")
                
                # 7. Efficiency rewards for fast work
                print("\n⚡ 7. EFFICIENCY RECOGNITION")
        
                # Dawn Herald: 4x faster (75% time saved)
                # EV: 11.25 points (75% * 15)
                incentive_loop.issue_reward(
                    agent_id="agent_dawn_herald",
                    category="efficiency",
                    trigger="Exceptional speed with quality",
                    description="Dawn dispatch in 30 min (expected 2 hours) - quality maintained",
                    value_changes={"EV": 11.25},
                    severity="moderate"
                )
                print("   ✓ Dawn Herald: +11.25 EV (4x faster with quality)")
                
                # Bundle Architect: 25% faster
                # EV: 3.75 points (25% * 15)
                incentive_loop.issue_reward(
                    agent_id="agent_bundle_architect",
                    category="efficiency",
                    trigger="Above-average efficiency",
                    description="Bundle optimization in 6 hours (expected 8) - quality maintained",
                    value_changes={"EV": 3.75},
                    severity="minor"
                )
                print("   ✓ Bundle Architect: +3.75 EV (25% faster with quality)")
                
                # 8. Display final reputation standings
                print("\n" + "=" * 60)
                print("🏆 FINAL REPUTATION STANDINGS")
                print("=" * 60)
                
                rankings = reputation_engine.get_rankings(limit=10)
                for i, profile in enumerate(rankings[:5], 1):
                    print(f"\n{i}. {profile.agent_id.upper()}")
                    print(f"   Overall Reputation: {profile.overall_reputation:.1f}")
                    print(f"   Tier: {profile.reputation_tier}")
                    print(f"   Voting Weight: {profile.voting_weight:.2f}")
                    print(f"   CQV: {profile.creative_quality_value:.1f} | CV: {profile.continuity_value:.1f}")
                    print(f"   EV: {profile.efficiency_value:.1f} | IV: {profile.innovation_value:.1f} | CoV: {profile.collaboration_value:.1f}")
                    
                    if profile.strengths:
                        print(f"   💪 Strengths: {', '.join(profile.strengths)}")
                # 9. Capture economy metrics
                print("\n" + "=" * 60)
                print("📈 ECONOMY HEALTH METRICS")
                print("=" * 60)
                
                from models import EconomyMetrics, AgentReputationProfile
                
                # Calculate metrics
                profiles = session.query(AgentReputationProfile).all()
                total_reps = [p.overall_reputation for p in profiles]
                avg_reputation = sum(total_reps) / len(total_reps) if total_reps else 0
                
                # Gini coefficient (simple approximation)
                sorted_reps = sorted(total_reps)
                n = len(sorted_reps)
                gini = (2 * sum((i+1) * rep for i, rep in enumerate(sorted_reps))) / (n * sum(sorted_reps)) - (n+1)/n if sorted_reps and sum(sorted_reps) > 0 else 0
        
                # Tier distribution
                tier_counts = {
                    "emerging": 0,
                    "established": 0,
                    "respected": 0,
                    "renowned": 0,
                    "legendary": 0
                }
                for p in profiles:
                    tier_counts[p.reputation_tier] = tier_counts.get(p.reputation_tier, 0) + 1
                
                metrics = EconomyMetrics(
                    id=f"metrics_{datetime.utcnow().strftime('%Y%m%d')}",
                    metric_date=datetime.utcnow(),
                    total_value_in_circulation=sum(total_reps),
                    average_agent_reputation=avg_reputation,
                    reputation_inequality=gini,
                    transactions_today=7,
                    emerging_agents=tier_counts["emerging"],
                    established_agents=tier_counts["established"],
                    respected_agents=tier_counts["respected"],
                    renowned_agents=tier_counts["renowned"],
                    legendary_agents=tier_counts["legendary"]
                )
                session.add(metrics)
                session.commit()
                
                print(f"   Total Agents: {len(profiles)}")
                print(f"   Average Reputation: {metrics.average_agent_reputation:.1f}")
                print(f"   Inequality (Gini): {metrics.reputation_inequality:.3f}")
                print(f"   Transactions Today: {metrics.transactions_today}")
                print(f"   Total Value: {metrics.total_value_in_circulation:.1f}")
                print(f"   Tier Distribution: Emerging={tier_counts['emerging']}, Established={tier_counts['established']}, Respected={tier_counts['respected']}, Renowned={tier_counts['renowned']}, Legendary={tier_counts['legendary']}")
                
                print("\n" + "=" * 60)
                print("🔥 THE VALUE SYSTEM BLUEPRINT IS OPERATIONAL!")
                print("=" * 60)
                print("\nWhat the Dominion measures:")
                print("  ✓ Creative Quality (CQV) — Advent devotionals earned 95%")
                print("  ✓ Continuity (CV) — Scripture Spotlight 95% identity alignment")
                print("  ✓ Efficiency (EV) — Dawn Herald 4x faster with quality")
                print("  ✓ Innovation (IV) — 2 proposals, 1 technique milestone")
                print("  ✓ Collaboration (CoV) — 7 agents working together")
                print("\nThe Dominion rewards:")
                print("  ✓ Excellence — High quality work earns CQV")
                print("  ✓ Identity — Alignment with sacred principles earns CV")
                print("  ✓ Speed — Fast, quality work earns EV")
                print("  ✓ Evolution — New ideas earn IV")
                print("  ✓ Teamwork — Collaboration earns CoV")
                print("\nThe civilization is self-sustaining and self-motivated.")
if __name__ == "__main__":
    initialize_economy()
