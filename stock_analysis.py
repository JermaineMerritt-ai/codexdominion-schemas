"""
Stock Analysis & Recommendations System
"""
import json
from datetime import datetime

PORTFOLIO_LEDGER = "portfolios.json"
STOCK_ANALYSIS_LEDGER = "stock_analysis.json"

def load_stock_analysis():
    """Load stock analysis ledger"""
    try:
        with open(STOCK_ANALYSIS_LEDGER, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Create initial structure
        return {
            "meta": {
                "version": "1.0.0",
                "last_updated": datetime.utcnow().isoformat() + "Z",
                "custodian_authority": "Jermaine Merritt",
                "ledger_type": "STOCK_ANALYSIS_LEDGER"
            },
            "analyses": []
        }

def save_stock_analysis(data):
    """Save stock analysis ledger with timestamp"""
    data["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open(STOCK_ANALYSIS_LEDGER, "w") as f:
        json.dump(data, f, indent=2)

def add_analysis(ticker, analysis_text, recommendation=None, target_price=None, analyst=None):
    """Add stock analysis"""
    data = load_stock_analysis()

    # Check if analysis exists
    existing = None
    for i, a in enumerate(data["analyses"]):
        if a["ticker"] == ticker:
            existing = i
            break

    analysis_entry = {
        "ticker": ticker,
        "analysis": analysis_text,
        "recommendation": recommendation or "Hold",
        "target_price": target_price,
        "analyst": analyst or "AI System",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }

    if existing is not None:
        # Update existing
        analysis_entry["created_at"] = data["analyses"][existing]["created_at"]
        data["analyses"][existing] = analysis_entry
        print(f"📝 Updated analysis for {ticker}")
    else:
        # Add new
        data["analyses"].append(analysis_entry)
        print(f"✅ Added new analysis for {ticker}")

    save_stock_analysis(data)
    return analysis_entry

def get_analysis(ticker):
    """Get stock analysis"""
    data = load_stock_analysis()

    for analysis in data["analyses"]:
        if analysis["ticker"] == ticker:
            return analysis

    return None

def display_analysis(ticker):
    """Display stock analysis"""
    analysis = get_analysis(ticker)

    if not analysis:
        print(f"⚠️  No analysis found for {ticker}")
        return None

    print("\n" + "="*60)
    print(f"📊 STOCK ANALYSIS: {ticker} 👑")
    print("="*60)
    print(f"\n📝 Analysis:")
    print(f"   {analysis['analysis']}")
    print(f"\n💡 Recommendation: {analysis['recommendation']}")

    if analysis.get("target_price"):
        print(f"🎯 Target Price: ${analysis['target_price']:.2f}")

    print(f"\n👤 Analyst: {analysis['analyst']}")
    print(f"📅 Updated: {analysis['updated_at']}")
    print("\n" + "="*60 + "\n")

    return analysis

def display_all_analyses():
    """Display all stock analyses"""
    data = load_stock_analysis()

    if not data["analyses"]:
        print("⚠️  No stock analyses available")
        return

    print("\n" + "="*60)
    print("📊 ALL STOCK ANALYSES 👑")
    print("="*60)

    for a in data["analyses"]:
        print(f"\n{a['ticker']}: {a['recommendation']}")
        print(f"   {a['analysis'][:100]}...")
        if a.get("target_price"):
            print(f"   Target: ${a['target_price']:.2f}")

    print("\n" + "="*60 + "\n")

def get_portfolio_with_analysis(portfolio_id):
    """Get portfolio with stock analyses"""
    from view_portfolio import load_portfolios

    portfolios = load_portfolios()

    for portfolio in portfolios["portfolios"]:
        if portfolio["id"] == portfolio_id:
            print("\n" + "="*60)
            print(f"🔥 PORTFOLIO #{portfolio_id} WITH ANALYSIS 👑")
            print("="*60)

            print(f"\nPortfolio: {portfolio['name']}")
            print(f"Total Value: ${portfolio['total_value']:,.2f}")
            print(f"Performance: ${portfolio['performance']['total_gain_loss']:,.2f} ({portfolio['performance']['total_gain_loss_pct']:+.2f}%)")

            print("\n📈 Holdings with Analysis:")
            print("-" * 60)

            for holding in portfolio.get("holdings", []):
                ticker = holding["ticker"]
                print(f"\n{ticker}: {holding['shares']} shares @ ${holding['price']:.2f}")
                print(f"  Value: ${holding['value']:,.2f} ({holding['weight']:.1f}%)")
                print(f"  Gain/Loss: ${holding['gain_loss']:,.2f} ({holding['gain_loss_pct']:+.2f}%)")

                # Get analysis
                analysis = get_analysis(ticker)
                if analysis:
                    print(f"\n  📊 Analysis:")
                    print(f"     {analysis['analysis'][:150]}...")
                    print(f"     Recommendation: {analysis['recommendation']}")
                    if analysis.get("target_price"):
                        upside = ((analysis['target_price'] - holding['price']) / holding['price'] * 100)
                        print(f"     Target: ${analysis['target_price']:.2f} ({upside:+.1f}% upside)")
                else:
                    print(f"  ⚠️  No analysis available")

            print("\n" + "="*60 + "\n")
            return portfolio

    print(f"❌ Portfolio #{portfolio_id} not found")
    return None

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "add":
            # python stock_analysis.py add AAPL "Great company..." Buy 200.00
            ticker = sys.argv[2]
            analysis_text = sys.argv[3]
            recommendation = sys.argv[4] if len(sys.argv) > 4 else None
            target_price = float(sys.argv[5]) if len(sys.argv) > 5 else None

            add_analysis(ticker, analysis_text, recommendation, target_price)
            display_analysis(ticker)

        elif command == "view":
            # python stock_analysis.py view AAPL
            ticker = sys.argv[2]
            display_analysis(ticker)

        elif command == "all":
            # python stock_analysis.py all
            display_all_analyses()

        elif command == "portfolio":
            # python stock_analysis.py portfolio 7
            portfolio_id = int(sys.argv[2])
            get_portfolio_with_analysis(portfolio_id)

        else:
            print("Usage:")
            print("  python stock_analysis.py add <ticker> <analysis> [recommendation] [target_price]")
            print("  python stock_analysis.py view <ticker>")
            print("  python stock_analysis.py all")
            print("  python stock_analysis.py portfolio <id>")
    else:
        # Default: Add AAPL analysis
        analysis_text = "Apple designs consumer electronics... This stock may suit moderate investors..."

        print("\n🔥 Adding Stock Analysis 👑\n")
        add_analysis("AAPL", analysis_text, "Buy", 200.00, "AI Investment Analyst")

        print("\n" + "="*60)
        display_analysis("AAPL")

        print("💡 Now viewing Portfolio #7 with analysis...")
        get_portfolio_with_analysis(7)
