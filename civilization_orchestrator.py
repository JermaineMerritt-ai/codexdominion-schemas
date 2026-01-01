"""
🔥 CIVILIZATION ORCHESTRATOR - THE INTEGRATION ENGINE 🔥
=========================================================
The central coordination system that connects:
- Agents (the population)
- Councils (the government)
- Cultural Memory (the identity)
- Evolution Engine (the growth mechanism)

This transforms separate components into one living, breathing civilization.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import uuid

from db import SessionLocal
from models import (
    Agent, Council, IdentityCodex, StylePattern, CulturalMemory,
    EvolutionProposal, AgentGenerationProposal, TechniqueEvolution,
    AgentCollaboration, ProposalWorkflow, KnowledgeAccess,
    IntegrationEvent, CivilizationMetrics
)


class CivilizationOrchestrator:
    """
    The Integration Engine - Civilization's Central Nervous System
    
    Coordinates all four pillars:
    1. Agents collaborate using social layer
    2. Councils govern through proposal routing
    3. Cultural Memory informs all decisions
    4. Evolution Engine improves the system
    """
    
    def __init__(self):
        self.session = SessionLocal()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
    
    # ========================================================================
    # PILLAR 1: AGENT SOCIAL LAYER
    # ========================================================================
    
    def initiate_collaboration(
        self,
        project_name: str,
        project_type: str,
        lead_agent_id: str,
        collaborating_agent_ids: List[str],
        project_goal: str
    ) -> str:
        """
        Agents begin working together on a project.
        
        This is where agents stop being isolated roles and become a society.
        They collaborate, debate, share ideas, and reference cultural memory together.
        """
        collaboration_id = f"collab_{uuid.uuid4().hex[:12]}"
        
        # Create collaboration record
        collaboration = AgentCollaboration(
            id=collaboration_id,
            project_name=project_name,
            project_type=project_type,
            lead_agent_id=lead_agent_id,
            collaborating_agents=collaborating_agent_ids,
            contributions={},
            debates=[],
            consensus_reached=False,
            deliverable={},
            impact={},
            status="active",
            cultural_memory_refs=[]
        )
        
        self.session.add(collaboration)
        
        # Log integration event
        event = IntegrationEvent(
            id=f"event_{uuid.uuid4().hex[:12]}",
            event_type="collaboration_started",
            title=f"Collaboration: {project_name}",
            description=project_goal,
            involved_agents=[lead_agent_id] + collaborating_agent_ids,
            collaboration_id=collaboration_id,
            impact_areas=["agent_social_layer"],
            significance="normal"
        )
        
        self.session.add(event)
        self.session.commit()
        
        return collaboration_id
    
    def add_collaboration_contribution(
        self,
        collaboration_id: str,
        agent_id: str,
        contribution_type: str,
        content: Dict[str, Any]
    ):
        """Agent contributes to collaborative project"""
        collaboration = self.session.query(AgentCollaboration).filter_by(
            id=collaboration_id
        ).first()
        
        if not collaboration:
            raise ValueError(f"Collaboration {collaboration_id} not found")
        
        # Add contribution
        if not collaboration.contributions:
            collaboration.contributions = {}
        
        if agent_id not in collaboration.contributions:
            collaboration.contributions[agent_id] = []
        
        collaboration.contributions[agent_id].append({
            "type": contribution_type,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        self.session.commit()
    
    def record_collaboration_debate(
        self,
        collaboration_id: str,
        debating_agents: List[str],
        topic: str,
        positions: Dict[str, str],
        resolution: Optional[str] = None
    ):
        """
        Record debates between agents - the dialectic process.
        
        This is where agents challenge each other and refine ideas.
        """
        collaboration = self.session.query(AgentCollaboration).filter_by(
            id=collaboration_id
        ).first()
        
        if not collaboration:
            raise ValueError(f"Collaboration {collaboration_id} not found")
        
        debate_record = {
            "topic": topic,
            "participants": debating_agents,
            "positions": positions,
            "resolution": resolution,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if not collaboration.debates:
            collaboration.debates = []
        
        collaboration.debates.append(debate_record)
        
        if resolution:
            collaboration.consensus_reached = True
        
        self.session.commit()
    
    def complete_collaboration(
        self,
        collaboration_id: str,
        deliverable: Dict[str, Any],
        measured_impact: Dict[str, Any]
    ) -> Optional[str]:
        """
        Complete collaboration and optionally create cultural memory.
        
        If the work produced valuable lessons, it becomes part of the shared brain.
        """
        collaboration = self.session.query(AgentCollaboration).filter_by(
            id=collaboration_id
        ).first()
        
        if not collaboration:
            raise ValueError(f"Collaboration {collaboration_id} not found")
        
        collaboration.status = "completed"
        collaboration.deliverable = deliverable
        collaboration.impact = measured_impact
        collaboration.completed_at = datetime.utcnow()
        
        # If significant, create cultural memory
        memory_id = None
        if measured_impact.get("create_cultural_memory", False):
            memory_id = self._create_memory_from_collaboration(collaboration)
            collaboration.created_memory_id = memory_id
        
        # Log event
        event = IntegrationEvent(
            id=f"event_{uuid.uuid4().hex[:12]}",
            event_type="collaboration_completed",
            title=f"Completed: {collaboration.project_name}",
            description=f"Collaboration produced valuable outcomes",
            involved_agents=[collaboration.lead_agent_id] + collaboration.collaborating_agents,
            collaboration_id=collaboration_id,
            cultural_memory_id=memory_id,
            impact_areas=["agent_social_layer", "cultural_memory"],
            significance="high" if memory_id else "normal"
        )
        
        self.session.add(event)
        self.session.commit()
        
        return memory_id
    
    def _create_memory_from_collaboration(self, collaboration: AgentCollaboration) -> str:
        """Extract lessons from collaboration and store in cultural memory"""
        memory_id = f"memory_collab_{uuid.uuid4().hex[:12]}"
        
        memory = CulturalMemory(
            id=memory_id,
            memory_type="lesson",
            title=f"Lessons from: {collaboration.project_name}",
            content=f"Collaborative effort produced: {collaboration.deliverable.get('summary', 'N/A')}",
            tags=["collaboration", collaboration.project_type],
            context={
                "collaboration_id": collaboration.id,
                "participants": [collaboration.lead_agent_id] + collaboration.collaborating_agents,
                "debates": len(collaboration.debates) if collaboration.debates else 0
            },
            source_project_id=collaboration.id,
            times_referenced=0
        )
        
        self.session.add(memory)
        return memory_id
    
    # ========================================================================
    # PILLAR 2: COUNCIL AS CENTRAL NERVOUS SYSTEM
    # ========================================================================
    
    def submit_proposal(
        self,
        proposal_type: str,
        originating_agent_id: str,
        title: str,
        description: str,
        rationale: str,
        expected_impact: Dict[str, Any],
        source_collaboration_id: Optional[str] = None
    ) -> str:
        """
        Agent submits proposal for council review.
        
        This auto-routes to the appropriate council based on domain.
        Council becomes the decision-making layer, not you.
        """
        # Determine which council should review
        council_id, routing_reason = self._route_proposal_to_council(
            proposal_type, expected_impact
        )
        
        proposal_id = f"prop_{uuid.uuid4().hex[:12]}"
        
        proposal = ProposalWorkflow(
            id=proposal_id,
            proposal_type=proposal_type,
            originating_agent_id=originating_agent_id,
            source_collaboration_id=source_collaboration_id,
            title=title,
            description=description,
            rationale=rationale,
            expected_impact=expected_impact,
            assigned_council_id=council_id,
            routing_reason=routing_reason,
            review_status="pending"
        )
        
        self.session.add(proposal)
        
        # Validate against identity
        identity_passed, concerns = self._validate_identity_alignment(proposal)
        proposal.identity_check_passed = identity_passed
        if concerns:
            proposal.identity_concerns = concerns
        
        # Log event
        event = IntegrationEvent(
            id=f"event_{uuid.uuid4().hex[:12]}",
            event_type="proposal_submitted",
            title=f"Proposal: {title}",
            description=f"Routed to {council_id} for review",
            involved_agents=[originating_agent_id],
            involved_councils=[council_id],
            proposal_id=proposal_id,
            impact_areas=["council_governance", "proposal_routing"],
            significance="high" if not identity_passed else "normal"
        )
        
        self.session.add(event)
        self.session.commit()
        
        return proposal_id
    
    def _route_proposal_to_council(
        self,
        proposal_type: str,
        expected_impact: Dict[str, Any]
    ) -> tuple[str, str]:
        """
        Intelligent proposal routing based on type and impact.
        
        This is the council's nervous system - proposals go to the right place.
        """
        # Strategic decisions → High Council
        if proposal_type in ["agent_generation", "major_evolution", "policy_change"]:
            return "council_high", "Strategic decision requiring High Council oversight"
        
        # Identity/brand concerns → Continuity Council
        if proposal_type in ["brand_evolution", "identity_refinement", "cultural_change"]:
            return "council_continuity", "Identity-related decision under Continuity Council domain"
        
        # Operational improvements → Operations Council
        if proposal_type in ["workflow_optimization", "technique_evolution", "process_improvement"]:
            return "council_operations", "Operational efficiency falls under Operations Council"
        
        # Default to High Council for ambiguous cases
        return "council_high", "Routed to High Council for strategic evaluation"
    
    def _validate_identity_alignment(self, proposal: ProposalWorkflow) -> tuple[bool, Optional[List[str]]]:
        """
        Check if proposal aligns with identity principles.
        
        This protects the Dominion's soul.
        """
        # Query identity codex
        identity_principles = self.session.query(IdentityCodex).all()
        
        concerns = []
        
        # Check for red flags in description
        for principle in identity_principles:
            # Simple keyword check (in production, use NLP)
            if principle.category == "sacred":
                keywords = ["scripture", "faith", "children", "family"]
                desc_lower = proposal.description.lower()
                
                # If proposal mentions sacred topics, flag for extra review
                if any(kw in desc_lower for kw in keywords):
                    if "accuracy" not in desc_lower and "quality" not in desc_lower:
                        concerns.append(
                            f"Proposal touches on {principle.principle_name} - requires careful review"
                        )
        
        return (len(concerns) == 0, concerns if concerns else None)
    
    def council_vote_on_proposal(
        self,
        proposal_id: str,
        council_member_agent_id: str,
        vote: str,  # approve, reject, request_revision
        notes: Optional[str] = None
    ):
        """Council member votes on proposal"""
        proposal = self.session.query(ProposalWorkflow).filter_by(
            id=proposal_id
        ).first()
        
        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found")
        
        if not proposal.council_votes:
            proposal.council_votes = {}
        
        proposal.council_votes[council_member_agent_id] = {
            "vote": vote,
            "notes": notes,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        proposal.review_status = "under_review"
        
        # Check if we have enough votes for decision
        self._check_voting_threshold(proposal)
        
        self.session.commit()
    
    def _check_voting_threshold(self, proposal: ProposalWorkflow):
        """Determine if enough votes to make decision"""
        if not proposal.council_votes:
            return
        
        votes = list(proposal.council_votes.values())
        total_votes = len(votes)
        
        # Need at least 3 votes (simple majority)
        if total_votes < 3:
            return
        
        approve_count = sum(1 for v in votes if v["vote"] == "approve")
        reject_count = sum(1 for v in votes if v["vote"] == "reject")
        
        # Majority approval
        if approve_count > total_votes / 2:
            proposal.review_status = "approved"
            proposal.approved_at = datetime.utcnow()
        
        # Majority rejection
        elif reject_count > total_votes / 2:
            proposal.review_status = "rejected"
    
    def implement_approved_proposal(
        self,
        proposal_id: str,
        implementation_notes: str
    ):
        """
        Execute approved proposal and log to cultural memory.
        
        This closes the feedback loop - changes are remembered.
        """
        proposal = self.session.query(ProposalWorkflow).filter_by(
            id=proposal_id
        ).first()
        
        if not proposal:
            raise ValueError(f"Proposal {proposal_id} not found")
        
        if proposal.review_status != "approved":
            raise ValueError("Proposal must be approved before implementation")
        
        proposal.implemented_at = datetime.utcnow()
        proposal.implementation_notes = implementation_notes
        
        # Create cultural memory of this decision
        memory_id = f"memory_prop_{uuid.uuid4().hex[:12]}"
        
        memory = CulturalMemory(
            id=memory_id,
            memory_type="milestone",
            title=f"Approved: {proposal.title}",
            content=f"{proposal.description}\n\nOutcome: {implementation_notes}",
            tags=["proposal", proposal.proposal_type],
            context={
                "proposal_id": proposal.id,
                "council": proposal.assigned_council_id,
                "votes": proposal.council_votes
            },
            source_agent_id=proposal.originating_agent_id,
            times_referenced=0
        )
        
        self.session.add(memory)
        
        proposal.logged_to_cultural_memory = True
        proposal.cultural_memory_id = memory_id
        
        # Log event
        event = IntegrationEvent(
            id=f"event_{uuid.uuid4().hex[:12]}",
            event_type="proposal_implemented",
            title=f"Implemented: {proposal.title}",
            description=implementation_notes,
            involved_agents=[proposal.originating_agent_id],
            involved_councils=[proposal.assigned_council_id],
            proposal_id=proposal_id,
            cultural_memory_id=memory_id,
            impact_areas=["council_governance", "cultural_memory", "evolution"],
            significance="high"
        )
        
        self.session.add(event)
        self.session.commit()
    
    # ========================================================================
    # PILLAR 3: CULTURAL MEMORY AS SHARED BRAIN
    # ========================================================================
    
    def agent_access_knowledge(
        self,
        agent_id: str,
        memory_type: str,
        memory_id: str,
        access_reason: str,
        related_project_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Agent queries cultural memory before creating.
        
        This ensures nothing is created in a vacuum - all work is informed by history.
        """
        # Retrieve the memory
        memory = None
        
        if memory_type == "identity":
            memory = self.session.query(IdentityCodex).filter_by(id=memory_id).first()
        elif memory_type == "pattern":
            memory = self.session.query(StylePattern).filter_by(id=memory_id).first()
        elif memory_type in ["lesson", "milestone", "insight"]:
            memory = self.session.query(CulturalMemory).filter_by(id=memory_id).first()
        
        if not memory:
            return {"error": "Memory not found"}
        
        # Log access
        access_id = f"access_{uuid.uuid4().hex[:12]}"
        
        access_record = KnowledgeAccess(
            id=access_id,
            agent_id=agent_id,
            memory_type=memory_type,
            memory_id=memory_id,
            memory_title=getattr(memory, 'title', getattr(memory, 'principle_name', 'Unknown')),
            access_reason=access_reason,
            related_project_id=related_project_id
        )
        
        self.session.add(access_record)
        
        # Update reference count
        if hasattr(memory, 'times_referenced'):
            memory.times_referenced += 1
            memory.last_referenced = datetime.utcnow()
        
        self.session.commit()
        
        # Return memory content
        if memory_type == "identity":
            return {
                "principle": memory.principle_name,
                "description": memory.description,
                "category": memory.category,
                "non_negotiables": memory.non_negotiables
            }
        elif memory_type == "pattern":
            return {
                "pattern_name": memory.pattern_name,
                "application": memory.application,
                "visual_rules": memory.visual_rules,
                "tone_rules": memory.tone_rules
            }
        else:
            return {
                "title": memory.title,
                "content": memory.content,
                "tags": memory.tags,
                "context": memory.context
            }
    
    def log_knowledge_application(
        self,
        access_id: str,
        how_used: str,
        contributed_to_success: bool
    ):
        """Record how agent applied cultural knowledge"""
        access = self.session.query(KnowledgeAccess).filter_by(id=access_id).first()
        
        if access:
            access.how_used = how_used
            access.contributed_to_outcome = contributed_to_success
            self.session.commit()
    
    # ========================================================================
    # PILLAR 4: EVOLUTION FEEDBACK LOOPS
    # ========================================================================
    
    def log_evolution_to_memory(
        self,
        evolution_proposal_id: str,
        evolution_type: str,
        outcome: str,
        lessons_learned: List[str]
    ) -> str:
        """
        Evolution changes are logged to cultural memory.
        
        This completes the feedback loop - the system learns from its own growth.
        """
        memory_id = f"memory_evo_{uuid.uuid4().hex[:12]}"
        
        memory = CulturalMemory(
            id=memory_id,
            memory_type="insight",
            title=f"Evolution: {evolution_type}",
            content=f"Outcome: {outcome}\n\nLessons:\n" + "\n".join(f"• {lesson}" for lesson in lessons_learned),
            tags=["evolution", evolution_type],
            context={
                "evolution_proposal_id": evolution_proposal_id,
                "timestamp": datetime.utcnow().isoformat()
            },
            times_referenced=0
        )
        
        self.session.add(memory)
        
        # Log event
        event = IntegrationEvent(
            id=f"event_{uuid.uuid4().hex[:12]}",
            event_type="evolution_logged",
            title=f"Evolution logged to memory: {evolution_type}",
            description=outcome,
            evolution_proposal_id=evolution_proposal_id,
            cultural_memory_id=memory_id,
            impact_areas=["evolution", "cultural_memory"],
            significance="high"
        )
        
        self.session.add(event)
        self.session.commit()
        
        return memory_id
    
    # ========================================================================
    # METRICS & HEALTH MONITORING
    # ========================================================================
    
    def capture_daily_metrics(self) -> str:
        """
        Capture daily civilization health metrics.
        
        This is the system's vital signs - how well are all pillars working together?
        """
        metrics_id = f"metrics_{datetime.utcnow().strftime('%Y%m%d')}"
        
        # Query current state
        active_collabs = self.session.query(AgentCollaboration).filter_by(
            status="active"
        ).count()
        
        proposals_today = self.session.query(ProposalWorkflow).filter(
            ProposalWorkflow.created_at >= datetime.utcnow() - timedelta(days=1)
        ).count()
        
        proposals_approved_today = self.session.query(ProposalWorkflow).filter(
            ProposalWorkflow.approved_at >= datetime.utcnow() - timedelta(days=1)
        ).count()
        
        memories_referenced_today = self.session.query(KnowledgeAccess).filter(
            KnowledgeAccess.accessed_at >= datetime.utcnow() - timedelta(days=1)
        ).count()
        
        # Check if metrics already exist for today
        existing = self.session.query(CivilizationMetrics).filter_by(id=metrics_id).first()
        
        if existing:
            # Update existing
            existing.collaborations_active = active_collabs
            existing.proposals_submitted = proposals_today
            existing.proposals_approved = proposals_approved_today
            existing.memories_referenced = memories_referenced_today
        else:
            # Create new
            metrics = CivilizationMetrics(
                id=metrics_id,
                active_agents=self.session.query(Agent).count(),
                collaborations_active=active_collabs,
                proposals_submitted=proposals_today,
                proposals_approved=proposals_approved_today,
                memories_referenced=memories_referenced_today,
                system_coherence_score=self._calculate_coherence_score()
            )
            
            self.session.add(metrics)
        
        self.session.commit()
        
        return metrics_id
    
    def _calculate_coherence_score(self) -> float:
        """
        Calculate how well the four pillars work together.
        
        1.0 = Perfect integration
        0.0 = Systems are disconnected
        """
        # Simple scoring based on cross-system activity
        total_collaborations = self.session.query(AgentCollaboration).count()
        total_proposals = self.session.query(ProposalWorkflow).count()
        total_knowledge_access = self.session.query(KnowledgeAccess).count()
        total_events = self.session.query(IntegrationEvent).count()
        
        # More cross-system activity = higher coherence
        activity_score = min(1.0, (total_collaborations + total_proposals + total_knowledge_access) / 100)
        
        # Proposals that reference collaborations = good integration
        proposals_from_collab = self.session.query(ProposalWorkflow).filter(
            ProposalWorkflow.source_collaboration_id.isnot(None)
        ).count()
        
        integration_score = proposals_from_collab / total_proposals if total_proposals > 0 else 0
        
        # Average the scores
        return (activity_score + integration_score) / 2


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def get_civilization_status() -> Dict[str, Any]:
    """Get complete civilization status - all four pillars"""
    with CivilizationOrchestrator() as orchestrator:
        session = orchestrator.session
        
        return {
            "agents": {
                "total": session.query(Agent).count(),
                "active_collaborations": session.query(AgentCollaboration).filter_by(
                    status="active"
                ).count()
            },
            "councils": {
                "total": session.query(Council).count(),
                "pending_proposals": session.query(ProposalWorkflow).filter_by(
                    review_status="pending"
                ).count(),
                "under_review": session.query(ProposalWorkflow).filter_by(
                    review_status="under_review"
                ).count()
            },
            "cultural_memory": {
                "total_memories": session.query(CulturalMemory).count(),
                "identity_principles": session.query(IdentityCodex).count(),
                "style_patterns": session.query(StylePattern).count(),
                "knowledge_accesses_today": session.query(KnowledgeAccess).filter(
                    KnowledgeAccess.accessed_at >= datetime.utcnow() - timedelta(days=1)
                ).count()
            },
            "evolution": {
                "active_proposals": session.query(EvolutionProposal).filter_by(
                    status="pending"
                ).count(),
                "pending_agent_proposals": session.query(AgentGenerationProposal).filter_by(
                    status="pending"
                ).count()
            },
            "integration": {
                "cross_system_events_today": session.query(IntegrationEvent).filter(
                    IntegrationEvent.timestamp >= datetime.utcnow() - timedelta(days=1)
                ).count(),
                "coherence_score": orchestrator._calculate_coherence_score()
            }
        }


if __name__ == "__main__":
    print("🔥 CIVILIZATION ORCHESTRATOR - Integration Engine")
    print("=" * 60)
    
    status = get_civilization_status()
    
    print("\n📊 CIVILIZATION STATUS:\n")
    
    print(f"👥 AGENTS (Population)")
    print(f"   Total Agents: {status['agents']['total']}")
    print(f"   Active Collaborations: {status['agents']['active_collaborations']}")
    
    print(f"\n🏛️ COUNCILS (Government)")
    print(f"   Total Councils: {status['councils']['total']}")
    print(f"   Pending Proposals: {status['councils']['pending_proposals']}")
    print(f"   Under Review: {status['councils']['under_review']}")
    
    print(f"\n🧠 CULTURAL MEMORY (Shared Brain)")
    print(f"   Total Memories: {status['cultural_memory']['total_memories']}")
    print(f"   Identity Principles: {status['cultural_memory']['identity_principles']}")
    print(f"   Style Patterns: {status['cultural_memory']['style_patterns']}")
    print(f"   Knowledge Accessed Today: {status['cultural_memory']['knowledge_accesses_today']}")
    
    print(f"\n🌱 EVOLUTION ENGINE (Growth)")
    print(f"   Active Evolution Proposals: {status['evolution']['active_proposals']}")
    print(f"   Pending New Agents: {status['evolution']['pending_agent_proposals']}")
    
    print(f"\n🔗 INTEGRATION (Coherence)")
    print(f"   Cross-System Events Today: {status['integration']['cross_system_events_today']}")
    print(f"   System Coherence Score: {status['integration']['coherence_score']:.2f}/1.00")
    
    print("\n" + "=" * 60)
    print("👑 The four pillars are now one living civilization.")
