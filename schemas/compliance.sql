-- Table for verified facts
CREATE TABLE verified_facts (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    ticker TEXT,
    value NUMERIC NOT NULL,
    unit TEXT,
    tolerance NUMERIC NOT NULL,
    last_verified TIMESTAMP NOT NULL,
    sources JSONB NOT NULL
);

-- Table for drift events
CREATE TABLE drift_events (
    id SERIAL PRIMARY KEY,
    fact_id TEXT REFERENCES verified_facts(id),
    old_value NUMERIC,
    new_value NUMERIC,
    detected_at TIMESTAMP DEFAULT NOW(),
    sources JSONB
);
