"""
Portfolio Services
Business logic for portfolio operations
"""
from models import Portfolio, Holding, Trade, Stock, Fundamental
from extensions import db
from sqlalchemy import func
import ai_prompts

def create_default_portfolio(user_id, risk):
    """Create a default portfolio with starter holdings based on risk profile"""
    templates = {
        "conservative": [
            ("VTI", 0.40),
            ("VOO", 0.20),
            ("VYM", 0.20),
            ("BND", 0.20)
        ],
        "moderate": [
            ("VTI", 0.30),
            ("VOO", 0.20),
            ("QQQ", 0.30),
            ("VYM", 0.20)
        ],
        "aggressive": [
            ("QQQ", 0.40),
            ("ARKK", 0.20),
            ("NVDA", 0.20),
            ("TSLA", 0.20)
        ],
        "trader": []
    }

    p = Portfolio(user_id=user_id, name=f"{risk.title()} Portfolio", risk_profile=risk)
    db.session.add(p)
    db.session.commit()

    for ticker, weight in templates[risk]:
        price = get_stock_price(ticker)
        shares = (10000 * weight) / price if price > 0 else 0  # starter model
        h = Holding(portfolio_id=p.id, ticker=ticker, shares=shares, avg_cost=price)
        db.session.add(h)

    db.session.commit()
    return p

def get_portfolio_holdings(portfolio_id):
    """Get all holdings for a portfolio"""
    holdings = Holding.query.filter_by(portfolio_id=portfolio_id).all()
    return holdings

def get_stock_price(ticker):
    """Get current stock price"""
    stock = Stock.query.filter_by(ticker=ticker.upper()).first()
    return float(stock.price) if stock and stock.price else 0.0

def get_stock_metadata(ticker):
    """Get stock metadata including sector"""
    stock = Stock.query.filter_by(ticker=ticker.upper()).first()
    if not stock:
        return {"sector": "Unknown", "name": ticker}

    return {
        "ticker": stock.ticker,
        "name": stock.name,
        "sector": stock.sector or "Unknown",
        "price": float(stock.price) if stock.price else 0.0,
        "market_cap": float(stock.market_cap) if stock.market_cap else 0.0,
        "pe_ratio": float(stock.pe_ratio) if stock.pe_ratio else None
    }

def compute_portfolio_value(holdings):
    """
    Compute total portfolio value and detailed breakdown

    Returns:
        total (float): Total portfolio value
        detailed (list): List of dicts with ticker, shares, price, value, gain/loss
    """
    total = 0
    detailed = []

    for h in holdings:
        price = get_stock_price(h.ticker)
        value = price * float(h.shares)
        total += value

        detailed.append({
            "ticker": h.ticker,
            "shares": float(h.shares),
            "price": price,
            "value": value,
            "avg_cost": float(h.avg_cost),
            "gain_loss": value - (float(h.avg_cost) * float(h.shares))
        })

    return total, detailed

def compute_allocations(detailed, total_value):
    """
    Add weight/allocation percentage to each holding

    Args:
        detailed (list): Holdings with values
        total_value (float): Total portfolio value

    Returns:
        list: Holdings with weight added
    """
    for row in detailed:
        row["weight"] = round((row["value"] / total_value) * 100, 2) if total_value > 0 else 0
    return detailed

def compute_sector_breakdown(detailed):
    """
    Compute sector allocation percentages

    Args:
        detailed (list): Holdings with weights

    Returns:
        dict: Sector names mapped to total weight percentages
    """
    sector_map = {}
    for row in detailed:
        meta = get_stock_metadata(row["ticker"])
        sector = meta.get("sector", "Unknown")
        sector_map.setdefault(sector, 0)
        sector_map[sector] += row["weight"]

    # Round sector percentages
    for sector in sector_map:
        sector_map[sector] = round(sector_map[sector], 2)

    return sector_map

def compute_portfolio_summary(portfolio):
    """
    Compute comprehensive portfolio summary

    Args:
        portfolio (Portfolio): Portfolio model instance

    Returns:
        dict: Complete portfolio summary with metrics
    """
    holdings = get_portfolio_holdings(portfolio.id)

    if not holdings:
        return {
            "total_value": 0,
            "num_holdings": 0,
            "largest_position": None,
            "sector_breakdown": {},
            "holdings": []
        }

    total_value, detailed = compute_portfolio_value(holdings)
    detailed = compute_allocations(detailed, total_value)
    sectors = compute_sector_breakdown(detailed)

    summary = {
        "total_value": round(total_value, 2),
        "num_holdings": len(holdings),
        "largest_position": max(detailed, key=lambda x: x["weight"])["ticker"] if detailed else None,
        "sector_breakdown": sectors,
        "holdings": detailed
    }

    return summary

def estimate_portfolio_volatility(detailed):
    """
    Estimate portfolio volatility (placeholder implementation)

    TODO: Implement proper volatility calculation using:
    - Individual stock volatility scores from alerts table
    - Weighted average by position size
    - Correlation adjustments

    Args:
        detailed (list): Holdings with weights

    Returns:
        str: 'low', 'medium', or 'high'
    """
    # Placeholder: Use sector concentration as proxy
    # High concentration = higher volatility
    num_positions = len(detailed)

    if num_positions >= 10:
        return "low"
    elif num_positions >= 5:
        return "medium"
    else:
        return "high"

def get_ai_portfolio_insights(portfolio):
    """
    Get AI-generated portfolio analysis and insights

    Args:
        portfolio (Portfolio): Portfolio model instance

    Returns:
        str: AI analysis text for display
    """
    summary = compute_portfolio_summary(portfolio)

    if not summary["holdings"]:
        return "No holdings in portfolio. Add positions to generate analysis."

    # Check if AI is configured
    try:
        from ai_services import run_portfolio_analysis, is_ai_configured

        if not is_ai_configured():
            return "⚠️ AI service not configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable to enable AI insights."

        # Prepare summary metrics
        summary_metrics = {
            "total_value": summary["total_value"],
            "num_holdings": summary["num_holdings"],
            "largest_position": summary["largest_position"],
            "sector_concentration": summary["sector_breakdown"],
            "overall_volatility": estimate_portfolio_volatility(summary["holdings"])
        }

        # Call AI service
        analysis = run_portfolio_analysis(
            portfolio_name=portfolio.name,
            risk_profile=portfolio.risk_profile,
            holdings=summary["holdings"],
            summary_metrics=summary_metrics
        )

        # Return the analysis text directly
        return analysis if isinstance(analysis, str) else str(analysis)

    except ImportError:
        # AI services not available - return placeholder with portfolio stats
        holdings_text = ", ".join([f"{h['ticker']} ({h['weight']}%)" for h in summary["holdings"][:5]])
        if len(summary["holdings"]) > 5:
            holdings_text += f", and {len(summary['holdings']) - 5} more"

        return f"""Portfolio Analysis:

📊 Portfolio Size: {summary['num_holdings']} holdings worth ${summary['total_value']:,.2f}

🎯 Risk Profile: {portfolio.risk_profile.capitalize()}

📈 Top Holdings: {holdings_text}

🏢 Sector Breakdown: {', '.join([f"{k}: {v}%" for k, v in summary['sector_breakdown'].items()])}

ℹ️ AI-powered insights require configuration of ai_services.py module."""

    except Exception as e:
        return f"Unable to generate AI insights at this time. Error: {str(e)}"

def get_portfolio_trades(portfolio_id, limit=50):
    """
    Get recent trade history for portfolio

    Args:
        portfolio_id (int): Portfolio ID
        limit (int): Maximum number of trades to return

    Returns:
        list: Trade instances ordered by date descending
    """
    trades = Trade.query.filter_by(portfolio_id=portfolio_id)\
        .order_by(Trade.trade_date.desc())\
        .limit(limit)\
        .all()
    return trades

def calculate_trade_metrics(portfolio_id):
    """
    Calculate trade statistics

    Args:
        portfolio_id (int): Portfolio ID

    Returns:
        dict: Trade statistics (total trades, buy/sell counts, fees)
    """
    trades = Trade.query.filter_by(portfolio_id=portfolio_id).all()

    if not trades:
        return {
            "total_trades": 0,
            "buy_count": 0,
            "sell_count": 0,
            "total_fees": 0.0
        }

    buy_count = sum(1 for t in trades if t.trade_type == 'buy')
    sell_count = sum(1 for t in trades if t.trade_type == 'sell')
    total_fees = sum(float(t.fees) for t in trades if t.fees)

    return {
        "total_trades": len(trades),
        "buy_count": buy_count,
        "sell_count": sell_count,
        "total_fees": round(total_fees, 2)
    }
