"""
🔥 AUTONOMOUS CREATIVE CIVILIZATION ENGINE (ACCE) - DATABASE MODELS 🔥
================================================================================
Phase 40: The Dominion evolves from singular intelligence to creative society

Four Pillars:
1. Autonomous Creative Agents (ACAs) - The population
2. Creative Council System (CCS+) - The government
3. Cultural Memory Archive (CMA) - The history
4. Evolution Engine (EE) - The future

These models define the civilization's structure, governance, memory, and evolution.
================================================================================
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Text, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

# =============================================================================
# ENUMS - Define Types and States
# =============================================================================

class AgentType(enum.Enum):
    """Types of creative agents in the civilization"""
    STORY = "story"              # Narrative and story development
    DESIGN = "design"            # Visual design and graphics
    AUDIO = "audio"              # Sound, music, voice
    VIDEO = "video"              # Video production and editing
    BRANDING = "branding"        # Brand identity and consistency
    CONTINUITY = "continuity"    # Cross-project consistency
    QUALITY = "quality"          # Quality assurance and standards
    INNOVATION = "innovation"    # New techniques and experimentation

class AgentStatus(enum.Enum):
    """Agent lifecycle states"""
    GENESIS = "genesis"          # Being created
    ACTIVE = "active"            # Fully operational
    LEARNING = "learning"        # In training phase
    EVOLVED = "evolved"          # Has undergone evolution
    RETIRED = "retired"          # No longer active
    LEGENDARY = "legendary"      # Achieved exceptional status

class CouncilType(enum.Enum):
    """Types of governing councils"""
    CREATIVE = "creative"        # Creative direction decisions
    QUALITY = "quality"          # Quality standards and review
    INNOVATION = "innovation"    # New ideas and experiments
    GOVERNANCE = "governance"    # Rules and structure
    EVOLUTION = "evolution"      # System improvement
    SUPREME = "supreme"          # Highest authority (Jermaine's council)

class VoteType(enum.Enum):
    """Types of voting mechanisms"""
    CONSENSUS = "consensus"      # All must agree
    MAJORITY = "majority"        # >50% required
    SUPERMAJORITY = "supermajority"  # 2/3 required
    VETO = "veto"               # Single veto blocks
    SOVEREIGN = "sovereign"      # Jermaine's final word

class ProposalStatus(enum.Enum):
    """Status of council proposals"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    DEBATE = "debate"
    VOTING = "voting"
    APPROVED = "approved"
    REJECTED = "rejected"
    VETOED = "vetoed"
    IMPLEMENTED = "implemented"

class MemoryType(enum.Enum):
    """Types of cultural memories"""
    PROJECT = "project"          # Completed project
    STYLE = "style"              # Style/aesthetic
    LESSON = "lesson"            # Learned lesson
    SUCCESS = "success"          # Success pattern
    FAILURE = "failure"          # Failure to avoid
    INNOVATION = "innovation"    # New technique
    BRAND_RULE = "brand_rule"    # Brand guideline

class EvolutionType(enum.Enum):
    """Types of evolutionary changes"""
    WORKFLOW = "workflow"        # Workflow improvement
    AGENT_BIRTH = "agent_birth"  # New agent created
    AGENT_EVOLUTION = "agent_evolution"  # Agent upgraded
    CAPABILITY = "capability"    # New capability added
    OPTIMIZATION = "optimization"  # Performance improvement
    INNOVATION = "innovation"    # Novel technique discovered

# =============================================================================
# JUNCTION TABLES - Many-to-Many Relationships
# =============================================================================

# Agents can serve on multiple councils
council_membership = Table('council_membership', Base.metadata,
    Column('agent_id', String, ForeignKey('agents.id'), primary_key=True),
    Column('council_id', String, ForeignKey('councils.id'), primary_key=True),
    Column('role', String),  # member, chair, secretary
    Column('appointed_at', DateTime, default=datetime.utcnow),
    Column('appointed_by', String)  # who appointed them
)

# Agents can collaborate on projects
project_collaboration = Table('project_collaboration', Base.metadata,
    Column('agent_id', String, ForeignKey('agents.id'), primary_key=True),
    Column('memory_id', String, ForeignKey('cultural_memories.id'), primary_key=True),
    Column('role', String),  # lead, contributor, reviewer
    Column('contribution_score', Float, default=0.0)
)

# Agents can mentor each other
agent_mentorship = Table('agent_mentorship', Base.metadata,
    Column('mentor_id', String, ForeignKey('agents.id'), primary_key=True),
    Column('mentee_id', String, ForeignKey('agents.id'), primary_key=True),
    Column('started_at', DateTime, default=datetime.utcnow),
    Column('mentorship_type', String),  # skill, wisdom, technique
    Column('progress', Float, default=0.0)
)

# =============================================================================
# PILLAR 1: AUTONOMOUS CREATIVE AGENTS (ACAs)
# =============================================================================

class Agent(Base):
    """
    Autonomous Creative Agent - A member of the creative civilization
    
    Each agent is a specialized intelligence with:
    - Unique personality and traits
    - Specific skills and capabilities
    - Thinking and creativity
    - Learning and evolution
    - Social relationships
    """
    __tablename__ = 'agents'
    
    # Identity
    id = Column(String, primary_key=True)  # Format: agent_TYPE_XXXX
    name = Column(String, unique=True, nullable=False)
    agent_type = Column(Enum(AgentType), nullable=False)
    status = Column(Enum(AgentStatus), default=AgentStatus.GENESIS)
    
    # Personality & Traits
    personality = Column(JSON)  # {traits, values, preferences, quirks}
    """
    Example:
    {
        "traits": ["creative", "analytical", "perfectionist"],
        "values": ["quality", "innovation", "consistency"],
        "preferences": {"style": "minimalist", "pace": "deliberate"},
        "quirks": ["always suggests gold accents", "debates every detail"]
    }
    """
    
    # Skills & Capabilities
    skills = Column(JSON)  # {skill_name: level (0-100)}
    """
    Example for Design Agent:
    {
        "typography": 95,
        "color_theory": 88,
        "layout": 92,
        "branding": 85,
        "illustration": 70
    }
    """
    
    specializations = Column(JSON)  # [specialized areas]
    """
    Example: ["logo design", "print layouts", "brand guidelines"]
    """
    
    # Intelligence & Thinking
    thinking_style = Column(String)  # analytical, intuitive, innovative, systematic
    creativity_level = Column(Float, default=50.0)  # 0-100
    learning_rate = Column(Float, default=1.0)  # How fast they improve
    
    # Experience & Growth
    experience_points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    projects_completed = Column(Integer, default=0)
    successful_contributions = Column(Integer, default=0)
    innovations_created = Column(Integer, default=0)
    
    # Evolution History
    generation = Column(Integer, default=1)  # How many times evolved
    evolution_history = Column(JSON)  # [{date, changes, reason}]
    dna_template = Column(JSON)  # Genetic template for reproduction
    
    # Lifecycle
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String)  # agent_id or "system" or "jermaine"
    activated_at = Column(DateTime)
    retired_at = Column(DateTime)
    
    # Governance
    council_seats = Column(Integer, default=0)  # Number of council positions
    voting_power = Column(Float, default=1.0)  # Influence in votes
    reputation = Column(Float, default=50.0)  # 0-100 standing in civilization
    
    # Communication & Social
    communication_style = Column(String)  # formal, casual, technical, poetic
    collaboration_preference = Column(String)  # solo, pair, team, ensemble
    
    # Performance Metrics
    quality_score = Column(Float, default=50.0)  # Average quality of work
    efficiency_score = Column(Float, default=50.0)  # Speed vs quality
    innovation_score = Column(Float, default=50.0)  # Novel contributions
    
    # State & Context
    current_task = Column(String)  # What they're working on
    availability = Column(Boolean, default=True)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # AI Model Configuration
    ai_model = Column(String, default="gpt-4")
    model_parameters = Column(JSON)  # {temperature, top_p, etc}
    system_prompt = Column(Text)  # Custom instructions for this agent
    
    # Relationships
    councils = relationship('Council', secondary=council_membership, back_populates='members')
    proposals_created = relationship('Proposal', back_populates='creator', foreign_keys='Proposal.creator_id')
    votes = relationship('Vote', back_populates='agent')
    debates = relationship('DebateContribution', back_populates='agent')
    memories_contributed = relationship('CulturalMemory', secondary=project_collaboration, back_populates='contributors')
    evolutions = relationship('Evolution', back_populates='affected_agent', foreign_keys='Evolution.affected_agent_id')

# =============================================================================
# PILLAR 2: CREATIVE COUNCIL SYSTEM (CCS+)
# =============================================================================

class Council(Base):
    """
    Governing Council - A decision-making body in the civilization
    
    Councils:
    - Review and approve creative decisions
    - Debate proposals and alternatives
    - Maintain standards and quality
    - Resolve conflicts
    - Guide evolution
    """
    __tablename__ = 'councils'
    
    # Identity
    id = Column(String, primary_key=True)  # Format: council_TYPE_XXXX
    name = Column(String, unique=True, nullable=False)
    council_type = Column(Enum(CouncilType), nullable=False)
    
    # Purpose & Scope
    purpose = Column(Text)  # What this council oversees
    jurisdiction = Column(JSON)  # What decisions they can make
    """
    Example:
    {
        "domains": ["branding", "visual identity"],
        "decision_types": ["approve_brand_change", "set_style_guidelines"],
        "veto_rights": ["brand_violations"],
        "required_approval": ["major_rebrand"]
    }
    """
    
    # Governance Rules
    voting_mechanism = Column(Enum(VoteType), default=VoteType.MAJORITY)
    quorum_required = Column(Integer, default=2)  # Min members for valid vote
    debate_period_hours = Column(Integer, default=24)
    
    # Structure
    min_members = Column(Integer, default=3)
    max_members = Column(Integer, default=7)
    chair_agent_id = Column(String, ForeignKey('agents.id'))
    
    # Status
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String)
    
    # Performance
    proposals_reviewed = Column(Integer, default=0)
    proposals_approved = Column(Integer, default=0)
    proposals_rejected = Column(Integer, default=0)
    average_deliberation_hours = Column(Float, default=0.0)
    
    # Relationships
    members = relationship('Agent', secondary=council_membership, back_populates='councils')
    chair = relationship('Agent', foreign_keys=[chair_agent_id])
    proposals = relationship('Proposal', back_populates='council')
    meetings = relationship('CouncilMeeting', back_populates='council')

class Proposal(Base):
    """
    Creative Proposal - A decision or change proposed to a council
    """
    __tablename__ = 'proposals'
    
    # Identity
    id = Column(String, primary_key=True)  # Format: proposal_XXXX
    title = Column(String, nullable=False)
    status = Column(Enum(ProposalStatus), default=ProposalStatus.DRAFT)
    
    # Content
    description = Column(Text)  # What is being proposed
    rationale = Column(Text)  # Why this should be done
    alternatives_considered = Column(JSON)  # [{alt, pros, cons}]
    expected_impact = Column(JSON)  # {quality, efficiency, innovation, risk}
    
    # Governance
    council_id = Column(String, ForeignKey('councils.id'), nullable=False)
    creator_id = Column(String, ForeignKey('agents.id'), nullable=False)
    requires_sovereign_approval = Column(Boolean, default=False)
    
    # Timeline
    created_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime)
    debate_ends_at = Column(DateTime)
    voting_ends_at = Column(DateTime)
    decided_at = Column(DateTime)
    implemented_at = Column(DateTime)
    
    # Outcome
    votes_for = Column(Integer, default=0)
    votes_against = Column(Integer, default=0)
    votes_abstain = Column(Integer, default=0)
    final_decision = Column(String)  # approved, rejected, vetoed
    decision_notes = Column(Text)
    
    # Implementation
    implementation_status = Column(String)  # pending, in_progress, complete
    implementation_notes = Column(Text)
    
    # Relationships
    council = relationship('Council', back_populates='proposals')
    creator = relationship('Agent', back_populates='proposals_created', foreign_keys=[creator_id])
    votes = relationship('Vote', back_populates='proposal')
    debates = relationship('DebateContribution', back_populates='proposal')

class Vote(Base):
    """Individual vote cast by an agent on a proposal"""
    __tablename__ = 'votes'
    
    id = Column(String, primary_key=True)
    proposal_id = Column(String, ForeignKey('proposals.id'), nullable=False)
    agent_id = Column(String, ForeignKey('agents.id'), nullable=False)
    
    vote = Column(String, nullable=False)  # for, against, abstain
    reasoning = Column(Text)  # Why they voted this way
    confidence = Column(Float, default=50.0)  # How confident (0-100)
    
    cast_at = Column(DateTime, default=datetime.utcnow)
    changed_from = Column(String)  # Previous vote if changed
    
    # Relationships
    proposal = relationship('Proposal', back_populates='votes')
    agent = relationship('Agent', back_populates='votes')

class DebateContribution(Base):
    """Arguments and discussion in proposal debates"""
    __tablename__ = 'debate_contributions'
    
    id = Column(String, primary_key=True)
    proposal_id = Column(String, ForeignKey('proposals.id'), nullable=False)
    agent_id = Column(String, ForeignKey('agents.id'), nullable=False)
    
    contribution_type = Column(String)  # support, oppose, question, alternative
    content = Column(Text, nullable=False)
    references = Column(JSON)  # Links to memories, past projects, etc
    
    persuasiveness_score = Column(Float, default=0.0)  # Impact on other agents
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    proposal = relationship('Proposal', back_populates='debates')
    agent = relationship('Agent', back_populates='debates')

class CouncilMeeting(Base):
    """Record of council meetings and deliberations"""
    __tablename__ = 'council_meetings'
    
    id = Column(String, primary_key=True)
    council_id = Column(String, ForeignKey('councils.id'), nullable=False)
    
    meeting_type = Column(String)  # regular, emergency, special
    agenda = Column(JSON)  # [{item, duration, priority}]
    attendees = Column(JSON)  # [agent_ids]
    
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    duration_minutes = Column(Integer)
    
    transcript = Column(Text)  # Full record of discussion
    decisions_made = Column(JSON)  # [{decision, votes, outcome}]
    action_items = Column(JSON)  # [{task, assigned_to, deadline}]
    
    # Relationships
    council = relationship('Council', back_populates='meetings')

# =============================================================================
# PILLAR 3: CULTURAL MEMORY ARCHIVE (CMA)
# =============================================================================

class CulturalMemory(Base):
    """
    Cultural Memory - Stored knowledge and lessons from civilization history
    
    The archive that helps agents:
    - Learn from the past
    - Maintain consistency
    - Avoid mistakes
    - Build on successes
    - Preserve culture
    """
    __tablename__ = 'cultural_memories'
    
    # Identity
    id = Column(String, primary_key=True)  # Format: memory_TYPE_XXXX
    title = Column(String, nullable=False)
    memory_type = Column(Enum(MemoryType), nullable=False)
    
    # Content
    description = Column(Text)
    key_insights = Column(JSON)  # [insight strings]
    lessons_learned = Column(JSON)  # [{lesson, importance}]
    
    # Context
    project_id = Column(String)  # Link to original project (if applicable)
    related_memories = Column(JSON)  # [memory_ids]
    tags = Column(JSON)  # [tag strings] for categorization
    
    # Quality & Impact
    success_rating = Column(Float, default=50.0)  # 0-100
    impact_score = Column(Float, default=50.0)  # How influential
    reference_count = Column(Integer, default=0)  # Times referenced
    
    # Pattern Recognition
    patterns = Column(JSON)  # Identified patterns in this memory
    """
    Example:
    {
        "style_patterns": ["minimalist", "gold_accents", "clean_lines"],
        "success_factors": ["strong_concept", "consistent_execution"],
        "pitfalls_avoided": ["scope_creep", "inconsistent_branding"]
    }
    """
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String)  # agent_id
    last_referenced = Column(DateTime)
    archived = Column(Boolean, default=False)
    
    # Searchability
    keywords = Column(JSON)  # Extracted keywords
    summary = Column(Text)  # AI-generated summary
    
    # Relationships
    contributors = relationship('Agent', secondary=project_collaboration, back_populates='memories_contributed')

class StyleGuide(Base):
    """Living style guide maintained by the civilization"""
    __tablename__ = 'style_guides'
    
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String)  # visual, audio, narrative, brand
    
    rules = Column(JSON)  # [{rule, reasoning, examples}]
    do_examples = Column(JSON)  # Good examples
    dont_examples = Column(JSON)  # Things to avoid
    
    authority_level = Column(String)  # guideline, standard, law
    enforcement_level = Column(String)  # suggest, encourage, require, enforce
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    version = Column(Integer, default=1)
    
    active = Column(Boolean, default=True)

# =============================================================================
# PILLAR 4: EVOLUTION ENGINE (EE)
# =============================================================================

class Evolution(Base):
    """
    Evolution Record - A change that improved the civilization
    
    Tracks:
    - Workflow improvements
    - New agent births
    - Agent upgrades
    - Capability expansions
    - Optimizations
    - Innovations
    """
    __tablename__ = 'evolutions'
    
    # Identity
    id = Column(String, primary_key=True)  # Format: evolution_XXXX
    title = Column(String, nullable=False)
    evolution_type = Column(Enum(EvolutionType), nullable=False)
    
    # Description
    description = Column(Text)
    motivation = Column(Text)  # Why this evolution was needed
    approach = Column(Text)  # How it was implemented
    
    # Impact
    before_state = Column(JSON)  # State before evolution
    after_state = Column(JSON)  # State after evolution
    improvements = Column(JSON)  # {metric: {before, after, change_pct}}
    """
    Example:
    {
        "quality_score": {"before": 75, "after": 82, "change": "+9.3%"},
        "efficiency": {"before": 60, "after": 78, "change": "+30%"},
        "agent_satisfaction": {"before": 70, "after": 85, "change": "+21.4%"}
    }
    """
    
    # Affected Entities
    affected_agent_id = Column(String, ForeignKey('agents.id'))
    affected_workflow = Column(String)
    affected_capability = Column(String)
    
    # Implementation
    implemented_at = Column(DateTime, default=datetime.utcnow)
    implemented_by = Column(String)  # agent_id or "system"
    approved_by = Column(String)  # council_id or "jermaine"
    
    # Evaluation
    success = Column(Boolean, default=True)
    adoption_rate = Column(Float, default=0.0)  # How widely adopted (0-100)
    lessons_learned = Column(Text)
    
    # Future
    inspired_evolutions = Column(JSON)  # [evolution_ids] spawned from this
    reversible = Column(Boolean, default=True)
    rollback_instructions = Column(Text)
    
    # Relationships
    affected_agent = relationship('Agent', back_populates='evolutions', foreign_keys=[affected_agent_id])

class CapabilityRegistry(Base):
    """Registry of all capabilities in the civilization"""
    __tablename__ = 'capability_registry'
    
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String)  # technical, creative, governance, social
    
    description = Column(Text)
    requirements = Column(JSON)  # {dependencies, prerequisites}
    providers = Column(JSON)  # [agent_ids] who have this capability
    
    maturity_level = Column(String)  # experimental, stable, mature, legacy
    usage_count = Column(Integer, default=0)
    
    introduced_at = Column(DateTime, default=datetime.utcnow)
    introduced_by = Column(String)

class WorkflowTemplate(Base):
    """Templates for workflows, can evolve over time"""
    __tablename__ = 'workflow_templates'
    
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String)  # creative, production, governance, evolution
    
    steps = Column(JSON)  # [{step, agents_required, duration, dependencies}]
    parameters = Column(JSON)  # Configurable parameters
    
    version = Column(Integer, default=1)
    optimization_level = Column(Integer, default=1)  # How many times optimized
    
    performance_metrics = Column(JSON)  # {avg_duration, success_rate, quality}
    last_optimized = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)

# =============================================================================
# GOVERNANCE & LAW
# =============================================================================

class DominionLaw(Base):
    """Laws that govern the civilization"""
    __tablename__ = 'dominion_laws'
    
    id = Column(String, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    category = Column(String)  # creative, governance, ethics, technical
    
    content = Column(Text, nullable=False)  # The actual law
    rationale = Column(Text)  # Why this law exists
    
    authority_level = Column(String)  # guideline, principle, law, constitution
    enforcement = Column(String)  # voluntary, recommended, required, absolute
    
    enacted_at = Column(DateTime, default=datetime.utcnow)
    enacted_by = Column(String)  # Usually "jermaine" or "supreme_council"
    
    violations = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)

class AgentPermission(Base):
    """Permissions and restrictions for agents"""
    __tablename__ = 'agent_permissions'
    
    id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey('agents.id'), nullable=False)
    
    permissions = Column(JSON)  # {action: allowed/denied}
    """
    Example:
    {
        "create_proposals": true,
        "vote_on_creative": true,
        "modify_workflows": false,
        "create_agents": false,
        "access_memory": true
    }
    """
    
    restrictions = Column(JSON)  # Special limitations
    granted_at = Column(DateTime, default=datetime.utcnow)
    granted_by = Column(String)
    expires_at = Column(DateTime)  # Optional expiration

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_agent_id(agent_type: AgentType) -> str:
    """Generate unique agent ID"""
    import uuid
    short_id = str(uuid.uuid4())[:8]
    return f"agent_{agent_type.value}_{short_id}"

def generate_council_id(council_type: CouncilType) -> str:
    """Generate unique council ID"""
    import uuid
    short_id = str(uuid.uuid4())[:8]
    return f"council_{council_type.value}_{short_id}"

def generate_proposal_id() -> str:
    """Generate unique proposal ID"""
    import uuid
    return f"proposal_{uuid.uuid4().hex[:12]}"

def generate_memory_id(memory_type: MemoryType) -> str:
    """Generate unique memory ID"""
    import uuid
    return f"memory_{memory_type.value}_{uuid.uuid4().hex[:12]}"

def generate_evolution_id() -> str:
    """Generate unique evolution ID"""
    import uuid
    return f"evolution_{uuid.uuid4().hex[:12]}"

# =============================================================================
# INITIALIZATION
# =============================================================================

if __name__ == '__main__':
    print("🔥 ACCE Database Models Loaded 👑")
    print(f"  - {len([c for c in Base.__subclasses__()])} main tables")
    print(f"  - 3 junction tables for relationships")
    print(f"  - 8 agent types")
    print(f"  - 6 council types")
    print(f"  - Ready for Phase 40 civilization")
