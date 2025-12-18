"""
Stock Services
Business logic for stock data operations
Supports both database and external API data sources
"""
from models import Stock, Fundamental, Alert
from extensions import db
from datetime import datetime, timedelta
import ai_prompts
import os
import requests

# API Configuration
STOCK_API_KEY = os.environ.get('STOCK_API_KEY')
STOCK_API_PROVIDER = os.environ.get('STOCK_API_PROVIDER', 'database')  # 'database', 'polygon', 'alphavantage'
POLYGON_BASE_URL = "https://api.polygon.io/v3"
ALPHAVANTAGE_BASE_URL = "https://www.alphavantage.co/query"

def get_stock_price(ticker, use_api=False):
    """
    Get current stock price from database or API

    Args:
        ticker (str): Stock ticker symbol
        use_api (bool): Force API call instead of database

    Returns:
        float: Current stock price
    """
    ticker = ticker.upper()

    # Try database first unless API forced
    if not use_api or STOCK_API_PROVIDER == 'database':
        stock = Stock.query.filter_by(ticker=ticker).first()
        if stock and stock.price:
            return float(stock.price)

    # Fall back to API if configured
    if STOCK_API_KEY and STOCK_API_PROVIDER == 'polygon':
        try:
            url = f"{POLYGON_BASE_URL}/last_trade/{ticker}?apiKey={STOCK_API_KEY}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            price = data.get("results", {}).get("price", 0)
            return float(price) if price else 0.0
        except Exception as e:
            print(f"Polygon API error for {ticker}: {e}")

    elif STOCK_API_KEY and STOCK_API_PROVIDER == 'alphavantage':
        try:
            url = f"{ALPHAVANTAGE_BASE_URL}?function=GLOBAL_QUOTE&symbol={ticker}&apikey={STOCK_API_KEY}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            price = data.get("Global Quote", {}).get("05. price", 0)
            return float(price) if price else 0.0
        except Exception as e:
            print(f"Alpha Vantage API error for {ticker}: {e}")

    return 0.0

def get_stock_metadata(ticker, use_api=False):
    """
    Get complete stock metadata from database or API

    Args:
        ticker (str): Stock ticker symbol
        use_api (bool): Force API call instead of database

    Returns:
        dict: Stock metadata (ticker, name, sector, price, market_cap, pe_ratio)
    """
    ticker = ticker.upper()

    # Try database first unless API forced
    if not use_api or STOCK_API_PROVIDER == 'database':
        stock = Stock.query.filter_by(ticker=ticker).first()
        if stock:
            return {
                "ticker": stock.ticker,
                "name": stock.name,
                "sector": stock.sector or "Unknown",
                "price": float(stock.price) if stock.price else 0.0,
                "market_cap": float(stock.market_cap) if stock.market_cap else 0.0,
                "pe_ratio": float(stock.pe_ratio) if stock.pe_ratio else None
            }

    # Fall back to API if configured
    if STOCK_API_KEY and STOCK_API_PROVIDER == 'polygon':
        try:
            url = f"{POLYGON_BASE_URL}/reference/tickers/{ticker}?apiKey={STOCK_API_KEY}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", {})

            return {
                "ticker": ticker,
                "name": results.get("name"),
                "sector": results.get("sic_description", "Unknown"),
                "price": get_stock_price(ticker, use_api=True),
                "market_cap": results.get("market_cap", 0),
                "pe_ratio": results.get("pe_ratio")
            }
        except Exception as e:
            print(f"Polygon API error for {ticker}: {e}")

    elif STOCK_API_KEY and STOCK_API_PROVIDER == 'alphavantage':
        try:
            # Alpha Vantage requires separate calls for overview and price
            url = f"{ALPHAVANTAGE_BASE_URL}?function=OVERVIEW&symbol={ticker}&apikey={STOCK_API_KEY}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            return {
                "ticker": ticker,
                "name": data.get("Name"),
                "sector": data.get("Sector", "Unknown"),
                "price": get_stock_price(ticker, use_api=True),
                "market_cap": float(data.get("MarketCapitalization", 0)),
                "pe_ratio": float(data.get("PERatio")) if data.get("PERatio") != "None" else None
            }
        except Exception as e:
            print(f"Alpha Vantage API error for {ticker}: {e}")

    # Default fallback
    return {"ticker": ticker, "name": ticker, "sector": "Unknown", "price": 0.0, "market_cap": 0.0, "pe_ratio": None}

def get_stock_fundamentals(ticker):
    """Get fundamental analysis data"""
    fundamental = Fundamental.query.filter_by(ticker=ticker.upper()).first()

    if not fundamental:
        return None

    return {
        "ticker": fundamental.ticker,
        "revenue_trend": fundamental.revenue_trend,
        "net_income_trend": fundamental.net_income_trend,
        "debt_level": fundamental.debt_level,
        "profit_margin_strength": fundamental.profit_margin_strength,
        "updated_at": fundamental.updated_at
    }

def get_recent_alerts(ticker, days=30):
    """Get recent alerts for a stock"""
    cutoff_date = datetime.utcnow().date() - timedelta(days=days)

    alerts = Alert.query.filter(
        Alert.ticker == ticker.upper(),
        Alert.date >= cutoff_date
    ).order_by(Alert.date.desc()).all()

    return alerts

def get_stock_volatility(ticker):
    """
    Get stock volatility score from most recent alert

    Returns:
        float or None: Volatility score (0-12 scale typically)
    """
    alert = Alert.query.filter_by(ticker=ticker.upper())\
        .order_by(Alert.date.desc())\
        .first()

    if alert and alert.volatility_score:
        return float(alert.volatility_score)

    return None

def get_ai_stock_analysis(ticker, user_risk_profile='moderate', use_api=False):
    """
    Get AI-generated stock analysis

    Args:
        ticker (str): Stock ticker symbol
        user_risk_profile (str): User's risk profile (conservative/moderate/aggressive)
        use_api (bool): Use external API for stock data

    Returns:
        str: AI analysis text for display
    """
    ticker = ticker.upper()

    # Get stock data (database or API)
    metadata = get_stock_metadata(ticker, use_api=use_api)
    fundamental = get_stock_fundamentals(ticker)
    volatility = get_stock_volatility(ticker)

    if not metadata or metadata.get("name") == ticker:
        return f"Stock {ticker} not found in database or API. Please check the ticker symbol."

    # Check if AI is configured
    try:
        from ai_services import run_stock_analysis, is_ai_configured

        if not is_ai_configured():
            return "⚠️ AI service not configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable to enable AI analysis."

        # Prepare metrics for AI
        metrics = {
            "price": metadata["price"],
            "sector": metadata["sector"],
            "market_cap": metadata["market_cap"],
            "pe_ratio": metadata["pe_ratio"],
            "revenue_trend": fundamental.get("revenue_trend", "unknown") if fundamental else "unknown",
            "net_income_trend": fundamental.get("net_income_trend", "unknown") if fundamental else "unknown",
            "debt_level": fundamental.get("debt_level", "unknown") if fundamental else "unknown",
            "profit_margin_strength": fundamental.get("profit_margin_strength", "unknown") if fundamental else "unknown",
            "volatility": volatility or "medium",
            "user_risk_profile": user_risk_profile
        }

        # Call AI service
        analysis = run_stock_analysis(ticker, metadata["name"], metrics)

        # Return the analysis text directly
        return analysis if isinstance(analysis, str) else str(analysis)

    except ImportError:
        # AI services not available - return placeholder with stock data
        price_text = f"${metadata['price']:.2f}" if metadata['price'] else "N/A"
        pe_text = f"{metadata['pe_ratio']:.2f}" if metadata['pe_ratio'] else "N/A"

        return f"""Stock Analysis for {ticker} ({metadata['name']}):

📊 Current Data:
• Price: {price_text}
• Sector: {metadata['sector']}
• P/E Ratio: {pe_text}
• Volatility: {volatility or 'Medium'}

🎯 Risk Profile: {user_risk_profile.capitalize()}

ℹ️ AI-powered insights require configuration of ai_services.py module."""

    except Exception as e:
        return f"Unable to generate AI analysis at this time. Error: {str(e)}"

def screen_stocks_by_sector(sector):
    """Get all stocks in a specific sector"""
    stocks = Stock.query.filter_by(sector=sector).all()
    return stocks

def screen_stocks_by_criteria(
    min_price=None,
    max_price=None,
    sector=None,
    min_market_cap=None,
    max_pe_ratio=None
):
    """
    Screen stocks by multiple criteria

    Args:
        min_price (float): Minimum stock price
        max_price (float): Maximum stock price
        sector (str): Sector filter
        min_market_cap (float): Minimum market cap
        max_pe_ratio (float): Maximum P/E ratio

    Returns:
        list: Filtered Stock instances
    """
    query = Stock.query

    if min_price is not None:
        query = query.filter(Stock.price >= min_price)

    if max_price is not None:
        query = query.filter(Stock.price <= max_price)

    if sector:
        query = query.filter(Stock.sector == sector)

    if min_market_cap is not None:
        query = query.filter(Stock.market_cap >= min_market_cap)

    if max_pe_ratio is not None:
        query = query.filter(Stock.pe_ratio <= max_pe_ratio)

    return query.all()

def get_top_alerts(days=7, limit=10):
    """
    Get top market alerts by volatility

    Args:
        days (int): Number of days to look back
        limit (int): Maximum number of alerts

    Returns:
        list: Alert instances ordered by volatility desc
    """
    cutoff_date = datetime.utcnow().date() - timedelta(days=days)

    alerts = Alert.query.filter(Alert.date >= cutoff_date)\
        .order_by(Alert.volatility_score.desc())\
        .limit(limit)\
        .all()

    return alerts

def get_day_trade_candidates(limit=3):
    """
    Get AI-generated day trade ideas

    Args:
        limit (int): Number of candidates to return

    Returns:
        dict: Day trade candidates with analysis
    """
    # Get recent high-volatility alerts
    alerts = get_top_alerts(days=1, limit=limit)

    if not alerts:
        return {
            "candidates": [],
            "message": "No high-volatility alerts in past 24 hours"
        }

    # Load AI prompt template
    prompt_template = ai_prompts.load_prompt('day_trade_ideas')

    # Prepare candidate data
    candidates = []
    for alert in alerts:
        stock = Stock.query.filter_by(ticker=alert.ticker).first()
        fundamental = get_stock_fundamentals(alert.ticker)

        candidates.append({
            "ticker": alert.ticker,
            "price": float(stock.price) if (stock and stock.price) else 0.0,
            "volatility_score": float(alert.volatility_score),
            "volume_vs_avg": float(alert.volume_vs_avg) if alert.volume_vs_avg else None,
            "reason": alert.reason_summary,
            "tags": alert.tags,
            "fundamentals": fundamental
        })

    # TODO: Replace with actual AI API call
    return {
        "candidates": candidates,
        "analysis_pending": True,
        "prompt_template": prompt_template,
        "message": "Day trade analysis pending - integrate OpenAI/Anthropic API"
    }
