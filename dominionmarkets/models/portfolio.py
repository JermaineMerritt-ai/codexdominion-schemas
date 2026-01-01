"""
DominionMarkets Portfolio Models
=================================
SQLAlchemy models for portfolio tracking, holdings management, and allocation analytics.

Last Updated: December 24, 2025
"""

from datetime import datetime
from typing import Optional, Dict, List
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from models import Base


class Portfolio(Base):
    """
    User's investment portfolio
    
    One user can have multiple portfolios (e.g., "Retirement", "Trading", "Long-term")
    """
    __tablename__ = "portfolios"
    
    id = Column(String(36), primary_key=True)  # UUID
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False, default="My Portfolio")
    description = Column(Text, nullable=True)
    
    # Identity-based fields
    identity_type = Column(String(50), nullable=True)  # "diaspora", "youth", "creator", "legacy-builder"
    risk_tolerance = Column(String(20), nullable=True)  # "conservative", "moderate", "aggressive"
    time_horizon = Column(String(20), nullable=True)   # "short", "medium", "long"
    
    # Metadata
    is_active = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)  # Default portfolio for user
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    holdings = relationship("Holding", back_populates="portfolio", cascade="all, delete-orphan")
    analytics = relationship("PortfolioAnalytics", back_populates="portfolio", uselist=False, cascade="all, delete-orphan")
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "identity_type": self.identity_type,
            "risk_tolerance": self.risk_tolerance,
            "time_horizon": self.time_horizon,
            "is_active": self.is_active,
            "is_default": self.is_default,
            "created_at": self.created_at.isoformat() + "Z" if self.created_at else None,
            "updated_at": self.updated_at.isoformat() + "Z" if self.updated_at else None,
            "holdings_count": len(self.holdings) if self.holdings else 0
        }


class Holding(Base):
    """
    Individual stock position within a portfolio
    """
    __tablename__ = "holdings"
    
    id = Column(String(36), primary_key=True)  # UUID
    portfolio_id = Column(String(36), ForeignKey("portfolios.id"), nullable=False, index=True)
    
    # Stock details
    symbol = Column(String(20), nullable=False, index=True)
    company_name = Column(String(200), nullable=True)
    sector = Column(String(50), nullable=True, index=True)
    
    # Position data
    shares = Column(Float, nullable=False, default=0.0)
    avg_cost = Column(Float, nullable=True)  # Average cost per share
    current_price = Column(Float, nullable=True)  # Latest market price (cached)
    
    # Calculated fields (updated on price refresh)
    total_value = Column(Float, nullable=True)  # shares * current_price
    gain_loss = Column(Float, nullable=True)    # (current_price - avg_cost) * shares
    gain_loss_percent = Column(Float, nullable=True)  # ((current_price - avg_cost) / avg_cost) * 100
    
    # Metadata
    purchase_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    last_price_update = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="holdings")
    
    def calculate_metrics(self):
        """Calculate total value and gain/loss based on current price"""
        if self.current_price and self.shares:
            self.total_value = self.current_price * self.shares
            
            if self.avg_cost:
                self.gain_loss = (self.current_price - self.avg_cost) * self.shares
                if self.avg_cost > 0:
                    self.gain_loss_percent = ((self.current_price - self.avg_cost) / self.avg_cost) * 100
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "symbol": self.symbol,
            "company_name": self.company_name,
            "sector": self.sector,
            "shares": self.shares,
            "avg_cost": self.avg_cost,
            "current_price": self.current_price,
            "total_value": self.total_value,
            "gain_loss": self.gain_loss,
            "gain_loss_percent": self.gain_loss_percent,
            "purchase_date": self.purchase_date.isoformat() + "Z" if self.purchase_date else None,
            "notes": self.notes,
            "last_price_update": self.last_price_update.isoformat() + "Z" if self.last_price_update else None,
            "created_at": self.created_at.isoformat() + "Z" if self.created_at else None,
            "updated_at": self.updated_at.isoformat() + "Z" if self.updated_at else None
        }


class PortfolioAnalytics(Base):
    """
    Cached analytics for a portfolio (Premium feature)
    
    Stores pre-calculated metrics to avoid expensive computations on every page load
    """
    __tablename__ = "portfolio_analytics"
    
    id = Column(String(36), primary_key=True)  # UUID
    portfolio_id = Column(String(36), ForeignKey("portfolios.id"), nullable=False, unique=True, index=True)
    
    # Portfolio-level metrics
    total_value = Column(Float, nullable=True)
    total_gain_loss = Column(Float, nullable=True)
    total_gain_loss_percent = Column(Float, nullable=True)
    daily_change = Column(Float, nullable=True)
    daily_change_percent = Column(Float, nullable=True)
    
    # Diversification metrics (Premium)
    diversification_score = Column(Integer, nullable=True)  # 0-100
    diversification_rating = Column(String(20), nullable=True)  # "Poor", "Fair", "Good", "Excellent"
    sector_count = Column(Integer, nullable=True)
    stock_count = Column(Integer, nullable=True)
    concentration_risk = Column(String(20), nullable=True)  # "Low", "Medium", "High"
    
    # Risk metrics (Premium)
    overall_risk_score = Column(Integer, nullable=True)  # 1-10
    overall_risk_rating = Column(String(20), nullable=True)  # "Low Risk", "Medium Risk", "High Risk"
    volatility_30d = Column(Float, nullable=True)  # 30-day standard deviation
    max_drawdown_30d = Column(Float, nullable=True)
    best_day_30d = Column(Float, nullable=True)
    worst_day_30d = Column(Float, nullable=True)
    high_risk_holdings = Column(Integer, nullable=True)
    medium_risk_holdings = Column(Integer, nullable=True)
    low_risk_holdings = Column(Integer, nullable=True)
    
    # Allocation breakdown (stored as JSON)
    sector_allocation = Column(JSON, nullable=True)  # {"Technology": {"percentage": 45.0, "value": 19283.00, "holdings": 8}}
    
    # AI Summary (Premium)
    ai_summary = Column(Text, nullable=True)
    ai_summary_generated_at = Column(DateTime, nullable=True)
    
    # Metadata
    last_calculated = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="analytics")
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "total_value": self.total_value,
            "total_gain_loss": self.total_gain_loss,
            "total_gain_loss_percent": self.total_gain_loss_percent,
            "daily_change": self.daily_change,
            "daily_change_percent": self.daily_change_percent,
            "diversification": {
                "score": self.diversification_score,
                "rating": self.diversification_rating,
                "sector_count": self.sector_count,
                "stock_count": self.stock_count,
                "concentration_risk": self.concentration_risk
            },
            "risk": {
                "overall_score": self.overall_risk_score,
                "overall_rating": self.overall_risk_rating,
                "volatility_30d": self.volatility_30d,
                "max_drawdown_30d": self.max_drawdown_30d,
                "best_day_30d": self.best_day_30d,
                "worst_day_30d": self.worst_day_30d,
                "high_risk_holdings": self.high_risk_holdings,
                "medium_risk_holdings": self.medium_risk_holdings,
                "low_risk_holdings": self.low_risk_holdings
            },
            "sector_allocation": self.sector_allocation,
            "ai_summary": self.ai_summary,
            "ai_summary_generated_at": self.ai_summary_generated_at.isoformat() + "Z" if self.ai_summary_generated_at else None,
            "last_calculated": self.last_calculated.isoformat() + "Z" if self.last_calculated else None
        }


class PortfolioSnapshot(Base):
    """
    Historical portfolio snapshots for performance tracking (Premium feature)
    
    Stores daily portfolio values to build historical performance charts
    """
    __tablename__ = "portfolio_snapshots"
    
    id = Column(String(36), primary_key=True)  # UUID
    portfolio_id = Column(String(36), ForeignKey("portfolios.id"), nullable=False, index=True)
    
    snapshot_date = Column(DateTime, nullable=False, index=True)
    total_value = Column(Float, nullable=False)
    daily_change = Column(Float, nullable=True)
    daily_change_percent = Column(Float, nullable=True)
    
    # Benchmark comparison
    sp500_value = Column(Float, nullable=True)  # S&P 500 level at snapshot
    portfolio_vs_sp500 = Column(Float, nullable=True)  # Relative performance
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "snapshot_date": self.snapshot_date.isoformat() + "Z" if self.snapshot_date else None,
            "total_value": self.total_value,
            "daily_change": self.daily_change,
            "daily_change_percent": self.daily_change_percent,
            "sp500_value": self.sp500_value,
            "portfolio_vs_sp500": self.portfolio_vs_sp500
        }
