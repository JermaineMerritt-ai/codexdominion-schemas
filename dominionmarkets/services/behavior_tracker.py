"""
Behavior Tracker - Tracks user activity for behavioral cross-promotion
Non-sensitive tracking: stocks viewed, news read, sectors explored
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey, func
from sqlalchemy.orm import relationship
from db import SessionLocal
import uuid

# Import Base from root models.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from models import Base


# ============================================================================
# BEHAVIOR TRACKING MODEL
# ============================================================================

class UserBehavior(Base):
    """
    Tracks non-sensitive user activity for behavioral cross-promotion.
    
    Tracked Activities:
    - Stocks viewed (symbols)
    - News articles read (categories, sectors)
    - Portfolio checks (frequency)
    - Sectors explored (technology, finance, etc.)
    - Alert creation patterns
    - AI summary usage
    
    NOT Tracked:
    - Dollar amounts
    - Specific holdings
    - Personal information
    - Transaction details
    """
    __tablename__ = "user_behaviors"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # References
    user_id = Column(String(36), nullable=False, index=True)
    
    # Activity Counters (rolling 7 days)
    stocks_viewed = Column(JSON, nullable=True)  # {"AAPL": 5, "TSLA": 3, ...}
    sectors_viewed = Column(JSON, nullable=True)  # {"technology": 10, "finance": 5, ...}
    news_categories_read = Column(JSON, nullable=True)  # {"earnings": 8, "markets": 12, ...}
    
    # Frequency Metrics
    portfolio_checks_today = Column(Integer, nullable=False, default=0)
    portfolio_checks_this_week = Column(Integer, nullable=False, default=0)
    news_views_this_week = Column(Integer, nullable=False, default=0)
    ai_summary_usage_today = Column(Integer, nullable=False, default=0)
    alert_count = Column(Integer, nullable=False, default=0)
    
    # Creator Economy Detection
    creator_stocks_viewed = Column(Integer, nullable=False, default=0)  # SHOP, ETSY, META, etc.
    creator_news_read = Column(Integer, nullable=False, default=0)
    
    # Diaspora Detection
    diaspora_news_read = Column(Integer, nullable=False, default=0)
    international_stocks_viewed = Column(Integer, nullable=False, default=0)
    
    # Youth Detection (implicit)
    beginner_articles_read = Column(Integer, nullable=False, default=0)
    mock_portfolio_usage = Column(Integer, nullable=False, default=0)
    
    # Legacy Detection
    dividend_stocks_viewed = Column(Integer, nullable=False, default=0)
    dividend_news_read = Column(Integer, nullable=False, default=0)
    
    # Timestamps
    last_activity = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================================================
# BEHAVIOR TRACKING SERVICE
# ============================================================================

class BehaviorTracker:
    """
    Service for tracking and analyzing user behavior for cross-promotion.
    """
    
    # Creator economy symbols
    CREATOR_STOCKS = ['SHOP', 'ETSY', 'META', 'PINS', 'SNAP', 'SPOT', 'RBLX', 'U', 'TWTR']
    
    # International/diaspora markets (partial list)
    INTERNATIONAL_STOCKS = ['EWJ', 'EWZ', 'EWW', 'EWG', 'EWU', 'FXI', 'INDA']  # ETFs
    
    # Dividend aristocrats (partial list)
    DIVIDEND_STOCKS = ['JNJ', 'PG', 'KO', 'PEP', 'MCD', 'WMT', 'CVX', 'XOM']
    
    def __init__(self):
        self.session = SessionLocal()
    
    def __del__(self):
        self.session.close()
    
    def track_stock_view(self, user_id: str, symbol: str):
        """Records that user viewed a stock"""
        behavior = self._get_or_create(user_id)
        
        # Update stocks_viewed dict
        stocks = behavior.stocks_viewed or {}
        stocks[symbol] = stocks.get(symbol, 0) + 1
        behavior.stocks_viewed = stocks
        
        # Update category counters
        if symbol in self.CREATOR_STOCKS:
            behavior.creator_stocks_viewed += 1
        if symbol in self.INTERNATIONAL_STOCKS:
            behavior.international_stocks_viewed += 1
        if symbol in self.DIVIDEND_STOCKS:
            behavior.dividend_stocks_viewed += 1
        
        behavior.last_activity = datetime.utcnow()
        self.session.commit()
    
    def track_sector_view(self, user_id: str, sector: str):
        """Records that user viewed a sector (e.g., 'technology', 'finance')"""
        behavior = self._get_or_create(user_id)
        
        sectors = behavior.sectors_viewed or {}
        sectors[sector] = sectors.get(sector, 0) + 1
        behavior.sectors_viewed = sectors
        
        behavior.last_activity = datetime.utcnow()
        self.session.commit()
    
    def track_news_read(self, user_id: str, category: str, is_diaspora: bool = False, is_creator: bool = False):
        """Records that user read a news article"""
        behavior = self._get_or_create(user_id)
        
        # Update news_categories_read dict
        categories = behavior.news_categories_read or {}
        categories[category] = categories.get(category, 0) + 1
        behavior.news_categories_read = categories
        
        # Update counters
        behavior.news_views_this_week += 1
        
        if is_diaspora:
            behavior.diaspora_news_read += 1
        if is_creator:
            behavior.creator_news_read += 1
        
        behavior.last_activity = datetime.utcnow()
        self.session.commit()
    
    def track_portfolio_check(self, user_id: str):
        """Records that user checked their portfolio"""
        behavior = self._get_or_create(user_id)
        
        behavior.portfolio_checks_today += 1
        behavior.portfolio_checks_this_week += 1
        behavior.last_activity = datetime.utcnow()
        
        self.session.commit()
    
    def track_ai_summary_usage(self, user_id: str):
        """Records that user used AI summary feature"""
        behavior = self._get_or_create(user_id)
        
        behavior.ai_summary_usage_today += 1
        behavior.last_activity = datetime.utcnow()
        
        self.session.commit()
    
    def track_alert_creation(self, user_id: str):
        """Records that user created an alert"""
        behavior = self._get_or_create(user_id)
        
        behavior.alert_count += 1
        behavior.last_activity = datetime.utcnow()
        
        self.session.commit()
    
    def get_behavior_context(self, user_id: str) -> Dict[str, Any]:
        """
        Returns behavior context for promotion selection.
        Used by PromotionService to refine recommendations.
        """
        behavior = self._get_or_create(user_id)
        
        # Get top viewed stocks
        stocks_viewed = behavior.stocks_viewed or {}
        top_stocks = sorted(stocks_viewed.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Get top sectors
        sectors_viewed = behavior.sectors_viewed or {}
        top_sectors = sorted(sectors_viewed.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "portfolio_checks_today": behavior.portfolio_checks_today,
            "portfolio_checks_this_week": behavior.portfolio_checks_this_week,
            "news_views_this_week": behavior.news_views_this_week,
            "ai_summary_usage_today": behavior.ai_summary_usage_today,
            "alert_count": behavior.alert_count,
            
            # Category strengths (for behavioral scoring)
            "creator_score": behavior.creator_stocks_viewed + behavior.creator_news_read,
            "diaspora_score": behavior.diaspora_news_read + behavior.international_stocks_viewed,
            "youth_score": behavior.beginner_articles_read + behavior.mock_portfolio_usage,
            "legacy_score": behavior.dividend_stocks_viewed + behavior.dividend_news_read,
            
            # Top interests
            "top_stocks": [symbol for symbol, count in top_stocks],
            "top_sectors": [sector for sector, count in top_sectors],
            
            # Recent activity
            "last_activity": behavior.last_activity.isoformat()
        }
    
    def calculate_behavioral_relevance(
        self,
        user_id: str,
        promotion_identity: str
    ) -> int:
        """
        Calculates behavioral relevance score for a promotion.
        Higher score = better fit based on recent behavior.
        
        Returns: Score from 0-100
        """
        behavior = self._get_or_create(user_id)
        
        # Base scores by identity
        scores = {
            'creator': behavior.creator_stocks_viewed * 2 + behavior.creator_news_read * 3,
            'diaspora': behavior.diaspora_news_read * 3 + behavior.international_stocks_viewed * 2,
            'youth': behavior.beginner_articles_read * 3 + behavior.mock_portfolio_usage * 4,
            'legacy': behavior.dividend_stocks_viewed * 2 + behavior.dividend_news_read * 3,
            'all': 10  # Universal products get base score
        }
        
        return min(scores.get(promotion_identity, 0), 100)
    
    def reset_daily_counters(self, user_id: str):
        """Resets daily counters (called by scheduled job)"""
        behavior = self._get_or_create(user_id)
        
        behavior.portfolio_checks_today = 0
        behavior.ai_summary_usage_today = 0
        
        self.session.commit()
    
    def reset_weekly_counters(self, user_id: str):
        """Resets weekly counters (called by scheduled job)"""
        behavior = self._get_or_create(user_id)
        
        behavior.portfolio_checks_this_week = 0
        behavior.news_views_this_week = 0
        
        # Decay behavior scores (50% reduction weekly)
        behavior.creator_stocks_viewed = int(behavior.creator_stocks_viewed * 0.5)
        behavior.creator_news_read = int(behavior.creator_news_read * 0.5)
        behavior.diaspora_news_read = int(behavior.diaspora_news_read * 0.5)
        behavior.international_stocks_viewed = int(behavior.international_stocks_viewed * 0.5)
        behavior.beginner_articles_read = int(behavior.beginner_articles_read * 0.5)
        behavior.mock_portfolio_usage = int(behavior.mock_portfolio_usage * 0.5)
        behavior.dividend_stocks_viewed = int(behavior.dividend_stocks_viewed * 0.5)
        behavior.dividend_news_read = int(behavior.dividend_news_read * 0.5)
        
        self.session.commit()
    
    def _get_or_create(self, user_id: str) -> UserBehavior:
        """Gets or creates UserBehavior record"""
        behavior = self.session.query(UserBehavior).filter_by(user_id=user_id).first()
        
        if not behavior:
            behavior = UserBehavior(user_id=user_id)
            self.session.add(behavior)
            self.session.commit()
        
        return behavior


# ============================================================================
# API HELPERS
# ============================================================================

def get_recent_behavior(user_id: str) -> Dict[str, Any]:
    """
    Returns recent behavior summary for API responses.
    Safe for external consumption (no PII).
    """
    tracker = BehaviorTracker()
    return tracker.get_behavior_context(user_id)


def track_activity(
    user_id: str,
    activity_type: str,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Convenience function for tracking activities from API routes.
    
    Usage:
        track_activity(user_id, 'stock_view', {'symbol': 'AAPL'})
        track_activity(user_id, 'news_read', {'category': 'earnings', 'is_creator': True})
        track_activity(user_id, 'portfolio_check')
    """
    tracker = BehaviorTracker()
    metadata = metadata or {}
    
    if activity_type == 'stock_view':
        symbol = metadata.get('symbol')
        if symbol:
            tracker.track_stock_view(user_id, symbol)
    
    elif activity_type == 'sector_view':
        sector = metadata.get('sector')
        if sector:
            tracker.track_sector_view(user_id, sector)
    
    elif activity_type == 'news_read':
        category = metadata.get('category', 'general')
        is_diaspora = metadata.get('is_diaspora', False)
        is_creator = metadata.get('is_creator', False)
        tracker.track_news_read(user_id, category, is_diaspora, is_creator)
    
    elif activity_type == 'portfolio_check':
        tracker.track_portfolio_check(user_id)
    
    elif activity_type == 'ai_summary':
        tracker.track_ai_summary_usage(user_id)
    
    elif activity_type == 'alert_creation':
        tracker.track_alert_creation(user_id)

