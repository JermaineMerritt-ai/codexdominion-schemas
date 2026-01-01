"""
🔥 PHASE 60 — STEP 3: MULTI-WORLD GOVERNANCE SYSTEM
How worlds collaborate, vote, resolve disputes, and maintain cosmic alignment.

This module implements the 4-component governance system:
1. Cosmic Council of Worlds (CCW) - Governing body with representatives
2. Inter-World Voting System (IWVS) - Democratic decision-making
3. Inter-World Resolution Protocol (IWRP) - Dispute resolution
4. Cosmic Alignment Framework (CAF) - Unity + autonomy + harmony

This is the cosmic parliament for creative ecosystems.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import uuid
import json

from db import SessionLocal
from models import Agent
from multiworld_schema import World, WorldAgent, InterWorldConnection, InterWorldMessage


# ============================================================================
# COMPONENT 1 — COSMIC COUNCIL OF WORLDS (CCW)
# ============================================================================

class RepresentativeRole(Enum):
    """Types of representatives each world sends to the council."""
    CREATIVE = "creative"           # Speaks for creative direction
    CONTINUITY = "continuity"       # Protects identity and alignment
    OPERATIONS = "operations"       # Oversees execution and feasibility


class CouncilRepresentative:
    """
    A world's representative in the Cosmic Council.
    Each world sends 3 representatives (one per role).
    """
    
    def __init__(
        self,
        representative_id: str,
        world_id: str,
        agent_id: str,
        role: RepresentativeRole,
        voting_weight: float = 1.0,
        appointed_date: datetime = None
    ):
        self.representative_id = representative_id
        self.world_id = world_id
        self.agent_id = agent_id
        self.role = role
        self.voting_weight = voting_weight
        self.appointed_date = appointed_date or datetime.utcnow()
        self.votes_cast = 0
        self.proposals_submitted = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "representative_id": self.representative_id,
            "world_id": self.world_id,
            "agent_id": self.agent_id,
            "role": self.role.value,
            "voting_weight": self.voting_weight,
            "appointed_date": self.appointed_date.isoformat(),
            "votes_cast": self.votes_cast,
            "proposals_submitted": self.proposals_submitted
        }


class CosmicCouncilOfWorlds:
    """
    COMPONENT 1: The governing body of the entire Dominion Cosmos.
    
    Structure:
    - Each world sends 3 representatives (Creative, Continuity, Operations)
    - Representatives vote on inter-world matters
    - Council maintains balance between worlds
    - Sovereign world (Dominion Prime) has special authority
    """
    
    def __init__(self):
        self.session = SessionLocal()
        self.representatives: Dict[str, CouncilRepresentative] = {}
        self._load_representatives()
    
    def appoint_representatives(
        self,
        world_id: str,
        creative_agent_id: str,
        continuity_agent_id: str,
        operations_agent_id: str
    ) -> List[CouncilRepresentative]:
        """
        Appoint the three representatives for a world.
        
        Each world must send:
        1. Creative Representative - Creative direction
        2. Continuity Representative - Identity protection
        3. Operations Representative - Execution oversight
        """
        world = self.session.query(World).filter_by(id=world_id).first()
        if not world:
            raise ValueError(f"World {world_id} not found")
        
        # Calculate voting weight based on world metrics
        base_weight = 1.0
        reputation_bonus = (world.creative_output_quality / 100) * 0.3
        collaboration_bonus = (world.collaboration_index / 100) * 0.2
        
        voting_weight = base_weight + reputation_bonus + collaboration_bonus
        
        # Cap at 1.5x to prevent dominance
        voting_weight = min(voting_weight, 1.5)
        
        representatives = []
        
        for role, agent_id in [
            (RepresentativeRole.CREATIVE, creative_agent_id),
            (RepresentativeRole.CONTINUITY, continuity_agent_id),
            (RepresentativeRole.OPERATIONS, operations_agent_id)
        ]:
            rep = CouncilRepresentative(
                representative_id=f"rep_{world_id}_{role.value}_{uuid.uuid4().hex[:8]}",
                world_id=world_id,
                agent_id=agent_id,
                role=role,
                voting_weight=voting_weight
            )
            
            self.representatives[rep.representative_id] = rep
            representatives.append(rep)
        
        return representatives
    
    def get_world_representatives(self, world_id: str) -> List[CouncilRepresentative]:
        """Get all representatives from a specific world."""
        return [
            rep for rep in self.representatives.values()
            if rep.world_id == world_id
        ]
    
    def get_total_voting_power(self, world_id: str) -> float:
        """Calculate total voting power for a world."""
        reps = self.get_world_representatives(world_id)
        return sum(rep.voting_weight for rep in reps)
    
    def get_council_composition(self) -> Dict[str, Any]:
        """Get overview of council composition."""
        worlds = {}
        for rep in self.representatives.values():
            if rep.world_id not in worlds:
                worlds[rep.world_id] = {
                    "representatives": [],
                    "total_voting_power": 0
                }
            worlds[rep.world_id]["representatives"].append(rep.to_dict())
            worlds[rep.world_id]["total_voting_power"] += rep.voting_weight
        
        return {
            "total_representatives": len(self.representatives),
            "total_worlds_represented": len(worlds),
            "worlds": worlds,
            "avg_voting_power_per_world": sum(w["total_voting_power"] for w in worlds.values()) / len(worlds) if worlds else 0
        }
    
    def _load_representatives(self):
        """Load existing representatives from storage."""
        # In production, this would load from database
        # For now, we'll generate on-demand
        pass
    
    def close(self):
        """Close database session."""
        self.session.close()


# ============================================================================
# COMPONENT 2 — INTER-WORLD VOTING SYSTEM (IWVS)
# ============================================================================

class VoteThreshold(Enum):
    """Vote thresholds for different decision types."""
    SIMPLE_MAJORITY = 0.51      # 51% for routine decisions
    SUPERMAJORITY = 0.66        # 66% for structural changes
    UNANIMOUS = 1.0             # 100% for identity-level changes


class ProposalType(Enum):
    """Types of proposals that can be voted on."""
    ROUTINE_DECISION = "routine_decision"           # Threshold: Simple Majority
    RESOURCE_ALLOCATION = "resource_allocation"     # Threshold: Simple Majority
    CULTURAL_PATTERN = "cultural_pattern"           # Threshold: Supermajority
    STRUCTURAL_CHANGE = "structural_change"         # Threshold: Supermajority
    NEW_WORLD_CREATION = "new_world_creation"       # Threshold: Supermajority
    IDENTITY_CHANGE = "identity_change"             # Threshold: Unanimous
    SOVEREIGN_OVERRIDE = "sovereign_override"       # Threshold: Sovereign only


class Vote:
    """A single vote cast by a representative."""
    
    def __init__(
        self,
        vote_id: str,
        representative_id: str,
        proposal_id: str,
        vote_value: str,  # "approve", "reject", "abstain"
        reasoning: str = ""
    ):
        self.vote_id = vote_id
        self.representative_id = representative_id
        self.proposal_id = proposal_id
        self.vote_value = vote_value
        self.reasoning = reasoning
        self.cast_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "vote_id": self.vote_id,
            "representative_id": self.representative_id,
            "proposal_id": self.proposal_id,
            "vote_value": self.vote_value,
            "reasoning": self.reasoning,
            "cast_at": self.cast_at.isoformat()
        }


class Proposal:
    """A proposal for the council to vote on."""
    
    def __init__(
        self,
        proposal_id: str,
        title: str,
        description: str,
        proposal_type: ProposalType,
        proposed_by_world: str,
        proposed_by_rep: str,
        threshold: VoteThreshold
    ):
        self.proposal_id = proposal_id
        self.title = title
        self.description = description
        self.proposal_type = proposal_type
        self.proposed_by_world = proposed_by_world
        self.proposed_by_rep = proposed_by_rep
        self.threshold = threshold
        self.votes: Dict[str, Vote] = {}
        self.status = "open"  # open, passed, rejected, withdrawn
        self.created_at = datetime.utcnow()
        self.voting_deadline = datetime.utcnow() + timedelta(days=7)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "proposal_id": self.proposal_id,
            "title": self.title,
            "description": self.description,
            "proposal_type": self.proposal_type.value,
            "proposed_by_world": self.proposed_by_world,
            "proposed_by_rep": self.proposed_by_rep,
            "threshold": self.threshold.value,
            "votes": [v.to_dict() for v in self.votes.values()],
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "voting_deadline": self.voting_deadline.isoformat()
        }


class InterWorldVotingSystem:
    """
    COMPONENT 2: Democratic decision-making across worlds.
    
    Features:
    - Weighted voting based on world reputation and contribution
    - Multiple threshold levels (51%, 66%, 100%)
    - Influence cap to prevent dominance
    - Transparent vote tracking
    """
    
    def __init__(self, council: CosmicCouncilOfWorlds):
        self.council = council
        self.proposals: Dict[str, Proposal] = {}
    
    def create_proposal(
        self,
        title: str,
        description: str,
        proposal_type: ProposalType,
        proposed_by_world: str,
        proposed_by_rep: str
    ) -> Proposal:
        """
        Create a new proposal for the council to vote on.
        """
        # Determine threshold based on proposal type
        threshold_map = {
            ProposalType.ROUTINE_DECISION: VoteThreshold.SIMPLE_MAJORITY,
            ProposalType.RESOURCE_ALLOCATION: VoteThreshold.SIMPLE_MAJORITY,
            ProposalType.CULTURAL_PATTERN: VoteThreshold.SUPERMAJORITY,
            ProposalType.STRUCTURAL_CHANGE: VoteThreshold.SUPERMAJORITY,
            ProposalType.NEW_WORLD_CREATION: VoteThreshold.SUPERMAJORITY,
            ProposalType.IDENTITY_CHANGE: VoteThreshold.UNANIMOUS,
            ProposalType.SOVEREIGN_OVERRIDE: VoteThreshold.UNANIMOUS
        }
        
        threshold = threshold_map.get(proposal_type, VoteThreshold.SIMPLE_MAJORITY)
        
        proposal = Proposal(
            proposal_id=f"prop_{uuid.uuid4().hex[:12]}",
            title=title,
            description=description,
            proposal_type=proposal_type,
            proposed_by_world=proposed_by_world,
            proposed_by_rep=proposed_by_rep,
            threshold=threshold
        )
        
        self.proposals[proposal.proposal_id] = proposal
        
        return proposal
    
    def cast_vote(
        self,
        proposal_id: str,
        representative_id: str,
        vote_value: str,
        reasoning: str = ""
    ) -> Vote:
        """
        Cast a vote on a proposal.
        
        Vote values: "approve", "reject", "abstain"
        """
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found")
        
        if proposal.status != "open":
            raise ValueError(f"Proposal {proposal_id} is not open for voting")
        
        representative = self.council.representatives.get(representative_id)
        if not representative:
            raise ValueError(f"Representative {representative_id} not found")
        
        vote = Vote(
            vote_id=f"vote_{uuid.uuid4().hex[:12]}",
            representative_id=representative_id,
            proposal_id=proposal_id,
            vote_value=vote_value,
            reasoning=reasoning
        )
        
        proposal.votes[representative_id] = vote
        representative.votes_cast += 1
        
        return vote
    
    def tally_votes(self, proposal_id: str) -> Dict[str, Any]:
        """
        Tally votes for a proposal and determine outcome.
        
        Returns:
        - vote counts
        - weighted totals
        - whether threshold is met
        - final status
        """
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found")
        
        approve_weight = 0.0
        reject_weight = 0.0
        abstain_weight = 0.0
        total_possible_weight = 0.0
        
        # Calculate total possible voting weight
        for rep in self.council.representatives.values():
            total_possible_weight += rep.voting_weight
        
        # Tally votes
        for vote in proposal.votes.values():
            rep = self.council.representatives.get(vote.representative_id)
            if not rep:
                continue
            
            if vote.vote_value == "approve":
                approve_weight += rep.voting_weight
            elif vote.vote_value == "reject":
                reject_weight += rep.voting_weight
            elif vote.vote_value == "abstain":
                abstain_weight += rep.voting_weight
        
        # Calculate percentages
        votes_cast_weight = approve_weight + reject_weight + abstain_weight
        participation_rate = votes_cast_weight / total_possible_weight if total_possible_weight > 0 else 0
        
        # Approval is based on votes cast (excluding abstentions)
        active_votes_weight = approve_weight + reject_weight
        approval_rate = approve_weight / active_votes_weight if active_votes_weight > 0 else 0
        
        # Check if threshold is met
        threshold_met = approval_rate >= proposal.threshold.value
        
        # Update proposal status
        if threshold_met:
            proposal.status = "passed"
        elif datetime.utcnow() > proposal.voting_deadline:
            proposal.status = "rejected"
        
        return {
            "proposal_id": proposal_id,
            "votes_cast": len(proposal.votes),
            "approve_weight": approve_weight,
            "reject_weight": reject_weight,
            "abstain_weight": abstain_weight,
            "total_possible_weight": total_possible_weight,
            "participation_rate": participation_rate,
            "approval_rate": approval_rate,
            "threshold_required": proposal.threshold.value,
            "threshold_met": threshold_met,
            "status": proposal.status
        }


# ============================================================================
# COMPONENT 3 — INTER-WORLD RESOLUTION PROTOCOL (IWRP)
# ============================================================================

class DisputeType(Enum):
    """Types of disputes between worlds."""
    RESOURCE_CONFLICT = "resource_conflict"         # Competing for same resource
    PATTERN_INCOMPATIBILITY = "pattern_incompatibility"  # Incompatible cultural patterns
    IDENTITY_DRIFT = "identity_drift"               # World drifting from core values
    WORKFLOW_INTERFERENCE = "workflow_interference"  # Conflicting workflows
    AGENT_ASSIGNMENT = "agent_assignment"           # Competing for same agent
    PROJECT_PRIORITY = "project_priority"           # Conflicting project priorities


class Dispute:
    """A dispute between worlds."""
    
    def __init__(
        self,
        dispute_id: str,
        dispute_type: DisputeType,
        world_a: str,
        world_b: str,
        description: str,
        severity: str = "medium"
    ):
        self.dispute_id = dispute_id
        self.dispute_type = dispute_type
        self.world_a = world_a
        self.world_b = world_b
        self.description = description
        self.severity = severity  # low, medium, high, critical
        self.status = "open"  # open, mediation, voting, resolved, escalated
        self.arguments: Dict[str, str] = {}  # world_id -> argument
        self.resolution = None
        self.created_at = datetime.utcnow()
        self.resolved_at = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "dispute_id": self.dispute_id,
            "dispute_type": self.dispute_type.value,
            "world_a": self.world_a,
            "world_b": self.world_b,
            "description": self.description,
            "severity": self.severity,
            "status": self.status,
            "arguments": self.arguments,
            "resolution": self.resolution,
            "created_at": self.created_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None
        }


class InterWorldResolutionProtocol:
    """
    COMPONENT 3: How worlds resolve disagreements.
    
    Process:
    1. Structured debate - Each world presents its case
    2. Council mediation - Representatives evaluate
    3. Vote - Council decides outcome
    4. Sovereign escalation - If needed, escalate to sovereign
    """
    
    def __init__(self, council: CosmicCouncilOfWorlds, voting_system: InterWorldVotingSystem):
        self.council = council
        self.voting_system = voting_system
        self.disputes: Dict[str, Dispute] = {}
    
    def file_dispute(
        self,
        dispute_type: DisputeType,
        world_a: str,
        world_b: str,
        description: str,
        severity: str = "medium"
    ) -> Dispute:
        """
        File a dispute between two worlds.
        """
        dispute = Dispute(
            dispute_id=f"dispute_{uuid.uuid4().hex[:12]}",
            dispute_type=dispute_type,
            world_a=world_a,
            world_b=world_b,
            description=description,
            severity=severity
        )
        
        self.disputes[dispute.dispute_id] = dispute
        
        return dispute
    
    def submit_argument(
        self,
        dispute_id: str,
        world_id: str,
        argument: str
    ):
        """
        Submit an argument from one world in the dispute.
        """
        dispute = self.disputes.get(dispute_id)
        if not dispute:
            raise ValueError(f"Dispute {dispute_id} not found")
        
        if world_id not in [dispute.world_a, dispute.world_b]:
            raise ValueError(f"World {world_id} is not part of this dispute")
        
        dispute.arguments[world_id] = argument
        
        # If both worlds have submitted arguments, move to mediation
        if len(dispute.arguments) == 2:
            dispute.status = "mediation"
    
    def create_resolution_proposal(
        self,
        dispute_id: str,
        resolution_description: str,
        proposed_by_rep: str
    ) -> Proposal:
        """
        Create a proposal to resolve the dispute via council vote.
        """
        dispute = self.disputes.get(dispute_id)
        if not dispute:
            raise ValueError(f"Dispute {dispute_id} not found")
        
        proposal = self.voting_system.create_proposal(
            title=f"Resolution: {dispute.dispute_type.value}",
            description=resolution_description,
            proposal_type=ProposalType.ROUTINE_DECISION,
            proposed_by_world="dominion_prime",  # Council mediates
            proposed_by_rep=proposed_by_rep
        )
        
        dispute.status = "voting"
        
        return proposal
    
    def resolve_dispute(
        self,
        dispute_id: str,
        resolution: str,
        resolved_by: str = "council_vote"
    ):
        """
        Mark a dispute as resolved.
        """
        dispute = self.disputes.get(dispute_id)
        if not dispute:
            raise ValueError(f"Dispute {dispute_id} not found")
        
        dispute.resolution = {
            "decision": resolution,
            "resolved_by": resolved_by,
            "resolved_at": datetime.utcnow().isoformat()
        }
        dispute.status = "resolved"
        dispute.resolved_at = datetime.utcnow()
    
    def escalate_to_sovereign(
        self,
        dispute_id: str,
        escalation_reason: str
    ) -> Dict[str, Any]:
        """
        Escalate a dispute to the sovereign authority (user).
        
        Used when:
        - Dispute affects cosmic identity
        - Council cannot reach consensus
        - Dispute has critical severity
        """
        dispute = self.disputes.get(dispute_id)
        if not dispute:
            raise ValueError(f"Dispute {dispute_id} not found")
        
        dispute.status = "escalated"
        
        return {
            "dispute_id": dispute_id,
            "escalated_to": "sovereign_authority",
            "reason": escalation_reason,
            "requires_decision": True,
            "dispute_summary": dispute.to_dict()
        }


# ============================================================================
# COMPONENT 4 — COSMIC ALIGNMENT FRAMEWORK (CAF)
# ============================================================================

class AlignmentPillar(Enum):
    """The three pillars of cosmic alignment."""
    SHARED_IDENTITY = "shared_identity"     # Core values and tone
    LOCAL_AUTONOMY = "local_autonomy"       # World-specific culture
    COSMIC_HARMONY = "cosmic_harmony"       # Collaboration over competition


class CosmicAlignmentFramework:
    """
    COMPONENT 4: The backbone of multi-world coherence.
    
    Three Pillars:
    1. Shared Identity - All worlds honor Dominion core values
    2. Local Autonomy - Each world maintains its own culture
    3. Cosmic Harmony - Worlds collaborate instead of competing
    
    Ensures:
    - Unity without uniformity
    - Diversity without fragmentation
    - Growth without chaos
    """
    
    def __init__(self):
        self.session = SessionLocal()
        
        # Core values all worlds must honor
        self.shared_identity = {
            "core_values": [
                "excellence",
                "identity",
                "innovation",
                "collaboration",
                "safety",
                "imagination"
            ],
            "brand_essence": "The Flame Burns Sovereign and Eternal",
            "quality_minimum": 70.0,
            "child_safety_absolute": True
        }
        
        # Autonomy guidelines
        self.autonomy_boundaries = {
            "allowed_variations": [
                "cultural_patterns",
                "workflow_processes",
                "creative_techniques",
                "agent_specializations"
            ],
            "protected_constants": [
                "core_values",
                "brand_identity",
                "safety_standards",
                "quality_thresholds"
            ]
        }
        
        # Harmony principles
        self.harmony_principles = {
            "collaboration_over_competition": True,
            "resource_sharing_encouraged": True,
            "innovation_broadcasting_required": True,
            "dispute_resolution_mandatory": True
        }
    
    def assess_world_alignment(self, world_id: str) -> Dict[str, Any]:
        """
        Assess how well a world aligns with the Cosmic Alignment Framework.
        
        Returns alignment scores for all three pillars.
        """
        world = self.session.query(World).filter_by(id=world_id).first()
        if not world:
            raise ValueError(f"World {world_id} not found")
        
        # Pillar 1: Shared Identity (0-100)
        identity_score = self._assess_shared_identity(world)
        
        # Pillar 2: Local Autonomy (0-100)
        autonomy_score = self._assess_local_autonomy(world)
        
        # Pillar 3: Cosmic Harmony (0-100)
        harmony_score = self._assess_cosmic_harmony(world)
        
        # Overall alignment
        overall_alignment = (identity_score + autonomy_score + harmony_score) / 3
        
        # Determine status
        if overall_alignment >= 80:
            status = "excellent"
        elif overall_alignment >= 60:
            status = "good"
        elif overall_alignment >= 40:
            status = "needs_improvement"
        else:
            status = "critical_drift"
        
        return {
            "world_id": world_id,
            "world_name": world.name,
            "alignment_scores": {
                "shared_identity": identity_score,
                "local_autonomy": autonomy_score,
                "cosmic_harmony": harmony_score,
                "overall": overall_alignment
            },
            "status": status,
            "recommendations": self._generate_alignment_recommendations(
                identity_score, autonomy_score, harmony_score
            )
        }
    
    def _assess_shared_identity(self, world: World) -> float:
        """Assess adherence to shared identity (0-100)."""
        score = 0.0
        
        # Check quality meets minimum
        if world.creative_output_quality >= self.shared_identity["quality_minimum"]:
            score += 40
        else:
            score += (world.creative_output_quality / self.shared_identity["quality_minimum"]) * 40
        
        # Check core values presence
        if world.culture and "core_values" in world.culture:
            world_values = set(world.culture["core_values"])
            required_values = set(self.shared_identity["core_values"])
            value_overlap = len(world_values.intersection(required_values))
            score += (value_overlap / len(required_values)) * 40
        else:
            score += 20  # Partial credit for having any culture
        
        # Check status
        if world.status == "active":
            score += 20
        
        return min(score, 100)
    
    def _assess_local_autonomy(self, world: World) -> float:
        """Assess healthy local autonomy (0-100)."""
        score = 0.0
        
        # World has unique specialization
        if world.specialization:
            score += 30
        
        # World has cultural identity
        if world.culture:
            score += 30
        
        # World has its own economy config
        if world.economy_config:
            score += 20
        
        # World has own agents
        if world.population > 0:
            score += 20
        
        return min(score, 100)
    
    def _assess_cosmic_harmony(self, world: World) -> float:
        """Assess collaboration and harmony (0-100)."""
        score = 0.0
        
        # High collaboration index
        score += (world.collaboration_index / 100) * 50
        
        # Has active connections
        active_connections = self.session.query(InterWorldConnection).filter(
            (InterWorldConnection.source_world_id == world.id) |
            (InterWorldConnection.target_world_id == world.id),
            InterWorldConnection.status == "active"
        ).count()
        
        if active_connections > 0:
            score += min(active_connections * 10, 30)
        
        # Participating in cross-world projects
        from multiworld_schema import CrossWorldProject
        active_projects = self.session.query(CrossWorldProject).filter(
            CrossWorldProject.participating_worlds.any(id=world.id),
            CrossWorldProject.status == "active"
        ).count()
        
        if active_projects > 0:
            score += 20
        
        return min(score, 100)
    
    def _generate_alignment_recommendations(
        self,
        identity_score: float,
        autonomy_score: float,
        harmony_score: float
    ) -> List[str]:
        """Generate recommendations for improving alignment."""
        recommendations = []
        
        if identity_score < 60:
            recommendations.append("Strengthen core value adherence")
            recommendations.append("Improve quality standards to meet minimum threshold")
        
        if autonomy_score < 60:
            recommendations.append("Develop unique cultural identity")
            recommendations.append("Create world-specific patterns and workflows")
        
        if harmony_score < 60:
            recommendations.append("Increase collaboration with other worlds")
            recommendations.append("Participate in more cross-world projects")
        
        if not recommendations:
            recommendations.append("Alignment is excellent - continue current trajectory")
        
        return recommendations
    
    def close(self):
        """Close database session."""
        self.session.close()


# ============================================================================
# UNIFIED GOVERNANCE INTERFACE
# ============================================================================

class MultiWorldGovernanceSystem:
    """
    Unified interface to the complete Multi-World Governance System.
    
    Provides access to all 4 components:
    - CCW: Cosmic Council of Worlds
    - IWVS: Inter-World Voting System
    - IWRP: Inter-World Resolution Protocol
    - CAF: Cosmic Alignment Framework
    """
    
    def __init__(self):
        self.ccw = CosmicCouncilOfWorlds()
        self.iwvs = InterWorldVotingSystem(self.ccw)
        self.iwrp = InterWorldResolutionProtocol(self.ccw, self.iwvs)
        self.caf = CosmicAlignmentFramework()
    
    def get_governance_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the governance system."""
        council_comp = self.ccw.get_council_composition()
        
        return {
            "governance_name": "Multi-World Governance System",
            "status": "operational",
            "components": {
                "ccw": f"Cosmic Council of Worlds - {council_comp['total_worlds_represented']} worlds represented",
                "iwvs": f"Inter-World Voting System - {len(self.iwvs.proposals)} proposals",
                "iwrp": f"Inter-World Resolution Protocol - {len(self.iwrp.disputes)} disputes",
                "caf": "Cosmic Alignment Framework - Monitoring alignment"
            },
            "council_composition": council_comp,
            "active_proposals": len([p for p in self.iwvs.proposals.values() if p.status == "open"]),
            "active_disputes": len([d for d in self.iwrp.disputes.values() if d.status in ["open", "mediation", "voting"]]),
            "capabilities": [
                "Democratic decision-making",
                "Weighted voting",
                "Dispute resolution",
                "Alignment monitoring",
                "Sovereign escalation",
                "Multi-threshold voting",
                "Representative governance"
            ]
        }
    
    def close(self):
        """Close all sessions."""
        self.ccw.close()
        self.caf.close()
