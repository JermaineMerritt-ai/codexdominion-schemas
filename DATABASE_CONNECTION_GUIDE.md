# Codex Dominion Database Connection Guide

# ========================================

## Method 1: Using Cloud Console (Easiest)

1. Go to: https://console.cloud.google.com/sql/instances/codex-ledger/overview?project=codex-dominion-prod
1. Click "Connect using Cloud Shell"
1. When prompted, use: `codex_user` as username
1. Copy and paste the migration_scroll.sql content

## Method 2: Using gcloud with psql (After installing PostgreSQL client)

```bash
# Connect to database
gcloud sql connect codex-ledger --user=codex_user

# Once connected, paste the migration script from migration_scroll.sql
```

## Method 3: Using Cloud SQL Auth Proxy (Alternative)

```bash
# Download and run Cloud SQL Auth Proxy
gcloud sql instances describe codex-ledger --format="value(connectionName)"
# Connection name: codex-dominion-prod:us-central1:codex-ledger

# Then use any PostgreSQL client to connect via proxy
```

## What the Migration Script Creates:

### Tables:

1. **capsules** - Master registry of operational capsules
   - Fields: id, slug, name, description, schedule_cron, created_at, updated_at, is_active, config
1. **capsule_runs** - Complete execution tracking
   - Fields: id, capsule_slug, status, execution_time_ms, archive_url, timestamp, execution_id, triggered_by, error_message, artifact_checksum, performance metrics, metadata

### Views:

1. **v_capsule_status** - Active capsule summary with success rates
1. **v_recent_executions** - Recent execution history (last 7 days)

### Functions:

1. **record_capsule_execution()** - Main function for your record_capsule_run() integration
1. **get_capsule_stats()** - Performance analytics

### Capsules Registered:

- signals-daily (Daily Market Signals Analysis) - 6 AM daily
- dawn-dispatch (Dawn Sovereignty Dispatch) - 6 AM daily
- treasury-audit (Treasury Sovereignty Audit) - 1st of month
- sovereignty-bulletin (Sovereignty Status Bulletin) - 12 PM daily
- education-matrix (Educational Sovereignty Matrix) - Weekly on Monday

## Connection Details:

- **Instance:** codex-ledger
- **Database:** codex
- **User:** codex_user
- **Connection:** codex-dominion-prod:us-central1:codex-ledger

## Next Steps:

1. Run the migration script via Cloud Console or psql
1. Update your record_capsule_run() function to use the PostgreSQL function
1. Enable smart archiver to use Cloud Storage
1. Test full end-to-end capsule execution with database tracking

## Verification Queries:

```sql
-- Check capsule registration
SELECT * FROM v_capsule_status;

-- View recent executions
SELECT * FROM v_recent_executions;

-- Test execution recording
SELECT record_capsule_execution('signals-daily', 'success', 1234, 'gs://test-url');
```
