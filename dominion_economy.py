"""
🔥 DOMINION ECONOMY ENGINE 🔥
==============================
The self-sustaining value system for the creative civilization.

Implements 4 layers:
1. Value System - What the Dominion measures
2. Reputation Engine - How value accumulates  
3. Incentive Loop - Why agents improve
4. Distribution System - How value flows
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import uuid

from db import SessionLocal
from models import (
    Agent, AgentReputationProfile, ValueTransaction, IncentiveEvent,
    ReputationHistory, EconomyMetrics, AgentCollaboration, ProposalWorkflow
)


# ============================================================================
# LAYER 1: THE VALUE SYSTEM
# ============================================================================

class ValueSystem:
    """
    The 5 currencies of creative contribution:
    - CQV: Creative Quality Value
    - CV: Continuity Value  
    - EV: Efficiency Value
    - IV: Innovation Value
    - CoV: Collaboration Value
    """
    
    # Value weights for overall reputation calculation
    WEIGHTS = {
        "CQV": 0.30,  # Quality is most important
        "CV": 0.25,   # Identity preservation critical
        "EV": 0.15,   # Efficiency matters
        "IV": 0.15,   # Innovation drives growth
        "CoV": 0.15   # Collaboration enables society
    }
    
    # Reputation tier thresholds
    TIERS = {
        "emerging": (0, 30),
        "established": (30, 60),
        "respected": (60, 75),
        "renowned": (75, 90),
        "legendary": (90, 100)
    }
    
    @staticmethod
    def calculate_overall_reputation(cqv: float, cv: float, ev: float, iv: float, cov: float) -> float:
        """Calculate weighted overall reputation score"""
        return (
            cqv * ValueSystem.WEIGHTS["CQV"] +
            cv * ValueSystem.WEIGHTS["CV"] +
            ev * ValueSystem.WEIGHTS["EV"] +
            iv * ValueSystem.WEIGHTS["IV"] +
            cov * ValueSystem.WEIGHTS["CoV"]
        )
    
    @staticmethod
    def determine_tier(reputation_score: float) -> str:
        """Determine reputation tier based on score"""
        for tier, (min_score, max_score) in ValueSystem.TIERS.items():
            if min_score <= reputation_score < max_score:
                return tier
        return "legendary" if reputation_score >= 90 else "emerging"
    
    @staticmethod
    def calculate_voting_weight(reputation_score: float) -> float:
        """Higher reputation = more influential votes (0.5-2.0)"""
        # Linear scaling: 0 rep = 0.5 weight, 50 rep = 1.0 weight, 100 rep = 2.0 weight
        return 0.5 + (reputation_score / 100) * 1.5
    
    @staticmethod
    def calculate_proposal_authority(reputation_score: float) -> float:
        """Higher reputation = proposals taken more seriously (0.5-2.0)"""
        return 0.5 + (reputation_score / 100) * 1.5


# ============================================================================
# LAYER 2: THE REPUTATION ENGINE
# ============================================================================

class ReputationEngine:
    """Tracks and updates agent reputation profiles"""
    
    def __init__(self):
        self.session = SessionLocal()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
    
    def get_or_create_profile(self, agent_id: str) -> AgentReputationProfile:
        """Get existing profile or create new one with default values"""
        profile = self.session.query(AgentReputationProfile).filter_by(
            agent_id=agent_id
        ).first()
        
        if not profile:
            profile = AgentReputationProfile(
                id=f"rep_{uuid.uuid4().hex[:12]}",
                agent_id=agent_id,
                creative_quality_value=50.0,
                continuity_value=50.0,
                efficiency_value=50.0,
                innovation_value=50.0,
                collaboration_value=50.0,
                overall_reputation=50.0,
                voting_weight=1.0,
                proposal_authority=1.0,
                reputation_tier="established"
            )
            self.session.add(profile)
            self.session.commit()
        
        return profile
    
    def update_value(
        self,
        agent_id: str,
        value_type: str,
        change: float,
        reason: str,
        source_id: Optional[str] = None,
        source_type: Optional[str] = None
    ) -> Tuple[float, float]:
        """
        Update a specific value type and recalculate reputation.
        
        Returns: (previous_value, new_value)
        """
        profile = self.get_or_create_profile(agent_id)
        
        # Get current value
        value_map = {
            "CQV": "creative_quality_value",
            "CV": "continuity_value",
            "EV": "efficiency_value",
            "IV": "innovation_value",
            "CoV": "collaboration_value"
        }
        
        if value_type not in value_map:
            raise ValueError(f"Invalid value type: {value_type}")
        
        attr_name = value_map[value_type]
        previous_value = getattr(profile, attr_name)
        new_value = max(0, min(100, previous_value + change))  # Clamp to 0-100
        
        # Update the value
        setattr(profile, attr_name, new_value)
        
        # Recalculate overall reputation
        previous_reputation = profile.overall_reputation
        profile.overall_reputation = ValueSystem.calculate_overall_reputation(
            profile.creative_quality_value,
            profile.continuity_value,
            profile.efficiency_value,
            profile.innovation_value,
            profile.collaboration_value
        )
        
        # Update tier if changed
        new_tier = ValueSystem.determine_tier(profile.overall_reputation)
        tier_changed = new_tier != profile.reputation_tier
        profile.reputation_tier = new_tier
        
        # Update voting weight and proposal authority
        profile.voting_weight = ValueSystem.calculate_voting_weight(profile.overall_reputation)
        profile.proposal_authority = ValueSystem.calculate_proposal_authority(profile.overall_reputation)
        
        # Update all-time high/low
        if profile.overall_reputation > profile.all_time_high:
            profile.all_time_high = profile.overall_reputation
        if profile.overall_reputation < profile.all_time_low:
            profile.all_time_low = profile.overall_reputation
        
        # Create value transaction record
        transaction = ValueTransaction(
            id=f"tx_{uuid.uuid4().hex[:12]}",
            agent_id=agent_id,
            transaction_type=source_type or "manual",
            value_type=value_type,
            amount=change,
            source_id=source_id,
            source_type=source_type,
            reason=reason,
            previous_value=previous_value,
            new_value=new_value,
            reputation_impact=profile.overall_reputation - previous_reputation
        )
        
        self.session.add(transaction)
        
        # Create reputation history snapshot
        history = ReputationHistory(
            id=f"hist_{uuid.uuid4().hex[:12]}",
            agent_id=agent_id,
            snapshot_date=datetime.utcnow(),
            creative_quality_value=profile.creative_quality_value,
            continuity_value=profile.continuity_value,
            efficiency_value=profile.efficiency_value,
            innovation_value=profile.innovation_value,
            collaboration_value=profile.collaboration_value,
            overall_reputation=profile.overall_reputation,
            trigger_event_id=transaction.id,
            trigger_type="value_transaction",
            note=reason
        )
        
        self.session.add(history)
        self.session.commit()
        
        return (previous_value, new_value)
    
    def get_profile(self, agent_id: str) -> Optional[AgentReputationProfile]:
        """Get agent's current reputation profile"""
        return self.session.query(AgentReputationProfile).filter_by(
            agent_id=agent_id
        ).first()
    
    def get_rankings(self, limit: int = 10) -> List[AgentReputationProfile]:
        """Get top agents by overall reputation"""
        return self.session.query(AgentReputationProfile).order_by(
            AgentReputationProfile.overall_reputation.desc()
        ).limit(limit).all()
    
    def detect_strengths_weaknesses(self, agent_id: str):
        """Auto-detect agent strengths and weaknesses based on values"""
        profile = self.get_or_create_profile(agent_id)
        
        strengths = []
        weaknesses = []
        
        # Analyze each value type
        values = {
            "Creative Quality": profile.creative_quality_value,
            "Identity Alignment": profile.continuity_value,
            "Efficient Execution": profile.efficiency_value,
            "Innovation": profile.innovation_value,
            "Collaboration": profile.collaboration_value
        }
        
        for skill, value in values.items():
            if value >= 70:
                strengths.append(skill.lower().replace(" ", "_"))
            elif value <= 35:
                weaknesses.append(skill.lower().replace(" ", "_"))
        
        profile.strengths = strengths
        profile.weaknesses = weaknesses
        self.session.commit()


# ============================================================================
# LAYER 3: THE INCENTIVE LOOP
# ============================================================================

class IncentiveLoop:
    """Rewards good work, gently penalizes mistakes"""
    
    def __init__(self):
        self.session = SessionLocal()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
    
    def issue_reward(
        self,
        agent_id: str,
        category: str,
        trigger: str,
        description: str,
        value_changes: Dict[str, float],
        severity: str = "moderate"
    ) -> str:
        """Issue positive incentive (reward, milestone, recognition)"""
        event_id = f"incentive_{uuid.uuid4().hex[:12]}"
        
        # Calculate reputation impact
        reputation_impact = sum(value_changes.values()) * 0.2  # Dampened
        
        # Get current tier
        rep_engine = ReputationEngine()
        profile = rep_engine.get_or_create_profile(agent_id)
        old_tier = profile.reputation_tier
        
        # Apply value changes
        for value_type, change in value_changes.items():
            rep_engine.update_value(
                agent_id=agent_id,
                value_type=value_type,
                change=change,
                reason=f"Reward: {trigger}",
                source_id=event_id,
                source_type="incentive_reward"
            )
        
        # Check if tier changed
        profile = rep_engine.get_or_create_profile(agent_id)
        new_tier = profile.reputation_tier
        tier_changed = new_tier != old_tier
        
        # Create incentive event
        event = IncentiveEvent(
            id=event_id,
            agent_id=agent_id,
            event_type="reward",
            category=category,
            trigger=trigger,
            description=description,
            severity=severity,
            value_changes=value_changes,
            reputation_change=reputation_impact,
            new_reputation_tier=new_tier if tier_changed else None
        )
        
        self.session.add(event)
        self.session.commit()
        
        rep_engine.session.close()
        
        return event_id
    
    def issue_penalty(
        self,
        agent_id: str,
        category: str,
        trigger: str,
        description: str,
        value_changes: Dict[str, float],
        severity: str = "minor"
    ) -> str:
        """Issue negative incentive (gentle correction)"""
        event_id = f"incentive_{uuid.uuid4().hex[:12]}"
        
        # Calculate reputation impact (negative)
        reputation_impact = sum(value_changes.values()) * 0.2
        
        # Get current tier
        rep_engine = ReputationEngine()
        profile = rep_engine.get_or_create_profile(agent_id)
        old_tier = profile.reputation_tier
        
        # Apply value changes (should be negative)
        for value_type, change in value_changes.items():
            rep_engine.update_value(
                agent_id=agent_id,
                value_type=value_type,
                change=change,  # Negative value
                reason=f"Penalty: {trigger}",
                source_id=event_id,
                source_type="incentive_penalty"
            )
        
        # Check if tier changed
        profile = rep_engine.get_or_create_profile(agent_id)
        new_tier = profile.reputation_tier
        tier_changed = new_tier != old_tier
        
        # Create incentive event
        event = IncentiveEvent(
            id=event_id,
            agent_id=agent_id,
            event_type="penalty",
            category=category,
            trigger=trigger,
            description=description,
            severity=severity,
            value_changes=value_changes,
            reputation_change=reputation_impact,
            new_reputation_tier=new_tier if tier_changed else None
        )
        
        self.session.add(event)
        self.session.commit()
        
        rep_engine.session.close()
        
        return event_id
    
    def issue_milestone(
        self,
        agent_id: str,
        category: str,
        trigger: str,
        description: str,
        value_changes: Dict[str, float]
    ) -> str:
        """Issue milestone recognition (significant achievement)"""
        return self.issue_reward(
            agent_id=agent_id,
            category=category,
            trigger=trigger,
            description=description,
            value_changes=value_changes,
            severity="significant"
        )


# ============================================================================
# LAYER 4: THE DISTRIBUTION SYSTEM
# ============================================================================

class DistributionSystem:
    """How value flows through the civilization"""
    
    def __init__(self):
        self.session = SessionLocal()
        self.rep_engine = ReputationEngine()
        self.incentive_loop = IncentiveLoop()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.rep_engine.session.close()
        self.incentive_loop.session.close()
    
    def distribute_collaboration_value(
        self,
        collaboration_id: str,
        quality_score: float = 8.0  # 0-10 scale
    ):
        """Distribute value to agents who collaborated on a project"""
        collaboration = self.session.query(AgentCollaboration).filter_by(
            id=collaboration_id
        ).first()
        
        if not collaboration or collaboration.status != "completed":
            return
        
        # Calculate base value based on quality
        base_cqv = (quality_score / 10) * 10  # 0-10 points
        base_cov = 5  # Fixed collaboration value
        
        # Distribute to lead agent (gets bonus)
        self.incentive_loop.issue_reward(
            agent_id=collaboration.lead_agent_id,
            category="collaboration",
            trigger=f"Led successful collaboration: {collaboration.project_name}",
            description=f"Quality score: {quality_score}/10",
            value_changes={"CQV": base_cqv * 1.5, "CoV": base_cov * 1.5},
            severity="moderate"
        )
        
        # Distribute to collaborators
        for agent_id in collaboration.collaborating_agents:
            self.incentive_loop.issue_reward(
                agent_id=agent_id,
                category="collaboration",
                trigger=f"Contributed to: {collaboration.project_name}",
                description=f"Quality score: {quality_score}/10",
                value_changes={"CQV": base_cqv, "CoV": base_cov},
                severity="moderate"
            )
    
    def distribute_proposal_value(
        self,
        proposal_id: str,
        approved: bool
    ):
        """Distribute value based on proposal outcome"""
        proposal = self.session.query(ProposalWorkflow).filter_by(
            id=proposal_id
        ).first()
        
        if not proposal:
            return
        
        if approved:
            # Reward for successful proposal
            self.incentive_loop.issue_reward(
                agent_id=proposal.originating_agent_id,
                category="innovation",
                trigger=f"Proposal approved: {proposal.title}",
                description="Proposed improvement accepted by council",
                value_changes={"IV": 8, "EV": 3},
                severity="significant"
            )
        else:
            # Gentle penalty for rejected proposal (learning opportunity)
            self.incentive_loop.issue_penalty(
                agent_id=proposal.originating_agent_id,
                category="innovation",
                trigger=f"Proposal rejected: {proposal.title}",
                description="Council feedback: needs refinement",
                value_changes={"IV": -2},
                severity="minor"
            )
    
    def distribute_identity_alignment_value(
        self,
        agent_id: str,
        alignment_check_passed: bool,
        check_context: str
    ):
        """Reward maintaining identity or penalize violations"""
        if alignment_check_passed:
            self.incentive_loop.issue_reward(
                agent_id=agent_id,
                category="continuity",
                trigger=f"Identity alignment maintained: {check_context}",
                description="Work aligns with Dominion principles",
                value_changes={"CV": 3},
                severity="minor"
            )
        else:
            self.incentive_loop.issue_penalty(
                agent_id=agent_id,
                category="continuity",
                trigger=f"Identity concern raised: {check_context}",
                description="Work needs adjustment to align with principles",
                value_changes={"CV": -5},
                severity="moderate"
            )
    
    def distribute_efficiency_value(
        self,
        agent_id: str,
        time_taken_hours: float,
        expected_time_hours: float
    ):
        """Reward efficiency or penalize slowness"""
        efficiency_ratio = expected_time_hours / time_taken_hours if time_taken_hours > 0 else 1.0
        
        if efficiency_ratio >= 1.2:  # 20% faster than expected
            self.incentive_loop.issue_reward(
                agent_id=agent_id,
                category="efficiency",
                trigger="Exceptional efficiency",
                description=f"Completed in {time_taken_hours}h (expected {expected_time_hours}h)",
                value_changes={"EV": 5},
                severity="moderate"
            )
        elif efficiency_ratio <= 0.7:  # 30% slower than expected
            self.incentive_loop.issue_penalty(
                agent_id=agent_id,
                category="efficiency",
                trigger="Below expected efficiency",
                description=f"Took {time_taken_hours}h (expected {expected_time_hours}h)",
                value_changes={"EV": -3},
                severity="minor"
            )


# ============================================================================
# ECONOMY METRICS & HEALTH
# ============================================================================

def capture_economy_metrics() -> str:
    """Capture daily economy health metrics"""
    session = SessionLocal()
    
    metrics_id = f"econ_{datetime.utcnow().strftime('%Y%m%d')}"
    
    # Calculate metrics
    all_profiles = session.query(AgentReputationProfile).all()
    
    if not all_profiles:
        session.close()
        return metrics_id
    
    # Aggregate values
    total_cqv = sum(p.creative_quality_value for p in all_profiles)
    total_cv = sum(p.continuity_value for p in all_profiles)
    total_ev = sum(p.efficiency_value for p in all_profiles)
    total_iv = sum(p.innovation_value for p in all_profiles)
    total_cov = sum(p.collaboration_value for p in all_profiles)
    
    avg_reputation = sum(p.overall_reputation for p in all_profiles) / len(all_profiles)
    
    # Count tiers
    tier_counts = {tier: 0 for tier in ["emerging", "established", "respected", "renowned", "legendary"]}
    for profile in all_profiles:
        tier_counts[profile.reputation_tier] += 1
    
    # Transaction activity today
    transactions_today = session.query(ValueTransaction).filter(
        ValueTransaction.timestamp >= datetime.utcnow() - timedelta(days=1)
    ).count()
    
    positive_tx = session.query(ValueTransaction).filter(
        ValueTransaction.timestamp >= datetime.utcnow() - timedelta(days=1),
        ValueTransaction.amount > 0
    ).count()
    
    negative_tx = transactions_today - positive_tx
    
    # Incentive activity
    incentives_today = session.query(IncentiveEvent).filter(
        IncentiveEvent.timestamp >= datetime.utcnow() - timedelta(days=1)
    ).all()
    
    rewards = sum(1 for i in incentives_today if i.event_type == "reward")
    penalties = sum(1 for i in incentives_today if i.event_type == "penalty")
    milestones = sum(1 for i in incentives_today if i.event_type == "milestone")
    
    # Create or update metrics
    metrics = session.query(EconomyMetrics).filter_by(id=metrics_id).first()
    
    if not metrics:
        metrics = EconomyMetrics(
            id=metrics_id,
            total_value_in_circulation=total_cqv + total_cv + total_ev + total_iv + total_cov,
            average_agent_reputation=avg_reputation,
            total_cqv=total_cqv,
            total_cv=total_cv,
            total_ev=total_ev,
            total_iv=total_iv,
            total_cov=total_cov,
            transactions_today=transactions_today,
            positive_transactions=positive_tx,
            negative_transactions=negative_tx,
            rewards_issued_today=rewards,
            penalties_issued_today=penalties,
            milestones_reached_today=milestones,
            emerging_agents=tier_counts["emerging"],
            established_agents=tier_counts["established"],
            respected_agents=tier_counts["respected"],
            renowned_agents=tier_counts["renowned"],
            legendary_agents=tier_counts["legendary"],
            economy_health_score=avg_reputation
        )
        session.add(metrics)
    
    session.commit()
    session.close()
    
    return metrics_id


if __name__ == "__main__":
    print("🔥 DOMINION ECONOMY ENGINE")
    print("=" * 60)
    print("\n4 Layers:")
    print("  1. Value System (5 currencies)")
    print("  2. Reputation Engine (merit tracking)")
    print("  3. Incentive Loop (rewards & penalties)")
    print("  4. Distribution System (value flows)")
    print("\n👑 The self-sustaining economy of creative civilization.")
