#!/usr/bin/env python
"""
Initialize SQLite Database for Investment App
Creates all tables and adds sample data
"""
import sys
import os

# Add investment_app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'investment_app'))

from app import create_app
from extensions import db
from models import User, Stock, Fundamental, Alert, Subscriber
from datetime import datetime, date

def init_database():
    """Create database and add sample data"""
    app = create_app()

    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✅ Tables created!")

        # Check if data already exists
        if Stock.query.first():
            print("✅ Database already has stocks")
            # Don't return - continue to add fundamentals and alerts if needed
        else:
            # Add sample stocks
            print("Adding sample stocks...")
            stocks = [
                Stock(ticker='AAPL', name='Apple Inc.', sector='Technology'),
                Stock(ticker='MSFT', name='Microsoft Corporation', sector='Technology'),
                Stock(ticker='GOOGL', name='Alphabet Inc.', sector='Technology'),
                Stock(ticker='AMZN', name='Amazon.com Inc.', sector='Consumer Cyclical'),
                Stock(ticker='TSLA', name='Tesla Inc.', sector='Consumer Cyclical'),
                Stock(ticker='NVDA', name='NVIDIA Corporation', sector='Technology'),
                Stock(ticker='META', name='Meta Platforms Inc.', sector='Technology'),
                Stock(ticker='JPM', name='JPMorgan Chase & Co.', sector='Financial'),
                Stock(ticker='JNJ', name='Johnson & Johnson', sector='Healthcare'),
                Stock(ticker='V', name='Visa Inc.', sector='Financial'),
            ]

            for stock in stocks:
                db.session.add(stock)

            db.session.commit()
            print(f"✅ Added {len(stocks)} sample stocks")

        # Add sample fundamentals
        print("Adding sample fundamentals...")
        fundamentals = [
            Fundamental(ticker='AAPL', revenue_trend='up', net_income_trend='up', debt_level='low', profit_margin_strength='strong'),
            Fundamental(ticker='MSFT', revenue_trend='up', net_income_trend='up', debt_level='low', profit_margin_strength='strong'),
            Fundamental(ticker='GOOGL', revenue_trend='up', net_income_trend='up', debt_level='low', profit_margin_strength='strong'),
        ]

        for fundamental in fundamentals:
            db.session.add(fundamental)

        db.session.commit()
        print(f"✅ Added {len(fundamentals)} fundamentals")

        # Add sample alerts
        print("Adding sample alerts...")
        from datetime import date
        alerts = [
            Alert(ticker='AAPL', date=date.today(), reason_summary='AAPL approaching resistance at $180', volatility_score=15.5),
            Alert(ticker='TSLA', date=date.today(), reason_summary='TSLA showing high volatility (30-day ATR)', volatility_score=35.2),
            Alert(ticker='NVDA', date=date.today(), reason_summary='NVDA earnings announcement next week', volatility_score=22.1),
        ]

        for alert in alerts:
            db.session.add(alert)

        db.session.commit()
        print(f"✅ Added {len(alerts)} alerts")

        print("\n🎉 Database initialization complete!")
        print(f"📊 Total stocks: {Stock.query.count()}")
        print(f"📈 Total fundamentals: {Fundamental.query.count()}")
        print(f"🔔 Total alerts: {Alert.query.count()}")
        print(f"\n💡 Database file: {app.config['SQLALCHEMY_DATABASE_URI']}")

if __name__ == '__main__':
    init_database()
