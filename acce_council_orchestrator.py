"""
🔥 ACCE COUNCIL ORCHESTRATOR - The Government in Action 🔥
===========================================================
Step 2: Council Formation Protocol - OPERATIONAL LAYER

This system:
- Orchestrates council meetings
- Manages proposals from creation to implementation
- Conducts debates and voting
- Resolves conflicts
- Enforces decisions
- Maintains governance records

The living government of the creative civilization.
===========================================================
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from acce_models import (
    Agent, Council, Proposal, Vote, DebateContribution, CouncilMeeting,
    AgentStatus, CouncilType, ProposalStatus, VoteType,
    generate_proposal_id
)
from datetime import datetime, timedelta
import json
from typing import List, Dict, Optional
import uuid

DATABASE_URL = "sqlite:///codex_civilization.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# =============================================================================
# PROPOSAL MANAGEMENT
# =============================================================================

class ProposalManager:
    """Manage the lifecycle of proposals"""
    
    def __init__(self, session):
        self.session = session
    
    def create_proposal(
        self,
        title: str,
        description: str,
        council_id: str,
        creator_id: str,
        rationale: str = None,
        alternatives: List[Dict] = None,
        expected_impact: Dict = None,
        requires_sovereign: bool = False
    ) -> Proposal:
        """Create a new proposal"""
        
        proposal_id = generate_proposal_id()
        
        proposal = Proposal(
            id=proposal_id,
            title=title,
            description=description,
            council_id=council_id,
            creator_id=creator_id,
            rationale=rationale or "",
            alternatives_considered=alternatives or [],
            expected_impact=expected_impact or {},
            requires_sovereign_approval=requires_sovereign,
            status=ProposalStatus.DRAFT
        )
        
        self.session.add(proposal)
        self.session.commit()
        
        print(f"📋 Proposal created: {title}")
        print(f"   ID: {proposal_id}")
        print(f"   Council: {council_id}")
        print(f"   Creator: {self.session.query(Agent).get(creator_id).name}")
        
        return proposal
    
    def submit_proposal(self, proposal_id: str) -> bool:
        """Submit a proposal for council review"""
        
        proposal = self.session.query(Proposal).get(proposal_id)
        if not proposal:
            print(f"❌ Proposal {proposal_id} not found")
            return False
        
        if proposal.status != ProposalStatus.DRAFT:
            print(f"❌ Proposal must be in DRAFT status to submit")
            return False
        
        # Get council to determine debate period
        council = self.session.query(Council).get(proposal.council_id)
        
        proposal.status = ProposalStatus.SUBMITTED
        proposal.submitted_at = datetime.utcnow()
        proposal.debate_ends_at = datetime.utcnow() + timedelta(hours=council.debate_period_hours)
        
        self.session.commit()
        
        print(f"📢 Proposal submitted to {council.name}")
        print(f"   Debate period: {council.debate_period_hours} hours")
        print(f"   Debate ends: {proposal.debate_ends_at}")
        
        return True
    
    def open_for_debate(self, proposal_id: str) -> bool:
        """Open proposal for council debate"""
        
        proposal = self.session.query(Proposal).get(proposal_id)
        if not proposal:
            return False
        
        proposal.status = ProposalStatus.DEBATE
        self.session.commit()
        
        print(f"💬 Proposal opened for debate: {proposal.title}")
        return True
    
    def close_debate_and_vote(self, proposal_id: str, voting_hours: int = 24) -> bool:
        """Close debate and open voting"""
        
        proposal = self.session.query(Proposal).get(proposal_id)
        if not proposal:
            return False
        
        proposal.status = ProposalStatus.VOTING
        proposal.voting_ends_at = datetime.utcnow() + timedelta(hours=voting_hours)
        
        self.session.commit()
        
        print(f"🗳️  Voting opened for: {proposal.title}")
        print(f"   Voting ends: {proposal.voting_ends_at}")
        
        return True
    
    def finalize_proposal(self, proposal_id: str) -> bool:
        """Count votes and finalize decision"""
        
        proposal = self.session.query(Proposal).get(proposal_id)
        if not proposal:
            return False
        
        # Count votes
        votes = self.session.query(Vote).filter_by(proposal_id=proposal_id).all()
        
        for_count = sum(1 for v in votes if v.vote == "for")
        against_count = sum(1 for v in votes if v.vote == "against")
        abstain_count = sum(1 for v in votes if v.vote == "abstain")
        
        proposal.votes_for = for_count
        proposal.votes_against = against_count
        proposal.votes_abstain = abstain_count
        
        # Get council voting mechanism
        council = self.session.query(Council).get(proposal.council_id)
        
        # Determine outcome based on voting mechanism
        decision = self._determine_outcome(
            council.voting_mechanism,
            for_count,
            against_count,
            len(votes),
            council.quorum_required
        )
        
        if decision == "approved":
            proposal.status = ProposalStatus.APPROVED
            proposal.final_decision = "approved"
        else:
            proposal.status = ProposalStatus.REJECTED
            proposal.final_decision = "rejected"
        
        proposal.decided_at = datetime.utcnow()
        
        # Update council stats
        council.proposals_reviewed += 1
        if decision == "approved":
            council.proposals_approved += 1
        else:
            council.proposals_rejected += 1
        
        self.session.commit()
        
        print(f"\n{'✅' if decision == 'approved' else '❌'} Proposal {decision}: {proposal.title}")
        print(f"   For: {for_count}, Against: {against_count}, Abstain: {abstain_count}")
        
        return True
    
    def _determine_outcome(
        self,
        voting_type: VoteType,
        for_votes: int,
        against_votes: int,
        total_votes: int,
        quorum: int
    ) -> str:
        """Determine outcome based on voting mechanism"""
        
        if total_votes < quorum:
            return "rejected"  # No quorum
        
        if voting_type == VoteType.CONSENSUS:
            return "approved" if against_votes == 0 else "rejected"
        
        elif voting_type == VoteType.MAJORITY:
            return "approved" if for_votes > against_votes else "rejected"
        
        elif voting_type == VoteType.SUPERMAJORITY:
            threshold = (2 * total_votes) / 3
            return "approved" if for_votes >= threshold else "rejected"
        
        elif voting_type == VoteType.VETO:
            # Any against vote blocks
            return "rejected" if against_votes > 0 else "approved"
        
        return "rejected"

# =============================================================================
# DEBATE SYSTEM
# =============================================================================

class DebateOrchestrator:
    """Orchestrate council debates"""
    
    def __init__(self, session):
        self.session = session
    
    def add_contribution(
        self,
        proposal_id: str,
        agent_id: str,
        contribution_type: str,
        content: str,
        references: List[str] = None
    ) -> DebateContribution:
        """Agent adds contribution to debate"""
        
        contribution = DebateContribution(
            id=f"debate_{uuid.uuid4().hex[:12]}",
            proposal_id=proposal_id,
            agent_id=agent_id,
            contribution_type=contribution_type,
            content=content,
            references=references or []
        )
        
        self.session.add(contribution)
        self.session.commit()
        
        agent = self.session.query(Agent).get(agent_id)
        print(f"💬 {agent.name} ({contribution_type}): {content[:100]}...")
        
        return contribution
    
    def get_debate_summary(self, proposal_id: str) -> Dict:
        """Get summary of debate"""
        
        contributions = self.session.query(DebateContribution).filter_by(
            proposal_id=proposal_id
        ).all()
        
        by_type = {}
        for contrib in contributions:
            if contrib.contribution_type not in by_type:
                by_type[contrib.contribution_type] = []
            by_type[contrib.contribution_type].append(contrib)
        
        return {
            "total_contributions": len(contributions),
            "by_type": {k: len(v) for k, v in by_type.items()},
            "participants": len(set(c.agent_id for c in contributions))
        }

# =============================================================================
# VOTING SYSTEM
# =============================================================================

class VotingOrchestrator:
    """Orchestrate council voting"""
    
    def __init__(self, session):
        self.session = session
    
    def cast_vote(
        self,
        proposal_id: str,
        agent_id: str,
        vote: str,
        reasoning: str = "",
        confidence: float = 50.0
    ) -> Vote:
        """Agent casts a vote"""
        
        # Check if already voted
        existing = self.session.query(Vote).filter_by(
            proposal_id=proposal_id,
            agent_id=agent_id
        ).first()
        
        if existing:
            # Update vote
            old_vote = existing.vote
            existing.vote = vote
            existing.reasoning = reasoning
            existing.confidence = confidence
            existing.changed_from = old_vote
            
            self.session.commit()
            
            agent = self.session.query(Agent).get(agent_id)
            print(f"🔄 {agent.name} changed vote: {old_vote} → {vote}")
            
            return existing
        
        # New vote
        new_vote = Vote(
            id=f"vote_{uuid.uuid4().hex[:12]}",
            proposal_id=proposal_id,
            agent_id=agent_id,
            vote=vote,
            reasoning=reasoning,
            confidence=confidence
        )
        
        self.session.add(new_vote)
        self.session.commit()
        
        agent = self.session.query(Agent).get(agent_id)
        print(f"🗳️  {agent.name} votes: {vote} (confidence: {confidence:.0f}%)")
        
        return new_vote
    
    def get_vote_tally(self, proposal_id: str) -> Dict:
        """Get current vote tally"""
        
        votes = self.session.query(Vote).filter_by(proposal_id=proposal_id).all()
        
        tally = {
            "for": sum(1 for v in votes if v.vote == "for"),
            "against": sum(1 for v in votes if v.vote == "against"),
            "abstain": sum(1 for v in votes if v.vote == "abstain"),
            "total": len(votes)
        }
        
        return tally

# =============================================================================
# COUNCIL MEETING ORCHESTRATOR
# =============================================================================

class MeetingOrchestrator:
    """Orchestrate council meetings"""
    
    def __init__(self, session):
        self.session = session
    
    def convene_meeting(
        self,
        council_id: str,
        meeting_type: str = "regular",
        agenda: List[Dict] = None
    ) -> CouncilMeeting:
        """Convene a council meeting"""
        
        council = self.session.query(Council).get(council_id)
        if not council:
            print(f"❌ Council not found")
            return None
        
        meeting = CouncilMeeting(
            id=f"meeting_{uuid.uuid4().hex[:12]}",
            council_id=council_id,
            meeting_type=meeting_type,
            agenda=agenda or [],
            attendees=[m.id for m in council.members],
            started_at=datetime.utcnow()
        )
        
        self.session.add(meeting)
        self.session.commit()
        
        print(f"\n🏛️  {council.name} - Meeting Convened")
        print(f"   Type: {meeting_type}")
        print(f"   Attendees: {len(meeting.attendees)}")
        print(f"   Chair: {council.chair.name}")
        
        return meeting
    
    def close_meeting(
        self,
        meeting_id: str,
        transcript: str = "",
        decisions: List[Dict] = None,
        action_items: List[Dict] = None
    ) -> bool:
        """Close a meeting and record outcomes"""
        
        meeting = self.session.query(CouncilMeeting).get(meeting_id)
        if not meeting:
            return False
        
        meeting.ended_at = datetime.utcnow()
        meeting.duration_minutes = int(
            (meeting.ended_at - meeting.started_at).total_seconds() / 60
        )
        meeting.transcript = transcript
        meeting.decisions_made = decisions or []
        meeting.action_items = action_items or []
        
        self.session.commit()
        
        print(f"✅ Meeting closed - Duration: {meeting.duration_minutes} minutes")
        print(f"   Decisions: {len(meeting.decisions_made)}")
        print(f"   Action items: {len(meeting.action_items)}")
        
        return True

# =============================================================================
# COMPLETE WORKFLOW EXAMPLE
# =============================================================================

def example_proposal_workflow():
    """Example: Complete proposal from creation to decision"""
    
    session = SessionLocal()
    
    try:
        print("\n" + "=" * 80)
        print("🔥 COUNCIL GOVERNANCE WORKFLOW DEMONSTRATION 🔥")
        print("=" * 80)
        
        # Initialize orchestrators
        proposal_mgr = ProposalManager(session)
        debate_orch = DebateOrchestrator(session)
        voting_orch = VotingOrchestrator(session)
        meeting_orch = MeetingOrchestrator(session)
        
        # Get councils and agents
        creative_council = session.query(Council).filter_by(
            council_type=CouncilType.CREATIVE
        ).first()
        
        innovation_pioneer = session.query(Agent).filter_by(
            name="Innovation Pioneer"
        ).first()
        
        # Step 1: Create proposal
        print("\n📋 STEP 1: Creating Proposal")
        print("-" * 80)
        
        proposal = proposal_mgr.create_proposal(
            title="Adopt AI-Generated Background Music System",
            description="Integrate an AI system to automatically generate background music for video projects, reducing production time and costs.",
            council_id=creative_council.id,
            creator_id=innovation_pioneer.id,
            rationale="Current music licensing is expensive and time-consuming. AI-generated music can be royalty-free and on-demand.",
            alternatives=[
                {"option": "Continue with licensed music", "pros": ["Higher quality"], "cons": ["Expensive", "Time-consuming"]},
                {"option": "Use stock music libraries", "pros": ["Cheaper"], "cons": ["Generic sound", "Still requires licensing"]}
            ],
            expected_impact={
                "quality": 0.8,
                "efficiency": 0.9,
                "innovation": 0.95,
                "risk": 0.3
            }
        )
        
        # Step 2: Submit and open for debate
        print("\n💬 STEP 2: Opening Debate")
        print("-" * 80)
        
        proposal_mgr.submit_proposal(proposal.id)
        proposal_mgr.open_for_debate(proposal.id)
        
        # Step 3: Agents debate
        print("\n🗣️  STEP 3: Council Debate")
        print("-" * 80)
        
        # Get all council members
        members = creative_council.members
        
        # Narrative Sage supports
        debate_orch.add_contribution(
            proposal.id,
            members[0].id,
            "support",
            "AI-generated music could enhance storytelling by adapting to narrative pacing in real-time. I support this innovation.",
            references=["memory_lesson_602384f892a5"]
        )
        
        # Visual Sovereign questions
        debate_orch.add_contribution(
            proposal.id,
            members[1].id,
            "question",
            "How will this maintain our brand's sophisticated aesthetic? Generic AI music could cheapen our premium feel.",
            references=["memory_style_9354c71a4789"]
        )
        
        # Brand Guardian opposes
        debate_orch.add_contribution(
            proposal.id,
            members[2].id,
            "oppose",
            "This poses a risk to brand consistency. Our golden aesthetic includes curated, premium audio. AI music may not meet our standards.",
            references=["memory_style_9354c71a4789"]
        )
        
        # Innovation Pioneer responds
        debate_orch.add_contribution(
            proposal.id,
            innovation_pioneer.id,
            "support",
            "We can train the AI on our brand guidelines and use it as a starting point, with human refinement. This is evolution, not replacement.",
            references=[]
        )
        
        debate_summary = debate_orch.get_debate_summary(proposal.id)
        print(f"\nDebate Summary:")
        print(f"  Total contributions: {debate_summary['total_contributions']}")
        print(f"  Participants: {debate_summary['participants']}")
        print(f"  By type: {debate_summary['by_type']}")
        
        # Step 4: Close debate, open voting
        print("\n🗳️  STEP 4: Voting Period")
        print("-" * 80)
        
        proposal_mgr.close_debate_and_vote(proposal.id, voting_hours=24)
        
        # All council members vote
        for member in members:
            if member.name == "Narrative Sage":
                voting_orch.cast_vote(proposal.id, member.id, "for", "Enhances storytelling", 85.0)
            elif member.name == "Visual Sovereign":
                voting_orch.cast_vote(proposal.id, member.id, "for", "With proper guidelines", 70.0)
            elif member.name == "Brand Guardian":
                voting_orch.cast_vote(proposal.id, member.id, "against", "Risks brand consistency", 80.0)
            elif member.name == "Sonic Architect":
                voting_orch.cast_vote(proposal.id, member.id, "for", "Excited to experiment", 90.0)
            elif member.name == "Motion Maestro":
                voting_orch.cast_vote(proposal.id, member.id, "for", "Faster production", 75.0)
        
        tally = voting_orch.get_vote_tally(proposal.id)
        print(f"\nVote Tally:")
        print(f"  For: {tally['for']}")
        print(f"  Against: {tally['against']}")
        print(f"  Abstain: {tally['abstain']}")
        
        # Step 5: Finalize decision
        print("\n✅ STEP 5: Decision")
        print("-" * 80)
        
        proposal_mgr.finalize_proposal(proposal.id)
        
        # Step 6: Record meeting
        print("\n📝 STEP 6: Meeting Record")
        print("-" * 80)
        
        meeting = meeting_orch.convene_meeting(
            creative_council.id,
            "special",
            [{"item": proposal.title, "duration": 60, "priority": "high"}]
        )
        
        meeting_orch.close_meeting(
            meeting.id,
            transcript=f"Council debated {proposal.title}. Decision: APPROVED (4-1 vote).",
            decisions=[{
                "proposal_id": proposal.id,
                "decision": "approved",
                "votes": tally
            }],
            action_items=[
                {"task": "Create AI music training dataset", "assigned_to": "Sonic Architect", "deadline": "2026-01-15"},
                {"task": "Develop brand guidelines for AI music", "assigned_to": "Brand Guardian", "deadline": "2026-01-20"}
            ]
        )
        
        print("\n" + "=" * 80)
        print("✅ GOVERNANCE WORKFLOW COMPLETE!")
        print("=" * 80)
        print("\nThe council has successfully:")
        print("  ✓ Reviewed a proposal")
        print("  ✓ Conducted structured debate")
        print("  ✓ Held a democratic vote")
        print("  ✓ Made a binding decision")
        print("  ✓ Recorded the outcome")
        print("\n🔥 The government is alive and functioning! 👑\n")
        
    finally:
        session.close()

# =============================================================================
# CLI INTERFACE
# =============================================================================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("\n🏛️  ACCE Council Orchestrator")
        print("\nUsage:")
        print("  python acce_council_orchestrator.py demo     - Run demonstration")
        print("  python acce_council_orchestrator.py propose  - Create proposal")
        print("  python acce_council_orchestrator.py vote     - Cast votes")
        print("  python acce_council_orchestrator.py meet     - Convene meeting")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "demo":
        example_proposal_workflow()
    else:
        print(f"❌ Unknown command: {command}")
