"""
Data models and JSON ledger utilities
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class LedgerManager:
    """Base class for managing JSON ledgers"""

    @staticmethod
    def load_json(filepath: str) -> Dict[str, Any]:
        """Load JSON file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def save_json(filepath: str, data: Dict[str, Any]) -> None:
        """Save JSON file with metadata update"""
        if 'meta' not in data:
            data['meta'] = {}
        data['meta']['last_updated'] = datetime.utcnow().isoformat() + 'Z'

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

class Portfolio:
    """Portfolio model"""

    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.user_id = data.get('user_id')
        self.name = data.get('name')
        self.risk_profile = data.get('risk_profile')
        self.holdings = data.get('holdings', [])
        self.total_value = data.get('total_value', 0.0)
        self.sector_breakdown = data.get('sector_breakdown', {})
        self.performance = data.get('performance', {})
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'risk_profile': self.risk_profile,
            'holdings': self.holdings,
            'total_value': self.total_value,
            'sector_breakdown': self.sector_breakdown,
            'performance': self.performance,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def get_holding(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get specific holding by ticker"""
        for holding in self.holdings:
            if holding['ticker'] == ticker:
                return holding
        return None

    def add_holding(self, holding: Dict[str, Any]) -> None:
        """Add or update holding"""
        existing = self.get_holding(holding['ticker'])
        if existing:
            # Update existing
            idx = self.holdings.index(existing)
            self.holdings[idx] = holding
        else:
            # Add new
            self.holdings.append(holding)

class StockAnalysis:
    """Stock analysis model"""

    def __init__(self, data: Dict[str, Any]):
        self.ticker = data.get('ticker')
        self.analysis = data.get('analysis')
        self.recommendation = data.get('recommendation')
        self.target_price = data.get('target_price')
        self.analyst = data.get('analyst')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'ticker': self.ticker,
            'analysis': self.analysis,
            'recommendation': self.recommendation,
            'target_price': self.target_price,
            'analyst': self.analyst,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class TradingPick:
    """Trading pick model"""

    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.date = data.get('date')
        self.ticker = data.get('ticker')
        self.reason = data.get('reason')
        self.pick_type = data.get('pick_type')
        self.entry_price = data.get('entry_price')
        self.target_price = data.get('target_price')
        self.stop_loss = data.get('stop_loss')
        self.confidence = data.get('confidence')
        self.status = data.get('status', 'active')
        self.result = data.get('result')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'date': self.date,
            'ticker': self.ticker,
            'reason': self.reason,
            'pick_type': self.pick_type,
            'entry_price': self.entry_price,
            'target_price': self.target_price,
            'stop_loss': self.stop_loss,
            'confidence': self.confidence,
            'status': self.status,
            'result': self.result,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def calculate_upside(self) -> float:
        """Calculate upside percentage"""
        if self.entry_price and self.target_price:
            return ((self.target_price - self.entry_price) / self.entry_price) * 100
        return 0.0

class Subscriber:
    """Newsletter subscriber model"""

    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.email = data.get('email')
        self.risk_profile = data.get('risk_profile')
        self.segments = data.get('segments', [])
        self.preferences = data.get('preferences', {})
        self.status = data.get('status', 'active')
        self.subscribed_at = data.get('subscribed_at')
        self.unsubscribed_at = data.get('unsubscribed_at')

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'risk_profile': self.risk_profile,
            'segments': self.segments,
            'preferences': self.preferences,
            'status': self.status,
            'subscribed_at': self.subscribed_at,
            'unsubscribed_at': self.unsubscribed_at
        }
