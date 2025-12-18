"""
Portfolio Insights & Recommendations System
"""
import json
from datetime import datetime

PORTFOLIO_LEDGER = "portfolios.json"
PORTFOLIO_INSIGHTS_LEDGER = "portfolio_insights.json"

def load_portfolios():
    """Load portfolio ledger"""
    with open(PORTFOLIO_LEDGER, "r") as f:
        return json.load(f)

def load_insights():
    """Load portfolio insights ledger"""
    try:
        with open(PORTFOLIO_INSIGHTS_LEDGER, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "meta": {
                "version": "1.0.0",
                "last_updated": datetime.utcnow().isoformat() + "Z",
                "custodian_authority": "Jermaine Merritt",
                "ledger_type": "PORTFOLIO_INSIGHTS_LEDGER"
            },
            "insights": []
        }

def save_insights(data):
    """Save portfolio insights ledger"""
    data["meta"]["last_updated"] = datetime.utcnow().isoformat() + "Z"
    with open(PORTFOLIO_INSIGHTS_LEDGER, "w") as f:
        json.dump(data, f, indent=2)

def analyze_portfolio(portfolio_id):
    """Generate comprehensive portfolio analysis"""
    portfolios = load_portfolios()

    portfolio = None
    for p in portfolios["portfolios"]:
        if p["id"] == portfolio_id:
            portfolio = p
            break

    if not portfolio:
        print(f"❌ Portfolio #{portfolio_id} not found")
        return None

    holdings = portfolio.get("holdings", [])
    sector_breakdown = portfolio.get("sector_breakdown", {})

    insights = {
        "portfolio_id": portfolio_id,
        "summary": "",
        "concentration_risk": [],
        "sector_analysis": {},
        "diversification_score": 0,
        "recommendations": [],
        "strengths": [],
        "risks": [],
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }

    # Sector concentration analysis
    max_sector = max(sector_breakdown.items(), key=lambda x: x[1]) if sector_breakdown else ("None", 0)
    total_tech_exposure = sector_breakdown.get("Technology", 0) + sector_breakdown.get("Other", 0)

    # Generate summary
    if total_tech_exposure > 70:
        insights["summary"] = f"Your portfolio is heavily weighted in tech ({total_tech_exposure:.1f}%), creating significant concentration risk. Consider diversifying into other sectors for better risk-adjusted returns."
    elif total_tech_exposure > 50:
        insights["summary"] = f"Your portfolio has moderate tech concentration ({total_tech_exposure:.1f}%). This aligns with growth objectives but monitor sector-specific risks."
    else:
        insights["summary"] = f"Your portfolio is well-diversified across sectors with {total_tech_exposure:.1f}% tech exposure."

    # Concentration risk
    for ticker, holding in [(h["ticker"], h) for h in holdings]:
        if holding["weight"] > 50:
            insights["concentration_risk"].append({
                "ticker": ticker,
                "weight": holding["weight"],
                "risk_level": "HIGH",
                "message": f"{ticker} represents {holding['weight']:.1f}% of portfolio - significant single-stock risk"
            })
        elif holding["weight"] > 30:
            insights["concentration_risk"].append({
                "ticker": ticker,
                "weight": holding["weight"],
                "risk_level": "MODERATE",
                "message": f"{ticker} at {holding['weight']:.1f}% - consider position sizing"
            })

    # Sector analysis
    for sector, weight in sector_breakdown.items():
        risk_level = "HIGH" if weight > 60 else "MODERATE" if weight > 40 else "LOW"
        insights["sector_analysis"][sector] = {
            "weight": weight,
            "risk_level": risk_level,
            "recommendation": f"{'Reduce' if weight > 60 else 'Monitor' if weight > 40 else 'Maintain'} {sector} exposure"
        }

    # Diversification score (0-100)
    num_holdings = len(holdings)
    num_sectors = len([s for s in sector_breakdown.values() if s > 0])
    max_position_weight = max([h["weight"] for h in holdings]) if holdings else 0

    diversification = (
        (min(num_holdings / 10, 1) * 40) +  # Number of holdings (max 40 points)
        (min(num_sectors / 5, 1) * 30) +     # Sector diversity (max 30 points)
        ((100 - max_position_weight) / 100 * 30)  # Position concentration (max 30 points)
    )
    insights["diversification_score"] = round(diversification, 1)

    # Recommendations
    if total_tech_exposure > 70:
        insights["recommendations"].append("Consider adding healthcare, financials, or consumer staples for diversification")
    if num_holdings < 5:
        insights["recommendations"].append(f"Increase portfolio to 5-10 holdings for better diversification (currently {num_holdings})")
    if max_position_weight > 50:
        insights["recommendations"].append("Trim largest position and redistribute to reduce single-stock risk")
    if portfolio["performance"]["total_gain_loss_pct"] < 0:
        insights["recommendations"].append("Review underperforming positions - consider tax-loss harvesting opportunities")

    # Strengths
    if portfolio["performance"]["total_gain_loss_pct"] > 0:
        insights["strengths"].append(f"Positive total return of {portfolio['performance']['total_gain_loss_pct']:.2f}%")
    if portfolio["risk_profile"] == "aggressive" and total_tech_exposure > 60:
        insights["strengths"].append("Tech concentration aligns well with aggressive growth mandate")
    if num_holdings >= 3:
        insights["strengths"].append(f"Adequate number of holdings ({num_holdings}) provides some diversification")

    # Risks
    if total_tech_exposure > 70:
        insights["risks"].append("High tech sector correlation - vulnerable to sector-wide downturns")
    if max_position_weight > 50:
        insights["risks"].append(f"Single-stock risk: largest position is {max_position_weight:.1f}% of portfolio")
    if portfolio["total_value"] < 10000:
        insights["risks"].append("Small portfolio size may limit diversification opportunities")

    return insights

def add_insight(portfolio_id, summary=None, custom_recommendations=None):
    """Add or update portfolio insights"""
    insights_data = load_insights()

    # Generate automated insights
    auto_insights = analyze_portfolio(portfolio_id)

    if not auto_insights:
        return None

    # Override with custom data if provided
    if summary:
        auto_insights["summary"] = summary
    if custom_recommendations:
        auto_insights["recommendations"] = custom_recommendations

    # Check if insights exist for this portfolio
    existing_idx = None
    for i, insight in enumerate(insights_data["insights"]):
        if insight["portfolio_id"] == portfolio_id:
            existing_idx = i
            break

    if existing_idx is not None:
        insights_data["insights"][existing_idx] = auto_insights
        print(f"📝 Updated insights for Portfolio #{portfolio_id}")
    else:
        insights_data["insights"].append(auto_insights)
        print(f"✅ Added insights for Portfolio #{portfolio_id}")

    save_insights(insights_data)
    return auto_insights

def display_insights(portfolio_id):
    """Display portfolio insights"""
    insights_data = load_insights()

    insights = None
    for i in insights_data["insights"]:
        if i["portfolio_id"] == portfolio_id:
            insights = i
            break

    if not insights:
        print(f"⚠️  No insights found for Portfolio #{portfolio_id}")
        return None

    print("\n" + "="*60)
    print(f"💡 PORTFOLIO #{portfolio_id} INSIGHTS 👑")
    print("="*60)

    print(f"\n📊 Summary:")
    print(f"   {insights['summary']}")

    print(f"\n🎯 Diversification Score: {insights['diversification_score']}/100")
    if insights['diversification_score'] >= 70:
        print("   ✅ Well diversified")
    elif insights['diversification_score'] >= 50:
        print("   ⚠️  Moderately diversified")
    else:
        print("   ❌ Needs diversification")

    if insights.get("concentration_risk"):
        print(f"\n⚠️  Concentration Risks:")
        for risk in insights["concentration_risk"]:
            print(f"   {risk['risk_level']}: {risk['message']}")

    if insights.get("sector_analysis"):
        print(f"\n🏢 Sector Analysis:")
        for sector, analysis in insights["sector_analysis"].items():
            print(f"   {sector}: {analysis['weight']:.1f}% ({analysis['risk_level']} risk)")
            print(f"      → {analysis['recommendation']}")

    if insights.get("strengths"):
        print(f"\n💪 Strengths:")
        for strength in insights["strengths"]:
            print(f"   ✅ {strength}")

    if insights.get("risks"):
        print(f"\n⚠️  Risks:")
        for risk in insights["risks"]:
            print(f"   ⚠️  {risk}")

    if insights.get("recommendations"):
        print(f"\n🎯 Recommendations:")
        for i, rec in enumerate(insights["recommendations"], 1):
            print(f"   {i}. {rec}")

    print(f"\n📅 Generated: {insights['generated_at']}")
    print("\n" + "="*60 + "\n")

    return insights

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "analyze":
            portfolio_id = int(sys.argv[2])
            add_insight(portfolio_id)
            display_insights(portfolio_id)

        elif command == "view":
            portfolio_id = int(sys.argv[2])
            display_insights(portfolio_id)

        else:
            print("Usage:")
            print("  python portfolio_insights.py analyze <portfolio_id>")
            print("  python portfolio_insights.py view <portfolio_id>")
    else:
        # Default: Analyze portfolio 7
        print("\n🔥 Analyzing Portfolio #7 👑\n")

        summary = "Your portfolio is heavily weighted in tech with 78.3% exposure (NVDA 65.1% + AAPL 13.2%). This creates significant sector concentration risk. While this aligns with your aggressive growth mandate, consider diversifying into other sectors for better risk management."

        add_insight(7, summary=summary)
        display_insights(7)
