"""
DominionMarkets Portfolio API
==============================
Flask routes for portfolio management, holdings CRUD, allocation analytics, and AI summaries.

Last Updated: December 24, 2025
"""

from flask import Blueprint, request, jsonify, session as flask_session
from datetime import datetime, timedelta
import uuid
import os
from typing import Dict, List, Optional
from sqlalchemy import func

from db import SessionLocal
from dominionmarkets.models.portfolio import Portfolio, Holding, PortfolioAnalytics, PortfolioSnapshot
from dominionmarkets.services.stock_service import StockDataService
from dominionmarkets.services.ai_service import generate_portfolio_summary
from dominionmarkets.utils.premium import require_premium, get_user_tier

portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/api/portfolio')

# Initialize services
stock_service = StockDataService()

# AI Service (fallback if import fails)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


# ============================================================================
# PORTFOLIO CRUD
# ============================================================================

@portfolio_bp.route('/', methods=['GET'])
def list_portfolios():
    """Get all portfolios for current user"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    session = SessionLocal()
    try:
        portfolios = session.query(Portfolio).filter_by(user_id=user_id, is_active=True).all()
        return jsonify({
            "portfolios": [p.to_dict() for p in portfolios]
        }), 200
    finally:
        session.close()


@portfolio_bp.route('/', methods=['POST'])
def create_portfolio():
    """Create new portfolio"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    
    session = SessionLocal()
    try:
        portfolio = Portfolio(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=data.get('name', 'My Portfolio'),
            description=data.get('description'),
            identity_type=data.get('identity_type'),
            risk_tolerance=data.get('risk_tolerance'),
            time_horizon=data.get('time_horizon'),
            is_default=data.get('is_default', False)
        )
        
        # If this is default, un-default others
        if portfolio.is_default:
            session.query(Portfolio).filter_by(user_id=user_id).update({"is_default": False})
        
        session.add(portfolio)
        
        # Create analytics record
        analytics = PortfolioAnalytics(
            id=str(uuid.uuid4()),
            portfolio_id=portfolio.id
        )
        session.add(analytics)
        
        session.commit()
        
        return jsonify({
            "success": True,
            "portfolio": portfolio.to_dict()
        }), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@portfolio_bp.route('/<portfolio_id>', methods=['GET'])
def get_portfolio(portfolio_id: str):
    """Get portfolio details with analytics"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    session = SessionLocal()
    try:
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id, user_id=user_id).first()
        if not portfolio:
            return jsonify({"error": "Portfolio not found"}), 404
        
        # Get analytics
        analytics = session.query(PortfolioAnalytics).filter_by(portfolio_id=portfolio_id).first()
        
        # Calculate if stale (>15 minutes old)
        needs_refresh = True
        if analytics and analytics.last_calculated:
            age = datetime.utcnow() - analytics.last_calculated
            needs_refresh = age > timedelta(minutes=15)
        
        # Refresh analytics if needed
        if needs_refresh:
            refresh_portfolio_analytics(portfolio, session)
            session.commit()
            analytics = session.query(PortfolioAnalytics).filter_by(portfolio_id=portfolio_id).first()
        
        response = {
            "portfolio": portfolio.to_dict(),
            "analytics": analytics.to_dict() if analytics else None,
            "holdings": [h.to_dict() for h in portfolio.holdings]
        }
        
        return jsonify(response), 200
    finally:
        session.close()


# ============================================================================
# HOLDINGS CRUD
# ============================================================================

@portfolio_bp.route('/<portfolio_id>/holdings', methods=['GET'])
def list_holdings(portfolio_id: str):
    """Get all holdings for a portfolio"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    session = SessionLocal()
    try:
        # Verify ownership
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id, user_id=user_id).first()
        if not portfolio:
            return jsonify({"error": "Portfolio not found"}), 404
        
        holdings = session.query(Holding).filter_by(portfolio_id=portfolio_id).order_by(Holding.total_value.desc()).all()
        
        return jsonify({
            "holdings": [h.to_dict() for h in holdings]
        }), 200
    finally:
        session.close()


@portfolio_bp.route('/<portfolio_id>/holdings', methods=['POST'])
def add_holding(portfolio_id: str):
    """Add new holding to portfolio"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    symbol = data.get('symbol', '').upper()
    shares = data.get('shares', 0)
    
    if not symbol or shares <= 0:
        return jsonify({"error": "Symbol and shares required"}), 400
    
    session = SessionLocal()
    try:
        # Verify ownership
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id, user_id=user_id).first()
        if not portfolio:
            return jsonify({"error": "Portfolio not found"}), 404
        
        # Get stock data
        stock_data = stock_service.get_stock_quote(symbol)
        if not stock_data:
            return jsonify({"error": f"Invalid stock symbol: {symbol}"}), 400
        
        # Check if holding already exists
        existing = session.query(Holding).filter_by(portfolio_id=portfolio_id, symbol=symbol).first()
        if existing:
            return jsonify({"error": f"Holding for {symbol} already exists. Use PATCH to update."}), 409
        
        holding = Holding(
            id=str(uuid.uuid4()),
            portfolio_id=portfolio_id,
            symbol=symbol,
            company_name=stock_data.get('company_name'),
            sector=stock_data.get('sector'),
            shares=shares,
            avg_cost=data.get('avg_cost'),
            current_price=stock_data.get('price'),
            purchase_date=data.get('purchase_date'),
            notes=data.get('notes'),
            last_price_update=datetime.utcnow()
        )
        
        holding.calculate_metrics()
        session.add(holding)
        
        # Trigger analytics refresh
        refresh_portfolio_analytics(portfolio, session)
        
        session.commit()
        
        return jsonify({
            "success": True,
            "holding": holding.to_dict()
        }), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@portfolio_bp.route('/<portfolio_id>/holdings/<holding_id>', methods=['PATCH'])
def update_holding(portfolio_id: str, holding_id: str):
    """Update existing holding"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    
    session = SessionLocal()
    try:
        # Verify ownership
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id, user_id=user_id).first()
        if not portfolio:
            return jsonify({"error": "Portfolio not found"}), 404
        
        holding = session.query(Holding).filter_by(id=holding_id, portfolio_id=portfolio_id).first()
        if not holding:
            return jsonify({"error": "Holding not found"}), 404
        
        # Update fields
        if 'shares' in data:
            holding.shares = data['shares']
        if 'avg_cost' in data:
            holding.avg_cost = data['avg_cost']
        if 'notes' in data:
            holding.notes = data['notes']
        
        holding.calculate_metrics()
        holding.updated_at = datetime.utcnow()
        
        # Trigger analytics refresh
        refresh_portfolio_analytics(portfolio, session)
        
        session.commit()
        
        return jsonify({
            "success": True,
            "holding": holding.to_dict()
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@portfolio_bp.route('/<portfolio_id>/holdings/<holding_id>', methods=['DELETE'])
def remove_holding(portfolio_id: str, holding_id: str):
    """Remove holding from portfolio"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    session = SessionLocal()
    try:
        # Verify ownership
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id, user_id=user_id).first()
        if not portfolio:
            return jsonify({"error": "Portfolio not found"}), 404
        
        holding = session.query(Holding).filter_by(id=holding_id, portfolio_id=portfolio_id).first()
        if not holding:
            return jsonify({"error": "Holding not found"}), 404
        
        session.delete(holding)
        
        # Trigger analytics refresh
        refresh_portfolio_analytics(portfolio, session)
        
        session.commit()
        
        return jsonify({"success": True}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# ============================================================================
# ANALYTICS & ALLOCATION
# ============================================================================

@portfolio_bp.route('/<portfolio_id>/allocation', methods=['GET'])
def get_allocation(portfolio_id: str):
    """Get portfolio allocation breakdown by sector"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    session = SessionLocal()
    try:
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id, user_id=user_id).first()
        if not portfolio:
            return jsonify({"error": "Portfolio not found"}), 404
        
        analytics = session.query(PortfolioAnalytics).filter_by(portfolio_id=portfolio_id).first()
        
        return jsonify({
            "sector_allocation": analytics.sector_allocation if analytics else {},
            "total_value": analytics.total_value if analytics else 0
        }), 200
    finally:
        session.close()


@portfolio_bp.route('/<portfolio_id>/analytics', methods=['GET'])
@require_premium
def get_premium_analytics(portfolio_id: str):
    """Get advanced analytics (Premium only)"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    session = SessionLocal()
    try:
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id, user_id=user_id).first()
        if not portfolio:
            return jsonify({"error": "Portfolio not found"}), 404
        
        analytics = session.query(PortfolioAnalytics).filter_by(portfolio_id=portfolio_id).first()
        if not analytics:
            return jsonify({"error": "Analytics not available"}), 404
        
        return jsonify(analytics.to_dict()), 200
    finally:
        session.close()


@portfolio_bp.route('/<portfolio_id>/refresh', methods=['POST'])
def refresh_prices(portfolio_id: str):
    """Refresh stock prices for all holdings"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    session = SessionLocal()
    try:
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id, user_id=user_id).first()
        if not portfolio:
            return jsonify({"error": "Portfolio not found"}), 404
        
        # Update all holding prices
        updated_count = 0
        for holding in portfolio.holdings:
            stock_data = stock_service.get_stock_quote(holding.symbol)
            if stock_data:
                holding.current_price = stock_data.get('price')
                holding.last_price_update = datetime.utcnow()
                holding.calculate_metrics()
                updated_count += 1
        
        # Refresh analytics
        refresh_portfolio_analytics(portfolio, session)
        
        session.commit()
        
        return jsonify({
            "success": True,
            "updated_holdings": updated_count,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# ============================================================================
# AI SUMMARY
# ============================================================================

@portfolio_bp.route('/<portfolio_id>/ai-summary', methods=['POST'])
@require_premium
def generate_ai_summary(portfolio_id: str):
    """Generate AI portfolio summary (Premium only)"""
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    session = SessionLocal()
    try:
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id, user_id=user_id).first()
        if not portfolio:
            return jsonify({"error": "Portfolio not found"}), 404
        
        analytics = session.query(PortfolioAnalytics).filter_by(portfolio_id=portfolio_id).first()
        
        # Generate summary
        summary = generate_portfolio_summary(
            portfolio=portfolio.to_dict(),
            holdings=[h.to_dict() for h in portfolio.holdings],
            analytics=analytics.to_dict() if analytics else None,
            identity_type=portfolio.identity_type or "general"
        )
        
        # Save to analytics
        if analytics:
            analytics.ai_summary = summary
            analytics.ai_summary_generated_at = datetime.utcnow()
            session.commit()
        
        return jsonify({
            "summary": summary,
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def refresh_portfolio_analytics(portfolio: Portfolio, session):
    """
    Recalculate portfolio analytics
    
    Called after any holding changes to keep metrics current
    """
    analytics = session.query(PortfolioAnalytics).filter_by(portfolio_id=portfolio.id).first()
    if not analytics:
        analytics = PortfolioAnalytics(
            id=str(uuid.uuid4()),
            portfolio_id=portfolio.id
        )
        session.add(analytics)
    
    holdings = portfolio.holdings
    
    # Calculate total value and P&L
    total_value = sum(h.total_value or 0 for h in holdings)
    total_gain_loss = sum(h.gain_loss or 0 for h in holdings)
    total_gain_loss_percent = (total_gain_loss / (total_value - total_gain_loss) * 100) if (total_value - total_gain_loss) > 0 else 0
    
    analytics.total_value = total_value
    analytics.total_gain_loss = total_gain_loss
    analytics.total_gain_loss_percent = total_gain_loss_percent
    
    # Calculate sector allocation
    sector_breakdown = {}
    for holding in holdings:
        sector = holding.sector or "Other"
        if sector not in sector_breakdown:
            sector_breakdown[sector] = {"value": 0, "holdings": 0}
        
        sector_breakdown[sector]["value"] += holding.total_value or 0
        sector_breakdown[sector]["holdings"] += 1
    
    # Add percentages
    for sector in sector_breakdown:
        sector_breakdown[sector]["percentage"] = (sector_breakdown[sector]["value"] / total_value * 100) if total_value > 0 else 0
    
    analytics.sector_allocation = sector_breakdown
    
    # Diversification score
    analytics.sector_count = len(sector_breakdown)
    analytics.stock_count = len(holdings)
    analytics.diversification_score = calculate_diversification_score(sector_breakdown, len(holdings))
    
    if analytics.diversification_score >= 80:
        analytics.diversification_rating = "Excellent"
        analytics.concentration_risk = "Low"
    elif analytics.diversification_score >= 60:
        analytics.diversification_rating = "Good"
        analytics.concentration_risk = "Low"
    elif analytics.diversification_score >= 40:
        analytics.diversification_rating = "Fair"
        analytics.concentration_risk = "Medium"
    else:
        analytics.diversification_rating = "Poor"
        analytics.concentration_risk = "High"
    
    analytics.last_calculated = datetime.utcnow()


def calculate_diversification_score(sector_breakdown: Dict, stock_count: int) -> int:
    """
    Calculate diversification score (0-100)
    
    Factors:
    - Number of sectors (more = better)
    - Sector concentration (more even = better)
    - Number of stocks (more = better)
    """
    sector_count = len(sector_breakdown)
    
    # Sector diversity component (0-40 points)
    sector_score = min(sector_count * 8, 40)
    
    # Concentration component (0-40 points)
    # Penalize if any sector >50%
    max_sector_pct = max(s["percentage"] for s in sector_breakdown.values()) if sector_breakdown else 0
    if max_sector_pct > 50:
        concentration_score = 10
    elif max_sector_pct > 40:
        concentration_score = 20
    elif max_sector_pct > 30:
        concentration_score = 30
    else:
        concentration_score = 40
    
    # Stock count component (0-20 points)
    stock_score = min(stock_count * 2, 20)
    
    return sector_score + concentration_score + stock_score


# ============================================================================
# AI SUMMARY ENDPOINT
# ============================================================================

@portfolio_bp.route('/<string:portfolio_id>/ai-summary', methods=['POST'])
@require_premium
def generate_ai_summary(portfolio_id: str):
    """
    Generate AI-powered portfolio summary with compliance guardrails.
    Premium/Pro only.
    """
    user_id = flask_session.get('user_id')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    if not OPENAI_AVAILABLE:
        return jsonify({"error": "AI service not available"}), 503
    
    session = SessionLocal()
    try:
        # Load portfolio
        portfolio = session.query(Portfolio).filter_by(
            id=portfolio_id, 
            user_id=user_id, 
            is_active=True
        ).first()
        
        if not portfolio:
            return jsonify({"error": "Portfolio not found"}), 404
        
        # Get holdings with current prices
        holdings = session.query(Holding).filter_by(
            portfolio_id=portfolio_id, 
            is_active=True
        ).all()
        
        if not holdings:
            return jsonify({"error": "No holdings in portfolio"}), 400
        
        # Get allocation data
        sector_breakdown = {}
        for holding in holdings:
            sector = holding.sector or "Unknown"
            if sector not in sector_breakdown:
                sector_breakdown[sector] = {
                    "sector": sector,
                    "value": 0,
                    "percentage": 0,
                    "count": 0
                }
            sector_breakdown[sector]["value"] += holding.current_value
            sector_breakdown[sector]["count"] += 1
        
        total_value = sum(s["value"] for s in sector_breakdown.values())
        for sector_data in sector_breakdown.values():
            sector_data["percentage"] = (sector_data["value"] / total_value * 100) if total_value > 0 else 0
        
        # Get user identity type
        user_identity = flask_session.get('user_identity', 'general')
        
        # Generate summary via OpenAI
        try:
            summary_text = generate_portfolio_summary(
                portfolio=portfolio.to_dict(),
                holdings=[h.to_dict() for h in holdings],
                sector_breakdown=list(sector_breakdown.values()),
                identity_type=user_identity
            )
        except Exception as e:
            return jsonify({"error": f"AI generation failed: {str(e)}"}), 500
        
        # Update analytics with AI summary
        analytics = session.query(PortfolioAnalytics).filter_by(
            portfolio_id=portfolio_id
        ).first()
        
        if not analytics:
            analytics = PortfolioAnalytics(
                portfolio_id=portfolio_id,
                ai_summary=summary_text,
                ai_summary_generated_at=datetime.utcnow()
            )
            session.add(analytics)
        else:
            analytics.ai_summary = summary_text
            analytics.ai_summary_generated_at = datetime.utcnow()
        
        session.commit()
        
        return jsonify({
            "success": True,
            "summary": summary_text,
            "generated_at": analytics.ai_summary_generated_at.isoformat()
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
