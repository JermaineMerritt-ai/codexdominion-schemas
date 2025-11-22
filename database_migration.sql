-- Codex Dominion Trading Platform Database Schema
-- Migration Script v1.0 - Initial Setup

-- Enable UUID extension if not exists
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing tables if they exist (for clean migration)
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS pools CASCADE;
DROP TABLE IF EXISTS signals CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS cycles CASCADE;
DROP TABLE IF EXISTS artifacts CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS incidents CASCADE;
DROP TABLE IF EXISTS amm_events CASCADE;
DROP TABLE IF EXISTS amm_pools CASCADE;
DROP TABLE IF EXISTS affiliate_metrics CASCADE;
DROP TABLE IF EXISTS daily_picks CASCADE;
DROP TABLE IF EXISTS positions CASCADE;
DROP TABLE IF EXISTS portfolios CASCADE;

-- Core Entity Tables (New Schema)

-- accounts table
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    role VARCHAR(50) NOT NULL, -- Custodian, Heir, Customer
    name VARCHAR(100),
    lineage TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- artifacts table
CREATE TABLE artifacts (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50),
    title VARCHAR(200),
    status VARCHAR(50),
    checksum TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- cycles table
CREATE TABLE cycles (
    id SERIAL PRIMARY KEY,
    kind VARCHAR(50),
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- transactions table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    stream VARCHAR(50), -- affiliate, stock, AMM
    amount NUMERIC(18,2),
    currency VARCHAR(10),
    source VARCHAR(100),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- signals table
CREATE TABLE signals (
    id SERIAL PRIMARY KEY,
    tier VARCHAR(50),
    rationale TEXT,
    issued_at TIMESTAMP DEFAULT NOW()
);

-- pools table
CREATE TABLE pools (
    id SERIAL PRIMARY KEY,
    asset_pair VARCHAR(50),
    strategy_id INT,
    weight NUMERIC(5,2),
    cap NUMERIC(18,2),
    state VARCHAR(50),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- events table
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    actor VARCHAR(100),
    artifact_id INT,
    action VARCHAR(100),
    hash TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Trading Platform Tables (Existing Schema)

-- Create portfolios table
CREATE TABLE portfolios (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  owner_id UUID NOT NULL,
  risk_tier TEXT CHECK (risk_tier IN ('conservative','moderate','aggressive')) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Indexes for performance
  CONSTRAINT portfolios_owner_id_idx UNIQUE (owner_id, id)
);

-- Create indexes for core entity tables
CREATE INDEX idx_accounts_role ON accounts(role);
CREATE INDEX idx_accounts_created_at ON accounts(created_at);
CREATE INDEX idx_artifacts_type ON artifacts(type);
CREATE INDEX idx_artifacts_status ON artifacts(status);
CREATE INDEX idx_artifacts_created_at ON artifacts(created_at);
CREATE INDEX idx_cycles_kind ON cycles(kind);
CREATE INDEX idx_cycles_started_at ON cycles(started_at);
CREATE INDEX idx_transactions_stream ON transactions(stream);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_created_at ON transactions(created_at);
CREATE INDEX idx_signals_tier ON signals(tier);
CREATE INDEX idx_signals_issued_at ON signals(issued_at);
CREATE INDEX idx_pools_asset_pair ON pools(asset_pair);
CREATE INDEX idx_pools_state ON pools(state);
CREATE INDEX idx_pools_updated_at ON pools(updated_at);
CREATE INDEX idx_events_actor ON events(actor);
CREATE INDEX idx_events_artifact_id ON events(artifact_id);
CREATE INDEX idx_events_action ON events(action);
CREATE INDEX idx_events_created_at ON events(created_at);

-- Create indexes for portfolios
CREATE INDEX idx_portfolios_owner_id ON portfolios(owner_id);
CREATE INDEX idx_portfolios_risk_tier ON portfolios(risk_tier);
CREATE INDEX idx_portfolios_created_at ON portfolios(created_at);

-- Create incidents table
CREATE TABLE incidents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  source TEXT NOT NULL,       -- e.g., 'affiliate_api', 'amm_node', 'market_data'
  message TEXT NOT NULL,
  severity TEXT CHECK (severity IN ('info','warning','error','critical')) DEFAULT 'warning',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for incidents
CREATE INDEX idx_incidents_source ON incidents(source);
CREATE INDEX idx_incidents_severity ON incidents(severity);
CREATE INDEX idx_incidents_created_at ON incidents(created_at);
CREATE INDEX idx_incidents_source_severity ON incidents(source, severity);

-- Create positions table
CREATE TABLE positions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  portfolio_id UUID NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
  symbol TEXT NOT NULL,
  quantity NUMERIC(18,8) NOT NULL CHECK (quantity > 0),
  avg_cost NUMERIC(18,8) NOT NULL CHECK (avg_cost > 0),
  last_price NUMERIC(18,8),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Prevent duplicate symbols in same portfolio
  CONSTRAINT unique_portfolio_symbol UNIQUE (portfolio_id, symbol)
);

-- Create indexes for positions
CREATE INDEX idx_positions_portfolio_id ON positions(portfolio_id);
CREATE INDEX idx_positions_symbol ON positions(symbol);
CREATE INDEX idx_positions_updated_at ON positions(updated_at);

-- Create daily picks table
CREATE TABLE daily_picks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL,
  trade_date DATE NOT NULL,
  symbols TEXT[] NOT NULL,
  scores JSONB DEFAULT '{}',               -- {liquidity, volatility, catalyst, technical}
  performance JSONB DEFAULT '{}',          -- PnL simulation result
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Prevent duplicate picks for same user/date
  CONSTRAINT unique_user_trade_date UNIQUE (user_id, trade_date)
);

-- Create indexes for daily picks
CREATE INDEX idx_daily_picks_user_id ON daily_picks(user_id);
CREATE INDEX idx_daily_picks_trade_date ON daily_picks(trade_date);
CREATE INDEX idx_daily_picks_created_at ON daily_picks(created_at);
CREATE INDEX idx_daily_picks_symbols ON daily_picks USING GIN(symbols);
CREATE INDEX idx_daily_picks_scores ON daily_picks USING GIN(scores);

-- Create affiliate metrics table
CREATE TABLE affiliate_metrics (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  program TEXT NOT NULL,
  clicks INT DEFAULT 0 CHECK (clicks >= 0),
  conversions INT DEFAULT 0 CHECK (conversions >= 0),
  commission NUMERIC(12,2) DEFAULT 0 CHECK (commission >= 0),
  captured_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for affiliate metrics
CREATE INDEX idx_affiliate_metrics_program ON affiliate_metrics(program);
CREATE INDEX idx_affiliate_metrics_captured_at ON affiliate_metrics(captured_at);
CREATE INDEX idx_affiliate_metrics_commission ON affiliate_metrics(commission);

-- Create amm pools table
CREATE TABLE amm_pools (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  pool_symbol TEXT NOT NULL UNIQUE,  -- e.g., "USDC/ETH"
  tvl_usd NUMERIC(18,2) DEFAULT 0 CHECK (tvl_usd >= 0),
  apr NUMERIC(8,4) DEFAULT 0 CHECK (apr >= 0),
  risk_tier TEXT CHECK (risk_tier IN ('low','medium','high')),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for amm pools
CREATE INDEX idx_amm_pools_pool_symbol ON amm_pools(pool_symbol);
CREATE INDEX idx_amm_pools_tvl_usd ON amm_pools(tvl_usd DESC);
CREATE INDEX idx_amm_pools_apr ON amm_pools(apr DESC);
CREATE INDEX idx_amm_pools_risk_tier ON amm_pools(risk_tier);

-- Create amm events table
CREATE TABLE amm_events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  pool_id UUID NOT NULL REFERENCES amm_pools(id) ON DELETE CASCADE,
  event_type TEXT CHECK (event_type IN ('stake','unstake','swap','harvest')) NOT NULL,
  payload JSONB DEFAULT '{}',
  tx_hash TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for amm events
CREATE INDEX idx_amm_events_pool_id ON amm_events(pool_id);
CREATE INDEX idx_amm_events_event_type ON amm_events(event_type);
CREATE INDEX idx_amm_events_created_at ON amm_events(created_at);
CREATE INDEX idx_amm_events_tx_hash ON amm_events(tx_hash);
CREATE INDEX idx_amm_events_payload ON amm_events USING GIN(payload);

-- Create composite indexes for common queries
CREATE INDEX idx_positions_portfolio_symbol ON positions(portfolio_id, symbol);
CREATE INDEX idx_daily_picks_user_date ON daily_picks(user_id, trade_date);
CREATE INDEX idx_affiliate_metrics_program_date ON affiliate_metrics(program, captured_at);
CREATE INDEX idx_amm_events_pool_type_date ON amm_events(pool_id, event_type, created_at);

-- Insert sample data for testing

-- Sample data for core entity tables

-- Sample accounts
INSERT INTO accounts (role, name, lineage) VALUES
  ('Custodian', 'Master Account', 'Genesis Node'),
  ('Heir', 'Primary Heir Account', 'Genesis Node -> Primary'),
  ('Customer', 'Demo User 1', 'Primary -> Demo Branch'),
  ('Customer', 'Demo User 2', 'Primary -> Demo Branch'),
  ('Heir', 'Secondary Heir', 'Genesis Node -> Secondary');

-- Sample artifacts
INSERT INTO artifacts (type, title, status, checksum) VALUES
  ('trading_signal', 'AAPL Long Signal - Nov 2025', 'active', 'sha256:abc123...'),
  ('portfolio_template', 'Conservative Growth Template', 'published', 'sha256:def456...'),
  ('risk_model', 'Volatility Assessment Model v2.1', 'active', 'sha256:ghi789...'),
  ('affiliate_campaign', 'Q4 2025 Trading Platform Campaign', 'running', 'sha256:jkl012...'),
  ('amm_strategy', 'USDC/ETH Liquidity Strategy', 'deployed', 'sha256:mno345...');

-- Sample cycles
INSERT INTO cycles (kind, started_at, completed_at) VALUES
  ('daily_rebalance', NOW() - INTERVAL '1 day', NOW() - INTERVAL '23 hours'),
  ('weekly_analysis', NOW() - INTERVAL '7 days', NOW() - INTERVAL '6 days 20 hours'),
  ('monthly_report', NOW() - INTERVAL '30 days', NOW() - INTERVAL '29 days'),
  ('affiliate_payout', NOW() - INTERVAL '14 days', NOW() - INTERVAL '13 days 22 hours'),
  ('risk_assessment', NOW() - INTERVAL '3 days', NULL); -- ongoing

-- Sample transactions
INSERT INTO transactions (stream, amount, currency, source, status) VALUES
  ('affiliate', 2250.00, 'USD', 'TradingView Commission', 'completed'),
  ('stock', 15525.00, 'USD', 'AAPL Position Sale', 'completed'),
  ('AMM', 8750.50, 'USDC', 'USDC/ETH LP Rewards', 'completed'),
  ('affiliate', 1600.00, 'USD', 'Webull Referral', 'pending'),
  ('stock', 22000.00, 'USD', 'TSLA Position Entry', 'completed'),
  ('AMM', 456.75, 'ETH', 'WBTC/ETH Swap', 'completed');

-- Sample signals
INSERT INTO signals (tier, rationale) VALUES
  ('premium', 'Strong bullish momentum on AAPL with earnings beat and guidance raise'),
  ('standard', 'Technical breakout pattern on MSFT above 320 resistance'),
  ('premium', 'High-probability mean reversion play on NVDA after 15% pullback'),
  ('standard', 'Sector rotation into financials - JPM showing strength'),
  ('premium', 'ETH DeFi yields attractive at current gas fee levels');

-- Sample pools
INSERT INTO pools (asset_pair, strategy_id, weight, cap, state) VALUES
  ('USDC/ETH', 1, 35.50, 125000.00, 'active'),
  ('DAI/USDC', 1, 25.00, 85000.00, 'active'),
  ('WBTC/ETH', 2, 20.75, 45000.00, 'active'),
  ('LINK/ETH', 2, 15.25, 25000.00, 'active'),
  ('UNI/ETH', 3, 3.50, 15000.00, 'paused');

-- Sample events
INSERT INTO events (actor, artifact_id, action, hash) VALUES
  ('trading_engine', 1, 'signal_generated', '0x' || encode(gen_random_bytes(32), 'hex')),
  ('portfolio_manager', 2, 'template_applied', '0x' || encode(gen_random_bytes(32), 'hex')),
  ('risk_monitor', 3, 'model_updated', '0x' || encode(gen_random_bytes(32), 'hex')),
  ('affiliate_tracker', 4, 'campaign_launched', '0x' || encode(gen_random_bytes(32), 'hex')),
  ('amm_controller', 5, 'strategy_deployed', '0x' || encode(gen_random_bytes(32), 'hex')),
  ('user_dashboard', 1, 'signal_viewed', '0x' || encode(gen_random_bytes(32), 'hex')),
  ('rebalancer', 2, 'portfolio_rebalanced', '0x' || encode(gen_random_bytes(32), 'hex'));

-- Sample portfolios
INSERT INTO portfolios (id, owner_id, risk_tier) VALUES
  ('550e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440101', 'moderate'),
  ('550e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440102', 'aggressive'),
  ('550e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440103', 'conservative');

-- Sample positions
INSERT INTO positions (portfolio_id, symbol, quantity, avg_cost, last_price) VALUES
  ('550e8400-e29b-41d4-a716-446655440001', 'AAPL', 100.00000000, 150.00000000, 155.25000000),
  ('550e8400-e29b-41d4-a716-446655440001', 'MSFT', 50.00000000, 300.00000000, 310.50000000),
  ('550e8400-e29b-41d4-a716-446655440001', 'GOOGL', 25.00000000, 2500.00000000, 2475.00000000),
  ('550e8400-e29b-41d4-a716-446655440002', 'TSLA', 75.00000000, 200.00000000, 220.00000000),
  ('550e8400-e29b-41d4-a716-446655440002', 'NVDA', 30.00000000, 400.00000000, 450.00000000),
  ('550e8400-e29b-41d4-a716-446655440003', 'SPY', 200.00000000, 400.00000000, 405.00000000);

-- Sample daily picks
INSERT INTO daily_picks (user_id, trade_date, symbols, scores, performance) VALUES
  ('550e8400-e29b-41d4-a716-446655440101', CURRENT_DATE, 
   ARRAY['AAPL', 'MSFT'], 
   '{"liquidity": 95, "volatility": 75, "catalyst": 80, "technical": 85}',
   '{"expected_return": 5.2, "risk_score": 65, "confidence": 78}'),
  ('550e8400-e29b-41d4-a716-446655440102', CURRENT_DATE - INTERVAL '1 day',
   ARRAY['TSLA', 'NVDA'],
   '{"liquidity": 85, "volatility": 90, "catalyst": 95, "technical": 80}',
   '{"expected_return": 8.5, "risk_score": 85, "confidence": 72}');

-- Sample affiliate metrics
INSERT INTO affiliate_metrics (program, clicks, conversions, commission) VALUES
  ('TradingView', 1250, 45, 2250.00),
  ('Webull', 890, 32, 1600.00),
  ('Interactive Brokers', 567, 18, 1800.00),
  ('TD Ameritrade', 345, 12, 1200.00);

-- Sample AMM pools
INSERT INTO amm_pools (pool_symbol, tvl_usd, apr, risk_tier) VALUES
  ('USDC/ETH', 125000000.00, 8.5, 'low'),
  ('DAI/USDC', 85000000.00, 4.2, 'low'),
  ('WBTC/ETH', 45000000.00, 12.8, 'medium'),
  ('LINK/ETH', 25000000.00, 18.5, 'medium'),
  ('UNI/ETH', 15000000.00, 35.2, 'high');

-- Sample AMM events
INSERT INTO amm_events (pool_id, event_type, payload, tx_hash) 
SELECT 
  p.id,
  'stake',
  '{"amount": 10000, "token": "USDC", "user": "0x123...abc"}',
  '0x' || encode(gen_random_bytes(32), 'hex')
FROM amm_pools p
WHERE p.pool_symbol = 'USDC/ETH'
LIMIT 1;

INSERT INTO amm_events (pool_id, event_type, payload, tx_hash)
SELECT 
  p.id,
  'swap',
  '{"from_token": "ETH", "to_token": "USDC", "amount_in": 5.5, "amount_out": 18750}',
  '0x' || encode(gen_random_bytes(32), 'hex')
FROM amm_pools p
WHERE p.pool_symbol = 'USDC/ETH'
LIMIT 1;

-- Sample incidents data
INSERT INTO incidents (source, message, severity, created_at) VALUES
  ('affiliate_api', 'API rate limit approaching 80% threshold', 'warning', NOW() - INTERVAL '2 hours'),
  ('market_data', 'Market data feed restored after 30s outage', 'info', NOW() - INTERVAL '4 hours'),
  ('amm_node', 'High gas fees detected: 150+ gwei', 'warning', NOW() - INTERVAL '6 hours'),
  ('trading_engine', 'Order execution delayed by 2.3 seconds', 'error', NOW() - INTERVAL '8 hours'),
  ('database', 'Connection pool at 90% capacity', 'warning', NOW() - INTERVAL '12 hours'),
  ('portfolio_sync', 'Portfolio rebalancing completed successfully', 'info', NOW() - INTERVAL '1 day'),
  ('risk_monitor', 'Portfolio exceeding risk tolerance by 15%', 'critical', NOW() - INTERVAL '2 days'),
  ('affiliate_tracker', 'Commission payment processed: $2,450', 'info', NOW() - INTERVAL '3 days');

-- Create views for common queries

-- Portfolio performance view
CREATE VIEW portfolio_performance AS
SELECT 
  p.id as portfolio_id,
  p.owner_id,
  p.risk_tier,
  COUNT(pos.id) as position_count,
  COALESCE(SUM(pos.quantity * pos.avg_cost), 0) as total_cost_basis,
  COALESCE(SUM(pos.quantity * COALESCE(pos.last_price, pos.avg_cost)), 0) as total_market_value,
  COALESCE(SUM(pos.quantity * (COALESCE(pos.last_price, pos.avg_cost) - pos.avg_cost)), 0) as unrealized_pnl,
  CASE 
    WHEN SUM(pos.quantity * pos.avg_cost) > 0 THEN
      ROUND((SUM(pos.quantity * (COALESCE(pos.last_price, pos.avg_cost) - pos.avg_cost)) / 
             SUM(pos.quantity * pos.avg_cost) * 100)::numeric, 2)
    ELSE 0 
  END as return_percentage
FROM portfolios p
LEFT JOIN positions pos ON p.id = pos.portfolio_id
GROUP BY p.id, p.owner_id, p.risk_tier;

-- Top performing symbols view
CREATE VIEW top_performing_symbols AS
SELECT 
  symbol,
  COUNT(*) as occurrence_count,
  AVG(quantity) as avg_quantity,
  AVG(avg_cost) as avg_entry_price,
  AVG(last_price) as avg_current_price,
  AVG((last_price - avg_cost) / avg_cost * 100) as avg_return_percentage
FROM positions 
WHERE last_price IS NOT NULL
GROUP BY symbol
HAVING COUNT(*) > 1
ORDER BY avg_return_percentage DESC;

-- Daily affiliate performance view
CREATE VIEW daily_affiliate_performance AS
SELECT 
  DATE(captured_at) as date,
  program,
  SUM(clicks) as total_clicks,
  SUM(conversions) as total_conversions,
  SUM(commission) as total_commission,
  CASE 
    WHEN SUM(clicks) > 0 THEN 
      ROUND((SUM(conversions)::numeric / SUM(clicks) * 100), 2)
    ELSE 0 
  END as conversion_rate
FROM affiliate_metrics
GROUP BY DATE(captured_at), program
ORDER BY date DESC, total_commission DESC;

-- Integrated views connecting new and existing schemas

-- Account portfolio summary
CREATE VIEW account_portfolio_summary AS
SELECT 
  a.id as account_id,
  a.role,
  a.name,
  COUNT(DISTINCT p.id) as portfolio_count,
  COALESCE(SUM(pp.total_market_value), 0) as total_portfolio_value,
  COALESCE(SUM(pp.unrealized_pnl), 0) as total_unrealized_pnl
FROM accounts a
LEFT JOIN portfolios p ON a.name = 'Demo User 1' AND p.owner_id = '550e8400-e29b-41d4-a716-446655440101'
  OR a.name = 'Demo User 2' AND p.owner_id = '550e8400-e29b-41d4-a716-446655440102'
LEFT JOIN portfolio_performance pp ON p.id = pp.portfolio_id
GROUP BY a.id, a.role, a.name;

-- Transaction flow summary
CREATE VIEW transaction_flow_summary AS
SELECT 
  t.stream,
  t.currency,
  COUNT(*) as transaction_count,
  SUM(t.amount) as total_amount,
  AVG(t.amount) as average_amount,
  MIN(t.created_at) as first_transaction,
  MAX(t.created_at) as last_transaction
FROM transactions t
WHERE t.status = 'completed'
GROUP BY t.stream, t.currency
ORDER BY total_amount DESC;

-- Signal performance tracking
CREATE VIEW signal_performance_tracking AS
SELECT 
  s.id as signal_id,
  s.tier,
  s.rationale,
  s.issued_at,
  COUNT(e.id) as event_count,
  ARRAY_AGG(DISTINCT e.action) as actions_taken
FROM signals s
LEFT JOIN events e ON e.artifact_id = s.id
GROUP BY s.id, s.tier, s.rationale, s.issued_at
ORDER BY s.issued_at DESC;

-- Pool activity summary
CREATE VIEW pool_activity_summary AS
SELECT 
  p.id as pool_id,
  p.asset_pair,
  p.weight,
  p.cap,
  p.state,
  amp.tvl_usd,
  amp.apr,
  COUNT(ame.id) as event_count,
  MAX(ame.created_at) as last_activity
FROM pools p
LEFT JOIN amm_pools amp ON p.asset_pair = amp.pool_symbol
LEFT JOIN amm_events ame ON amp.id = ame.pool_id
GROUP BY p.id, p.asset_pair, p.weight, p.cap, p.state, amp.tvl_usd, amp.apr
ORDER BY p.weight DESC;

-- Codex Capsules System
-- ==========================================
-- Index ceremonial + technical capsules for digital sovereignty

-- capsules table: index ceremonial + technical capsules
CREATE TABLE capsules (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(120) UNIQUE NOT NULL,   -- e.g., 'festival', 'great-year', 'signals-daily'
    title VARCHAR(200) NOT NULL,
    kind VARCHAR(50) NOT NULL,           -- 'ceremony' | 'engine' | 'dispatch' | 'treasury' | 'education'
    mode VARCHAR(50) NOT NULL,           -- 'custodian' | 'heir' | 'customer' | 'public'
    version VARCHAR(50) DEFAULT '1.0.0',
    status VARCHAR(50) DEFAULT 'active',  -- 'active' | 'archived'
    entrypoint TEXT,                      -- command, URL, or script path
    schedule VARCHAR(50),                 -- cron-like '0 6 * * *' or null
    created_at TIMESTAMP DEFAULT NOW()
);

-- capsule_runs table: replay, audits, lineage
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

-- Create indexes for capsules system
CREATE INDEX idx_capsules_slug ON capsules(slug);
CREATE INDEX idx_capsules_kind ON capsules(kind);
CREATE INDEX idx_capsules_mode ON capsules(mode);
CREATE INDEX idx_capsules_status ON capsules(status);
CREATE INDEX idx_capsules_schedule ON capsules(schedule);
CREATE INDEX idx_capsules_created_at ON capsules(created_at);
CREATE INDEX idx_capsule_runs_capsule_slug ON capsule_runs(capsule_slug);
CREATE INDEX idx_capsule_runs_actor ON capsule_runs(actor);
CREATE INDEX idx_capsule_runs_status ON capsule_runs(status);
CREATE INDEX idx_capsule_runs_started_at ON capsule_runs(started_at);
CREATE INDEX idx_capsule_runs_completed_at ON capsule_runs(completed_at);

-- Sample capsules data
INSERT INTO capsules (slug, title, kind, mode, version, entrypoint, schedule) VALUES
  ('dawn-dispatch', 'Daily Dawn Dispatch', 'dispatch', 'custodian', '2.0.0', 'python codex_dawn_dispatch.py', '0 6 * * *'),
  ('signals-daily', 'Codex Signals Daily Generation', 'engine', 'custodian', '1.0.0', 'POST /signals/daily', '0 7 * * *'),
  ('signals-bulletin', 'Portfolio Intelligence Bulletin', 'engine', 'public', '1.0.0', 'POST /bulletin?format=md', null),
  ('treasury-reconciliation', 'Treasury Ledger Reconciliation', 'treasury', 'custodian', '1.5.0', 'python codex_treasury_database.py', '0 23 * * *'),
  ('great-year-ceremony', 'Annual Digital Sovereignty Ceremony', 'ceremony', 'custodian', '1.0.0', 'python ceremonies/great_year.py', '0 0 1 1 *'),
  ('festival-capsule', 'Quarterly Performance Festival', 'ceremony', 'heir', '1.0.0', 'python ceremonies/festival.py', '0 12 1 */3 *'),
  ('portfolio-rebalance', 'Automated Portfolio Rebalancing', 'engine', 'custodian', '1.2.0', 'python codex_portfolio_rebalance.py', '0 4 * * 1'),
  ('affiliate-payouts', 'Affiliate Commission Processing', 'treasury', 'custodian', '1.0.0', 'python affiliate_payout_processor.py', '0 2 1 * *'),
  ('education-digest', 'Weekly Financial Education Digest', 'education', 'customer', '1.0.0', 'python education/weekly_digest.py', '0 10 * * 1'),
  ('sovereignty-metrics', 'Digital Sovereignty Health Check', 'engine', 'custodian', '1.0.0', 'python sovereignty_health_check.py', '0 */6 * * *');

-- Sample capsule runs data
INSERT INTO capsule_runs (capsule_slug, actor, started_at, completed_at, status, artifact_uri, checksum) VALUES
  ('dawn-dispatch', 'system@codex-dominion', NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day' + INTERVAL '2 minutes', 'success', 'gs://codex-artifacts/dawn-dispatch/20251108_060000.json', 'sha256:a1b2c3d4e5f6'),
  ('signals-daily', 'signals-engine@codex-dominion', NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day' + INTERVAL '45 seconds', 'success', 'gs://codex-artifacts/signals/20251108_070000.json', 'sha256:f6e5d4c3b2a1'),
  ('signals-bulletin', 'public-api@codex-dominion', NOW() - INTERVAL '2 hours', NOW() - INTERVAL '2 hours' + INTERVAL '1.5 seconds', 'success', 'gs://codex-bulletins/bulletin_20251108.md', 'sha256:123abc456def'),
  ('treasury-reconciliation', 'treasury@codex-dominion', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days' + INTERVAL '15 minutes', 'success', 'gs://codex-artifacts/treasury/reconciliation_20251106.json', 'sha256:789ghi012jkl'),
  ('portfolio-rebalance', 'portfolio-engine@codex-dominion', NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days' + INTERVAL '3 minutes', 'success', 'gs://codex-artifacts/rebalance/20251105_040000.json', 'sha256:mno345pqr678'),
  ('sovereignty-metrics', 'health-monitor@codex-dominion', NOW() - INTERVAL '6 hours', NOW() - INTERVAL '6 hours' + INTERVAL '5 seconds', 'success', 'gs://codex-metrics/sovereignty_20251108_060000.json', 'sha256:stu901vwx234'),
  ('signals-daily', 'signals-engine@codex-dominion', NOW() - INTERVAL '2 days', NULL, 'error', null, null); -- Failed run

-- Capsule performance view
CREATE VIEW capsule_performance AS
SELECT 
  c.slug,
  c.title,
  c.kind,
  c.mode,
  c.status as capsule_status,
  COUNT(cr.id) as total_runs,
  COUNT(CASE WHEN cr.status = 'success' THEN 1 END) as successful_runs,
  COUNT(CASE WHEN cr.status = 'error' THEN 1 END) as failed_runs,
  CASE 
    WHEN COUNT(cr.id) > 0 THEN 
      ROUND((COUNT(CASE WHEN cr.status = 'success' THEN 1 END)::numeric / COUNT(cr.id) * 100), 2)
    ELSE 0 
  END as success_rate,
  MAX(cr.completed_at) as last_successful_run,
  AVG(EXTRACT(EPOCH FROM (cr.completed_at - cr.started_at))) as avg_runtime_seconds
FROM capsules c
LEFT JOIN capsule_runs cr ON c.slug = cr.capsule_slug
GROUP BY c.slug, c.title, c.kind, c.mode, c.status
ORDER BY c.kind, c.slug;

-- Scheduled capsules view
CREATE VIEW scheduled_capsules AS
SELECT 
  c.slug,
  c.title,
  c.kind,
  c.schedule,
  c.entrypoint,
  MAX(cr.completed_at) as last_run,
  COUNT(CASE WHEN cr.started_at > NOW() - INTERVAL '24 hours' THEN 1 END) as runs_today
FROM capsules c
LEFT JOIN capsule_runs cr ON c.slug = cr.capsule_slug
WHERE c.schedule IS NOT NULL AND c.status = 'active'
GROUP BY c.slug, c.title, c.kind, c.schedule, c.entrypoint
ORDER BY c.schedule;

-- Comprehensive system status view (updated with capsules)
CREATE VIEW system_status_dashboard AS
SELECT 
  'accounts' as entity_type,
  COUNT(*) as total_count,
  COUNT(CASE WHEN role = 'Customer' THEN 1 END) as active_customers,
  MAX(created_at) as last_created
FROM accounts
UNION ALL
SELECT 
  'portfolios' as entity_type,
  COUNT(*) as total_count,
  COUNT(CASE WHEN risk_tier = 'aggressive' THEN 1 END) as high_risk_count,
  MAX(created_at) as last_created
FROM portfolios
UNION ALL
SELECT 
  'transactions' as entity_type,
  COUNT(*) as total_count,
  COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_count,
  MAX(created_at) as last_created
FROM transactions
UNION ALL
SELECT 
  'amm_pools' as entity_type,
  COUNT(*) as total_count,
  COUNT(CASE WHEN risk_tier = 'high' THEN 1 END) as high_risk_count,
  MAX(updated_at) as last_updated
FROM amm_pools
UNION ALL
SELECT 
  'capsules' as entity_type,
  COUNT(*) as total_count,
  COUNT(CASE WHEN status = 'active' THEN 1 END) as active_count,
  MAX(created_at) as last_created
FROM capsules
UNION ALL
SELECT 
  'capsule_runs' as entity_type,
  COUNT(*) as total_count,
  COUNT(CASE WHEN status = 'success' THEN 1 END) as successful_count,
  MAX(started_at) as last_started
FROM capsule_runs;

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO codex_admin;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO codex_admin;