"""
Stock Search API Endpoint
=========================
Symbol search for adding holdings to portfolio
"""

from flask import Blueprint, request, jsonify
import requests
import os

stock_search_bp = Blueprint('stock_search', __name__, url_prefix='/api/stocks')

# Use Alpha Vantage API (free tier available)
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")


@stock_search_bp.route('/search', methods=['GET'])
def search_stocks():
    """
    Search for stock symbols by query string.
    Example: /api/stocks/search?q=AAPL
    """
    query = request.args.get('q', '').strip().upper()
    
    if len(query) < 1:
        return jsonify({"results": []}), 200
    
    if len(query) > 10:
        return jsonify({"error": "Query too long"}), 400
    
    try:
        # Use Alpha Vantage SYMBOL_SEARCH endpoint
        url = f"https://www.alphavantage.co/query"
        params = {
            "function": "SYMBOL_SEARCH",
            "keywords": query,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        # Extract results
        matches = data.get("bestMatches", [])
        results = []
        
        for match in matches[:10]:  # Limit to top 10
            results.append({
                "symbol": match.get("1. symbol", ""),
                "name": match.get("2. name", ""),
                "type": match.get("3. type", ""),
                "region": match.get("4. region", ""),
                "currency": match.get("8. currency", "USD")
            })
        
        return jsonify({"results": results}), 200
        
    except requests.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500
