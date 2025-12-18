"""
Direct Portfolio Viewer - Access portfolio data without API server
"""
import json
from datetime import datetime

PORTFOLIO_LEDGER = "portfolios.json"

def load_portfolios():
    """Load portfolio ledger"""
    with open(PORTFOLIO_LEDGER, "r") as f:
        return json.load(f)

def display_portfolio(portfolio_id):
    """Display complete portfolio details"""
    data = load_portfolios()

    for portfolio in data["portfolios"]:
        if portfolio["id"] == portfolio_id:
            print("\n" + "="*60)
            print(f"🔥 PORTFOLIO #{portfolio['id']}: {portfolio['name']} 👑")
            print("="*60)

            print(f"\n📊 Overview:")
            print(f"  User ID: {portfolio['user_id']}")
            print(f"  Risk Profile: {portfolio['risk_profile'].upper()}")
            print(f"  Total Value: ${portfolio['total_value']:,.2f}")
            print(f"  Created: {portfolio['created_at']}")
            print(f"  Updated: {portfolio['updated_at']}")

            # Performance
            if portfolio.get("performance"):
                perf = portfolio["performance"]
                print(f"\n💰 Performance:")
                print(f"  Total Gain/Loss: ${perf.get('total_gain_loss', 0):,.2f} ({perf.get('total_gain_loss_pct', 0):.2f}%)")
                print(f"  Daily Change: ${perf.get('daily_change', 0):,.2f} ({perf.get('daily_change_pct', 0):.2f}%)")

            # Holdings
            holdings = portfolio.get("holdings", [])
            if holdings:
                print(f"\n📈 Holdings ({len(holdings)} positions):")
                print("-" * 60)
                for h in holdings:
                    print(f"  {h['ticker']}: {h['shares']} shares @ ${h['price']:.2f}")
                    print(f"    Value: ${h['value']:,.2f} ({h.get('weight', 0):.1f}% of portfolio)")
                    print(f"    Gain/Loss: ${h.get('gain_loss', 0):,.2f} ({h.get('gain_loss_pct', 0):.2f}%)")
                    if 'purchase_price' in h:
                        print(f"    Purchase Price: ${h['purchase_price']:.2f}")
                    print()

            # Sector Breakdown
            sectors = portfolio.get("sector_breakdown", {})
            if sectors:
                print(f"\n🏢 Sector Allocation:")
                for sector, weight in sorted(sectors.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {sector}: {weight:.1f}%")

            print("\n" + "="*60 + "\n")
            return portfolio

    print(f"❌ Portfolio #{portfolio_id} not found")
    return None

def list_all_portfolios():
    """List all portfolios"""
    data = load_portfolios()

    print("\n" + "="*60)
    print("🔥 ALL PORTFOLIOS 👑")
    print("="*60)

    for p in data["portfolios"]:
        print(f"\nID {p['id']}: {p['name']}")
        print(f"  Risk: {p['risk_profile']} | Value: ${p['total_value']:,.2f}")
        print(f"  Holdings: {len(p.get('holdings', []))} positions")
        if p.get("performance"):
            gain_loss = p["performance"].get("total_gain_loss", 0)
            gain_pct = p["performance"].get("total_gain_loss_pct", 0)
            print(f"  Performance: ${gain_loss:,.2f} ({gain_pct:.2f}%)")

    print("\n" + "="*60 + "\n")

def show_risk_profiles():
    """Display risk profile definitions"""
    data = load_portfolios()

    print("\n" + "="*60)
    print("📊 RISK PROFILE DEFINITIONS 👑")
    print("="*60)

    for profile, rules in data["risk_profiles"].items():
        print(f"\n{profile.upper()}:")
        print(f"  Description: {rules.get('description', 'N/A')}")
        print(f"  Max Stock Allocation: {rules.get('max_stock_allocation', 0)*100:.0f}%")
        print(f"  Min Bond Allocation: {rules.get('min_bond_allocation', 0)*100:.0f}%")

    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "all":
            list_all_portfolios()
        elif sys.argv[1] == "risk":
            show_risk_profiles()
        else:
            try:
                portfolio_id = int(sys.argv[1])
                display_portfolio(portfolio_id)
            except ValueError:
                print("Usage: python view_portfolio.py [portfolio_id|all|risk]")
    else:
        # Default: show portfolio 7
        display_portfolio(7)
        print("💡 Usage:")
        print("  python view_portfolio.py 7         # View specific portfolio")
        print("  python view_portfolio.py all       # List all portfolios")
        print("  python view_portfolio.py risk      # Show risk profiles")
