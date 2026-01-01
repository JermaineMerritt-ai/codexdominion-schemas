"""
🔥 CODEX DOMINION - UNIFIED DATA MODELS 🔥
==========================================
Comprehensive SQLAlchemy models for the entire Codex Dominion system

Includes:
- Governance: Council, CouncilMember
- Agents: Agent, AgentReputation, AgentTraining
- Workflows: Workflow, WorkflowMetric, WorkflowVote, WorkflowType
- Authentication: User, UserRole, AuditLog
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
import enum
import json

from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text, 
    ForeignKey, Table, Enum as SQLEnum, JSON, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

# Single declarative base for all models
Base = declarative_base()


# ============================================================================
# ENUMS
# ============================================================================

class UserRole(enum.Enum):
    """User role types for authentication"""
    ADMIN = "admin"
    COUNCIL_OPERATOR = "council_operator"
    VIEWER = "viewer"
    OWNER = "owner"  # Tenant owner
    COLLABORATOR = "collaborator"  # Tenant collaborator
    TENANT_VIEWER = "tenant_viewer"  # Tenant read-only


class WorkflowStatus(enum.Enum):
    """Workflow execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PENDING_REVIEW = "pending_review"


class NotificationType(enum.Enum):
    """Portal notification types"""
    WORKFLOW_STARTED = "workflow_started"
    STEP_COMPLETED = "step_completed"
    WORKFLOW_COMPLETED = "workflow_completed"
    NEEDS_REVIEW = "needs_review"
    WORKFLOW_FAILED = "workflow_failed"


class WorkflowDecision(enum.Enum):
    """Workflow approval decision states"""
    PENDING = "pending"
    APPROVED = "approved"
    NEEDS_REVISION = "needs_revision"
    REJECTED = "rejected"


class CommentType(enum.Enum):
    """Comment source types"""
    REVIEWER = "reviewer"  # From council member or internal reviewer
    CUSTOMER = "customer"  # From tenant owner/collaborator
    SYSTEM = "system"  # Automated timeline events


class DraftStatus(enum.Enum):
    """Workflow draft status"""
    EDITING = "editing"  # User is still editing
    PENDING_REVIEW = "pending_review"  # Submitted for council review
    APPROVED = "approved"  # Approved and ready to convert
    REJECTED = "rejected"  # Rejected by council
    CONVERTED = "converted"  # Already converted to workflow
    DISCARDED = "discarded"  # User discarded the draft


class TemplateStatus(enum.Enum):
    """Workflow template status"""
    DRAFT = "draft"  # Template being created
    PENDING_REVIEW = "pending_review"  # Submitted for approval
    APPROVED = "approved"  # Approved and active
    REJECTED = "rejected"  # Rejected by council
    DEPRECATED = "deprecated"  # Superseded by newer version


class TriggerType(enum.Enum):
    """Automation trigger types"""
    EVENT = "event"  # Fires when something happens
    SCHEDULE = "schedule"  # Fires on time pattern
    THRESHOLD = "threshold"  # Fires when metric crosses threshold
    BEHAVIOR = "behavior"  # Fires based on customer behavior


class ActionType(enum.Enum):
    """Automation action types"""
    START_WORKFLOW = "start_workflow"  # Start a workflow from template
    SEND_NOTIFICATION = "send_notification"  # Send alert/email/push
    UPDATE_PRODUCT = "update_product"  # Modify product data
    GENERATE_CAMPAIGN = "generate_campaign"  # Create marketing campaign
    CREATE_LANDING_PAGE = "create_landing_page"  # Generate landing page
    ADD_PRODUCT = "add_product"  # Create new product
    UPDATE_STORE = "update_store"  # Modify store settings
    GENERATE_DRAFT = "generate_draft"  # Create workflow draft


class RiskLevel(enum.Enum):
    """Automation risk levels for governance"""
    LOW = "low"  # Safe for auto-execution
    MEDIUM = "medium"  # Review recommended
    HIGH = "high"  # Requires council approval
    CRITICAL = "critical"  # Always requires approval


class ProposalStatus(enum.Enum):
    """AI workflow proposal status"""
    PENDING = "pending"  # Waiting for user action
    ACCEPTED = "accepted"  # User accepted and created draft
    DISMISSED = "dismissed"  # User dismissed
    EXPIRED = "expired"  # Too old to be relevant


class EventResult(enum.Enum):
    """Automation event execution results"""
    SUCCESS = "success"  # Automation fired successfully
    SKIPPED = "skipped"  # Automation did not fire (no match, conditions not met)
    FAILED = "failed"  # Automation encountered an error


class RecommendationType(enum.Enum):
    """AI Advisor recommendation types"""
    WORKFLOW = "workflow"  # Suggest creating a workflow
    AUTOMATION = "automation"  # Suggest enabling automation
    PRODUCT = "product"  # Suggest adding/updating products
    CAMPAIGN = "campaign"  # Suggest marketing campaigns
    OPTIMIZATION = "optimization"  # Suggest optimizations
    ALERT = "alert"  # Alert about issues


class RecommendationStatus(enum.Enum):
    """Status of advisor recommendations"""
    PENDING = "pending"  # Not yet acted upon
    ACCEPTED = "accepted"  # Tenant accepted recommendation
    DISMISSED = "dismissed"  # Tenant dismissed recommendation
    EXPIRED = "expired"  # Time-sensitive recommendation expired
    COMPLETED = "completed"  # Action completed


# ============================================================================
# ASSOCIATION TABLES (Many-to-Many)
# ============================================================================

user_councils = Table(
    'user_councils',
    Base.metadata,
    Column('user_id', String, ForeignKey('users.id'), primary_key=True),
    Column('council_id', String, ForeignKey('councils.id'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow)
)


# ============================================================================# TENANCY
# ============================================================================

class Tenant(Base):
    """
    Multi-tenant organization model
    
    Each tenant represents a client business using Codex Dominion as a service.
    Owns users, stores, workflows, sites.
    """
    __tablename__ = 'tenants'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)  # e.g., "Brand X Studios"
    slug = Column(String, nullable=False, unique=True, index=True)  # URL-safe identifier
    
    # Billing
    plan = Column(String, default="starter")  # starter, growth, enterprise
    status = Column(String, default="active")  # active, suspended, cancelled
    
    # Settings
    settings = Column(JSON, nullable=True, default=dict)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    workflows = relationship("Workflow", back_populates="tenant")
    stores = relationship("Store", back_populates="tenant")
    automation_rules = relationship("AutomationRule", back_populates="tenant")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "plan": self.plan,
            "status": self.status,
            "settings": self.settings,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# ============================================================================# AUTHENTICATION MODELS
# ============================================================================

class User(Base):
    """
    User model with authentication and role-based permissions
    
    Roles:
    - admin: Full system access, can edit councils and agents
    - council_operator: Can vote on workflows in assigned councils
    - viewer: Read-only access
    """
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey('tenants.id'), nullable=True, index=True)  # Nullable for internal users
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.VIEWER)
    user_type = Column(String, nullable=True)  # 'creator', 'youth', or 'both'
    onboarding_completed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    councils = relationship(
        "Council",
        secondary=user_councils,
        back_populates="operators",
        doc="Councils this user can operate (vote on workflows)"
    )
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    workflow_votes = relationship("WorkflowVote", back_populates="user", cascade="all, delete-orphan")
    
    def set_password(self, password: str):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def has_permission(self, permission: str) -> bool:
        """
        Check if user has a specific permission
        
        Permissions:
        - edit_councils: Admin only
        - edit_agents: Admin only
        - vote_workflow: Admin or council_operator (in assigned council)
        - view_all: All roles
        """
        if self.role == UserRole.ADMIN:
            return True  # Admin has all permissions
        
        if permission == "view_all":
            return True  # All users can view
        
        if permission == "vote_workflow" and self.role == UserRole.COUNCIL_OPERATOR:
            return True
        
        return False
    
    def can_vote_in_council(self, council_id: str) -> bool:
        """Check if user can vote in specific council"""
        if self.role == UserRole.ADMIN:
            return True
        
        if self.role == UserRole.COUNCIL_OPERATOR:
            return any(c.id == council_id for c in self.councils)
        
        return False
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """Convert to dictionary"""
        data = {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role.value,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "council_ids": [c.id for c in self.councils] if self.councils else []
        }
        
        if include_sensitive:
            data["password_hash"] = self.password_hash
        
        return data


class AuditLog(Base):
    """
    Audit log for security-sensitive actions
    
    Tracks:
    - User logins
    - Permission changes
    - Council votes
    - Agent/council edits
    """
    __tablename__ = 'audit_logs'
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    action = Column(String, nullable=False)
    resource_type = Column(String, nullable=True)  # council, agent, workflow, etc.
    resource_id = Column(String, nullable=True)
    details = Column(Text, nullable=True)  # JSON string for additional context
    ip_address = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    user = relationship("User", back_populates="audit_logs")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "details": self.details,
            "ip_address": self.ip_address,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }


# ============================================================================
# GOVERNANCE MODELS
# ============================================================================

class Council(Base):
    """
    Council governance model
    
    Represents a decision-making council that reviews and votes on workflows
    """
    __tablename__ = 'councils'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Council configuration (stored as JSON)
    config = Column(JSON, nullable=True, default=dict)
    
    # Relationships
    operators = relationship(
        "User",
        secondary=user_councils,
        back_populates="councils",
        doc="Users who can vote on workflows in this council"
    )
    members = relationship("CouncilMember", back_populates="council", cascade="all, delete-orphan")
    workflows = relationship("Workflow", back_populates="assigned_council")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "config": self.config,
            "operator_ids": [u.id for u in self.operators] if self.operators else [],
            "member_count": len(self.members) if self.members else 0
        }


class CouncilMember(Base):
    """
    Individual council members (agents or entities)
    """
    __tablename__ = 'council_members'
    
    id = Column(String, primary_key=True)
    council_id = Column(String, ForeignKey('councils.id'), nullable=False)
    agent_id = Column(String, ForeignKey('agents.id'), nullable=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=True)  # e.g., "chair", "secretary"
    is_active = Column(Boolean, default=True)
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    council = relationship("Council", back_populates="members")
    agent = relationship("Agent", foreign_keys=[agent_id])
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "council_id": self.council_id,
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "is_active": self.is_active,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None
        }


# ============================================================================
# AGENT MODELS
# ============================================================================

class Agent(Base):
    """
    AI Agent model
    
    Represents an autonomous agent in the Codex Dominion system
    """
    __tablename__ = 'agents'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    display_name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Agent capabilities (stored as JSON)
    capabilities = Column(JSON, nullable=True, default=dict)
    
    # Relationships
    reputation = relationship("AgentReputation", back_populates="agent", uselist=False, cascade="all, delete-orphan")
    training_records = relationship("AgentTraining", back_populates="agent", cascade="all, delete-orphan")
    created_workflows = relationship("Workflow", foreign_keys="Workflow.created_by_agent", back_populates="creator")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        data = {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "avatar_url": self.avatar_url,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "capabilities": self.capabilities
        }
        
        # Include reputation if loaded
        if self.reputation:
            data["reputation"] = self.reputation.to_dict()
        
        return data


class AgentReputation(Base):
    """
    Agent reputation and performance metrics
    """
    __tablename__ = 'agent_reputations'
    
    id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey('agents.id'), nullable=False, unique=True)
    trust_score = Column(Float, default=0.0)
    total_actions = Column(Integer, default=0)
    successful_actions = Column(Integer, default=0)
    failed_actions = Column(Integer, default=0)
    total_savings_generated = Column(Float, default=0.0)
    last_action_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    agent = relationship("Agent", back_populates="reputation")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        success_rate = (self.successful_actions / self.total_actions * 100) if self.total_actions > 0 else 0.0
        
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "trust_score": self.trust_score,
            "total_actions": self.total_actions,
            "successful_actions": self.successful_actions,
            "failed_actions": self.failed_actions,
            "success_rate": round(success_rate, 2),
            "total_savings_generated": self.total_savings_generated,
            "last_action_at": self.last_action_at.isoformat() if self.last_action_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class AgentTraining(Base):
    """
    Agent training records and learning history
    """
    __tablename__ = 'agent_training'
    
    id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey('agents.id'), nullable=False)
    training_type = Column(String, nullable=False)  # e.g., "workflow", "conversation"
    topic = Column(String, nullable=True)
    outcome = Column(String, nullable=True)  # "success", "failure", "partial"
    feedback_score = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    trained_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    agent = relationship("Agent", back_populates="training_records")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "training_type": self.training_type,
            "topic": self.topic,
            "outcome": self.outcome,
            "feedback_score": self.feedback_score,
            "notes": self.notes,
            "trained_at": self.trained_at.isoformat() if self.trained_at else None
        }


# ============================================================================
# WORKFLOW MODELS
# ============================================================================

class WorkflowType(Base):
    """
    Workflow type definitions
    """
    __tablename__ = 'workflow_types'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)  # e.g., "finance", "operations"
    domain = Column(String, nullable=True)  # Domain for council routing (commerce, finance, media, etc.)
    required_inputs = Column(JSON, nullable=True)  # JSON array of input specifications
    expected_outputs = Column(JSON, nullable=True)  # JSON array of output field names
    estimated_duration_minutes = Column(Integer, nullable=True)  # Expected execution time
    estimated_savings_weekly = Column(Float, nullable=True)  # USD saved per week
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workflows = relationship("Workflow", back_populates="workflow_type")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "domain": self.domain,
            "required_inputs": self.required_inputs,
            "expected_outputs": self.expected_outputs,
            "estimated_duration_minutes": self.estimated_duration_minutes,
            "estimated_savings_weekly": self.estimated_savings_weekly,
            "estimated_savings_annual": self.estimated_savings_weekly * 52 if self.estimated_savings_weekly else None,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Workflow(Base):
    """
    Workflow model for agent actions
    
    Tracks workflow execution from creation through council approval to completion
    """
    __tablename__ = 'workflows'
    
    id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey('tenants.id'), nullable=True, index=True)  # Nullable for internal workflows
    workflow_type_id = Column(String, ForeignKey('workflow_types.id'), nullable=False)
    created_by_agent = Column(String, ForeignKey('agents.id'), nullable=False)
    assigned_council_id = Column(String, ForeignKey('councils.id'), nullable=True)
    
    # Type & category
    type = Column(String, nullable=True)  # e.g. "sales.empire_store_ignition_intake"
    category = Column(String, nullable=True)  # e.g. "sales", "store", "social"
    
    # Status & decision
    status = Column(SQLEnum(WorkflowStatus), default=WorkflowStatus.PENDING, index=True)
    decision = Column(String, nullable=True)  # DEPRECATED - use decision_status
    decision_status = Column(SQLEnum(WorkflowDecision), default=WorkflowDecision.PENDING, index=True)
    
    # Review tracking
    reviewed_by_user_id = Column(String, ForeignKey('users.id'), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    review_comment = Column(Text, nullable=True)
    resubmission_count = Column(Integer, default=0)
    
    # Linking / hierarchy
    parent_workflow_id = Column(String, nullable=True, index=True)  # Parent workflow
    related_store_id = Column(String, ForeignKey('stores.id'), nullable=True, index=True)  # Related store
    
    # Workflow data
    inputs = Column(JSON, nullable=True, default=dict)
    outputs = Column(JSON, nullable=True, default=dict)
    calculated_savings = Column(JSON, nullable=True, default=dict)
    summary = Column(Text, nullable=True)  # AI-generated summary for councils
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Error tracking
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="workflows")
    workflow_type = relationship("WorkflowType", back_populates="workflows")
    creator = relationship("Agent", foreign_keys=[created_by_agent], back_populates="created_workflows")
    assigned_council = relationship("Council", back_populates="workflows")
    related_store = relationship("Store", foreign_keys=[related_store_id], back_populates="workflows")
    reviewed_by = relationship("User", foreign_keys=[reviewed_by_user_id])
    artifacts = relationship("WorkflowArtifact", back_populates="workflow", cascade="all, delete-orphan")
    metrics = relationship("WorkflowMetric", back_populates="workflow", cascade="all, delete-orphan")
    votes = relationship("WorkflowVote", back_populates="workflow", cascade="all, delete-orphan")
    comments = relationship("WorkflowComment", back_populates="workflow", cascade="all, delete-orphan")
    timeline_events = relationship("WorkflowTimelineEvent", back_populates="workflow", cascade="all, delete-orphan")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        # Extract weekly savings from calculated_savings
        weekly_savings = 0
        if self.calculated_savings:
            weekly_savings = (
                self.calculated_savings.get("weekly_savings") or 
                self.calculated_savings.get("total_weekly_savings") or 
                0
            )
        
        return {
            "id": self.id,
            "workflow_type_id": self.workflow_type_id,
            "created_by_agent": self.created_by_agent,
            "assigned_council_id": self.assigned_council_id,
            "status": self.status.value,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "calculated_savings": self.calculated_savings,
            "weekly_savings": weekly_savings,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "error_message": self.error_message,
            "retry_count": self.retry_count
        }


class WorkflowArtifact(Base):
    """
    Workflow artifacts - things created by workflows (URLs, files, IDs)
    
    Stores artifacts separately for cleaner UI display without overloading workflow row.
    """
    __tablename__ = 'workflow_artifacts'
    
    id = Column(String, primary_key=True)
    workflow_id = Column(String, ForeignKey('workflows.id'), nullable=False, index=True)
    tenant_id = Column(String, ForeignKey('tenants.id'), nullable=False, index=True)
    
    # Artifact metadata
    kind = Column(String, nullable=False)  # storefront_url, admin_url, marketing_site_url, product_list, etc.
    label = Column(String, nullable=False)  # Human description: "Storefront URL", "Product Catalog JSON"
    value = Column(Text, nullable=True)  # URL, JSON, or text content
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workflow = relationship("Workflow", back_populates="artifacts")
    tenant = relationship("Tenant")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "workflow_id": self.workflow_id,
            "tenant_id": self.tenant_id,
            "kind": self.kind,
            "label": self.label,
            "value": self.value,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class WorkflowMetric(Base):
    """
    Performance metrics for workflow execution
    """
    __tablename__ = 'workflow_metrics'
    
    id = Column(String, primary_key=True)
    workflow_id = Column(String, ForeignKey('workflows.id'), nullable=False)
    
    # Performance metrics
    duration_seconds = Column(Float, nullable=True)
    cpu_usage_percent = Column(Float, nullable=True)
    memory_usage_mb = Column(Float, nullable=True)
    api_calls_made = Column(Integer, default=0)
    estimated_weekly_savings = Column(Float, default=0.0)
    
    # Quality metrics
    success_rate = Column(Float, nullable=True)
    error_count = Column(Integer, default=0)
    
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    workflow = relationship("Workflow", back_populates="metrics")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "workflow_id": self.workflow_id,
            "duration_seconds": self.duration_seconds,
            "cpu_usage_percent": self.cpu_usage_percent,
            "memory_usage_mb": self.memory_usage_mb,
            "api_calls_made": self.api_calls_made,
            "estimated_weekly_savings": self.estimated_weekly_savings,
            "success_rate": self.success_rate,
            "error_count": self.error_count,
            "recorded_at": self.recorded_at.isoformat() if self.recorded_at else None
        }


class WorkflowVote(Base):
    """
    Council voting records on workflows
    """
    __tablename__ = 'workflow_votes'
    __table_args__ = (
        UniqueConstraint('workflow_id', 'user_id', name='unique_workflow_user_vote'),
    )
    
    id = Column(String, primary_key=True)
    workflow_id = Column(String, ForeignKey('workflows.id'), nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    
    # Vote details
    vote = Column(String, nullable=False)  # "approve", "reject", "abstain"
    comment = Column(Text, nullable=True)
    voted_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workflow = relationship("Workflow", back_populates="votes")
    user = relationship("User", back_populates="workflow_votes")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "workflow_id": self.workflow_id,
            "user_id": self.user_id,
            "vote": self.vote,
            "comment": self.comment,
            "voted_at": self.voted_at.isoformat() if self.voted_at else None
        }


# ============================================================================
# STORE MODEL
# ============================================================================

class Store(Base):
    """
    E-commerce store model
    
    Represents a customer's Shopify/WooCommerce store managed by Codex Dominion.
    """
    __tablename__ = 'stores'
    
    id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey('tenants.id'), nullable=False, index=True)
    
    # Identity
    name = Column(String, nullable=False)  # Brand/store name
    platform = Column(String, nullable=False)  # shopify, woocommerce
    domain = Column(String, nullable=False, unique=True, index=True)  # mybrand.myshopify.com
    storefront_url = Column(String, nullable=True)  # Public URL
    admin_url = Column(String, nullable=True)  # Admin dashboard URL
    
    # Connection / Credentials (encrypted in production)
    access_token = Column(String, nullable=True)  # Platform access token
    owner_email = Column(String, nullable=True)  # Store owner email
    
    # Store settings
    settings = Column(JSON, nullable=True, default=dict)  # colors, fonts, categories, etc.
    
    # Status
    status = Column(String, default="pending_setup")  # pending_setup, active, error
    created_via_workflow_id = Column(String, ForeignKey('workflows.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="stores")
    workflows = relationship("Workflow", foreign_keys="Workflow.related_store_id", back_populates="related_store")
    created_via_workflow = relationship("Workflow", foreign_keys=[created_via_workflow_id])
    
    def to_dict(self) -> dict:
        """Convert to dictionary (excludes credentials)"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "platform": self.platform,
            "domain": self.domain,
            "settings": self.settings,
            "status": self.status,
            "created_by_workflow_id": self.created_by_workflow_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# ============================================================================
# PORTAL NOTIFICATIONS
# ============================================================================

class PortalNotification(Base):
    """
    Portal notifications for workflow lifecycle events
    
    Notifications appear in /portal/notifications and notify users
    about workflow progress, completions, and issues.
    """
    __tablename__ = 'portal_notifications'
    
    id = Column(String, primary_key=True, default=lambda: f"notif_{datetime.utcnow().timestamp()}")
    tenant_id = Column(String, ForeignKey('tenants.id'), nullable=False, index=True)
    workflow_id = Column(String, ForeignKey('workflows.id'), nullable=False, index=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=True, index=True)  # Specific user or null for all tenant users
    
    # Notification content
    type = Column(SQLEnum(NotificationType), nullable=False, index=True)
    subject = Column(String, nullable=False)  # Email subject / notification title
    body = Column(Text, nullable=False)  # Email body / notification message
    
    # Metadata
    step_name = Column(String, nullable=True)  # For step_completed notifications
    summary = Column(JSON, nullable=True, default=dict)  # For workflow_completed highlights
    
    # Status tracking
    is_read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime, nullable=True)
    email_sent = Column(Boolean, default=False)
    email_sent_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    tenant = relationship("Tenant")
    workflow = relationship("Workflow")
    user = relationship("User")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "workflow_id": self.workflow_id,
            "user_id": self.user_id,
            "type": self.type.value if self.type else None,
            "subject": self.subject,
            "body": self.body,
            "step_name": self.step_name,
            "summary": self.summary,
            "is_read": self.is_read,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "workflow": {
                "id": self.workflow.id,
                "workflow_type_id": self.workflow.workflow_type_id,
                "status": self.workflow.status.value if self.workflow.status else None
            } if self.workflow else None
        }
    
    def mark_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.read_at = datetime.utcnow()


# ============================================================================
# WORKFLOW REVIEW & COMMENTS
# ============================================================================

class WorkflowComment(Base):
    """
    Comments on workflows for review and collaboration
    
    Supports threaded discussions between reviewers, customers, and system events
    """
    __tablename__ = 'workflow_comments'
    
    id = Column(String, primary_key=True)
    workflow_id = Column(String, ForeignKey('workflows.id'), nullable=False, index=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    parent_id = Column(String, ForeignKey('workflow_comments.id'), nullable=True)  # For threading
    
    # Comment details
    comment_type = Column(SQLEnum(CommentType), default=CommentType.CUSTOMER)
    content = Column(Text, nullable=False)  # Markdown supported
    
    # Resolution tracking
    is_resolved = Column(Boolean, default=False)
    resolved_by_user_id = Column(String, ForeignKey('users.id'), nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workflow = relationship("Workflow", back_populates="comments")
    user = relationship("User", foreign_keys=[user_id])
    resolved_by = relationship("User", foreign_keys=[resolved_by_user_id])
    parent = relationship("WorkflowComment", remote_side=[id], backref="replies")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "workflow_id": self.workflow_id,
            "user_id": self.user_id,
            "parent_id": self.parent_id,
            "comment_type": self.comment_type.value if self.comment_type else None,
            "content": self.content,
            "is_resolved": self.is_resolved,
            "resolved_by_user_id": self.resolved_by_user_id,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user": {
                "id": self.user.id,
                "name": self.user.name,
                "email": self.user.email,
                "role": self.user.role.value if self.user.role else None
            } if self.user else None,
            "reply_count": len(self.replies) if hasattr(self, 'replies') else 0
        }


class WorkflowTimelineEvent(Base):
    """
    Timeline events for workflow history tracking
    
    Records key milestones: submission, approval, changes requested, resubmission
    """
    __tablename__ = 'workflow_timeline_events'
    
    id = Column(String, primary_key=True)
    workflow_id = Column(String, ForeignKey('workflows.id'), nullable=False, index=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=True)  # Null for system events
    
    # Event details
    event_type = Column(String, nullable=False)  # created, approved, changes_requested, resubmitted, completed, failed
    title = Column(String, nullable=False)  # e.g., "Workflow approved by John Doe"
    description = Column(Text, nullable=True)
    event_metadata = Column(JSON, nullable=True)  # Additional event context (renamed from metadata to avoid SQLAlchemy conflict)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    workflow = relationship("Workflow", back_populates="timeline_events")
    user = relationship("User")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "workflow_id": self.workflow_id,
            "user_id": self.user_id,
            "event_type": self.event_type,
            "title": self.title,
            "description": self.description,
            "metadata": self.event_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user": {
                "id": self.user.id,
                "name": self.user.name
            } if self.user else None
        }


# ============================================================================
# DRAFT MODE & TEMPLATES
# ============================================================================

class WorkflowDraft(Base):
    """
    Workflow draft - a proposal that hasn't been executed yet
    
    Drafts can be created by:
    - Users manually
    - AI proposals
    - Council-approved templates
    
    Lifecycle: editing → pending_review → approved → converted to Workflow
    """
    __tablename__ = 'workflow_drafts'
    
    id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey('tenants.id'), nullable=False, index=True)
    created_by_user_id = Column(String, ForeignKey('users.id'), nullable=False)
    workflow_type_id = Column(String, nullable=False)  # Type of workflow this draft will create
    
    # Draft content
    name = Column(String, nullable=False)  # User-friendly name
    purpose = Column(Text, nullable=True)  # What this draft is trying to achieve
    inputs = Column(JSON, nullable=True, default=dict)  # User-editable inputs
    preview_data = Column(JSON, nullable=True, default=dict)  # Generated preview content
    
    # Metadata
    status = Column(SQLEnum(DraftStatus), default=DraftStatus.EDITING, index=True)
    expected_outputs = Column(JSON, nullable=True)  # What will be created
    estimated_duration_minutes = Column(Integer, nullable=True)
    required_approvals = Column(JSON, nullable=True)  # List of council IDs or roles
    dependencies = Column(JSON, nullable=True)  # Prerequisites (e.g., ["store_exists"])
    
    # Source tracking
    created_from_template_id = Column(String, ForeignKey('workflow_templates.id'), nullable=True)
    created_from_proposal_id = Column(String, ForeignKey('ai_workflow_proposals.id'), nullable=True)
    
    # Review tracking
    assigned_council_id = Column(String, ForeignKey('councils.id'), nullable=True)
    reviewed_by_user_id = Column(String, ForeignKey('users.id'), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    review_comment = Column(Text, nullable=True)
    
    # Conversion tracking
    converted_to_workflow_id = Column(String, ForeignKey('workflows.id'), nullable=True, unique=True)
    converted_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_edited_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant")
    created_by = relationship("User", foreign_keys=[created_by_user_id])
    reviewed_by = relationship("User", foreign_keys=[reviewed_by_user_id])
    assigned_council = relationship("Council")
    template = relationship("WorkflowTemplate", foreign_keys=[created_from_template_id])
    proposal = relationship("AIWorkflowProposal", foreign_keys=[created_from_proposal_id])
    converted_workflow = relationship("Workflow", foreign_keys=[converted_to_workflow_id])
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "workflow_type_id": self.workflow_type_id,
            "name": self.name,
            "purpose": self.purpose,
            "status": self.status.value if self.status else None,
            "inputs": self.inputs,
            "preview_data": self.preview_data,
            "expected_outputs": self.expected_outputs,
            "estimated_duration_minutes": self.estimated_duration_minutes,
            "required_approvals": self.required_approvals,
            "dependencies": self.dependencies,
            "created_by_user_id": self.created_by_user_id,
            "assigned_council_id": self.assigned_council_id,
            "converted_to_workflow_id": self.converted_to_workflow_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_edited_at": self.last_edited_at.isoformat() if self.last_edited_at else None,
            "created_by": {
                "id": self.created_by.id,
                "name": self.created_by.name
            } if self.created_by else None
        }


class WorkflowTemplate(Base):
    """
    Council-approved workflow templates
    
    Pre-approved blueprints that customers can use instantly without review.
    Templates include default values, approved copy, and structure.
    """
    __tablename__ = 'workflow_templates'
    
    id = Column(String, primary_key=True)
    workflow_type_id = Column(String, nullable=False, index=True)
    
    # Template metadata
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)  # "commerce", "media", "automation", etc.
    icon = Column(String, nullable=True)  # Icon name for UI
    
    # Template content
    default_inputs = Column(JSON, nullable=True, default=dict)  # Pre-filled values
    required_input_fields = Column(JSON, nullable=True, default=list)  # Fields user must fill
    optional_input_fields = Column(JSON, nullable=True, default=list)  # Fields user can fill
    approved_copy_blocks = Column(JSON, nullable=True)  # Pre-approved text templates
    approved_structure = Column(JSON, nullable=True)  # Pre-approved workflow structure
    
    # Approval tracking
    is_active = Column(Boolean, default=True)
    is_pre_approved = Column(Boolean, default=False)  # If true, no council review needed
    approved_by_council_id = Column(String, ForeignKey('councils.id'), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    approved_by_council = relationship("Council")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "workflow_type_id": self.workflow_type_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "icon": self.icon,
            "default_inputs": self.default_inputs,
            "required_input_fields": self.required_input_fields,
            "optional_input_fields": self.optional_input_fields,
            "is_active": self.is_active,
            "is_pre_approved": self.is_pre_approved,
            "usage_count": self.usage_count,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def increment_usage(self):
        """Track template usage"""
        self.usage_count += 1
        self.last_used_at = datetime.utcnow()


class AIWorkflowProposal(Base):
    """
    AI-generated workflow proposals
    
    The AI scans tenant data and proposes workflows proactively.
    Proposals become drafts when accepted by the user.
    """
    __tablename__ = 'ai_workflow_proposals'
    
    id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey('tenants.id'), nullable=False, index=True)
    workflow_type_id = Column(String, nullable=False)
    
    # Proposal content
    title = Column(String, nullable=False)  # e.g., "Holiday Bundle Launch"
    description = Column(Text, nullable=False)  # Why this is recommended
    reasoning = Column(Text, nullable=True)  # AI explanation
    
    # AI analysis
    confidence_score = Column(Float, nullable=True)  # 0.0 to 1.0
    based_on = Column(JSON, nullable=True)  # Factors considered (sales, trends, gaps)
    expected_impact = Column(JSON, nullable=True)  # Predicted outcomes
    
    # Proposed workflow data
    suggested_inputs = Column(JSON, nullable=True, default=dict)  # Pre-filled recommendations
    
    # Status tracking
    status = Column(SQLEnum(ProposalStatus), default=ProposalStatus.PENDING, index=True)
    priority = Column(String, default="normal")  # low, normal, high, urgent
    expires_at = Column(DateTime, nullable=True)  # When proposal becomes irrelevant
    
    # User action tracking
    viewed_at = Column(DateTime, nullable=True)
    acted_on_at = Column(DateTime, nullable=True)
    created_draft_id = Column(String, ForeignKey('workflow_drafts.id'), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    tenant = relationship("Tenant")
    created_draft = relationship("WorkflowDraft", foreign_keys=[created_draft_id])
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "workflow_type_id": self.workflow_type_id,
            "title": self.title,
            "description": self.description,
            "reasoning": self.reasoning,
            "confidence_score": self.confidence_score,
            "based_on": self.based_on,
            "expected_impact": self.expected_impact,
            "suggested_inputs": self.suggested_inputs,
            "status": self.status.value if self.status else None,
            "priority": self.priority,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "viewed_at": self.viewed_at.isoformat() if self.viewed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


# ============================================================================
# AUTOMATION RULES
# ============================================================================

class AutomationRule(Base):
    """
    Automation rules that trigger workflows, notifications, or actions
    based on events, schedules, thresholds, or customer behavior.
    
    Schema Structure:
    - identity: name, description, category, enabled
    - trigger: type (event/schedule/threshold/behavior), config
    - conditions: list of logical checks (product count, store status, etc.)
    - action: what to do (start workflow, send notification, etc.)
    - governance: council approval, risk level, auto-approval rules
    """
    __tablename__ = 'automation_rules'
    
    # Identity
    id = Column(String, primary_key=True, default=lambda: f"automation_{uuid.uuid4().hex[:12]}")
    tenant_id = Column(String, ForeignKey('tenants.id'), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))  # marketing, store, product, campaign, customer
    enabled = Column(Boolean, default=True, index=True)
    
    # Trigger Configuration
    trigger_type = Column(SQLEnum(TriggerType), nullable=False, index=True)
    trigger_config = Column(JSON, nullable=False)
    # trigger_config examples:
    # EVENT: {"event_type": "product_added", "source": "store"}
    # SCHEDULE: {"pattern": "daily", "time": "09:00", "timezone": "UTC"}
    # THRESHOLD: {"metric": "product_count", "operator": "<", "value": 3}
    # BEHAVIOR: {"behavior_type": "abandoned_cart", "timeframe_hours": 24}
    
    # Conditions (all must pass)
    conditions = Column(JSON, default=list)
    # conditions format:
    # [
    #   {"type": "product_count", "operator": "<", "value": 3},
    #   {"type": "workflow_status", "operator": "=", "value": "completed"},
    #   {"type": "date", "operator": ">=", "value": "2025-12-01"}
    # ]
    
    # Action Configuration
    action_type = Column(SQLEnum(ActionType), nullable=False)
    action_config = Column(JSON, nullable=False)
    # action_config examples:
    # START_WORKFLOW: {"workflow_type_id": "website_creation", "template_id": "basic_site"}
    # SEND_NOTIFICATION: {"recipients": ["owner"], "message": "Low product count"}
    # GENERATE_CAMPAIGN: {"template_id": "seasonal_promo", "channels": ["email", "social"]}
    
    # Governance
    risk_level = Column(SQLEnum(RiskLevel), default=RiskLevel.LOW, index=True)
    requires_approval = Column(Boolean, default=False)
    assigned_council_id = Column(String, ForeignKey('councils.id'), index=True)
    auto_approval_rules = Column(JSON, default=dict)
    # auto_approval_rules format:
    # {"max_budget": 100, "trusted_users_only": true, "business_hours_only": false}
    
    # Execution Tracking
    last_triggered_at = Column(DateTime)
    last_executed_at = Column(DateTime)
    execution_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)
    average_execution_time_ms = Column(Float)
    
    # Metadata
    created_by_user_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship('Tenant', back_populates='automation_rules')
    council = relationship('Council', foreign_keys=[assigned_council_id])
    execution_logs = relationship('AutomationExecution', back_populates='automation_rule', cascade='all, delete-orphan')
    events = relationship('AutomationEvent', back_populates='automation', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "enabled": self.enabled,
            "trigger_type": self.trigger_type.value if self.trigger_type else None,
            "trigger_config": self.trigger_config,
            "conditions": self.conditions,
            "action_type": self.action_type.value if self.action_type else None,
            "action_config": self.action_config,
            "risk_level": self.risk_level.value if self.risk_level else None,
            "requires_approval": self.requires_approval,
            "assigned_council_id": self.assigned_council_id,
            "auto_approval_rules": self.auto_approval_rules,
            "last_triggered_at": self.last_triggered_at.isoformat() if self.last_triggered_at else None,
            "last_executed_at": self.last_executed_at.isoformat() if self.last_executed_at else None,
            "execution_count": self.execution_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "average_execution_time_ms": self.average_execution_time_ms,
            "created_by_user_id": self.created_by_user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def evaluate_conditions(self, context: dict) -> bool:
        """
        Evaluate all conditions against the provided context.
        Returns True if all conditions pass, False otherwise.
        
        Args:
            context: Dictionary with metrics and state (e.g., {"product_count": 2, "store_status": "active"})
        """
        if not self.conditions:
            return True
        
        for condition in self.conditions:
            condition_type = condition.get("type")
            operator = condition.get("operator")
            expected_value = condition.get("value")
            
            actual_value = context.get(condition_type)
            
            if actual_value is None:
                return False  # Missing required context
            
            # Evaluate based on operator
            if operator == "=":
                if actual_value != expected_value:
                    return False
            elif operator == "!=":
                if actual_value == expected_value:
                    return False
            elif operator == "<":
                if actual_value >= expected_value:
                    return False
            elif operator == ">":
                if actual_value <= expected_value:
                    return False
            elif operator == "<=":
                if actual_value > expected_value:
                    return False
            elif operator == ">=":
                if actual_value < expected_value:
                    return False
            elif operator == "contains":
                if expected_value not in str(actual_value):
                    return False
            elif operator == "not_contains":
                if expected_value in str(actual_value):
                    return False
        
        return True  # All conditions passed
    
    def should_auto_approve(self, context: dict) -> bool:
        """
        Check if this automation can be auto-approved based on governance rules.
        
        Args:
            context: Dictionary with execution context (e.g., {"user_trusted": True, "budget": 50})
        """
        if not self.auto_approval_rules:
            return self.risk_level == RiskLevel.LOW
        
        # Check budget limit
        max_budget = self.auto_approval_rules.get("max_budget")
        if max_budget and context.get("budget", 0) > max_budget:
            return False
        
        # Check trusted users only
        if self.auto_approval_rules.get("trusted_users_only") and not context.get("user_trusted"):
            return False
        
        # Check business hours
        if self.auto_approval_rules.get("business_hours_only"):
            current_hour = datetime.utcnow().hour
            if not (9 <= current_hour <= 17):  # 9 AM to 5 PM UTC
                return False
        
        return True
    
    def record_execution(self, success: bool, execution_time_ms: float):
        """Record execution statistics"""
        self.execution_count += 1
        self.last_executed_at = datetime.utcnow()
        
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
        
        # Update rolling average execution time
        if self.average_execution_time_ms:
            self.average_execution_time_ms = (self.average_execution_time_ms * 0.9) + (execution_time_ms * 0.1)
        else:
            self.average_execution_time_ms = execution_time_ms


class AutomationExecution(Base):
    """
    Log of automation rule executions with results and timeline.
    """
    __tablename__ = 'automation_executions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    automation_rule_id = Column(String, ForeignKey('automation_rules.id'), nullable=False, index=True)
    tenant_id = Column(String, ForeignKey('tenants.id'), nullable=False, index=True)
    
    # Execution Details
    triggered_at = Column(DateTime, default=datetime.utcnow, index=True)
    trigger_source = Column(String(100))  # event, scheduler, manual
    trigger_data = Column(JSON)  # Event data or context that triggered execution
    
    # Condition Evaluation
    conditions_met = Column(Boolean, default=False)
    condition_results = Column(JSON)  # Detailed results of each condition check
    
    # Action Execution
    action_started_at = Column(DateTime)
    action_completed_at = Column(DateTime)
    action_result = Column(JSON)  # Result of action execution (workflow_id, notification_id, etc.)
    success = Column(Boolean, default=False, index=True)
    error_message = Column(Text)
    execution_time_ms = Column(Float)
    
    # Governance
    required_approval = Column(Boolean, default=False)
    approved_by_user_id = Column(String)
    approved_at = Column(DateTime)
    
    # Relationships
    automation_rule = relationship('AutomationRule', back_populates='execution_logs')
    tenant = relationship('Tenant')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "automation_rule_id": self.automation_rule_id,
            "tenant_id": self.tenant_id,
            "triggered_at": self.triggered_at.isoformat() if self.triggered_at else None,
            "trigger_source": self.trigger_source,
            "trigger_data": self.trigger_data,
            "conditions_met": self.conditions_met,
            "condition_results": self.condition_results,
            "action_started_at": self.action_started_at.isoformat() if self.action_started_at else None,
            "action_completed_at": self.action_completed_at.isoformat() if self.action_completed_at else None,
            "action_result": self.action_result,
            "success": self.success,
            "error_message": self.error_message,
            "execution_time_ms": self.execution_time_ms,
            "required_approval": self.required_approval,
            "approved_by_user_id": self.approved_by_user_id,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None
        }


class AutomationTemplate(Base):
    """
    Pre-built automation templates in the Automation Library.
    
    Templates are ready-to-use automations that tenants can enable with minimal configuration.
    Organized by category: Store, Marketing, Website, Customer Behavior, Analytics
    """
    __tablename__ = 'automation_templates'
    
    # Identity
    id = Column(String, primary_key=True, default=lambda: f"template_{uuid.uuid4().hex[:12]}")
    name = Column(String(255), nullable=False)
    description = Column(Text)
    short_description = Column(String(500))  # For card display
    icon = Column(String(50))  # Icon name (e.g., "bell", "zap", "mail")
    category = Column(String(100), nullable=False, index=True)
    # Categories: Store, Marketing, Website, Customer Behavior, Analytics
    
    # Template Configuration
    trigger_type = Column(SQLEnum(TriggerType), nullable=False)
    default_trigger_config = Column(JSON, nullable=False)
    default_conditions = Column(JSON, default=list)
    action_type = Column(SQLEnum(ActionType), nullable=False)
    default_action_config = Column(JSON, nullable=False)
    
    # Configuration Schema (defines what users can customize)
    config_schema = Column(JSON, default=list)
    # config_schema format:
    # [
    #   {
    #     "key": "platforms",
    #     "label": "Platforms",
    #     "type": "multiselect",
    #     "options": ["Instagram", "TikTok", "YouTube"],
    #     "default": ["Instagram"],
    #     "required": true,
    #     "help_text": "Where to post"
    #   }
    # ]
    
    # Governance
    risk_level = Column(SQLEnum(RiskLevel), default=RiskLevel.LOW)
    requires_approval = Column(Boolean, default=False)
    recommended_council_id = Column(String, ForeignKey('councils.id'))
    
    # Metadata
    popularity_score = Column(Float, default=0.0)  # Based on usage
    success_rate = Column(Float)  # Average success rate across all instances
    avg_value_generated = Column(Float)  # Average value (time saved, revenue, etc.)
    
    # AI Enhancement
    ai_enhanced = Column(Boolean, default=False)  # Uses AI for configuration
    ai_suggestion_rules = Column(JSON, default=dict)
    # ai_suggestion_rules format:
    # {
    #   "suggest_when": {
    #     "product_count": {"operator": "<", "value": 3}
    #   },
    #   "suggestion_message": "Your product catalog is low. Enable auto-generation?"
    # }
    
    # Status
    active = Column(Boolean, default=True)  # Available in library
    featured = Column(Boolean, default=False)  # Show in featured section
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    council = relationship('Council', foreign_keys=[recommended_council_id])
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "short_description": self.short_description,
            "icon": self.icon,
            "category": self.category,
            "trigger_type": self.trigger_type.value if self.trigger_type else None,
            "default_trigger_config": self.default_trigger_config,
            "default_conditions": self.default_conditions,
            "action_type": self.action_type.value if self.action_type else None,
            "default_action_config": self.default_action_config,
            "config_schema": self.config_schema,
            "risk_level": self.risk_level.value if self.risk_level else None,
            "requires_approval": self.requires_approval,
            "recommended_council_id": self.recommended_council_id,
            "popularity_score": self.popularity_score,
            "success_rate": self.success_rate,
            "avg_value_generated": self.avg_value_generated,
            "ai_enhanced": self.ai_enhanced,
            "ai_suggestion_rules": self.ai_suggestion_rules,
            "active": self.active,
            "featured": self.featured,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def create_automation_from_template(self, tenant_id: str, user_config: Dict[str, Any], created_by_user_id: str = None) -> 'AutomationRule':
        """
        Create an AutomationRule instance from this template with user configuration.
        
        Args:
            tenant_id: Tenant ID
            user_config: User-provided configuration values
            created_by_user_id: User who enabled the automation
        
        Returns:
            New AutomationRule instance
        """
        # Merge user config with defaults
        trigger_config = self.default_trigger_config.copy()
        action_config = self.default_action_config.copy()
        
        # Apply user configuration overrides
        for field in self.config_schema:
            key = field.get('key')
            if key in user_config:
                # Determine where to put this config value
                target = field.get('target', 'action_config')  # action_config or trigger_config
                if target == 'trigger_config':
                    trigger_config[key] = user_config[key]
                else:
                    action_config[key] = user_config[key]
        
        # Create automation rule
        automation = AutomationRule(
            tenant_id=tenant_id,
            name=f"{self.name} (from template)",
            description=self.description,
            category=self.category,
            trigger_type=self.trigger_type,
            trigger_config=trigger_config,
            conditions=self.default_conditions.copy(),
            action_type=self.action_type,
            action_config=action_config,
            risk_level=self.risk_level,
            requires_approval=self.requires_approval,
            assigned_council_id=self.recommended_council_id,
            created_by_user_id=created_by_user_id,
            enabled=not self.requires_approval  # Auto-enable if no approval needed
        )
        
        return automation
    
    def should_suggest_to_tenant(self, tenant_context: Dict[str, Any]) -> bool:
        """
        Check if this template should be suggested to a tenant based on their context.
        
        Args:
            tenant_context: Tenant's current state (product_count, store_status, etc.)
        
        Returns:
            True if should suggest, False otherwise
        """
        if not self.ai_suggestion_rules:
            return False
        
        suggest_when = self.ai_suggestion_rules.get('suggest_when', {})
        
        for metric, rule in suggest_when.items():
            operator = rule.get('operator')
            threshold = rule.get('value')
            actual_value = tenant_context.get(metric)
            
            if actual_value is None:
                continue
            
            # Evaluate condition
            if operator == '<' and actual_value < threshold:
                return True
            elif operator == '>' and actual_value > threshold:
                return True
            elif operator == '=' and actual_value == threshold:
                return True
            elif operator == '<=' and actual_value <= threshold:
                return True
            elif operator == '>=' and actual_value >= threshold:
                return True
        
        return False


class AutomationEvent(Base):
    """
    Timeline record of automation executions
    
    Every time an automation fires (success, skip, or fail), an event is created.
    Powers the Automation Timeline UI showing what automations have done.
    
    Example Events:
    - SUCCESS: "Weekly Social Post Generator" created 5 posts for Instagram
    - SKIPPED: "Abandoned Cart Sequence" had no abandoned carts
    - FAILED: "Homepage Hero Update" failed due to missing product data
    
    Fields:
    - id: Unique event identifier
    - tenant_id: Owner of this automation
    - automation_id: The AutomationRule that fired
    - timestamp: When this event occurred
    - trigger_type: What triggered it (event, schedule, threshold, behavior)
    - result: Outcome (success, skipped, failed)
    - message: Human-readable summary
    - workflow_id: Optional workflow created by this automation
    - metadata: JSON with additional details
    
    Usage:
        from automation_timeline_api import create_automation_event
        from models import EventResult
        
        event = create_automation_event(
            tenant_id="tenant_123",
            automation_id="auto_456",
            trigger_type=TriggerType.SCHEDULE,
            result=EventResult.SUCCESS,
            message="Generated 5 posts for Instagram and TikTok",
            workflow_id="workflow_789",
            metadata={"platforms": ["Instagram", "TikTok"], "post_count": 5}
        )
    """
    __tablename__ = 'automation_events'
    
    # Identity
    id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey('tenants.id'), nullable=False, index=True)
    automation_id = Column(String, ForeignKey('automation_rules.id'), nullable=False, index=True)
    
    # Timing
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Trigger
    trigger_type = Column(SQLEnum(TriggerType), nullable=False)
    
    # Result
    result = Column(SQLEnum(EventResult), nullable=False, index=True)
    message = Column(Text, nullable=False)  # "Generated 5 posts for Instagram"
    
    # Optional workflow created
    workflow_id = Column(String, ForeignKey('workflows.id'), nullable=True)
    
    # Additional details
    event_metadata = Column(JSON, nullable=True, default=dict)
    
    # Relationships
    tenant = relationship("Tenant")
    automation = relationship("AutomationRule", back_populates="events")
    workflow = relationship("Workflow")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "automation_id": self.automation_id,
            "timestamp": self.timestamp.isoformat() + 'Z' if self.timestamp else None,
            "trigger_type": self.trigger_type.value,
            "result": self.result.value,
            "message": self.message,
            "workflow_id": self.workflow_id,
            "metadata": self.event_metadata or {}
        }


class AutomationDebugLog(Base):
    """
    Debug log for automation execution - the truth table
    
    Stores detailed diagnostic information about why an automation
    triggered or didn't trigger, which conditions passed/failed,
    and what actions were taken.
    """
    __tablename__ = 'automation_debug_logs'
    
    id = Column(String, primary_key=True)
    tenant_id = Column(String, ForeignKey('tenants.id'), nullable=False, index=True)
    automation_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Trigger evaluation
    trigger_fired = Column(Boolean, nullable=False)  # Did the trigger activate?
    trigger_type = Column(SQLEnum(TriggerType), nullable=False)
    trigger_details = Column(JSON, nullable=True)  # When, why, what data
    next_scheduled_run = Column(DateTime, nullable=True)  # For scheduled triggers
    
    # Condition evaluation (array of results)
    conditions_evaluated = Column(JSON, nullable=True)  # List of condition checks
    # Example: [{"condition": "product_count < 3", "passed": true, "actual_value": 2}, ...]
    all_conditions_passed = Column(Boolean, nullable=False)
    
    # Action results
    actions_taken = Column(JSON, nullable=True)  # What actions were executed
    # Example: [{"action": "create_workflow", "status": "success", "workflow_id": "wf_123"}, ...]
    actions_skipped = Column(JSON, nullable=True)  # What was skipped and why
    
    # Execution metrics
    execution_time_ms = Column(Integer, nullable=True)
    errors = Column(JSON, nullable=True)  # Array of error messages
    warnings = Column(JSON, nullable=True)  # Array of warnings
    
    # Data snapshot (raw data evaluated)
    data_snapshot = Column(JSON, nullable=True)  # Input data, metrics, context
    
    # Result
    result = Column(SQLEnum(EventResult), nullable=False)  # SUCCESS, SKIPPED, FAILED
    workflow_id = Column(String, nullable=True)  # If workflow was created
    
    # Relationships
    tenant = relationship("Tenant")
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "automation_id": self.automation_id,
            "timestamp": self.timestamp.isoformat() + 'Z' if self.timestamp else None,
            "trigger_fired": self.trigger_fired,
            "trigger_type": self.trigger_type.value,
            "trigger_details": self.trigger_details or {},
            "next_scheduled_run": self.next_scheduled_run.isoformat() + 'Z' if self.next_scheduled_run else None,
            "conditions_evaluated": self.conditions_evaluated or [],
            "all_conditions_passed": self.all_conditions_passed,
            "actions_taken": self.actions_taken or [],
            "actions_skipped": self.actions_skipped or [],
            "execution_time_ms": self.execution_time_ms,
            "errors": self.errors or [],
            "warnings": self.warnings or [],
            "data_snapshot": self.data_snapshot or {},
            "result": self.result.value,
            "workflow_id": self.workflow_id
        }


# ============================================================================
# AI ADVISOR RECOMMENDATION MODEL
# ============================================================================

class AdvisorRecommendation(Base):
    """
    AI Advisor recommendations for workflows, automations, and optimizations.
    
    The Advisor monitors signals across the tenant's ecosystem and suggests
    actions to improve performance, capture opportunities, and mitigate risks.
    """
    __tablename__ = 'advisor_recommendations'
    
    # Core fields
    id = Column(String, primary_key=True)
    tenant_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Recommendation metadata
    recommendation_type = Column(SQLEnum(RecommendationType), nullable=False)
    status = Column(SQLEnum(RecommendationStatus), default=RecommendationStatus.PENDING, nullable=False)
    
    # Content
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    
    # Impact and confidence
    impact_level = Column(String(20), nullable=False)  # 'low', 'medium', 'high', 'critical'
    confidence_score = Column(Integer, nullable=False)  # 0-100
    
    # Template and action data
    workflow_template_id = Column(String, nullable=True)  # If suggesting workflow
    automation_template_id = Column(String, nullable=True)  # If suggesting automation
    pre_filled_data = Column(JSON, nullable=True)  # Pre-filled inputs for template
    
    # Context and signals
    triggering_signals = Column(JSON, nullable=False)  # What signals triggered this
    context = Column(JSON, nullable=True)  # Additional context
    
    # Actions
    primary_action = Column(String(50), nullable=False)  # 'review_draft', 'configure', 'enable'
    secondary_action = Column(String(50), nullable=True)  # Optional secondary action
    
    # Expiration
    expires_at = Column(DateTime, nullable=True)  # Time-sensitive recommendations expire
    
    # Learning loop
    accepted_at = Column(DateTime, nullable=True)
    dismissed_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    tenant_feedback = Column(JSON, nullable=True)  # Optional feedback from tenant
    
    # Performance tracking
    estimated_impact = Column(JSON, nullable=True)  # Estimated outcomes
    actual_impact = Column(JSON, nullable=True)  # Actual outcomes (measured later)
    
    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "created_at": self.created_at.isoformat() + 'Z' if self.created_at else None,
            "updated_at": self.updated_at.isoformat() + 'Z' if self.updated_at else None,
            "recommendation_type": self.recommendation_type.value if self.recommendation_type else None,
            "status": self.status.value if self.status else None,
            "title": self.title,
            "description": self.description,
            "impact_level": self.impact_level,
            "confidence_score": self.confidence_score,
            "workflow_template_id": self.workflow_template_id,
            "automation_template_id": self.automation_template_id,
            "pre_filled_data": self.pre_filled_data,
            "triggering_signals": self.triggering_signals,
            "context": self.context,
            "primary_action": self.primary_action,
            "secondary_action": self.secondary_action,
            "expires_at": self.expires_at.isoformat() + 'Z' if self.expires_at else None,
            "accepted_at": self.accepted_at.isoformat() + 'Z' if self.accepted_at else None,
            "dismissed_at": self.dismissed_at.isoformat() + 'Z' if self.dismissed_at else None,
            "completed_at": self.completed_at.isoformat() + 'Z' if self.completed_at else None,
            "tenant_feedback": self.tenant_feedback,
            "estimated_impact": self.estimated_impact,
            "actual_impact": self.actual_impact
        }


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    'Base',
    'UserRole',
    'WorkflowStatus',
    'NotificationType',
    'TriggerType',
    'ActionType',
    'RiskLevel',
    'EventResult',
    'user_councils',
    'Tenant',
    'User',
    'AuditLog',
    'Council',
    'CouncilMember',
    'Agent',
    'AgentReputation',
    'AgentTraining',
    'WorkflowType',
    'Workflow',
    'WorkflowArtifact',
    'WorkflowMetric',
    'WorkflowVote',
    'Store',
    'PortalNotification',
    'AutomationRule',
    'AutomationExecution',
    'AutomationEvent',
    'AutomationDebugLog',
    'AutomationTemplate',
    'AutomationEvent',
    'AdvisorRecommendation',
    'RecommendationType',
    'RecommendationStatus',
    # Cultural Memory Architecture (Phase 40 Step 3)
    'CreativeProject',
    'CreativeDecision',
    'IdentityCodex',
    'StylePattern',
    'CulturalMemory',
    'BrandEvolution',
    # Evolution Engine (Phase 40 Step 4)
    'EvolutionProposal',
    'AgentGenerationProposal',
    'TechniqueEvolution',
    'EvolutionBoundary',
    'EvolutionCycle'
]


# ============================================================================
# EVOLUTION ENGINE MODELS (PHASE 40 - STEP 4)
# ============================================================================

class EvolutionBoundary(Base):
    """LAYER 4: Defines what the Dominion can and cannot change"""
    __tablename__ = 'evolution_boundaries'
    
    id = Column(String, primary_key=True)
    boundary_type = Column(String, nullable=False)  # sacred, guarded, flexible
    category = Column(String, nullable=False)  # identity, tone, content, brand, governance, etc.
    principle = Column(String, nullable=False)
    description = Column(Text)
    
    # Protection details
    what_is_protected = Column(String)
    flexibility_level = Column(String)  # none, limited, moderate, high
    approval_required = Column(String)  # sovereign_architect, high_council, operations_council, etc.
    rationale = Column(Text)
    examples = Column(JSON)
    
    # Lifecycle
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(String, default="active")


class EvolutionProposal(Base):
    """LAYER 1: Self-improvement proposals from agents"""
    __tablename__ = 'evolution_proposals'
    
    id = Column(String, primary_key=True)
    proposal_type = Column(String, nullable=False)  # workflow_optimization, creative_technique, agent_expansion, etc.
    title = Column(String, nullable=False)
    description = Column(Text)
    
    # Proposal details
    proposed_by_agent = Column(String, nullable=False)
    current_state = Column(Text)
    proposed_state = Column(Text)
    expected_benefits = Column(JSON)
    alignment_with_identity = Column(Text)
    risks = Column(JSON)
    estimated_effort = Column(String)
    
    # Review and approval
    status = Column(String, default="pending_council_review")  # pending, approved, rejected, implemented
    reviewed_by_council = Column(String, nullable=True)
    council_vote_summary = Column(JSON, nullable=True)
    approval_date = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # Implementation
    implemented_by_agent = Column(String, nullable=True)
    implementation_date = Column(DateTime, nullable=True)
    actual_results = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AgentGenerationProposal(Base):
    """LAYER 2: Proposals for new agent creation"""
    __tablename__ = 'agent_generation_proposals'
    
    id = Column(String, primary_key=True)
    proposed_agent_name = Column(String, nullable=False)
    proposed_agent_role = Column(String, nullable=False)
    proposed_domain = Column(String)  # faith_content, distribution, analytics, etc.
    proposed_capabilities = Column(JSON)  # primary, secondary, tertiary skills
    
    # Justification
    gap_identified = Column(Text, nullable=False)
    proposed_by_agent = Column(String, nullable=False)
    justification = Column(Text)
    expected_impact = Column(String)
    
    # Council assignment
    council_assignment = Column(String)  # which council would this agent join
    
    # Training and activation
    training_requirements = Column(JSON)
    cultural_memory_references = Column(JSON, nullable=True)
    
    # Review and approval
    status = Column(String, default="pending_high_council_review")
    high_council_vote = Column(JSON, nullable=True)
    sovereign_acknowledgment = Column(String, default="pending")  # pending, acknowledged, rejected
    approval_date = Column(DateTime, nullable=True)
    
    # Post-creation
    agent_id_created = Column(String, nullable=True)
    activation_date = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TechniqueEvolution(Base):
    """LAYER 3: Creative technique evolution tracking"""
    __tablename__ = 'technique_evolutions'
    
    id = Column(String, primary_key=True)
    technique_category = Column(String, nullable=False)  # visual, narrative, audio, structural
    technique_name = Column(String, nullable=False)
    
    # Evolution details
    old_approach = Column(Text)
    new_approach = Column(Text, nullable=False)
    reason_for_evolution = Column(Text)
    
    # Testing and validation
    tested_where = Column(String)  # where was this tested
    test_results = Column(JSON)  # metrics from testing
    identity_alignment_check = Column(Text)
    
    # Impact assessment
    affected_principles = Column(JSON)  # identity_codex IDs
    affected_patterns = Column(JSON)  # style_pattern IDs
    
    # Approval
    status = Column(String, default="testing")  # testing, approved, rejected, retired
    approved_by_council = Column(String, nullable=True)
    approval_date = Column(DateTime, nullable=True)
    
    # Implementation
    implementation_date = Column(DateTime, nullable=True)
    cultural_memory_update = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EvolutionCycle(Base):
    """LAYER 1: Tracks the self-improvement loop iterations"""
    __tablename__ = 'evolution_cycles'
    
    id = Column(String, primary_key=True)
    cycle_number = Column(Integer, nullable=False)
    
    # The six-step cycle
    observation = Column(Text, nullable=False)  # Step 1: What was observed
    analysis = Column(Text)  # Step 2: Analysis of the observation
    proposal_id = Column(String, nullable=True)  # Step 3: Link to proposal created
    council_review_status = Column(String, default="pending")  # Step 4: Review status
    implementation_status = Column(String, default="not_started")  # Step 5: Implementation
    memory_updated = Column(Boolean, default=False)  # Step 6: Cultural memory updated
    
    # Cycle metadata
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    cycle_duration = Column(String, nullable=True)  # human-readable duration
    
    # Results
    outcome = Column(String, nullable=True)  # success, failure, abandoned
    lessons_learned = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================================================
# CULTURAL MEMORY ARCHITECTURE MODELS (PHASE 40 - STEP 3)
# ============================================================================

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


# ============================================================================
# PHASE 50: THE DOMINION ECONOMY
# ============================================================================

class AgentReputationProfile(Base):
    """LAYER 2: Agent reputation tracking - Merit system"""
    __tablename__ = 'agent_reputation_profiles'
    
    id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey('agents.id'), unique=True)
    
    # The 5 Value Types (0-100 scale)
    creative_quality_value = Column(Float, default=50.0)  # CQV
    continuity_value = Column(Float, default=50.0)  # CV
    efficiency_value = Column(Float, default=50.0)  # EV
    innovation_value = Column(Float, default=50.0)  # IV
    collaboration_value = Column(Float, default=50.0)  # CoV
    
    # Overall reputation score (weighted average)
    overall_reputation = Column(Float, default=50.0)
    
    # Influence metrics
    voting_weight = Column(Float, default=1.0)  # 0.5-2.0, affects council votes
    proposal_authority = Column(Float, default=1.0)  # 0.5-2.0, affects proposal credibility
    
    # Track record
    successful_proposals = Column(Integer, default=0)
    failed_proposals = Column(Integer, default=0)
    continuity_violations = Column(Integer, default=0)
    creative_breakthroughs = Column(Integer, default=0)
    
    # Collaboration stats
    collaborations_led = Column(Integer, default=0)
    collaborations_participated = Column(Integer, default=0)
    debates_won = Column(Integer, default=0)  # When their position was adopted
    debates_lost = Column(Integer, default=0)
    
    # Strengths and weaknesses (auto-detected)
    strengths = Column(JSON, default=list)  # ["identity_alignment", "efficient_execution"]
    weaknesses = Column(JSON, default=list)  # ["rushed_work", "ignores_feedback"]
    
    # Historical performance
    last_30_days_score = Column(Float, default=50.0)
    all_time_high = Column(Float, default=50.0)
    all_time_low = Column(Float, default=50.0)
    
    # Status
    reputation_tier = Column(String, default="established")  # emerging, established, respected, renowned, legendary
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ValueTransaction(Base):
    """LAYER 4: Value distribution - How value flows through the economy"""
    __tablename__ = 'value_transactions'
    
    id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey('agents.id'))
    
    # Transaction details
    transaction_type = Column(String)  # project_contribution, council_vote, evolution_proposal, cultural_alignment, collaboration
    value_type = Column(String)  # CQV, CV, EV, IV, CoV
    amount = Column(Float)  # Positive = gain, negative = loss
    
    # Context
    source_id = Column(String, nullable=True)  # ID of project, proposal, collaboration, etc.
    source_type = Column(String, nullable=True)  # project, proposal, collaboration, evolution
    reason = Column(Text)  # Why this value was gained/lost
    
    # Impact
    previous_value = Column(Float)
    new_value = Column(Float)
    reputation_impact = Column(Float)  # How much overall reputation changed
    
    timestamp = Column(DateTime, default=datetime.utcnow)


class IncentiveEvent(Base):
    """LAYER 3: Incentive tracking - What drives agent improvement"""
    __tablename__ = 'incentive_events'
    
    id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey('agents.id'))
    
    # Event details
    event_type = Column(String)  # reward, penalty, milestone, recognition, warning
    category = Column(String)  # quality, continuity, efficiency, innovation, collaboration
    
    # What happened
    trigger = Column(Text)  # What caused this incentive event
    description = Column(Text)
    severity = Column(String)  # minor, moderate, significant, major
    
    # Impact
    value_changes = Column(JSON)  # {"CQV": +5, "CV": +2}
    reputation_change = Column(Float)
    new_reputation_tier = Column(String, nullable=True)  # If tier changed
    
    # Agent response (optional)
    agent_acknowledged = Column(Boolean, default=False)
    improvement_observed = Column(Boolean, default=None)
    
    timestamp = Column(DateTime, default=datetime.utcnow)


class ReputationHistory(Base):
    """Track reputation changes over time - Historical record"""
    __tablename__ = 'reputation_history'
    
    id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey('agents.id'))
    
    # Snapshot of reputation at this point in time
    snapshot_date = Column(DateTime, default=datetime.utcnow)
    
    creative_quality_value = Column(Float)
    continuity_value = Column(Float)
    efficiency_value = Column(Float)
    innovation_value = Column(Float)
    collaboration_value = Column(Float)
    overall_reputation = Column(Float)
    
    # What caused the change
    trigger_event_id = Column(String, nullable=True)  # IncentiveEvent or ValueTransaction ID
    trigger_type = Column(String, nullable=True)  # incentive_event, value_transaction
    
    # Context
    note = Column(Text, nullable=True)


class EconomyMetrics(Base):
    """System-wide economy health metrics"""
    __tablename__ = 'economy_metrics'
    
    id = Column(String, primary_key=True)
    metric_date = Column(DateTime, default=datetime.utcnow)
    
    # Overall economy health
    total_value_in_circulation = Column(Float, default=0.0)
    average_agent_reputation = Column(Float, default=50.0)
    reputation_inequality = Column(Float, default=0.0)  # Gini coefficient (0-1)
    
    # Value type distribution
    total_cqv = Column(Float, default=0.0)
    total_cv = Column(Float, default=0.0)
    total_ev = Column(Float, default=0.0)
    total_iv = Column(Float, default=0.0)
    total_cov = Column(Float, default=0.0)
    
    # Transaction activity
    transactions_today = Column(Integer, default=0)
    positive_transactions = Column(Integer, default=0)
    negative_transactions = Column(Integer, default=0)
    net_value_flow = Column(Float, default=0.0)
    
    # Incentive activity
    rewards_issued_today = Column(Integer, default=0)
    penalties_issued_today = Column(Integer, default=0)
    milestones_reached_today = Column(Integer, default=0)
    
    # Reputation tiers
    emerging_agents = Column(Integer, default=0)
    established_agents = Column(Integer, default=0)
    respected_agents = Column(Integer, default=0)
    renowned_agents = Column(Integer, default=0)
    legendary_agents = Column(Integer, default=0)
    
    # Performance trends
    quality_trend = Column(String, default="stable")  # declining, stable, improving
    innovation_trend = Column(String, default="stable")
    collaboration_trend = Column(String, default="stable")
    
    # Economy health score (0-100)
    economy_health_score = Column(Float, default=50.0)


# ============================================================================
# PHASE 40 - STEP 5: CIVILIZATION INTEGRATION LAYER
# ============================================================================

class AgentCollaboration(Base):
    """Multi-agent collaborative projects - The social layer"""
    __tablename__ = 'agent_collaborations'
    
    id = Column(String, primary_key=True)
    project_name = Column(String, nullable=False)
    project_type = Column(String)  # creative_project, proposal, research, optimization
    
    # Participants
    lead_agent_id = Column(String, ForeignKey('agents.id'))
    collaborating_agents = Column(JSON)  # List of agent IDs
    
    # Collaboration dynamics
    contributions = Column(JSON)  # Who contributed what
    debates = Column(JSON)  # Recorded discussions/disagreements
    consensus_reached = Column(Boolean, default=False)
    
    # Output
    deliverable = Column(JSON)  # The result of collaboration
    impact = Column(JSON)  # Measured outcomes
    
    # Status
    status = Column(String, default="active")  # active, completed, paused, cancelled
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Cultural memory integration
    cultural_memory_refs = Column(JSON)  # Memories referenced during work
    created_memory_id = Column(String, nullable=True)  # New memory created from this work


class ProposalWorkflow(Base):
    """End-to-end proposal routing - Council as central nervous system"""
    __tablename__ = 'proposal_workflows'
    
    id = Column(String, primary_key=True)
    proposal_type = Column(String)  # evolution, agent_generation, technique, policy
    
    # Source
    originating_agent_id = Column(String, ForeignKey('agents.id'))
    source_collaboration_id = Column(String, nullable=True)  # If from collaboration
    
    # Proposal content
    title = Column(String, nullable=False)
    description = Column(Text)
    rationale = Column(Text)
    expected_impact = Column(JSON)
    
    # Routing
    assigned_council_id = Column(String, ForeignKey('councils.id'))
    routing_reason = Column(String)  # Why this council?
    
    # Council review
    review_status = Column(String, default="pending")  # pending, under_review, approved, rejected, needs_revision
    council_votes = Column(JSON)  # Record of council member votes
    review_notes = Column(Text, nullable=True)
    
    # Identity validation
    identity_check_passed = Column(Boolean, default=None)
    identity_concerns = Column(JSON, nullable=True)
    
    # Execution
    approved_at = Column(DateTime, nullable=True)
    implemented_at = Column(DateTime, nullable=True)
    implementation_notes = Column(Text, nullable=True)
    
    # Feedback loop
    logged_to_cultural_memory = Column(Boolean, default=False)
    cultural_memory_id = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class KnowledgeAccess(Base):
    """Track how agents access cultural memory - Shared brain usage"""
    __tablename__ = 'knowledge_access'
    
    id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey('agents.id'))
    
    # What was accessed
    memory_type = Column(String)  # identity, history, pattern, lesson, wisdom
    memory_id = Column(String)  # ID of the accessed memory
    memory_title = Column(String)
    
    # Context
    access_reason = Column(String)  # Why did agent need this?
    related_project_id = Column(String, nullable=True)
    related_collaboration_id = Column(String, nullable=True)
    
    # Application
    how_used = Column(Text, nullable=True)  # How agent applied this knowledge
    contributed_to_outcome = Column(Boolean, default=None)
    
    accessed_at = Column(DateTime, default=datetime.utcnow)


class IntegrationEvent(Base):
    """System-wide events - Tracks civilization activity"""
    __tablename__ = 'integration_events'
    
    id = Column(String, primary_key=True)
    event_type = Column(String)  # collaboration_started, proposal_submitted, council_decision, evolution_approved, knowledge_applied
    
    # Event details
    title = Column(String, nullable=False)
    description = Column(Text)
    
    # Participants
    involved_agents = Column(JSON)  # Agent IDs
    involved_councils = Column(JSON, nullable=True)  # Council IDs
    
    # Cross-system references
    collaboration_id = Column(String, nullable=True)
    proposal_id = Column(String, nullable=True)
    evolution_proposal_id = Column(String, nullable=True)
    cultural_memory_id = Column(String, nullable=True)
    
    # Impact
    impact_areas = Column(JSON)  # Which systems were affected
    significance = Column(String, default="normal")  # low, normal, high, critical
    
    timestamp = Column(DateTime, default=datetime.utcnow)


class CivilizationMetrics(Base):
    """Health metrics of the ecosystem - System vitals"""
    __tablename__ = 'civilization_metrics'
    
    id = Column(String, primary_key=True)
    metric_date = Column(DateTime, default=datetime.utcnow)
    
    # Agent activity
    active_agents = Column(Integer, default=0)
    collaborations_active = Column(Integer, default=0)
    proposals_submitted = Column(Integer, default=0)
    
    # Council activity
    proposals_reviewed = Column(Integer, default=0)
    proposals_approved = Column(Integer, default=0)
    proposals_rejected = Column(Integer, default=0)
    average_review_time_hours = Column(Float, default=0.0)
    
    # Cultural memory usage
    memories_referenced = Column(Integer, default=0)
    new_memories_created = Column(Integer, default=0)
    most_referenced_memory_id = Column(String, nullable=True)
    
    # Evolution activity
    evolution_proposals_submitted = Column(Integer, default=0)
    evolutions_approved = Column(Integer, default=0)
    new_agents_created = Column(Integer, default=0)
    techniques_evolved = Column(Integer, default=0)
    
    # Identity integrity
    identity_checks_performed = Column(Integer, default=0)
    identity_concerns_raised = Column(Integer, default=0)
    boundary_violations_prevented = Column(Integer, default=0)
    
    # Integration health
    cross_system_events = Column(Integer, default=0)
    system_coherence_score = Column(Float, default=1.0)  # 0-1, how well systems work together
    
    # Performance
    average_collaboration_duration_hours = Column(Float, default=0.0)
    average_proposal_to_implementation_hours = Column(Float, default=0.0)

