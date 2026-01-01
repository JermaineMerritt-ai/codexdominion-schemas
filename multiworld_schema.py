"""
🔥 PHASE 60 — MULTI-WORLD CREATIVE EXPANSION
Database schema for worlds, inter-world network, and multi-world relationships.

This module adds:
- World model (creative domains with their own agents, councils, economy)
- WorldType enum (Creative, Production, Innovation, Governance)
- InterWorldConnection (relationships between worlds)
- AgentMigration (agent movement between worlds)
- CrossWorldProject (collaborative projects spanning multiple worlds)
- InterWorldMessage (communication between worlds)
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Text, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from models import Base


class WorldType(enum.Enum):
    """Types of creative worlds in the Dominion multiverse."""
    CREATIVE = "creative"           # Domain specialization (Stories, Faith, Music, Design)
    PRODUCTION = "production"       # Execution at scale (Video Factory, Asset Forge)
    INNOVATION = "innovation"       # Future exploration (Techniques Lab, Style Evolution)
    GOVERNANCE = "governance"       # Structural support (Council Training, Memory Expansion)


class World(Base):
    """
    A creative world - a fully functioning environment with its own agents,
    council, memory, evolution, economy, and purpose.
    
    Think of worlds as universes, departments, ecosystems, or creative realities.
    Each world specializes in something the Dominion needs.
    """
    __tablename__ = "worlds"
    
    id = Column(String, primary_key=True)  # world_childrens_stories
    name = Column(String, nullable=False)  # "Children's Story World"
    world_type = Column(Enum(WorldType), nullable=False)
    
    # Core Purpose
    primary_domain = Column(String, nullable=False)  # "children's_stories", "short_form_video", "techniques_lab"
    specialization = Column(String)  # Specific focus within domain
    creative_purpose = Column(Text)  # Why this world exists
    
    # World Configuration
    culture = Column(JSON)  # World-specific cultural values and norms
    rules = Column(JSON)  # World-specific governance rules
    economy_config = Column(JSON)  # Value weights, reputation tiers specific to this world
    
    # Status
    status = Column(String, default="active")  # active, dormant, evolving, merging
    population = Column(Integer, default=0)  # Number of agents in this world
    maturity_level = Column(String, default="emerging")  # emerging, established, mature, legendary
    
    # Performance Metrics
    creative_output_quality = Column(Float, default=0.0)  # 0-100
    innovation_rate = Column(Float, default=0.0)  # New techniques/approaches per cycle
    efficiency_score = Column(Float, default=0.0)  # Resource utilization
    collaboration_index = Column(Float, default=0.0)  # Cross-world cooperation level
    
    # Inter-World Network
    parent_world_id = Column(String, ForeignKey("worlds.id"), nullable=True)  # Usually "dominion_prime"
    is_sovereign = Column(Boolean, default=False)  # True only for Dominion Prime
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    last_evolution = Column(DateTime, nullable=True)
    
    # Relationships
    parent_world = relationship("World", remote_side=[id], backref="child_worlds")
    agents = relationship("WorldAgent", foreign_keys="WorldAgent.world_id", back_populates="world")
    projects = relationship("CrossWorldProject", secondary="world_project_participation", back_populates="participating_worlds")
    outgoing_connections = relationship("InterWorldConnection", foreign_keys="InterWorldConnection.source_world_id", back_populates="source_world")
    incoming_connections = relationship("InterWorldConnection", foreign_keys="InterWorldConnection.target_world_id", back_populates="target_world")


class WorldAgent(Base):
    """
    An agent's presence in a specific world.
    Agents can exist in multiple worlds simultaneously or migrate between them.
    """
    __tablename__ = "world_agents"
    
    id = Column(String, primary_key=True)  # worldagent_uuid
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    world_id = Column(String, ForeignKey("worlds.id"), nullable=False)
    
    # Status in World
    role = Column(String)  # creator, coordinator, innovator, mentor, etc.
    citizenship_status = Column(String, default="resident")  # resident, citizen, visitor, migrating
    arrival_date = Column(DateTime, default=datetime.utcnow)
    
    # Performance in this World
    world_reputation = Column(Float, default=50.0)  # Reputation specific to this world
    contributions = Column(Integer, default=0)  # Number of contributions in this world
    specialization = Column(String, nullable=True)  # What agent specializes in here
    
    # Migration
    origin_world_id = Column(String, ForeignKey("worlds.id"), nullable=True)  # Where agent came from
    is_temporary = Column(Boolean, default=False)  # Temporary assignment vs permanent move
    
    # Relationships
    agent = relationship("Agent", backref="world_memberships")
    world = relationship("World", foreign_keys=[world_id], back_populates="agents")
    origin_world = relationship("World", foreign_keys=[origin_world_id])


class InterWorldConnection(Base):
    """
    A relationship between two worlds.
    Defines how worlds communicate, share resources, and collaborate.
    """
    __tablename__ = "inter_world_connections"
    
    id = Column(String, primary_key=True)  # iwc_uuid
    source_world_id = Column(String, ForeignKey("worlds.id"), nullable=False)
    target_world_id = Column(String, ForeignKey("worlds.id"), nullable=False)
    
    # Connection Type
    connection_type = Column(String, nullable=False)  # collaboration, resource_sharing, mentorship, pipeline
    relationship_strength = Column(Float, default=50.0)  # 0-100, grows with interaction
    
    # Capabilities
    allows_agent_migration = Column(Boolean, default=True)
    allows_resource_sharing = Column(Boolean, default=True)
    allows_cross_world_projects = Column(Boolean, default=True)
    allows_voting_influence = Column(Boolean, default=False)  # Can source world vote on target world decisions?
    
    # Activity
    total_exchanges = Column(Integer, default=0)  # Number of interactions
    last_interaction = Column(DateTime, nullable=True)
    
    # Metadata
    established_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="active")  # active, dormant, severed
    
    # Relationships
    source_world = relationship("World", foreign_keys=[source_world_id], back_populates="outgoing_connections")
    target_world = relationship("World", foreign_keys=[target_world_id], back_populates="incoming_connections")


class AgentMigration(Base):
    """
    Records of agents moving between worlds.
    Tracks migration history and reasons.
    """
    __tablename__ = "agent_migrations"
    
    id = Column(String, primary_key=True)  # migration_uuid
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    from_world_id = Column(String, ForeignKey("worlds.id"), nullable=False)
    to_world_id = Column(String, ForeignKey("worlds.id"), nullable=False)
    
    # Migration Details
    migration_type = Column(String, nullable=False)  # permanent, temporary, exploratory, assignment
    reason = Column(Text)  # Why the migration happened
    duration_expected_days = Column(Integer, nullable=True)  # For temporary migrations
    
    # Status
    status = Column(String, default="active")  # active, completed, returned
    initiated_date = Column(DateTime, default=datetime.utcnow)
    completion_date = Column(DateTime, nullable=True)
    
    # Outcome
    success = Column(Boolean, nullable=True)  # Did migration achieve its purpose?
    value_generated = Column(JSON, nullable=True)  # CQV, CV, EV, IV, CoV earned during migration
    
    # Relationships
    agent = relationship("Agent", backref="migration_history")
    from_world = relationship("World", foreign_keys=[from_world_id])
    to_world = relationship("World", foreign_keys=[to_world_id])


# Association table for many-to-many relationship between worlds and projects
world_project_participation = Table(
    'world_project_participation',
    Base.metadata,
    Column('world_id', String, ForeignKey('worlds.id'), primary_key=True),
    Column('project_id', String, ForeignKey('cross_world_projects.id'), primary_key=True)
)


class CrossWorldProject(Base):
    """
    A project that spans multiple worlds.
    Requires coordination across different creative domains.
    """
    __tablename__ = "cross_world_projects"
    
    id = Column(String, primary_key=True)  # cwp_uuid
    name = Column(String, nullable=False)
    project_type = Column(String, nullable=False)  # content_creation, process_improvement, world_creation
    
    # Leadership
    lead_world_id = Column(String, ForeignKey("worlds.id"), nullable=False)
    coordinating_agent_id = Column(String, ForeignKey("agents.id"), nullable=True)
    
    # Project Details
    description = Column(Text)
    objectives = Column(JSON)  # List of goals
    requirements = Column(JSON)  # What each world needs to contribute
    
    # Status
    status = Column(String, default="planning")  # planning, active, completed, archived
    progress_percentage = Column(Float, default=0.0)
    
    # Outcomes
    value_generated = Column(JSON, nullable=True)  # Total value created by project
    innovations_created = Column(JSON, nullable=True)  # New techniques, agents, processes
    
    # Timeline
    initiated_date = Column(DateTime, default=datetime.utcnow)
    target_completion_date = Column(DateTime, nullable=True)
    actual_completion_date = Column(DateTime, nullable=True)
    
    # Relationships
    lead_world = relationship("World", foreign_keys=[lead_world_id])
    coordinator = relationship("Agent", foreign_keys=[coordinating_agent_id])
    participating_worlds = relationship("World", secondary=world_project_participation, back_populates="projects")


class InterWorldMessage(Base):
    """
    Communication between worlds.
    Messages can be requests, proposals, reports, or general communication.
    """
    __tablename__ = "inter_world_messages"
    
    id = Column(String, primary_key=True)  # iwm_uuid
    from_world_id = Column(String, ForeignKey("worlds.id"), nullable=False)
    to_world_id = Column(String, ForeignKey("worlds.id"), nullable=False)
    
    # Message Details
    message_type = Column(String, nullable=False)  # request, proposal, report, notification, question
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    
    # Context
    related_project_id = Column(String, ForeignKey("cross_world_projects.id"), nullable=True)
    priority = Column(String, default="normal")  # low, normal, high, urgent
    
    # Status
    status = Column(String, default="sent")  # sent, read, responded, archived
    sent_date = Column(DateTime, default=datetime.utcnow)
    read_date = Column(DateTime, nullable=True)
    response_id = Column(String, ForeignKey("inter_world_messages.id"), nullable=True)  # If this is a response
    
    # Relationships
    from_world = relationship("World", foreign_keys=[from_world_id])
    to_world = relationship("World", foreign_keys=[to_world_id])
    related_project = relationship("CrossWorldProject", foreign_keys=[related_project_id])
    response = relationship("InterWorldMessage", remote_side=[id])


def create_multiworld_tables():
    """Create all Phase 60 tables."""
    from db import engine
    Base.metadata.create_all(bind=engine, tables=[
        World.__table__,
        WorldAgent.__table__,
        InterWorldConnection.__table__,
        AgentMigration.__table__,
        world_project_participation,
        CrossWorldProject.__table__,
        InterWorldMessage.__table__
    ])
    print("✅ Phase 60 multi-world tables created successfully!")


if __name__ == "__main__":
    create_multiworld_tables()
