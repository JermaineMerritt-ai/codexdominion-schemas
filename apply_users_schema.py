#!/usr/bin/env python3
"""
Apply Users Schema to Codex Database
=====================================
Applies the users table schema to the existing PostgreSQL database.
"""

import os
import sys

try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    print("❌ psycopg2 not installed. Installing...")
    os.system("pip install psycopg2-binary")
    import psycopg2
    from psycopg2 import sql

# Database connection from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://pgadmin:Jer47@localhost:5432/codex")

# Users table schema
USERS_SCHEMA = """
-- Users table: authentication and user management
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('user', 'admin', 'advisor')),
    risk_profile_default VARCHAR(50) DEFAULT 'moderate' CHECK (risk_profile_default IN ('conservative', 'moderate', 'aggressive', 'trader')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Indexes for users table
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

-- Insert default admin user (password: 'admin123' - CHANGE THIS!)
INSERT INTO users (email, password_hash, role, risk_profile_default)
VALUES ('admin@codexdominion.app', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LVvdPDPyC6o6QqE9u', 'admin', 'moderate')
ON CONFLICT (email) DO NOTHING;

-- Portfolios table: user-specific investment portfolios with risk profiles
CREATE TABLE IF NOT EXISTS portfolios (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    risk_profile VARCHAR(50) DEFAULT 'moderate' CHECK (risk_profile IN ('conservative', 'moderate', 'aggressive')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true,
    total_value DECIMAL(15, 2) DEFAULT 0.00,
    description TEXT
);

-- Indexes for portfolios table
CREATE INDEX IF NOT EXISTS idx_portfolios_user_id ON portfolios(user_id);
CREATE INDEX IF NOT EXISTS idx_portfolios_risk_profile ON portfolios(risk_profile);
CREATE INDEX IF NOT EXISTS idx_portfolios_created_at ON portfolios(created_at);

-- Insert default portfolios for admin user
INSERT INTO portfolios (user_id, name, risk_profile, description)
SELECT
    u.id,
    'Conservative Portfolio',
    'conservative',
    'Low-risk investment strategy focused on capital preservation'
FROM users u WHERE u.email = 'admin@codexdominion.app'
ON CONFLICT DO NOTHING;

INSERT INTO portfolios (user_id, name, risk_profile, description)
SELECT
    u.id,
    'Aggressive Portfolio',
    'aggressive',
    'High-risk, high-reward investment strategy for active trading'
FROM users u WHERE u.email = 'admin@codexdominion.app'
ON CONFLICT DO NOTHING;

-- Holdings table: individual stock positions within portfolios
CREATE TABLE IF NOT EXISTS holdings (
    id SERIAL PRIMARY KEY,
    portfolio_id INTEGER NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
    ticker VARCHAR(20) NOT NULL,
    shares DECIMAL(15, 4) NOT NULL DEFAULT 0,
    avg_cost DECIMAL(15, 4) NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_trade_date TIMESTAMP,
    notes TEXT
);

-- Indexes for holdings table
CREATE INDEX IF NOT EXISTS idx_holdings_portfolio_id ON holdings(portfolio_id);
CREATE INDEX IF NOT EXISTS idx_holdings_ticker ON holdings(ticker);
CREATE INDEX IF NOT EXISTS idx_holdings_created_at ON holdings(created_at);

-- Insert sample holdings for conservative portfolio
INSERT INTO holdings (portfolio_id, ticker, shares, avg_cost, notes)
SELECT
    p.id,
    'VTI',
    100.00,
    225.50,
    'Vanguard Total Stock Market ETF - Core holding'
FROM portfolios p
JOIN users u ON p.user_id = u.id
WHERE u.email = 'admin@codexdominion.app' AND p.name = 'Conservative Portfolio'
ON CONFLICT DO NOTHING;

INSERT INTO holdings (portfolio_id, ticker, shares, avg_cost, notes)
SELECT
    p.id,
    'BND',
    200.00,
    78.25,
    'Vanguard Total Bond Market ETF - Income generation'
FROM portfolios p
JOIN users u ON p.user_id = u.id
WHERE u.email = 'admin@codexdominion.app' AND p.name = 'Conservative Portfolio'
ON CONFLICT DO NOTHING;

-- Insert sample holdings for aggressive portfolio
INSERT INTO holdings (portfolio_id, ticker, shares, avg_cost, notes)
SELECT
    p.id,
    'TSLA',
    50.00,
    245.75,
    'Tesla Inc - High-growth technology play'
FROM portfolios p
JOIN users u ON p.user_id = u.id
WHERE u.email = 'admin@codexdominion.app' AND p.name = 'Aggressive Portfolio'
ON CONFLICT DO NOTHING;

INSERT INTO holdings (portfolio_id, ticker, shares, avg_cost, notes)
SELECT
    p.id,
    'NVDA',
    75.00,
    485.20,
    'NVIDIA Corporation - AI/GPU leader'
FROM portfolios p
JOIN users u ON p.user_id = u.id
WHERE u.email = 'admin@codexdominion.app' AND p.name = 'Aggressive Portfolio'
ON CONFLICT DO NOTHING;

-- Trades table: buy/sell transaction history for portfolio positions
CREATE TABLE IF NOT EXISTS trades (
    id SERIAL PRIMARY KEY,
    portfolio_id INTEGER NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
    ticker VARCHAR(20) NOT NULL,
    trade_type VARCHAR(10) NOT NULL CHECK (trade_type IN ('buy', 'sell')),
    shares DECIMAL(15, 4) NOT NULL,
    price DECIMAL(15, 4) NOT NULL,
    fees DECIMAL(15, 4) DEFAULT 0.00,
    trade_date TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    notes TEXT
);

-- Indexes for trades table
CREATE INDEX IF NOT EXISTS idx_trades_portfolio_id ON trades(portfolio_id);
CREATE INDEX IF NOT EXISTS idx_trades_ticker ON trades(ticker);
CREATE INDEX IF NOT EXISTS idx_trades_trade_date ON trades(trade_date);
CREATE INDEX IF NOT EXISTS idx_trades_trade_type ON trades(trade_type);

-- Insert sample trades for conservative portfolio
INSERT INTO trades (portfolio_id, ticker, trade_type, shares, price, fees, trade_date, notes)
SELECT
    p.id,
    'VTI',
    'buy',
    100.00,
    225.50,
    6.95,
    NOW() - INTERVAL '30 days',
    'Initial VTI purchase - Long-term hold'
FROM portfolios p
JOIN users u ON p.user_id = u.id
WHERE u.email = 'admin@codexdominion.app' AND p.name = 'Conservative Portfolio';

INSERT INTO trades (portfolio_id, ticker, trade_type, shares, price, fees, trade_date, notes)
SELECT
    p.id,
    'BND',
    'buy',
    200.00,
    78.25,
    6.95,
    NOW() - INTERVAL '25 days',
    'Bond position for income stability'
FROM portfolios p
JOIN users u ON p.user_id = u.id
WHERE u.email = 'admin@codexdominion.app' AND p.name = 'Conservative Portfolio';

-- Insert sample trades for aggressive portfolio
INSERT INTO trades (portfolio_id, ticker, trade_type, shares, price, fees, trade_date, notes)
SELECT
    p.id,
    'TSLA',
    'buy',
    50.00,
    245.75,
    6.95,
    NOW() - INTERVAL '15 days',
    'Tesla initial position - Growth play'
FROM portfolios p
JOIN users u ON p.user_id = u.id
WHERE u.email = 'admin@codexdominion.app' AND p.name = 'Aggressive Portfolio';

INSERT INTO trades (portfolio_id, ticker, trade_type, shares, price, fees, trade_date, notes)
SELECT
    p.id,
    'NVDA',
    'buy',
    75.00,
    485.20,
    6.95,
    NOW() - INTERVAL '10 days',
    'NVIDIA - AI/GPU market leader'
FROM portfolios p
JOIN users u ON p.user_id = u.id
WHERE u.email = 'admin@codexdominion.app' AND p.name = 'Aggressive Portfolio';

-- Sample sell trade
INSERT INTO trades (portfolio_id, ticker, trade_type, shares, price, fees, trade_date, notes)
SELECT
    p.id,
    'TSLA',
    'sell',
    10.00,
    268.50,
    6.95,
    NOW() - INTERVAL '5 days',
    'Partial profit taking on Tesla'
FROM portfolios p
JOIN users u ON p.user_id = u.id
WHERE u.email = 'admin@codexdominion.app' AND p.name = 'Aggressive Portfolio';

-- Stocks table: market data and pricing information for securities
CREATE TABLE IF NOT EXISTS stocks (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) UNIQUE NOT NULL,
    price DECIMAL(15, 4),
    market_cap BIGINT,
    pe_ratio DECIMAL(10, 2),
    updated_at TIMESTAMP DEFAULT NOW(),
    company_name VARCHAR(255),
    sector VARCHAR(100),
    exchange VARCHAR(50)
);

-- Indexes for stocks table
CREATE INDEX IF NOT EXISTS idx_stocks_ticker ON stocks(ticker);
CREATE INDEX IF NOT EXISTS idx_stocks_updated_at ON stocks(updated_at);
CREATE INDEX IF NOT EXISTS idx_stocks_sector ON stocks(sector);

-- Insert sample stock data
INSERT INTO stocks (ticker, price, market_cap, pe_ratio, company_name, sector, exchange)
VALUES
    ('VTI', 225.50, 1800000000000, 22.5, 'Vanguard Total Stock Market ETF', 'ETF', 'NYSE'),
    ('BND', 78.25, 350000000000, NULL, 'Vanguard Total Bond Market ETF', 'ETF', 'NYSE'),
    ('TSLA', 245.75, 780000000000, 65.2, 'Tesla Inc', 'Automotive', 'NASDAQ'),
    ('NVDA', 485.20, 1200000000000, 78.9, 'NVIDIA Corporation', 'Technology', 'NASDAQ'),
    ('AAPL', 178.50, 2800000000000, 28.4, 'Apple Inc', 'Technology', 'NASDAQ'),
    ('MSFT', 375.80, 2700000000000, 32.1, 'Microsoft Corporation', 'Technology', 'NASDAQ'),
    ('GOOGL', 140.25, 1750000000000, 24.8, 'Alphabet Inc', 'Technology', 'NASDAQ'),
    ('AMZN', 152.30, 1580000000000, 52.6, 'Amazon.com Inc', 'Consumer Cyclical', 'NASDAQ'),
    ('SPY', 460.75, 420000000000, NULL, 'SPDR S&P 500 ETF Trust', 'ETF', 'NYSE'),
    ('QQQ', 395.60, 195000000000, NULL, 'Invesco QQQ Trust', 'ETF', 'NASDAQ')
ON CONFLICT (ticker) DO UPDATE SET
    price = EXCLUDED.price,
    market_cap = EXCLUDED.market_cap,
    pe_ratio = EXCLUDED.pe_ratio,
    updated_at = NOW();

-- Fundamentals table: financial analysis and fundamental metrics
CREATE TABLE IF NOT EXISTS fundamentals (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    revenue_trend VARCHAR(10) CHECK (revenue_trend IN ('up', 'flat', 'down')),
    net_income_trend VARCHAR(10) CHECK (net_income_trend IN ('up', 'flat', 'down')),
    debt_level VARCHAR(10) CHECK (debt_level IN ('low', 'medium', 'high')),
    profit_margin_strength VARCHAR(10) CHECK (profit_margin_strength IN ('strong', 'average', 'weak')),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (ticker) REFERENCES stocks(ticker) ON DELETE CASCADE,
    UNIQUE(ticker)
);

-- Indexes for fundamentals table
CREATE INDEX IF NOT EXISTS idx_fundamentals_ticker ON fundamentals(ticker);
CREATE INDEX IF NOT EXISTS idx_fundamentals_revenue_trend ON fundamentals(revenue_trend);
CREATE INDEX IF NOT EXISTS idx_fundamentals_debt_level ON fundamentals(debt_level);

-- Insert sample fundamental analysis data
INSERT INTO fundamentals (ticker, revenue_trend, net_income_trend, debt_level, profit_margin_strength)
VALUES
    ('VTI', 'up', 'up', 'low', 'average'),
    ('BND', 'flat', 'flat', 'low', 'average'),
    ('TSLA', 'up', 'up', 'medium', 'strong'),
    ('NVDA', 'up', 'up', 'low', 'strong'),
    ('AAPL', 'up', 'up', 'low', 'strong'),
    ('MSFT', 'up', 'up', 'low', 'strong'),
    ('GOOGL', 'up', 'up', 'low', 'strong'),
    ('AMZN', 'up', 'flat', 'medium', 'average'),
    ('SPY', 'up', 'up', 'low', 'average'),
    ('QQQ', 'up', 'up', 'low', 'average')
ON CONFLICT (ticker) DO UPDATE SET
    revenue_trend = EXCLUDED.revenue_trend,
    net_income_trend = EXCLUDED.net_income_trend,
    debt_level = EXCLUDED.debt_level,
    profit_margin_strength = EXCLUDED.profit_margin_strength,
    updated_at = NOW();

-- Alerts table: market signals and trading notifications
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL DEFAULT NOW(),
    ticker VARCHAR(20) NOT NULL,
    reason_summary TEXT NOT NULL,
    volatility_score DECIMAL(5, 2),
    volume_vs_avg DECIMAL(10, 2),
    tags JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for alerts table
CREATE INDEX IF NOT EXISTS idx_alerts_ticker ON alerts(ticker);
CREATE INDEX IF NOT EXISTS idx_alerts_date ON alerts(date);
CREATE INDEX IF NOT EXISTS idx_alerts_volatility_score ON alerts(volatility_score);
CREATE INDEX IF NOT EXISTS idx_alerts_tags ON alerts USING GIN(tags);

-- Insert sample alert data
INSERT INTO alerts (date, ticker, reason_summary, volatility_score, volume_vs_avg, tags)
VALUES
    (NOW() - INTERVAL '1 hour', 'TSLA', 'Breaking above 250 resistance with strong volume', 8.5, 2.3, '{"type": "breakout", "sentiment": "bullish", "priority": "high"}'),
    (NOW() - INTERVAL '2 hours', 'NVDA', 'Unusual options activity detected - heavy call buying', 7.2, 1.8, '{"type": "options_flow", "sentiment": "bullish", "priority": "medium"}'),
    (NOW() - INTERVAL '3 hours', 'AAPL', 'Earnings beat expectations by 15% - price gapping up', 6.8, 3.1, '{"type": "earnings", "sentiment": "bullish", "priority": "high"}'),
    (NOW() - INTERVAL '4 hours', 'AMZN', 'Downgrade from major analyst - support test at 150', 9.1, 2.7, '{"type": "analyst_rating", "sentiment": "bearish", "priority": "high"}'),
    (NOW() - INTERVAL '5 hours', 'GOOGL', 'Volume spike with price consolidation - potential breakout setup', 5.5, 1.9, '{"type": "technical", "sentiment": "neutral", "priority": "medium"}'),
    (NOW() - INTERVAL '6 hours', 'MSFT', 'New cloud contract announced - bullish momentum building', 4.2, 1.5, '{"type": "news", "sentiment": "bullish", "priority": "medium"}'),
    (NOW() - INTERVAL '1 day', 'SPY', 'Market-wide selloff - high volatility across all sectors', 12.3, 4.5, '{"type": "market_event", "sentiment": "bearish", "priority": "critical"}'),
    (NOW() - INTERVAL '2 days', 'VTI', 'Rebalancing day - increased volume expected', 3.1, 1.2, '{"type": "rebalancing", "sentiment": "neutral", "priority": "low"}'),
    (NOW() - INTERVAL '3 days', 'QQQ', 'Tech sector rotation - momentum shifting to value stocks', 6.9, 2.1, '{"type": "sector_rotation", "sentiment": "bearish", "priority": "medium"}'),
    (NOW() - INTERVAL '4 days', 'BND', 'Fed rate decision upcoming - bond volatility rising', 7.8, 1.6, '{"type": "macro_event", "sentiment": "neutral", "priority": "high"}');

-- Subscribers table: lead capture and risk preference tracking
CREATE TABLE IF NOT EXISTS subscribers (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    risk_preference VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for subscribers table
CREATE INDEX IF NOT EXISTS idx_subscribers_email ON subscribers(email);
CREATE INDEX IF NOT EXISTS idx_subscribers_created_at ON subscribers(created_at);

-- Insert sample subscriber data
INSERT INTO subscribers (email, risk_preference, created_at)
VALUES
    ('john.investor@email.com', 'conservative', NOW() - INTERVAL '30 days'),
    ('sarah.trader@email.com', 'aggressive', NOW() - INTERVAL '25 days'),
    ('mike.analyst@email.com', 'moderate', NOW() - INTERVAL '20 days'),
    ('emma.portfolio@email.com', 'conservative', NOW() - INTERVAL '15 days'),
    ('alex.growth@email.com', 'aggressive', NOW() - INTERVAL '10 days'),
    ('lisa.wealth@email.com', 'moderate', NOW() - INTERVAL '8 days'),
    ('david.value@email.com', 'conservative', NOW() - INTERVAL '5 days'),
    ('rachel.momentum@email.com', 'aggressive', NOW() - INTERVAL '3 days'),
    ('chris.balanced@email.com', 'moderate', NOW() - INTERVAL '2 days'),
    ('jessica.dividend@email.com', 'conservative', NOW() - INTERVAL '1 day')
ON CONFLICT (email) DO NOTHING;

-- Advisor-Client relationships table: connects advisors with their clients
CREATE TABLE IF NOT EXISTS advisor_clients (
    id SERIAL PRIMARY KEY,
    advisor_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    client_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(advisor_id, client_user_id)
);

-- Indexes for advisor_clients table
CREATE INDEX IF NOT EXISTS idx_advisor_clients_advisor_id ON advisor_clients(advisor_id);
CREATE INDEX IF NOT EXISTS idx_advisor_clients_client_user_id ON advisor_clients(client_user_id);

-- Insert sample advisor-client relationships
-- First, insert additional users (advisors and clients)
INSERT INTO users (email, password_hash, role, risk_profile_default)
VALUES
    ('advisor1@codexdominion.app', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LVvdPDPyC6o6QqE9u', 'advisor', 'moderate'),
    ('advisor2@codexdominion.app', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LVvdPDPyC6o6QqE9u', 'advisor', 'moderate'),
    ('client1@codexdominion.app', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LVvdPDPyC6o6QqE9u', 'user', 'conservative'),
    ('client2@codexdominion.app', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LVvdPDPyC6o6QqE9u', 'user', 'aggressive'),
    ('client3@codexdominion.app', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LVvdPDPyC6o6QqE9u', 'user', 'moderate')
ON CONFLICT (email) DO NOTHING;

-- Create advisor-client relationships
INSERT INTO advisor_clients (advisor_id, client_user_id)
SELECT
    (SELECT id FROM users WHERE email = 'advisor1@codexdominion.app'),
    (SELECT id FROM users WHERE email = 'client1@codexdominion.app')
WHERE EXISTS (SELECT 1 FROM users WHERE email = 'advisor1@codexdominion.app')
  AND EXISTS (SELECT 1 FROM users WHERE email = 'client1@codexdominion.app')
ON CONFLICT (advisor_id, client_user_id) DO NOTHING;

INSERT INTO advisor_clients (advisor_id, client_user_id)
SELECT
    (SELECT id FROM users WHERE email = 'advisor1@codexdominion.app'),
    (SELECT id FROM users WHERE email = 'client2@codexdominion.app')
WHERE EXISTS (SELECT 1 FROM users WHERE email = 'advisor1@codexdominion.app')
  AND EXISTS (SELECT 1 FROM users WHERE email = 'client2@codexdominion.app')
ON CONFLICT (advisor_id, client_user_id) DO NOTHING;

INSERT INTO advisor_clients (advisor_id, client_user_id)
SELECT
    (SELECT id FROM users WHERE email = 'advisor2@codexdominion.app'),
    (SELECT id FROM users WHERE email = 'client3@codexdominion.app')
WHERE EXISTS (SELECT 1 FROM users WHERE email = 'advisor2@codexdominion.app')
  AND EXISTS (SELECT 1 FROM users WHERE email = 'client3@codexdominion.app')
ON CONFLICT (advisor_id, client_user_id) DO NOTHING;
"""

def apply_schema():
    """Apply the users schema to the database"""
    try:
        print("🔌 Connecting to database...")
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        print("📋 Creating users table...")
        cur.execute(USERS_SCHEMA)

        conn.commit()

        print("✅ Users schema applied successfully!")
        print("\n📊 Checking tables...")
        cur.execute("SELECT COUNT(*) FROM users;")
        count = cur.fetchone()[0]
        print(f"   Users in database: {count}")

        cur.execute("SELECT COUNT(*) FROM portfolios;")
        portfolio_count = cur.fetchone()[0]
        print(f"   Portfolios in database: {portfolio_count}")

        cur.execute("SELECT COUNT(*) FROM holdings;")
        holdings_count = cur.fetchone()[0]
        print(f"   Holdings in database: {holdings_count}")

        cur.execute("SELECT COUNT(*) FROM trades;")
        trades_count = cur.fetchone()[0]
        print(f"   Trades in database: {trades_count}")

        cur.execute("SELECT COUNT(*) FROM stocks;")
        stocks_count = cur.fetchone()[0]
        print(f"   Stocks in database: {stocks_count}")

        cur.execute("SELECT COUNT(*) FROM fundamentals;")
        fundamentals_count = cur.fetchone()[0]
        print(f"   Fundamentals in database: {fundamentals_count}")

        cur.execute("SELECT COUNT(*) FROM alerts;")
        alerts_count = cur.fetchone()[0]
        print(f"   Alerts in database: {alerts_count}")

        cur.execute("SELECT COUNT(*) FROM subscribers;")
        subscribers_count = cur.fetchone()[0]
        print(f"   Subscribers in database: {subscribers_count}")

        cur.execute("SELECT COUNT(*) FROM advisor_clients;")
        advisor_clients_count = cur.fetchone()[0]
        print(f"   Advisor-client relationships: {advisor_clients_count}")

        if count > 0:
            cur.execute("SELECT email, role, risk_profile_default, created_at FROM users LIMIT 5;")
            users = cur.fetchall()
            print("\n👥 Sample users:")
            for user in users:
                print(f"   - {user[0]} ({user[1]}, {user[2]})")

        if portfolio_count > 0:
            cur.execute("SELECT name, risk_profile, total_value FROM portfolios LIMIT 5;")
            portfolios = cur.fetchall()
            print("\n💼 Sample portfolios:")
            for portfolio in portfolios:
                print(f"   - {portfolio[0]} ({portfolio[1]}, ${portfolio[2]:,.2f})")

        if holdings_count > 0:
            cur.execute("SELECT ticker, shares, avg_cost FROM holdings LIMIT 5;")
            holdings = cur.fetchall()
            print("\n📊 Sample holdings:")
            for holding in holdings:
                print(f"   - {holding[0]}: {holding[1]:.2f} shares @ ${holding[2]:.2f}")

        if trades_count > 0:
            cur.execute("SELECT ticker, trade_type, shares, price, trade_date FROM trades ORDER BY trade_date DESC LIMIT 5;")
            trades = cur.fetchall()
            print("\n💰 Recent trades:")
            for trade in trades:
                action = "📈 BUY" if trade[1] == 'buy' else "📉 SELL"
                print(f"   - {action} {trade[0]}: {trade[2]:.2f} shares @ ${trade[3]:.2f} on {trade[4].strftime('%Y-%m-%d')}")

        if stocks_count > 0:
            cur.execute("SELECT ticker, company_name, price, market_cap, pe_ratio FROM stocks ORDER BY market_cap DESC LIMIT 5;")
            stocks = cur.fetchall()
            print("\n📊 Top stocks by market cap:")
            for stock in stocks:
                pe_str = f"P/E: {stock[4]:.1f}" if stock[4] else "P/E: N/A"
                mcap_b = stock[3] / 1000000000 if stock[3] else 0
                print(f"   - {stock[0]} ({stock[1]}): ${stock[2]:.2f} | MCap: ${mcap_b:.1f}B | {pe_str}")

        if fundamentals_count > 0:
            cur.execute("SELECT ticker, revenue_trend, net_income_trend, debt_level, profit_margin_strength FROM fundamentals WHERE profit_margin_strength = 'strong' LIMIT 5;")
            fundamentals = cur.fetchall()
            print("\n🔍 Strong fundamental stocks:")
            for fund in fundamentals:
                print(f"   - {fund[0]}: Rev {fund[1]} | Income {fund[2]} | Debt {fund[3]} | Margin {fund[4]}")

        if alerts_count > 0:
            cur.execute("SELECT ticker, reason_summary, volatility_score, volume_vs_avg, date FROM alerts ORDER BY date DESC LIMIT 5;")
            alerts = cur.fetchall()
            print("\n🚨 Recent market alerts:")
            for alert in alerts:
                print(f"   - {alert[0]}: {alert[1][:60]}... | Vol: {alert[2]:.1f} | Volume: {alert[3]:.1f}x avg")

        if subscribers_count > 0:
            cur.execute("SELECT email, risk_preference, created_at FROM subscribers ORDER BY created_at DESC LIMIT 5;")
            subscribers = cur.fetchall()
            print("\n📧 Recent subscribers:")
            for sub in subscribers:
                print(f"   - {sub[0]} | Risk: {sub[1]} | Joined: {sub[2].strftime('%Y-%m-%d')}")

        if advisor_clients_count > 0:
            cur.execute("""
                SELECT
                    u_advisor.email as advisor_email,
                    u_client.email as client_email,
                    ac.created_at
                FROM advisor_clients ac
                JOIN users u_advisor ON ac.advisor_id = u_advisor.id
                JOIN users u_client ON ac.client_user_id = u_client.id
                ORDER BY ac.created_at DESC
                LIMIT 5;
            """)
            relationships = cur.fetchall()
            print("\n🤝 Advisor-client relationships:")
            for rel in relationships:
                print(f"   - Advisor: {rel[0]} → Client: {rel[1]}")

        cur.close()
        conn.close()

        return True

    except psycopg2.OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        print("\n💡 Make sure PostgreSQL is running:")
        print("   - Check DATABASE_URL in .env")
        print("   - Verify PostgreSQL service is active")
        return False

    except Exception as e:
        print(f"❌ Error applying schema: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("👑 CODEX DOMINION - USERS SCHEMA SETUP")
    print("=" * 50)
    print()

    success = apply_schema()

    print()
    print("=" * 50)
    if success:
        print("🔥 USERS SYSTEM READY FOR AUTHENTICATION")
        print("=" * 50)
        sys.exit(0)
    else:
        print("⚠️  SCHEMA APPLICATION FAILED")
        print("=" * 50)
        sys.exit(1)
