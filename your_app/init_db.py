"""
Database initialization script
Run this to create database tables
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from database import db, User, Portfolio, Holding, Transaction, StockPrice, MarketAlert, NewsletterSubscriber

def init_database():
    """Initialize database and create tables"""
    # Force SQLite - remove any DATABASE_URL from environment
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']
        print("🗑️  Removed DATABASE_URL from environment - using SQLite")

    app = create_app('development')

    with app.app_context():
        print("🔥 Initializing Codex Dominion Database 👑")

        # Drop all tables (use with caution!)
        # db.drop_all()
        # print("🗑️  Dropped all existing tables")

        # Create all tables
        db.create_all()
        print("✅ Created all database tables")

        # Check if admin user exists
        admin = User.query.filter_by(email='admin@codexdominion.com').first()

        if not admin:
            # Create default admin user
            admin = User(
                email='admin@codexdominion.com',
                role='admin',
                risk_profile_default='moderate'
            )
            admin.set_password('codex2025')  # CHANGE THIS IN PRODUCTION!

            db.session.add(admin)
            db.session.commit()

            # Create sample portfolio for admin
            sample_portfolio = Portfolio(
                user_id=admin.id,
                name='Growth Portfolio',
                risk_profile='aggressive'
            )
            db.session.add(sample_portfolio)
            db.session.commit()

            # Create sample holdings
            holdings_data = [
                {'ticker': 'AAPL', 'shares': 10, 'avg_price': 180.50},
                {'ticker': 'MSFT', 'shares': 15, 'avg_price': 375.25},
                {'ticker': 'GOOGL', 'shares': 8, 'avg_price': 140.75}
            ]

            for holding_data in holdings_data:
                holding = Holding(
                    portfolio_id=sample_portfolio.id,
                    ticker=holding_data['ticker'],
                    shares=holding_data['shares'],
                    avg_price=holding_data['avg_price']
                )
                db.session.add(holding)

            # Create sample transactions
            transactions_data = [
                {'ticker': 'AAPL', 'trade_type': 'buy', 'shares': 5, 'price': 175.00, 'fees': 1.50},
                {'ticker': 'AAPL', 'trade_type': 'buy', 'shares': 5, 'price': 186.00, 'fees': 1.50},
                {'ticker': 'MSFT', 'trade_type': 'buy', 'shares': 15, 'price': 375.25, 'fees': 2.25},
                {'ticker': 'GOOGL', 'trade_type': 'buy', 'shares': 10, 'price': 138.50, 'fees': 2.00},
                {'ticker': 'GOOGL', 'trade_type': 'sell', 'shares': 2, 'price': 145.00, 'fees': 0.50}
            ]

            for trans_data in transactions_data:
                transaction = Transaction(
                    portfolio_id=sample_portfolio.id,
                    ticker=trans_data['ticker'],
                    trade_type=trans_data['trade_type'],
                    shares=trans_data['shares'],
                    price=trans_data['price'],
                    fees=trans_data['fees']
                )
                db.session.add(transaction)

            # Create sample stock price data
            from datetime import date, timedelta
            today = date.today()

            price_data = [
                # AAPL - 5 days
                {'ticker': 'AAPL', 'days_ago': 4, 'open': 178.50, 'high': 182.30, 'low': 177.90, 'close': 180.50, 'volume': 52340000},
                {'ticker': 'AAPL', 'days_ago': 3, 'open': 180.75, 'high': 183.20, 'low': 179.80, 'close': 182.10, 'volume': 48920000},
                {'ticker': 'AAPL', 'days_ago': 2, 'open': 182.00, 'high': 185.40, 'low': 181.50, 'close': 184.75, 'volume': 55670000},
                {'ticker': 'AAPL', 'days_ago': 1, 'open': 184.80, 'high': 187.20, 'low': 183.90, 'close': 186.50, 'volume': 51230000},
                {'ticker': 'AAPL', 'days_ago': 0, 'open': 186.40, 'high': 188.90, 'low': 185.70, 'close': 187.80, 'volume': 49850000},
                # MSFT - 5 days
                {'ticker': 'MSFT', 'days_ago': 4, 'open': 372.50, 'high': 376.80, 'low': 371.20, 'close': 375.25, 'volume': 28340000},
                {'ticker': 'MSFT', 'days_ago': 3, 'open': 375.50, 'high': 378.90, 'low': 374.30, 'close': 377.60, 'volume': 26920000},
                {'ticker': 'MSFT', 'days_ago': 2, 'open': 377.70, 'high': 381.20, 'low': 376.50, 'close': 379.80, 'volume': 30120000},
                {'ticker': 'MSFT', 'days_ago': 1, 'open': 379.90, 'high': 383.40, 'low': 378.80, 'close': 382.50, 'volume': 27840000},
                {'ticker': 'MSFT', 'days_ago': 0, 'open': 382.40, 'high': 385.70, 'low': 381.30, 'close': 384.90, 'volume': 29560000},
                # GOOGL - 5 days
                {'ticker': 'GOOGL', 'days_ago': 4, 'open': 138.20, 'high': 141.50, 'low': 137.80, 'close': 140.75, 'volume': 32340000},
                {'ticker': 'GOOGL', 'days_ago': 3, 'open': 140.80, 'high': 143.20, 'low': 139.90, 'close': 142.30, 'volume': 30920000},
                {'ticker': 'GOOGL', 'days_ago': 2, 'open': 142.40, 'high': 145.60, 'low': 141.80, 'close': 144.50, 'volume': 35670000},
                {'ticker': 'GOOGL', 'days_ago': 1, 'open': 144.60, 'high': 147.30, 'low': 143.70, 'close': 146.20, 'volume': 33230000},
                {'ticker': 'GOOGL', 'days_ago': 0, 'open': 146.30, 'high': 148.90, 'low': 145.50, 'close': 147.80, 'volume': 31850000}
            ]

            for price in price_data:
                stock_price = StockPrice(
                    ticker=price['ticker'],
                    date=today - timedelta(days=price['days_ago']),
                    open=price['open'],
                    high=price['high'],
                    low=price['low'],
                    close=price['close'],
                    volume=price['volume']
                )
                db.session.add(stock_price)

            db.session.commit()

            # Create sample market alerts
            alerts_data = [
                {
                    'ticker': 'AAPL',
                    'days_ago': 2,
                    'reason_summary': 'Unusual trading volume spike after product announcement',
                    'volatility_score': 8.5,
                    'volume_vs_avg': 2.3,
                    'tags': ['high_volume', 'news_driven', 'bullish']
                },
                {
                    'ticker': 'MSFT',
                    'days_ago': 1,
                    'reason_summary': 'Strong earnings beat, raised guidance',
                    'volatility_score': 6.2,
                    'volume_vs_avg': 1.8,
                    'tags': ['earnings', 'bullish', 'institutional_buying']
                },
                {
                    'ticker': 'GOOGL',
                    'days_ago': 0,
                    'reason_summary': 'Regulatory concerns causing sharp intraday moves',
                    'volatility_score': 9.1,
                    'volume_vs_avg': 3.2,
                    'tags': ['high_volatility', 'regulatory', 'risk']
                }
            ]

            for alert in alerts_data:
                market_alert = MarketAlert(
                    date=today - timedelta(days=alert['days_ago']),
                    ticker=alert['ticker'],
                    reason_summary=alert['reason_summary'],
                    volatility_score=alert['volatility_score'],
                    volume_vs_avg=alert['volume_vs_avg'],
                    tags=alert['tags']
                )
                db.session.add(market_alert)

            db.session.commit()

            # Create sample newsletter subscribers
            subscribers_data = [
                {
                    'email': 'investor1@example.com',
                    'risk_profile': 'conservative',
                    'segments': ['dividend_stocks', 'bonds', 'blue_chip']
                },
                {
                    'email': 'trader2@example.com',
                    'risk_profile': 'aggressive',
                    'segments': ['tech_stocks', 'options', 'day_trading']
                },
                {
                    'email': 'analyst3@example.com',
                    'risk_profile': 'moderate',
                    'segments': ['market_analysis', 'earnings', 'sector_rotation']
                },
                {
                    'email': 'growth4@example.com',
                    'risk_profile': 'aggressive',
                    'segments': ['growth_stocks', 'tech_stocks', 'ipos']
                }
            ]

            for sub in subscribers_data:
                subscriber = NewsletterSubscriber(
                    email=sub['email'],
                    risk_profile=sub['risk_profile'],
                    segments=sub['segments']
                )
                db.session.add(subscriber)

            db.session.commit()

            print(f"✅ Created admin user: {admin.email}")
            print(f"⚠️  Default password: codex2025 (CHANGE THIS!)")
            print(f"💼 Created sample portfolio: Growth Portfolio")
            print(f"📊 Created {len(holdings_data)} sample holdings")
            print(f"💰 Created {len(transactions_data)} sample transactions")
            print(f"📈 Created {len(price_data)} stock price records")
            print(f"🚨 Created {len(alerts_data)} market alerts")
            print(f"📧 Created {len(subscribers_data)} newsletter subscribers")
        else:
            print(f"✅ Admin user already exists: {admin.email}")

        # Print table info
        print("\n📊 Database Tables:")
        for table in db.metadata.tables.keys():
            count = db.session.execute(db.text(f"SELECT COUNT(*) FROM {table}")).scalar()
            print(f"  - {table}: {count} records")

        print("\n🔥 Database initialization complete! 👑")

if __name__ == '__main__':
    init_database()
