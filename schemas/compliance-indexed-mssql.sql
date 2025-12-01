-- Create table for verified facts
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'verified_facts')
BEGIN
    CREATE TABLE verified_facts (
        id NVARCHAR(255) PRIMARY KEY,
        type NVARCHAR(255) NOT NULL,
        ticker NVARCHAR(255),
        value FLOAT NOT NULL,
        unit NVARCHAR(255),
        tolerance FLOAT NOT NULL,
        last_verified DATETIME2 NOT NULL,
        sources NVARCHAR(MAX) NOT NULL -- Use JSON string
    );
END

-- Create table for drift events
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'drift_events')
BEGIN
    CREATE TABLE drift_events (
        id INT IDENTITY(1,1) PRIMARY KEY,
        fact_id NVARCHAR(255) FOREIGN KEY REFERENCES verified_facts(id) ON DELETE CASCADE,
        old_value FLOAT,
        new_value FLOAT,
        detected_at DATETIME2 DEFAULT GETDATE(),
        sources NVARCHAR(MAX)
    );
END

-- Indexes for faster queries
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_verified_facts_ticker')
BEGIN
    CREATE INDEX idx_verified_facts_ticker ON verified_facts(ticker);
END
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_drift_events_fact_id')
BEGIN
    CREATE INDEX idx_drift_events_fact_id ON drift_events(fact_id);
END
