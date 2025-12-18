# tasks/jobs.py

from datetime import datetime, timedelta
from extensions import db

# Import models with fallback for missing ones
try:
    from models import Portfolio, Stock, Alert, Fundamental
except ImportError:
    Portfolio = Stock = Alert = Fundamental = None

# These models will be added in future
DailyPrices = None
DailyPicks = None
NewsletterSubscribers = None

# Import services with fallback
try:
    from stocks.services import get_stock_price, get_stock_metadata
except ImportError:
    def get_stock_price(ticker):
        return 0.0
    def get_stock_metadata(ticker):
        return {}

try:
    from ai_services import run_daily_picks, run_portfolio_analysis
except ImportError:
    def run_daily_picks(candidates, context):
        return "AI service not configured"
    def run_portfolio_analysis(**kwargs):
        return "AI service not configured"

try:
    from newsletter.services import send_email
except ImportError:
    def send_email(to, subject, body):
        print(f"Email to {to}: {subject}")
        return True

# -----------------------------------------
# 1. DAILY STOCK DATA REFRESH
# -----------------------------------------

def update_daily_prices(tickers):
    """
    Pulls daily OHLC + volume for each ticker and stores in DB.
    """
    if DailyPrices is None:
        print("⚠️ DailyPrices model not yet implemented")
        return False

    for t in tickers:
        # Fetch from API (Polygon, Finnhub, etc.)
        price = get_stock_price(t)
        meta = get_stock_metadata(t)

        dp = DailyPrices(
            ticker=t,
            date=datetime.utcnow().date(),
            open=price,  # placeholder
            high=price,
            low=price,
            close=price,
            volume=meta.get("volume", 0)
        )
        db.session.add(dp)

    db.session.commit()
    return True


# -----------------------------------------
# 2. DAILY AI STOCK ACTION PICKS
# -----------------------------------------

def generate_daily_picks():
    """
    Selects 3 stocks using simple filters + AI explanation.
    """
    if DailyPicks is None:
        print("⚠️ DailyPicks model not yet implemented")
        return "Model not available"

    # Example: choose from a curated list
    universe = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "META"]

    candidates = []
    for t in universe:
        price = get_stock_price(t)
        meta = get_stock_metadata(t)

        candidates.append({
            "ticker": t,
            "reason_data": {
                "price": price,
                "volume": meta.get("volume"),
                "sector": meta.get("sector")
            }
        })

    # Market context (placeholder)
    context = {
        "futures": "mixed",
        "volatility_index": "moderate",
        "key_events": ["Earnings season", "Fed commentary"]
    }

    ai_output = run_daily_picks(candidates, context)

    # Save to DB
    dp = DailyPicks(
        date=datetime.utcnow().date(),
        ticker="MULTI",
        reason_summary=ai_output,
        volatility_score=0,
        volume_vs_avg=0,
        tags={}
    )
    db.session.add(dp)
    db.session.commit()

    return ai_output


# -----------------------------------------
# 3. DAILY NEWSLETTER SEND
# -----------------------------------------

def send_daily_newsletter():
    """
    Sends the daily AI stock picks email to subscribers.
    """
    if DailyPicks is None or NewsletterSubscribers is None:
        print("⚠️ Required models not yet implemented")
        return False

    picks = DailyPicks.query.order_by(DailyPicks.date.desc()).first()
    subs = NewsletterSubscribers.query.filter(
        NewsletterSubscribers.segments.contains("daily_picks")
    ).all()

    for s in subs:
        send_email(
            to=s.email,
            subject="Today's AI Stock Action Picks",
            body=picks.reason_summary
        )

    return True


# -----------------------------------------
# 4. WEEKLY PORTFOLIO SUMMARY
# -----------------------------------------

def send_weekly_portfolio_summaries():
    """
    Sends a weekly portfolio health check to each user.
    """
    if Portfolio is None:
        print("⚠️ Portfolio model not available")
        return False

    portfolios = Portfolio.query.all()

    for p in portfolios:
        ai_summary = run_portfolio_analysis(
            portfolio_name=p.name,
            risk_profile=p.risk_profile,
            holdings=[],  # you can load real holdings here
            summary_metrics={
                "num_holdings": 0,
                "largest_position": None,
                "sector_concentration": {},
                "overall_volatility": "medium"
            }
        )

        # Send to user
        user = p.user
        send_email(
            to=user.email,
            subject=f"Weekly Portfolio Health Check – {p.name}",
            body=ai_summary
        )

    return True


# -----------------------------------------
# 5. MONTHLY DEEP DIVE
# -----------------------------------------

def send_monthly_deep_dive():
    """
    Sends a monthly macro + strategy deep dive.
    """
    if NewsletterSubscribers is None:
        print("⚠️ NewsletterSubscribers model not yet implemented")
        return False

    subs = NewsletterSubscribers.query.filter(
        NewsletterSubscribers.segments.contains("monthly_deep_dive")
    ).all()

    deep_dive = """
    Monthly Deep Dive:
    - Macro overview
    - Sector trends
    - Conservative / Moderate / Aggressive sample allocations
    - AI insights on key themes
    """

    for s in subs:
        send_email(
            to=s.email,
            subject="Monthly Deep Dive & Strategy",
            body=deep_dive
        )

    return True
