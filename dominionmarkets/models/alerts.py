"""
Alert System Database Models
=============================
Models for the Alerts Center personal signal hub
"""

from sqlalchemy import Column, String, Integer, Decimal, Boolean, Enum as SQLEnum, JSON, ForeignKey, DateTime, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from models import Base  # Import from root models.py


# Enums
class AlertType(enum.Enum):
    """Alert type categories"""
    PRICE = 'price'
    NEWS = 'news'
    EARNINGS = 'earnings'
    DIVIDEND = 'dividend'
    PORTFOLIO = 'portfolio'
    VOLUME = 'volume'
    CULTURAL_ALPHA = 'cultural_alpha'


class AlertStatus(enum.Enum):
    """Alert lifecycle states"""
    ACTIVE = 'active'                # Monitoring for condition
    TRIGGERED = 'triggered'          # Condition met, notification sent
    PAUSED = 'paused'               # User paused, not monitoring
    EXPIRED = 'expired'             # Time-based alert expired
    DELETED = 'deleted'             # User deleted
    ERROR = 'error'                 # System error, needs retry


class ConditionType(enum.Enum):
    """Alert condition types"""
    # Price conditions
    ABOVE = 'above'
    BELOW = 'below'
    PERCENT_UP = 'percent_up'
    PERCENT_DOWN = 'percent_down'
    
    # News conditions
    ANY_NEWS = 'any_news'
    CATEGORY_NEWS = 'category_news'
    HIGH_VERIFICATION = 'high_verification'
    
    # Earnings conditions
    EARNINGS_UPCOMING_7D = 'earnings_upcoming_7d'
    EARNINGS_UPCOMING_1D = 'earnings_upcoming_1d'
    EARNINGS_RELEASED = 'earnings_released'
    
    # Dividend conditions
    DIVIDEND_ANNOUNCED = 'dividend_announced'
    EX_DATE_APPROACHING = 'ex_date_approaching'
    PAYMENT_DATE_APPROACHING = 'payment_date_approaching'
    DIVIDEND_CHANGED = 'dividend_changed'
    
    # Portfolio conditions
    PORTFOLIO_GAIN = 'portfolio_gain'
    PORTFOLIO_LOSS = 'portfolio_loss'
    HOLDING_GAIN = 'holding_gain'
    HOLDING_LOSS = 'holding_loss'
    SECTOR_ALLOCATION = 'sector_allocation'
    DIVERSIFICATION_LOW = 'diversification_low'
    
    # Volume conditions
    VOLUME_2X = 'volume_2x'
    VOLUME_5X = 'volume_5x'
    VOLUME_SPIKE = 'volume_spike'


class IdentityType(enum.Enum):
    """User identity personas"""
    DIASPORA = 'diaspora'
    YOUTH = 'youth'
    CREATOR = 'creator'
    LEGACY = 'legacy'
    ALL = 'all'


class DigestFrequency(enum.Enum):
    """Alert digest frequency"""
    NEVER = 'never'
    DAILY = 'daily'
    WEEKLY = 'weekly'


# Models
class Alert(Base):
    """
    Alert model - User-created alerts for market events
    """
    __tablename__ = 'alerts'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)  # FK to users table
    
    # Alert configuration
    alert_type = Column(SQLEnum(AlertType), nullable=False, index=True)
    symbol = Column(String(10), nullable=True, index=True)  # Stock ticker (null for portfolio/cultural)
    condition_type = Column(SQLEnum(ConditionType), nullable=False)
    target_value = Column(Decimal(12, 2), nullable=True)  # Price target or percent threshold
    
    # News-specific settings
    min_verification_score = Column(Integer, default=75)  # For news alerts
    article_threshold = Column(Integer, default=1)  # Min articles to trigger news alert
    
    # Portfolio-specific settings
    portfolio_id = Column(UUID(as_uuid=True), nullable=True)  # FK to portfolio table
    
    # Alert metadata
    alert_name = Column(String(100), nullable=True)  # Optional custom name
    status = Column(SQLEnum(AlertStatus), default=AlertStatus.ACTIVE, nullable=False, index=True)
    trigger_count = Column(Integer, default=0)
    last_triggered_at = Column(DateTime, nullable=True)
    
    # Notification preferences
    notification_push = Column(Boolean, default=True)
    notification_email = Column(Boolean, default=False)
    notification_sms = Column(Boolean, default=False)  # Pro only
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    triggers = relationship('AlertTrigger', back_populates='alert', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Alert {self.id} {self.alert_type.value} {self.symbol or 'N/A'} {self.status.value}>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'alert_type': self.alert_type.value,
            'symbol': self.symbol,
            'condition_type': self.condition_type.value,
            'target_value': float(self.target_value) if self.target_value else None,
            'min_verification_score': self.min_verification_score,
            'alert_name': self.alert_name,
            'status': self.status.value,
            'trigger_count': self.trigger_count,
            'last_triggered_at': self.last_triggered_at.isoformat() if self.last_triggered_at else None,
            'notification_push': self.notification_push,
            'notification_email': self.notification_email,
            'notification_sms': self.notification_sms,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def get_tier_limits(self, user_tier: str) -> dict:
        """Get alert limits for user tier"""
        limits = {
            'free': {
                'price': 5,
                'news': 3,
                'earnings': 10,
                'dividend': 5,
                'portfolio': 3,
                'volume': 0,
                'cultural_alpha': 2
            },
            'premium': {
                'price': 50,
                'news': 20,
                'earnings': 100,
                'dividend': 30,
                'portfolio': 15,
                'volume': 10,
                'cultural_alpha': 10
            },
            'pro': {
                'price': 999999,
                'news': 999999,
                'earnings': 999999,
                'dividend': 999999,
                'portfolio': 999999,
                'volume': 50,
                'cultural_alpha': 999999
            }
        }
        return limits.get(user_tier, limits['free'])


class AlertTrigger(Base):
    """
    Alert Trigger model - Record of when alerts triggered
    """
    __tablename__ = 'alert_triggers'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_id = Column(UUID(as_uuid=True), ForeignKey('alerts.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Trigger details
    triggered_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    trigger_value = Column(Decimal(12, 2), nullable=True)  # Actual price/value when triggered
    trigger_data = Column(JSON, nullable=True)  # Additional context (articles, earnings, etc.)
    
    # Notification tracking
    notification_sent = Column(Boolean, default=False)
    notification_sent_at = Column(DateTime, nullable=True)
    notification_method = Column(String(20), nullable=True)  # 'push', 'email', 'sms'
    
    # Relationships
    alert = relationship('Alert', back_populates='triggers')
    
    def __repr__(self):
        return f"<AlertTrigger {self.id} alert={self.alert_id} at {self.triggered_at}>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': str(self.id),
            'alert_id': str(self.alert_id),
            'triggered_at': self.triggered_at.isoformat(),
            'trigger_value': float(self.trigger_value) if self.trigger_value else None,
            'trigger_data': self.trigger_data,
            'notification_sent': self.notification_sent,
            'notification_sent_at': self.notification_sent_at.isoformat() if self.notification_sent_at else None,
            'notification_method': self.notification_method
        }


class UserAlertPreference(Base):
    """
    User Alert Preferences - Global notification settings
    """
    __tablename__ = 'user_alert_preferences'
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, index=True)  # FK to users table
    
    # Identity configuration
    identity_type = Column(SQLEnum(IdentityType), default=IdentityType.ALL)
    
    # Default notification settings (applied to new alerts)
    default_notification_push = Column(Boolean, default=True)
    default_notification_email = Column(Boolean, default=False)
    default_notification_sms = Column(Boolean, default=False)
    
    # Quiet hours (no notifications during this window)
    quiet_hours_start = Column(Time, nullable=True)  # e.g., 22:00:00
    quiet_hours_end = Column(Time, nullable=True)    # e.g., 07:00:00
    timezone = Column(String(50), default='America/New_York')
    
    # Digest settings
    digest_frequency = Column(SQLEnum(DigestFrequency), default=DigestFrequency.NEVER)
    last_digest_sent_at = Column(DateTime, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserAlertPreference user={self.user_id} identity={self.identity_type.value}>"
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'user_id': str(self.user_id),
            'identity_type': self.identity_type.value,
            'default_notification_push': self.default_notification_push,
            'default_notification_email': self.default_notification_email,
            'default_notification_sms': self.default_notification_sms,
            'quiet_hours_start': self.quiet_hours_start.isoformat() if self.quiet_hours_start else None,
            'quiet_hours_end': self.quiet_hours_end.isoformat() if self.quiet_hours_end else None,
            'timezone': self.timezone,
            'digest_frequency': self.digest_frequency.value,
            'last_digest_sent_at': self.last_digest_sent_at.isoformat() if self.last_digest_sent_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# Helper functions
def get_active_alerts_by_type(session, user_id: uuid.UUID, alert_type: AlertType):
    """Get all active alerts of a specific type for a user"""
    return session.query(Alert).filter(
        Alert.user_id == user_id,
        Alert.alert_type == alert_type,
        Alert.status == AlertStatus.ACTIVE
    ).all()


def get_user_alert_count_by_type(session, user_id: uuid.UUID) -> dict:
    """Get count of active alerts by type for a user"""
    counts = {}
    for alert_type in AlertType:
        count = session.query(Alert).filter(
            Alert.user_id == user_id,
            Alert.alert_type == alert_type,
            Alert.status.in_([AlertStatus.ACTIVE, AlertStatus.TRIGGERED])
        ).count()
        counts[alert_type.value] = count
    return counts


def check_tier_limit(session, user_id: uuid.UUID, alert_type: AlertType, user_tier: str) -> tuple[bool, int, int]:
    """
    Check if user can create more alerts of this type
    
    Returns: (can_create: bool, current_count: int, limit: int)
    """
    current_count = session.query(Alert).filter(
        Alert.user_id == user_id,
        Alert.alert_type == alert_type,
        Alert.status.in_([AlertStatus.ACTIVE, AlertStatus.TRIGGERED, AlertStatus.PAUSED])
    ).count()
    
    alert_obj = Alert()
    limits = alert_obj.get_tier_limits(user_tier)
    limit = limits.get(alert_type.value, 0)
    
    can_create = current_count < limit
    return can_create, current_count, limit


def get_recent_triggers(session, user_id: uuid.UUID, hours: int = 24):
    """Get recent alert triggers for a user"""
    from datetime import timedelta
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    
    return session.query(AlertTrigger).join(Alert).filter(
        Alert.user_id == user_id,
        AlertTrigger.triggered_at >= cutoff
    ).order_by(AlertTrigger.triggered_at.desc()).all()


def get_user_alert_summary(session, user_id: uuid.UUID, user_tier: str) -> dict:
    """Get comprehensive alert summary for dashboard"""
    active_count = session.query(Alert).filter(
        Alert.user_id == user_id,
        Alert.status == AlertStatus.ACTIVE
    ).count()
    
    recent_triggers = get_recent_triggers(session, user_id, hours=24)
    trigger_count = len(recent_triggers)
    
    counts_by_type = get_user_alert_count_by_type(session, user_id)
    
    alert_obj = Alert()
    limits = alert_obj.get_tier_limits(user_tier)
    
    return {
        'active_count': active_count,
        'triggered_today': trigger_count,
        'counts_by_type': counts_by_type,
        'limits_by_type': limits,
        'user_tier': user_tier
    }
