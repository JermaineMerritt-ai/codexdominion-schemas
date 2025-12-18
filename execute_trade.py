"""
Trade Execution System - Add holdings to portfolios
"""
import json
from datetime import datetime

PORTFOLIO_LEDGER = "portfolios.json"

def load_portfolios():
    """Load portfolio ledger"""
    with open(PORTFOLIO_LEDGER, "r") as f:
        return json.load(f)

def save_portfolios(data):
    """Save portfolio ledger with timestamp"""
    data["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open(PORTFOLIO_LEDGER, "w") as f:
        json.dump(data, f, indent=2)

def execute_trade(portfolio_id, trade):
    """Execute a trade and update portfolio"""
    data = load_portfolios()

    ticker = trade["ticker"]
    trade_type = trade["trade_type"]
    shares = trade["shares"]
    price = trade["price"]
    fees = trade.get("fees", 0)
    sector = trade.get("sector", get_sector(ticker))

    # Find portfolio
    for i, portfolio in enumerate(data["portfolios"]):
        if portfolio["id"] == portfolio_id:
            holdings = portfolio.get("holdings", [])

            if trade_type == "buy":
                # Check if holding exists
                existing = None
                for h in holdings:
                    if h["ticker"] == ticker:
                        existing = h
                        break

                if existing:
                    # Average up
                    total_shares = existing["shares"] + shares
                    total_cost = (existing["shares"] * existing["purchase_price"]) + (shares * price)
                    new_avg_price = total_cost / total_shares

                    existing["shares"] = total_shares
                    existing["purchase_price"] = round(new_avg_price, 2)
                    existing["price"] = price
                    existing["value"] = round(total_shares * price, 2)

                    print(f"📈 Averaged up {ticker}: {shares} shares @ ${price:.2f}")
                    print(f"   New position: {total_shares} shares @ ${new_avg_price:.2f} avg")
                else:
                    # New position
                    new_holding = {
                        "ticker": ticker,
                        "shares": shares,
                        "price": price,
                        "value": round(shares * price, 2),
                        "purchase_price": price,
                        "purchase_date": datetime.utcnow().isoformat() + "Z",
                        "gain_loss": 0,
                        "gain_loss_pct": 0,
                        "sector": sector
                    }
                    holdings.append(new_holding)
                    print(f"✅ Bought {shares} shares of {ticker} @ ${price:.2f}")

            elif trade_type == "sell":
                # Find and reduce/remove position
                for h in holdings:
                    if h["ticker"] == ticker:
                        if h["shares"] <= shares:
                            holdings.remove(h)
                            print(f"✅ Sold entire {ticker} position: {h['shares']} shares @ ${price:.2f}")
                        else:
                            h["shares"] -= shares
                            h["value"] = round(h["shares"] * price, 2)
                            h["price"] = price
                            print(f"✅ Sold {shares} shares of {ticker} @ ${price:.2f}")
                            print(f"   Remaining: {h['shares']} shares")
                        break

            # Recalculate portfolio
            portfolio["holdings"] = holdings
            total_value = sum(h["value"] for h in holdings)

            # Calculate weights
            for h in holdings:
                h["weight"] = round((h["value"] / total_value * 100) if total_value > 0 else 0, 2)

                # Update gain/loss
                cost_basis = h["shares"] * h["purchase_price"]
                h["gain_loss"] = round(h["value"] - cost_basis, 2)
                h["gain_loss_pct"] = round((h["gain_loss"] / cost_basis * 100) if cost_basis > 0 else 0, 2)

            # Sector breakdown
            sector_totals = {}
            for h in holdings:
                s = h.get("sector", "Other")
                sector_totals[s] = sector_totals.get(s, 0) + h["value"]

            portfolio["sector_breakdown"] = {
                sector: round((value / total_value * 100), 2)
                for sector, value in sector_totals.items()
            } if total_value > 0 else {}

            # Performance
            total_cost = sum(h["shares"] * h["purchase_price"] for h in holdings)
            total_gain_loss = total_value - total_cost

            portfolio["performance"] = {
                "total_gain_loss": round(total_gain_loss, 2),
                "total_gain_loss_pct": round((total_gain_loss / total_cost * 100) if total_cost > 0 else 0, 2),
                "daily_change": 0,  # Would need historical data
                "daily_change_pct": 0
            }

            portfolio["total_value"] = round(total_value, 2)
            portfolio["updated_at"] = datetime.utcnow().isoformat() + "Z"

            data["portfolios"][i] = portfolio
            save_portfolios(data)

            print(f"\n💰 Portfolio #{portfolio_id} Updated:")
            print(f"   Total Value: ${total_value:,.2f}")
            print(f"   Total Gain/Loss: ${total_gain_loss:,.2f} ({portfolio['performance']['total_gain_loss_pct']:.2f}%)")
            print(f"   Holdings: {len(holdings)} positions")

            return portfolio

    print(f"❌ Portfolio #{portfolio_id} not found")
    return None

def get_sector(ticker):
    """Map ticker to sector (simplified)"""
    sector_map = {
        "AAPL": "Technology",
        "MSFT": "Technology",
        "GOOGL": "Technology",
        "AMZN": "Consumer",
        "TSLA": "Consumer",
        "NVDA": "Technology",
        "META": "Technology",
        "JPM": "Financials",
        "V": "Financials",
        "WMT": "Consumer",
        "PG": "Consumer",
        "JNJ": "Healthcare",
        "UNH": "Healthcare",
        "XOM": "Energy",
        "CVX": "Energy"
    }
    return sector_map.get(ticker, "Other")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Command line: python execute_trade.py 7 AAPL buy 5 180.50
        try:
            portfolio_id = int(sys.argv[1])
            ticker = sys.argv[2]
            trade_type = sys.argv[3].lower()
            shares = int(sys.argv[4])
            price = float(sys.argv[5])

            trade = {
                "ticker": ticker,
                "trade_type": trade_type,
                "shares": shares,
                "price": price,
                "fees": 0
            }

            print(f"\n🔥 Executing {trade_type.upper()} trade 👑")
            print(f"   {ticker}: {shares} shares @ ${price:.2f}\n")

            execute_trade(portfolio_id, trade)
        except (ValueError, IndexError):
            print("Usage: python execute_trade.py <portfolio_id> <ticker> <buy|sell> <shares> <price>")
    else:
        # Default: Execute the AAPL trade
        trade = {
            "ticker": "AAPL",
            "trade_type": "buy",
            "shares": 5,
            "price": 180.50,
            "fees": 0
        }

        print("\n🔥 Executing BUY trade 👑")
        print(f"   AAPL: 5 shares @ $180.50\n")

        execute_trade(7, trade)

        # Display updated portfolio
        print("\n" + "="*60)
        import view_portfolio
        view_portfolio.display_portfolio(7)
