# Codex Capsules API

Operational sovereignty tracking for ceremonial and technical operations within the Codex Dominion system.

## Overview

The Codex Capsules API provides a comprehensive system for registering, tracking, and monitoring operational capsules - discrete units of work that represent both ceremonial and technical operations in the digital sovereignty ecosystem.

## Features

- **Capsule Registration**: Register and manage operational capsules with metadata
- **Run Tracking**: Record and monitor capsule executions
- **Performance Analytics**: Get insights into capsule success rates and execution patterns
- **Scheduling Support**: Track scheduled capsules and their next run times
- **Artifact Management**: Link executions to stored artifacts with checksums

## API Endpoints

### Core Operations

- `POST /api/capsules` - Register a new capsule
- `GET /api/capsules` - List all registered capsules
- `POST /api/capsules/run` - Record a capsule execution
- `GET /api/capsules/runs` - List all runs (with optional filtering)

### Analytics

- `GET /api/capsules/performance` - Get performance metrics
- `GET /api/capsules/scheduled` - Get scheduled capsules

### Health

- `GET /health` - Service health check

## Data Models

### Capsule

```json
{
  "slug": "dawn-dispatch-engine",
  "title": "Dawn Dispatch Engine",
  "kind": "engine",
  "mode": "automated",
  "version": "1.2.0",
  "status": "active",
  "entrypoint": "python codex_dawn_dispatch.py",
  "schedule": "0 6 * * *"
}
```

### Capsule Run

```json
{
  "capsule_slug": "dawn-dispatch-engine",
  "actor": "system-scheduler",
  "status": "success",
  "artifact_uri": "gs://codex-artifacts/dawn-dispatch-20241108.tar.gz",
  "checksum": "sha256:abc123def456..."
}
```

## Running Locally

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

1. **Set database URL**:

   ```bash
   export DATABASE_URL="postgresql://localhost:5432/codex_dominion"
   ```

1. **Run the service**:

   ```bash
   python main.py
   ```

1. **Test the API**:

   ```bash
   python test_api.py
   ```

The service will be available at `http://localhost:8080` with interactive docs at `/docs`.

## Deployment

### Local Development

```powershell
python main.py
```

### Cloud Run Deployment

```powershell
.\deploy.ps1 -ProjectId "your-project-id" -ServiceName "codex-capsules"
```

## Database Schema

The service integrates with the Codex Dominion database schema, specifically the `capsules` and `capsule_runs` tables. See `database_migration.sql` for the complete schema.

### Key Tables

- `capsules`: Core capsule definitions
- `capsule_runs`: Execution history and artifacts
- `capsule_performance`: Performance analytics view
- `scheduled_capsules`: Scheduling information view

## Integration

The Capsules API is designed to integrate with:

- **Dawn Dispatch System**: Automated ceremonial operations
- **Treasury System**: Financial sovereignty operations
- **Education System**: Knowledge dissemination operations
- **Trading Systems**: Market intelligence operations

## Security

- Database connections use connection pooling
- Input validation via Pydantic models
- Error handling prevents information leakage
- Health checks for monitoring

## Monitoring

- `/health` endpoint for health checks
- Performance metrics via `/api/capsules/performance`
- Structured logging for operations
- Database connection monitoring

## Development

### Adding New Capsule Types

1. Update the `kind` enum in the database schema
1. Add any specific validation logic in `api.py`
1. Update documentation and tests

### Custom Analytics

The performance views in the database can be extended for custom analytics:

```sql
-- Example: Success rate by capsule kind
SELECT kind, AVG(CASE WHEN status = 'success' THEN 1.0 ELSE 0.0 END) as success_rate
FROM capsule_performance
GROUP BY kind;
```

## License

Part of the Codex Dominion system - Digital Sovereignty Infrastructure.
