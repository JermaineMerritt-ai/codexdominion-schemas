"""
🔥 PHASE 60 — STEP 4: WORLD EVOLUTION ENGINE
Each world gains the ability to evolve independently, intelligently, and in alignment with the Dominion.

This module implements the 4-layer evolution system:
1. Local Evolution Loops - Internal improvement cycles per world
2. World-Specific Agent Generation - Worlds create specialized agents
3. World-Level Style Evolution - Creative style adaptation
4. Cosmic Evolution Synchronization - Prevent drift/destabilization

This is the moment worlds gain their own life cycles.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import uuid
import json

from db import SessionLocal
from models import Agent
from multiworld_schema import World, WorldAgent
from inter_world_network import InterWorldNetwork, MessageType


# ============================================================================
# LAYER 1 — LOCAL EVOLUTION LOOPS
# ============================================================================

class EvolutionPhase(Enum):
    """Phases in the local evolution loop."""
    OBSERVATION = "observation"         # Monitor patterns
    ANALYSIS = "analysis"               # Identify opportunities
    PROPOSAL = "proposal"               # Draft improvement
    REVIEW = "review"                   # Council debate
    IMPLEMENTATION = "implementation"   # Update workflows
    MEMORY_UPDATE = "memory_update"     # Log the change


class EvolutionProposal:
    """A proposal for world improvement."""
    
    def __init__(
        self,
        proposal_id: str,
        world_id: str,
        title: str,
        description: str,
        category: str,  # "workflow", "technique", "pattern", "platform", "agent"
        proposed_by_agent: str,
        impact_scope: str = "local",  # "local", "network", "cosmic"
        priority: str = "medium"
    ):
        self.proposal_id = proposal_id
        self.world_id = world_id
        self.title = title
        self.description = description
        self.category = category
        self.proposed_by_agent = proposed_by_agent
        self.impact_scope = impact_scope
        self.priority = priority
        self.status = "proposed"  # proposed, under_review, approved, rejected, implemented
        self.observations: List[Dict[str, Any]] = []
        self.analysis: Dict[str, Any] = {}
        self.council_votes: Dict[str, str] = {}  # agent_id -> vote
        self.implementation_notes = None
        self.created_at = datetime.utcnow()
        self.implemented_at = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "proposal_id": self.proposal_id,
            "world_id": self.world_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "proposed_by_agent": self.proposed_by_agent,
            "impact_scope": self.impact_scope,
            "priority": self.priority,
            "status": self.status,
            "observations": self.observations,
            "analysis": self.analysis,
            "council_votes": self.council_votes,
            "implementation_notes": self.implementation_notes,
            "created_at": self.created_at.isoformat(),
            "implemented_at": self.implemented_at.isoformat() if self.implemented_at else None
        }


class LocalEvolutionLoop:
    """
    LAYER 1: Internal improvement cycle for each world.
    
    6-Phase Loop:
    1. Observation - Agents monitor patterns
    2. Analysis - Identify opportunities/inefficiencies
    3. Proposal - Innovation Scout drafts improvement
    4. Review - World council debates and votes
    5. Implementation - Update workflows/techniques
    6. Memory Update - Log change in cultural memory
    """
    
    def __init__(self, world_id: str):
        self.world_id = world_id
        self.session = SessionLocal()
        self.proposals: Dict[str, EvolutionProposal] = {}
        self.evolution_history: List[Dict[str, Any]] = []
    
    def phase_1_observe(
        self,
        observation_type: str,
        observation_data: Dict[str, Any],
        observed_by_agent: str
    ) -> Dict[str, Any]:
        """
        Phase 1: Observation
        
        Agents monitor patterns in their domain:
        - Performance metrics
        - Quality trends
        - Audience feedback
        - Platform changes
        - Competitive analysis
        """
        observation = {
            "observation_id": f"obs_{uuid.uuid4().hex[:12]}",
            "observation_type": observation_type,
            "data": observation_data,
            "observed_by": observed_by_agent,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return observation
    
    def phase_2_analyze(
        self,
        observations: List[Dict[str, Any]],
        analyzed_by_agent: str
    ) -> Dict[str, Any]:
        """
        Phase 2: Analysis
        
        Identify:
        - Inefficiencies in workflow
        - Opportunities for improvement
        - Emerging trends
        - Quality gaps
        - Resource bottlenecks
        """
        analysis = {
            "analysis_id": f"analysis_{uuid.uuid4().hex[:12]}",
            "observations_count": len(observations),
            "patterns_identified": [],
            "opportunities": [],
            "risks": [],
            "recommendations": [],
            "analyzed_by": analyzed_by_agent,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Analyze observations to identify patterns
        for obs in observations:
            obs_type = obs.get("observation_type", "")
            
            if "performance" in obs_type.lower():
                analysis["patterns_identified"].append(f"Performance pattern: {obs_type}")
            elif "quality" in obs_type.lower():
                analysis["patterns_identified"].append(f"Quality pattern: {obs_type}")
            elif "trend" in obs_type.lower():
                analysis["patterns_identified"].append(f"Market trend: {obs_type}")
        
        return analysis
    
    def phase_3_propose(
        self,
        title: str,
        description: str,
        category: str,
        observations: List[Dict[str, Any]],
        analysis: Dict[str, Any],
        proposed_by_agent: str,
        impact_scope: str = "local",
        priority: str = "medium"
    ) -> EvolutionProposal:
        """
        Phase 3: Proposal
        
        Innovation Scout drafts improvement proposal:
        - Clear title and description
        - Supporting observations
        - Analysis rationale
        - Expected impact
        - Implementation plan
        """
        proposal = EvolutionProposal(
            proposal_id=f"evol_{self.world_id}_{uuid.uuid4().hex[:8]}",
            world_id=self.world_id,
            title=title,
            description=description,
            category=category,
            proposed_by_agent=proposed_by_agent,
            impact_scope=impact_scope,
            priority=priority
        )
        
        proposal.observations = observations
        proposal.analysis = analysis
        proposal.status = "under_review"
        
        self.proposals[proposal.proposal_id] = proposal
        
        return proposal
    
    def phase_4_review(
        self,
        proposal_id: str,
        council_votes: Dict[str, str]  # agent_id -> "approve"/"reject"/"abstain"
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Phase 4: World Council Review
        
        Local council debates and votes:
        - Creative representative
        - Continuity representative
        - Operations representative
        - Simple majority (2/3) required
        """
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found")
        
        proposal.council_votes = council_votes
        
        # Tally votes
        approve_count = sum(1 for v in council_votes.values() if v == "approve")
        reject_count = sum(1 for v in council_votes.values() if v == "reject")
        total_votes = approve_count + reject_count  # Exclude abstentions
        
        # Simple majority
        approved = approve_count > (total_votes / 2) if total_votes > 0 else False
        
        if approved:
            proposal.status = "approved"
        else:
            proposal.status = "rejected"
        
        review_result = {
            "proposal_id": proposal_id,
            "votes_cast": len(council_votes),
            "approve": approve_count,
            "reject": reject_count,
            "approved": approved,
            "status": proposal.status
        }
        
        return approved, review_result
    
    def phase_5_implement(
        self,
        proposal_id: str,
        implementation_notes: str
    ) -> Dict[str, Any]:
        """
        Phase 5: Implementation
        
        Update world's:
        - Workflows
        - Techniques
        - Patterns
        - Agent behaviors
        - Cultural markers
        """
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found")
        
        if proposal.status != "approved":
            raise ValueError(f"Proposal {proposal_id} not approved")
        
        proposal.implementation_notes = implementation_notes
        proposal.status = "implemented"
        proposal.implemented_at = datetime.utcnow()
        
        # Update world in database (simplified)
        world = self.session.query(World).filter_by(id=self.world_id).first()
        if world:
            # Increment evolution cycle count
            if world.economy_config:
                evolution_count = world.economy_config.get("evolution_cycles_completed", 0)
                world.economy_config["evolution_cycles_completed"] = evolution_count + 1
                world.economy_config["last_evolution"] = datetime.utcnow().isoformat()
            
            self.session.commit()
        
        implementation_result = {
            "proposal_id": proposal_id,
            "implemented_at": proposal.implemented_at.isoformat(),
            "category": proposal.category,
            "impact_scope": proposal.impact_scope,
            "notes": implementation_notes
        }
        
        return implementation_result
    
    def phase_6_memory_update(
        self,
        proposal_id: str,
        memory_entry: str
    ):
        """
        Phase 6: Memory Update
        
        Cultural Memory Keeper logs the change:
        - What evolved
        - Why it evolved
        - Who proposed it
        - Impact observed
        - Lineage connection
        """
        proposal = self.proposals.get(proposal_id)
        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found")
        
        evolution_record = {
            "proposal_id": proposal_id,
            "title": proposal.title,
            "category": proposal.category,
            "memory_entry": memory_entry,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.evolution_history.append(evolution_record)
        
        # Update world's cultural memory
        world = self.session.query(World).filter_by(id=self.world_id).first()
        if world and world.culture:
            if "evolution_history" not in world.culture:
                world.culture["evolution_history"] = []
            world.culture["evolution_history"].append(evolution_record)
            self.session.commit()
    
    def get_evolution_status(self) -> Dict[str, Any]:
        """Get current evolution status for this world."""
        return {
            "world_id": self.world_id,
            "active_proposals": len([p for p in self.proposals.values() if p.status in ["proposed", "under_review", "approved"]]),
            "implemented_proposals": len([p for p in self.proposals.values() if p.status == "implemented"]),
            "total_evolution_cycles": len(self.evolution_history),
            "recent_proposals": [p.to_dict() for p in list(self.proposals.values())[-5:]]
        }
    
    def close(self):
        """Close database session."""
        self.session.close()


# ============================================================================
# LAYER 2 — WORLD-SPECIFIC AGENT GENERATION
# ============================================================================

class AgentGenerationTemplate:
    """Template for generating new specialized agents."""
    
    def __init__(
        self,
        template_id: str,
        world_id: str,
        role_name: str,
        role_description: str,
        specialization: str,
        base_reputation: float = 50.0,
        initial_capabilities: List[str] = None
    ):
        self.template_id = template_id
        self.world_id = world_id
        self.role_name = role_name
        self.role_description = role_description
        self.specialization = specialization
        self.base_reputation = base_reputation
        self.initial_capabilities = initial_capabilities or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "template_id": self.template_id,
            "world_id": self.world_id,
            "role_name": self.role_name,
            "role_description": self.role_description,
            "specialization": self.specialization,
            "base_reputation": self.base_reputation,
            "initial_capabilities": self.initial_capabilities
        }


class WorldSpecificAgentGenerator:
    """
    LAYER 2: Generate new agents tailored to each world's purpose.
    
    Examples:
    - Children's Story World: Emotion-Clarity Specialist, Moral-Arc Advisor
    - Music World: Rhythm Evolution Agent, Genre-Fusion Composer
    - Branding World: Identity Pattern Analyst, Audience Resonance Mapper
    
    Each world grows its own population.
    """
    
    def __init__(self, world_id: str):
        self.world_id = world_id
        self.session = SessionLocal()
        self.agent_templates: Dict[str, AgentGenerationTemplate] = {}
    
    def create_agent_template(
        self,
        role_name: str,
        role_description: str,
        specialization: str,
        base_reputation: float = 50.0,
        initial_capabilities: List[str] = None
    ) -> AgentGenerationTemplate:
        """
        Create a template for a new agent role in this world.
        """
        template = AgentGenerationTemplate(
            template_id=f"template_{self.world_id}_{uuid.uuid4().hex[:8]}",
            world_id=self.world_id,
            role_name=role_name,
            role_description=role_description,
            specialization=specialization,
            base_reputation=base_reputation,
            initial_capabilities=initial_capabilities or []
        )
        
        self.agent_templates[template.template_id] = template
        
        return template
    
    def generate_agent_from_template(
        self,
        template_id: str,
        agent_name: str
    ) -> Tuple[Agent, WorldAgent]:
        """
        Generate a new agent from a template.
        
        Returns both Agent and WorldAgent records.
        """
        template = self.agent_templates.get(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        # Create Agent record
        agent = Agent(
            id=f"agent_{self.world_id}_{uuid.uuid4().hex[:8]}",
            name=agent_name,
            display_name=agent_name,
            description=template.role_description,
            is_active=True,
            capabilities={
                "role": template.role_name,
                "specialization": template.specialization,
                "base_reputation": template.base_reputation,
                "initial_capabilities": template.initial_capabilities
            }
        )
        
        self.session.add(agent)
        
        # Create WorldAgent record
        world_agent = WorldAgent(
            id=f"wa_{uuid.uuid4().hex[:12]}",
            world_id=self.world_id,
            agent_id=agent.id,
            role=template.role_name,
            citizenship_status="citizen",  # Generated agents are citizens
            world_reputation=template.base_reputation,
            contributions=0,
            specialization=template.specialization,
            arrival_date=datetime.utcnow()
        )
        
        self.session.add(world_agent)
        
        # Update world population
        world = self.session.query(World).filter_by(id=self.world_id).first()
        if world:
            world.population += 1
            world.last_population_change = datetime.utcnow()
        
        self.session.commit()
        
        return agent, world_agent
    
    def get_world_population_growth(self) -> Dict[str, Any]:
        """Get statistics on world's population growth."""
        world = self.session.query(World).filter_by(id=self.world_id).first()
        if not world:
            return {}
        
        world_agents = self.session.query(WorldAgent).filter_by(world_id=self.world_id).all()
        
        founding_citizens = sum(1 for wa in world_agents if wa.citizenship_status == "citizen" and wa.origin_world_id is None)
        generated_agents = sum(1 for wa in world_agents if wa.citizenship_status == "citizen" and wa.origin_world_id is not None)
        
        return {
            "world_id": self.world_id,
            "world_name": world.name,
            "total_population": world.population,
            "founding_citizens": founding_citizens,
            "generated_agents": generated_agents,
            "growth_rate": (generated_agents / founding_citizens * 100) if founding_citizens > 0 else 0,
            "templates_created": len(self.agent_templates)
        }
    
    def close(self):
        """Close database session."""
        self.session.close()


# ============================================================================
# LAYER 3 — WORLD-LEVEL STYLE EVOLUTION
# ============================================================================

class StyleEvolutionProposal:
    """A proposal to evolve world's creative style."""
    
    def __init__(
        self,
        style_proposal_id: str,
        world_id: str,
        style_aspect: str,  # "palette", "tone", "pacing", "complexity", "emotional_arc"
        current_value: Any,
        proposed_value: Any,
        rationale: str,
        proposed_by_agent: str
    ):
        self.style_proposal_id = style_proposal_id
        self.world_id = world_id
        self.style_aspect = style_aspect
        self.current_value = current_value
        self.proposed_value = proposed_value
        self.rationale = rationale
        self.proposed_by_agent = proposed_by_agent
        self.status = "proposed"
        self.approval_votes = 0
        self.rejection_votes = 0
        self.created_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "style_proposal_id": self.style_proposal_id,
            "world_id": self.world_id,
            "style_aspect": self.style_aspect,
            "current_value": self.current_value,
            "proposed_value": self.proposed_value,
            "rationale": self.rationale,
            "proposed_by_agent": self.proposed_by_agent,
            "status": self.status,
            "approval_votes": self.approval_votes,
            "rejection_votes": self.rejection_votes,
            "created_at": self.created_at.isoformat()
        }


class WorldStyleEvolution:
    """
    LAYER 3: Evolution of world's creative style.
    
    Examples:
    - Children's Story World: Shift to softer palettes, simpler arcs
    - Motion Graphics World: Adopt new animation rhythms
    - Faith-Inspiration World: Refine tone for clarity and warmth
    
    Worlds evolve organically based on purpose and history.
    """
    
    def __init__(self, world_id: str):
        self.world_id = world_id
        self.session = SessionLocal()
        self.style_proposals: Dict[str, StyleEvolutionProposal] = {}
    
    def propose_style_evolution(
        self,
        style_aspect: str,
        current_value: Any,
        proposed_value: Any,
        rationale: str,
        proposed_by_agent: str
    ) -> StyleEvolutionProposal:
        """
        Propose a change to world's creative style.
        """
        proposal = StyleEvolutionProposal(
            style_proposal_id=f"style_{self.world_id}_{uuid.uuid4().hex[:8]}",
            world_id=self.world_id,
            style_aspect=style_aspect,
            current_value=current_value,
            proposed_value=proposed_value,
            rationale=rationale,
            proposed_by_agent=proposed_by_agent
        )
        
        self.style_proposals[proposal.style_proposal_id] = proposal
        
        return proposal
    
    def vote_on_style_proposal(
        self,
        style_proposal_id: str,
        vote: str  # "approve" or "reject"
    ):
        """
        Vote on a style evolution proposal.
        """
        proposal = self.style_proposals.get(style_proposal_id)
        if not proposal:
            raise ValueError(f"Style proposal {style_proposal_id} not found")
        
        if vote == "approve":
            proposal.approval_votes += 1
        elif vote == "reject":
            proposal.rejection_votes += 1
    
    def apply_style_evolution(
        self,
        style_proposal_id: str
    ) -> Dict[str, Any]:
        """
        Apply an approved style evolution to the world.
        """
        proposal = self.style_proposals.get(style_proposal_id)
        if not proposal:
            raise ValueError(f"Style proposal {style_proposal_id} not found")
        
        # Check approval
        total_votes = proposal.approval_votes + proposal.rejection_votes
        approval_rate = proposal.approval_votes / total_votes if total_votes > 0 else 0
        
        if approval_rate < 0.5:
            proposal.status = "rejected"
            return {"status": "rejected", "approval_rate": approval_rate}
        
        proposal.status = "applied"
        
        # Update world's culture
        world = self.session.query(World).filter_by(id=self.world_id).first()
        if world and world.culture:
            if "style_evolution_history" not in world.culture:
                world.culture["style_evolution_history"] = []
            
            evolution_record = {
                "aspect": proposal.style_aspect,
                "from": proposal.current_value,
                "to": proposal.proposed_value,
                "rationale": proposal.rationale,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            world.culture["style_evolution_history"].append(evolution_record)
            
            # Update current style patterns
            if "current_style" not in world.culture:
                world.culture["current_style"] = {}
            world.culture["current_style"][proposal.style_aspect] = proposal.proposed_value
            
            self.session.commit()
        
        return {
            "status": "applied",
            "approval_rate": approval_rate,
            "evolution_record": evolution_record
        }
    
    def get_style_evolution_history(self) -> List[Dict[str, Any]]:
        """Get complete style evolution history for this world."""
        world = self.session.query(World).filter_by(id=self.world_id).first()
        if not world or not world.culture:
            return []
        
        return world.culture.get("style_evolution_history", [])
    
    def close(self):
        """Close database session."""
        self.session.close()


# ============================================================================
# LAYER 4 — COSMIC EVOLUTION SYNCHRONIZATION
# ============================================================================

class CosmicEvolutionSynchronizer:
    """
    LAYER 4: Safeguards to maintain cosmic coherence.
    
    Ensures:
    - No world drifts too far from identity
    - No world contradicts core values
    - No world destabilizes the constellation
    - No world harms others through evolution
    
    Synchronizes:
    - Identity updates
    - Lineage updates
    - Creative breakthroughs
    - Evolution proposals
    - Cross-world improvements
    """
    
    def __init__(self):
        self.session = SessionLocal()
        self.network = InterWorldNetwork()
        
        # Core identity standards all worlds must maintain
        self.core_identity_standards = {
            "quality_minimum": 70.0,
            "child_safety_absolute": True,
            "brand_essence": "The Flame Burns Sovereign and Eternal",
            "core_values": [
                "excellence",
                "identity",
                "innovation",
                "collaboration",
                "safety",
                "imagination"
            ]
        }
        
        # Maximum drift thresholds
        self.drift_thresholds = {
            "quality_drop_max": 15.0,  # Max quality drop before intervention
            "identity_alignment_min": 60.0,  # Min identity score
            "collaboration_index_min": 40.0,  # Min collaboration
            "evolution_frequency_max": 10  # Max evolutions per month
        }
    
    def validate_evolution_proposal(
        self,
        world_id: str,
        proposal: EvolutionProposal
    ) -> Tuple[bool, List[str]]:
        """
        Validate evolution proposal against cosmic standards.
        
        Returns:
        - is_valid: bool
        - violations: List[str] (empty if valid)
        """
        violations = []
        
        world = self.session.query(World).filter_by(id=world_id).first()
        if not world:
            violations.append("World not found")
            return False, violations
        
        # Check impact scope
        if proposal.impact_scope == "cosmic":
            violations.append("Cosmic-level changes require sovereign approval")
        
        # Check if world has evolved too frequently
        if world.economy_config:
            recent_evolutions = world.economy_config.get("evolution_cycles_completed", 0)
            if recent_evolutions > self.drift_thresholds["evolution_frequency_max"]:
                violations.append(f"Evolution frequency exceeds limit ({recent_evolutions}/month)")
        
        # Check if proposal affects core identity
        if proposal.category in ["identity", "values", "brand"]:
            violations.append("Core identity changes require sovereign approval")
        
        is_valid = len(violations) == 0
        return is_valid, violations
    
    def validate_style_evolution(
        self,
        world_id: str,
        style_proposal: StyleEvolutionProposal
    ) -> Tuple[bool, List[str]]:
        """
        Validate style evolution against cosmic standards.
        """
        violations = []
        
        world = self.session.query(World).filter_by(id=world_id).first()
        if not world:
            violations.append("World not found")
            return False, violations
        
        # Check if style change affects child safety
        if "safety" in style_proposal.style_aspect.lower():
            violations.append("Safety-related changes require sovereign approval")
        
        # Check if style change contradicts brand essence
        if "brand" in style_proposal.style_aspect.lower() or "identity" in style_proposal.style_aspect.lower():
            violations.append("Brand identity changes require sovereign approval")
        
        is_valid = len(violations) == 0
        return is_valid, violations
    
    def synchronize_evolution_to_network(
        self,
        world_id: str,
        evolution_type: str,
        evolution_data: Dict[str, Any]
    ):
        """
        Broadcast evolution to Inter-World Network.
        
        Types:
        - "innovation" - New technique/pattern
        - "style_change" - Style evolution
        - "agent_generation" - New agent role created
        - "workflow_update" - Process improvement
        """
        world = self.session.query(World).filter_by(id=world_id).first()
        if not world:
            return
        
        # Broadcast via Inter-World Network
        message_content = {
            "evolution_type": evolution_type,
            "world_id": world_id,
            "world_name": world.name,
            "data": evolution_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Use innovation broadcast from IWN
        self.network.cms.sync_innovation(
            originating_world_id=world_id,
            innovation_type=evolution_type,
            innovation_data=evolution_data
        )
    
    def detect_world_drift(
        self,
        world_id: str
    ) -> Dict[str, Any]:
        """
        Detect if a world is drifting from cosmic alignment.
        
        Returns drift report with recommendations.
        """
        world = self.session.query(World).filter_by(id=world_id).first()
        if not world:
            return {"error": "World not found"}
        
        drift_detected = False
        drift_factors = []
        recommendations = []
        
        # Check quality drift
        if world.creative_output_quality < self.core_identity_standards["quality_minimum"]:
            drift_detected = True
            drift_factors.append(f"Quality below minimum ({world.creative_output_quality} < {self.core_identity_standards['quality_minimum']})")
            recommendations.append("Improve quality standards and review processes")
        
        # Check collaboration drift
        if world.collaboration_index < self.drift_thresholds["collaboration_index_min"]:
            drift_detected = True
            drift_factors.append(f"Collaboration too low ({world.collaboration_index})")
            recommendations.append("Increase participation in cross-world projects")
        
        # Check evolution frequency
        if world.economy_config:
            recent_evolutions = world.economy_config.get("evolution_cycles_completed", 0)
            if recent_evolutions > self.drift_thresholds["evolution_frequency_max"]:
                drift_detected = True
                drift_factors.append(f"Evolution too rapid ({recent_evolutions} cycles)")
                recommendations.append("Slow down evolution pace to ensure stability")
        
        severity = "none"
        if len(drift_factors) >= 3:
            severity = "critical"
        elif len(drift_factors) >= 2:
            severity = "high"
        elif len(drift_factors) == 1:
            severity = "medium"
        
        return {
            "world_id": world_id,
            "world_name": world.name,
            "drift_detected": drift_detected,
            "severity": severity,
            "drift_factors": drift_factors,
            "recommendations": recommendations,
            "requires_intervention": severity in ["critical", "high"]
        }
    
    def get_cosmic_evolution_status(self) -> Dict[str, Any]:
        """Get status of evolution across the entire cosmos."""
        all_worlds = self.session.query(World).all()
        
        total_evolutions = 0
        worlds_evolving = 0
        worlds_drifting = 0
        
        for world in all_worlds:
            if world.economy_config:
                evolutions = world.economy_config.get("evolution_cycles_completed", 0)
                total_evolutions += evolutions
                if evolutions > 0:
                    worlds_evolving += 1
            
            # Check for drift
            drift_report = self.detect_world_drift(world.id)
            if drift_report["drift_detected"]:
                worlds_drifting += 1
        
        return {
            "total_worlds": len(all_worlds),
            "worlds_evolving": worlds_evolving,
            "total_evolutions": total_evolutions,
            "avg_evolutions_per_world": total_evolutions / len(all_worlds) if all_worlds else 0,
            "worlds_drifting": worlds_drifting,
            "drift_percentage": (worlds_drifting / len(all_worlds) * 100) if all_worlds else 0,
            "cosmic_health": "good" if worlds_drifting == 0 else "needs_attention"
        }
    
    def close(self):
        """Close sessions."""
        self.session.close()
        self.network.close()


# ============================================================================
# UNIFIED WORLD EVOLUTION ENGINE
# ============================================================================

class WorldEvolutionEngine:
    """
    Unified interface to the complete World Evolution Engine.
    
    Provides access to all 4 layers:
    - Layer 1: Local Evolution Loops
    - Layer 2: World-Specific Agent Generation
    - Layer 3: World-Level Style Evolution
    - Layer 4: Cosmic Evolution Synchronization
    """
    
    def __init__(self, world_id: str):
        self.world_id = world_id
        self.evolution_loop = LocalEvolutionLoop(world_id)
        self.agent_generator = WorldSpecificAgentGenerator(world_id)
        self.style_evolution = WorldStyleEvolution(world_id)
        self.synchronizer = CosmicEvolutionSynchronizer()
    
    def get_evolution_status(self) -> Dict[str, Any]:
        """Get comprehensive evolution status for this world."""
        loop_status = self.evolution_loop.get_evolution_status()
        population_growth = self.agent_generator.get_world_population_growth()
        style_history = self.style_evolution.get_style_evolution_history()
        drift_report = self.synchronizer.detect_world_drift(self.world_id)
        
        return {
            "world_id": self.world_id,
            "evolution_engine_status": "operational",
            "layers": {
                "local_evolution_loops": {
                    "active_proposals": loop_status["active_proposals"],
                    "implemented_proposals": loop_status["implemented_proposals"],
                    "total_cycles": loop_status["total_evolution_cycles"]
                },
                "agent_generation": {
                    "total_population": population_growth["total_population"],
                    "generated_agents": population_growth["generated_agents"],
                    "templates_created": population_growth["templates_created"]
                },
                "style_evolution": {
                    "style_changes": len(style_history),
                    "active_proposals": len([p for p in self.style_evolution.style_proposals.values() if p.status == "proposed"])
                },
                "cosmic_sync": {
                    "drift_detected": drift_report["drift_detected"],
                    "drift_severity": drift_report["severity"],
                    "requires_intervention": drift_report["requires_intervention"]
                }
            },
            "capabilities": [
                "Observe patterns",
                "Analyze opportunities",
                "Propose improvements",
                "Council review",
                "Implement changes",
                "Update memory",
                "Generate new agents",
                "Evolve creative style",
                "Synchronize with cosmos"
            ]
        }
    
    def close(self):
        """Close all sessions."""
        self.evolution_loop.close()
        self.agent_generator.close()
        self.style_evolution.close()
        self.synchronizer.close()
