"""
Stock services - Business logic for stock analysis and picks
"""

from flask import current_app
from typing import List, Dict, Any, Optional
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import StockAnalysis, TradingPick, LedgerManager

class StockService:
    """Service for stock operations"""

    def get_all_analyses(self) -> List[StockAnalysis]:
        """Get all stock analyses"""
        filepath = current_app.config['STOCK_ANALYSIS_FILE']
        data = LedgerManager.load_json(filepath)

        analyses = []
        for a_data in data.get('analyses', []):
            analyses.append(StockAnalysis(a_data))

        return analyses

    def get_analysis(self, ticker: str) -> Optional[StockAnalysis]:
        """Get analysis for specific ticker"""
        analyses = self.get_all_analyses()
        for analysis in analyses:
            if analysis.ticker == ticker.upper():
                return analysis
        return None

    def get_trading_picks(self) -> List[TradingPick]:
        """Get all trading picks"""
        filepath = current_app.config['TRADING_PICKS_FILE']
        data = LedgerManager.load_json(filepath)

        picks = []
        for p_data in data.get('picks', []):
            picks.append(TradingPick(p_data))

        return sorted(picks, key=lambda x: x.date, reverse=True)

    def get_active_picks(self) -> List[TradingPick]:
        """Get only active trading picks"""
        all_picks = self.get_trading_picks()
        return [p for p in all_picks if p.status == 'active']

    def get_picks_performance(self) -> Dict[str, Any]:
        """Calculate trading picks performance"""
        picks = self.get_trading_picks()

        total_picks = len(picks)
        active = len([p for p in picks if p.status == 'active'])
        hit_target = len([p for p in picks if p.status == 'hit_target'])
        stopped_out = len([p for p in picks if p.status == 'stopped_out'])
        expired = len([p for p in picks if p.status == 'expired'])

        completed = hit_target + stopped_out + expired
        win_rate = (hit_target / completed * 100) if completed > 0 else 0

        return {
            'total_picks': total_picks,
            'active': active,
            'completed': completed,
            'hit_target': hit_target,
            'stopped_out': stopped_out,
            'expired': expired,
            'win_rate': round(win_rate, 1)
        }

    def update_pick_status(self, pick_id: int, status: str, result: Optional[Dict[str, Any]] = None) -> bool:
        """Update pick status"""
        filepath = current_app.config['TRADING_PICKS_FILE']
        data = LedgerManager.load_json(filepath)

        for pick in data.get('picks', []):
            if pick['id'] == pick_id:
                pick['status'] = status
                pick['updated_at'] = datetime.utcnow().isoformat() + 'Z'
                if result:
                    pick['result'] = result

                LedgerManager.save_json(filepath, data)
                return True

        return False
