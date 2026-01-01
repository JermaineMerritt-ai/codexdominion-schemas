"""
Evolution Engine - Query and Execution System
The self-improvement loop in action
"""

from typing import List, Dict, Any, Optional
from sqlalchemy import desc
from db import SessionLocal
from models import (
    EvolutionProposal, AgentGenerationProposal, TechniqueEvolution,
    EvolutionBoundary, EvolutionCycle, Agent, Council
)
from datetime import datetime


class EvolutionEngine:
    """Manages the Dominion's self-improvement capabilities"""
    
    def __init__(self):
        self.session = SessionLocal()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
    
    # ========== LAYER 4: BOUNDARY CHECKING ==========
    
    def check_boundary(self, category: str, change_type: str) -> Dict[str, Any]:
        """Check if a proposed change is within evolution boundaries"""
        boundary = self.session.query(EvolutionBoundary).filter(
            EvolutionBoundary.category == category,
            EvolutionBoundary.is_active == "active"
        ).first()
        
        if not boundary:
            return {
                "allowed": True,
                "boundary_type": "undefined",
                "approval_required": "operations_council",
                "message": "No specific boundary defined. Default approval needed."
            }
        
        flexibility_map = {
            "none": {"allowed": False, "approval": "sovereign_architect"},
            "limited": {"allowed": True, "approval": "high_council"},
            "moderate": {"allowed": True, "approval": "high_council"},
            "high": {"allowed": True, "approval": "operations_council"}
        }
        
        flexibility = flexibility_map.get(boundary.flexibility_level, flexibility_map["moderate"])
        
        return {
            "allowed": flexibility["allowed"],
            "boundary_type": boundary.boundary_type,
            "principle": boundary.principle,
            "approval_required": boundary.approval_required,
            "flexibility_level": boundary.flexibility_level,
            "what_is_protected": boundary.what_is_protected,
            "rationale": boundary.rationale,
            "message": f"{boundary.principle} - Approval required from: {boundary.approval_required}"
        }
    
    def get_all_boundaries(self, boundary_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all evolution boundaries"""
        query = self.session.query(EvolutionBoundary).filter_by(is_active="active")
        
        if boundary_type:
            query = query.filter(EvolutionBoundary.boundary_type == boundary_type)
        
        boundaries = query.order_by(EvolutionBoundary.boundary_type).all()
        
        return [{
            "id": b.id,
            "type": b.boundary_type,
            "category": b.category,
            "principle": b.principle,
            "flexibility": b.flexibility_level,
            "approval_required": b.approval_required,
            "protected": b.what_is_protected
        } for b in boundaries]
    
    # ========== LAYER 1: SELF-IMPROVEMENT LOOP ==========
    
    def create_evolution_proposal(
        self,
        proposal_type: str,
        title: str,
        description: str,
        proposed_by_agent: str,
        current_state: str,
        proposed_state: str,
        expected_benefits: Dict[str, Any],
        alignment_with_identity: str,
        risks: List[str],
        estimated_effort: str
    ) -> str:
        """Step 3 of cycle: Create an evolution proposal"""
        
        proposal = EvolutionProposal(
            id=f"evolution_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            proposal_type=proposal_type,
            title=title,
            description=description,
            proposed_by_agent=proposed_by_agent,
            current_state=current_state,
            proposed_state=proposed_state,
            expected_benefits=expected_benefits,
            alignment_with_identity=alignment_with_identity,
            risks=risks,
            estimated_effort=estimated_effort,
            status="pending_council_review"
        )
        
        self.session.add(proposal)
        self.session.commit()
        
        return proposal.id
    
    def get_pending_proposals(self) -> List[Dict[str, Any]]:
        """Get all proposals awaiting council review"""
        proposals = self.session.query(EvolutionProposal).filter_by(
            status="pending_council_review"
        ).all()
        
        return [{
            "id": p.id,
            "type": p.proposal_type,
            "title": p.title,
            "description": p.description,
            "proposed_by": p.proposed_by_agent,
            "expected_benefits": p.expected_benefits,
            "risks": p.risks,
            "created": p.created_at.strftime("%Y-%m-%d")
        } for p in proposals]
    
    def approve_proposal(
        self,
        proposal_id: str,
        council_id: str,
        vote_summary: Dict[str, Any]
    ) -> bool:
        """Step 4: Council approves a proposal"""
        proposal = self.session.query(EvolutionProposal).filter_by(id=proposal_id).first()
        
        if not proposal:
            return False
        
        proposal.status = "approved"
        proposal.reviewed_by_council = council_id
        proposal.council_vote_summary = vote_summary
        proposal.approval_date = datetime.utcnow()
        
        self.session.commit()
        return True
    
    def implement_proposal(
        self,
        proposal_id: str,
        implemented_by_agent: str,
        actual_results: Dict[str, Any]
    ) -> bool:
        """Step 5: Implement an approved proposal"""
        proposal = self.session.query(EvolutionProposal).filter_by(id=proposal_id).first()
        
        if not proposal or proposal.status != "approved":
            return False
        
        proposal.status = "implemented"
        proposal.implemented_by_agent = implemented_by_agent
        proposal.implementation_date = datetime.utcnow()
        proposal.actual_results = actual_results
        
        self.session.commit()
        return True
    
    # ========== LAYER 2: AGENT GENERATION ==========
    
    def propose_new_agent(
        self,
        agent_name: str,
        agent_role: str,
        domain: str,
        capabilities: Dict[str, Any],
        gap_identified: str,
        proposed_by: str,
        justification: str,
        expected_impact: str,
        council_assignment: str,
        training_requirements: List[str]
    ) -> str:
        """Propose a new agent for creation"""
        
        proposal = AgentGenerationProposal(
            id=f"agent_proposal_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            proposed_agent_name=agent_name,
            proposed_agent_role=agent_role,
            proposed_domain=domain,
            proposed_capabilities=capabilities,
            gap_identified=gap_identified,
            proposed_by_agent=proposed_by,
            justification=justification,
            expected_impact=expected_impact,
            council_assignment=council_assignment,
            training_requirements=training_requirements,
            status="pending_high_council_review"
        )
        
        self.session.add(proposal)
        self.session.commit()
        
        return proposal.id
    
    def get_pending_agent_proposals(self) -> List[Dict[str, Any]]:
        """Get all new agent proposals awaiting review"""
        proposals = self.session.query(AgentGenerationProposal).filter_by(
            status="pending_high_council_review"
        ).all()
        
        return [{
            "id": p.id,
            "name": p.proposed_agent_name,
            "role": p.proposed_agent_role,
            "domain": p.proposed_domain,
            "gap": p.gap_identified,
            "proposed_by": p.proposed_by_agent,
            "justification": p.justification,
            "council": p.council_assignment
        } for p in proposals]
    
    def approve_new_agent(
        self,
        proposal_id: str,
        high_council_vote: Dict[str, Any],
        sovereign_acknowledgment: str = "acknowledged"
    ) -> Optional[str]:
        """Approve creation of new agent"""
        proposal = self.session.query(AgentGenerationProposal).filter_by(id=proposal_id).first()
        
        if not proposal:
            return None
        
        # Create the actual agent
        agent_id = f"agent_{proposal.proposed_agent_name.lower().replace(' ', '_')}"
        
        new_agent = Agent(
            id=agent_id,
            name=proposal.proposed_agent_name,
            display_name=proposal.proposed_agent_name,
            role=proposal.proposed_agent_role,
            domain=proposal.proposed_domain,
            capabilities=proposal.proposed_capabilities,
            status="active",
            generation=2  # Second generation agent (created by the system)
        )
        
        self.session.add(new_agent)
        
        # Update proposal
        proposal.status = "approved"
        proposal.high_council_vote = high_council_vote
        proposal.sovereign_acknowledgment = sovereign_acknowledgment
        proposal.approval_date = datetime.utcnow()
        proposal.agent_id_created = agent_id
        proposal.activation_date = datetime.utcnow()
        
        self.session.commit()
        
        return agent_id
    
    # ========== LAYER 3: TECHNIQUE EVOLUTION ==========
    
    def propose_technique_evolution(
        self,
        category: str,
        technique_name: str,
        old_approach: str,
        new_approach: str,
        reason: str,
        test_results: Dict[str, Any],
        identity_alignment: str
    ) -> str:
        """Propose a new creative technique"""
        
        evolution = TechniqueEvolution(
            id=f"technique_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            technique_category=category,
            technique_name=technique_name,
            old_approach=old_approach,
            new_approach=new_approach,
            reason_for_evolution=reason,
            test_results=test_results,
            identity_alignment_check=identity_alignment,
            status="testing"
        )
        
        self.session.add(evolution)
        self.session.commit()
        
        return evolution.id
    
    def approve_technique(
        self,
        technique_id: str,
        council_id: str,
        cultural_memory_update: str
    ) -> bool:
        """Approve a technique evolution"""
        technique = self.session.query(TechniqueEvolution).filter_by(id=technique_id).first()
        
        if not technique:
            return False
        
        technique.status = "approved"
        technique.approved_by_council = council_id
        technique.approval_date = datetime.utcnow()
        technique.implementation_date = datetime.utcnow()
        technique.cultural_memory_update = cultural_memory_update
        
        self.session.commit()
        return True
    
    # ========== EVOLUTION CYCLE TRACKING ==========
    
    def start_evolution_cycle(self, observation: str, analysis: str) -> str:
        """Begin a new self-improvement cycle"""
        # Get next cycle number
        last_cycle = self.session.query(EvolutionCycle).order_by(
            desc(EvolutionCycle.cycle_number)
        ).first()
        
        next_number = (last_cycle.cycle_number + 1) if last_cycle else 1
        
        cycle = EvolutionCycle(
            id=f"cycle_{next_number:03d}",
            cycle_number=next_number,
            observation=observation,
            analysis=analysis
        )
        
        self.session.add(cycle)
        self.session.commit()
        
        return cycle.id
    
    def get_active_cycles(self) -> List[Dict[str, Any]]:
        """Get all active evolution cycles"""
        cycles = self.session.query(EvolutionCycle).filter(
            EvolutionCycle.completed_at.is_(None)
        ).all()
        
        return [{
            "id": c.id,
            "cycle_number": c.cycle_number,
            "observation": c.observation,
            "analysis": c.analysis,
            "status": {
                "council_review": c.council_review_status,
                "implementation": c.implementation_status,
                "memory_updated": c.memory_updated
            },
            "started": c.started_at.strftime("%Y-%m-%d")
        } for c in cycles]


def demonstrate_evolution_engine():
    """Demonstrate the Evolution Engine in action"""
    
    print("\n" + "=" * 70)
    print("🔥 EVOLUTION ENGINE - DEMONSTRATION")
    print("=" * 70)
    
    with EvolutionEngine() as engine:
        
        # Check boundaries
        print("\n📋 CHECKING EVOLUTION BOUNDARIES")
        print("-" * 70)
        
        check1 = engine.check_boundary("identity", "core_change")
        print(f"\n1️⃣ Can we change core identity?")
        print(f"   Allowed: {check1['allowed']}")
        print(f"   Boundary: {check1['boundary_type']}")
        print(f"   Approval: {check1.get('approval_required', 'N/A')}")
        
        check2 = engine.check_boundary("creative", "new_technique")
        print(f"\n2️⃣ Can we introduce new creative techniques?")
        print(f"   Allowed: {check2['allowed']}")
        print(f"   Boundary: {check2['boundary_type']}")
        print(f"   Approval: {check2.get('approval_required', 'N/A')}")
        
        # View boundaries by type
        print("\n\n📋 SACRED BOUNDARIES (Cannot change)")
        print("-" * 70)
        sacred = engine.get_all_boundaries("sacred")
        for boundary in sacred:
            print(f"   • {boundary['principle']}")
            print(f"     Protected: {boundary['protected']}")
        
        print("\n📋 FLEXIBLE BOUNDARIES (Can evolve)")
        print("-" * 70)
        flexible = engine.get_all_boundaries("flexible")
        for boundary in flexible:
            print(f"   • {boundary['principle']}")
            print(f"     Approval: {boundary['approval_required']}")
        
        # View pending proposals
        print("\n\n📋 PENDING EVOLUTION PROPOSALS")
        print("-" * 70)
        proposals = engine.get_pending_proposals()
        for proposal in proposals:
            print(f"\n   {proposal['title']}")
            print(f"   Type: {proposal['type']}")
            print(f"   Proposed by: {proposal['proposed_by']}")
            print(f"   Expected benefits: {list(proposal['expected_benefits'].keys())}")
        
        # View agent proposals
        print("\n\n📋 PENDING NEW AGENT PROPOSALS")
        print("-" * 70)
        agent_proposals = engine.get_pending_agent_proposals()
        for proposal in agent_proposals:
            print(f"\n   {proposal['name']} ({proposal['role']})")
            print(f"   Domain: {proposal['domain']}")
            print(f"   Gap identified: {proposal['gap'][:60]}...")
        
        # View active cycles
        print("\n\n📋 ACTIVE EVOLUTION CYCLES")
        print("-" * 70)
        cycles = engine.get_active_cycles()
        for cycle in cycles:
            print(f"\n   Cycle #{cycle['cycle_number']}: {cycle['observation'][:50]}...")
            print(f"   Status: {cycle['status']}")
    
    print("\n" + "=" * 70)
    print("🔥 The Dominion evolves with structure and governance.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    demonstrate_evolution_engine()
