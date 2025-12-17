"""
Portfolio services - Business logic for portfolio operations
"""

from flask import current_app
from typing import List, Dict, Any, Optional
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Portfolio, LedgerManager

class PortfolioService:
    """Service for portfolio operations"""

    def get_all_portfolios(self) -> List[Portfolio]:
        """Get all portfolios"""
        filepath = current_app.config['PORTFOLIOS_FILE']
        data = LedgerManager.load_json(filepath)

        portfolios = []
        for p_data in data.get('portfolios', []):
            portfolios.append(Portfolio(p_data))

        return portfolios

    def get_portfolio(self, portfolio_id: int) -> Optional[Portfolio]:
        """Get portfolio by ID"""
        portfolios = self.get_all_portfolios()
        for portfolio in portfolios:
            if portfolio.id == portfolio_id:
                return portfolio
        return None

    def create_portfolio(self, portfolio_data: Dict[str, Any]) -> Portfolio:
        """Create new portfolio"""
        filepath = current_app.config['PORTFOLIOS_FILE']
        data = LedgerManager.load_json(filepath)

        if 'portfolios' not in data:
            data['portfolios'] = []

        # Generate ID
        portfolio_id = max([p['id'] for p in data['portfolios']], default=0) + 1

        # Create portfolio
        now = datetime.utcnow().isoformat() + 'Z'
        portfolio = {
            'id': portfolio_id,
            'user_id': portfolio_data.get('user_id', 1),
            'name': portfolio_data.get('name', f'Portfolio {portfolio_id}'),
            'risk_profile': portfolio_data.get('risk_profile', 'moderate'),
            'holdings': [],
            'total_value': 0.0,
            'sector_breakdown': {},
            'performance': {
                'total_gain_loss': 0.0,
                'total_return_pct': 0.0,
                'daily_change': 0.0,
                'daily_change_pct': 0.0
            },
            'created_at': now,
            'updated_at': now
        }

        data['portfolios'].append(portfolio)
        LedgerManager.save_json(filepath, data)

        return Portfolio(portfolio)

    def execute_trade(self, portfolio_id: int, trade_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute buy/sell trade"""
        filepath = current_app.config['PORTFOLIOS_FILE']
        data = LedgerManager.load_json(filepath)

        # Find portfolio
        portfolio = None
        for p in data.get('portfolios', []):
            if p['id'] == portfolio_id:
                portfolio = p
                break

        if not portfolio:
            return {"success": False, "error": "Portfolio not found"}

        action = trade_data.get('action')  # 'buy' or 'sell'
        ticker = trade_data.get('ticker')
        shares = trade_data.get('shares')
        price = trade_data.get('price')
        sector = trade_data.get('sector', 'Other')

        if action == 'buy':
            # Find existing holding
            holding = None
            for h in portfolio['holdings']:
                if h['ticker'] == ticker:
                    holding = h
                    break

            if holding:
                # Average up
                total_shares = holding['shares'] + shares
                total_cost = (holding['shares'] * holding['purchase_price']) + (shares * price)
                holding['shares'] = total_shares
                holding['purchase_price'] = total_cost / total_shares
                holding['current_price'] = price
                holding['current_value'] = total_shares * price
                holding['cost_basis'] = total_cost
                holding['gain_loss'] = holding['current_value'] - total_cost
                holding['gain_loss_pct'] = (holding['gain_loss'] / total_cost) * 100
            else:
                # New holding
                cost = shares * price
                holding = {
                    'ticker': ticker,
                    'shares': shares,
                    'purchase_price': price,
                    'current_price': price,
                    'cost_basis': cost,
                    'current_value': cost,
                    'gain_loss': 0.0,
                    'gain_loss_pct': 0.0,
                    'sector': sector,
                    'weight': 0.0
                }
                portfolio['holdings'].append(holding)

        elif action == 'sell':
            # Find holding
            holding = None
            for h in portfolio['holdings']:
                if h['ticker'] == ticker:
                    holding = h
                    break

            if not holding:
                return {"success": False, "error": f"No holding found for {ticker}"}

            if shares > holding['shares']:
                return {"success": False, "error": "Insufficient shares"}

            if shares == holding['shares']:
                # Full sale - remove holding
                portfolio['holdings'].remove(holding)
            else:
                # Partial sale
                holding['shares'] -= shares
                holding['cost_basis'] = holding['shares'] * holding['purchase_price']
                holding['current_value'] = holding['shares'] * holding['current_price']
                holding['gain_loss'] = holding['current_value'] - holding['cost_basis']
                holding['gain_loss_pct'] = (holding['gain_loss'] / holding['cost_basis']) * 100 if holding['cost_basis'] > 0 else 0

        # Recalculate portfolio
        self._recalculate_portfolio(portfolio)

        # Update timestamp
        portfolio['updated_at'] = datetime.utcnow().isoformat() + 'Z'

        # Save
        LedgerManager.save_json(filepath, data)

        return {
            "success": True,
            "message": f"{action.title()} trade executed successfully",
            "portfolio": Portfolio(portfolio).to_dict()
        }

    def update_stock_price(self, portfolio_id: int, ticker: str, price_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update stock price in portfolio"""
        filepath = current_app.config['PORTFOLIOS_FILE']
        data = LedgerManager.load_json(filepath)

        # Find portfolio
        portfolio = None
        for p in data.get('portfolios', []):
            if p['id'] == portfolio_id:
                portfolio = p
                break

        if not portfolio:
            return {"success": False, "error": "Portfolio not found"}

        # Find holding
        holding = None
        for h in portfolio['holdings']:
            if h['ticker'] == ticker:
                holding = h
                break

        if not holding:
            return {"success": False, "error": f"No holding found for {ticker}"}

        # Update price
        new_price = price_data.get('price')
        holding['current_price'] = new_price
        holding['current_value'] = holding['shares'] * new_price
        holding['gain_loss'] = holding['current_value'] - holding['cost_basis']
        holding['gain_loss_pct'] = (holding['gain_loss'] / holding['cost_basis']) * 100 if holding['cost_basis'] > 0 else 0

        # Recalculate portfolio
        self._recalculate_portfolio(portfolio)

        # Update timestamp
        portfolio['updated_at'] = datetime.utcnow().isoformat() + 'Z'

        # Save
        LedgerManager.save_json(filepath, data)

        return {
            "success": True,
            "message": f"Price updated for {ticker}",
            "portfolio": Portfolio(portfolio).to_dict()
        }

    def _recalculate_portfolio(self, portfolio: Dict[str, Any]) -> None:
        """Recalculate portfolio totals and weights"""
        holdings = portfolio['holdings']

        # Calculate total value
        total_value = sum(h['current_value'] for h in holdings)
        portfolio['total_value'] = total_value

        # Calculate weights
        for holding in holdings:
            holding['weight'] = (holding['current_value'] / total_value * 100) if total_value > 0 else 0

        # Calculate sector breakdown
        sector_breakdown = {}
        for holding in holdings:
            sector = holding.get('sector', 'Other')
            sector_breakdown[sector] = sector_breakdown.get(sector, 0) + holding['weight']
        portfolio['sector_breakdown'] = sector_breakdown

        # Calculate performance
        total_cost = sum(h['cost_basis'] for h in holdings)
        total_gain_loss = total_value - total_cost
        total_return_pct = (total_gain_loss / total_cost * 100) if total_cost > 0 else 0

        portfolio['performance'] = {
            'total_gain_loss': total_gain_loss,
            'total_return_pct': total_return_pct,
            'daily_change': 0.0,  # Would need historical data
            'daily_change_pct': 0.0
        }

    def get_performance(self, portfolio_id: int) -> Optional[Dict[str, Any]]:
        """Get portfolio performance"""
        portfolio = self.get_portfolio(portfolio_id)
        if portfolio:
            return portfolio.performance
        return None

    def get_portfolio_analysis(self, portfolio_id: int) -> Dict[str, Any]:
        """Get stock analysis for portfolio holdings"""
        from flask import current_app
        filepath = current_app.config['STOCK_ANALYSIS_FILE']
        data = LedgerManager.load_json(filepath)

        portfolio = self.get_portfolio(portfolio_id)
        if not portfolio:
            return {}

        analysis = {}
        for holding in portfolio.holdings:
            ticker = holding['ticker']
            for a in data.get('analyses', []):
                if a['ticker'] == ticker:
                    analysis[ticker] = a
                    break

        return analysis

    def get_portfolio_insights(self, portfolio_id: int) -> Optional[Dict[str, Any]]:
        """Get AI insights for portfolio"""
        from flask import current_app
        filepath = current_app.config['PORTFOLIO_INSIGHTS_FILE']
        data = LedgerManager.load_json(filepath)

        for insight in data.get('insights', []):
            if insight.get('portfolio_id') == portfolio_id:
                return insight

        return None
