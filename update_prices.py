"""
Stock Price Update System - Revalue portfolios with current market prices
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

def update_stock_price(ticker, market_data):
    """Update stock price across all portfolios and recalculate"""
    data = load_portfolios()

    new_price = market_data["price"]
    updated_portfolios = []

    print(f"\n🔥 Updating {ticker} to ${new_price:.2f} 👑")
    if "name" in market_data:
        print(f"   {market_data['name']}")
    if "sector" in market_data:
        print(f"   Sector: {market_data['sector']}")
    if "pe_ratio" in market_data:
        print(f"   P/E Ratio: {market_data['pe_ratio']}")
    if "market_cap" in market_data:
        print(f"   Market Cap: ${market_data['market_cap']:,.0f}")
    print()

    for i, portfolio in enumerate(data["portfolios"]):
        holdings = portfolio.get("holdings", [])
        portfolio_updated = False

        for h in holdings:
            if h["ticker"] == ticker:
                old_price = h["price"]
                old_value = h["value"]

                # Update price and value
                h["price"] = new_price
                h["value"] = round(h["shares"] * new_price, 2)

                # Update sector if provided
                if "sector" in market_data:
                    h["sector"] = market_data["sector"]

                # Recalculate gain/loss
                cost_basis = h["shares"] * h["purchase_price"]
                h["gain_loss"] = round(h["value"] - cost_basis, 2)
                h["gain_loss_pct"] = round((h["gain_loss"] / cost_basis * 100) if cost_basis > 0 else 0, 2)

                # Calculate daily change
                h["daily_change"] = round(h["value"] - old_value, 2)
                h["daily_change_pct"] = round((h["daily_change"] / old_value * 100) if old_value > 0 else 0, 2)

                portfolio_updated = True

                print(f"📊 Portfolio #{portfolio['id']}: {portfolio['name']}")
                print(f"   {ticker}: ${old_price:.2f} → ${new_price:.2f} ({h['daily_change_pct']:+.2f}%)")
                print(f"   Position Value: ${old_value:,.2f} → ${h['value']:,.2f} ({h['daily_change']:+.2f})")

        if portfolio_updated:
            # Recalculate portfolio totals
            total_value = sum(h["value"] for h in holdings)

            # Update weights
            for h in holdings:
                h["weight"] = round((h["value"] / total_value * 100) if total_value > 0 else 0, 2)

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
            daily_change = sum(h.get("daily_change", 0) for h in holdings)

            portfolio["performance"] = {
                "total_gain_loss": round(total_gain_loss, 2),
                "total_gain_loss_pct": round((total_gain_loss / total_cost * 100) if total_cost > 0 else 0, 2),
                "daily_change": round(daily_change, 2),
                "daily_change_pct": round((daily_change / (total_value - daily_change) * 100) if (total_value - daily_change) > 0 else 0, 2)
            }

            portfolio["total_value"] = round(total_value, 2)
            portfolio["updated_at"] = datetime.utcnow().isoformat() + "Z"

            data["portfolios"][i] = portfolio
            updated_portfolios.append(portfolio["id"])

            print(f"   Portfolio Total: ${total_value:,.2f}")
            print(f"   Total Gain/Loss: ${total_gain_loss:,.2f} ({portfolio['performance']['total_gain_loss_pct']:+.2f}%)")
            print(f"   Daily Change: ${daily_change:,.2f} ({portfolio['performance']['daily_change_pct']:+.2f}%)\n")

    if updated_portfolios:
        save_portfolios(data)
        print(f"✅ Updated {len(updated_portfolios)} portfolio(s): {updated_portfolios}")
    else:
        print(f"⚠️  No portfolios contain {ticker}")

    return updated_portfolios

def batch_update_prices(price_updates):
    """Update multiple stock prices at once"""
    print(f"\n🔥 Batch Price Update - {len(price_updates)} stocks 👑\n")

    all_updated = []
    for update in price_updates:
        ticker = update["ticker"]
        updated = update_stock_price(ticker, update)
        all_updated.extend(updated)

    print(f"\n✅ Batch update complete - {len(set(all_updated))} unique portfolio(s) updated")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Command line: python update_prices.py AAPL 182.12
        try:
            ticker = sys.argv[1]
            price = float(sys.argv[2])

            market_data = {
                "ticker": ticker,
                "price": price
            }

            # Optional additional parameters
            if len(sys.argv) > 3:
                market_data["sector"] = sys.argv[3]

            update_stock_price(ticker, market_data)

            # Show updated portfolio
            print("\n" + "="*60)
            import view_portfolio
            data = load_portfolios()
            for portfolio in data["portfolios"]:
                if any(h["ticker"] == ticker for h in portfolio.get("holdings", [])):
                    view_portfolio.display_portfolio(portfolio["id"])
        except (ValueError, IndexError) as e:
            print("Usage: python update_prices.py <ticker> <price> [sector]")
    else:
        # Default: Update AAPL with provided data
        market_data = {
            "ticker": "AAPL",
            "name": "Apple Inc.",
            "sector": "Technology",
            "price": 182.12,
            "pe_ratio": 29.4,
            "market_cap": 2800000000000
        }

        update_stock_price("AAPL", market_data)

        # Show updated portfolio
        print("\n" + "="*60)
        import view_portfolio
        view_portfolio.display_portfolio(7)
