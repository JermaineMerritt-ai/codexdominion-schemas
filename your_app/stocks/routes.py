"""
Stock routes - Analysis and trading picks
"""

from flask import render_template, request, jsonify, flash, redirect, url_for
import sys
import os

# Import blueprint and service
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from stocks import stocks_bp
from stocks.services import StockService

stock_service = StockService()

@stocks_bp.route('/analysis')
def analysis_list():
    """List all stock analyses"""
    analyses = stock_service.get_all_analyses()
    return render_template('stocks/analysis.html', analyses=analyses)

@stocks_bp.route('/analysis/<ticker>')
def view_analysis(ticker):
    """View analysis for specific stock"""
    analysis = stock_service.get_analysis(ticker)
    if not analysis:
        flash(f'No analysis found for {ticker}', 'warning')
        return redirect(url_for('stocks.analysis_list'))

    return render_template('stocks/view_analysis.html', analysis=analysis)

@stocks_bp.route('/picks')
def trading_picks():
    """View trading picks"""
    picks = stock_service.get_trading_picks()
    performance = stock_service.get_picks_performance()

    return render_template(
        'stocks/picks.html',
        picks=picks,
        performance=performance
    )

@stocks_bp.route('/picks/active')
def active_picks():
    """View only active trading picks"""
    picks = stock_service.get_active_picks()
    return render_template('stocks/active_picks.html', picks=picks)

# API Routes
@stocks_bp.route('/api/analysis')
def api_get_analyses():
    """Get all analyses (API)"""
    analyses = stock_service.get_all_analyses()
    return jsonify([a.to_dict() for a in analyses])

@stocks_bp.route('/api/analysis/<ticker>')
def api_get_analysis(ticker):
    """Get analysis for ticker (API)"""
    analysis = stock_service.get_analysis(ticker)
    if analysis:
        return jsonify(analysis.to_dict())
    else:
        return jsonify({"error": "Analysis not found"}), 404

@stocks_bp.route('/api/picks')
def api_get_picks():
    """Get all trading picks (API)"""
    picks = stock_service.get_trading_picks()
    return jsonify([p.to_dict() for p in picks])

@stocks_bp.route('/api/picks/active')
def api_get_active_picks():
    """Get active picks (API)"""
    picks = stock_service.get_active_picks()
    return jsonify([p.to_dict() for p in picks])

@stocks_bp.route('/api/picks/<int:pick_id>/update', methods=['POST'])
def api_update_pick(pick_id):
    """Update pick status (API)"""
    data = request.get_json()
    status = data.get('status')
    result = data.get('result')

    success = stock_service.update_pick_status(pick_id, status, result)

    if success:
        return jsonify({"success": True, "message": "Pick updated"})
    else:
        return jsonify({"success": False, "error": "Pick not found"}), 404
