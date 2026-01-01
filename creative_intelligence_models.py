"""
CREATIVE INTELLIGENCE ENGINE - DATABASE MODELS
SQLAlchemy ORM models for persistent storage

PURPOSE:
Replace in-memory storage with PostgreSQL/SQLite persistence.
Enable multi-user support, version control, and production scalability.

MODELS:
1. CreativeProject - Master project record
2. CreativeAsset - Individual assets (video, audio, graphics)
3. CreativeWorkflow - Workflow execution tracking
4. ProductionTimeline - Timeline assembly records
5. ContinuityReport - Validation results
6. Deliverable - Final export records
7. User - Multi-user support

Author: CodexDominion Creative Intelligence Division
Date: December 23, 2025
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON, ForeignKey, Enum as SQLEnum, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime, timezone
from enum import Enum
import json

Base = declarative_base()


# ============================================================================
# ENUMS
# ============================================================================

class ProjectType(str, Enum):
    """Project type classifications"""
    MARKETING_CAMPAIGN = "marketing_campaign"
    DOCUMENTARY = "documentary"
    EDUCATIONAL = "educational"
    ENTERTAINMENT = "entertainment"
    SOCIAL_MEDIA = "social_media"
    PODCAST = "podcast"
    MUSIC_VIDEO = "music_video"
    CORPORATE = "corporate"
    OTHER = "other"


class ProjectStatus(str, Enum):
    """Project lifecycle status"""
    DRAFT = "draft"
    INTERPRETED = "interpreted"
    IN_PRODUCTION = "in_production"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    RENDERING = "rendering"
    COMPLETE = "complete"
    ARCHIVED = "archived"
    FAILED = "failed"


class AssetType(str, Enum):
    """Asset type classifications"""
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"
    GRAPHICS = "graphics"
    TEXT = "text"
    VOICEOVER = "voiceover"
    MUSIC = "music"
    SFX = "sfx"
    OVERLAY = "overlay"


class AssetStatus(str, Enum):
    """Asset production status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    READY = "ready"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class WorkflowStatus(str, Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETE = "complete"
    FAILED = "failed"
    CANCELLED = "cancelled"


class DeliverableStatus(str, Enum):
    """Deliverable export status"""
    PENDING = "pending"
    RENDERING = "rendering"
    READY = "ready"
    DELIVERED = "delivered"
    FAILED = "failed"


# ============================================================================
# ASSOCIATION TABLES (Many-to-Many)
# ============================================================================

project_assets = Table(
    'project_assets',
    Base.metadata,
    Column('project_id', String(50), ForeignKey('creative_projects.id', ondelete='CASCADE')),
    Column('asset_id', String(50), ForeignKey('creative_assets.id', ondelete='CASCADE'))
)

project_users = Table(
    'project_users',
    Base.metadata,
    Column('project_id', String(50), ForeignKey('creative_projects.id', ondelete='CASCADE')),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'))
)


# ============================================================================
# CORE MODELS
# ============================================================================

class User(Base):
    """User accounts for multi-user support"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100))
    role = Column(String(20), default='creator')  # creator, reviewer, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    created_projects = relationship('CreativeProject', back_populates='creator', foreign_keys='CreativeProject.creator_id')
    workflows = relationship('CreativeWorkflow', back_populates='user')
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class CreativeProject(Base):
    """Master project record - replaces PIC in-memory storage"""
    __tablename__ = 'creative_projects'
    
    # Primary identification
    id = Column(String(50), primary_key=True)  # pic_project_xxxxx
    project_type = Column(SQLEnum(ProjectType), nullable=False)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.DRAFT)
    
    # Project details
    title = Column(String(200))
    description = Column(Text)
    complexity = Column(String(20))  # simple, moderate, complex, epic
    
    # Requirements
    required_mediums = Column(JSON)  # ["video", "audio", "graphics"]
    asset_requirements = Column(JSON)  # List of required assets
    timeline_hints = Column(JSON)  # Duration, pacing hints
    goals = Column(JSON)  # Project objectives
    constraints = Column(JSON)  # Budget, technical constraints
    
    # Metadata
    project_metadata = Column(JSON)  # Additional project-specific data (renamed from 'metadata')
    creative_vision = Column(JSON)  # CRE output stored here
    
    # Ownership
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship('User', back_populates='created_projects', foreign_keys=[creator_id])
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    assets = relationship('CreativeAsset', secondary=project_assets, back_populates='projects')
    workflows = relationship('CreativeWorkflow', back_populates='project', cascade='all, delete-orphan')
    timelines = relationship('ProductionTimeline', back_populates='project', cascade='all, delete-orphan')
    continuity_reports = relationship('ContinuityReport', back_populates='project', cascade='all, delete-orphan')
    deliverables = relationship('Deliverable', back_populates='project', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<CreativeProject(id='{self.id}', type={self.project_type.value}, status={self.status.value})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'project_type': self.project_type.value,
            'status': self.status.value,
            'title': self.title,
            'description': self.description,
            'complexity': self.complexity,
            'required_mediums': self.required_mediums,
            'asset_requirements': self.asset_requirements,
            'timeline_hints': self.timeline_hints,
            'goals': self.goals,
            'constraints': self.constraints,
            'project_metadata': self.project_metadata,
            'creative_vision': self.creative_vision,
            'creator_id': self.creator_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


class CreativeAsset(Base):
    """Individual assets - replaces ADG in-memory storage"""
    __tablename__ = 'creative_assets'
    
    # Primary identification
    id = Column(String(50), primary_key=True)  # asset_xxxxx
    project_id = Column(String(50), ForeignKey('creative_projects.id', ondelete='CASCADE'))
    
    # Asset details
    asset_name = Column(String(200), nullable=False)
    asset_type = Column(SQLEnum(AssetType), nullable=False)
    status = Column(SQLEnum(AssetStatus), default=AssetStatus.PENDING)
    
    # File information
    file_path = Column(String(500))
    file_format = Column(String(20))
    file_size_mb = Column(Float)
    duration_seconds = Column(Float)  # For video/audio
    resolution = Column(String(20))   # For video/images
    
    # Metadata
    asset_metadata = Column(JSON)  # Additional asset-specific data (renamed from 'metadata')
    dependencies = Column(JSON)  # List of asset IDs this depends on
    tags = Column(JSON)  # ["intro", "music", "background"]
    
    # Production tracking
    owner_module = Column(String(20))  # Which module created it (PIC, CRE, MMOE, etc.)
    version = Column(Integer, default=1)
    parent_asset_id = Column(String(50), ForeignKey('creative_assets.id'))  # For versioning
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    approved_at = Column(DateTime(timezone=True))
    
    # Relationships
    projects = relationship('CreativeProject', secondary=project_assets, back_populates='assets')
    versions = relationship('CreativeAsset', remote_side=[id])  # Self-referential for versions
    
    def __repr__(self):
        return f"<CreativeAsset(id='{self.id}', name='{self.asset_name}', type={self.asset_type.value})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'asset_name': self.asset_name,
            'asset_type': self.asset_type.value,
            'status': self.status.value,
            'file_path': self.file_path,
            'file_format': self.file_format,
            'file_size_mb': self.file_size_mb,
            'duration_seconds': self.duration_seconds,
            'resolution': self.resolution,
            'asset_metadata': self.asset_metadata,
            'dependencies': self.dependencies,
            'tags': self.tags,
            'owner_module': self.owner_module,
            'version': self.version,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class CreativeWorkflow(Base):
    """Workflow execution tracking - replaces workflow orchestrator state"""
    __tablename__ = 'creative_workflows'
    
    # Primary identification
    id = Column(Integer, primary_key=True)
    project_id = Column(String(50), ForeignKey('creative_projects.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Workflow tracking
    status = Column(SQLEnum(WorkflowStatus), default=WorkflowStatus.PENDING)
    current_step = Column(String(20))  # PIC, CRE, MMOE, ADG, CCS, OAE, Dashboard
    completed_steps = Column(JSON)  # ["PIC", "CRE", "MMOE"]
    
    # Execution log
    execution_log = Column(JSON)  # List of timestamped log entries
    error_log = Column(JSON)  # Error messages if failed
    
    # Results storage
    pic_output = Column(JSON)  # Step 1 results
    cre_output = Column(JSON)  # Step 2 results
    mmoe_output = Column(JSON)  # Step 3 results
    adg_output = Column(JSON)  # Step 4 results
    ccs_output = Column(JSON)  # Step 5 results
    oae_output = Column(JSON)  # Step 6 results
    dashboard_output = Column(JSON)  # Step 7 results
    
    # Performance metrics
    total_duration_seconds = Column(Float)
    steps_duration = Column(JSON)  # Duration for each step
    
    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    failed_at = Column(DateTime(timezone=True))
    
    # Relationships
    project = relationship('CreativeProject', back_populates='workflows')
    user = relationship('User', back_populates='workflows')
    
    def __repr__(self):
        return f"<CreativeWorkflow(id={self.id}, project_id='{self.project_id}', status={self.status.value})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'status': self.status.value,
            'current_step': self.current_step,
            'completed_steps': self.completed_steps,
            'execution_log': self.execution_log,
            'error_log': self.error_log,
            'total_duration_seconds': self.total_duration_seconds,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


class ProductionTimeline(Base):
    """Timeline assembly records - replaces TAE in-memory storage"""
    __tablename__ = 'production_timelines'
    
    # Primary identification
    id = Column(Integer, primary_key=True)
    project_id = Column(String(50), ForeignKey('creative_projects.id', ondelete='CASCADE'), nullable=False)
    timeline_id = Column(String(100), unique=True)  # project_id_timeline
    
    # Timeline data
    duration_seconds = Column(Float, nullable=False)
    total_clips = Column(Integer)
    tracks = Column(JSON)  # Track structure with clips
    
    # Orchestration plan (from MMOE)
    orchestration_plan = Column(JSON)
    waves = Column(JSON)  # Parallel/sequential execution waves
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship('CreativeProject', back_populates='timelines')
    
    def __repr__(self):
        return f"<ProductionTimeline(id={self.id}, project_id='{self.project_id}', duration={self.duration_seconds}s)>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'timeline_id': self.timeline_id,
            'duration_seconds': self.duration_seconds,
            'total_clips': self.total_clips,
            'tracks': self.tracks,
            'orchestration_plan': self.orchestration_plan,
            'waves': self.waves,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ContinuityReport(Base):
    """Continuity validation reports - replaces CCS in-memory storage"""
    __tablename__ = 'continuity_reports'
    
    # Primary identification
    id = Column(Integer, primary_key=True)
    project_id = Column(String(50), ForeignKey('creative_projects.id', ondelete='CASCADE'), nullable=False)
    report_id = Column(String(100), unique=True)
    
    # Validation results
    overall_score = Column(Float)
    critical_violations = Column(Integer, default=0)
    ready_for_assembly = Column(Boolean, default=False)
    
    # Module scores
    module_scores = Column(JSON)  # Scores for each validation module
    violations = Column(JSON)  # List of violation details
    recommendations = Column(JSON)  # Suggested fixes
    
    # Cross-medium analysis
    cross_medium_links = Column(JSON)
    style_consistency_score = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship('CreativeProject', back_populates='continuity_reports')
    
    def __repr__(self):
        return f"<ContinuityReport(id={self.id}, project_id='{self.project_id}', score={self.overall_score})>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'report_id': self.report_id,
            'overall_score': self.overall_score,
            'critical_violations': self.critical_violations,
            'ready_for_assembly': self.ready_for_assembly,
            'module_scores': self.module_scores,
            'violations': self.violations,
            'recommendations': self.recommendations,
            'cross_medium_links': self.cross_medium_links,
            'style_consistency_score': self.style_consistency_score,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Deliverable(Base):
    """Final deliverable records - replaces OAE export tracking"""
    __tablename__ = 'deliverables'
    
    # Primary identification
    id = Column(Integer, primary_key=True)
    project_id = Column(String(50), ForeignKey('creative_projects.id', ondelete='CASCADE'), nullable=False)
    deliverable_id = Column(String(100), unique=True)
    
    # Deliverable details
    platform = Column(String(20))  # youtube, tiktok, instagram, etc.
    deliverable_type = Column(String(30))  # video, audio, graphics_pack, social_post
    status = Column(SQLEnum(DeliverableStatus), default=DeliverableStatus.PENDING)
    
    # File information
    file_path = Column(String(500))
    file_format = Column(String(20))
    file_size_mb = Column(Float)
    resolution = Column(String(20))
    duration_seconds = Column(Float)
    
    # Quality settings
    codec = Column(String(50))
    bitrate = Column(String(20))
    quality_preset = Column(String(20))
    
    # Metadata
    deliverable_metadata = Column(JSON)  # Additional deliverable-specific data (renamed from 'metadata')
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    rendered_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    
    # Relationships
    project = relationship('CreativeProject', back_populates='deliverables')
    
    def __repr__(self):
        return f"<Deliverable(id={self.id}, project_id='{self.project_id}', platform='{self.platform}')>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'deliverable_id': self.deliverable_id,
            'platform': self.platform,
            'deliverable_type': self.deliverable_type,
            'status': self.status.value,
            'file_path': self.file_path,
            'file_format': self.file_format,
            'file_size_mb': self.file_size_mb,
            'resolution': self.resolution,
            'duration_seconds': self.duration_seconds,
            'codec': self.codec,
            'bitrate': self.bitrate,
            'quality_preset': self.quality_preset,
            'deliverable_metadata': self.deliverable_metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'rendered_at': self.rendered_at.isoformat() if self.rendered_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None
        }


# ============================================================================
# DATABASE UTILITIES
# ============================================================================

def init_database(engine):
    """Initialize database schema"""
    Base.metadata.create_all(engine)
    print("✅ Database schema created successfully")


def drop_database(engine):
    """Drop all tables (use with caution!)"""
    Base.metadata.drop_all(engine)
    print("⚠️  Database schema dropped")


def create_demo_user(session):
    """Create demo user for testing"""
    user = User(
        username='creator1',
        email='creator1@codexdominion.ai',
        full_name='Codex Creator',
        role='creator'
    )
    session.add(user)
    session.commit()
    print(f"✅ Demo user created: {user.username}")
    return user


# ============================================================================
# DEMO - TEST DATABASE MODELS
# ============================================================================

if __name__ == "__main__":
    import sys
    import io
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    # Windows UTF-8 encoding fix
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("🔥 CREATIVE INTELLIGENCE ENGINE - DATABASE MODELS DEMO 🔥\n")
    print("=" * 80)
    print("DATABASE SCHEMA")
    print("=" * 80)
    
    # Create in-memory SQLite database for demo
    engine = create_engine('sqlite:///:memory:', echo=False)
    
    # Initialize schema
    init_database(engine)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create demo user
    user = create_demo_user(session)
    
    print("\n" + "=" * 80)
    print("TEST 1: Create Creative Project")
    print("=" * 80)
    
    # Create project
    project = CreativeProject(
        id='pic_project_demo001',
        project_type=ProjectType.MARKETING_CAMPAIGN,
        status=ProjectStatus.INTERPRETED,
        title='Demo Marketing Campaign',
        description='A comprehensive marketing campaign for product launch',
        complexity='moderate',
        required_mediums=['video', 'audio', 'graphics'],
        asset_requirements=['intro_video', 'background_music', 'logo'],
        timeline_hints={'duration': 60, 'pacing': 'fast'},
        goals=['Increase brand awareness', 'Drive conversions'],
        constraints={'budget': 5000, 'deadline': '2025-12-31'},
        metadata={'client': 'Acme Corp'},
        creator_id=user.id
    )
    
    session.add(project)
    session.commit()
    
    print(f"✅ Project created: {project.id}")
    print(f"   Type: {project.project_type.value}")
    print(f"   Status: {project.status.value}")
    print(f"   Complexity: {project.complexity}\n")
    
    print("=" * 80)
    print("TEST 2: Create Creative Assets")
    print("=" * 80)
    
    # Create assets
    assets = [
        CreativeAsset(
            id='asset_video_001',
            project_id=project.id,
            asset_name='Intro Video',
            asset_type=AssetType.VIDEO,
            status=AssetStatus.READY,
            file_path='/assets/intro.mp4',
            file_format='mp4',
            file_size_mb=25.5,
            duration_seconds=10.0,
            resolution='1920x1080',
            owner_module='MMOE',
            tags=['intro', 'hero']
        ),
        CreativeAsset(
            id='asset_audio_001',
            asset_name='Background Music',
            asset_type=AssetType.MUSIC,
            status=AssetStatus.READY,
            file_path='/assets/music.mp3',
            file_format='mp3',
            file_size_mb=5.2,
            duration_seconds=60.0,
            owner_module='AMME',
            tags=['background', 'music']
        ),
        CreativeAsset(
            id='asset_graphics_001',
            asset_name='Logo Overlay',
            asset_type=AssetType.GRAPHICS,
            status=AssetStatus.READY,
            file_path='/assets/logo.png',
            file_format='png',
            file_size_mb=0.5,
            resolution='512x512',
            owner_module='VCE',
            tags=['logo', 'overlay']
        )
    ]
    
    for asset in assets:
        session.add(asset)
        project.assets.append(asset)
    
    session.commit()
    
    print(f"✅ Created {len(assets)} assets")
    for asset in assets:
        print(f"   - {asset.asset_name} ({asset.asset_type.value})")
    
    print("\n" + "=" * 80)
    print("TEST 3: Create Workflow Execution")
    print("=" * 80)
    
    workflow = CreativeWorkflow(
        project_id=project.id,
        user_id=user.id,
        status=WorkflowStatus.COMPLETE,
        current_step='Dashboard',
        completed_steps=['PIC', 'CRE', 'MMOE', 'ADG', 'CCS', 'OAE', 'Dashboard'],
        execution_log=[
            '[2025-12-23T08:00:00] Step 1: PIC - Project interpreted',
            '[2025-12-23T08:00:01] Step 2: CRE - Creative direction established',
            '[2025-12-23T08:00:02] Step 3: MMOE - Orchestration complete',
            '[2025-12-23T08:00:03] Step 4: ADG - Assets tracked',
            '[2025-12-23T08:00:04] Step 5: CCS - Continuity validated',
            '[2025-12-23T08:00:05] Step 6: OAE - Deliverables assembled',
            '[2025-12-23T08:00:06] Step 7: Dashboard - Generated'
        ],
        total_duration_seconds=6.5
    )
    
    session.add(workflow)
    session.commit()
    
    print(f"✅ Workflow created: ID {workflow.id}")
    print(f"   Status: {workflow.status.value}")
    print(f"   Completed steps: {len(workflow.completed_steps)}")
    print(f"   Duration: {workflow.total_duration_seconds}s\n")
    
    print("=" * 80)
    print("TEST 4: Create Continuity Report")
    print("=" * 80)
    
    report = ContinuityReport(
        project_id=project.id,
        report_id=f'{project.id}_continuity',
        overall_score=0.95,
        critical_violations=0,
        ready_for_assembly=True,
        module_scores={
            'style_consistency': 0.98,
            'audio_quality': 0.92,
            'visual_quality': 0.96,
            'narrative_flow': 0.94
        },
        violations=[],
        recommendations=['Consider adding transition effects'],
        style_consistency_score=0.98
    )
    
    session.add(report)
    session.commit()
    
    print(f"✅ Continuity report created")
    print(f"   Overall score: {report.overall_score}/1.0")
    print(f"   Ready for assembly: {report.ready_for_assembly}")
    print(f"   Critical violations: {report.critical_violations}\n")
    
    print("=" * 80)
    print("TEST 5: Create Deliverables")
    print("=" * 80)
    
    deliverables = [
        Deliverable(
            project_id=project.id,
            deliverable_id=f'{project.id}_youtube_video',
            platform='youtube',
            deliverable_type='video',
            status=DeliverableStatus.READY,
            file_path='/exports/youtube/final.mp4',
            file_format='mp4',
            file_size_mb=150.0,
            resolution='1920x1080',
            duration_seconds=60.0,
            codec='libx264',
            bitrate='5000k',
            quality_preset='high'
        ),
        Deliverable(
            project_id=project.id,
            deliverable_id=f'{project.id}_instagram_post',
            platform='instagram',
            deliverable_type='social_post',
            status=DeliverableStatus.READY,
            file_path='/exports/instagram/post.png',
            file_format='png',
            file_size_mb=2.5,
            resolution='1080x1080',
            quality_preset='high'
        )
    ]
    
    for deliverable in deliverables:
        session.add(deliverable)
    
    session.commit()
    
    print(f"✅ Created {len(deliverables)} deliverables")
    for d in deliverables:
        print(f"   - {d.platform} ({d.deliverable_type}): {d.status.value}")
    
    print("\n" + "=" * 80)
    print("TEST 6: Query Database")
    print("=" * 80)
    
    # Query project with relationships
    db_project = session.query(CreativeProject).filter_by(id='pic_project_demo001').first()
    
    print(f"✅ Project: {db_project.title}")
    print(f"   Assets: {len(db_project.assets)}")
    print(f"   Workflows: {len(db_project.workflows)}")
    print(f"   Deliverables: {len(db_project.deliverables)}")
    print(f"   Continuity Reports: {len(db_project.continuity_reports)}\n")
    
    print("=" * 80)
    print("📊 DATABASE SUMMARY")
    print("=" * 80)
    print(f"✅ Users: {session.query(User).count()}")
    print(f"✅ Projects: {session.query(CreativeProject).count()}")
    print(f"✅ Assets: {session.query(CreativeAsset).count()}")
    print(f"✅ Workflows: {session.query(CreativeWorkflow).count()}")
    print(f"✅ Timelines: {session.query(ProductionTimeline).count()}")
    print(f"✅ Continuity Reports: {session.query(ContinuityReport).count()}")
    print(f"✅ Deliverables: {session.query(Deliverable).count()}")
    
    print("\n" + "=" * 80)
    print("🔥 Database Models Complete! 👑")
    print("=" * 80)
    print("✅ All models operational")
    print("✅ Relationships configured")
    print("✅ Ready for production integration")
    
    session.close()
