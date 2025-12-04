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

-- Insert initial capsules for Codex Dominion system
INSERT INTO capsules (slug, title, kind, mode, entrypoint, schedule) VALUES
('signals-daily', 'Daily Signals Dispatch', 'engine', 'custodian', '/api/signals/daily', '0 6 * * *'),
('dawn-dispatch', 'Dawn Proclamation Capsule', 'dispatch', 'custodian', '/api/capsules/dawn-dispatch', '0 6 * * *'),
('sovereignty-bulletin', 'Operational Sovereignty Bulletin', 'ceremony', 'public', '/api/bulletins/generate', null),
('treasury-audit', 'Treasury Compliance Audit', 'treasury', 'custodian', '/api/treasury/audit', '0 0 1 * *'),
('education-matrix', 'Educational Content Matrix', 'education', 'public', '/api/education/matrix', null);
