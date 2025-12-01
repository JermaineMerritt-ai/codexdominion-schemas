"""
🔥 CODEX SIGNALS DATA FEEDS 📊
Market data integration and normalization

The Merritt Method™ - Real-time Financial Intelligence
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests

from .engine import MarketSnapshot


class DataFeedManager:
    """
    Unified market data feed manager supporting multiple sources
    """

    def __init__(self, config_file: str = "market_config.json"):
        self.config = self._load_config(config_file)
        self.logger = logging.getLogger(__name__)

    def _load_config(self, config_file: str) -> Dict:
        """Load market data configuration"""
        try:
            with open(config_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            # Default configuration
            return {
                "data_sources": {
                    "alpha_vantage": {"api_key": "", "enabled": False},
                    "yahoo_finance": {"enabled": True},
                    "coinbase": {"enabled": True},
                },
                "symbols": {
                    "stocks": ["MSFT", "AAPL", "GOOGL", "TSLA", "NVDA"],
                    "crypto": ["BTC-USD", "ETH-USD", "SOL-USD"],
                    "etfs": ["SPY", "QQQ", "VTI"],
                },
                "update_interval": 300,  # seconds
            }

    def fetch_yahoo_data(self, symbol: str) -> Optional[Dict]:
        """Fetch data from Yahoo Finance (free tier)"""
        try:
            # This would use yfinance library in production
            # For now, return mock data structure
            return {
                "symbol": symbol,
                "price": 420.50,
                "volume": 1000000,
                "volatility_30d": 0.25,
                "trend_20d": 0.35,
            }
        except Exception as e:
            self.logger.error(f"Yahoo Finance error for {symbol}: {e}")
            return None

    def fetch_coinbase_data(self, symbol: str) -> Optional[Dict]:
        """Fetch crypto data from Coinbase Pro"""
        try:
            # Mock Coinbase data
            return {
                "symbol": symbol,
                "price": 3500.0,
                "volume": 500000,
                "volatility_30d": 0.45,
                "trend_20d": 0.25,
            }
        except Exception as e:
            self.logger.error(f"Coinbase error for {symbol}: {e}")
            return None

    def calculate_volatility(self, prices: List[float]) -> float:
        """Calculate realized volatility from price history"""
        if len(prices) < 2:
            return 0.0

        returns = []
        for i in range(1, len(prices)):
            ret = (prices[i] - prices[i - 1]) / prices[i - 1]
            returns.append(ret)

        # Standard deviation of returns (annualized)
        import math

        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        volatility = math.sqrt(variance * 252)  # Annualize (252 trading days)

        return round(volatility, 4)

    def calculate_trend(self, prices: List[float]) -> float:
        """Calculate normalized trend score [-1, 1]"""
        if len(prices) < 2:
            return 0.0

        # Simple linear regression slope normalized
        n = len(prices)
        x_vals = list(range(n))

        x_mean = sum(x_vals) / n
        y_mean = sum(prices) / n

        numerator = sum((x_vals[i] - x_mean) * (prices[i] - y_mean) for i in range(n))
        denominator = sum((x_vals[i] - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return 0.0

        slope = numerator / denominator

        # Normalize to [-1, 1] range based on price magnitude
        price_range = max(prices) - min(prices)
        if price_range > 0:
            normalized_slope = slope * n / price_range
            # Clamp to [-1, 1]
            return max(-1.0, min(1.0, normalized_slope))

        return 0.0

    def get_liquidity_rank(self, symbol: str, volume: float) -> int:
        """Estimate liquidity rank based on volume and symbol type"""
        # Mock liquidity ranking - in production would use real market data
        high_liquidity = [
            "MSFT",
            "AAPL",
            "GOOGL",
            "TSLA",
            "SPY",
            "QQQ",
            "BTC-USD",
            "ETH-USD",
        ]
        medium_liquidity = ["NVDA", "AMD", "VTI", "SOL-USD"]

        if symbol in high_liquidity:
            return min(50, max(1, int(volume / 100000)))
        elif symbol in medium_liquidity:
            return min(100, max(51, int(volume / 50000)))
        else:
            return min(500, max(101, int(volume / 10000)))

    def create_market_snapshot(self, symbol: str) -> Optional[MarketSnapshot]:
        """Create MarketSnapshot from live data"""
        try:
            # Determine data source based on symbol
            if "-USD" in symbol:
                data = self.fetch_coinbase_data(symbol)
            else:
                data = self.fetch_yahoo_data(symbol)

            if not data:
                return None

            # In production, would fetch historical prices for calculations
            mock_prices = [data["price"] * (1 + i * 0.01) for i in range(-20, 1)]

            snapshot = MarketSnapshot(
                symbol=symbol,
                price=data["price"],
                vol_30d=self.calculate_volatility(mock_prices),
                trend_20d=self.calculate_trend(mock_prices),
                liquidity_rank=self.get_liquidity_rank(
                    symbol, data.get("volume", 100000)
                ),
            )

            return snapshot

        except Exception as e:
            self.logger.error(f"Error creating snapshot for {symbol}: {e}")
            return None

    def get_market_snapshots(self, symbols: List[str] = None) -> List[MarketSnapshot]:
        """Get market snapshots for multiple symbols"""
        if symbols is None:
            symbols = (
                self.config["symbols"]["stocks"]
                + self.config["symbols"]["crypto"]
                + self.config["symbols"]["etfs"]
            )

        snapshots = []
        for symbol in symbols:
            snapshot = self.create_market_snapshot(symbol)
            if snapshot:
                snapshots.append(snapshot)

        return snapshots


class MockDataFeed:
    """
    Mock data feed for testing and development
    """

    @staticmethod
    def get_mock_snapshots() -> List[MarketSnapshot]:
        """Generate realistic mock market snapshots"""
        return [
            MarketSnapshot(
                symbol="MSFT",
                price=420.1,
                vol_30d=0.22,
                trend_20d=0.48,
                liquidity_rank=5,
            ),
            MarketSnapshot(
                symbol="AAPL",
                price=195.3,
                vol_30d=0.28,
                trend_20d=0.15,
                liquidity_rank=3,
            ),
            MarketSnapshot(
                symbol="GOOGL",
                price=142.8,
                vol_30d=0.31,
                trend_20d=-0.05,
                liquidity_rank=8,
            ),
            MarketSnapshot(
                symbol="TSLA",
                price=248.5,
                vol_30d=0.52,
                trend_20d=0.25,
                liquidity_rank=12,
            ),
            MarketSnapshot(
                symbol="NVDA",
                price=145.2,
                vol_30d=0.45,
                trend_20d=0.65,
                liquidity_rank=15,
            ),
            MarketSnapshot(
                symbol="BTC-USD",
                price=43250.0,
                vol_30d=0.38,
                trend_20d=0.42,
                liquidity_rank=10,
            ),
            MarketSnapshot(
                symbol="ETH-USD",
                price=3500.0,
                vol_30d=0.40,
                trend_20d=0.30,
                liquidity_rank=15,
            ),
            MarketSnapshot(
                symbol="SOL-USD",
                price=215.0,
                vol_30d=0.65,
                trend_20d=0.55,
                liquidity_rank=35,
            ),
            MarketSnapshot(
                symbol="SPY",
                price=573.2,
                vol_30d=0.18,
                trend_20d=0.25,
                liquidity_rank=1,
            ),
            MarketSnapshot(
                symbol="QQQ",
                price=495.8,
                vol_30d=0.24,
                trend_20d=0.35,
                liquidity_rank=2,
            ),
        ]


if __name__ == "__main__":
    # Test the data feed
    feed_manager = DataFeedManager()
    snapshots = MockDataFeed.get_mock_snapshots()

    print("🔥 Codex Signals Data Feed Test 📊")
    print("=" * 40)

    for snapshot in snapshots[:3]:
        print(f"Symbol: {snapshot.symbol}")
        print(f"Price: ${snapshot.price:.2f}")
        print(f"30d Vol: {snapshot.vol_30d:.2f}")
        print(f"20d Trend: {snapshot.trend_20d:.2f}")
        print(f"Liquidity Rank: {snapshot.liquidity_rank}")
        print("-" * 30)
