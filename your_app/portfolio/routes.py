"""
Portfolio routes
"""

from flask import render_template, request, jsonify, current_app, flash, redirect, url_for
import sys
import os

# Import blueprint and service
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from portfolio import portfolio_bp
from portfolio.services import PortfolioService

portfolio_service = PortfolioService()

@portfolio_bp.route('/dashboard')
def dashboard():
    """Portfolio dashboard"""
    portfolios = portfolio_service.get_all_portfolios()
    return render_template('portfolio/dashboard.html', portfolios=portfolios)

@portfolio_bp.route('/<int:portfolio_id>')
def view_portfolio(portfolio_id):
    """View specific portfolio"""
    portfolio = portfolio_service.get_portfolio(portfolio_id)
    if not portfolio:
        flash('Portfolio not found', 'error')
        return redirect(url_for('portfolio.dashboard'))

    # Get analysis and insights
    analysis = portfolio_service.get_portfolio_analysis(portfolio_id)
    insights = portfolio_service.get_portfolio_insights(portfolio_id)

    return render_template(
        'portfolio/view.html',
        portfolio=portfolio,
        analysis=analysis,
        insights=insights
    )

@portfolio_bp.route('/create', methods=['GET', 'POST'])
def create_portfolio():
    """Create new portfolio"""
    if request.method == 'POST':
        data = request.form.to_dict()
        portfolio = portfolio_service.create_portfolio(data)
        flash(f'Portfolio "{portfolio.name}" created successfully! 🔥', 'success')
        return redirect(url_for('portfolio.view_portfolio', portfolio_id=portfolio.id))

    return render_template('portfolio/create.html')

@portfolio_bp.route('/<int:portfolio_id>/trade', methods=['POST'])
def execute_trade(portfolio_id):
    """Execute trade"""
    trade_data = request.get_json()

    result = portfolio_service.execute_trade(portfolio_id, trade_data)

    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 400

@portfolio_bp.route('/<int:portfolio_id>/update-price', methods=['POST'])
def update_price(portfolio_id):
    """Update stock price"""
    data = request.get_json()
    ticker = data.get('ticker')
    price_data = data.get('price_data')

    result = portfolio_service.update_stock_price(portfolio_id, ticker, price_data)

    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 400

# API Routes
@portfolio_bp.route('/api/portfolios')
def api_get_portfolios():
    """Get all portfolios (API)"""
    portfolios = portfolio_service.get_all_portfolios()
    return jsonify([p.to_dict() for p in portfolios])

@portfolio_bp.route('/api/portfolios/<int:portfolio_id>')
def api_get_portfolio(portfolio_id):
    """Get portfolio by ID (API)"""
    portfolio = portfolio_service.get_portfolio(portfolio_id)
    if portfolio:
        return jsonify(portfolio.to_dict())
    else:
        return jsonify({"error": "Portfolio not found"}), 404

@portfolio_bp.route('/api/portfolios/<int:portfolio_id>/performance')
def api_get_performance(portfolio_id):
    """Get portfolio performance (API)"""
    performance = portfolio_service.get_performance(portfolio_id)
    if performance:
        return jsonify(performance)
    else:
        return jsonify({"error": "Portfolio not found"}), 404
