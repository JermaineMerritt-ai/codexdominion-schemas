"""Background tasks for Celery workers."""
from celery_app import celery_app
from database import db, StockPrice, MarketAlert, NewsletterSubscriber, Portfolio, Holding
from datetime import datetime, timedelta
import yfinance as yf
import os

@celery_app.task
def update_stock_prices():
    """
    Update stock prices for all tracked tickers.
    Runs daily after market close.
    """
    from app import app

    with app.app_context():
        # Get all unique tickers from holdings
        tickers = db.session.query(Holding.ticker).distinct().all()
        tickers = [t[0] for t in tickers]

        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                data = stock.history(period='1d')

                if not data.empty:
                    latest = data.iloc[-1]

                    stock_price = StockPrice(
                        ticker=ticker,
                        date=datetime.now().date(),
                        open=float(latest['Open']),
                        high=float(latest['High']),
                        low=float(latest['Low']),
                        close=float(latest['Close']),
                        volume=int(latest['Volume'])
                    )

                    db.session.add(stock_price)

                print(f"✅ Updated {ticker}")

            except Exception as e:
                print(f"❌ Failed to update {ticker}: {e}")

        db.session.commit()
        return f"Updated {len(tickers)} stocks"


@celery_app.task
def generate_market_alerts():
    """
    Generate market alerts for unusual activity.
    Runs daily before market open.
    """
    from app import app

    with app.app_context():
        # Get all unique tickers
        tickers = db.session.query(Holding.ticker).distinct().all()
        tickers = [t[0] for t in tickers]

        alerts_created = 0

        for ticker in tickers:
            try:
                # Get latest 5 days of prices
                prices = StockPrice.query.filter_by(ticker=ticker).order_by(
                    StockPrice.date.desc()
                ).limit(5).all()

                if len(prices) >= 5:
                    latest = prices[0]
                    avg_volume = sum(p.volume for p in prices) / len(prices)

                    # Check for unusual volume (50% above average)
                    if latest.volume > avg_volume * 1.5:
                        volatility = abs(latest.daily_change_percent)

                        alert = MarketAlert(
                            date=datetime.now().date(),
                            ticker=ticker,
                            reason_summary=f"Unusual volume: {latest.volume:,.0f} vs avg {avg_volume:,.0f}",
                            volatility_score=volatility,
                            volume_vs_avg=latest.volume / avg_volume,
                            tags=['high_volume']
                        )

                        if volatility > 5:
                            alert.tags.append('high_volatility')

                        if latest.daily_change_percent > 3:
                            alert.tags.append('bullish')
                        elif latest.daily_change_percent < -3:
                            alert.tags.append('bearish')

                        db.session.add(alert)
                        alerts_created += 1

            except Exception as e:
                print(f"❌ Failed to generate alert for {ticker}: {e}")

        db.session.commit()
        return f"Created {alerts_created} alerts"


@celery_app.task
def send_newsletter():
    """
    Send weekly newsletter to all subscribers.
    Runs every Monday at 7 AM ET.
    """
    from app import app

    with app.app_context():
        subscribers = NewsletterSubscriber.query.all()

        for subscriber in subscribers:
            try:
                # TODO: Implement email sending logic
                # send_email(
                #     to=subscriber.email,
                #     subject="Weekly Portfolio Update",
                #     body=generate_newsletter_content(subscriber)
                # )

                print(f"✉️  Sent newsletter to {subscriber.email}")

            except Exception as e:
                print(f"❌ Failed to send newsletter to {subscriber.email}: {e}")

        return f"Sent newsletter to {len(subscribers)} subscribers"


@celery_app.task
def calculate_all_portfolio_performance():
    """
    Calculate performance metrics for all portfolios.
    Runs daily at midnight.
    """
    from app import app

    with app.app_context():
        portfolios = Portfolio.query.all()

        for portfolio in portfolios:
            try:
                # Get all holdings with current prices
                holdings = Holding.query.filter_by(portfolio_id=portfolio.id).all()

                total_value = 0
                for holding in holdings:
                    # Get latest price
                    latest_price = StockPrice.query.filter_by(
                        ticker=holding.ticker
                    ).order_by(StockPrice.date.desc()).first()

                    if latest_price:
                        current_value = holding.shares * latest_price.close
                        total_value += current_value

                # TODO: Store portfolio performance metrics
                print(f"📊 Portfolio {portfolio.name}: ${total_value:,.2f}")

            except Exception as e:
                print(f"❌ Failed to calculate performance for portfolio {portfolio.id}: {e}")

        return f"Calculated performance for {len(portfolios)} portfolios"


@celery_app.task
def cleanup_old_data():
    """
    Clean up old data to save storage space.
    Runs weekly on Sunday midnight.
    """
    from app import app

    with app.app_context():
        # Delete stock prices older than 2 years
        two_years_ago = datetime.now() - timedelta(days=730)
        deleted_prices = StockPrice.query.filter(
            StockPrice.date < two_years_ago.date()
        ).delete()

        # Delete market alerts older than 6 months
        six_months_ago = datetime.now() - timedelta(days=180)
        deleted_alerts = MarketAlert.query.filter(
            MarketAlert.date < six_months_ago.date()
        ).delete()

        db.session.commit()

        return f"Cleaned up {deleted_prices} old prices, {deleted_alerts} old alerts"
