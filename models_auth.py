"""
🔐 Authentication Models - Users & Roles
=========================================
Database models for user authentication and role-based access control
"""

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Table, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()


class UserRole(enum.Enum):
    """User role types"""
    ADMIN = "admin"
    COUNCIL_OPERATOR = "council_operator"
    VIEWER = "viewer"


# Association table for user-council relationship (council operators)
user_councils = Table(
    'user_councils',
    Base.metadata,
    Column('user_id', String, ForeignKey('users.id'), primary_key=True),
    Column('council_id', String, ForeignKey('councils.id'), primary_key=True)
)


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
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.VIEWER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    councils = relationship(
        "Council",
        secondary=user_councils,
        back_populates="operators",
        doc="Councils this user can operate (vote on workflows)"
    )
    
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
    details = Column(String, nullable=True)  # JSON string for additional context
    ip_address = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User")
    
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


# Update Council model to include operators relationship
# Add this to your existing models.py:
"""
from models_auth import user_councils

class Council(Base):
    # ... existing fields ...
    
    operators = relationship(
        "User",
        secondary=user_councils,
        back_populates="councils",
        doc="Users who can vote on workflows in this council"
    )
"""
