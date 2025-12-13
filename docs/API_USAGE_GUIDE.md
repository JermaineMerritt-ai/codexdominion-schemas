# Codex Dominion API Usage Guide

## Overview
The Codex Dominion API provides cryptographically sealed capsule archives with multi-format exports and role-based filtering.

## Base URL
```
Production: http://codex-api-eastus.eastus.azurecontainer.io:8000
Documentation: http://codex-api-eastus.eastus.azurecontainer.io:8000/docs
```

## Authentication
Currently public API. Future versions will implement API key authentication.

## Core Endpoints

### Health Check
```bash
GET /health
```
Returns system health status and version.

**Response:**
```json
{
  "status": "healthy",
  "service": "codex-dominion-api",
  "version": "1.0.3"
}
```

### Export Annotations
```bash
GET /api/annotations/export?format={format}&cycle={cycle}&role={role}&engine={engine}
```

**Parameters:**
- `format` (required): `yaml`, `markdown`, or `pdf`
- `cycle` (optional): `daily`, `seasonal`, `epochal`, `millennial`
- `role` (optional): `heir`, `council`, `custodian`, `observer`
- `engine` (optional): Filter by AI engine name

**Example:**
```bash
# Export YAML for daily heir capsules
curl "http://codex-api-eastus.eastus.azurecontainer.io:8000/api/annotations/export?format=yaml&cycle=daily&role=heir"

# Export PDF ledger
curl "http://codex-api-eastus.eastus.azurecontainer.io:8000/api/annotations/export?format=pdf" -o capsules.pdf

# Export Markdown scroll for council
curl "http://codex-api-eastus.eastus.azurecontainer.io:8000/api/annotations/export?format=markdown&role=council"
```

### Verify Seal
```bash
POST /api/seal/verify
```

**Request Body:**
```json
{
  "signatures": [
    {
      "name": "Signer Name",
      "seal_id": "custodian_abc123",
      "signature_hash": "..."
    }
  ],
  "content_hash": "sha256_hash",
  "timestamp": "2025-12-11T00:00:00Z"
}
```

## Export Formats

### YAML Archive
- Structured data format
- Includes cryptographic covenant
- Machine-readable
- Ideal for automation

### Markdown Scroll
- Human-readable ceremonial format
- Visual seals and dedication
- Formatted for documentation
- Ideal for reports

### PDF Ledger
- Sealed document format
- Cryptographic signatures
- Print-ready
- Ideal for compliance

## Cryptographic Seals

All exports include:
- **Content Hash**: SHA-256 of export content
- **Signatures**: RSA-2048-PSS-SHA256 signatures
- **Timestamp**: ISO 8601 UTC timestamp
- **Seal ID**: Unique identifier
- **Covenant Type**: Single or multi-signature

## Cycle Filters

| Cycle | Time Range |
|-------|------------|
| daily | Last 24 hours |
| seasonal | Last 90 days |
| epochal | Last 365 days |
| millennial | All time |

## Role Filters

- **heir**: Designated successors
- **council**: Decision-making body
- **custodian**: System administrators
- **observer**: Read-only access

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad request (invalid parameters) |
| 404 | Not found |
| 422 | Validation error |
| 500 | Server error |

## Rate Limiting
Not currently implemented. Future versions will have rate limiting.

## Caching
Responses are cached for 5 minutes via Redis. Subsequent identical requests within this window return cached data.

## Examples

### Python
```python
import requests

# Export YAML
response = requests.get(
    "http://codex-api-eastus.eastus.azurecontainer.io:8000/api/annotations/export",
    params={"format": "yaml", "cycle": "daily"}
)
archive = response.text

# Verify seal
seal_data = {
    "signatures": [...],
    "content_hash": "...",
    "timestamp": "2025-12-11T00:00:00Z"
}
verify = requests.post(
    "http://codex-api-eastus.eastus.azurecontainer.io:8000/api/seal/verify",
    json=seal_data
)
```

### PowerShell
```powershell
# Export PDF
Invoke-WebRequest `
    -Uri "http://codex-api-eastus.eastus.azurecontainer.io:8000/api/annotations/export?format=pdf" `
    -OutFile "capsules.pdf"

# Get health
$health = Invoke-RestMethod `
    -Uri "http://codex-api-eastus.eastus.azurecontainer.io:8000/health"
Write-Output $health
```

### cURL
```bash
# Export Markdown with filters
curl -X GET \
  "http://codex-api-eastus.eastus.azurecontainer.io:8000/api/annotations/export?format=markdown&role=heir&engine=gpt-4o" \
  -H "Accept: text/markdown"
```

## Support
For issues or questions, contact: jermainemerrittjr@gmail.com

## Version History
- **v1.0.3**: Redis caching, database integration
- **v1.0.2**: Database service implementation
- **v1.0.1**: Seal verification fixes
- **v1.0.0**: Initial release
