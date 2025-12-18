-- Codex Dominion Database Schema
-- Capsules system for operational sovereignty tracking

-- Capsules table: indexes ceremonial + technical capsules
CREATE TABLE capsules (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(120) UNIQUE NOT NULL,   -- e.g., 'festival', 'signals-daily'
    title VARCHAR(200) NOT NULL,
    kind VARCHAR(50) NOT NULL,           -- 'ceremony' | 'engine' | 'dispatch' | 'treasury' | 'education'
    mode VARCHAR(50) NOT NULL,           -- 'custodian' | 'heir' | 'customer' | 'public'
    version VARCHAR(50) DEFAULT '1.0.0',
    status VARCHAR(50) DEFAULT 'active', -- 'active' | 'archived'
    entrypoint TEXT,                     -- command, URL, or script path
    schedule VARCHAR(50),                -- cron-like '0 6 * * *' or null
    created_at TIMESTAMP DEFAULT NOW()
);

-- Capsule runs table: records executions, audits, lineage
CREATE TABLE capsule_runs (
    id SERIAL PRIMARY KEY,
    capsule_slug VARCHAR(120) NOT NULL REFERENCES capsules(slug) ON DELETE CASCADE,
    actor VARCHAR(120) NOT NULL,         -- 'custodian' | service account
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'success',-- 'success' | 'error'
    artifact_uri TEXT,                   -- Cloud Storage path or URL to snapshot/bulletin
    checksum TEXT                        -- integrity hash for idempotency
);

-- Indexes for fast lookup
CREATE INDEX idx_capsules_slug ON capsules(slug);
CREATE INDEX idx_runs_capsule_slug ON capsule_runs(capsule_slug);
CREATE INDEX idx_runs_started_at ON capsule_runs(started_at);

-- Users table: authentication and user management
CREATE TABLE users (
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
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Portfolios table: user-specific investment portfolios with risk profiles
CREATE TABLE portfolios (
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
CREATE INDEX idx_portfolios_user_id ON portfolios(user_id);
CREATE INDEX idx_portfolios_risk_profile ON portfolios(risk_profile);
CREATE INDEX idx_portfolios_created_at ON portfolios(created_at);

-- Holdings table: individual stock positions within portfolios
CREATE TABLE holdings (
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
CREATE INDEX idx_holdings_portfolio_id ON holdings(portfolio_id);
CREATE INDEX idx_holdings_ticker ON holdings(ticker);
CREATE INDEX idx_holdings_created_at ON holdings(created_at);

-- Trades table: buy/sell transaction history for portfolio positions
CREATE TABLE trades (
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
CREATE INDEX idx_trades_portfolio_id ON trades(portfolio_id);
CREATE INDEX idx_trades_ticker ON trades(ticker);
CREATE INDEX idx_trades_trade_date ON trades(trade_date);
CREATE INDEX idx_trades_trade_type ON trades(trade_type);

-- Stocks table: market data and pricing information for securities
CREATE TABLE stocks (
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
CREATE INDEX idx_stocks_ticker ON stocks(ticker);
CREATE INDEX idx_stocks_updated_at ON stocks(updated_at);
CREATE INDEX idx_stocks_sector ON stocks(sector);

-- Fundamentals table: financial analysis and fundamental metrics
CREATE TABLE fundamentals (
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
CREATE INDEX idx_fundamentals_ticker ON fundamentals(ticker);
CREATE INDEX idx_fundamentals_revenue_trend ON fundamentals(revenue_trend);
CREATE INDEX idx_fundamentals_debt_level ON fundamentals(debt_level);

-- Alerts table: market signals and trading notifications
CREATE TABLE alerts (
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
CREATE INDEX idx_alerts_ticker ON alerts(ticker);
CREATE INDEX idx_alerts_date ON alerts(date);
CREATE INDEX idx_alerts_volatility_score ON alerts(volatility_score);
CREATE INDEX idx_alerts_tags ON alerts USING GIN(tags);

-- Subscribers table: lead capture and risk preference tracking
CREATE TABLE subscribers (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    risk_preference VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for subscribers table
CREATE INDEX idx_subscribers_email ON subscribers(email);
CREATE INDEX idx_subscribers_created_at ON subscribers(created_at);

-- Advisor-Client relationships table: connects advisors with their clients
CREATE TABLE advisor_clients (
    id SERIAL PRIMARY KEY,
    advisor_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    client_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(advisor_id, client_user_id)
);

-- Indexes for advisor_clients table
CREATE INDEX idx_advisor_clients_advisor_id ON advisor_clients(advisor_id);
CREATE INDEX idx_advisor_clients_client_user_id ON advisor_clients(client_user_id);

-- Insert initial capsules for Codex Dominion system
INSERT INTO capsules (slug, title, kind, mode, entrypoint, schedule) VALUES
('signals-daily', 'Daily Signals Dispatch', 'engine', 'custodian', '/api/signals/daily', '0 6 * * *'),
('dawn-dispatch', 'Dawn Proclamation Capsule', 'dispatch', 'custodian', '/api/capsules/dawn-dispatch', '0 6 * * *'),
('sovereignty-bulletin', 'Operational Sovereignty Bulletin', 'ceremony', 'public', '/api/bulletins/generate', null),
('treasury-audit', 'Treasury Compliance Audit', 'treasury', 'custodian', '/api/treasury/audit', '0 0 1 * *'),
('education-matrix', 'Educational Content Matrix', 'education', 'public', '/api/education/matrix', null);
