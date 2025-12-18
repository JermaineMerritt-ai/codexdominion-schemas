"""
Portfolio Routes
"""
from flask import render_template, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import portfolio_bp
from .services import (
    compute_portfolio_summary,
    get_ai_portfolio_insights,
    create_default_portfolio
)
from models import Portfolio, Trade

@portfolio_bp.route('/')
@login_required
def index():
    """Portfolio dashboard"""
    portfolios = current_user.portfolios.all()
    return render_template('portfolio/index.html', portfolios=portfolios)

@portfolio_bp.route('/<int:portfolio_id>')
@login_required
def view(portfolio_id):
    """View specific portfolio"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)

    if portfolio.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    holdings = portfolio.holdings.all()

    # Calculate portfolio summary with total value and weighted holdings
    summary = compute_portfolio_summary(portfolio)

    # Generate AI insights for portfolio analysis
    ai_insights = get_ai_portfolio_insights(portfolio)

    return render_template(
        'portfolio/view.html',
        portfolio=portfolio,
        holdings=holdings,
        summary=summary,
        ai_insights=ai_insights
    )

@portfolio_bp.route('/<int:portfolio_id>/analyze')
@login_required
def analyze(portfolio_id):
    """AI portfolio analysis"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)

    if portfolio.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    # Use service layer for analysis
    ai_insights = get_ai_portfolio_insights(portfolio)
    summary = compute_portfolio_summary(portfolio)

    return jsonify({
        'portfolio': {
            'name': portfolio.name,
            'risk_profile': portfolio.risk_profile,
            'summary': summary
        },
        'ai_insights': ai_insights
    })

@portfolio_bp.route('/<int:portfolio_id>/trades')
@login_required
def trades(portfolio_id):
    """View trade history"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)

    if portfolio.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    trades = portfolio.trades.order_by(Trade.trade_date.desc()).all()
    return render_template(
        'portfolio/trades.html',
        portfolio=portfolio,
        trades=trades
    )

@portfolio_bp.route('/create-default', methods=['POST'])
@login_required
def create_default():
    """Create default portfolio for new user"""
    risk = current_user.risk_profile
    portfolio = create_default_portfolio(current_user.id, risk)
    return redirect(url_for('portfolio.view', portfolio_id=portfolio.id) + '?first_run=1')
