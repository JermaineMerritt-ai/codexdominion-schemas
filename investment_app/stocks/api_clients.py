"""
External API Integrations
Wrappers for third-party stock market data APIs
"""
import os
import requests
from datetime import datetime

class StockAPIClient:
    """Base class for stock API clients"""

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('STOCK_API_KEY')

    def get_price(self, ticker):
        raise NotImplementedError

    def get_metadata(self, ticker):
        raise NotImplementedError

class PolygonClient(StockAPIClient):
    """Polygon.io API client"""

    BASE_URL = "https://api.polygon.io/v3"

    def get_price(self, ticker):
        """Get last trade price"""
        try:
            url = f"{self.BASE_URL}/last_trade/{ticker}?apiKey={self.api_key}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get("results", {}).get("price", 0)
        except Exception as e:
            print(f"Polygon get_price error for {ticker}: {e}")
            return None

    def get_metadata(self, ticker):
        """Get ticker details"""
        try:
            url = f"{self.BASE_URL}/reference/tickers/{ticker}?apiKey={self.api_key}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", {})

            return {
                "ticker": ticker,
                "name": results.get("name"),
                "sector": results.get("sic_description"),
                "market_cap": results.get("market_cap"),
                "pe_ratio": None,  # Polygon doesn't provide P/E in ticker details
                "description": results.get("description")
            }
        except Exception as e:
            print(f"Polygon get_metadata error for {ticker}: {e}")
            return None

    def get_aggregates(self, ticker, days=30):
        """Get historical aggregates"""
        try:
            from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            to_date = datetime.now().strftime('%Y-%m-%d')

            url = f"{self.BASE_URL}/aggs/ticker/{ticker}/range/1/day/{from_date}/{to_date}?apiKey={self.api_key}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            return data.get("results", [])
        except Exception as e:
            print(f"Polygon get_aggregates error for {ticker}: {e}")
            return []

class AlphaVantageClient(StockAPIClient):
    """Alpha Vantage API client"""

    BASE_URL = "https://www.alphavantage.co/query"

    def get_price(self, ticker):
        """Get global quote price"""
        try:
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": ticker,
                "apikey": self.api_key
            }
            response = requests.get(self.BASE_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            price = data.get("Global Quote", {}).get("05. price")
            return float(price) if price else None
        except Exception as e:
            print(f"AlphaVantage get_price error for {ticker}: {e}")
            return None

    def get_metadata(self, ticker):
        """Get company overview"""
        try:
            params = {
                "function": "OVERVIEW",
                "symbol": ticker,
                "apikey": self.api_key
            }
            response = requests.get(self.BASE_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            if not data or "Symbol" not in data:
                return None

            return {
                "ticker": ticker,
                "name": data.get("Name"),
                "sector": data.get("Sector"),
                "market_cap": float(data.get("MarketCapitalization", 0)),
                "pe_ratio": float(data.get("PERatio")) if data.get("PERatio") != "None" else None,
                "description": data.get("Description"),
                "dividend_yield": float(data.get("DividendYield", 0)) * 100 if data.get("DividendYield") else None
            }
        except Exception as e:
            print(f"AlphaVantage get_metadata error for {ticker}: {e}")
            return None

    def get_time_series(self, ticker, outputsize='compact'):
        """Get daily time series"""
        try:
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": ticker,
                "apikey": self.api_key,
                "outputsize": outputsize  # 'compact' = 100 days, 'full' = 20+ years
            }
            response = requests.get(self.BASE_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            return data.get("Time Series (Daily)", {})
        except Exception as e:
            print(f"AlphaVantage get_time_series error for {ticker}: {e}")
            return {}

def get_api_client(provider=None):
    """
    Factory function to get appropriate API client

    Args:
        provider (str): 'polygon' or 'alphavantage'

    Returns:
        StockAPIClient: Configured API client instance
    """
    provider = provider or os.environ.get('STOCK_API_PROVIDER', 'database')

    if provider == 'polygon':
        return PolygonClient()
    elif provider == 'alphavantage':
        return AlphaVantageClient()
    else:
        return None

# Convenience functions
def fetch_from_api(ticker, provider=None):
    """
    Fetch stock data from external API

    Args:
        ticker (str): Stock ticker
        provider (str): API provider name

    Returns:
        dict: Combined price and metadata
    """
    client = get_api_client(provider)

    if not client:
        return {"error": "No API client configured"}

    price = client.get_price(ticker)
    metadata = client.get_metadata(ticker)

    if metadata:
        metadata["current_price"] = price

    return metadata or {"error": "Failed to fetch data"}
