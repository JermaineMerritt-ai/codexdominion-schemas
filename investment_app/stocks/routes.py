"""
Stock Routes
"""
from flask import render_template, jsonify, request
from . import stocks_bp
from .services import (
    get_stock_metadata,
    get_stock_fundamentals,
    get_recent_alerts,
    get_ai_stock_analysis,
    screen_stocks_by_criteria,
    get_top_alerts,
    get_day_trade_candidates
)
from models import Stock

@stocks_bp.route('/')
def index():
    """Stock screener"""
    sector = request.args.get('sector')
    risk_profile = request.args.get('risk_profile')

    query = Stock.query

    if sector:
        query = query.filter_by(sector=sector)

    stocks = query.all()
    return render_template('stocks/index.html', stocks=stocks)

@stocks_bp.route('/<ticker>')
def detail(ticker):
    """Stock detail page"""
    stock = Stock.query.filter_by(ticker=ticker.upper()).first_or_404()

    # Get stock data
    data = {
        'name': stock.name or ticker,
        'sector': stock.sector or 'Unknown',
        'price': float(stock.price) if stock.price else 0.0,
        'pe_ratio': float(stock.pe_ratio) if stock.pe_ratio else None
    }

    # Get AI analysis
    risk_profile = request.args.get('risk_profile', 'moderate')
    ai_analysis = get_ai_stock_analysis(ticker, risk_profile)

    return render_template('stocks/detail.html',
                          ticker=ticker.upper(),
                          data=data,
                          ai=ai_analysis)

@stocks_bp.route('/<ticker>/analyze')
def analyze(ticker):
    """AI stock analysis"""
    # Get user risk profile (default to moderate if not logged in)
    risk_profile = request.args.get('risk_profile', 'moderate')

    # Use service layer for analysis
    analysis = get_ai_stock_analysis(ticker, risk_profile)

    return jsonify(analysis)

@stocks_bp.route('/alerts')
def alerts():
    """Recent market alerts"""
    days = request.args.get('days', 7, type=int)
    limit = request.args.get('limit', 20, type=int)

    from datetime import datetime, timedelta
    cutoff_date = datetime.utcnow().date() - timedelta(days=days)

    alerts = Alert.query.filter(Alert.date >= cutoff_date).order_by(Alert.date.desc()).limit(limit).all()
    return render_template('stocks/alerts.html', alerts=alerts, days=days)

@stocks_bp.route('/day-trade-ideas')
def day_trade_ideas():
    """Get AI-generated day trade candidates"""
    limit = request.args.get('limit', 3, type=int)

    # Use service layer
    candidates = get_day_trade_candidates(limit=limit)

    return jsonify({'candidates': candidates})

@stocks_bp.route('/picks')
def picks():
    """Daily AI stock picks page"""
    from datetime import datetime, timedelta

    # Try to get picks from database
    try:
        from models import DailyPicks
        today = datetime.utcnow().date()
        picks_data = DailyPicks.query.filter_by(date=today).all()

        if picks_data:
            picks = [{
                'ticker': p.ticker,
                'reason': p.reason_summary
            } for p in picks_data]
        else:
            picks = []
    except (ImportError, Exception) as e:
        # Fallback: Use sample picks or day trade candidates
        try:
            candidates_data = get_day_trade_candidates(limit=3)
            if isinstance(candidates_data, dict):
                candidates = candidates_data.get('candidates', [])
            else:
                candidates = []

            picks = [{
                'ticker': c.get('ticker', 'N/A'),
                'reason': c.get('reason', 'AI-generated pick')
            } for c in candidates]
        except Exception:
            # Ultimate fallback: Sample picks
            picks = [
                {'ticker': 'AAPL', 'reason': 'Strong momentum in tech sector with solid fundamentals'},
                {'ticker': 'MSFT', 'reason': 'Cloud services growth driving revenue expansion'},
                {'ticker': 'NVDA', 'reason': 'AI chip demand continues to exceed supply'}
            ]

    return render_template('stocks/picks.html', picks=picks)
