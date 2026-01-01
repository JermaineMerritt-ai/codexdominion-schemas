"""
DominionMarkets News Verification Models
=========================================
Database schema for multi-source news verification system.

Tables:
- NewsArticle: Core article metadata
- NewsSource: Trusted news sources catalog
- VerificationCheck: Cross-source verification records
- UserNewsPreference: Personalized feed settings
- UserBookmark: Saved articles

Last Updated: December 24, 2025
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from models import Base  # Import from root models.py


# Many-to-many association table for articles and sources
article_sources = Table(
    'article_sources',
    Base.metadata,
    Column('article_id', String(36), ForeignKey('news_articles.id'), primary_key=True),
    Column('source_id', String(36), ForeignKey('news_sources.id'), primary_key=True),
    Column('reported_at', DateTime, default=datetime.utcnow),
    Column('content_url', String(500)),  # URL to this source's version
)


class VerificationStatus(enum.Enum):
    """Verification pipeline status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    FAILED = "failed"
    CONFLICT = "conflict"


class NewsTier(enum.Enum):
    """Source trust tiers"""
    AAA = "aaa"  # Highest trust (Bloomberg, Reuters)
    AA = "aa"    # High trust (WSJ, FT)
    A = "a"      # Good trust (CNBC, MarketWatch)
    B = "b"      # Moderate trust (Yahoo Finance)
    C = "c"      # Lower trust (blog sources)


class BiasRating(enum.Enum):
    """Political/editorial bias"""
    LEFT = "left"
    CENTER_LEFT = "center-left"
    CENTER = "center"
    CENTER_RIGHT = "center-right"
    RIGHT = "right"
    VARIES = "varies"


class NewsArticle(Base):
    """
    Core news article with verification metadata.
    Represents a single news story verified across multiple sources.
    """
    __tablename__ = 'news_articles'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Content
    title = Column(String(500), nullable=False, index=True)
    summary = Column(Text, nullable=True)  # AI-generated or first paragraph
    content = Column(Text, nullable=True)  # Full article text (if available)
    url_primary = Column(String(500), nullable=True)  # Primary source URL
    
    # Metadata
    published_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Author/Attribution
    author = Column(String(200), nullable=True)
    primary_source_id = Column(String(36), ForeignKey('news_sources.id'), nullable=True)
    
    # Verification
    verification_score = Column(Integer, nullable=True, index=True)  # 0-100
    verification_status = Column(Enum(VerificationStatus), default=VerificationStatus.PENDING, index=True)
    source_count = Column(Integer, default=0)  # Number of sources reporting
    agreement_rate = Column(Float, nullable=True)  # % of sources agreeing (0-100)
    has_conflicts = Column(Boolean, default=False, index=True)
    
    # Categorization
    category = Column(String(100), nullable=True, index=True)  # 'earnings', 'market_news', 'policy', etc.
    ticker_symbols = Column(JSON, nullable=True)  # List of related stock symbols
    tags = Column(JSON, nullable=True)  # General tags
    
    # Identity-Aware Tagging
    relevant_for_diaspora = Column(Boolean, default=False, index=True)
    relevant_for_youth = Column(Boolean, default=False, index=True)
    relevant_for_creator = Column(Boolean, default=False, index=True)
    relevant_for_legacy = Column(Boolean, default=False, index=True)
    
    # Premium Features (cached)
    sentiment_score = Column(Float, nullable=True)  # -1 to +1 (negative to positive)
    sentiment_label = Column(String(20), nullable=True)  # 'negative', 'neutral', 'positive'
    bias_detected = Column(String(50), nullable=True)  # BiasRating enum value
    sensationalism_score = Column(Integer, nullable=True)  # 0-100 (low to high)
    
    # Engagement
    view_count = Column(Integer, default=0)
    bookmark_count = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_featured = Column(Boolean, default=False, index=True)
    
    # Relationships
    primary_source = relationship('NewsSource', foreign_keys=[primary_source_id], back_populates='primary_articles')
    sources = relationship('NewsSource', secondary=article_sources, back_populates='articles')
    verification_checks = relationship('VerificationCheck', back_populates='article', cascade='all, delete-orphan')
    bookmarks = relationship('UserBookmark', back_populates='article', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'url_primary': self.url_primary,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'author': self.author,
            'verification_score': self.verification_score,
            'verification_status': self.verification_status.value if self.verification_status else None,
            'source_count': self.source_count,
            'agreement_rate': self.agreement_rate,
            'has_conflicts': self.has_conflicts,
            'category': self.category,
            'ticker_symbols': self.ticker_symbols or [],
            'tags': self.tags or [],
            'sentiment_label': self.sentiment_label,
            'is_featured': self.is_featured,
            'view_count': self.view_count,
            'bookmark_count': self.bookmark_count
        }


class NewsSource(Base):
    """
    Trusted news sources with historical accuracy tracking.
    """
    __tablename__ = 'news_sources'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Identity
    name = Column(String(200), nullable=False, unique=True, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)  # 'bloomberg', 'reuters'
    url_base = Column(String(200), nullable=True)
    logo_url = Column(String(500), nullable=True)
    
    # Trust Metrics
    trust_score = Column(Integer, nullable=False, default=50)  # 0-100
    tier = Column(Enum(NewsTier), nullable=False, default=NewsTier.B)
    bias_rating = Column(Enum(BiasRating), nullable=False, default=BiasRating.CENTER)
    
    # Historical Performance
    articles_verified = Column(Integer, default=0)  # Total articles cross-checked
    accuracy_rate = Column(Float, nullable=True)  # % of articles verified as accurate
    conflict_rate = Column(Float, nullable=True)  # % of articles with conflicts
    avg_verification_score = Column(Float, nullable=True)  # Average score of their articles
    
    # Feed Configuration
    rss_feed_url = Column(String(500), nullable=True)
    api_endpoint = Column(String(500), nullable=True)
    api_key_required = Column(Boolean, default=False)
    
    # Metadata
    description = Column(Text, nullable=True)
    founded_year = Column(Integer, nullable=True)
    coverage_focus = Column(JSON, nullable=True)  # ['stocks', 'bonds', 'commodities', 'forex']
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_premium_only = Column(Boolean, default=False)  # Only show to premium users
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_fetched_at = Column(DateTime, nullable=True)
    
    # Relationships
    primary_articles = relationship('NewsArticle', foreign_keys='NewsArticle.primary_source_id', back_populates='primary_source')
    articles = relationship('NewsArticle', secondary=article_sources, back_populates='sources')
    user_preferences = relationship('UserNewsPreference', back_populates='source')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'logo_url': self.logo_url,
            'trust_score': self.trust_score,
            'tier': self.tier.value if self.tier else None,
            'bias_rating': self.bias_rating.value if self.bias_rating else None,
            'articles_verified': self.articles_verified,
            'accuracy_rate': self.accuracy_rate,
            'conflict_rate': self.conflict_rate,
            'description': self.description,
            'is_active': self.is_active
        }


class VerificationCheck(Base):
    """
    Individual verification checks performed on articles.
    Tracks the verification process and conflict detection.
    """
    __tablename__ = 'verification_checks'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    article_id = Column(String(36), ForeignKey('news_articles.id'), nullable=False, index=True)
    
    # Check Metadata
    check_type = Column(String(50), nullable=False)  # 'source_count', 'agreement', 'quality', 'conflict'
    performed_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Results
    passed = Column(Boolean, nullable=False)
    score = Column(Integer, nullable=True)  # Sub-score for this check
    details = Column(JSON, nullable=True)  # Detailed results
    
    # Conflict Details (if applicable)
    conflict_severity = Column(String(20), nullable=True)  # 'low', 'medium', 'high'
    conflicting_sources = Column(JSON, nullable=True)  # List of source IDs
    conflict_description = Column(Text, nullable=True)
    resolution_explanation = Column(Text, nullable=True)  # AI-generated (premium)
    
    # Relationships
    article = relationship('NewsArticle', back_populates='verification_checks')
    
    def to_dict(self):
        return {
            'id': self.id,
            'article_id': self.article_id,
            'check_type': self.check_type,
            'performed_at': self.performed_at.isoformat() if self.performed_at else None,
            'passed': self.passed,
            'score': self.score,
            'details': self.details,
            'conflict_severity': self.conflict_severity,
            'conflict_description': self.conflict_description
        }


class UserNewsPreference(Base):
    """
    User-specific news feed preferences.
    Controls which sources, categories, and topics to prioritize.
    """
    __tablename__ = 'user_news_preferences'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False, index=True)  # References User table
    
    # Source Preferences
    source_id = Column(String(36), ForeignKey('news_sources.id'), nullable=True, index=True)
    is_following = Column(Boolean, default=False)  # User follows this source
    is_blocked = Column(Boolean, default=False)  # User blocked this source
    
    # Category Preferences
    preferred_categories = Column(JSON, nullable=True)  # List of category strings
    blocked_categories = Column(JSON, nullable=True)
    
    # Ticker Alerts
    watched_tickers = Column(JSON, nullable=True)  # List of stock symbols to track
    
    # Identity-Aware Settings
    identity_type = Column(String(50), nullable=True)  # 'diaspora', 'youth', 'creator', 'legacy'
    enable_identity_filtering = Column(Boolean, default=True)
    
    # Notification Settings
    email_alerts_enabled = Column(Boolean, default=False)
    push_alerts_enabled = Column(Boolean, default=False)
    alert_frequency = Column(String(20), default='daily')  # 'instant', 'hourly', 'daily'
    
    # Thresholds
    min_verification_score = Column(Integer, default=60)  # Only show articles above this score
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    source = relationship('NewsSource', back_populates='user_preferences')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'source_id': self.source_id,
            'is_following': self.is_following,
            'is_blocked': self.is_blocked,
            'preferred_categories': self.preferred_categories or [],
            'watched_tickers': self.watched_tickers or [],
            'identity_type': self.identity_type,
            'min_verification_score': self.min_verification_score
        }


class UserBookmark(Base):
    """
    User-saved articles for later reading.
    """
    __tablename__ = 'user_bookmarks'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False, index=True)
    article_id = Column(String(36), ForeignKey('news_articles.id'), nullable=False, index=True)
    
    # Metadata
    bookmarked_at = Column(DateTime, default=datetime.utcnow, index=True)
    notes = Column(Text, nullable=True)  # User's personal notes
    tags = Column(JSON, nullable=True)  # User's custom tags
    
    # Status
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    
    # Relationships
    article = relationship('NewsArticle', back_populates='bookmarks')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'article_id': self.article_id,
            'bookmarked_at': self.bookmarked_at.isoformat() if self.bookmarked_at else None,
            'notes': self.notes,
            'tags': self.tags or [],
            'is_read': self.is_read
        }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_source_by_slug(session, slug: str) -> NewsSource:
    """Get source by slug (e.g., 'bloomberg')"""
    return session.query(NewsSource).filter_by(slug=slug, is_active=True).first()


def get_articles_by_verification_score(session, min_score: int = 70, limit: int = 50):
    """Get high-quality verified articles"""
    return session.query(NewsArticle).filter(
        NewsArticle.verification_score >= min_score,
        NewsArticle.verification_status == VerificationStatus.VERIFIED,
        NewsArticle.is_active == True
    ).order_by(NewsArticle.published_at.desc()).limit(limit).all()


def get_user_bookmarks(session, user_id: str, limit: int = 100):
    """Get user's bookmarked articles"""
    return session.query(UserBookmark).filter_by(
        user_id=user_id
    ).order_by(UserBookmark.bookmarked_at.desc()).limit(limit).all()


def get_identity_relevant_articles(session, identity_type: str, limit: int = 20):
    """Get articles tagged for specific identity type"""
    filter_map = {
        'diaspora': NewsArticle.relevant_for_diaspora == True,
        'youth': NewsArticle.relevant_for_youth == True,
        'creator': NewsArticle.relevant_for_creator == True,
        'legacy': NewsArticle.relevant_for_legacy == True
    }
    
    if identity_type not in filter_map:
        return []
    
    return session.query(NewsArticle).filter(
        filter_map[identity_type],
        NewsArticle.verification_status == VerificationStatus.VERIFIED,
        NewsArticle.is_active == True
    ).order_by(NewsArticle.published_at.desc()).limit(limit).all()
