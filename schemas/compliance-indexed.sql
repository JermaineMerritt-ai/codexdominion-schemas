-- Create table for verified facts
CREATE TABLE IF NOT EXISTS verified_facts (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    ticker TEXT,
    value NUMERIC NOT NULL,
    unit TEXT,
    tolerance NUMERIC NOT NULL,
    last_verified TIMESTAMP NOT NULL,
    sources JSONB NOT NULL
);

-- Create table for drift events
CREATE TABLE IF NOT EXISTS drift_events (
    id SERIAL PRIMARY KEY,
    fact_id TEXT REFERENCES verified_facts(id) ON DELETE CASCADE,
    old_value NUMERIC,
    new_value NUMERIC,
    detected_at TIMESTAMP DEFAULT NOW(),
    sources JSONB
);

CREATE INDEX IF NOT EXISTS idx_verified_facts_ticker ON verified_facts(ticker);
CREATE INDEX IF NOT EXISTS idx_drift_events_fact_id ON drift_events(fact_id);

-- Add audit trail for compliance
CREATE TABLE IF NOT EXISTS audit_trail (
    id SERIAL PRIMARY KEY,
    action TEXT NOT NULL,
    fact_id TEXT,
    details JSONB,
    performed_at TIMESTAMP DEFAULT NOW()
);
