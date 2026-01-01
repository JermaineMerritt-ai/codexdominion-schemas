"""
Cultural Memory Architecture - Database Models
The soul of the Dominion: history, identity, and wisdom.
"""

from sqlalchemy import Column, String, Text, DateTime, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base


class CreativeProject(Base):
    """LAYER 1: The Creative Lineage Archive - Past project records"""
    __tablename__ = 'creative_projects'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    project_type = Column(String)  # video, ebook, bundle, social_post, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    target_audience = Column(String)  # kids, homeschoolers, families, etc.
    
    # Creative metadata - what made this project unique
    styles_used = Column(JSON)  # ["watercolor", "bold typography", "warm colors"]
    narrative_structure = Column(String)  # "hero's journey", "problem-solution"
    emotional_tone = Column(String)  # "joyful", "reflective", "adventurous"
    brand_elements = Column(JSON)  # colors, fonts, patterns used
    
    # Outcome tracking
    success_metrics = Column(JSON)  # views, engagement, sales, etc.
    audience_response = Column(Text)  # qualitative feedback
    lessons_learned = Column(Text)
    would_repeat = Column(String)  # "yes", "no", "with_modifications"
    
    # Relationships
    decisions = relationship("CreativeDecision", back_populates="project")


class CreativeDecision(Base):
    """LAYER 1: Decision log - Every creative choice and why"""
    __tablename__ = 'creative_decisions'
    
    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey('creative_projects.id'))
    
    # Decision details
    decision_type = Column(String)  # style, narrative, brand, technical, etc.
    decision = Column(Text, nullable=False)
    rationale = Column(Text)  # why this choice was made
    alternatives_considered = Column(JSON)  # what else was considered
    
    # Who was involved
    agents_involved = Column(JSON)  # list of agent IDs
    council_id = Column(String, ForeignKey('councils.id'), nullable=True)
    debate_summary = Column(Text, nullable=True)
    
    # Outcome
    outcome = Column(String)  # success, failure, mixed, unknown
    impact_score = Column(Float)  # 0-1 how much this mattered
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("CreativeProject", back_populates="decisions")


class IdentityCodex(Base):
    """LAYER 2: The Identity Codex - Cultural DNA of the Dominion"""
    __tablename__ = 'identity_codex'
    
    id = Column(String, primary_key=True)
    category = Column(String, nullable=False)  # tone, values, aesthetic, narrative, ethics
    principle = Column(String, nullable=False)  # the core rule/value
    description = Column(Text)  # detailed explanation
    
    # Examples and guidance
    examples = Column(JSON)  # concrete examples of this principle
    anti_examples = Column(JSON)  # what violates this principle
    
    # Context
    priority = Column(Integer, default=5)  # 1-10 importance
    applies_to = Column(JSON)  # which audiences/project types
    created_by = Column(String)  # which agent or architect defined this
    
    # Lifecycle
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(String, default="active")  # active, deprecated, evolving


class StylePattern(Base):
    """LAYER 1: Successful creative patterns - What works"""
    __tablename__ = 'style_patterns'
    
    id = Column(String, primary_key=True)
    pattern_name = Column(String, nullable=False)
    pattern_type = Column(String)  # visual, narrative, audio, structural
    
    # Pattern definition
    description = Column(Text)
    elements = Column(JSON)  # specific components of this pattern
    when_to_use = Column(Text)  # contexts where this pattern shines
    audience_fit = Column(JSON)  # which audiences respond to this
    
    # Performance
    times_used = Column(Integer, default=0)
    success_rate = Column(Float)  # 0-1 how often this pattern works
    avg_engagement = Column(Float, nullable=True)
    
    # Examples
    example_projects = Column(JSON)  # project IDs where this was used
    created_at = Column(DateTime, default=datetime.utcnow)


class CulturalMemory(Base):
    """LAYER 3: Memory-to-Action Engine - Queryable wisdom"""
    __tablename__ = 'cultural_memory'
    
    id = Column(String, primary_key=True)
    memory_type = Column(String)  # lesson, pattern, milestone, rule, insight
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    
    # Context and retrieval
    tags = Column(JSON)  # searchable tags
    context = Column(JSON)  # when/where/why this memory matters
    related_memories = Column(JSON)  # IDs of related memories
    
    # Usage tracking
    times_referenced = Column(Integer, default=0)
    last_referenced = Column(DateTime, nullable=True)
    relevance_score = Column(Float, default=1.0)  # decays over time if unused
    
    # Origin
    source_project_id = Column(String, nullable=True)
    source_agent_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class BrandEvolution(Base):
    """LAYER 2: Brand evolution tracking - How identity changes over time"""
    __tablename__ = 'brand_evolution'
    
    id = Column(String, primary_key=True)
    evolution_type = Column(String)  # refinement, expansion, pivot, consolidation
    what_changed = Column(Text)
    why_changed = Column(Text)
    
    # Before and after
    previous_state = Column(JSON)
    new_state = Column(JSON)
    
    # Impact
    affected_principles = Column(JSON)  # identity_codex IDs
    affected_patterns = Column(JSON)  # style_pattern IDs
    transition_period = Column(String)  # how long to phase in
    
    # Approval
    approved_by_council = Column(String, nullable=True)
    architect_approval = Column(String, default="pending")  # pending, approved, rejected
    
    created_at = Column(DateTime, default=datetime.utcnow)


# Future expansion: SeasonalTheme, AudienceProfile, CreativeLineage, etc.
