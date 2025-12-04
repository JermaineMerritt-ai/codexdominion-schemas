-- ============================================================================
-- CODEX DOMINION DATABASE MIGRATION SCROLL
-- Operational Sovereignty Schema for Capsule Management
-- ============================================================================

-- Connect to the codex database first
\c codex;

-- ============================================================================
-- CAPSULES TABLE: Master registry of all operational capsules
-- ============================================================================

CREATE TABLE IF NOT EXISTS capsules (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    schedule_cron VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    config JSONB DEFAULT '{}',

    -- Indexing for performance
    CONSTRAINT capsules_slug_check CHECK (slug ~ '^[a-z0-9-]+$')
);

-- Create index for fast lookups
CREATE INDEX IF NOT EXISTS idx_capsules_slug ON capsules(slug);
CREATE INDEX IF NOT EXISTS idx_capsules_active ON capsules(is_active);

-- ============================================================================
-- CAPSULE_RUNS TABLE: Complete execution tracking and audit trail
-- ============================================================================

CREATE TABLE IF NOT EXISTS capsule_runs (
    id SERIAL PRIMARY KEY,
    capsule_slug VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    execution_time_ms INTEGER NOT NULL DEFAULT 0,
    archive_url TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Execution metadata
    execution_id UUID DEFAULT gen_random_uuid(),
    triggered_by VARCHAR(100) DEFAULT 'scheduler',
    error_message TEXT,
    artifact_checksum VARCHAR(64),

    -- Performance metrics
    cpu_usage_percent DECIMAL(5,2),
    memory_usage_mb INTEGER,
    network_bytes_in BIGINT,
    network_bytes_out BIGINT,

    -- Additional metadata
    metadata JSONB DEFAULT '{}',

    -- Constraints
    CONSTRAINT capsule_runs_status_check CHECK (
        status IN ('pending', 'running', 'success', 'failed', 'timeout', 'cancelled')
    ),
    CONSTRAINT capsule_runs_execution_time_check CHECK (execution_time_ms >= 0),

    -- Foreign key relationship
    CONSTRAINT fk_capsule_runs_capsule FOREIGN KEY (capsule_slug)
        REFERENCES capsules(slug) ON DELETE CASCADE
);

-- Performance indexes
CREATE INDEX IF NOT EXISTS idx_capsule_runs_slug ON capsule_runs(capsule_slug);
CREATE INDEX IF NOT EXISTS idx_capsule_runs_timestamp ON capsule_runs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_capsule_runs_status ON capsule_runs(status);
CREATE INDEX IF NOT EXISTS idx_capsule_runs_execution_id ON capsule_runs(execution_id);

-- Composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_capsule_runs_slug_timestamp ON capsule_runs(capsule_slug, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_capsule_runs_status_timestamp ON capsule_runs(status, timestamp DESC);

-- ============================================================================
-- INSERT OPERATIONAL SOVEREIGNTY CAPSULES
-- ============================================================================

INSERT INTO capsules (slug, name, description, schedule_cron) VALUES
    ('signals-daily', 'Daily Market Signals Analysis', 'Autonomous market analysis and investment signal generation', '0 6 * * *'),
    ('dawn-dispatch', 'Dawn Sovereignty Dispatch', 'Morning operational status and strategic briefings', '0 6 * * *'),
    ('treasury-audit', 'Treasury Sovereignty Audit', 'Monthly financial sovereignty and asset allocation review', '0 0 1 * *'),
    ('sovereignty-bulletin', 'Sovereignty Status Bulletin', 'Daily operational independence status report', '0 12 * * *'),
    ('education-matrix', 'Educational Sovereignty Matrix', 'Weekly knowledge sovereignty and learning pathway updates', '0 0 * * 1')
ON CONFLICT (slug) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    schedule_cron = EXCLUDED.schedule_cron,
    updated_at = CURRENT_TIMESTAMP;

-- ============================================================================
-- CREATE VIEWS FOR OPERATIONAL SOVEREIGNTY MONITORING
-- ============================================================================

-- Active capsule summary view
CREATE OR REPLACE VIEW v_capsule_status AS
SELECT
    c.slug,
    c.name,
    c.schedule_cron,
    c.is_active,
    COUNT(cr.id) as total_runs,
    COUNT(CASE WHEN cr.status = 'success' THEN 1 END) as successful_runs,
    COUNT(CASE WHEN cr.status = 'failed' THEN 1 END) as failed_runs,
    ROUND(
        (COUNT(CASE WHEN cr.status = 'success' THEN 1 END) * 100.0 / NULLIF(COUNT(cr.id), 0)), 2
    ) as success_rate_percent,
    MAX(cr.timestamp) as last_run,
    AVG(cr.execution_time_ms) as avg_execution_time_ms
FROM capsules c
LEFT JOIN capsule_runs cr ON c.slug = cr.capsule_slug
WHERE c.is_active = true
GROUP BY c.slug, c.name, c.schedule_cron, c.is_active
ORDER BY c.slug;

-- Recent execution history view
CREATE OR REPLACE VIEW v_recent_executions AS
SELECT
    cr.capsule_slug,
    c.name as capsule_name,
    cr.status,
    cr.execution_time_ms,
    cr.timestamp,
    cr.execution_id,
    cr.archive_url,
    cr.error_message
FROM capsule_runs cr
JOIN capsules c ON cr.capsule_slug = c.slug
WHERE cr.timestamp >= (CURRENT_TIMESTAMP - INTERVAL '7 days')
ORDER BY cr.timestamp DESC;

-- ============================================================================
-- FUNCTIONS FOR OPERATIONAL SOVEREIGNTY
-- ============================================================================

-- Function to record capsule execution
CREATE OR REPLACE FUNCTION record_capsule_execution(
    p_capsule_slug VARCHAR(100),
    p_status VARCHAR(50),
    p_execution_time_ms INTEGER,
    p_archive_url TEXT DEFAULT NULL,
    p_triggered_by VARCHAR(100) DEFAULT 'scheduler',
    p_error_message TEXT DEFAULT NULL,
    p_artifact_checksum VARCHAR(64) DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    run_id INTEGER;
BEGIN
    INSERT INTO capsule_runs (
        capsule_slug,
        status,
        execution_time_ms,
        archive_url,
        triggered_by,
        error_message,
        artifact_checksum,
        timestamp
    ) VALUES (
        p_capsule_slug,
        p_status,
        p_execution_time_ms,
        p_archive_url,
        p_triggered_by,
        p_error_message,
        p_artifact_checksum,
        CURRENT_TIMESTAMP
    ) RETURNING id INTO run_id;

    RETURN run_id;
END;
$$ LANGUAGE plpgsql;

-- Function to get capsule statistics
CREATE OR REPLACE FUNCTION get_capsule_stats(p_capsule_slug VARCHAR(100) DEFAULT NULL)
RETURNS TABLE(
    capsule_slug VARCHAR(100),
    total_executions BIGINT,
    success_rate DECIMAL(5,2),
    avg_execution_time DECIMAL(10,2),
    last_execution TIMESTAMP WITH TIME ZONE,
    last_status VARCHAR(50)
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.slug,
        COUNT(cr.id) as total_executions,
        ROUND(
            (COUNT(CASE WHEN cr.status = 'success' THEN 1 END) * 100.0 / NULLIF(COUNT(cr.id), 0)), 2
        ) as success_rate,
        ROUND(AVG(cr.execution_time_ms), 2) as avg_execution_time,
        MAX(cr.timestamp) as last_execution,
        (SELECT status FROM capsule_runs WHERE capsule_slug = c.slug ORDER BY timestamp DESC LIMIT 1) as last_status
    FROM capsules c
    LEFT JOIN capsule_runs cr ON c.slug = cr.capsule_slug
    WHERE (p_capsule_slug IS NULL OR c.slug = p_capsule_slug)
    AND c.is_active = true
    GROUP BY c.slug
    ORDER BY c.slug;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- TRIGGERS FOR OPERATIONAL SOVEREIGNTY
-- ============================================================================

-- Trigger to update capsule updated_at timestamp
CREATE OR REPLACE FUNCTION update_capsule_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_capsules_updated_at
    BEFORE UPDATE ON capsules
    FOR EACH ROW
    EXECUTE FUNCTION update_capsule_timestamp();

-- ============================================================================
-- GRANTS FOR OPERATIONAL SOVEREIGNTY
-- ============================================================================

-- Grant permissions to codex_user
GRANT SELECT, INSERT, UPDATE, DELETE ON capsules TO codex_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON capsule_runs TO codex_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO codex_user;
GRANT SELECT ON v_capsule_status, v_recent_executions TO codex_user;
GRANT EXECUTE ON FUNCTION record_capsule_execution TO codex_user;
GRANT EXECUTE ON FUNCTION get_capsule_stats TO codex_user;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Verify table creation
SELECT
    table_name,
    table_type
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('capsules', 'capsule_runs');

-- Verify capsule insertion
SELECT slug, name, schedule_cron FROM capsules ORDER BY slug;

-- Show table structures
\d+ capsules
\d+ capsule_runs

-- ============================================================================
-- OPERATIONAL SOVEREIGNTY ESTABLISHED
-- Database schema ready for autonomous capsule execution tracking
-- ============================================================================

-- Sample test execution (remove in production)
SELECT record_capsule_execution(
    'signals-daily',
    'success',
    1234,
    'gs://codex-artifacts-codex-dominion-prod/signals/test.json',
    'manual',
    NULL,
    'abc123def456'
);

-- Display current status
SELECT * FROM v_capsule_status;

COMMIT;
